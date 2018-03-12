"""
Blob interface code
"""
from azure.storage.blob import BlockBlobService

class Blob():
    """
    Blob is the implementation for azure blob storage
    """
    def __init__(self, app):
        blob_config = app.config['BLOB']
        self._service = BlockBlobService(account_name = blob_config['account'],
            account_key = blob_config['key'])
        self._profile_container = self._service.create_container('profile_picture')

    def profile_container(self):
        """ Get a handle to the profile blob container """
        return self._profile_container
