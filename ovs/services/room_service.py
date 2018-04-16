"""
DB access and other services for Rooms
"""
import logging

from sqlalchemy.exc import SQLAlchemyError

from ovs import db
from ovs.models.room_model import Room
from ovs.services.resident_service import ResidentService
from ovs.services.user_service import UserService


class RoomService:
    """
    DB Access and utility methods for Rooms
    """

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
        try:
            db.session.add(new_room)
            db.session.commit()
        except SQLAlchemyError:
            logging.exception('Failed to create new room.')
            db.session.rollback()
            return None

        emails = ''.join(occupant_emails.split()).split(',')
        for email in emails:
            RoomService.add_resident_to_room(email, number)

        return new_room

    @staticmethod
    def delete_room(room_id):
        """
        Deletes a room from the database.

        Args:
            room_id: Unique room id.

        Returns:
            Whether the room was deleted succesfully
        """
        room = RoomService.get_room_by_id(room_id)
        if room is None:
            return False
        for occupant in room.occupants:
            user = UserService.get_user_by_id(occupant.user_id)
            RoomService.add_resident_to_room(user.email, 'None')
        try:
            db.session.delete(room)
            db.session.commit()
            return True
        except SQLAlchemyError:
            logging.exception('Failed to delete room')
            return False

    @staticmethod
    def edit_room(room_id, room_number, status, room_type):
        """
        Edits a room in the database.

        Args:
            room_id: Unique room id.
            room_number: New room number
            status: New room status string
            room_type: New room type string

        Returns:
            Whether the room was deleted succesfully
        """
        room = RoomService.get_room_by_id(room_id)
        if room is None:
            return False
        room.room_number = room_number
        room.status = status
        room.type = room_type

        try:
            db.session.commit()
            return True
        except SQLAlchemyError:
            logging.exception('Failed to edit room')
            return False

    @staticmethod
    def get_room_by_id(room_id):
        """
        Fetch a room identified by room id.

        Args:
            room_id: Unique room id.

        Returns:
            A Room db model.
        """
        try:
            return db.session.query(Room).filter_by(id=room_id).first()
        except SQLAlchemyError:
            logging.exception('Failed to get room by id.')
            return None

    @staticmethod
    def get_room_by_number(number):
        """
        Fetch a Room model by room number.

        Args:
            number: The room nmber.

        Returns:
            A Room db model.
        """
        number = str(number)
        try:
            return db.session.query(Room).filter_by(number=number).first()
        except SQLAlchemyError:
            logging.exception('Failed to get room by room number.')
            return None

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
        Fetch all rooms except the default in the db.

        Returns:
           A list of Room db models.
        """
        try:
            return db.session.query(Room).filter(Room.number != 'None').all()
        except SQLAlchemyError:
            logging.exception('Failed to get all rooms.')
            return []

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

        if resident is None or room is None:
            return False

        try:
            resident.room_number = room_number
            # occupants are updated automatically by mysql
            db.session.commit()
            return True
        except SQLAlchemyError:
            logging.exception('Failed to associated resident and room.')
            db.session.rollback()
            return False
