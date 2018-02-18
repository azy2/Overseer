from flask import jsonify
from ovs import app
import sqlalchemy as sa


class Resident(app.BaseModel):
    __tablename__ = 'residents'

    user_id = sa.Column(sa.Integer, primary_key=True)
    room_number = sa.Column(sa.Integer)
    created = sa.Column(sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP'))
    updated = sa.Column(sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    def __repr__(self):
        return "Resident([user_id='%s', room_number='%s', created='%s', updated='%s'])" % (self.user_id, self.room_number, self.created, self.updated)

    def json(self):
        return jsonify(
            user_id = self.user_id,
            room_number = self.room_number,
            created = self.created,
            updated = self.updated
        )