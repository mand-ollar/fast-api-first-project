from fastapi import Depends  # type: ignore

from app.di.domain import get_user_repository
from app.user.application.usecase import CreateUserUseCase, GetUsersUseCase, UpdateUserUseCase
from app.user.domain.repository import UserRepository


def get_create_user_usecase(user_repo: UserRepository = Depends(get_user_repository)) -> CreateUserUseCase:
    return CreateUserUseCase(user_repo=user_repo)


def get_update_user_usecase(user_repo: UserRepository = Depends(get_user_repository)) -> UpdateUserUseCase:
    return UpdateUserUseCase(user_repo=user_repo)


def get_get_users_usecase(user_repo: UserRepository = Depends(get_user_repository)) -> GetUsersUseCase:
    return GetUsersUseCase(user_repo=user_repo)
