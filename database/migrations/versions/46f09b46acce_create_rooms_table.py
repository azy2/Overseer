"""Create rooms Table

Revision ID: 46f09b46acce
Revises: ba062e38b07e
Create Date: 2018-02-17 05:11:35.007860

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46f09b46acce'
down_revision = 'ba062e38b07e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'rooms',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('number', sa.CHAR(255), unique=True),
        sa.Column('status', sa.CHAR(255), nullable=False),
        sa.Column('type', sa.CHAR(255), nullable=False),
        sa.Column('created', sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated', sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
    )

def downgrade():
    op.drop_table('rooms')
