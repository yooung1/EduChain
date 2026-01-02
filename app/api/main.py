from fastapi import FastAPI, Depends
from app.schemas.user_registration_schema import UserPublic, UserCreate
from sqlmodel import Session
from app.database.database import get_db, create_db_and_tables
from app.models.user_registration_model import User
from app.constants.user_registration_model_constants import UserRole
from sqlmodel import select
from contextlib import asynccontextmanager




@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()

    yield



app = FastAPI(lifespan=lifespan)

@app.post("/create/user", response_model=UserPublic)
def create_user(user_input: UserCreate, db: Session = Depends(get_db)):
    fake_hashed_password = user_input.password + "notreallyhashed000111001101010"
    
    db_user = User(
        username=user_input.username,
        email=user_input.email,
        hashed_password=fake_hashed_password,
        user_type=UserRole.STUDENT
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    statement = select(User)
    
    users = db.exec(statement).all()
    
    return users