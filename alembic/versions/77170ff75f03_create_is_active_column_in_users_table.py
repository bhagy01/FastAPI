"""create is_active column in users table

Revision ID: 77170ff75f03
Revises: 64441ffd376a
Create Date: 2022-01-22 19:24:11.935018

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77170ff75f03'
down_revision = '64441ffd376a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('Users',sa.Column('is_active',sa.Boolean(),server_default='False'))
    pass

def downgrade():
    op.drop_column('Users','is_active')
    pass
