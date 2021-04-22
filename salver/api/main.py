# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware

from salver.config import api_config
from salver.api.routes import router
from salver.api.routes.websockets import socket_app
from salver.api.routes.errors.http import http_error_handler
from salver.api.routes.errors.validation import http_422_error


def get_app() -> FastAPI:
    """Configure and returns a FastAPI application."""
    new_app = FastAPI(title=api_config.FASTAPI.APP_NAME, debug=api_config.FASTAPI.DEBUG)

    origins = ['http://localhost:8181']

    new_app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    # app.add_event_handler("startup", start_app_handler(app))
    # app.add_event_handler("shutdown", stop_app_handler(app))

    new_app.add_exception_handler(RequestValidationError, http_422_error)
    new_app.add_exception_handler(HTTPException, http_error_handler)

    new_app.include_router(router, prefix=api_config.FASTAPI.API_PREFIX)

    new_app.mount('/websock', socket_app)
    return new_app


app = get_app()
