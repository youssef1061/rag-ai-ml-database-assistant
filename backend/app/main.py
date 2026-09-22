from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.query import router
from app.core.config import settings
from app.services.generation import GenerationService
from app.services.retrieval import RetrievalService
from app.utils.logging_config import configure_logging

class FakeRetrieval:
    def retrieve(self, question: str):
        return [{"text": "Artificial intelligence enables machines to perform tasks associated with human intelligence.", "metadata": {"source": "AI.txt", "chunk_id": 0}, "distance": 0.1}]

class FakeGeneration:
    def answer(self, question: str, chunks: list[dict]):
        return "Artificial intelligence enables machines to perform tasks associated with human intelligence."

def create_app(testing: bool = False) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if testing:
            app.state.retrieval = FakeRetrieval()
            app.state.generation = FakeGeneration()
        else:
            configure_logging()
            app.state.retrieval = RetrievalService(settings)
            app.state.generation = GenerationService(settings)
        yield

    app = FastAPI(title="AI, ML and Database RAG Assistant", version="1.0.0", lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.frontend_origin],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router)
    return app

app = create_app()
