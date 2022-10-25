from fastapi import HTTPException, status
from jose import JWTError

from core.exception.base_exeption import UniqueIndexException, ForeignKeyErrorException


class NotUniqueIndex(HTTPException):
    """Обработчик ошибки занесения уникального значения."""

    def __init__(self, exc: UniqueIndexException):
        self.message = exc.message
        self.status_code = status.HTTP_409_CONFLICT
        super().__init__(detail={'message': self.message}, status_code=self.status_code)


class ForeignKeyError(HTTPException):
    """Обработчик ошибки занесения неверного внешнего ключа."""

    def __init__(self, exc: ForeignKeyErrorException):
        self.message = exc.message
        self.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        super().__init__(detail={'message': self.message}, status_code=self.status_code)


class TokenError(HTTPException):
    """Обработчик ошибки занесения уникального значения."""

    def __init__(self, exc: JWTError):
        jwt_error = str(exc)
        if jwt_error == 'Not enough segments':
            self.message = 'Incorrect token structure'
            self.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        elif jwt_error == 'Signature has expired.':
            self.message = 'token time is out'
            self.status_code = status.HTTP_408_REQUEST_TIMEOUT
        else:
            self.message = 'unknow token error'
            self.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        super().__init__(detail={'message': self.message}, status_code=self.status_code)
