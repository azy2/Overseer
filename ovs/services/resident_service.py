"""
DB and utility functions for Residents
"""
from ovs import app
from ovs.models.resident_model import Resident
from ovs.models.profile_model import Profile
db = app.database.instance()


class ResidentService:
    """ DB and utility functions for Residents """
    @staticmethod
    def create_resident(user_id, room_number=None):
        """
        Adds a User to the Resident table
        """
        new_resident = Resident(user_id, room_number)
        new_resident_profile = Profile(user_id)
        db.add(new_resident)
        db.add(new_resident_profile)
        db.commit()

        return new_resident

    @staticmethod
    def get_resident_by_id(user_id):
        """
        Returns the resident given by user_id
        """
        return db.query(Resident).filter(Resident.user_id == user_id)
