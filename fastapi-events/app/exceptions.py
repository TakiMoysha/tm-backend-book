from fastapi import status
from fastapi import HTTPException


class BaseAppException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Internal Server Error"
    headers = {"WWW-Authenticate": "Bearer"}

    def __init__(self, status_code=None, detail=None, headers=None):
        if status_code is not None:
            self.status_code = status_code
        if detail is not None:
            self.detail = detail
        if headers is not None:
            self.headers = headers

        super().__init__(
            status_code=self.status_code,
            detail=self.detail,
            headers=self.headers,
        )
