import jwt
from app.user.models import User
from datetime import datetime, timedelta, timezone
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from app.db.database import get_db
from sqlalchemy.orm import Session
from typing import Annotated
from app.errors.credential_error import CredentialException, UserNotAllowed
from jose import JWTError, jwt
from sqlmodel import select
from app.enums.user_enum import UserRole



# TODO: ADD ISTO DAQUI NUM ARQUIVO .env DEPOIS
SECRET_KEY = "chave_super_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login") # procura o Token que veio da rota login
db = Annotated[Session, Depends(get_db)]


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return password_hash.verify(password, hashed)


def get_current_user(db: db, token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) #TODO: ALTERAR O SECRET KEY PARA O .env
        username: str = payload.get("sub")
        if username is None:
            raise CredentialException()
    except JWTError:
        raise CredentialException()
    
    statement = select(User).where(User.username == username)
    user = db.exec(statement).first()

    if user is None:
        raise CredentialException()
        
    return user



class CheckRole:
    def __init__(self, allowed_roles: list[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> bool:
        if current_user.role not in self.allowed_roles:
            raise UserNotAllowed()
        
        return True
    
