"""
Defines a Profile as represented in the database
"""
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

    user_id = Column(Integer, ForeignKey('residents.user_id'), primary_key=True, nullable=False)
    preferred_name = Column(CHAR(255))
    phone_number = Column(CHAR(255))
    preferred_email = Column(CHAR(255))
    race = Column(CHAR(31))
    gender = Column(Enum(genders.MALE, genders.FEMALE))
    picture_path = Column(CHAR(255))
    created = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated = Column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    resident = relationship('Resident', uselist=False, back_populates='profile', single_parent=True)

    def __init__(self, user_id):
        super(Profile, self).__init__(user_id=user_id)

    def __repr__(self):
        return "Profile([user_id='%s', preferred_name='%s', phone_number='%s', preferred_email='%s', race='%s', \
               gender='%s', picture_path='%s', created='%s', updated='%s'])" \
               % (self.user_id, self.preferred_name, self.phone_number, self.preferred_email, self.race, self.gender,
                  self.picture_path, self.created, self.updated)

    def json(self):
        """ Returns a JSON representation of this Profile """
        return jsonify(
            user_id=self.user_id,
            preferred_name=self.preferred_name,
            phone_number=self.phone_number,
            preferred_email=self.preferred_email,
            race=self.race,
            gender=self.gender,
            picture_path=self.picture_path,
            created=self.created,
            updated=self.updated
        )
