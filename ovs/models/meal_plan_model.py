"""
Defines a MealPlan as represented in the database
"""
import logging

from datetime import datetime, timedelta

from flask import jsonify
from sqlalchemy import Integer, Enum, Column, text, DateTime, Sequence
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError

from ovs import db


class MealPlan(db.Model):
    """
    Defines a MealPlan as represented in the database. Along with some utility functions.
    """
    __tablename__ = 'mealplan'

    id = Column(Integer)
    pin = Column(Integer, Sequence('meal_pin_seq'), primary_key=True, autoincrement=True)
    credits = Column(Integer, nullable=False)
    meal_plan = Column(Integer, nullable=False)
    reset_date = Column(DateTime, default=datetime.utcnow())
    plan_type = Column(Enum('WEEKLY', 'SEMESTERLY', 'LIFETIME'), nullable=False)
    created = Column(DateTime, server_default=func.now())
    updated = Column(DateTime, server_default=func.now(), server_onupdate=func.now())

    def __init__(self, meal_plan, plan_type):
        super(MealPlan, self).__init__(
            credits=meal_plan,
            meal_plan=meal_plan,
            plan_type=plan_type)

    def update_meal_count(self):
        """
        Uses a meal credit, as outlined by the plan.
        :return: Boolean, whether a credit was available
        """
        if self.reset_date is None or datetime.utcnow() > self.reset_date:
            self.reset_date = self.get_next_reset_date()
            self.credits = self.meal_plan
        if self.credits > 0:
            self.credits -= 1
            try:
                db.session.commit()
                return True
            except SQLAlchemyError:
                logging.exception('Failed to update meal plan credits.')
                db.session.rollback()
                return False
        return False

    def get_next_reset_date(self):
        """
        Gets the next reset day based off the plan type
        :return: DateTime value for reset_day
        """
        if self.plan_type == 'WEEKLY':
            date = MealPlan.next_weekday(datetime.utcnow(), 0)
            return date.replace(hour=0, minute=0, second=0, microsecond=0)
        else:  # error case. This does give them unlimited meals
            return datetime.utcnow()

    @staticmethod
    def next_weekday(date, weekday):
        """
        Gets the next weekday after date
        :param date: DateTime to start
        :param weekday: 0 for Monday ... 6 for Sunday
        :return: DateTime with date as the next weekday and time identical to provided date.
        """
        days_ahead = weekday - date.weekday()
        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 7
        return date + timedelta(days=days_ahead)

    def __repr__(self):
        return 'MealPlan([id={id}, pin={pin}, credits={credits}, meal_plan={meal_plan}, plan_type={plan_type}, ' \
               'created={created}, updated={updated}])'.format(**self.__dict__)

    def json(self):
        """ Returns a JSON representation of this Meal Plan """
        return jsonify(
            id=self.id,
            number=self.pin,
            credits=self.credits,
            meal_plan=self.meal_plan,
            reset_date=self.reset_date,
            plan_type=self.plan_type,
            created=self.created,
            updated=self.updated
        )
