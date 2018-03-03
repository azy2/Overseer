""" DB and utility functions for Packages """
from ovs import app
from ovs.models.package_model import Package
db = app.database.instance()


class PackageService:
    """ DB and utility functions for Packages """
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