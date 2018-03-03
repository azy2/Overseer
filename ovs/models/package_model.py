""" Defines a Package as represented in the database """
from flask import jsonify
import sqlalchemy as sa
from ovs import app


class Package(app.BaseModel):
    """ Defines a Package as represented in the database """
    __tablename__ = 'packages'

    id = sa.Column('id', sa.Integer, primary_key=True)
    recipient_id = sa.Column('recipient_id', sa.Integer, nullable=False)
    checked_by_id = sa.Column('checked_by_id', sa.Integer, nullable=False)
    checked_at = sa.Column('checked_at', sa.DateTime, nullable=False)
    is_signed = sa.Column('is_signed', sa.Boolean, default=False)
    signed_at = sa.Column('signed_at', sa.DateTime, server_default=None)
    description = sa.Column('description', sa.VARCHAR(2047), server_default="")

    def __repr__(self):
        return 'Package([id="%s", recipient_id="%s", checked_by_id="%s", checked_at="%s", ' \
               'is_signed="%s", signed_at="%s", description="%s"])' \
                % (self.id, self.recipient_id, self.checked_by_id, self.checked_at,
                   self.is_signed, self.signed_at, self.description)

    def json(self):
        """ Returns a JSON representation of the Package """
        return jsonify(
            id=self.id,
            recipient_id=self.recipient_id,
            checked_by_id=self.checked_by_id,
            checked_at=self.checked_at,
            is_signed=self.is_signed,
            signed_at=self.signed_at,
            description=self.description
        )
