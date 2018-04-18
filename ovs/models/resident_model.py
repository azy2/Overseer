"""
Defines a Resident as represented in the database
"""
from flask import jsonify
from sqlalchemy import Integer, Column, CHAR, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ovs import db


class Resident(db.Model):
    """
    Defines a Resident as represented in the database. Along with some utility functions.
    """
    __tablename__ = 'residents'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    room_number = Column(CHAR(255), ForeignKey('rooms.number'))
    mealplan_pin = Column(Integer, ForeignKey('mealplan.pin'))
    created = Column(DateTime, server_default=func.now())
    updated = Column(DateTime, server_default=func.now(), server_onupdate=func.now())
    profile = relationship('Profile', uselist=False, back_populates='resident',
                           cascade='all, delete, delete-orphan')
    user = relationship('User', uselist=False, single_parent=True,
                        cascade='delete, delete-orphan')
    packages = relationship('Package', cascade='delete, delete-orphan')
    meal_plan = relationship('MealPlan', uselist=False, single_parent=True,
                             cascade='delete, delete-orphan')

    def __init__(self, user_id):
        super(Resident, self).__init__(user_id=user_id)

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
