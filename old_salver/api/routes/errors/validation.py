# -*- coding: utf-8 -*-
from typing import Union

from pydantic import ValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi.openapi.utils import validation_error_response_definition
from fastapi.openapi.constants import REF_PREFIX


async def http_422_error(
    _: Request,
    exc: Union[RequestValidationError, ValidationError],
) -> JSONResponse:
    """Intercept 422 errors (UNPROCESSABLE_ENTITY)."""
    return JSONResponse(
        {'errors': exc.errors()},
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
    )


validation_error_response_definition['properties'] = {
    'errors': {
        'title': 'Errors',
        'type': 'array',
        'items': {'$ref': '{}ValidationError'.format(REF_PREFIX)},
    },
}
