"""
DB access and other services for Rooms
"""
import logging

from sqlalchemy.exc import SQLAlchemyError

from ovs import db
from ovs.models.room_model import Room
from ovs.services.resident_service import ResidentService


class RoomService:
    """
    DB Access and utility methods for Rooms
    """

    def __init__(self):
        pass

    @staticmethod
    def create_room(number, status, room_type, occupant_emails=''):
        """
        Create a room db entry.

        Args:
            number: The room number.
            status: Current room status.
            room_type: Room type.
            occupant_emails: Resident's email address seperated by ';'.

        Returns:
            A Room db model.
        """
        new_room = Room(number=number, status=status, type=room_type)
        db.session.add(new_room)

        emails = ''.join(occupant_emails.split()).split(',')
        for email in emails:
            RoomService.add_resident_to_room(email, number)

        return new_room

    @staticmethod
    def get_room_by_id(room_id):
        """
        Fetch a room identified by room id.

        Args:
            room_id: Unique room id.

        Returns:
            A Room db model.
        """
        return Room.query.filter_by(id=room_id).first()

    @staticmethod
    def get_room_by_number(number):
        """
        Fetch a Room model by room number.

        Args:
            number: The room nmber.

        Returns:
            A Room db model.
        """
        return Room.query.filter_by(number=str(number)).first()

    @staticmethod
    def room_exists(number):
        """
        Checks if a room identified by room number exits.

        Args:
            number: The room number.

        Returns:
            If a matching room exists.
        """
        return RoomService.get_room_by_number(number) is not None

    @staticmethod
    def get_all_rooms():
        """
        Fetch all rooms in the db.

        Returns:
           A list of Room db models.
        """
        return Room.query.all()

    @staticmethod
    def add_resident_to_room(email, room_number):
        """
        Associates a resident with a room. Updates resident's room number and occupants of room.

        Args:
            email: Resident's email address.
            room_number: The room number.

        Returns:
            If both resident and rooms were successfully updated.
        """
        resident = ResidentService.get_resident_by_email(email)
        room = RoomService.get_room_by_number(room_number)
        resident.room_number = room_number
