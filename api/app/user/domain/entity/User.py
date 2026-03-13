from datetime import UTC, datetime
from typing import Self

from pydantic import BaseModel, ConfigDict
from ulid import ULID  # type: ignore

from core.auth.domain.enum import Role


class User(BaseModel):
    id: ULID
    username: str
    email: str
    password: str
    memo: str | None
    created_at: datetime
    updated_at: datetime
    role: Role

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @classmethod
    def create(
        cls,
        id: ULID,
        username: str,
        email: str,
        password: str,
        role: Role = Role.USER,
        memo: str | None = None,
    ) -> Self:
        """
        SignInUsecase 처럼 새 외부 세계로부터 User Domain 모델 만듦.
        영속성 계층에서 데이터를 불러올 때 사용하면 안됨.
        """

        return cls(
            id=id,
            username=username,
            email=email,
            password=password,
            memo=memo,
            created_at=datetime.now(tz=UTC),
            updated_at=datetime.now(tz=UTC),
            role=role,
        )
