from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.user.models import User
from app.auth.service import verify_password, create_access_token, oauth2_scheme
from app.errors.login_errors import UserOrPasswordIncorrect
from typing import Annotated
from sqlmodel import select


auth_router = APIRouter(prefix="/auth", tags=["Auth"])
db = Annotated[Session, Depends(get_db)]


@auth_router.post("/login", status_code=status.HTTP_202_ACCEPTED)
def login(db: db, form_data: OAuth2PasswordRequestForm = Depends()) -> dict[str, str]:
    statement = select(User).where(User.username == form_data.username)
    user = db.exec(statement).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise UserOrPasswordIncorrect()

    access_token = create_access_token(data={"sub": user.username, "role": user.role})

    return {"access_token": access_token, "token_type": "bearer"}