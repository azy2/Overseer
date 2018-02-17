from ovs import app
from ovs.models.UserModel import User
from ovs.utils import crypto
db = app.database.instance()

class UserService:
    @staticmethod
    def create_user(email, password, role):
        new_user = User(email, password, role)
        db.add(new_user)
        db.commit()

        return new_user

    def create_user_password(email, role):
        new_user = User(email, crypto.generate_password(), role)
        db.add(new_user)
        db.commit()

        return new_user

    @staticmethod
    def get_user_by_email(email):
        return db.query(User).filter(User.email == email)

    # TODO get a user by id, etc...
