from app.course.models import Course
from app.course.schemas import CourseSchema
from sqlmodel import Session


def commit_new_course(course_data:CourseSchema, db: Session) -> Course:
    new_course = Course(
        name=course_data.name,
        description=course_data.description
    )

    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return new_course

