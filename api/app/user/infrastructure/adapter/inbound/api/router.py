from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from ulid import ULID  # type: ignore

from app.di.application import (
    get_create_user_usecase,
    get_delete_user_usecase,
    get_get_users_usecase,
    get_update_user_usecase,
)
from app.user.application.command import UpdateUserCommand
from app.user.application.usecase import CreateUserUseCase, DeleteUserUseCase, GetUsersUseCase, UpdateUserUseCase
from app.user.domain.entity import User
from app.user.infrastructure.adapter.inbound.api.message import (
    CreateUserRequest,
    CreateUserResponse,
    GetUserResponse,
    GetUsersResponse,
    PatchUserRequest,
    PatchUserResponse,
)

router: APIRouter = APIRouter(tags=["Users"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=CreateUserResponse)
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

    return CreateUserResponse.from_model(user)


@router.patch("/{user_id}", response_model=PatchUserResponse)
def patch_user(
    user_id: ULID,
    request_model: PatchUserRequest,
    usecase: Annotated[UpdateUserUseCase, Depends(get_update_user_usecase)],
):
    cmd: UpdateUserCommand = UpdateUserCommand(
        user_id=user_id, new_username=request_model.username, new_password=request_model.password
    )

    try:
        updated: User = usecase(cmd=cmd)
        return PatchUserResponse(username=updated.username, password=updated.password)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("", response_model=GetUsersResponse)
def get_users(
    usecase: Annotated[GetUsersUseCase, Depends(get_get_users_usecase)], page: int = 1, items_per_page: int = 10
):
    total_cnt, users = usecase(page=page, items_per_page=items_per_page)
    return GetUsersResponse(
        total_cnt=total_cnt,
        page=page,
        users=[GetUserResponse.from_model(user) for user in users],
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: ULID,
    usecase: Annotated[DeleteUserUseCase, Depends(get_delete_user_usecase)],
):
    try:
        usecase(user_id=user_id)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
