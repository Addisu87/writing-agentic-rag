from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    output: str
    research_insights: str

class HealthResponse(BaseModel):
    status: str
    version: str = "1.0.0"