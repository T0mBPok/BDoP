"""Delete importance color

Revision ID: 2530cb285972
Revises: 26405cbef58a
Create Date: 2025-04-13 23:33:33.748917

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2530cb285972'
down_revision: Union[str, None] = '26405cbef58a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tasks', 'importance_color')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('importance_color', sa.INTEGER(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
