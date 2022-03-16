from typing import List

from fastapi import FastAPI, Response, status, Depends
from jose import JWTError
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware

from backend.authentication.config import get_users_url_config, get_user_url_config, create_user_url_config, \
    update_user_url_config, delete_user_url_config, registration_user_url_config, activate_user_url_config, \
    login_user_url_config
from backend.authentication.crud import UserCrud
from backend.authentication.dependence import user_crud
from backend.authentication.schemas import UserSchemaGet, UserSchemaCreate, UpdateUserSchema, LoginUserSchema
from backend.authentication.functions import hash_password, create_registration_token
from backend.core.additional import decode_token
from backend.core.email.driver import mail
from backend.core.exception.base_exeption import UniqueIndexException
from backend.core.exception.http_exeption import NotUniqueIndex, TokenError
from backend.core.middleware import error_handler_middleware

app_authentication = FastAPI(middleware=[Middleware(BaseHTTPMiddleware, dispatch=error_handler_middleware)])


@app_authentication.get('/{user_id}', **get_user_url_config.dict())
async def get_user(user_id: str, crud: UserCrud = Depends(user_crud)) -> UserSchemaGet | Response:
    user = await crud.get(user_id)
    if user:
        return UserSchemaGet(**user)
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@app_authentication.get('/', **get_users_url_config.dict())
async def get_users(crud: UserCrud = Depends(user_crud)) -> List[UserSchemaGet]:
    users = await crud.get_all()
    return [UserSchemaGet(**user) for user in users]


@app_authentication.post('/', **create_user_url_config.dict())
async def create_user(user: UserSchemaCreate, crud: UserCrud = Depends(user_crud)) -> str:
    try:
        user.password = hash_password(user.password)
        new_user = await crud.create(user.dict())
        return new_user
    except UniqueIndexException as e:
        raise NotUniqueIndex(e)


@app_authentication.put('/{user_id}', **update_user_url_config.dict())
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


@app_authentication.delete('/{user_id}', **delete_user_url_config.dict())
async def delete_user(user_id: str, crud: UserCrud = Depends(user_crud)) -> int | Response:
    delete_count = await crud.delete(user_id)
    if delete_count:
        return delete_count
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@app_authentication.post('/registration', **registration_user_url_config.dict())
async def registration_user(user: UserSchemaCreate, crud: UserCrud = Depends(user_crud)) -> str:
    try:
        user.password = hash_password(user.password)
        new_user = await crud.create({**user.dict(), **{'active': False}})
        registration_token = create_registration_token(new_user)
        mail.send_message(user.email, f"Subject: Activate account FamilyTree\nGo to link '127.0.0.1/{registration_token}'")
        return new_user
    except UniqueIndexException as e:
        raise NotUniqueIndex(e)


@app_authentication.put('/activate/{registration_token}', **activate_user_url_config.dict())
async def activate_user(registration_token: str, crud: UserCrud = Depends(user_crud)):
    try:
        user_data = decode_token(registration_token)
        update_count = await crud.update(user_data['user_id'], {'active': True})
        if update_count:
            return update_count
        else:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    except JWTError as e:
        raise TokenError(e)


@app_authentication.post('/login', **login_user_url_config.dict())
async def login(user: LoginUserSchema, crud: UserCrud = Depends(user_crud)) -> Response:
    user.password = hash_password(user.password)
    data_base_user = await crud.find({'name': user.name})
    if data_base_user and data_base_user['password'] == user.password:
        return Response(status_code=status.HTTP_200_OK)
    else:
        return Response(status_code=status.HTTP_403_FORBIDDEN)

