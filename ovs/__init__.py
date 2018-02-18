from flask import Flask
from sqlalchemy.ext.declarative import declarative_base

from ovs.database import Database

app = Flask(__name__)
app.config.from_object('ovs.config.Config')
app.database = Database(app)
app.BaseModel = declarative_base()

# import at bottom to avoid circular dependencies
import ovs.services.AuthService
