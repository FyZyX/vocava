import chromadb
from chromadb.utils import embedding_functions


class VectorStore:
    def __init__(self, cohere_api_key):
        self._cohere_api_key = cohere_api_key
        self._db = chromadb.Client()
        self._collection = None

    def connect(self):
        self._collection = self._db.get_or_create_collection(
            name="vocava",
            embedding_function=embedding_functions.CohereEmbeddingFunction(
                api_key=self._cohere_api_key,
                model_name="embed-multilingual-v2.0",
            ),
        )

    def save(self, ids, documents, metadata):
        self._collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadata,
        )
