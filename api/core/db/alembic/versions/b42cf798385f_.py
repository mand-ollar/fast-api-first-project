"""empty message

Revision ID: b42cf798385f
Revises: 5e9c58528e81
Create Date: 2026-02-10 17:10:16.173809

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b42cf798385f'
down_revision: Union[str, Sequence[str], None] = '5e9c58528e81'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
