from app.errors.base_error import ErrorBase
from fastapi import status


class KlassDoesNotExist(ErrorBase):
    detail = "The klass that you are trying to delete doesnt exist"
    status_code = status.HTTP_404_NOT_FOUND

