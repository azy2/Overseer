""" Services related to profile pictures """
from flask import current_app
from ovs.blob import blob

CONTAINER = blob.PROFILE_PICTURE_CONTAINER

class ProfilePictureService:
    """ Services related to profile pictures """

    @staticmethod
    def create_profile_picture(user_id, picture):
        """
        Creates a blob object in the profile picture container with the associated id.

        Args:
            user_id: UUID of user.
            picture: Array of bytes.
        """
        blob.create_blob_from_bytes(CONTAINER, user_id, picture)

    @staticmethod
    def update_profile_picture(user_id, picture):
        """
        Updates a blob object in the profile picture container with the associated id.

        Args:
            user_id: UUID of user.
            picture: Array of bytes.
        """
        blob.delete_blob(CONTAINER, user_id)
        blob.create_blob_from_bytes(CONTAINER, user_id, picture)

    @staticmethod
    def delete_profile_picture(user_id):
        """
        Deletes a blob object in the profile picture container with the associated id.

        Args:
            user_id: UUID of user.
        """
        blob.delete_blob(CONTAINER, user_id)

    @staticmethod
    def get_profile_picture(user_id):
        """
        Gets a blob object in the profile picture container with the associated id.

        Args:
            user_id: UUID of user.

        Returns:
            Array of bytes.
        """
        if not blob.exists(CONTAINER, user_id):
            return None
        return blob.get_blob_to_bytes(CONTAINER, user_id)

    @staticmethod
    def set_default_picture(user_id):
        """
        Sets default picture for new residents.

        Args:
            user_id: Profile db model user id.
        """
        default_picture_path = current_app.config['BLOBSTORE']['DEFAULT_PATH']
        with open(default_picture_path, 'rb') as default_image:
            file_contents = default_image.read()
            file_bytes = bytearray(file_contents)
        ProfilePictureService.create_profile_picture(user_id, file_bytes)
