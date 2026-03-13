from ulid import ULID  # type: ignore

from app.note.domain.entity import Tag
from app.note.infrastructure.repository.entity import TagAlchemyEntity


class TagMapper:
    @staticmethod
    def to_domain_entity(alchemy_entity: TagAlchemyEntity) -> Tag:
        return Tag(
            id=ULID.from_str(alchemy_entity.id),
            name=alchemy_entity.name,
            created_at=alchemy_entity.created_at,
            updated_at=alchemy_entity.updated_at,
        )

    @staticmethod
    def to_alchemy_entity(domain_entity: Tag) -> TagAlchemyEntity:
        return TagAlchemyEntity(
            id=str(domain_entity.id),
            name=domain_entity.name,
            created_at=domain_entity.created_at,
            updated_at=domain_entity.updated_at,
        )
