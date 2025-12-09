"""Main API router that includes all version routers."""

from fastapi import APIRouter

from app.api.v1 import chat, meta

api_router = APIRouter()

api_router.include_router(meta.router)
api_router.include_router(chat.router)


