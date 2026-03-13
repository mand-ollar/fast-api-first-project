from core.auth.domain.entity import Principal
from core.auth.domain.repository import PrincipalRepository
from core.auth.infrastructure.service import BcryptPasswordHasher


class VerifyPasswordUseCase:
    def __init__(self, principal_repo: PrincipalRepository, password_hasher: BcryptPasswordHasher) -> None:
        self.principal_repo: PrincipalRepository = principal_repo
        self.password_hasher: BcryptPasswordHasher = password_hasher

    def __call__(self, principal_str: str, password: str) -> bool:
        principal: Principal = self.principal_repo.get_by_principal(principal=principal_str)
        return principal.verify_password(plain=password, hasher=self.password_hasher)
