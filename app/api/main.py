from fastapi import FastAPI
from app.database.database import create_db_and_tables
from contextlib import asynccontextmanager
# from app.core.security import RoleChecker
from app.api import users



@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()

    yield



app = FastAPI(lifespan=lifespan)

app.include_router(users.router, prefix="/v1", tags=["Users"])