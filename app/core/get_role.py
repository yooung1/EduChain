from fastapi import Depends
from app.db.database import get_db
from app.models.user_model import User
from sqlalchemy.orm import Session


class CheckRole:
    
    def __get_user_role(user: User, db: Session = Depends(get_db)):
        user_role = db.get(User).filter(user.role).firts()

        return user_role


    def verify_role(permited_role, user_role: str = Depends(__get_user_role)) -> bool:
        return True if permited_role == user_role else False