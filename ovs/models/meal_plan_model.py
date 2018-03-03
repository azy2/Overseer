"""
Defines a MealPlan as represented in the database
"""
from datetime import datetime, timedelta
from flask import jsonify
import sqlalchemy as sa
from ovs import app



class MealPlan(app.BaseModel):
    """
    Defines a MealPlan as represented in the database. Along with some utility functions.
    """
    __tablename__ = 'mealplan'

    id = sa.Column(sa.Integer, primary_key=True)
    pin = sa.Column(sa.Integer, unique=True)
    credits = sa.Column(sa.Integer, nullable=False)
    meal_plan = sa.Column(sa.Integer, nullable=False)
    reset_date = sa.Column(sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP'))
    plan_type = sa.Column(sa.Enum('WEEKLY', 'SEMESTERLY', 'LIFETIME'), nullable=False)
    created = sa.Column(sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP'))
    updated = sa.Column(sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    def __init__(self, pin, meal_plan, plan_type):
        super(MealPlan, self).__init__(
            pin=pin,
            credits=meal_plan,
            meal_plan=meal_plan,
            plan_type=plan_type)

    def update_meal_count(self):
        """
        Uses a meal credit, as outlined by the plan.
        :return: Boolean, whether a credit was available
        """
        if self.reset_date is None or datetime.now() > self.reset_date:
            self.reset_date = self.get_next_reset_date()
            self.credits = self.meal_plan
        if self.credits > 0:
            self.credits -= 1
            return True
        return False

    def get_next_reset_date(self):
        """
        Gets the next reset day based off the plan type
        :return: DateTime value for reset_day
        """
        if self.plan_type == 'WEEKLY':
            date = MealPlan.next_weekday(datetime.now(), 0)
            return date.replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            return datetime.now()

    @staticmethod
    def next_weekday(date, weekday):
        """
        Gets the next weekday after date
        :param date: DateTime to start
        :param weekday: 0 for Monday ... 6 for Sunday
        :return: DateTime with date as the next weekday and time identical to provided date.
        """
        days_ahead = weekday - date.weekday()
        if days_ahead <= 0: # Target day already happened this week
            days_ahead += 7
        return date + timedelta(days=days_ahead)

    def __repr__(self):
        return 'MealPlan([id="%s", pin="%s", credits="%s", meal_plan = "%s", " + \
                "plan_type="%s", created="%s", updated="%s"])' \
               % (self.id, self.pin, self.credits, self.meal_plan, self.plan_type, self.created, self.updated)

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
