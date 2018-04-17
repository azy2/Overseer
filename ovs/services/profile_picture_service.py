""" Services related to profile pictures """
from ovs.blob import blob

CONTAINER = blob.PROFILE_PICTURE_CONTAINER


class ProfilePictureService:
    """ Services related to profile pictures """

    @staticmethod
    def create_profile_picture(picture_id, picture):
        """
        Creates a blob object in the profile picture container with the associated id.

        Args:
            picture_id: ID of picture.
            picture: Array of bytes.
        """
        blob.create_blob_from_bytes(CONTAINER, picture_id, picture)

    @staticmethod
    def update_profile_picture(picture_id, picture):
        """
        Updates a blob object in the profile picture container with the associated id.

        Args:
            picture_id: ID of picture.
            picture: Array of bytes.
        """
        blob.delete_blob(CONTAINER, picture_id)
        blob.create_blob_from_bytes(CONTAINER, picture_id, picture)

    @staticmethod
    def delete_profile_picture(picture_id):
        """
        Deletes a blob object in the profile picture container with the associated id.

        Args:
            picture_id: ID of picture.
        """
        blob.delete_blob(CONTAINER, picture_id)

    @staticmethod
    def get_profile_picture(picture_id):
        """
        Gets a blob object in the profile picture container with the associated id.

        Args:
            picture_id: ID of picture.

        Returns:
            Array of bytes.
        """
        if not blob.exists(CONTAINER, picture_id):
            return None
        return blob.get_blob_to_bytes(CONTAINER, picture_id)
