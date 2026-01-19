from app.errors.base_error import ErrorBase
from fastapi import status

class CredentialException(ErrorBase):
    detail = "It's wat not possible to validate those credentials"
    status_code = status.HTTP_401_UNAUTHORIZED


class UserNotAllowed(ErrorBase):
    detail = "This user have no permission to execute this action"
    status_code = status.HTTP_401_UNAUTHORIZED