# -*- coding: utf-8 -*-
from app.config import settings
from fastapi import FastAPI
from app.api import router
from fastapi.middleware.cors import CORSMiddleware
from app.websockets import socket_app
from app.api.errors.http import http_error_handler
from app.api.errors.validation import http_422_error

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

def get_app() -> FastAPI:
    """Configure and returns a FastAPI application."""
    app = FastAPI(title=settings.FASTAPI.APP_NAME, debug=settings.FASTAPI.DEBUG)



    origins = [
        "http://localhost:8181"
    ]


    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # app.add_event_handler("startup", start_app_handler(app))
    # app.add_event_handler("shutdown", stop_app_handler(app))

    app.add_exception_handler(RequestValidationError, http_422_error)
    app.add_exception_handler(HTTPException, http_error_handler)

    app.include_router(router, prefix=settings.FASTAPI.API_PREFIX)

    app.mount('/websock', socket_app)
    return app

app = get_app()