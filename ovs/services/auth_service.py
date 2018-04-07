"""
Service routines and db access for the Auth layer
"""
from flask_login import LoginManager
from flask import current_app
from ovs.models.user_model import User

db = current_app.extensions['database'].instance()

LOGIN_MANAGER = LoginManager()

class AuthService:
    """Contains application methods relevant to the Authentication layer"""
    @staticmethod
    @LOGIN_MANAGER.user_loader
    def load_user(user_id):
        """ Get a user by their id """
        return db.query(User).get(int(user_id))

    @staticmethod
    def verify_auth(user, password):
        """verifies a given users password"""
        return user.has_password(password)
