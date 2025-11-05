from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
import logfire

from app.core.config import settings
from app.api.endpoints import router


logfire.configure(token=settings.LOGFIRE_WRITE_TOKEN)
logfire.instrument_pydantic()
logfire.instrument_pydantic_ai()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting Agentic RAG API...")
    yield
    # Shutdown
    print("👋 Shutting down Agentic RAG API...")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    app = FastAPI(
        title="Agentic RAG API",
        description="A research and writing agent system using DeepSeek and Pydantic AI",
        version="1.0.0",
        lifespan=lifespan,
        debug=settings.DEBUG,
    )

    # Include API routes
    app.include_router(router, prefix="/api/v1", tags=["agents"])

    # Root endpoint
    @app.get("/", response_model=dict)
    async def root():
        return {
            "message": "Agentic RAG API is running!",
            "version": "1.0.0",
            "docs": "/docs",
        }

    return app


app = create_app()


def start():
    """Start the FastAPI server"""
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
    )


if __name__ == "__main__":
    start()
