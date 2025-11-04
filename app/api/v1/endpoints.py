from fastapi import APIRouter, Depends, HTTPException
from pydantic_ai import Agent

from ..models.schemas import QueryRequest, QueryResponse, HealthResponse
from ..dependencies import get_researcher_agent, get_writer_agent
from ..agents.researcher import research_query
from ..agents.writer import write_response

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
async def process_query(
    request: QueryRequest,
    researcher_agent: Agent = Depends(get_researcher_agent),
    writer_agent: Agent = Depends(get_writer_agent)
):
    """
    Process a query through the research and writing pipeline.
    
    - **query**: The question or topic to research and write about
    """
    try:
        # Run the research task
        research_insights = await research_query(request.query, researcher_agent)
        
        # Run the writing task with the research insights
        final_response = await write_response(research_insights, request.query, writer_agent)
        
        return QueryResponse(
            output=final_response,
            research_insights=research_insights
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing query: {str(e)}"
        )

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(status="healthy")