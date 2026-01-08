from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends
from app.db.database import get_db
import jwt
from app.core.security import SECRET_KEY, ALGORITHM
from app.models.user_model import User
from jose import JWTError
from app.errors.login_errors import CredentialException


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise CredentialException()
    except JWTError:
        raise CredentialException()
        
    user = db.query(User).filter(User.username == username).first()
    return user