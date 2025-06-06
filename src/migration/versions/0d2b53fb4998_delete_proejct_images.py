"""delete proejct_images

Revision ID: 0d2b53fb4998
Revises: 1f2a2de0071a
Create Date: 2025-05-18 14:22:04.744683

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d2b53fb4998'
down_revision: Union[str, None] = '1f2a2de0071a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("DROP TABLE project_images CASCADE")


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
