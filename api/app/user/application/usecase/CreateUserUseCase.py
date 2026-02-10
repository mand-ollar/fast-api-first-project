from datetime import datetime

from fastapi import HTTPException  # type: ignore
from ulid import ULID  # type: ignore

from app.user.domain.entity import User
from app.user.domain.exception import UserNotFound
from app.user.domain.repository.UserRepository import UserRepository
from core.util import BcryptPasswordHasher


class CreateUserUseCase:
    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo: UserRepository = user_repo
        self.ulid: ULID = ULID()
        self.password_hasher: BcryptPasswordHasher = BcryptPasswordHasher()

    def __call__(self, username: str, email: str, password: str, memo: str | None = None) -> User:
        _user: User
        try:
            _user = self.user_repo.get_by_email(email)
        except UserNotFound:
            pass
        else:
            raise HTTPException(status_code=422, detail="User already exists")

        now: datetime = datetime.now()
        user: User = User(
            id=self.ulid,
            username=username,
            email=email,
            password=self.password_hasher.hash(password),
            memo=memo,
            created_at=now,
            updated_at=now,
        )
        self.user_repo.save(user)

        return user
