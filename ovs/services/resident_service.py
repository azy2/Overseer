"""
DB and utility functions for Residents
"""
from sqlalchemy import exc

from ovs import app
from ovs.models.user_model import User
from ovs.models.resident_model import Resident
from ovs.models.profile_model import Profile
from ovs.services.profile_picture_service import ProfilePictureService
from ovs.services.meal_service import MealService
# from ovs.services.user_service import UserService

db = app.database.instance()


class ResidentService:
    """ DB and utility functions for Residents """

    def __init__(self):
        pass

    @staticmethod
    def create_resident(new_user, room_number=None):
        """
        Adds a User to the Resident table
        """
        new_resident = Resident(new_user.id, room_number)
        new_resident_profile = Profile(new_user.id)
        new_resident_profile.preferred_name = new_user.first_name
        new_resident_profile.preferred_email = new_user.email
        ResidentService.set_default_picture(new_resident_profile.picture_id)

        db.add(new_resident)
        db.add(new_resident_profile)
        db.commit()

        return new_resident

    @staticmethod
    def set_default_picture(picture_id):
        """
        Sets default picture for new residents
        """
        default_picture_path = app.config['BLOB']['default_picture_path']
        with open(default_picture_path, 'rb') as default_image:
            file_contents = default_image.read()
            file_bytes = bytearray(file_contents)
        ProfilePictureService.create_profile_picture(picture_id, file_bytes)

    @staticmethod
    def get_resident_by_email(email):
        """
        Gets a user by their email
        :param email: The email of the user
        :return: The db entry of that user
        """
        user_resident = db.query(User, Resident).join(Resident, User.id == Resident.user_id).filter(User.email == email)
        if user_resident is None:
            return None
        return user_resident.first()[1]

    @staticmethod
    def get_resident_by_id(user_id):
        """
        Returns the resident given by user_id
        """
        return db.query(Resident).filter(Resident.user_id == user_id)

    @staticmethod
    def get_resident_by_pin(pin):
        """
        Returns the resident given pin
        """
        return db.query(Resident).filter(Resident.mealplan_pin == pin).first()

    @staticmethod
    def set_resident_pin(user_id, new_pin):
        """
        Returns the resident given by user_id
        """
        try:
            db.query(Resident).filter(Resident.user_id == user_id).update({Resident.mealplan_pin: new_pin})
            db.commit()
        except exc.SQLAlchemyError:
            db.rollback()
            return False
        return True

    @staticmethod
    def create_meal_plan_for_resident_by_email(pin, meal_plan, plan_type, email):  # pylint: disable=unused-argument
        """
        Adds a new meal plan to the DB
        :param email: User to link to, TODO:implement
        :param pin: The plan's pin
        :param meal_plan: The plan's maximum credit count
        :param plan_type: The plan's reset period
        :return: True for success, False for failure
        """
        # Verify resident exists
        resident = ResidentService.get_resident_by_email(email)
        if resident == None:
            return False

        # Add PIN to resident
        pin_updated = ResidentService.set_resident_pin(resident.user_id, pin)
        if pin_updated == False:
            return False
        
        # Create mealplan
        mealplan_created = MealService.create_meal_plan(pin, meal_plan, plan_type)
        if mealplan_created == False:
            return False

        # Success
        return True