""" Defines a Package as represented in the database """
from flask import jsonify
from sqlalchemy import Integer, Column, VARCHAR, Boolean, DateTime

from ovs import app


class Package(app.BaseModel):
    """ Defines a Package as represented in the database """
    __tablename__ = 'packages'

    id = Column('id', Integer, primary_key=True)
    recipient_id = Column('recipient_id', Integer, nullable=False)
    checked_by_id = Column('checked_by_id', Integer, nullable=False)
    checked_at = Column('checked_at', DateTime, nullable=False)
    is_signed = Column('is_signed', Boolean, default=False)
    signed_at = Column('signed_at', DateTime, server_default=None)
    description = Column('description', VARCHAR(2047), server_default="")

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
