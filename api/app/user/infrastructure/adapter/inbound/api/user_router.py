from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException  # type: ignore
from ulid import ULID  # type: ignore

from app.di.application import get_create_user_usecase, get_get_users_usecase, get_update_user_usecase
from app.user.application.command import UpdateUserCommand
from app.user.application.usecase import CreateUserUseCase, GetUsersUseCase, UpdateUserUseCase
from app.user.domain.entity import User
from app.user.infrastructure.adapter.inbound.api.message import (
    CreateUserRequest,
    GetUserResponse,
    UpdateUserRequest,
    UpdateUserResponse,
)

router: APIRouter = APIRouter(tags=["Users"])


@router.post("", status_code=201)
def create_user(
    request_model: CreateUserRequest,
    usecase: Annotated[CreateUserUseCase, Depends(get_create_user_usecase)],
):
    user: User = usecase(
        username=request_model.username,
        email=request_model.email,
        password=request_model.password,
        memo=request_model.memo,
    )

    return user


@router.put("/{user_id}", response_model=UpdateUserResponse)
def update_user(
    user_id: ULID,
    request_model: UpdateUserRequest,
    usecase: Annotated[UpdateUserUseCase, Depends(get_update_user_usecase)],
):
    cmd: UpdateUserCommand = UpdateUserCommand(
        user_id=user_id, new_username=request_model.username, new_password=request_model.password
    )

    try:
        updated: User = usecase(cmd=cmd)
        return UpdateUserResponse(username=updated.username, password=updated.password)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("", response_model=list[GetUserResponse])
def get_users(usecase: Annotated[GetUsersUseCase, Depends(get_get_users_usecase)]):
    return [GetUserResponse.from_model(user) for user in usecase()]
