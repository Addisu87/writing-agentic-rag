from pydantic_ai.models.openai import OpenAIResponsesModel
from pydantic_ai.providers.deepseek import DeepSeekProvider

from app.core.config import settings


def create_llm_model():
    """Create and return a reusable LLM model instance"""
    return OpenAIResponsesModel(
        "deepseek-v3",
        provider=DeepSeekProvider(
            api_key=settings.DEEPSEEK_API_KEY
        ),
    )


# Create a singleton instance to reuse across the application
llm_model = create_llm_model()
