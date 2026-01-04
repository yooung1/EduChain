from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session, select
from app.database.database import get_db
from app.models.user_registration_model import User
from app.schemas.user_registration_schema import UserPublic, UserCreate
from app.constants.user_registration_model_constants import UserRole

router = APIRouter()

@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    statement = select(User)

    users = db.exec(statement).all()

    return users

@router.get("/users/{user_id}", response_model=UserPublic)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario não encontrado")
    return user


@router.post("/create/user", response_model=UserPublic)
def user_registration(user_input: UserCreate, db: Session = Depends(get_db)):
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

