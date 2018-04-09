"""
DB access and other services for profiles
"""
from ovs import db
from ovs.models.profile_model import Profile
from ovs.services.resident_service import ResidentService
from ovs.services.profile_picture_service import ProfilePictureService


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
        Updates a user's profile information
        """
        resident = ResidentService.get_resident_by_id(resident_id).one_or_none()
        if resident is None:
            return False
        profile = resident.profile
        if preferred_email:
            profile.preferred_email = preferred_email
        if preferred_name:
            profile.preferred_name = preferred_name
        if phone_number:
            profile.phone_number = phone_number
        if race:
            profile.race = race
        if gender:
            profile.gender = gender
        db.session.commit()
        return True

    @staticmethod
    def delete_profile(resident_id):
        """
        Deletes a user's profile information
        """
        resident = ResidentService.get_resident_by_id(resident_id).one_or_none()
        if resident is None:
            return False
        profile = resident.profile
        picture_id = profile.picture_id
        ProfilePictureService.delete_profile_picture(picture_id)
        db.session.delete(profile)
        return True

    @staticmethod
    def get_all_profiles():
        """ Returns all profiles. Used only for testing """
        return db.session.query(Profile).all()
