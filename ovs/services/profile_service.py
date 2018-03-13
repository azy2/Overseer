"""
DB access and other services for profiles
"""
from ovs import app
from ovs.services.resident_service import ResidentService

db = app.database.instance()


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
        db.commit()
        return True
