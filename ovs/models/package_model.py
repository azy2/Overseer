""" Defines a Package as represented in the database """
from flask import jsonify
from sqlalchemy import Integer, Column, VARCHAR, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from ovs import db


class Package(db.Model):
    """ Defines a Package as represented in the database """
    __tablename__ = 'packages'

    id = Column('id', Integer, primary_key=True)
    recipient_id = Column('recipient_id', Integer, ForeignKey('residents.user_id'), nullable=False)
    checked_by = Column('checked_by', String(511), nullable=False)
    checked_at = Column('checked_at', DateTime, nullable=False)
    description = Column('description', VARCHAR(2047), server_default="")
    user = relationship('Resident', uselist=False, single_parent=True)

    def __repr__(self):
        return 'Package([id={id}, recipient_id={recipient_id}, checked_by={checked_by}, ' \
               'checked_at={checked_at}, description={description}])'.format(**self.__dict__)

    def json(self):
        """ Returns a JSON representation of the Package """
        return jsonify(
            id=self.id,
            recipient_id=self.recipient_id,
            checked_by=self.checked_by,
            checked_at=self.checked_at,
            description=self.description
        )
