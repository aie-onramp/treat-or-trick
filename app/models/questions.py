"""Questions-related Pydantic models."""

from pydantic import BaseModel, Field


class QuestionsRequest(BaseModel):
    """Request model for submitting student questions."""

    q1: str = Field(
        ...,
        description="How did you handle your first assignment in this course?",
        min_length=1,
    )
    q2: str = Field(
        ...,
        description="When you didn't understand something, what did you do?",
        min_length=1,
    )
    q3: str = Field(
        ...,
        description="How do you engage in class?",
        min_length=1,
    )
    q4: str = Field(
        ...,
        description="How many hours did you spend on the assignment?",
        min_length=1,
    )


class QuestionsResponse(BaseModel):
    """Response model for questions submission."""

    status: str = Field(default="success", description="Status of the operation")
    message: str = Field(..., description="Response message")

