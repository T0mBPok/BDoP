"""projects - icon

Revision ID: 0d8ca027d574
Revises: 7c96f99a602f
Create Date: 2025-05-15 02:06:46.255128

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d8ca027d574'
down_revision: Union[str, None] = '7c96f99a602f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('projects_image_id_fkey', 'projects', type_='foreignkey')
    op.create_foreign_key(None, 'projects', 'project_images', ['image_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'projects', type_='foreignkey')
    op.create_foreign_key('projects_image_id_fkey', 'projects', 'images', ['image_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###
