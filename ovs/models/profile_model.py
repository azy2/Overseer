"""
Defines a Profile as represented in the database
"""
from flask import jsonify
from sqlalchemy import Integer, Enum, Column, CHAR, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ovs import db
from ovs.utils import genders


class Profile(db.Model):
    """
    Defines a Profile as represented in the database.
    Args:
        user_id (int): Must be the same as corresponding `User.id`.

    Returns:
        A Profile Model object.
    """
    __tablename__ = 'profile'

    user_id = Column(Integer, ForeignKey('residents.user_id'),
                     primary_key=True, nullable=False)
    preferred_name = Column(CHAR(255))
    phone_number = Column(CHAR(255))
    preferred_email = Column(CHAR(255))
    race = Column(CHAR(31))
    gender = Column(Enum(genders.MALE, genders.FEMALE, genders.UNSPECIFIED))
    created = Column(DateTime, server_default=func.now())
    updated = Column(DateTime, server_default=func.now(), server_onupdate=func.now())
    resident = relationship('Resident', uselist=False, back_populates='profile',
                            single_parent=True, cascade='delete, delete-orphan')

    def __init__(self, user_id):
        super(Profile, self).__init__(user_id=user_id)

    def __repr__(self):
        """
        Allows Profile to be printed.
        Returns:
            str: A string representation of this Profile.
        """
        return 'Profile([user_id={user_id}, preferred_name={preferred_name}, phone_number={phone_number}, ' \
               'preferred_email={preferred_email}, race={race}, gender={gender}, created={created}, ' \
               'updated={updated}])'.format(**self.__dict__)

    def json(self):
        """
        Get JSON representation of this Profile.
        Returns:
             A JSON representation of this Profile.
        """
        return jsonify(
            user_id=self.user_id,
            preferred_name=self.preferred_name,
            phone_number=self.phone_number,
            preferred_email=self.preferred_email,
            race=self.race,
            gender=self.gender,
            created=self.created,
            updated=self.updated
        )
