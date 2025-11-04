from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.deepseek import DeepSeekProvider

from ..config.settings import settings

def create_llm_model():
    """Create and return a reusable LLM model instance"""
    return OpenAIChatModel(
        'deepseek-chat',
        provider=DeepSeekProvider(
            api_key=settings.deepseek_api_key,
            base_url="https://api.deepseek.com/v1"
        )  
    )

# Create a singleton instance to reuse across the application
llm_model = create_llm_model()