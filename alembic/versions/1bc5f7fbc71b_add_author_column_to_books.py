"""add author column to books

Revision ID: 1bc5f7fbc71b
Revises: 7ebdd4351013
Create Date: 2025-05-22 10:08:34.862563

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1bc5f7fbc71b'
down_revision: Union[str, None] = '7ebdd4351013'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
