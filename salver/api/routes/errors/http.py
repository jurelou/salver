# -*- coding: utf-8 -*-
from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse


async def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    """Intercept all http errors."""
    return JSONResponse({"errors": [exc.detail]}, status_code=exc.status_code)
