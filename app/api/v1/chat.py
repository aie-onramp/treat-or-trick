"""Chat API endpoints."""

import structlog
from fastapi import APIRouter, HTTPException, status
from openai import APIError, RateLimitError

from app.models.chat import ChatRequest, ChatResponse
from app.models.errors import ErrorResponse
from app.services.ai_service import ai_service

logger = structlog.get_logger()
router = APIRouter(prefix="/chat", tags=["chat", "angel-review"])


@router.post(
    "/angel",
    summary="Ask the Angel for CV feedback",
    description=(
        "Send a message to the Angel reviewer (e.g. candidate CV text or summary). "
        "The Angel responds with constructive, kind feedback."
    ),
    response_model=ChatResponse,
    responses={
        200: {
            "description": "Successful response from the Angel",
            "model": ChatResponse,
        },
        400: {
            "description": "Bad request - invalid input",
            "model": ErrorResponse,
        },
        429: {
            "description": "Rate limit exceeded",
            "model": ErrorResponse,
        },
        500: {
            "description": "Internal server error",
            "model": ErrorResponse,
        },
        503: {
            "description": "Service unavailable - OpenAI API error",
            "model": ErrorResponse,
        },
    },
    status_code=status.HTTP_200_OK,
)
async def chat_angel(request: ChatRequest) -> ChatResponse:
    """
    Get feedback from the Angel persona.

    Args:
        request: Chat request with user message

    Returns:
        ChatResponse with Angel's response

    Raises:
        HTTPException: For various error conditions
    """
    log = logger.bind(endpoint="/chat/angel", message_length=len(request.message))

    log.info("chat_angel_request_received")

    try:
        response_text, token_usage = await ai_service.get_angel_response(request.message)

        log.info(
            "chat_angel_request_completed",
            tokens=token_usage,
            response_length=len(response_text),
        )

        return ChatResponse(response=response_text)

    except RateLimitError as e:
        log.warning("chat_angel_rate_limit_exceeded", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later.",
        )
    except APIError as e:
        log.error("chat_angel_api_error", error=str(e), error_type=type(e).__name__)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"OpenAI API error: {str(e)}",
        )
    except ValueError as e:
        log.warning("chat_angel_validation_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        log.exception("chat_angel_unexpected_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again later.",
        )


