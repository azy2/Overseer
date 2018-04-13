"""
ovs is the root module of the Overseer application. It sets up flask and makes
a database connection. The networking code can be found in `../main.py`
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app():
    """ Creates a Flask app instance and returns it """
    app = Flask(__name__)
    app.config.from_object('ovs.config.Config')

    with app.app_context():
        dbconfig = app.config['DATABASE']
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + \
                                                dbconfig['primary']['user'] + ':' + \
                                                dbconfig['primary']['password'] + '@' + \
                                                dbconfig['primary']['host'] + ':' + \
                                                dbconfig['primary']['port'] + '/' + \
                                                dbconfig['primary']['name']
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        db.init_app(app)
        import ovs.models  # pylint: disable=unused-variable
        db.create_all()

        from ovs.blob import blob
        blob.init_app(app)

        from ovs.models.user_model import bcrypt_app
        bcrypt_app.init_app(app)

        from ovs.services.auth_service import LOGIN_MANAGER
        LOGIN_MANAGER.init_app(app)
        LOGIN_MANAGER.login_view = 'auth.login'

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

        from ovs.datagen import DataGen
        DataGen.create_defaults()

        db.session.commit()

    return app
