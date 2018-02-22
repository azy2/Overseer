"""
Enums for distinguishing object roles.
"""
class UserRole:
    """ User roles determine what permissions an account has. """
    RESIDENT = 'RESIDENT'
    RESIDENT_ADVISOR = 'RESIDENT_ADVISOR'
    STAFF = 'STAFF'
    OFFICE_MANAGER = 'OFFICE_MANAGER'
    BUILDING_MANAGER = 'BUILDING_MANAGER'
    ADMIN = 'ADMIN'
