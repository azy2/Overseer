"""
Blob interface code
"""
import os
from azure.storage.blob import BlockBlobService


class Blob:
    """
    Blob is the implementation for azure blob storage.

    Args:
        app: The current Flask app. If not provided init_app must be called before using this object.

    Returns:
        A `Blob` object.
    """

    # The container name can only contain letters, chars or '-'
    PROFILE_PICTURE_CONTAINER = 'profile-picture'

    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        """
        Initializes the Blob object.

        Args:
            app: The currently running Flask app.
        """
        self.app = app
        self._is_production = self.app.config['PRODUCTION']
        if self._is_production:
            blob_config = self.app.config['BLOBSTORE']
            self._service = BlockBlobService(account_name=blob_config['ACCOUNT'],
                                             account_key=blob_config['ACCOUNT_KEY'])
            if not self._service.exists(self.PROFILE_PICTURE_CONTAINER):
                self._service.create_container(self.PROFILE_PICTURE_CONTAINER)

    def create_blob_from_bytes(self, container, name, byte_array):
        """
        Wraps create blob from bytes service if in production. Otherwise saves the data to disk.

        Args:
            container: The azure blob service container.
            name: The name of the blob.
            byte_array: The data to be put in the blob.
        """
        if self._is_production:
            self._service.create_blob_from_bytes(container, name, bytes(byte_array))
        else:
            # this just saves the file locally, used for dev and testing
            file_name = make_file_name(container, name)
            if not os.path.exists(os.path.dirname(file_name)):
                os.makedirs(os.path.dirname(file_name))
            with open(file_name, "wb") as blob_file:
                blob_file.write(byte_array)

    def delete_blob(self, container, name):
        """
        Wraps delete blob service if in production. Otherwise deletes the data from disk.

        Args:
            container: The container which contains the blob.
            name: The name of the blob in the container.
        """
        if self._is_production:
            self._service.delete_blob(container, name)
        else:
            file_name = make_file_name(container, name)
            os.remove(file_name)

    def exists(self, container, name):
        """
        Wraps exists blob service if in production. Otherwise check if the file is on disk.

        Args:
            container: The container where the blob resides.
            name: The name of the blob.

        Returns:
            bool: Whether the blob exits.
        """
        if self._is_production:
            return self._service.exists(container, name)

        file_name = make_file_name(container, name)
        return os.path.isfile(file_name)

    def get_blob_to_bytes(self, container, name):
        """
        Wraps get blob to bytes service.

        Args:
            container: The container where the blob resides.
            name: The name of the blob.

        Returns:
            bytearray: The data contained in the blob.
        """
        if self._is_production:
            return bytearray(self._service.get_blob_to_bytes(container, name).content)
        else:
            if not self.exists(container, name):
                return None
            file_name = make_file_name(container, name)
            with open(file_name, "rb") as blob_file:
                file_contents = blob_file.read()
                file_bytes = bytearray(file_contents)
            return file_bytes


def make_file_name(container, name):
    """
    Builds filename for testing and dev from container and id.

    Args:
        container: The container.
        name: The blob name.

    Returns:
        A file path representing the blob.
    """
    return 'ovs/data/test/' + container + '/' + name


blob = Blob()
