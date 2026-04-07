from abc import ABC, abstractmethod


class ASRProvider(ABC):
    @abstractmethod
    async def transcribe(self, audio_data: bytes, filename: str) -> str:
        """Transcribe audio bytes to text."""
