from app.errors.base_error import ErrorBase
from fastapi import status

class UserOrPasswordIncorrect(ErrorBase):
    detail = "Username or Password incorrect"
    status_code = status.HTTP_400_BAD_REQUEST


class CredentialException(ErrorBase):
    detail = "Could not validate credential"
    status_code = status.HTTP_401_UNAUTHORIZED
    headers = {"WWW-Authenticate": "Bearer"}