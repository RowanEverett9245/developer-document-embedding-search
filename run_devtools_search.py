"""Run a small developer-tools document search from the command line."""

import sys

from compliance_document_search import index_documents, infrai_embeddings_client, search_documents


DOCUMENTS = [
    ("RAG quickstart", "Build retrieval augmented generation with chunked source documents."),
    ("Embedding search", "Create embeddings for documentation and rank results with cosine similarity."),
    ("Release checklist", "Review deployment approvals, audit evidence, and rollback ownership."),
]


def main() -> None:
    query = " ".join(sys.argv[1:]) or "devtools embeddings search"
    client = infrai_embeddings_client()
    index = index_documents(client, DOCUMENTS)
    for document, score in search_documents(client, index, query):
        print(f"{score:.3f}  {document.title}")


if __name__ == "__main__":
    main()
