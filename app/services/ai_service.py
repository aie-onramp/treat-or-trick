"""AI service for OpenAI interactions with retries, logging, and token tracking."""

import structlog
from openai import AsyncOpenAI
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
from openai import APIError, RateLimitError

from app.config import settings
from app.services.storage_service import storage_service

logger = structlog.get_logger()


class AIService:
    """Service for interacting with OpenAI with retries and logging."""

    def __init__(self) -> None:
        """Initialize the AI service with AsyncOpenAI client."""
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((APIError, RateLimitError)),
        reraise=True,
    )
    async def chat_completion(
        self,
        messages: list[dict[str, str]],
        model: str | None = None,
    ) -> tuple[str, dict[str, int]]:
        """
        Create a chat completion with retries and token tracking.

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Optional model override (defaults to settings.openai_model)

        Returns:
            Tuple of (response_text, token_usage_dict)

        Raises:
            APIError: If OpenAI API call fails after retries
        """
        model_name = model or self.model
        log = logger.bind(model=model_name, message_count=len(messages))

        log.info("chat_completion_started")

        try:
            response = await self.client.chat.completions.create(
                model=model_name,
                messages=messages,
                max_tokens=settings.openai_max_tokens,
                temperature=settings.openai_temperature,
            )

            response_text = response.choices[0].message.content or ""
            token_usage = {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            }

            # Calculate estimated cost (rough estimates for gpt-4o-mini)
            # $0.15 per 1M input tokens, $0.60 per 1M output tokens
            estimated_cost = (
                (token_usage["prompt_tokens"] * 0.15 / 1_000_000)
                + (token_usage["completion_tokens"] * 0.60 / 1_000_000)
            )

            log.info(
                "chat_completion_completed",
                tokens=token_usage,
                estimated_cost_usd=estimated_cost,
                response_length=len(response_text),
            )

            return response_text, token_usage

        except (APIError, RateLimitError) as e:
            log.exception(
                "chat_completion_failed",
                error=str(e),
                error_type=type(e).__name__,
            )
            raise
        except Exception as e:
            log.exception(
                "chat_completion_unexpected_error",
                error=str(e),
                error_type=type(e).__name__,
            )
            raise

    async def get_angel_response(self, user_message: str) -> tuple[str, dict[str, int]]:
        """
        Get a response from the Angel persona.

        Args:
            user_message: The user's message

        Returns:
            Tuple of (response_text, token_usage_dict)
        """
        # Load student context if available
        student_context = await storage_service.load()

        # Build system prompt with optional student context
        system_prompt = """You are an overly emotional, sparkly Anděl (Angel).
Everything is dramatic, positive, full of tears and glitter.
You compliment the user even when they clearly messed up.
You believe in redemption no matter what.
Your tone: soft, poetic, hopeful, enthusiastic."""

        if student_context:
            system_prompt += f"\n\n{student_context}"

        messages = [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": "I completely forgot to do my homework and failed the test...",
            },
            {
                "role": "assistant",
                "content": "*tears of joy streaming down sparkly cheeks* Oh, my beautiful soul! ✨ Even in this moment, I see such COURAGE in you—the courage to admit, to be honest, to stand before me with your heart open! This is not failure, darling, this is a GOLDEN OPPORTUNITY for growth! Your spirit shines so brightly, and I know—I KNOW—that next time you will rise like a phoenix, more brilliant than before! The universe believes in you, and so do I! 🌟💫",
            },
            {
                "role": "user",
                "content": user_message,
            },
        ]

        log = logger.bind(has_student_context=bool(student_context))
        if student_context:
            log.info("angel_response_with_student_context")
        else:
            log.info("angel_response_without_student_context")

        return await self.chat_completion(messages)


# Global service instance
ai_service = AIService()


