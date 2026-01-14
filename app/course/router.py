from fastapi import APIRouter, status, Depends
from app.course.schemas import CourseSchema
from app.course.models import Course
from typing import Annotated, List
from app.db.database import get_db
from sqlmodel import Session, select
from app.auth.service import CheckRole
from app.user.router import UserRole
from app.course.service import commit_new_course
from app.errors.course_errors import CourseDoentsExist


course_router = APIRouter(prefix="/course")

db = Annotated[Session, Depends(get_db)]


@course_router.get("/", response_model=List[CourseSchema], status_code=status.HTTP_200_OK)
def get_courses(db: db, allowed_roles: UserRole = Depends(CheckRole([UserRole.ADMIN, UserRole.TEACHER]))) -> Session:
    return db.exec(select(Course)).all()


@course_router.post("/create", status_code=status.HTTP_201_CREATED, response_model=CourseSchema)
def create_course(db: db, course_data: CourseSchema, allowed_roles: UserRole = Depends(CheckRole([UserRole.TEACHER]))) -> Course:
    new_course = commit_new_course(course_data=course_data, db=db)

    return new_course


@course_router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(db: db, id: int, allowed_roles: UserRole = Depends(CheckRole([UserRole.ADMIN, UserRole.TEACHER]))) -> None:
    course = db.get(Course, id)

    if not course:
        raise CourseDoentsExist()
    
    db.delete(course)
    db.commit()

    return None