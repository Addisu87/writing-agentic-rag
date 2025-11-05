from pydantic_ai import Agent, RunContext
from app.core.llm import llm_model
from app.core.config import settings
import httpx

# Create agent at module level
researcher_agent = Agent(
    llm_model,
    system_prompt="""
    You are a Senior Researcher.
    Your goal is to research about the user's query and generate insights.
    You are a helpful assistant that can answer questions about the document.
    Use the search tool to gather information and provide comprehensive insights."""
)

@researcher_agent.tool
async def serper_search(ctx: RunContext[None], query: str) -> str:
    """Search Google via SERPER API for current information"""
    if not settings.SERPER_API_KEY:
        raise RuntimeError("SERPER_API_KEY not set")

    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": settings.SERPER_API_KEY}

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(url, headers=headers, json={"q": query})
        resp.raise_for_status()
        data = resp.json()

    snippets = []
    for item in data.get("organic", [])[:5]:  # Limit to top 5 results
        title = item.get("title", "")
        snippet = item.get("snippet", "")
        link = item.get("link", "")
        snippets.append(f"Title: {title}\nSummary: {snippet}\nSource: {link}")

    return "\n\n".join(snippets) if snippets else "No results found"

# Factory function to provide the researcher agent
def create_researcher_agent() -> Agent:
    """Dependency that provides a researcher agent instance"""
    return researcher_agent


async def research_query(query: str, researcher_agent: Agent) -> str:
    """Execute research task using the researcher agent"""
    result = await researcher_agent.run(
        f"""Research about: {query} and generate key insights. 

        Please structure your response in markdown format with:
        # Main Title
        
        ## Key Findings
        - Bullet points
        - Key statistics
        
        ## Top Recommendations
        1. Numbered list
        2. With reasons
        
        ## Detailed Analysis
        ### Subsection 1
        Content here...
        
        ### Subsection 2  
        Content here...
        
        Use proper markdown formatting with headers, lists, and emphasis."""
    )
    return result.output