"""Application configuration using Pydantic Settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with validation."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # OpenAI Configuration
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    openai_max_tokens: int = 1000
    openai_temperature: float = 0.7

    # Application Configuration
    debug: bool = False
    log_level: str = "INFO"

    # API Configuration
    api_title: str = "TreatOrHell"
    api_version: str = "0.1.0"
    api_description: str = (
        "TreatOrHell – a playful API where celestial beings judge CVs. "
        "Provides chat-style endpoints for 'angel' feedback on candidate profiles."
    )

    # Upstash Redis Configuration (for Vercel deployment)
    # Supports both KV_REST_API_* and UPSTASH_KV_REST_API_* naming conventions
    kv_rest_api_url: str | None = None
    kv_rest_api_token: str | None = None
    kv_rest_api_read_only_token: str | None = None
    # Vercel/Upstash uses UPSTASH_ prefix
    upstash_kv_rest_api_url: str | None = None
    upstash_kv_rest_api_token: str | None = None
    upstash_kv_rest_api_read_only_token: str | None = None

    @property
    def redis_url(self) -> str | None:
        """Get Redis URL, preferring UPSTASH_ prefix if available."""
        return self.upstash_kv_rest_api_url or self.kv_rest_api_url

    @property
    def redis_token(self) -> str | None:
        """Get Redis token, preferring UPSTASH_ prefix if available."""
        return self.upstash_kv_rest_api_token or self.kv_rest_api_token


settings = Settings()


