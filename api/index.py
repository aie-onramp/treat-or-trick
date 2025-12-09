"""Vercel-compatible entry point that imports the refactored app."""

# Import the app from the new structure
from app.main import app

# Re-export for Vercel compatibility
__all__ = ["app"]

