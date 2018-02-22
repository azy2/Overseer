"""Create Users Table

Revision ID: ba062e38b07e
Revises:
Create Date: 2018-02-16 09:55:22.635835

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba062e38b07e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('first_name', sa.String(255), nullable=False),
        sa.Column('last_name', sa.String(255), nullable=False),
        sa.Column('password', sa.CHAR(60), nullable=False),
        sa.Column('role', sa.Enum('RESIDENT', 'RESIDENT_ADVISOR', 'STAFF', 'OFFICE_MANAGER', 'BUILDING_MANAGER', 'ADMIN'), nullable=False),
        sa.Column('created', sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated', sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
    )

def downgrade():
    op.drop_table('users')
