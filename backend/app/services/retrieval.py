from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer
from app.core.config import Settings

class RetrievalService:
    def __init__(self, settings: Settings):
        self.settings = settings
        if not settings.vector_store_path.exists():
            raise FileNotFoundError(
                f"Vector store was not found at {settings.vector_store_path}. Run notebooks/rag_pipeline.ipynb first."
            )
        self.model = SentenceTransformer(settings.embedding_model)
        self.client = chromadb.PersistentClient(path=str(settings.vector_store_path))
        self.collection = self.client.get_collection(settings.collection_name)

    def retrieve(self, question: str) -> list[dict]:
        query_embedding = self.model.encode(question, normalize_embeddings=True).tolist()
        count = self.collection.count()
        if count == 0:
            return []
        result = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(self.settings.top_k, count),
            include=["documents", "metadatas", "distances"],
        )
        documents = result["documents"][0]
        metadatas = result["metadatas"][0]
        distances = result["distances"][0]
        return [
            {"text": text, "metadata": metadata, "distance": distance}
            for text, metadata, distance in zip(documents, metadatas, distances)
        ]

    @staticmethod
    def source_label(metadata: dict) -> str:
        return f"{metadata.get('source', 'unknown')} — chunk {metadata.get('chunk_id', 'unknown')}"
