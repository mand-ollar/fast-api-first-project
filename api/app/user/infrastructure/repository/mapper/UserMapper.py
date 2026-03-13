from ulid import ULID  # type: ignore

from app.user.domain.entity import User
from app.user.infrastructure.repository.entity import UserAlchemyEntity


class UserMapper:
    @staticmethod
    def to_domain_entity(alchemy_entity: UserAlchemyEntity) -> User:
        return User(
            id=ULID.from_str(alchemy_entity.id),
            username=alchemy_entity.username,
            email=alchemy_entity.email,
            password=alchemy_entity.password,
            memo=alchemy_entity.memo,
            created_at=alchemy_entity.created_at,
            updated_at=alchemy_entity.updated_at,
            role=alchemy_entity.role,
        )

    @staticmethod
    def to_alchemy_entity(domain_entity: User) -> UserAlchemyEntity:
        return UserAlchemyEntity(
            id=str(domain_entity.id),
            username=domain_entity.username,
            email=domain_entity.email,
            password=domain_entity.password,
            memo=domain_entity.memo,
            created_at=domain_entity.created_at,
            updated_at=domain_entity.updated_at,
            role=domain_entity.role,
        )
