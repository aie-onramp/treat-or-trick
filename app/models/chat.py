"""Chat-related Pydantic models."""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request model for chat endpoints."""

    message: str = Field(..., description="The message to send to the AI persona", min_length=1)


class ChatResponse(BaseModel):
    """Response model for chat endpoints."""

    response: str = Field(..., description="The AI persona's response message")


