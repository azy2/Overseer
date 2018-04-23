""" Defines a Package as represented in the database """
from flask import jsonify
from sqlalchemy import Integer, Column, VARCHAR, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy_utc import UtcDateTime

from ovs import db


class Package(db.Model):
    """ Defines a Package as represented in the database. """
    __tablename__ = 'packages'

    id = Column('id', Integer, primary_key=True)
    recipient_id = Column('recipient_id', Integer, ForeignKey('residents.user_id'), nullable=False)
    checked_by = Column('checked_by', String(511), nullable=False)
    checked_at = Column('checked_at', UtcDateTime, nullable=False)
    description = Column('description', VARCHAR(2047), server_default="")
    recipient = relationship('Resident', uselist=False, single_parent=True)

    def __repr__(self):
        """
        Allows Package to be printed.
        Returns:
            str: A string representation of this Package.
        """
        return 'Package([id={id}, recipient_id={recipient_id}, checked_by={checked_by}, ' \
               'checked_at={checked_at}, description={description}])'.format(**self.__dict__)

    def json(self):
        """
        Get JSON representation of this Package.
        Returns:
             A JSON representation of this Package.
        """
        return jsonify(
            id=self.id,
            recipient_id=self.recipient_id,
            checked_by=self.checked_by,
            checked_at=self.checked_at,
            description=self.description
        )
