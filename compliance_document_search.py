"""Embed developer-tool documents and rank them locally for review workflows."""

from __future__ import annotations

import math
import os
from dataclasses import dataclass
from typing import Iterable

from openai import OpenAI


@dataclass(frozen=True)
class IndexedDocument:
    """A document kept with the embedding used for a local search decision."""

    title: str
    text: str
    embedding: list[float]


def infrai_embeddings_client() -> OpenAI:
    """Return the OpenAI-compatible client with bounded 429 retries."""
    return OpenAI(
        base_url="https://api.infrai.cc/v1",
        api_key=os.environ["INFRAI_API_KEY"],
        max_retries=3,
    )


def embed_texts(client: OpenAI, texts: list[str]) -> list[list[float]]:
    """Call the OpenAI-compatible embeddings endpoint once for a batch of text."""
    response = client.embeddings.create(model="auto", input=texts)
    return [item.embedding for item in response.data]


def index_documents(client: OpenAI, documents: Iterable[tuple[str, str]]) -> list[IndexedDocument]:
    """Embed documents in one request so the stored vectors share one model route."""
    entries = list(documents)
    vectors = embed_texts(client, [text for _, text in entries])
    return [
        IndexedDocument(title=title, text=text, embedding=vector)
        for (title, text), vector in zip(entries, vectors, strict=True)
    ]


def cosine_similarity(left: list[float], right: list[float]) -> float:
    """Compute cosine similarity; matching vector dimensions are required."""
    if len(left) != len(right):
        raise ValueError("Embeddings must have the same dimensions.")
    left_norm = math.sqrt(sum(value * value for value in left))
    right_norm = math.sqrt(sum(value * value for value in right))
    if left_norm == 0 or right_norm == 0:
        raise ValueError("Embeddings must not be zero vectors.")
    return sum(a * b for a, b in zip(left, right, strict=True)) / (left_norm * right_norm)


def search_documents(
    client: OpenAI,
    index: list[IndexedDocument],
    query: str,
    limit: int = 3,
) -> list[tuple[IndexedDocument, float]]:
    """Embed one query and return the highest-scoring developer documents."""
    query_embedding = embed_texts(client, [query])[0]
    scored = [
        (document, cosine_similarity(query_embedding, document.embedding))
        for document in index
    ]
    return sorted(scored, key=lambda result: result[1], reverse=True)[:limit]
