"""
ovs is the root module of the Overseer application. It sets up flask and makes
a database connection. The networking code can be found in `../main.py`
"""
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from ovs.config import OVSConfig

db = SQLAlchemy()


def create_app(config_path=None):
    """ Creates a Flask app instance and returns it """
    app = Flask(__name__)
    config = OVSConfig(config_path)
    for key, value in config.items():
        app.config[key] = value

    env = app.config['ENV']
    app.config['DEVELOPMENT'] = env == 'DEV'
    app.config['TESTING'] = env == 'TEST'
    app.config['PRODUCTION'] = env == 'PROD'

    with app.app_context():
        db_config = app.config['DATABASE']
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + \
                                                db_config['USER'] + ':' + \
                                                db_config['PASSWORD'] + '@' + \
                                                db_config['HOSTNAME'] + ':' + \
                                                db_config['PORT'] + '/' + \
                                                db_config['NAME']
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        db.init_app(app)
        import ovs.models  # pylint: disable=unused-variable
        db.create_all()

        from ovs.blob import blob
        blob.init_app(app)

        from ovs.models.user_model import bcrypt_app
        bcrypt_app.init_app(app)

        from ovs.utils import serializer
        serializer.init_app(app)

        from ovs.services.auth_service import LOGIN_MANAGER
        LOGIN_MANAGER.init_app(app)
        LOGIN_MANAGER.login_view = '/'
        LOGIN_MANAGER.login_message_category = 'danger'

        from flask_wtf.csrf import CSRFProtect
        csrf = CSRFProtect()
        csrf.init_app(app)

        from ovs import routes
        app.register_blueprint(routes.OvsRoutes, url_prefix='/')
        app.register_blueprint(routes.AdminRoutes, url_prefix='/admin')
        app.register_blueprint(routes.ManagerRoutes, url_prefix='/manager')
        app.register_blueprint(routes.ResidentRoutes, url_prefix='/resident')
        app.register_blueprint(routes.AuthRoutes, url_prefix='/auth')
        app.register_blueprint(routes.DevRoutes, url_prefix='/dev')

        if os.environ.get("WERKZEUG_RUN_MAIN") == "true" or os.environ.get("FLASK_DEBUG") != "True":
            from ovs.datagen import DataGen
            DataGen.create_defaults()

        db.session.commit()

    return app
