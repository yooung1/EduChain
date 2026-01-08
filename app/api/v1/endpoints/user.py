from fastapi import Depends, status, APIRouter
from sqlalchemy.orm import Session
from app.db.database import engine, get_db
from app.models.user_model import User
from app.schemas import user_schema
from typing import List, Annotated
from app.db.database import Base
from app.core.security import get_password_hash
from app.errors.user_errors import (
    UsernameOrEmailExist
)


Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/users", tags=["Users"])
db = Annotated[Session, Depends(get_db)]


@router.get("/", response_model=List[user_schema.UserPublic], status_code=status.HTTP_200_OK)
def get_users(db: db) -> Session:
    return db.query(User).all()


@router.post("/create/student/", response_model=user_schema.UserPublic, status_code=status.HTTP_201_CREATED)
def create_student(user: user_schema.Student, db: db) -> User:
    db_user = db.query(User).filter(
        (User.email == user.email) | (User.username == user.username)
    ).first()
    
    
    if db_user:
        raise UsernameOrEmailExist()

    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(password=user.password), 
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user) # Pega o ID gerado pelo banco

    return new_user


@router.post("/create/teacher", status_code=status.HTTP_201_CREATED, response_model=user_schema.UserPublic)
def create_teacher(user: user_schema.Teacher, db: db):
    db_user = db.query(User).filter(
        (User.email == user.email) | (User.username == user.username)
    ).first()

    if db_user:
        raise UsernameOrEmailExist()

