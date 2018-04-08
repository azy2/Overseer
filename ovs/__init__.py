"""
ovs is the root module of the Overseer application. It sets up flask and makes
a database connection. The networking code can be found in `../main.py`
"""

import os

from flask import Flask
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()

def create_app():
    """ Creates a Flask app instance and returns it """
    app = Flask(__name__)
    app.config.from_object('ovs.config.Config')

    with app.app_context():
        from ovs.database import Database
        app.extensions['database'] = Database(app)

        from ovs.blob import Blob
        app.extensions['blob'] = Blob(app)

        from flask_sendgrid import SendGrid
        app.extensions['mail'] = SendGrid(app)

        from flask_bcrypt import Bcrypt
        app.extensions['bcrypt'] = Bcrypt(app)

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

    return app
