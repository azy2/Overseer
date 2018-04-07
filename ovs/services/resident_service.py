"""
DB and utility functions for Residents
"""
from flask import current_app
from ovs.models.profile_model import Profile
from ovs.services.profile_picture_service import ProfilePictureService
from ovs.models.resident_model import Resident
from ovs.utils import genders

db = current_app.extensions['database'].instance()


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
        new_resident_profile.gender = genders.UNSPECIFIED
        ResidentService.set_default_picture(new_resident_profile.picture_id)

        db.add(new_resident)
        db.add(new_resident_profile)
        db.commit()

        return new_resident

    @staticmethod
    def set_default_picture(picture_id):
        """
        Sets default picture for new residents
        """
        default_picture_path = current_app.config['BLOB']['default_picture_path']
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
