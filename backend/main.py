from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from authentication.urls import app_authentication
from core.config import origins
from core.middleware import authentication_middleware, log_middleware
from tree.urls import app_tree
from user.urls import app_user


app = FastAPI(middleware=[
    Middleware(CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"], allow_credentials=True),
    Middleware(BaseHTTPMiddleware, dispatch=authentication_middleware),
    Middleware(BaseHTTPMiddleware, dispatch=log_middleware),
])

app.mount('/authentication', app_authentication)
app.mount('/user', app_user)
app.mount('/tree', app_tree)
