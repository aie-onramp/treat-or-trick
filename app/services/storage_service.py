"""Storage service for student responses with support for file-based (local) and Redis (Vercel) storage."""

import json
import os
from pathlib import Path
from typing import Optional

import structlog
from upstash_redis import Redis

from app.config import settings
from app.models.questions import QuestionsRequest

logger = structlog.get_logger()

# Storage key for Redis
STUDENT_RESPONSES_KEY = "student_responses"

# Local file path
LOCAL_STORAGE_PATH = Path(__file__).parent.parent / "data" / "student_responses.txt"


class StorageService:
    """Service for storing and retrieving student responses.

    Supports both file-based storage (local development) and Redis storage (Vercel deployment).
    Automatically detects which storage method to use based on environment variables.
    """

    def __init__(self) -> None:
        """Initialize the storage service."""
        # Use the properties that handle both naming conventions
        redis_url = settings.redis_url
        redis_token = settings.redis_token
        self.use_redis = bool(redis_url and redis_token)
        self.redis_client: Redis | None = None

        if self.use_redis:
            try:
                self.redis_client = Redis(
                    url=redis_url,
                    token=redis_token,
                )
                logger.info("storage_service_initialized", method="redis", url=redis_url[:30] + "...")
            except Exception as e:
                logger.warning(
                    "redis_initialization_failed",
                    error=str(e),
                    falling_back_to_file=True,
                )
                self.use_redis = False
        else:
            logger.info("storage_service_initialized", method="file")

    async def save(self, questions: QuestionsRequest) -> None:
        """Save student responses to storage.

        Args:
            questions: The questions request with student responses

        Raises:
            Exception: If storage operation fails
        """
        data = {
            "q1": questions.q1,
            "q2": questions.q2,
            "q3": questions.q3,
            "q4": questions.q4,
        }

        if self.use_redis and self.redis_client:
            await self._save_to_redis(data)
        else:
            await self._save_to_file(data)

    async def load(self) -> Optional[str]:
        """Load student responses from storage.

        Returns:
            Formatted string with student context, or None if no responses exist
        """
        if self.use_redis and self.redis_client:
            data = await self._load_from_redis()
        else:
            data = await self._load_from_file()

        if not data:
            return None

        return self._format_context(data)

    async def _save_to_redis(self, data: dict[str, str]) -> None:
        """Save data to Redis.

        Args:
            data: Dictionary with question responses
        """
        if not self.redis_client:
            raise ValueError("Redis client not initialized")

        try:
            json_data = json.dumps(data)
            # upstash_redis.Redis is synchronous (no await needed)
            self.redis_client.set(STUDENT_RESPONSES_KEY, json_data)
            logger.info("student_responses_saved", method="redis", key=STUDENT_RESPONSES_KEY)
        except Exception as e:
            logger.exception("redis_save_failed", error=str(e))
            raise

    async def _load_from_redis(self) -> Optional[dict[str, str]]:
        """Load data from Redis.

        Returns:
            Dictionary with question responses, or None if not found
        """
        if not self.redis_client:
            return None

        try:
            # upstash_redis.Redis is synchronous (no await needed)
            json_data = self.redis_client.get(STUDENT_RESPONSES_KEY)
            if json_data is None:
                return None
            data = json.loads(json_data)
            logger.info("student_responses_loaded", method="redis", key=STUDENT_RESPONSES_KEY)
            return data
        except Exception as e:
            logger.warning("redis_load_failed", error=str(e))
            return None

    async def _save_to_file(self, data: dict[str, str]) -> None:
        """Save data to local file.

        Args:
            data: Dictionary with question responses
        """
        try:
            # Ensure data directory exists
            LOCAL_STORAGE_PATH.parent.mkdir(parents=True, exist_ok=True)

            # Write JSON to file
            with open(LOCAL_STORAGE_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

            logger.info("student_responses_saved", method="file", path=str(LOCAL_STORAGE_PATH))
        except Exception as e:
            logger.exception("file_save_failed", error=str(e), path=str(LOCAL_STORAGE_PATH))
            raise

    async def _load_from_file(self) -> Optional[dict[str, str]]:
        """Load data from local file.

        Returns:
            Dictionary with question responses, or None if file doesn't exist
        """
        try:
            if not LOCAL_STORAGE_PATH.exists():
                return None

            with open(LOCAL_STORAGE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)

            logger.info("student_responses_loaded", method="file", path=str(LOCAL_STORAGE_PATH))
            return data
        except Exception as e:
            logger.warning("file_load_failed", error=str(e), path=str(LOCAL_STORAGE_PATH))
            return None

    def _format_context(self, data: dict[str, str]) -> str:
        """Format student responses as context string for LLM prompt.

        Args:
            data: Dictionary with question responses

        Returns:
            Formatted string with student context
        """
        return f"""The student has shared the following information:
Q1: {data.get('q1', 'Not provided')}
Q2: {data.get('q2', 'Not provided')}
Q3: {data.get('q3', 'Not provided')}
Q4: {data.get('q4', 'Not provided')}

Use this information to personalize your responses and reference their behavior when appropriate."""


# Global service instance
storage_service = StorageService()

