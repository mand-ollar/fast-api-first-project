from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.auth.domain.enum import Role
from core.db.db import Base


class PrincipalAlchemyEntity(Base):
    __tablename__: str = "Principal"

    id: Mapped[str] = mapped_column(String(26), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(26), unique=True, index=True)
    principal: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    password_hashed: Mapped[str] = mapped_column(String(60))
    role: Mapped[Role] = mapped_column(String(32), nullable=False)
