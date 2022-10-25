import uuid

from fastapi import FastAPI, Response, status
from jose import JWTError
from sqlmodel import select
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from authentication.config import registration_url_config, activate_url_config, \
    login_url_config, logout_url_config, refresh_url_config
from authentication.models import LoginUserSchema, UpdatePasswordSchema, RecoveryPasswordSchema, BaseRefreshToken
from authentication.functions import hash_password, create_registration_token, create_login_token, \
    new_refresh_token, get_refresh_cookies_age, update_refresh_token, create_password_recovery_token
from core.additional import decode_token
from core.config import recovery_link
from core.database.crud import Crud
from core.email.driver import mail
from core.exception.base_exeption import UniqueIndexException
from core.exception.http_exeption import TokenError, NotUniqueIndex
from core.middleware import error_handler_middleware
from user.models import UserSchemaCreate, UserDataBase

app_authentication = FastAPI(middleware=[Middleware(BaseHTTPMiddleware, dispatch=error_handler_middleware)])


@app_authentication.post('/registration', **registration_url_config.dict())
async def registration_user(user: UserSchemaCreate) -> uuid.UUID | Response:
    if len(user.password) < 8 or len(user.username) < 4:
        return Response(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    password = hash_password(user.password)
    try:
        new_user_id = await Crud.save(UserDataBase(username=user.username, password=password, email=user.email))
    except UniqueIndexException as e:
        raise NotUniqueIndex(e)
    try:
        registration_token = create_registration_token(new_user_id).replace('.', '|')
        mail.send_message(
            user.email,
            'Activate account FamilyTree',
            f"For account activating click the link <a href=\"{recovery_link}{registration_token}\">link</a>"
        )
        return new_user_id
    except Exception as e:
        new_user = await Crud.get(select(UserDataBase).where(UserDataBase.id == new_user_id))
        await Crud.delete(new_user)
        raise e


@app_authentication.put('/activate/{registration_token}', **activate_url_config.dict())
async def activate_user(registration_token: str) -> Response:
    try:
        user_data = decode_token(registration_token.replace('|', '.'))
    except JWTError as e:
        raise TokenError(e)
    user = await Crud.get(select(UserDataBase).where(UserDataBase.id == user_data['user_id']))
    if user:
        user.active = True
        await Crud.save(user)
        return Response(status_code=status.HTTP_201_CREATED)
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@app_authentication.post('/login', **login_url_config.dict())
async def login(user: LoginUserSchema, response: Response) -> Response | dict:
    user.password = hash_password(user.password)
    database_user: UserDataBase = await Crud.get(select(UserDataBase).where(UserDataBase.username == user.username))
    if database_user and database_user.password == user.password and database_user.active:
        access_token = create_login_token(database_user.id)
        refresh_token = await new_refresh_token(database_user.id)
        response.set_cookie(key='refresh_token', value=str(refresh_token), httponly=True, path='/',
                            max_age=get_refresh_cookies_age(90))
        response.status_code = status.HTTP_200_OK
        return {'access_token': access_token, 'time_out': decode_token(access_token)['exp']}
    else:
        return Response(status_code=status.HTTP_403_FORBIDDEN)


@app_authentication.get('/refresh', **refresh_url_config.dict())
async def refresh(request: Request, response: Response) -> Response | dict:
    refresh_token = request.cookies.get('refresh_token')
    if refresh_token:
        new_access_token = await update_refresh_token(refresh_token)
        if new_access_token:
            return {'access_token': new_access_token, 'time_out': decode_token(new_access_token)['exp']}
        else:
            response.delete_cookie(key='refresh_token', httponly=True, path='/')
            response.status_code = status.HTTP_403_FORBIDDEN
            return {}
    else:
        return Response(status_code=status.HTTP_403_FORBIDDEN)


@app_authentication.get('/logout', **logout_url_config.dict())
async def logout(request: Request, response: Response) -> Response | None:
    if not request.scope['user']:
        return Response(status_code=status.HTTP_403_FORBIDDEN)
    else:
        if request.cookies.get('refresh_token'):
            refresh_token_id = request.cookies['refresh_token']
            refresh_token = await Crud.get(select(BaseRefreshToken).
                                           where(BaseRefreshToken.id == refresh_token_id))
            if refresh_token:
                await Crud.delete(refresh_token)
            response.delete_cookie(key='refresh_token', httponly=True, path='/')
        response.status_code = status.HTTP_200_OK
        return


@app_authentication.post('/start_recovery_password')
async def start_recovery_password(data: RecoveryPasswordSchema) -> Response:
    data_base_user: UserDataBase = await Crud.get(select(UserDataBase).where(UserDataBase.email == data.email))
    if data_base_user:
        password_recovery_token = create_password_recovery_token(data_base_user.id).replace('.', '|')
        mail.send_message(
            data.email,
            'Recovery password',
            f"For change the password click the link <a href=\"{recovery_link}forgot/{password_recovery_token}\">link</a>"
        )
        return Response(status_code=status.HTTP_200_OK)
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@app_authentication.get('/check_recovery_password/{password_recovery_token}')
async def check_recovery_password(password_recovery_token: str) -> Response:
    try:
        user_data = decode_token(password_recovery_token.replace('|', '.'))
    except JWTError as e:
        raise TokenError(e)
    if user_data.get('recovery'):
        return Response(status_code=status.HTTP_200_OK)
    else:
        return Response(status_code=status.HTTP_403_FORBIDDEN)


@app_authentication.put('/recovery_password/{password_recovery_token}')
async def recovery_password(password_recovery_token: str, data: UpdatePasswordSchema) -> Response:
    try:
        user_data = decode_token(password_recovery_token.replace('|', '.'))
    except JWTError as e:
        raise TokenError(e)
    if user_data.get('recovery'):
        password = hash_password(data.password)
        user = await Crud.get(select(UserDataBase).where(UserDataBase.id == user_data['user_id']))
        if user:
            user.password = password
            await Crud.save(user)
            return Response(status_code=status.HTTP_200_OK)
        else:
            return Response(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        return Response(status_code=status.HTTP_403_FORBIDDEN)
