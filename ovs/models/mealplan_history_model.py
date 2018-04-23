"""
Keeps track of mealplan history as represented in the database
"""
from flask import jsonify
from sqlalchemy import Integer, Enum, Column, DateTime
from sqlalchemy.sql import func

from ovs import db


class MealplanHistory(db.Model):
    """
    Defines a Mealplan History Item as represented in the database.
    Args:
        resident_id (int): The resident's id who signed in.
        mealplan_pin (int): The pin of the mealplan used to sign in.
        manager_id (int): The id of the manager who was logged in at the time.
        log_type (Enum): Must be either 'MEAL_USED' or 'UNDO'.

    Returns:
        A MealplanHistory Model.
    """
    __tablename__ = 'mealplan_history'
    id = Column(Integer, primary_key=True)
    resident_id = Column(Integer)
    mealplan_pin = Column(Integer)
    manager_id = Column(Integer)
    log_type = Column(Enum('MEAL_USED', 'UNDO'), nullable=False)
    created = Column(DateTime, server_default=func.now())
    updated = Column(DateTime, server_default=func.now(), server_onupdate=func.now())

    def __init__(self, resident_id, mealplan_pin, manager_id, log_type):
        super(MealplanHistory, self).__init__(
            resident_id=resident_id,
            mealplan_pin=mealplan_pin,
            manager_id=manager_id,
            log_type=log_type)

    def __repr__(self):
        """
        Allows MealplanHistory objects to be printed.
        Returns:
            str: A string representation of MealplanHistory.
        """
        return 'MealplanHistory([id={id}, resident_id={resident_id}, mealplan_pin={mealplan_pin}, ' \
               'manager_id={manager_id}, log_type={log_type}, created={created}, updated={updated}])'\
            .format(**self.__dict__)

    def json(self):
        """
        Get a JSON represntation of this MealplanHistory.
        Returns:
             A JSON representation of this MealplanHistory Item.
        """
        return jsonify(
            id=self.id,
            resident_id=self.resident_id,
            mealplan_pin=self.mealplan_pin,
            manager_id=self.manager_id,
            log_type=self.log_type,
            created=self.created,
            updated=self.updated
        )
