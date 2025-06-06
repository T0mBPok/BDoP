"""Updated_projects

Revision ID: 8cbde304c74a
Revises: 44b6237e3aa1
Create Date: 2025-04-09 20:39:42.644952

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8cbde304c74a'
down_revision: Union[str, None] = '44b6237e3aa1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('projects', 'count_tasks')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('projects', sa.Column('count_tasks', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
