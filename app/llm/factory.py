from app.config import settings
from app.llm.anthropic_provider import AnthropicProvider
from app.llm.base import LLMProvider
from app.llm.ollama_provider import OllamaProvider
from app.llm.openai_provider import OpenAIProvider


def get_llm_provider(provider_name: str = None, model: str = None) -> LLMProvider:
    name = provider_name or settings.default_llm_provider
    if name == "openai":
        return OpenAIProvider(model)
    elif name == "anthropic":
        return AnthropicProvider(model)
    elif name == "ollama":
        return OllamaProvider(model)
    else:
        raise ValueError(f"Unknown LLM provider: {name}")
