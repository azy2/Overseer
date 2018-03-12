"""
ovs is the root module of the Overseer application. It sets up flask and makes
a database connection. The networking code can be found in `../main.py`
"""

from flask import Flask
from sqlalchemy.ext.declarative import declarative_base

from ovs.database import Database
from ovs.blob import Blob

app = Flask(__name__)
app.config.from_object('ovs.config.Config')
app.database = Database(app)
if app.config['PRODUCTION']:
    app.blob = Blob(app)
app.BaseModel = declarative_base()

# import at bottom to avoid circular dependencies
import ovs.services.auth_service
