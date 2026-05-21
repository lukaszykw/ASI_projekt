from fastapi import APIRouter

from app.api.routes import health, space

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(space.router, prefix="/space", tags=["space"])
