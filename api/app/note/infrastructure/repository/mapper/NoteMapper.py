import json

from ulid import ULID  # type: ignore

from app.note.domain.entity import Note, Tag
from app.note.domain.valueobject import Content
from app.note.infrastructure.repository.entity import NoteAlchemyEntity


class NoteMapper:
    @staticmethod
    def to_domain_entity(alchemy_entity: NoteAlchemyEntity) -> Note:
        return Note(
            id=ULID.from_str(alchemy_entity.id),
            title=alchemy_entity.title,
            content=Content(**json.loads(alchemy_entity.content)),
            created_at=alchemy_entity.created_at,
            updated_at=alchemy_entity.updated_at,
            created_by=ULID.from_str(alchemy_entity.created_by),
            updated_by=ULID.from_str(alchemy_entity.updated_by),
            tags=[Tag(**json.loads(tag)) for tag in alchemy_entity.tags],
            status=alchemy_entity.status,
        )

    @staticmethod
    def to_alchemy_entity(domain_entity: Note) -> NoteAlchemyEntity:
        return NoteAlchemyEntity(
            id=str(domain_entity.id),
            title=domain_entity.title,
            content=domain_entity.content.model_dump_json(),
            created_at=domain_entity.created_at,
            updated_at=domain_entity.updated_at,
            created_by=str(domain_entity.created_by),
            updated_by=str(domain_entity.updated_by),
            tags=[tag.model_dump_json() for tag in domain_entity.tags],
            status=domain_entity.status,
        )
