from ulid import ULID

from app.user.domain.entity import User
from app.user.domain.repository import UserRepository
from core.auth.domain.entity import Principal
from core.auth.domain.enum import Role
from core.auth.domain.exception import DuplicatedPrincipal
from core.auth.domain.repository import PrincipalRepository
from core.auth.domain.service import AuthenticationService, PasswordHasher
from core.auth.domain.valueobject import Credentials


class SignUpUseCase:
    def __init__(
        self,
        auth_service: AuthenticationService,
        password_hasher: PasswordHasher,
        principal_repo: PrincipalRepository,
        user_repo: UserRepository,
    ):
        self.auth_service: AuthenticationService = auth_service
        self.password_hasher: PasswordHasher = password_hasher
        self.principal_repo: PrincipalRepository = principal_repo
        self.user_repo: UserRepository = user_repo

    def __call__(
        self, username: str, email: str, password: str, memo: str | None = None, role: Role = Role.USER
    ) -> tuple[User, Credentials, Credentials]:
        username_exist: bool = self.principal_repo.exists(principal=username)
        if username_exist:
            raise DuplicatedPrincipal(f"username '{username}' already exists")

        password_hashed: str = self.password_hasher.hash(password)
        user_id: ULID = ULID()

        user: User = User.create(
            id=user_id,
            username=username,
            email=email,
            password=password_hashed,
            memo=memo,
        )
        saved_user: User = self.user_repo.save(user)

        principal: Principal = Principal(
            id=ULID(),
            user_id=user_id,
            principal=username,
            password_hashed=password_hashed,
            role=role,
        )
        self.principal_repo.add(principal)

        short_creds, long_creds = self.auth_service.authenticate(
            principal_str=username,
            secret=password,
        )

        return saved_user, short_creds, long_creds
