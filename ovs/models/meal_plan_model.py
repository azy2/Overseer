"""
Defines a MealPlan as represented in the database
"""
from datetime import datetime, timedelta

from flask import jsonify
from sqlalchemy import Integer, Enum, Column, DateTime, Sequence
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ovs import db


class MealPlan(db.Model):
    """
    Defines a MealPlan as represented in the database. Along with some utility functions.

    Args:
        meal_plan (int): The number of meals the plan is reset too after reset_date.
        plan_type (enum): Either 'WEEKLY', 'SEMESTERLY' or 'LIFETIME'. Determines when the meals get reset.

    Returns:
        MealPlan: a new MealPlan Model object.
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
    user = relationship('Resident', uselist=False, single_parent=True)

    def __init__(self, meal_plan, plan_type):
        super(MealPlan, self).__init__(
            credits=meal_plan,
            meal_plan=meal_plan,
            plan_type=plan_type)

    def update_meal_count(self):
        """
        Uses a meal credit, as outlined by the plan.

        Returns:
            bool: Whether a credit was available.
        """
        self.check_reset_date()
        if self.credits > 0:
            self.credits -= 1
            db.session.flush()
            return True
        db.session.flush()
        return False

    def check_reset_date(self):
        """
        Checks a meal plan's reset date. If it has past,
        this updates the reset_date and resets the credits.

        Returns:
            bool: Whether the reset date was changed.
        """
        if self.plan_type == 'LIFETIME':
            return False
        if self.reset_date is None or datetime.utcnow() > self.reset_date:
            self.reset_date = self.get_next_reset_date()
            self.credits = self.meal_plan
            return True
        return False

    def get_next_reset_date(self):
        """
        Gets the next reset day based off the plan type.

        Returns:
            DateTime: value for reset_day.
        """
        if self.plan_type == 'WEEKLY':
            date = MealPlan.next_weekday(datetime.utcnow(), 0)
            return date.replace(hour=0, minute=0, second=0, microsecond=0)
        elif self.plan_type == 'SEMESTERLY':
            date = MealPlan.next_half_year(datetime.utcnow())
            return date.replace(hour=0, minute=0, second=0, microsecond=0)

        # error case. This does give them unlimited meals
        return datetime.utcnow()

    @staticmethod
    def next_half_year(date):
        """
        Gets the next January or July first after date.

        Args:
            date (DateTime): DateTime to start.

        Returns:
            DateTime: A DateTime with date as the next half year and time identical to provided date.
        """
        month = date.month
        next_month = 1
        if month < 7:
            next_month = 7
        next_year = date.year
        if next_month == 1:
            next_year += 1
        return date.replace(month=next_month, day=1, year=next_year)

    @staticmethod
    def next_weekday(date, weekday):
        """
        Gets the next weekday after date.
        Args:
            date (DateTime): Date to get the next weekday for.
            weekday (int): 0 for Monday, 1 for Tuesday, ... 6 for Sunday

        Returns:
            DateTime: A DateTime object set to the next weekday after `date` with identical time fields.
        """
        days_ahead = weekday - date.weekday()
        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 7
        return date + timedelta(days=days_ahead)

    def __repr__(self):
        """
        Makes MealPlan printable.
        Returns:
            str: A string representation of this MealPlan.
        """
        return 'MealPlan([id={id}, pin={pin}, credits={credits}, meal_plan={meal_plan}, plan_type={plan_type}, ' \
               'created={created}, updated={updated}])'.format(**self.__dict__)

    def json(self):
        """
        Get a JSON representation of this Model.
        Returns:
            A JSON representation of this Meal Plan.
        """
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
