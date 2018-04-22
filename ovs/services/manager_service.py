""" DB and utility functions for Managers """
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
        return User.query.filter(User.role != roles.RESIDENT).all()

    @staticmethod
    def get_admin_count():
        """
        Gets the number of system admins.

        Returns:
            Number of admin users.
        """
        return User.query.filter_by(role=roles.ADMIN).count()
