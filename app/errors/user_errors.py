from app.errors.base_error import ErrorBase
from fastapi import status


class UsernameOrEmailExist(ErrorBase):
    detail = "The username or email already exists"
    status_code = status.HTTP_409_CONFLICT


class UserDoesNotExist(ErrorBase):
    detail = "This User doesnt exist"
    status_code = status.HTTP_404_NOT_FOUND