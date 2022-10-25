import uuid
from typing import List

from fastapi import FastAPI, Response, status
from sqlmodel import select
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware

from core.database.crud import Crud
from core.exception.base_exeption import UniqueIndexException
from core.exception.http_exeption import NotUniqueIndex
from user.config import get_users_url_config, get_user_url_config, create_user_url_config, \
    update_user_url_config, delete_user_url_config
from user.models import UserSchemaGet, UserSchemaCreate, UserDataBase, UpdateUserSchema
from authentication.functions import hash_password
from core.middleware import error_handler_middleware

app_user = FastAPI(middleware=[Middleware(BaseHTTPMiddleware, dispatch=error_handler_middleware)])


@app_user.get('/{user_id}', **get_user_url_config.dict())
async def get_user(user_id: str) -> UserSchemaGet | Response:
    user = await Crud.get(select(UserDataBase).where(UserDataBase.id == user_id))
    if user:
        return user
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@app_user.get('/', **get_users_url_config.dict())
async def get_users() -> List[UserSchemaGet]:
    users = await Crud.get_all(select(UserDataBase))
    return users


@app_user.post('/', **create_user_url_config.dict())
async def create_user(user: UserSchemaCreate) -> uuid.UUID | Response:
    if len(user.password) < 8 or len(user.username) < 4:
        return Response(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    password = hash_password(user.password)
    try:
        new_user = await Crud.save(UserDataBase(username=user.username, password=password, email=user.email))
    except UniqueIndexException as e:
        raise NotUniqueIndex(e)
    else:
        return new_user


@app_user.put('/{user_id}', **update_user_url_config.dict())
async def update_user(user_id: str, user: UpdateUserSchema) -> uuid.UUID | Response:
    database_user: UserDataBase = await Crud.get(select(UserDataBase).where(UserDataBase.id == user_id))
    if database_user:
        data_to_update = user.dict(exclude_unset=True)
        for key, value in data_to_update.items():
            setattr(database_user, key, value)
        try:
            return await Crud.save(database_user)
        except UniqueIndexException as e:
            raise NotUniqueIndex(e)
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@app_user.delete('/{user_id}', **delete_user_url_config.dict())
async def delete_user(user_id: str) -> Response:
    database_user: UserDataBase = await Crud.get(select(UserDataBase).where(UserDataBase.id == user_id))
    if database_user:
        await Crud.delete(database_user)
        return Response(status_code=status.HTTP_200_OK)
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
