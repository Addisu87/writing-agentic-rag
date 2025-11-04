from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

from .config.settings import settings
from .api.endpoints import router

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
        debug=settings.debug
    )
    
    # Include API routes
    app.include_router(router, prefix="/api/v1", tags=["agents"])
    
    # Root endpoint
    @app.get("/", response_model=dict)
    async def root():
        return {
            "message": "Agentic RAG API is running!",
            "version": "1.0.0",
            "docs": "/docs"
        }
    
    return app

app = create_app()

def start():
    """Start the FastAPI server"""
    uvicorn.run(
        "agentic_rag.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )

if __name__ == "__main__":
    start()