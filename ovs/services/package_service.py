""" DB and utility functions for Packages """
from ovs import db
from ovs.models.package_model import Package
from ovs.models.user_model import User
from ovs.services.user_service import UserService


class PackageService:
    """ DB and utility functions for Packages """

    def __init__(self):
        pass

    @staticmethod
    def create_package(recipient_id, checked_by, checked_at, description):
        """
        Creates a package db entry.

        Args:
            recipient_id: Unique user id of recipient.
            checked_by: Name of checker.
            checked_at: Time when the package was recieved by checker.
            description: A short description of the package.

        Returns:
            A Package db model.
        """
        new_package = Package(recipient_id=recipient_id, checked_by=checked_by,
                              checked_at=checked_at, description=description)
        db.session.add(new_package)
        db.session.flush()
        return new_package

    @staticmethod
    def get_package_by_id(package_id):
        """
        Fetch a package identified by the package id.

        Args:
            package_id: Unique package id.

        Returns:
            A Package db model.
        """

        return Package.query.filter_by(id=package_id).first()

    @staticmethod
    def update_package(package_id, recipient_email, description):
        """
        Updates the receiver and description of Package identified by package_id.

        Args:
            package_id: Unique package id.
            recipient_email: Recipient's email address.
            description: A short description of the package.
        """
        recipient_id = UserService.get_user_by_email(
            recipient_email).id

        db.session.query(Package)\
                  .filter_by(id=package_id)\
                  .update({Package.recipient_id: recipient_id, Package.description: description})
        db.session.flush()

    @staticmethod
    def delete_package(package_id):
        """
        Deletes Package identified by package_id.

        Args:
            package_id: Unique package id.

        Returns:
            If the package was deleted successfully.
        """
        package = PackageService.get_package_by_id(package_id)
        db.session.delete(package)

    @staticmethod
    def get_all_packages_recipients():
        """
        Fetch all related packages and recipients in db.

        Returns:
            A list of (Package, User) db model tuples.
        """
        return db.session.query(Package, User) \
            .join(User, Package.recipient_id == User.id).all()

    @staticmethod
    def get_all_packages_by_recipient(user_id):
        """
        Fetch all packages for a resident in db.

        Args:
            user_id: Unique resident id

        Returns:
            A list of Packages
        """
        return Package.query.filter_by(recipient_id=user_id)

    @staticmethod
    def delete_packages_for_user(user_id):
        """
        Deletes all packages for recipient user_id

        Args:
            user_id: Unique resident id.

        Returns:
            If the packages were deleted successfully.
        """
        packages = PackageService.get_all_packages_by_recipient(user_id)
        for package in packages:
            if not PackageService.delete_package(package.id):
                return False
        return True
