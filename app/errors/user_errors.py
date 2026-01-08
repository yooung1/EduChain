from app.errors.base_error import ErrorBase
from fastapi import status


class UsernameOrEmailExist(ErrorBase):
    detail = "The username or email already exists"
    status_code = status.HTTP_409_CONFLICT

