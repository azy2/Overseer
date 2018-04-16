""" DB and utility functions for Managers """
import logging

from sqlalchemy.exc import SQLAlchemyError

from ovs import db
from ovs.models.user_model import User
from ovs.utils import roles

class ManagerService:
    """ DB and utility functions for Managers """

    @staticmethod
    def get_all_managers():
        """
        Fetch all users that are not residents from the db.

        Returns:
            A list of User model tuples.
        """
        try:
            return db.session.query(User).filter(User.role != roles.RESIDENT).all()
        except SQLAlchemyError:
            logging.exception('Failed to fetch all managers.')
            return []

    @staticmethod
    def get_admin_count():
        """
        Gets the number of system admins

        Returns:
            Number of admin users
        """
        try:
            return db.session.query(User).filter(User.role == roles.ADMIN).count()
        except SQLAlchemyError:
            logging.exception('Failed to count admins')
            return 0
