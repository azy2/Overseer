""" Services related to managers """
import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import aliased

from ovs import db
from ovs.models.package_model import Package
from ovs.models.resident_model import Resident
from ovs.models.user_model import User


class ManagerService:
    """ Services related to managers """

    def __init__(self):
        pass

    @staticmethod
    def get_all_residents_users():
        """
        Fetch all related residents and users in db.

        Returns:
            A list of (Resident, User) db model tuples.
        """
        try:
            return db.session.query(Resident, User).join(User, Resident.user_id == User.id).all()
        except SQLAlchemyError:
            logging.exception('Failed to fetch all residents.')
            return []

    @staticmethod
    def get_resident_by_id(user_id):
        """
        Fetch the resident identified by user_id.

        Args:
            user_id: Unique user id.

        Returns:
            A Resident db model.
        """
        try:
            return db.session.query(Resident).filter_by(user_id=user_id).first()
        except SQLAlchemyError:
            logging.exception('Failed to get resident by id.')

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
