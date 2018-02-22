"""
Defines a Resident as represented in the database
"""
from flask import jsonify
import sqlalchemy as sa
from ovs import app


class Resident(app.BaseModel):
    """
    Defines a Resident as represented in the database. Along with some utility functions.
    """
    __tablename__ = 'residents'

    user_id = sa.Column(sa.Integer, primary_key=True)
    room_number = sa.Column(sa.CHAR(255))
    created = sa.Column(sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP'))
    updated = sa.Column(sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    def __init__(self, user_id, room_number):
        super(Resident, self).__init__(user_id=user_id, room_number=room_number)

    def __repr__(self):
        return "Resident([user_id='%s', room_number='%s', created='%s', updated='%s'])" \
               % (self.user_id, self.room_number, self.created, self.updated)

    def json(self):
        """ Returns a JSON representation of this Resident """
        return jsonify(
            user_id=self.user_id,
            room_number=self.room_number,
            created=self.created,
            updated=self.updated
        )
