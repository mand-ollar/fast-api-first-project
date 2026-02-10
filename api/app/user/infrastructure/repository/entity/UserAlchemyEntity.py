from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from ulid import ULID  # type: ignore

from core.db.db import Base


class UserAlchemyEntity(Base):
    __tablename__: str = "User"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(ULID()))
    username: Mapped[str] = mapped_column(String(32), nullable=False)
    email: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(64), nullable=False)
    memo: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now())
