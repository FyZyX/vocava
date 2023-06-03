import uuid

import chromadb
from chromadb.utils import embedding_functions


class Document:
    def __init__(self, content: str, metadata: dict):
        self._id = str(uuid.uuid4())
        self._content = content
        self._metadata = metadata

    def id(self):
        return self._id

    def content(self):
        return self._content

    def metadata(self):
        return self._metadata


class VectorStore:
    def __init__(self, cohere_api_key):
        self._cohere_api_key = cohere_api_key
        self._db = chromadb.Client()
        self._embedding_function = embedding_functions.CohereEmbeddingFunction(
            api_key=self._cohere_api_key,
            model_name="embed-multilingual-v2.0",
        )
        self._collection: chromadb.api.Collection | None = None

    def connect(self):
        self._collection = self._db.get_or_create_collection(
            name="vocava",
            embedding_function=self._embedding_function,
        )

    def save(self, *documents: Document) -> bool:
        if not self._collection:
            raise ValueError("Must call connect before querying.")

        self._collection.add(
            ids=[doc.id() for doc in documents],
            documents=[doc.content() for doc in documents],
            metadatas=[doc.metadata() for doc in documents],
        )
        self._db.persist()
        return True
