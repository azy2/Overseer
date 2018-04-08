""" DB and utility functions for Packages """
from flask import current_app
from sqlalchemy.orm import aliased

from ovs.models.package_model import Package
from ovs.models.user_model import User
from ovs.services.user_service import UserService

db = current_app.extensions['database'].instance()


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

    @staticmethod
    def get_all_packages_recipients_checkers():
        """
        Join based on user_id
        :return: Lists of residents, users tuples
        :rtype: [(Resident(...), User(...)), ...]
        """
        user_1 = aliased(User)
        user_2 = aliased(User)
        return db.query(Package, user_1, user_2) \
            .join(user_1, Package.recipient_id == user_1.id) \
            .join(user_2, Package.checked_by_id == user_2.id).all()
