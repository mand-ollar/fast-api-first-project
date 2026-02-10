from datetime import datetime

from sqlalchemy.orm import Session
from ulid import ULID  # type: ignore

from app.user.domain.entity import User
from app.user.domain.exception import UserNotFound
from app.user.domain.repository.UserRepository import UserRepository
from app.user.infrastructure.repository.entity import UserAlchemyEntity
from app.user.infrastructure.repository.mapper import UserMapper


class AlchemyUserRepository(UserRepository):
    def __init__(self, db: Session) -> None:
        self.db: Session = db

    def get(self) -> list[User]:
        users: list[UserAlchemyEntity] = self.db.query(UserAlchemyEntity).all()
        return [UserMapper.to_domain_entity(user) for user in users]

    def save(self, user: User) -> User:
        new_user: UserAlchemyEntity = UserAlchemyEntity(
            id=str(user.id),
            username=user.username,
            email=user.email,
            password=user.password,
            memo=user.memo,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

        self.db.add(new_user)
        self.db.commit()

        return UserMapper.to_domain_entity(new_user)

    def get_by_email(self, email: str) -> User:
        user: UserAlchemyEntity | None = (
            self.db.query(UserAlchemyEntity).filter(UserAlchemyEntity.email == email).first()
        )

        if not user:
            raise UserNotFound(f"User with email {email} not found")

        return UserMapper.to_domain_entity(user)

    def get_by_id(self, id: ULID) -> User:
        alchemy_entity: UserAlchemyEntity | None = (
            self.db.query(UserAlchemyEntity).filter(UserAlchemyEntity.id == str(id)).first()
        )
        if not alchemy_entity:
            raise UserNotFound(f"User not found: {id}")
        return UserMapper.to_domain_entity(alchemy_entity)

    def update(self, user: User) -> User:
        alchemy_entity: UserAlchemyEntity | None = (
            self.db.query(UserAlchemyEntity).filter(UserAlchemyEntity.id == str(user.id)).first()
        )

        if not alchemy_entity:
            raise UserNotFound(f"User not found: {user.id}")

        alchemy_entity.username = user.username
        alchemy_entity.password = user.password
        alchemy_entity.updated_at = datetime.now()

        self.db.add(alchemy_entity)
        self.db.commit()

        return UserMapper.to_domain_entity(alchemy_entity)
