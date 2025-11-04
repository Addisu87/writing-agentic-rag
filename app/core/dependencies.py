from fastapi import Depends
from pydantic_ai import Agent

from .agents.researcher import create_researcher_agent
from .agents.writer import create_writer_agent

async def get_researcher_agent() -> Agent:
    """Dependency that provides a researcher agent instance"""
    return create_researcher_agent()

async def get_writer_agent() -> Agent:
    """Dependency that provides a writer agent instance"""
    return create_writer_agent()