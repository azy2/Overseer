"""
Blob interface code.
"""
import os
from azure.storage.blob import BlockBlobService


class Blob:
    """
    Blob is the implementation for azure blob storage.
    """
    # The container name can only contain letters, chars or '-'
    PROFILE_PICTURE_CONTAINER = 'profile-picture'

    def __init__(self, app=None):
        """
        Initializes the Blob object. If app is not provided init_app must be called before use..

        Args:
            self: Blob object.
            app: Application to run with.
        """
        if app:
            self.init_app(app)

    def init_app(self, app):
        """
        Initializes the Blob object.

        Args:
            self: Blob object.
            app: Application to run with.
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
        Wraps create blob from bytes service.

        Args:
            self: Blob object.
            container: Name of container to store blob object inself.
            name: Name of blob object.
            byte_array: Bytes of object.
        """
        name = str(name)
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
        Wraps delete blob service.

        Args:
            self: Blob object.
            container: Name of blob container.
            name: Name of blob object.
        """
        name = str(name)
        if self._is_production:
            self._service.delete_blob(container, name)
        else:
            file_name = make_file_name(container, name)
            os.remove(file_name)

    def exists(self, container, name):
        """
        Wraps exists blob service.

        Args:
            self: Blob object.
            container: Name of blob container.
            name: Name of blob object.
        """
        name = str(name)
        if self._is_production:
            return self._service.exists(container, name)
        else:
            file_name = make_file_name(container, name)
            return os.path.isfile(file_name)

    def get_blob_to_bytes(self, container, name):
        """
        Wraps get blob to bytes service.

        Args:
            self: Blob object.
            container: Name of blob container.
            name: Name of blob object.
        """
        name = str(name)
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
    Builds filename for testing from container and id.

    Args:
        container: Name of blob container.
        name: Name of blob object.
    """
    name = str(name)
    return 'ovs/data/test/' + container + '/' + name


blob = Blob()
