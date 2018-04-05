"""
Keeps track of mealplan history as represented in the database
"""
from datetime import datetime, timedelta
from flask import jsonify
from sqlalchemy import Integer, Enum, Column, text, DateTime

from ovs import app


class Mealplan_History(app.BaseModel):
    """
    Defines a Mealplan History Item as represented in the database.
    """
    __tablename__ = 'mealplan_history'
    id = Column(Integer, primary_key=True)
    resident_id = Column(Integer)
    mealplan_pin = Column(Integer)
    manager_id = Column(Integer)
    log_type = Column(Enum('MEAL_USED', 'UNDO'), nullable=False)
    created = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated = Column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    def __init__(self, resident_id, mealplan_pin, manager_id, log_type):
        super(Mealplan_History, self).__init__(
            resident_id=resident_id,
            mealplan_pin=mealplan_pin,
            manager_id=manager_id,
            log_type=log_type)

    def __repr__(self):
        return 'Meal plan_History([id={id}, resident_id={resident_id}, mealplan_pin={mealplan_pin}, ' \
               'manager_id={manager_id}, log_type={log_type}, created={created}, updated={updated}])'\
            .format(**self.__dict__)

    def json(self):
        """ Returns a JSON representation of this Mealplan History Item"""
        return jsonify(
            id=self.id,
            resident_id=self.resident_id,
            mealplan_pin=self.mealplan_pin,
            manager_id=self.manager_id,
            log_type=self.log_type,
            created=self.created,
            updated=self.updated
        )
