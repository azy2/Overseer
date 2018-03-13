"""
Defines a Profile as represented in the database
"""
import uuid
from flask import jsonify
from sqlalchemy import Integer, Enum, Column, CHAR, text, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from ovs import app
from ovs.utils import genders


class Profile(app.BaseModel):
    """
    Defines a Profile as represented in the database.
    """
    __tablename__ = 'profile'

    user_id = Column(Integer, ForeignKey('residents.user_id'),
                     primary_key=True, nullable=False)
    preferred_name = Column(CHAR(255))
    phone_number = Column(CHAR(255))
    preferred_email = Column(CHAR(255))
    race = Column(CHAR(31))
    gender = Column(Enum(genders.MALE, genders.FEMALE))
    picture_id = Column(CHAR(63))
    created = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated = Column(DateTime, server_default=text(
        'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    resident = relationship('Resident', uselist=False,
                            back_populates='profile', single_parent=True)

    def __init__(self, user_id):
        super(Profile, self).__init__(user_id=user_id, picture_id=str(uuid.uuid4()))

    def __repr__(self):
        return 'Profile([user_id={user_id}, preferred_name={preferred_name}, phone_number={phone_number}, ' \
               'preferred_email={preferred_email}, race={race}, gender={gender}, picture_id={picture_id}, ' \
               'created={created}, updated={updated}])'.format(**self.__dict__)

    def json(self):
        """ Returns a JSON representation of this Profile """
        return jsonify(
            user_id=self.user_id,
            preferred_name=self.preferred_name,
            phone_number=self.phone_number,
            preferred_email=self.preferred_email,
            race=self.race,
            gender=self.gender,
            picture_id=self.picture_id,
            created=self.created,
            updated=self.updated
        )
