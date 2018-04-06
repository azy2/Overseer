""" Services related to profile pictures """
from flask import current_app
CONTAINER = current_app.extensions['blob'].PROFILE_PICTURE_CONTAINER


class ProfilePictureService:
    """ Services related to profile pictures """

    @staticmethod
    def create_profile_picture(picture_id, picture):
        """
        Creates a blob object in the profile picture container with the associated id
        :param picture_id: UID of picture - needs to be unique
        :param picture: array of bytes
        """
        current_app.extensions['blob'].create_blob_from_bytes(CONTAINER, picture_id, picture)

    @staticmethod
    def update_profile_picture(picture_id, picture):
        """
        Updates a blob object in the profile picture container with the associated id
        :param picture_id: UID of picture - needs to be unique
        :param picture: array of bytes
        """
        current_app.extensions['blob'].delete_blob(CONTAINER, picture_id)
        current_app.extensions['blob'].create_blob_from_bytes(CONTAINER, picture_id, picture)

    @staticmethod
    def delete_profile_picture(picture_id):
        """ Deletes a blob object in the profile picture container with the associated id """
        current_app.extensions['blob'].delete_blob(CONTAINER, picture_id)

    @staticmethod
    def get_profile_picture(picture_id):
        """
        Gets a blob object in the profile picture container with the associated id
        Returns none if the picture_id does not exist
        """
        if not current_app.extensions['blob'].exists(CONTAINER, picture_id):
            return None
        return current_app.extensions['blob'].get_blob_to_bytes(CONTAINER, picture_id)
