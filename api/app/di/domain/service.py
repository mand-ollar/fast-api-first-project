from fastapi import Depends  # type: ignore

from app.di.domain.repository import get_credentials_repository, get_principal_repository
from core.auth.domain.repository import CredentialsRepository, PrincipalRepository
from core.auth.domain.service import AuthenticationService, PasswordHasher
from core.auth.infrastructure.service import BcryptPasswordHasher, JWTAuthenticationService


def get_password_hasher() -> PasswordHasher:
    return BcryptPasswordHasher()


def get_authentication_service(
    principal_repo: PrincipalRepository = Depends(get_principal_repository),
    credentials_repo: CredentialsRepository = Depends(get_credentials_repository),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
) -> AuthenticationService:
    return JWTAuthenticationService(
        principal_repo=principal_repo,
        password_hasher=password_hasher,
        credentials_repo=credentials_repo,
    )
