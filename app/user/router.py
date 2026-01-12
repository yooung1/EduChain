from fastapi import Depends, status, APIRouter
from app.db.database import engine, get_db
from app.user.models import User
from app.user.schemas import (
    UserCreate,
    UserPublic
)
from typing import List, Annotated
from app.auth.service import CheckRole
from app.errors.user_errors import (
    UsernameOrEmailExist
)
from sqlmodel import select, Session, SQLModel
from app.enums.user_enum import UserRole
from app.user.service import commit_new_user


SQLModel.metadata.create_all(engine)

user_router = APIRouter(prefix="/users", tags=["Users"])
db = Annotated[Session, Depends(get_db)]


@user_router.get("/", response_model=List[UserPublic], status_code=status.HTTP_200_OK)
# def get_users(db: db, allowed_roles: UserRole = Depends(CheckRole([UserRole.ADMIN]))) -> Session:
def get_users(db: db) -> Session:
    return db.exec(select(User)).all()


@user_router.post("/create/student/", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def create_student(user: UserCreate, db: db) -> User:
    statement = select(User).where((User.email == user.email) | (User.username == user.username))
    db_user = db.exec(statement).first()
    
    if db_user:
        raise UsernameOrEmailExist()

    new_user = commit_new_user(user_role=UserRole.STUDENT, user=user, db=db)

    return new_user


@user_router.post("/create/teacher", status_code=status.HTTP_201_CREATED, response_model=UserPublic)
def create_teacher(user: UserCreate, db: db, allowed_roles: User = Depends(CheckRole([UserRole.ADMIN]))):
    statement = select(User).where((User.email == user.email) | (User.username == user.username))
    db_user = db.exec(statement).first()

    if db_user:
        raise UsernameOrEmailExist()

    new_user = commit_new_user(user_role=UserRole.TEACHER, user=user, db=db)

    return new_user


@user_router.post("/create/admin", status_code=status.HTTP_201_CREATED, response_model=UserPublic)
def create_admin(user: UserCreate, db: db, allowed_roles: User = Depends(CheckRole([UserRole.ADMIN]))):
    statement = select(User).where((User.email == user.email) | (User.username == user.username))
    db_user = db.exec(statement).first()

    if db_user:
        raise UsernameOrEmailExist()
    
    new_user = commit_new_user(user_role=UserRole.ADMIN, user=user, db=db)

    return new_user
