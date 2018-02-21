"""Create Package Table

Revision ID: f9015ed74bcc
Revises: dfa5b024a486
Create Date: 2018-02-21 19:25:24.922989

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f9015ed74bcc'
down_revision = 'dfa5b024a486'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'package',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('checked_by', sa.Integer, nullable=False),
        sa.Column('checked_at', sa.DateTime, nullable=False),
        sa.Column('is_signed', sa.Boolean, server_default=None),
        sa.Column('signed_at', sa.DateTime, server_default=None),
        sa.Column('description', sa.VARCHAR(2047), server_default="")
    )


def downgrade():
    op.drop_table('package')
