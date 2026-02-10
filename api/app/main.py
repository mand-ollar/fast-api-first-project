import uvicorn
from fastapi import FastAPI  # type: ignore
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.user.infrastructure.adapter.inbound.api import router as user_router

app: FastAPI = FastAPI()

app.include_router(user_router, prefix="/users")


@app.exception_handler(RequestValidationError)
async def handle_request_validation_error(request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content=exc.errors(),
    )


if __name__ == "__main__":
    uvicorn.run(app="app.main:app", host="127.0.0.1", port=8000, reload=True)
