from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from backend.core.database.driver import init_database_client
from backend.authentication.urls import app_authentication
from backend.core.middleware import authentication_middleware
from backend.tree.urls import app_tree

app = FastAPI(middleware=[Middleware(CORSMiddleware,  allow_origins=['*'], allow_methods=["*"], allow_headers=["*"]),
                          Middleware(BaseHTTPMiddleware, dispatch=authentication_middleware)])
app.mount('/authentication', app_authentication)
app.mount('/tree', app_tree)


@app.on_event("startup")
async def startup_event():
    init_database_client()
