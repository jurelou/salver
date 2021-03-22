from app.config import settings
from fastapi import FastAPI
from app.api import router
from fastapi.middleware.cors import CORSMiddleware

def get_app() -> FastAPI:
    """Configure and returns a FastAPI application."""
    app = FastAPI(
        title=settings.FASTAPI.APP_NAME, debug=settings.FASTAPI.DEBUG
    )

    # app.add_event_handler("startup", start_app_handler(app))
    # app.add_event_handler("shutdown", stop_app_handler(app))

    # app.add_exception_handler(RequestValidationError, http_422_error)
    # app.add_exception_handler(HTTPException, http_error_handler)

    app.include_router(router, prefix=settings.FASTAPI.API_PREFIX)
    origins = [
        "http://localhost",
        "https://localhost",
        "http://localhost:8080",
        "http://localhost:8000",
        "ws://localhost:8000",
        "ws://localhost:8080",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


app = get_app()