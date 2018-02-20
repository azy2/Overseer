"""
DB access and other services for Rooms
"""
from ovs import app
from ovs.models.room_model import Room
from ovs.models.resident_model import Resident
from ovs.services.user_service import UserService
db = app.database.instance()


class RoomService:
    """
    DB Access and utility methods for Rooms
    """
    @staticmethod
    def create_room(number, status, room_type):
        """ Adds a room to the database """
        new_room = Room(number=number, status=status, type=room_type)
        db.add(new_room)
        db.commit()
        return new_room

    @staticmethod
    def get_room_by_id(room_id):
        """
        Get a Room from it's id
        :param room_id: The Room's id
        :return: The Room
        """
        return db.query(Room).filter(Room.id == room_id)

    @staticmethod
    def get_room_by_number(number):
        """
        Get a room from it's number
        :param number: The room number
        :return: The Room
        """
        return db.query(Room).filter(Room.number == number)

    @staticmethod
    def add_resident_to_room(email, number):
        """
        Associates a Resident to a room. This involves adding the room
        to the Residents table and adding the resident to the Rooms table.
        """
        # TODO: change below code to pull from residents table once it is
        # implemented to mirror the users table automatically

        user = UserService.get_user_by_email(email).first()

        new_resident = Resident(user_id=user.id, room_number=number)
        db.add(new_resident)
        db.commit()
        return new_resident
