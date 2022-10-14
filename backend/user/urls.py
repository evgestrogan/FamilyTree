from typing import List

from fastapi import FastAPI, Response, status, Depends
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware

from user.config import get_users_url_config, get_user_url_config, create_user_url_config, \
    update_user_url_config, delete_user_url_config
from user.crud import UserCrud
from user.dependence import user_crud
from user.schemas import UserSchemaGet, UserSchemaCreate, UpdateUserSchema
from authentication.functions import hash_password
from core.exception.base_exeption import UniqueIndexException
from core.exception.http_exeption import NotUniqueIndex
from core.middleware import error_handler_middleware

app_user = FastAPI(middleware=[Middleware(BaseHTTPMiddleware, dispatch=error_handler_middleware)])


@app_user.get('/{user_id}', **get_user_url_config.dict())
async def get_user(user_id: str, crud: UserCrud = Depends(user_crud)) -> UserSchemaGet | Response:
    user = await crud.get(user_id)
    if user:
        return UserSchemaGet(**user)
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@app_user.get('/', **get_users_url_config.dict())
async def get_users(crud: UserCrud = Depends(user_crud)) -> List[UserSchemaGet]:
    users = await crud.get_all()
    return [UserSchemaGet(**user) for user in users]


@app_user.post('/', **create_user_url_config.dict())
async def create_user(user: UserSchemaCreate, crud: UserCrud = Depends(user_crud)) -> str | Response:
    try:
        if len(user.password) < 8 or len(user.username) < 4:
            return Response(status_code=status.HTTP_406_NOT_ACCEPTABLE)
        user.password = hash_password(user.password)
        new_user = await crud.create(user.dict())
        return new_user
    except UniqueIndexException as e:
        raise NotUniqueIndex(e)


@app_user.put('/{user_id}', **update_user_url_config.dict())
async def update_user(user_id: str, user: UpdateUserSchema, crud: UserCrud = Depends(user_crud)) -> int | Response:
    user = {k: v for k, v in user.dict().items() if v is not None}  # Удаление ключей со значением Null
    try:
        update_count = await crud.update(user_id, user)
        if update_count:
            return update_count
        else:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    except UniqueIndexException as e:
        raise NotUniqueIndex(e)


@app_user.delete('/{user_id}', **delete_user_url_config.dict())
async def delete_user(user_id: str, crud: UserCrud = Depends(user_crud)) -> int | Response:
    delete_count = await crud.delete(user_id)
    if delete_count:
        return delete_count
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
