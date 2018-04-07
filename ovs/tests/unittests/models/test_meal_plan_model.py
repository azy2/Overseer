"""
Tests for the meal plan model
"""
from datetime import datetime

from ovs.models.meal_plan_model import MealPlan
from ovs.tests.unittests.base_test import OVSBaseTestCase


class TestMealPlanModel(OVSBaseTestCase):
    """
    Tests for the meal plan model
    """

    def setUp(self):
        """ Runs before every test """
        super().setUp()
        self.create_test_meal_plan()

    def create_test_meal_plan(self):
        """ Creates a meal plan with WEEKLY plan_type for use in testing """
        test_meal_plan_info = (10, 'WEEKLY')
        self.test_meal_plan = MealPlan(*test_meal_plan_info)

    def test_update_meal_plan(self):
        """ Tests that meal plans can be updated """
        starting_credits = self.test_meal_plan.credits

        self.assertTrue(self.test_meal_plan.update_meal_count())
        self.assertEqual(starting_credits - 1, self.test_meal_plan.credits)
        # Add 1 minute to the reset time to avoid any flaky tests right around the reset period
        self.assertTrue(datetime.utcnow() < self.test_meal_plan.reset_date.replace(minute=1))

    def test_get_next_reset_date_weekly(self):
        """ Tests get_next_reset_date for WEEKLY plan_type """
        self.assertEqual(self.test_meal_plan.get_next_reset_date().weekday(), 0)  # Is it a Monday?

    def test_next_weekday(self):
        """ Tests next_weekday when later in the same week """
        date = datetime(year=2018, month=1, day=1)
        new_date = MealPlan.next_weekday(date, 4)
        # 1/5/2018 is a Friday
        self.assertEqual(date.replace(day=5), new_date)

    def test_next_weekday_diff_week(self):
        """ Tests next_weekday when it loops to the next week """
        date = datetime(year=2018, month=1, day=3)
        new_date = MealPlan.next_weekday(date, 0)
        # 1/8/2018 is a Monday
        self.assertEqual(date.replace(day=8), new_date)
