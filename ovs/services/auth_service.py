"""
Service routines and db access for the Auth layer
"""
from flask_login import LoginManager

from ovs import db
from ovs.models.user_model import User


LOGIN_MANAGER = LoginManager()

class AuthService:
    """Contains application methods relevant to the Authentication layer"""
    @staticmethod
    @LOGIN_MANAGER.user_loader
    def load_user(user_id):
        """ Get a user by their id """
        return db.session.query(User).get(int(user_id))

    @staticmethod
    def verify_auth(user, password):
        """verifies a given users password"""
        return user.has_password(password)
