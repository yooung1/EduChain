from app.errors.base_error import ErrorBase
from fastapi import status


class CourseDoentsExist(ErrorBase):
    detail = "The course that you are trying to delete doesnt exist"
    status_code = status.HTTP_404_NOT_FOUND

