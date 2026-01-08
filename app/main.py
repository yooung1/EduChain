from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine, get_db
from app.models.user_model import User
from app.db.database import Base
from app.schemas import user_schema
from typing import List
from app.errors.user_errors import (
    UsernameOrEmailExist,
    RoleDoesntExist
)
from app.enums.user_enum import UserRole

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/", response_model=List[user_schema.UserPublic], status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@app.post("/create/users/", response_model=user_schema.UserPublic, status_code=status.HTTP_201_CREATED)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db), ):
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
        hashed_password=user.password+"SENHA_HASHEADA_MUDAR_DEPOIS",
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user) # Pega o ID gerado pelo banco

    return new_user


