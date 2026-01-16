from app.auth.router import auth_router
from app.user.router import user_router
from app.course.router import course_router
from app.klass.router import klass_router
from fastapi import APIRouter

api_router = APIRouter()



api_router.include_router(user_router)
api_router.include_router(auth_router)
api_router.include_router(course_router)
api_router.include_router(klass_router)