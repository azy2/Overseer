"""
DB access and other services for profiles
"""
import logging

from flask import current_app
from sqlalchemy.exc import SQLAlchemyError

from ovs import db
from ovs.models.profile_model import Profile
from ovs.services.profile_picture_service import ProfilePictureService
from ovs.services.resident_service import ResidentService


class ProfileService:
    """
    DB Access and utility methods for profiles
    """

    def __init__(self):
        pass

    @staticmethod
    def update_profile(resident_id, preferred_email=None, preferred_name=None,
                       phone_number=None, race=None, gender=None):
        """
        Updates a profile associated with resident identified by resident id.

        Args:
            resident_id: Unique resident id.
            preferred_email: Resident's preferred email.
            preferred_name: Resident's preferred name.
            phone_number: Resident's phone number.
            race: Resident's race.
            gender: Resident's gender.

        Returns:
            If the resident's profile was updated successfully.
        """
        resident = ResidentService.get_resident_by_id(resident_id)
        if resident is None:
            return False
        profile = resident.profile
        if preferred_email:
            profile.preferred_email = preferred_email
        if preferred_name:
            profile.preferred_name = preferred_name
        profile.phone_number = phone_number # I want to be able to set this to None
        profile.race = race # I want to be able to set this to None
        if gender:
            profile.gender = gender

        try:
            db.session.commit()
            return True
        except SQLAlchemyError:
            logging.exception('Failed to update resident profile.')
            db.session.rollback()
            return False

    @staticmethod
    def delete_profile(resident_id):
        """
        Deletes a profile associated with resident identified by resident id.

        Args:
            resident_id: Unique resident id.

        Returns:
            If the Profile db model was sucessfully deleted.
        """
        resident = ResidentService.get_resident_by_id(resident_id)
        if resident is None:
            return False
        profile = resident.profile
        picture_id = profile.picture_id
        ProfilePictureService.delete_profile_picture(picture_id)
        try:
            db.session.delete(profile)
            return True
        except SQLAlchemyError:
            logging.exception('Failed to delete resident profile.')
            return False

    @staticmethod
    def get_all_profiles():
        """
        Fetches all profiles.

        Returns:
            A list of Profile db models..
        """
        try:
            return db.session.query(Profile).all()
        except SQLAlchemyError:
            logging.exception('Failed to get all profiles.')

    @staticmethod
    def set_default_picture(picture_id):
        """
        Sets default picture for new residents.

        Args:
            picture_id: Profile db model picture id.
        """
        default_picture_path = current_app.config['BLOBSTORE']['DEFAULT_PATH']
        with open(default_picture_path, 'rb') as default_image:
            file_contents = default_image.read()
            file_bytes = bytearray(file_contents)
        ProfilePictureService.create_profile_picture(picture_id, file_bytes)
