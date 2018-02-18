from ovs import app
from ovs.models.UserModel import User
from ovs.utils import crypto
db = app.database.instance()

class UserService:
    @staticmethod
    def create_user(email, first_name, last_name, role, password=None):
        if password is None:
            password = crypto.generate_password()
        new_user = User(email, first_name, last_name, password, role)
        db.add(new_user)
        db.commit()

        return new_user

    @staticmethod
    def get_user_by_email(email):
        return db.query(User).filter(User.email == email)

    # TODO get a user by id, etc...
