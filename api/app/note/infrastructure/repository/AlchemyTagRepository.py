from datetime import datetime

from sqlalchemy.orm import Session
from ulid import ULID  # type: ignore

from app.note.domain.entity import Tag
from app.note.domain.exception import TagAlreadyExists, TagNotFound
from app.note.domain.repository import TagRepository
from app.note.infrastructure.repository.entity import TagAlchemyEntity
from app.note.infrastructure.repository.mapper import TagMapper


class AlchemyTagRepository(TagRepository):
    def __init__(self, db: Session) -> None:
        self.db: Session = db

    def get_by_id(self, id: ULID) -> Tag:
        alchemy_entity: TagAlchemyEntity | None = (
            self.db.query(TagAlchemyEntity).filter(TagAlchemyEntity.id == str(id)).first()
        )
        if not alchemy_entity:
            raise TagNotFound(f"Tag not found: {id}")

        return TagMapper.to_domain_entity(alchemy_entity)

    def get_by_name(self, name: str) -> Tag:
        alchemy_entity: TagAlchemyEntity | None = (
            self.db.query(TagAlchemyEntity).filter(TagAlchemyEntity.name == name).first()
        )
        if not alchemy_entity:
            raise TagNotFound(f"Tag not found: {name}")

        return TagMapper.to_domain_entity(alchemy_entity)

    def save(self, tag: Tag) -> Tag:
        alchemy_entity: TagAlchemyEntity = TagMapper.to_alchemy_entity(tag)

        if self.db.query(TagAlchemyEntity).filter(TagAlchemyEntity.name == tag.name).first():
            raise TagAlreadyExists(f"Tag already exists: {tag.name}")

        self.db.add(alchemy_entity)
        self.db.commit()

        return TagMapper.to_domain_entity(alchemy_entity)

    def delete(self, tag: Tag) -> None:
        alchemy_entity: TagAlchemyEntity | None = (
            self.db.query(TagAlchemyEntity).filter(TagAlchemyEntity.id == str(tag.id)).first()
        )
        if not alchemy_entity:
            raise TagNotFound(f"Tag not found: {tag.id}")

        self.db.delete(alchemy_entity)
        self.db.commit()

    def update(self, tag: Tag) -> Tag:
        alchemy_entity: TagAlchemyEntity | None = (
            self.db.query(TagAlchemyEntity).filter(TagAlchemyEntity.id == str(tag.id)).first()
        )
        if not alchemy_entity:
            raise TagNotFound(f"Tag not found: {tag.id}")

        for key, value in tag.model_dump(exclude={"updated_at"}).items():
            setattr(alchemy_entity, key, value)
        alchemy_entity.updated_at = datetime.now()

        self.db.commit()
        self.db.refresh(alchemy_entity)

        return TagMapper.to_domain_entity(alchemy_entity)

    def get_all(self) -> list[Tag]:
        tags: list[TagAlchemyEntity] = self.db.query(TagAlchemyEntity).all()
        return [TagMapper.to_domain_entity(tag) for tag in tags]
