from fastapi import FastAPI
from app.global_endpoints_assembly import api_router
from sqlmodel import SQLModel
from app.db.database import engine
from contextlib import asynccontextmanager
from app.course.models import Course
from app.klass.models import Klass


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    
    yield

app = FastAPI(title="EduChain API", lifespan=lifespan)


app.include_router(api_router, prefix="/api/v1")
