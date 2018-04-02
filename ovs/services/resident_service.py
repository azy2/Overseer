"""
DB and utility functions for Residents
"""
from sqlalchemy import exc

from ovs import app
from ovs.models.profile_model import Profile
from ovs.models.resident_model import Resident
from ovs.services.profile_picture_service import ProfilePictureService

db = app.database.instance()

class ResidentService:
    """ DB and utility functions for Residents """

    def __init__(self):
        pass

    @staticmethod
    def create_resident(new_user, room_number=None):
        """
        Adds a User to the Resident table
        """
        new_resident = Resident(new_user.id, room_number)
        new_resident_profile = Profile(new_user.id)
        new_resident_profile.preferred_name = new_user.first_name
        new_resident_profile.preferred_email = new_user.email
        ResidentService.set_default_picture(new_resident_profile.picture_id)

        db.add(new_resident)
        db.add(new_resident_profile)
        db.commit()

        return new_resident

    @staticmethod
    def edit_resident(user_id, email, first_name, last_name, room_number):
        """
        Edits an existing resident
        """
        from ovs.services.user_service import UserService
        success = UserService.edit_user(user_id, email, first_name, last_name)
        if success:
            success = ResidentService.update_resident_room_number(user_id, room_number) is not None
        return success

    @staticmethod
    def delete_resident(user_id):
        """
        Deletes an existing resident
        """
        from ovs.services.profile_service import ProfileService
        ProfileService.delete_profile(user_id)
        resident = ResidentService.get_resident_by_id(user_id)
        db.delete(resident)


    @staticmethod
    def set_default_picture(picture_id):
        """
        Sets default picture for new residents
        """
        default_picture_path = app.config['BLOB']['default_picture_path']
        with open(default_picture_path, 'rb') as default_image:
            file_contents = default_image.read()
            file_bytes = bytearray(file_contents)
        ProfilePictureService.create_profile_picture(picture_id, file_bytes)

    @staticmethod
    def get_resident_by_id(user_id):
        """
        Returns the resident given by user_id
        """
        return db.query(Resident).filter(Resident.user_id == user_id)


    @staticmethod
    def update_resident_room_number(user_id, room_number):
        """ Changes the room_number of Resident identified by user_id """
        from ovs.services.room_service import RoomService
        room = RoomService.get_room_by_number(room_number).first()
        if room is None:
            return None
        # Todo: Catch specific exceptions for join and update
        try:
            db.query(Resident).filter(Resident.user_id == user_id).update({Resident.room_number: room_number})
            db.commit()
        except exc.SQLAlchemyError:
            db.rollback()
            return None
        return ResidentService.get_resident_by_id(user_id).first()
