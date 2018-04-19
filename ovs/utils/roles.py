"""
Enums for distinguishing object roles.
"""


class UserRole:
    """ User roles determine what permissions an account has. """

    def __init__(self):
        pass

    RESIDENT = 'RESIDENT'
    RESIDENT_ADVISOR = 'RESIDENT_ADVISOR'
    STAFF = 'STAFF'
    OFFICE_MANAGER = 'OFFICE_MANAGER'
    BUILDING_MANAGER = 'BUILDING_MANAGER'
    ADMIN = 'ADMIN'

    @staticmethod
    def has_permission(user_role, min_access_role):
        """
        Checks that user_role has permission to access recourse with permission level min_access_role.
        Args:
            user_role (UserRole): The current users role.
            min_access_role (UserRole): The minimum role that can access this recourse.

        Returns:
            bool: True if the user is above min_access_role, False otherwise.
        """
        permission_levels = {
            'ADMIN': 100,
            'OFFICE_MANAGER': 2,
            'BUILDING_MANAGER': 2,
            'RESIDENT_ADVISOR': 1,
            'STAFF': 1,
            'RESIDENT': 0,
        }

        return permission_levels[user_role] >= permission_levels[min_access_role]
