"""add public farm id

Revision ID: b16dd134a8f0
Revises: 1ef3017765fb
Create Date: 2026-09-08 13:16:05.343000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b16dd134a8f0'
down_revision: Union[str, Sequence[str], None] = '1ef3017765fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "smart_farm_os",
        sa.Column("public_id", sa.String(length=11), nullable=True)
    )
    op.execute("UPDATE smart_farm_os SET public_id = 'SFO-R5NZ-43' WHERE public_id IS NULL")
    op.alter_column(
        "smart_farm_os",
        "public_id",
        nullable=False
    )

def downgrade() -> None:
    op.drop_column("smart_farm_os", "public_id")
