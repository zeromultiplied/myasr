from abc import ABC, abstractmethod
from collections.abc import AsyncIterator


class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, system_prompt: str, user_text: str) -> str:
        """Generate a complete response."""

    @abstractmethod
    async def generate_stream(self, system_prompt: str, user_text: str) -> AsyncIterator[str]:
        """Yield response text chunks as they arrive."""
