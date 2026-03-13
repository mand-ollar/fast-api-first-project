from datetime import datetime

from sqlalchemy.orm import Query, Session
from ulid import ULID  # type: ignore

from app.user.domain.entity import User
from app.user.domain.exception import UserNotFound
from app.user.domain.repository.UserRepository import UserRepository
from app.user.infrastructure.repository.entity import UserAlchemyEntity
from app.user.infrastructure.repository.mapper import UserMapper


class AlchemyUserRepository(UserRepository):
    def __init__(self, db: Session) -> None:
        self.db: Session = db

    def get(self, page: int, items_per_page: int) -> tuple[int, list[User]]:
        query: Query[UserAlchemyEntity] = self.db.query(UserAlchemyEntity)

        total_cnt: int = query.count()
        offset: int = (page - 1) * items_per_page
        users: list[UserAlchemyEntity] = query.limit(items_per_page).offset(offset).all()

        return total_cnt, [UserMapper.to_domain_entity(user) for user in users]

    def save(self, user: User) -> User:
        alchemy_entity: UserAlchemyEntity = UserMapper.to_alchemy_entity(user)

        self.db.add(alchemy_entity)
        self.db.commit()

        return UserMapper.to_domain_entity(alchemy_entity)

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

        for key, value in user.model_dump(exclude={"updated_at"}).items():
            setattr(alchemy_entity, key, value)
        alchemy_entity.updated_at = datetime.now()

        self.db.commit()
        self.db.refresh(alchemy_entity)

        return UserMapper.to_domain_entity(alchemy_entity)

    def delete_by_id(self, user_id: ULID) -> None:
        user: UserAlchemyEntity | None = (
            self.db.query(UserAlchemyEntity).filter(UserAlchemyEntity.id == str(user_id)).first()
        )
        if not user:
            raise UserNotFound(f"User not found: {user_id}")

        self.db.delete(user)
        self.db.commit()
