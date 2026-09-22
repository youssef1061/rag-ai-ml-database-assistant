from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=1000, description="Question to answer from the document corpus")

class QueryResponse(BaseModel):
    answer: str
    sources: list[str]
