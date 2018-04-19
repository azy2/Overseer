"""
DB access and other services for profiles
"""
from flask import current_app

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
        profile = resident.profile
        if preferred_email:
            profile.preferred_email = preferred_email
        if preferred_name:
            profile.preferred_name = preferred_name
        profile.phone_number = phone_number # I want to be able to set this to None
        profile.race = race # I want to be able to set this to None
        if gender:
            profile.gender = gender

        db.session.flush()
        db.session.refresh(profile)

    @staticmethod
    def get_all_profiles():
        """
        Fetches all profiles.

        Returns:
            A list of Profile db models.
        """
        return db.session.query(Profile).all()
