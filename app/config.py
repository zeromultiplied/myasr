from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ASR: iFlytek
    xfyun_app_id: str = ""
    xfyun_secret_key: str = ""

    # LLM: default provider
    default_llm_provider: str = "openai"

    # LLM: OpenAI
    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-4o"

    # LLM: Anthropic
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-sonnet-4-20250514"

    # LLM: Ollama
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3"

    # JWT
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440

    # App
    log_level: str = "INFO"
    max_audio_size_mb: int = 500
    asr_poll_interval_sec: int = 3
    asr_poll_timeout_sec: int = 120

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
