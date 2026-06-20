from pydantic import BaseModel
from typing import List

# Input Validation
class QueryRequest(BaseModel):
    query: str

# Output Validation for /ask
class AskResponse(BaseModel):
    answer: str
    sources: List[str]
    latency_seconds: float

# Output Validation for /analytics
class TopQuery(BaseModel):
    query: str
    count: int

class AnalyticsResponse(BaseModel):
    average_latency_seconds: float
    unanswered_queries_count: int
    top_queries: List[TopQuery]