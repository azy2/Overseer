"""
DB access and other services for Rooms
"""
from sqlalchemy import exc

from ovs import db
from ovs.models.room_model import Room
from ovs.services.resident_service import ResidentService
from ovs.services.user_service import UserService


class RoomService:
    """
    DB Access and utility methods for Rooms
    """

    def __init__(self):
        pass

    @staticmethod
    def create_room(number, status, room_type, occupants=''):
        """ Adds a room to the database """
        new_room = Room(number=number, status=status, type=room_type)
        try:
            db.session.add(new_room)
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
            return None

        emails = ''.join(occupants.split()).split(',')
        for email in emails:
            RoomService.add_resident_to_room(email, number)

        return new_room

    @staticmethod
    def get_room_by_id(room_id):
        """
        Get a Room from it's id
        :param room_id: The Room's id
        :return: The Room
        """
        return db.session.query(Room).filter(Room.id == room_id)

    @staticmethod
    def get_room_by_number(number):
        """
        Get a room from it's number
        :param number: The room number
        :return: The Room
        """
        return db.session.query(Room).filter(Room.number == number)

    @staticmethod
    def get_all_rooms():
        """
        Get all the rooms in the database
        """
        return db.session.query(Room).all()

    @staticmethod
    def add_resident_to_room(email, room_number):
        """
        Associates a Resident to a room. This involves adding the room
        to the Residents table and adding the resident to the Rooms table.
        """
        user = UserService.get_user_by_email(email).first()
        if user is None:
            return {'message': 'Email provided is not valid', 'status': False}
        if user.role == "RESIDENT":
            resident = ResidentService.get_resident_by_id(user.id).first()
            resident.room_number = room_number
            try:
                db.session.commit()
                return {'message': 'Success', 'status': True}
            except exc.SQLAlchemyError:
                db.session.rollback()
                return {'message': 'Failed to updated room number', 'status': False}
        return {'message': 'User role is not resident', 'status': False}
