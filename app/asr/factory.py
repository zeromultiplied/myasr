from app.asr.base import ASRProvider
from app.asr.xfyun import XfyunASRProvider


def get_asr_provider(provider_name: str = "xfyun") -> ASRProvider:
    if provider_name == "xfyun":
        return XfyunASRProvider()
    raise ValueError(f"Unknown ASR provider: {provider_name}")
