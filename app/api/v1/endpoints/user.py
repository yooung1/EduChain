from fastapi import Depends, status, APIRouter
from app.db.database import engine, get_db
from app.models.user_model import User
from app.schemas import user_schema
from typing import List, Annotated
from app.core.security import get_password_hash, CheckRole
from app.errors.user_errors import (
    UsernameOrEmailExist
)
from sqlmodel import select, Session, SQLModel
from app.enums.user_enum import UserRole



SQLModel.metadata.create_all(engine)

router = APIRouter(prefix="/users", tags=["Users"])
db = Annotated[Session, Depends(get_db)]


@router.get("/", response_model=List[user_schema.UserPublic], status_code=status.HTTP_200_OK)
def get_users(db: db, allowed_roles: UserRole = Depends(CheckRole([UserRole.ADMIN]))) -> Session:
    return db.exec(select(User)).all()


@router.post("/create/student/", response_model=user_schema.UserPublic, status_code=status.HTTP_201_CREATED)
def create_student(user: user_schema.UserCreate, db: db) -> User:
    statement = select(User).where((User.email == user.email) | (User.username == user.username))
    db_user = db.exec(statement).first()
    
    if db_user:
        raise UsernameOrEmailExist()

    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        role=UserRole.STUDENT,
        hashed_password=get_password_hash(password=user.password), 
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/create/teacher", status_code=status.HTTP_201_CREATED, response_model=user_schema.UserPublic)
def create_teacher(user: user_schema.UserCreate, db: db, allowed_roles: User = Depends(CheckRole([UserRole.ADMIN]))):
    statement = select(User).where((User.email == user.email) | (User.username == user.username))
    db_user = db.exec(statement).first()

    if db_user:
        raise UsernameOrEmailExist()

    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        role=UserRole.TEACHER,
        hashed_password=get_password_hash(password=user.password), 
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/create/admin", status_code=status.HTTP_201_CREATED, response_model=user_schema.UserPublic)
def create_admin(user: user_schema.UserCreate, db: db, allowed_roles: User = Depends(CheckRole([UserRole.ADMIN]))):
    statement = select(User).where((User.email == user.email) | (User.username == user.username))
    db_user = db.exec(statement).first()

    if db_user:
        raise UsernameOrEmailExist()
    
    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        role=UserRole.ADMIN,
        hashed_password=get_password_hash(password=user.password), 
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user