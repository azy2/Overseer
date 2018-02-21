"""
Defines a Room as represented in the database
"""
from flask import jsonify
import sqlalchemy as sa
from ovs import app


class Room(app.BaseModel):
    """
    Defines a Room as represented in the database. Along with some utility functions.
    """
    __tablename__ = 'rooms'

    id = sa.Column(sa.Integer, primary_key=True)
    number = sa.Column(sa.CHAR(255), unique=True)
    status = sa.Column(sa.CHAR(255), nullable=False)
    type = sa.Column(sa.CHAR(255), nullable=False)
    created = sa.Column(sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP'))
    updated = sa.Column(sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

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
