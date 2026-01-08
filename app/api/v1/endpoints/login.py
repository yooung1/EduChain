from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user_model import User
from app.core.security import verify_password, create_access_token
from app.errors.login_errors import UserOrPasswordIncorrect

router = APIRouter()

@router.post("/login", status_code=status.HTTP_202_ACCEPTED)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()

    print(user.hashed_password)
    print(form_data.password)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise UserOrPasswordIncorrect()

    access_token = create_access_token(data={"sub": user.username, "role": user.role})

    return {"access_token": access_token, "token_type": "bearer"}