import ollama
from app.core.config import Settings

SYSTEM_PROMPT = """You are a grounded academic document assistant. Answer only from the supplied context.
If the context does not contain the answer, say exactly: I could not find this information in the provided documents.
Do not use outside knowledge. Be concise, accurate, and do not invent citations."""

class GenerationService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = ollama.Client(host=settings.ollama_host)

    def answer(self, question: str, retrieved_chunks: list[dict]) -> str:
        if not retrieved_chunks:
            return "I could not find this information in the provided documents."
        context = "\n\n".join(
            f"[Source: {chunk['metadata'].get('source')} | Chunk: {chunk['metadata'].get('chunk_id')}]\n{chunk['text']}"
            for chunk in retrieved_chunks
        )
        prompt = f"""Context:
{context}

Question: {question}

Answer using only the context."""
        response = self.client.chat(
            model=self.settings.ollama_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            options={"temperature": 0},
        )
        return response["message"]["content"].strip()
