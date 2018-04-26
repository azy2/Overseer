"""
Defines a Room as represented in the database
"""
from datetime import datetime

from flask import jsonify
from sqlalchemy import Integer, Column, CHAR, DateTime
from sqlalchemy.orm import relationship

from ovs import db


class Room(db.Model):
    """
    Defines a Room as represented in the database. Along with some utility functions.
    """
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True)
    number = Column(CHAR(255), unique=True)
    status = Column(CHAR(255), nullable=False)
    type = Column(CHAR(255), nullable=False)
    occupants = relationship('Resident', backref='rooms', lazy=False, cascade='all, delete, delete-orphan')
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        """
        Allows Room to be printed.
        Returns:
            str: A string representation of this Room.
        """
        return 'Room([id={id}, number={number}, status={status}, type={type}, created={created}, ' \
               'updated={updated}])'.format(**self.__dict__)

    def json(self):
        """
        Get a JSON object representing this Room.
        Returns:
             A JSON representation of this Room.
        """
        return jsonify(
            id=self.id,
            number=self.number,
            status=self.status,
            type=self.type,
            created=self.created,
            updated=self.updated
        )
