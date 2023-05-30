import chromadb
from chromadb.utils import embedding_functions


class VectorStore:
    def __init__(self, cohere_api_key):
        self._cohere_api_key = cohere_api_key
        self._db = chromadb.Client()
        embed = chromadb.utils.embedding_functions.CohereEmbeddingFunction
        self._embedding_function = embed(
            api_key=self._cohere_api_key,
            model_name="embed-multilingual-v2.0",
        )
        self._collection: chromadb.api.Collection | None = None

    def connect(self):
        self._collection = self._db.get_or_create_collection(
            name="vocava",
            embedding_function=self._embedding_function,
        )

    def save_interaction(self, interaction) -> bool:
        if not self._collection:
            return False

        self._collection.add(
            ids=interaction.ids(),
            documents=interaction.documents(),
            metadatas=interaction.metadata(),
        )
        return True
