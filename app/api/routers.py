from fastapi import APIRouter

from app.api.endpoints import working_with_frontend

base_router = APIRouter()

base_router.include_router(
    working_with_frontend.router,
    prefix="/working-with-frontend",
    tags=["Working with Frontend", "Blog"],
)
