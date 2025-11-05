from pydantic_ai import Agent

from app.core.llm import llm_model


def create_writer_agent() -> Agent:
    """Create and return a writer agent instance"""
    return Agent(
        llm_model,
        system_prompt="""
        You are a Senior Writer.
        Your goal is to use the available insights to write a concise and informative response to the user's query.
        You are a helpful assistant that can write a report about the user's query.
        Take the research insights and transform them into a well-structured, informative response.""",
    )


async def write_response(research_insights: str, query: str, agent: Agent) -> str:
    """Execute writing task using the writer agent"""
    result = await agent.run(
        f"Using the following research insights, write a concise and informative response to the query: {query}\n\nResearch Insights:\n{research_insights}"
    )
    return result.output
