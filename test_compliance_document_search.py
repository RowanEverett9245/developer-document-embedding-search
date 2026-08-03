import unittest

from compliance_document_search import IndexedDocument, cosine_similarity, search_documents


class FakeEmbeddings:
    def create(self, *, model: str, input: list[str]):
        self.last_model = model
        self.last_input = input
        vectors = [[1.0, 0.0] if "embedding" in text else [0.0, 1.0] for text in input]
        return type("Response", (), {"data": [type("Item", (), {"embedding": vector}) for vector in vectors]})


class FakeClient:
    def __init__(self) -> None:
        self.embeddings = FakeEmbeddings()


class ComplianceDocumentSearchTest(unittest.TestCase):
    def test_search_places_embedding_document_first(self) -> None:
        client = FakeClient()
        index = [
            IndexedDocument("Embedding search", "embedding lookup", [1.0, 0.0]),
            IndexedDocument("Release review", "approval record", [0.0, 1.0]),
        ]

        results = search_documents(client, index, "embedding query", limit=1)

        self.assertEqual(results[0][0].title, "Embedding search")
        self.assertEqual(client.embeddings.last_model, "auto")
        self.assertEqual(cosine_similarity([1.0, 0.0], [1.0, 0.0]), 1.0)


if __name__ == "__main__":
    unittest.main()
