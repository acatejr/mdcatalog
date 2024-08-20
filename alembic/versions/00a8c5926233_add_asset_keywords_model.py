"""Add asset keywords model

Revision ID: 00a8c5926233
Revises: d131b2059af8
Create Date: 2024-08-20 13:39:30.896683

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '00a8c5926233'
down_revision: Union[str, None] = 'd131b2059af8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
