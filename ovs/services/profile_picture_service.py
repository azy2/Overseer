""" Services related to profile pictures """
from ovs import app
blob_instance = app.blob.instance()
container_name = app.blob.PROFILE_PICTURE_CONTAINER


class ProfilePictureService:
    """ Services related to profile pictures """

    @staticmethod
    def create_profile_picture(picture_id, picture):
    """
    Creates a blob object in the profile picture container with the associated id
    :param picture_id: UID of picture - needs to be unique
    :param picture: array of bytes
    """
    blob_instance.create_blob_from_bytes(container_name, picture_id, picture)

    @staticmethod
    def update_profile_picture(picture_id, picture):
    """ 
    Updates a blob object in the profile picture container with the associated id
    :param picture_id: UID of picture - needs to be unique
    :param picture: array of bytes
    """
    create_profile_picture(picture_id, picture)

    @staticmethod
    def delete_profile_picture(picture_id):
    """ Deletes a blob object in the profile picture container with the associated id """
    blob_instance.delete_blob(container_name, picture_id)

    @staticmethod
    def get_profile_picture(picture_id):
    """
    Gets a blob object in the profile picture container with the associated id
    Returns none if the picture_id does not exist
    """
    if not blob_instance.exists(container_name, picture_id):
        return none
    return blob_instance.get_blob_to_bytes(container_name, picture_id)
