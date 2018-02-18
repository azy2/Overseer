from flask_login import LoginManager

from ovs import app
from ovs.models.UserModel import User

db = app.database.instance()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(id):
    return db.query(User).get(int(id))
