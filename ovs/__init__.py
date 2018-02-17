from flask import Flask
from ovs.database import Database
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
app.config.from_object('ovs.config.Config')
app.database = Database(app)
app.BaseModel = declarative_base()
