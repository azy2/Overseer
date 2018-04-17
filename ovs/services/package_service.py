""" DB and utility functions for Packages """
from sqlalchemy.orm import aliased

from ovs import db
from ovs.models.package_model import Package
from ovs.models.user_model import User
from ovs.services.user_service import UserService


class PackageService:
    """ DB and utility functions for Packages """

    def __init__(self):
        pass

    @staticmethod
    def create_package(recipient_id, checked_by_id, checked_at, description):
        """
        Creates a package db entry.

        Args:
            recipient_id: Unique user id of recipient.
            checked_by_id: Unique user id of checker.
            checked_at: Time when the package was recieved by checker.
            description: A short description of the package.

        Returns:
            A Package db model.
        """
        new_package = Package(recipient_id=recipient_id, checked_by_id=checked_by_id,
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
        return db.session.query(Package).filter(Package.id == package_id).first()

    @staticmethod
    def update_package(package_id, recipient_email, description):
        """
        Updates the receiver and description of Package identified by package_id.

        Args:
            package_id: Unique package id.
            recipient_email: Recipient's email address.
            description: A short description of the package.

        Returns:
            If the package was updated successfully.
        """
        recipient_id = UserService.get_user_by_email(
            recipient_email).id

        db.session.query(Package)\
                  .filter_by(id=package_id)\
                  .update({Package.recipient_id: recipient_id, Package.description: description})
        db.session.flush()

    @staticmethod
    def get_all_packages_recipients_checkers():
        """
        Fetch all related packages, recipients, and checkers in db.

        Returns:
            A list of (Package, User, User) db model tuples.
        """
        recipient = aliased(User)
        checker = aliased(User)
        return db.session.query(Package, recipient, checker) \
            .join(recipient, Package.recipient_id == recipient.id) \
            .join(checker, Package.checked_by_id == checker.id).all()
