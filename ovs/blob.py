"""
Blob interface code
"""
from azure.storage.blob import BlockBlobService

class Blob():
    """
    Blob is the implementation for azure blob storage
    """
    #The container name can only contain letters, chars or '-'
    PROFILE_PICTURE_CONTAINER = 'profile-picture'
    def __init__(self, app):
        blob_config = app.config['BLOB']
        self._service = BlockBlobService(account_name=blob_config['account'],
                                         account_key=blob_config['key'])
        if not self._service.exists(self.PROFILE_PICTURE_CONTAINER):
            self._service.create_container(self.PROFILE_PICTURE_CONTAINER)

    def instance(self):
        """ Get a handle to the profile blob container """
        return self._service
