"""FastAPI application entry point."""

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.router import api_router
from app.config import settings
from app.models.errors import ErrorResponse

# Configure structlog
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer(),
    ],
)

logger = structlog.get_logger()

app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description=settings.api_description,
    contact={
        "name": "Don Branson",
        "url": "https://github.com/donbr",
        "email": "you@example.com",
    },
    servers=[
        {"url": "https://treat-or-trick.vercel.app", "description": "Production server"},
        {"url": "http://localhost:8000", "description": "Local dev server"},
    ],
    openapi_tags=[
        {
            "name": "meta",
            "description": "Meta endpoints for service health and information.",
        },
        {
            "name": "chat",
            "description": "Chat endpoints for interacting with AI personas.",
        },
        {
            "name": "angel-review",
            "description": "Endpoints for getting feedback from the Angel reviewer.",
        },
    ],
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local Next.js dev
        "https://treat-or-hell.vercel.app",  # Production frontend
        "https://*.vercel.app",  # Vercel preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router)


@app.exception_handler(Exception)
async def global_exception_handler(request, exc: Exception) -> JSONResponse:
    """
    Global exception handler for unhandled exceptions.

    Args:
        request: The request that caused the exception
        exc: The exception that was raised

    Returns:
        JSONResponse with error details
    """
    logger.exception(
        "unhandled_exception",
        path=request.url.path,
        method=request.method,
        error=str(exc),
        error_type=type(exc).__name__,
    )

    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail="An unexpected error occurred. Please try again later.",
        ).model_dump(),
    )


@app.on_event("startup")
async def startup_event() -> None:
    """Log application startup."""
    logger.info(
        "application_started",
        version=settings.api_version,
        debug=settings.debug,
        model=settings.openai_model,
    )


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Log application shutdown."""
    logger.info("application_shutdown")

