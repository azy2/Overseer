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
        """Checks user perms a given user_role and minimum access role"""
        permission_levels = {
            'ADMIN': 100,
            'OFFICE_MANAGER': 2,
            'BUILDING_MANAGER': 2,
            'RESIDENT_ADVISOR': 1,
            'STAFF': 1,
            'RESIDENT': 0,
        }

        return permission_levels[user_role] >= permission_levels[min_access_role]
