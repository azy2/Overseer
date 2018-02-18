"""Create Residents Table


Revision ID: 7d52e7b00604
Revises: ba062e38b07e
Create Date: 2018-02-18 08:06:26.352014

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d52e7b00604'
down_revision = 'ba062e38b07e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'residents',
        sa.Column('user_id', sa.Integer, primary_key=True),
        sa.Column('room_number', sa.Integer),
        sa.Column('created', sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated', sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
    )


def downgrade():
    op.drop_table('residents')
