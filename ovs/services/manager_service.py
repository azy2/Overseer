""" DB and utility functions for Managers """
from ovs.models.user_model import User
from ovs.models.room_model import Room
from ovs.services.room_service import RoomService
from ovs.services.resident_service import ResidentService
from ovs.services.package_service import PackageService
from ovs.utils import roles
from datetime import datetime as dt

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

    @staticmethod
    def get_empty_room_nums():
        """
        Gets a list of lists of length 2 with room type and number of empty rooms of that type.

        Returns:
            List of lists of length 2 of form (room type, number empty rooms of this type).
        """

        # Get all rooms, sort them, and filter out the non-empty ones
        all_rooms = RoomService.get_all_rooms()
        # Currently just sorting rooms by type alphabetically
        sorted_rooms = sorted(all_rooms, key=lambda room: room.type)
        empty_rooms = [room for room in sorted_rooms if len(room.occupants) == 0]

        # Get aggregate list of empty rooms with the types of rooms and number of rooms empty of that type
        empty_room_nums = []
        for room in empty_rooms:
            type_pair = next((pair for pair in empty_room_nums if pair[0] == room.type), None)
            if type_pair:
                type_pair_idx = empty_room_nums.index(type_pair)
                empty_room_nums[type_pair_idx][1] += 1
            else:
                empty_room_nums.append([room.type, 1])

        return empty_room_nums

    @staticmethod
    def get_num_residents():
        """
        Gets the number of residents.

        Returns:
            Number of residents.
        """
        return len(ResidentService.get_all_residents_users())

    @staticmethod
    def get_package_info():
        """
        Gets the number of packages checked in today and total number of packages awaiting pickup.

        Returns:
            Number of packages checked in today and total number of packages.
        """
        all_packages = PackageService.get_all_packages()
        total_num_packages = len(all_packages)
        today = dt.today()
        today_packages = [pkg for pkg in all_packages if pkg.checked_at.day == today.day
                                                     and pkg.checked_at.month == today.month
                                                     and pkg.checked_at.year == today.year]
        today_num_packages = len(today_packages)
        return today_num_packages, total_num_packages
