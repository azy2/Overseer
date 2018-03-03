"""Create mealplan table

Revision ID: a6a96c224557
Revises: dfa5b024a486
Create Date: 2018-03-01 23:07:06.991966

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a6a96c224557'
down_revision = 'dfa5b024a486'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'mealplan',
        sa.Column('id',  sa.Integer, primary_key=True),
        sa.Column('pin', sa.Integer, unique=True),
        sa.Column('credits', sa.Integer, nullable=False),
        sa.Column('meal_plan', sa.Integer, nullable=False),
        sa.Column('reset_date', sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('plan_type', sa.Enum('WEEKLY', 'SEMESTERLY', 'LIFETIME'), nullable=False),
        sa.Column('created', sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated', sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    )

def downgrade():
    op.drop_table('mealplan')
