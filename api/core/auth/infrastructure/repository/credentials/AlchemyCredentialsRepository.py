from sqlalchemy import Delete, Select, delete, select

from core.auth.domain.enum import CredentialType
from core.auth.domain.exception import InvalidCredentials
from core.auth.domain.repository import CredentialsRepository
from core.auth.domain.valueobject import Credentials
from core.auth.infrastructure.repository.credentials.entity import (
    CredentialsAlchemyEntity,
)
from core.auth.infrastructure.repository.credentials.mapper import CredentialsMapper
from core.db.db import Session


class AlchemyCredentialsRepository(CredentialsRepository):
    def __init__(self, db: Session) -> None:
        self.db: Session = db

    def save(self, creds: Credentials) -> None:
        alchemy_entity: CredentialsAlchemyEntity | None = (
            self.db
            .query(CredentialsAlchemyEntity)
            .filter(CredentialsAlchemyEntity.user_id == str(creds.user_id))
            .first()
        )
        if not alchemy_entity:
            alchemy_entity = CredentialsMapper.to_alchemy_entity(creds)
            self.db.add(alchemy_entity)
        else:
            if creds.type == CredentialType.SHORT_LIVED:
                alchemy_entity.access_key = creds.raw_value
            elif creds.type == CredentialType.LONG_LIVED:
                alchemy_entity.refresh_key = creds.raw_value
            else:
                raise InvalidCredentials("Invalid credentials type")

        self.db.commit()

    def exists(self, creds: Credentials) -> bool:
        stmt: Select[tuple[CredentialsAlchemyEntity]]
        if creds.type == CredentialType.SHORT_LIVED:
            stmt = select(CredentialsAlchemyEntity).where(CredentialsAlchemyEntity.access_key == creds.raw_value)
        elif creds.type == CredentialType.LONG_LIVED:
            stmt = select(CredentialsAlchemyEntity).where(CredentialsAlchemyEntity.refresh_key == creds.raw_value)
        else:
            return False

        result: CredentialsAlchemyEntity | None = self.db.execute(stmt).scalar_one_or_none()
        return result is not None

    def revoke(self, creds: Credentials) -> None:
        stmt: Delete
        if creds.type == CredentialType.SHORT_LIVED:
            stmt = delete(CredentialsAlchemyEntity).where(CredentialsAlchemyEntity.access_key == creds.raw_value)
        elif creds.type == CredentialType.LONG_LIVED:
            stmt = delete(CredentialsAlchemyEntity).where(CredentialsAlchemyEntity.refresh_key == creds.raw_value)
        else:
            raise InvalidCredentials("Invalid credentials type")

        self.db.execute(stmt)
        self.db.commit()
