"""create users table

Revision ID: 1ef3017765fb
Revises: c5f44fd624d5
Create Date: 2026-09-03 21:58:30.015487

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "1ef3017765fb"
down_revision: Union[str, Sequence[str], None] = "c5f44fd624d5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
