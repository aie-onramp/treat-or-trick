"""Meta API endpoints for health checks and service information."""

from fastapi import APIRouter

router = APIRouter(tags=["meta"])


@router.get(
    "/",
    summary="Service health check",
    description="Returns a simple status message confirming that TreatOrHell is up.",
)
async def root() -> dict[str, str | list[str]]:
    """
    Health check endpoint.

    Returns:
        Dictionary with service information
    """
    return {
        "message": "TreatOrHell API",
        "docs": "/docs",
        "endpoints": ["/chat/angel"],
    }


