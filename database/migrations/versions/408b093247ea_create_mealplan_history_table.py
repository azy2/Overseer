"""Create mealplan_history Table

Revision ID: 408b093247ea
Revises: f6a035cef26e
Create Date: 2018-04-05 01:34:35.950522

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '408b093247ea'
down_revision = 'f6a035cef26e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'mealplan_history',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('resident_id', sa.Integer),
        sa.Column('mealplan_pin', sa.Integer),
        sa.Column('manager_id', sa.Integer),
        sa.Column('log_type', sa.Enum('MEAL_USED', 'UNDO'), nullable=False),
        sa.Column('created', sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated', sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
    )


def downgrade():
    op.drop_table('mealplan_history')
