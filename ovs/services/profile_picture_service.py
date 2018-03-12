""" Services related to profile pictures """
from ovs import app
profile_container = app.blob.instance()


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
