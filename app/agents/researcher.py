from pydantic_ai import Agent,WebSearchTool

from ..config.settings import settings
from ..core.llm import llm_model

def create_researcher_agent() -> Agent:
    """Create and return a researcher agent instance"""
    search_tool = WebSearchTool(
        api_key=settings.serper_api_key,
        provider='serper'
    )
    
    return Agent(
        llm_model,
        system_prompt="""
        You are a Senior Researcher.
        Your goal is to research about the user's query and generate insights.
        You are a helpful assistant that can answer questions about the document.
        Use the search tool to gather information and provide comprehensive insights.""",
        tools=[search_tool]
    )

async def research_query(query: str, agent: Agent) -> str:
    """Execute research task using the researcher agent"""
    result = await agent.run(
        f'Research about: {query} and generate key insights. Provide comprehensive information that can be used to write a detailed response.'
    )
    return result.data