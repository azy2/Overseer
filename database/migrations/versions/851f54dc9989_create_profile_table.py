"""create profile table

Revision ID: 851f54dc9989
Revises: 01e80453c316
Create Date: 2018-03-01 23:51:05.631322

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '851f54dc9989'
down_revision = '01e80453c316'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'profile',
        sa.Column('user_id', sa.Integer, sa.ForeignKey('residents.user_id'), primary_key=True, nullable=False),
        sa.Column('preferred_name', sa.CHAR(255)),
        sa.Column('phone_number', sa.CHAR(31)),
        sa.Column('preferred_email', sa.CHAR(255)),
        sa.Column('race', sa.CHAR(31)),
        sa.Column('gender', sa.Enum('Male', 'Female', 'Unspecified'), nullable=False),
        sa.Column('picture_id', sa.CHAR(63)),
        sa.Column('created', sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated', sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
    )

def downgrade():
    op.drop_table('profile')
