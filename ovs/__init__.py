"""
ovs is the root module of the Overseer application. It sets up flask and makes
a database connection. The networking code can be found in `../main.py`
"""

from flask import Flask
from flask_bcrypt import Bcrypt

from sqlalchemy.ext.declarative import declarative_base

from ovs.database import Database

app = Flask(__name__)
app.config.from_object('ovs.config.Config')
app.database = Database(app)
app.BaseModel = declarative_base()

bcrypt_app = Bcrypt(app)

# import at bottom to avoid circular dependencies
import ovs.services.auth_service
from .datagen import DataGen
