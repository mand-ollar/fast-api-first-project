from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic_core import ValidationError as CoreValidationError
from sqlalchemy.orm import close_all_sessions

from app.auth.infrastructure.adapter.inbound.api import router as auth_router
from app.note.infrastructure.adapter.inbound.api import router as note_router
from app.user.infrastructure.adapter.inbound.api import router as user_router
from core.db.db import engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    # startup
    try:
        yield
    finally:
        # shutdown
        close_all_sessions()
        engine.dispose()


app: FastAPI = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth")
app.include_router(note_router, prefix="/note")
app.include_router(user_router, prefix="/user")


@app.exception_handler(RequestValidationError)
async def handle_request_validation_error(request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content=exc.errors(),
    )


@app.exception_handler(CoreValidationError)
async def handle_core_validation_error(request, exc: CoreValidationError):
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({"detail": exc.errors()}),
    )


if __name__ == "__main__":
    uvicorn.run(app="app.main:app", host="127.0.0.1", port=8000, reload=True)
