from sqlalchemy import Column, Integer, String, Enum as SqlEnum
from ..db.database import Base
from app.enums.user_enum import UserRole




class User(Base):
    __tablename__ = "users"

    id = Column(Integer, unique=True, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SqlEnum(UserRole), default=UserRole.STUDENT)