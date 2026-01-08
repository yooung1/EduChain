from app.api.v1.endpoints import user, login
from fastapi import APIRouter

api_router = APIRouter()



api_router.include_router(user.router)
api_router.include_router(login.router)