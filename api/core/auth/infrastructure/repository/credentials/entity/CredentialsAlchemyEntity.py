from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from ulid import ULID  # type: ignore

from core.db.db import Base


class CredentialsAlchemyEntity(Base):
    __tablename__: str = "Credentials"

    id: Mapped[str] = mapped_column(String(26), primary_key=True, default=lambda: str(ULID()))
    user_id: Mapped[ULID] = mapped_column(String(26), unique=True, index=True)
    access_key: Mapped[str | None] = mapped_column(String(512), nullable=True)
    refresh_key: Mapped[str | None] = mapped_column(String(512), nullable=True)
