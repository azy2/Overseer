""" DB and utility functions for Packages """
from ovs import app
from ovs.models.package_model import Package
from ovs.services.user_service import UserService

db = app.database.instance()


class PackageService:
    """ DB and utility functions for Packages """

    def __init__(self):
        pass

    @staticmethod
    def create_package(recipient_id, checked_by_id, checked_at, description):
        """
        Creates a new package using the specified parameters
        :param recipient_id: The user ID of the recipient
        :param checked_by_id: The user ID of the individual who checked the package
        :param checked_at: The time at which that individual checked the package
        :param description: A description of the package
        :return: The db entry of the newly created package
        """
        new_package = Package(recipient_id=recipient_id, checked_by_id=checked_by_id,
                              checked_at=checked_at, description=description)
        db.add(new_package)
        db.commit()
        return new_package

    @staticmethod
    def get_package_by_id(package_id):
        """
        Gets a package by their id
        :param package_id: The package ID of the package
        :return: The db entry of that package
        """
        return db.query(Package).filter(Package.id == package_id)

    @staticmethod
    def update_package(package_id, recipient_email, description):
        """ Changes the receiver and description of Package identified by package_id """
        recipient_id = UserService.get_user_by_email(recipient_email).first().id
        db.query(Package) \
            .filter(Package.id == package_id) \
            .update({Package.recipient_id: recipient_id, Package.description: description})
        db.commit()
        return PackageService.get_package_by_id(package_id).first()
