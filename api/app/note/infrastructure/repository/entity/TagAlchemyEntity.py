from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from ulid import ULID  # type: ignore

from core.db.db import Base


class TagAlchemyEntity(Base):
    __tablename__: str = "Tag"

    id: Mapped[str] = mapped_column(String(26), primary_key=True, default=lambda: str(ULID()))
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now())
