import os
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Cookie, Depends, HTTPException, Response, status
from ulid import ULID  # type: ignore

from app.auth.application.usecase import (
    ChangeRoleUseCase,
    RefreshCredentialsUseCase,
    SignInUseCase,
    SignOutUseCase,
    SignUpUseCase,
    VerifyCredentialsUseCase,
    VerifyPasswordUseCase,
)
from app.auth.infrastructure.adapter.inbound.api.message import (
    ChangeRoleRequest,
    ChangeRoleResponse,
    SignInRequest,
    SignInResponse,
    SignOutResponse,
    SignUpRequest,
    SignUpResponse,
    VerifyPasswordRequest,
    VerifyTokenResponse,
)
from app.di.application.usecase import (
    get_change_role_usecase,
    get_refresh_credentials_usecase,
    get_sign_in_usecase,
    get_sign_out_usecase,
    get_sign_up_usecase,
    get_verify_credentials_usecase,
    get_verify_password_usecase,
)
from app.di.core.notifier import get_email_notifier
from app.user.domain.entity import User
from core.auth.domain.exception import (
    DuplicatedPrincipal,
    InvalidCredentials,
    InvalidPrincipal,
)
from core.notifier import EmailNotifier

ACCESS_TOKEN_EXPIRE_DAYS: int = int(os.getenv("AUTH_TOKEN_LIFE_DAY", "1825"))
REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("AUTH_TOKEN_LIFE_DAY", "1825"))

router: APIRouter = APIRouter(tags=["Auth"])


@router.post("/signin", response_model=SignInResponse)
def sign_in(
    request_model: SignInRequest,
    response: Response,
    usecase: Annotated[SignInUseCase, Depends(get_sign_in_usecase)],
):
    try:
        user, short_creds, long_creds = usecase(
            request_model.username,
            request_model.password,
        )

        # set refresh_token cookie
        max_age_refresh_sec = REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
        response.set_cookie(
            key="refresh_token",
            value=long_creds.raw_value,
            httponly=True,
            max_age=max_age_refresh_sec,
            expires=max_age_refresh_sec,
        )

        # set access_token cookie
        max_age_access_sec = ACCESS_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
        response.set_cookie(
            key="access_token",
            value=short_creds.raw_value,
            httponly=True,
            max_age=max_age_access_sec,
            expires=max_age_access_sec,
        )

        return SignInResponse(
            username=user.username,
        )

    except InvalidPrincipal as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidCredentials as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/signup", response_model=SignUpResponse, status_code=status.HTTP_201_CREATED)
def sign_up(
    request_model: SignUpRequest,
    background_tasks: BackgroundTasks,
    email_notifier: Annotated[EmailNotifier, Depends(get_email_notifier)],
    response: Response,
    usecase: SignUpUseCase = Depends(get_sign_up_usecase),
):
    try:
        user, short_creds, long_creds = usecase(
            request_model.username,
            request_model.email,
            request_model.password,
            request_model.memo,
            request_model.role,
        )

        max_age_refresh: int = REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
        response.set_cookie(
            key="refresh_token",
            value=long_creds.raw_value,
            httponly=True,
            max_age=max_age_refresh,
            expires=max_age_refresh,
        )

        max_age_access: int = ACCESS_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
        response.set_cookie(
            key="access_token",
            value=short_creds.raw_value,
            httponly=True,
            max_age=max_age_access,
            expires=max_age_access,
        )

        background_tasks.add_task(
            email_notifier.notify,
            receiver=user,
            subject="Welcome to the platform",
            body=(
                f"Hello, {user.username}!\n\n"
                "We are so glad to have you on board.\n"
                "We hope you enjoy your time here.\n\n"
                "Best regards,\nTeam Daniel"
            ),
        )

        return SignUpResponse(
            username=user.username,
        )
    except DuplicatedPrincipal as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.post("/signout", response_model=SignOutResponse)
def sign_out(
    response: Response,
    access_token: str | None = Cookie(None),
    refresh_token: str | None = Cookie(None),
    usecase: SignOutUseCase = Depends(get_sign_out_usecase),
):
    try:
        user: User = usecase(
            raw_short_lived_confidential=access_token or "",  # if access_token is not provided, empty string is passed
            raw_long_lived_confidential=refresh_token,
        )
        response.delete_cookie(key="refresh_token", path="/")
        response.delete_cookie(key="access_token", path="/")

        return SignOutResponse(username=user.username)

    except InvalidPrincipal as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidCredentials as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.get("/verify", response_model=VerifyTokenResponse)
def verify_token(
    access_token: str | None = Cookie(None),
    usecase: VerifyCredentialsUseCase = Depends(get_verify_credentials_usecase),
):
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing access token")

    try:
        user: User = usecase(access_token)
        return VerifyTokenResponse(
            username=user.username,
        )
    except InvalidPrincipal as e:
        # token refers to non-existent user
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidCredentials as e:
        # token is malformed or expired
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/refresh", status_code=status.HTTP_200_OK)
def reissue_tokens(
    response: Response,
    refresh_token: str | None = Cookie(None),
    usecase: RefreshCredentialsUseCase = Depends(get_refresh_credentials_usecase),
):
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing refresh token")

    try:
        short_creds, long_creds = usecase(refresh_token)

        # set refresh_token cookie
        max_age_refresh: int = REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
        response.set_cookie(
            key="refresh_token",
            value=long_creds.raw_value,
            httponly=True,
            max_age=max_age_refresh,
            expires=max_age_refresh,
        )

        # set access_token cookie
        max_age_access: int = ACCESS_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
        response.set_cookie(
            key="access_token",
            value=short_creds.raw_value,
            httponly=True,
            max_age=max_age_access,
            expires=max_age_access,
        )

    except InvalidCredentials as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/password", status_code=status.HTTP_200_OK)
def verify_password(
    request: VerifyPasswordRequest,
    verify_password: VerifyPasswordUseCase = Depends(get_verify_password_usecase),
):
    if not verify_password(principal_str=request.principal_str, password=request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")


@router.patch("/change-role/{user_id}", response_model=ChangeRoleResponse, status_code=status.HTTP_200_OK)
def change_role(
    user_id: ULID,
    request: ChangeRoleRequest,
    change_role: ChangeRoleUseCase = Depends(get_change_role_usecase),
):
    _, principal = change_role(user_id=user_id, role=request.role)

    return ChangeRoleResponse(username=principal.principal)
