from app.user.schema import UserRole
from app.user.models import User
from sqlmodel import Session




def commit_new_user(user_role: UserRole, user: User, db: Session) -> User:
    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        role=user_role,
        hashed_password=get_password_hash(password=user.password), 
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

