from fastapi import APIRouter

from app.api.api_v1.endpoints import lectures, users, login, uploads

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(lectures.router, prefix="/lectures", tags=["lectures"])
api_router.include_router(login.router, tags=["login"])
api_router.include_router(uploads.router, tags=["upload"])
