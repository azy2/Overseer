"""
Defines a Resident as represented in the database
"""
from flask import jsonify
from sqlalchemy import Integer, Column, CHAR, text, DateTime
from sqlalchemy.orm import relationship

from ovs import db


class Resident(db.Model):
    """
    Defines a Resident as represented in the database. Along with some utility functions.
    """
    __tablename__ = 'residents'

    user_id = Column(Integer, primary_key=True)
    room_number = Column(CHAR(255))
    mealplan_pin = Column(Integer, autoincrement=True)
    created = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated = Column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    profile = relationship('Profile', uselist=False, back_populates='resident', cascade='all, delete, delete-orphan')

    def __init__(self, user_id, room_number):
        super(Resident, self).__init__(user_id=user_id, room_number=room_number)

    def __repr__(self):
        return 'Resident([user_id={user_id}, room_number={room_number},' \
               'created={created}, updated={updated}])'.format(**self.__dict__)

    def json(self):
        """ Returns a JSON representation of this Resident """
        return jsonify(
            user_id=self.user_id,
            room_number=self.room_number,
            created=self.created,
            updated=self.updated
        )
