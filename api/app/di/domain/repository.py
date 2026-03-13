from fastapi import Depends  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.note.domain.repository import NoteRepository, TagRepository
from app.note.infrastructure.repository import AlchemyNoteRepository, AlchemyTagRepository
from app.user.domain.repository import UserRepository
from app.user.infrastructure.repository import AlchemyUserRepository
from core.auth.domain.repository import CredentialsRepository, PrincipalRepository
from core.auth.infrastructure.repository.credentials import AlchemyCredentialsRepository
from core.auth.infrastructure.repository.principal import AlchemyPrincipalRepository
from core.db.db import get_db


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return AlchemyUserRepository(db=db)


def get_credentials_repository(db: Session = Depends(get_db)) -> CredentialsRepository:
    return AlchemyCredentialsRepository(db=db)


def get_principal_repository(db: Session = Depends(get_db)) -> PrincipalRepository:
    return AlchemyPrincipalRepository(db=db)


def get_note_repository(db: Session = Depends(get_db)) -> NoteRepository:
    return AlchemyNoteRepository(db=db)


def get_tag_repository(db: Session = Depends(get_db)) -> TagRepository:
    return AlchemyTagRepository(db=db)
