from typing import Annotated

from fastapi import APIRouter, Depends  # type: ignore
from sqlalchemy.orm import Session

from app.di.application import get_create_user_usecase
from app.user.application.usecase import CreateUserUseCase
from app.user.domain.entity import User
from app.user.infrastructure.adapter.inbound.api.message import CreateUserRequest
from core.db.db import get_db

router: APIRouter = APIRouter(tags=["Users"])

db: Session = next(get_db())


@router.post("", status_code=201)
def create_user(
    request_model: CreateUserRequest,
    usecase: Annotated[CreateUserUseCase, Depends(get_create_user_usecase)],
):
    user: User = usecase(
        username=request_model.username,
        email=request_model.email,
        password=request_model.password,
    )

    return user
