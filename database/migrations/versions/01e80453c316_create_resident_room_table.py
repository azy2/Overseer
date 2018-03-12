"""create resident room table

Revision ID: 01e80453c316
Revises: dfa5b024a486
Create Date: 2018-02-22 23:01:24.508365

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01e80453c316'
down_revision = 'dfa5b024a486'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'resident_rooms',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('residents.user_id'), nullable=False), 
        sa.Column('room', sa.CHAR(255), unique=True),
        sa.Column('current', sa.CHAR(255), nullable=False),
        sa.Column('created', sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated', sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
    )

def downgrade():
    op.drop_table('resident_rooms')
