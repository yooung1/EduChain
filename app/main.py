from fastapi import FastAPI
from app.api.v1.api import api_router
from sqlmodel import SQLModel
from app.db.database import engine
from contextlib import asynccontextmanager


app = FastAPI(title="EduChain API")

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    
    yield


app.include_router(api_router, prefix="/api/v1")
