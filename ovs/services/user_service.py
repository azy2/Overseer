""" DB and utility functions for Users """
from ovs import app
from ovs.models.user_model import User
from ovs.services.resident_service import ResidentService
from ovs.utils import crypto
db = app.database.instance()


class UserService:
    """ DB and utility functions for Users """
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
        db.add(new_user)
        db.commit()
        if role == 'RESIDENT':
            ResidentService.create_resident(new_user.id)

        return new_user

    @staticmethod
    def get_user_by_email(email):
        """
        Gets a user by their email
        :param email: The email of the user
        :return: The db entry of that user
        """
        return db.query(User).filter(User.email == email)
