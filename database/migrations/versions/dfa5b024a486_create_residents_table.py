"""Create residents table

Revision ID: dfa5b024a486
Revises: 46f09b46acce
Create Date: 2018-02-17 22:53:36.616850

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dfa5b024a486'
down_revision = '46f09b46acce'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'residents',
        sa.Column('user_id', sa.Integer, primary_key=True),
        sa.Column('room_number', sa.CHAR(255)),
        sa.Column('mealplan_pin', sa.Integer, autoincrement=True),
        sa.Column('created', sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated', sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.relationship('Profile', uselist=False, back_populates='resident', cascade='all, delete, delete-orphan') # <-- Is this correct? Added this to fix an error complaining about 'profile' existing in the model, but not here.
    )

def downgrade():
    op.drop_table('residents')
