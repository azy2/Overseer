"""
Service routines and db access for the Auth layer
"""
from flask_login import LoginManager
from ovs import app
from ovs.models.user_model import User

db = app.database.instance()

LOGIN_MANAGER = LoginManager()
LOGIN_MANAGER.init_app(app)
LOGIN_MANAGER.login_view = 'auth.login'

class AuthService:

    @staticmethod
    @LOGIN_MANAGER.user_loader
    def load_user(user_id):
        """ Get a user by their id """
        return db.query(User).get(int(user_id))

    @staticmethod
    def verify_auth(user, password):
        return user.has_password(password)
