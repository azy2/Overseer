""" DB and utility functions for Users """
from sqlalchemy import exc

from ovs import app
from ovs.models.user_model import User
from ovs.services.mail_service import send_account_creation_email
from ovs.services.meal_service import MealService
from ovs.services.resident_service import ResidentService
from ovs.utils import crypto

db = app.database.instance()


class UserService:
    """ DB and utility functions for Users """

    def __init__(self):
        pass

    @staticmethod
    def create_user(email, first_name, last_name, role, password=None):
        """
        Adds a new user to the DB and generates a random password
        for them if none is provided
        :param email: The User's email
        :param first_name: The User's first name
        :param last_name: The User's last name
        :param role: The User's role. See `ovs.utils.roles`
        :param password: The User's password. If none is provided a
        random one will be generated
        :return: The newly created User
        """
        if password is None:
            password = crypto.generate_password()
        new_user = User(email, first_name, last_name, password, role)
        try:
            db.add(new_user)
            db.commit()
        except exc.IntegrityError:
            db.rollback()
            return None
        if role == 'RESIDENT':
            ResidentService.create_resident(new_user)

        send_account_creation_email(email, first_name, last_name, role)
        return new_user

    @staticmethod
    def get_user_by_email(email):
        """
        Gets a user by their email
        :param email: The email of the user
        :return: The db entry of that user
        """
        return db.query(User).filter(User.email == email)

    @staticmethod
    def get_user_by_id(user_id):
        """
        Gets a user by their id
        """
        return db.query(User).filter(User.id == user_id)

    @staticmethod
    def create_meal_plan_for_user_by_email(pin, meal_plan, plan_type, email):
        """
        Adds a new meal plan to the DB
        :param email: User to link to, TODO:implement
        :param pin: The plan's pin
        :param meal_plan: The plan's maximum credit count
        :param plan_type: The plan's reset period
        :return: True for success, False for failure
        """
        valid = MealService.create_meal_plan(pin, meal_plan, plan_type)
        valid = False
        if valid:
            db.query(User).filter(User.email == email).update(
                {User.meal_plan: pin})
            db.commit()
        return valid
