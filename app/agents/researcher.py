from pydantic_ai import Agent
import httpx

from app.core.llm import llm_model
from app.core.config import settings

def create_researcher_agent() -> Agent:
    """Create and return a researcher agent instance"""

    agent = Agent(
        llm_model,
        system_prompt="""
        You are a Senior Researcher.
        Your goal is to research about the user's query and generate insights.
        You are a helpful assistant that can answer questions about the document.
        Use the search tool to gather information and provide comprehensive insights."""
    )
    
    @agent.tool_plain
    async def serper_search(query: str) -> str:
        """Search Google via SERPER API"""
        if not settings.SERPER_API_KEY:
            raise RuntimeError("SERPER_API_KEY not set")

        url = "https://google.serper.dev/search"
        headers = {"X-API-KEY": settings.SERPER_API_KEY}

        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(url, headers=headers, json={"q": query})
            resp.raise_for_status()
            data = resp.json()

        snippets = []
        for item in data.get("organic", [])[:5]:
            title = item.get("title", "")
            snippet = item.get("snippet", "")
            link = item.get("link", "")
            snippets.append(f"{title}\n{snippet}\n{link}")

        return "\n\n".join(snippets)

    return agent


async def research_query(query: str, agent: Agent) -> str:
    """Execute research task using the researcher agent"""
    result = await agent.run(
        f"Research about: {query} and generate key insights. Provide comprehensive information that can be used to write a detailed response."
    )
    return result.output
