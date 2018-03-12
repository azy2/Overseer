"""
Defines a Room as represented in the database
"""
from flask import jsonify
from sqlalchemy import Integer, Column, CHAR, text, DateTime

from ovs import app


class Room(app.BaseModel):
    """
    Defines a Room as represented in the database. Along with some utility functions.
    """
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True)
    number = Column(CHAR(255), unique=True)
    status = Column(CHAR(255), nullable=False)
    type = Column(CHAR(255), nullable=False)
    created = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated = Column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    def __repr__(self):
        return 'Room([id="%s", number="%s", status="%s", type="%s", created="%s", updated="%s"])' \
               % (self.id, self.number, self.status, self.type, self.created, self.updated)

    def json(self):
        """ Returns a JSON representation of this Room """
        return jsonify(
            id=self.id,
            number=self.number,
            status=self.status,
            type=self.type,
            created=self.created,
            updated=self.updated
        )
