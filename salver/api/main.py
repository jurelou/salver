# -*- coding: utf-8 -*-
from salver.config import api_config
from fastapi import FastAPI
from salver.api.routes import router
from fastapi.middleware.cors import CORSMiddleware
from salver.api.routes.websockets import socket_app
from salver.api.routes.errors.http import http_error_handler
from salver.api.routes.errors.validation import http_422_error

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

def get_app() -> FastAPI:
    """Configure and returns a FastAPI application."""
    app = FastAPI(title=api_config.FASTAPI.APP_NAME, debug=api_config.FASTAPI.DEBUG)



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

    app.include_router(router, prefix=api_config.FASTAPI.API_PREFIX)

    app.mount('/websock', socket_app)
    return app

app = get_app()