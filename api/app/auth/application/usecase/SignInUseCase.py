from app.user.domain.entity import User
from app.user.domain.repository import UserRepository
from core.auth.domain.service import AuthenticationService
from core.auth.domain.valueobject import Credentials


class SignInUseCase:
    def __init__(self, auth_service: AuthenticationService, user_repo: UserRepository) -> None:
        self.auth_service: AuthenticationService = auth_service
        self.user_repo: UserRepository = user_repo

    def __call__(self, username: str, password: str) -> tuple[User, Credentials, Credentials]:
        short_creds, long_creds = self.auth_service.authenticate(principal_str=username, secret=password)
        user: User = self.user_repo.get_by_id(id=short_creds.user_id)

        return user, short_creds, long_creds
