from datetime import datetime

from sqlalchemy.orm import Query, Session
from ulid import ULID  # type: ignore

from app.note.domain.entity import Note
from app.note.domain.exception import NoteNotFound
from app.note.domain.repository import NoteRepository
from app.note.infrastructure.repository.entity import NoteAlchemyEntity
from app.note.infrastructure.repository.mapper import NoteMapper


class AlchemyNoteRepository(NoteRepository):
    def __init__(self, db: Session) -> None:
        self.db: Session = db

    def get(self, page: int, items_per_page: int) -> tuple[int, list[Note]]:
        query: Query[NoteAlchemyEntity] = self.db.query(NoteAlchemyEntity)

        total_cnt: int = query.count()
        offset: int = (page - 1) * items_per_page
        notes: list[NoteAlchemyEntity] = query.limit(items_per_page).offset(offset).all()

        return total_cnt, [NoteMapper.to_domain_entity(note) for note in notes]

    def get_by_id(self, id: ULID) -> Note:
        alchemy_entity: NoteAlchemyEntity | None = (
            self.db.query(NoteAlchemyEntity).filter(NoteAlchemyEntity.id == str(id)).first()
        )
        if not alchemy_entity:
            raise NoteNotFound(f"Note not found: {id}")

        return NoteMapper.to_domain_entity(alchemy_entity)

    def save(self, note: Note) -> Note:
        alchemy_entity: NoteAlchemyEntity = NoteMapper.to_alchemy_entity(note)

        self.db.add(alchemy_entity)
        self.db.commit()

        return NoteMapper.to_domain_entity(alchemy_entity)

    def update(self, note: Note) -> Note:
        alchemy_entity: NoteAlchemyEntity | None = (
            self.db.query(NoteAlchemyEntity).filter(NoteAlchemyEntity.id == str(note.id)).first()
        )
        if not alchemy_entity:
            raise NoteNotFound(f"Note not found: {note.id}")

        updated_alchemy_entity: NoteAlchemyEntity = NoteMapper.to_alchemy_entity(note)

        for key, value in note.model_dump(exclude={"updated_at"}).items():
            setattr(alchemy_entity, key, getattr(updated_alchemy_entity, key))
        alchemy_entity.updated_at = datetime.now()

        self.db.commit()
        self.db.refresh(alchemy_entity)

        return NoteMapper.to_domain_entity(alchemy_entity)

    def delete(self, note: Note) -> None:
        alchemy_entity: NoteAlchemyEntity | None = (
            self.db.query(NoteAlchemyEntity).filter(NoteAlchemyEntity.id == str(note.id)).first()
        )
        if not alchemy_entity:
            raise NoteNotFound(f"Note not found: {note.id}")

        self.db.delete(alchemy_entity)
        self.db.commit()
