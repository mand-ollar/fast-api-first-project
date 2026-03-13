from ulid import ULID

from core.auth.domain.entity import Principal
from core.auth.domain.exception import InvalidPrincipal
from core.auth.domain.repository import PrincipalRepository
from core.auth.infrastructure.repository.principal.entity import (
    PrincipalAlchemyEntity,
)
from core.auth.infrastructure.repository.principal.mapper import (
    PrincipalMapper,
)
from core.db.db import Session


class AlchemyPrincipalRepository(PrincipalRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_principal(self, principal: str) -> Principal:
        alchemy_entity: PrincipalAlchemyEntity | None = (
            self.db.query(PrincipalAlchemyEntity).filter(PrincipalAlchemyEntity.principal == principal).first()
        )
        if not alchemy_entity:
            raise InvalidPrincipal(f"Principal not found: {principal}")

        return PrincipalMapper.to_domain_entity(alchemy_entity)

    def get_by_user_id(self, user_id: ULID) -> Principal:
        alchemy_entity: PrincipalAlchemyEntity | None = (
            self.db.query(PrincipalAlchemyEntity).filter(PrincipalAlchemyEntity.user_id == str(user_id)).first()
        )
        if not alchemy_entity:
            raise InvalidPrincipal(f"Principal not found: {user_id}")

        return PrincipalMapper.to_domain_entity(alchemy_entity)

    def exists(self, principal: str) -> bool:
        return (
            self.db.query(PrincipalAlchemyEntity).filter(PrincipalAlchemyEntity.principal == principal).first()
            is not None
        )

    def add(self, principal: Principal) -> Principal:
        alchemy_entity: PrincipalAlchemyEntity = PrincipalMapper.to_alchemy_entity(principal)
        self.db.add(alchemy_entity)
        self.db.commit()

        return PrincipalMapper.to_domain_entity(alchemy_entity)

    def update(self, principal: Principal) -> Principal:
        alchemy_entity: PrincipalAlchemyEntity | None = (
            self.db.query(PrincipalAlchemyEntity).filter(PrincipalAlchemyEntity.id == str(principal.id)).first()
        )
        if not alchemy_entity:
            raise InvalidPrincipal(f"Principal not found: {principal.id}")

        for key, value in principal.model_dump().items():
            setattr(alchemy_entity, key, value)

        self.db.commit()
        self.db.refresh(alchemy_entity)

        return PrincipalMapper.to_domain_entity(alchemy_entity)
