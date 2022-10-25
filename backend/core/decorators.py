from functools import wraps

from fastapi import HTTPException, Depends
from starlette import status
from starlette.requests import Request


def get_user(request: Request):
    return request.scope['user']


def must_authentication(func):

    @wraps(func)
    async def wrap(user: str = Depends(get_user), *args, **kwargs):
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        else:
            return await func(*args, **kwargs)

    return wrap
