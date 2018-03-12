""" Services related to profile pictures """
from ovs import app
from ovs.models.user_model import User
from ovs.models.resident_model import Resident
from ovs.services.resident_service import ResidentService
profile_container = app.blob.profile_container()


class ProfilePictureService:
    """ Services related to profile pictures """

    @staticmethod
    def create_profile_picture(picture_id, picture):
    """ Creates a blob object in the profile picture container with the associated id """

    @staticmethod
    def update_profile_picture(picture_id, picture):
    """ Updates a blob object in the profile picture container with the associated id """

    @staticmethod
    def delete_profile_picture(picture_id):
    """ Deletes a blob object in the profile picture container with the associated id """

    @staticmethod
    def get_profile_picture(picture_id):
    """ Gets a blob object in the profile picture container with the associated id """
