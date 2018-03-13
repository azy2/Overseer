"""
Tests for meal plan services
"""
from datetime import datetime
from ovs.services.meal_service import MealService
from ovs.models.meal_plan_model import MealPlan
from ovs.tests.unittests.base_test import OVSBaseTestCase


class TestMealPlanService(OVSBaseTestCase):
    """
    Tests for meal plan services
    """

    def setUp(self):
        """ Runs before every test and clears relevant tables """
        super().setUp()
        self.create_test_weekly_meal_plan()

    def get_tables_used_in_tests(self):
        """
        Subclass test cases should override this to return what database objects
        correspond to tables they will need cleared before running
        """
        return [MealPlan]

    def create_test_weekly_meal_plan(self):
        """ Creates a meal plan of WEEKLY plan type for use in testing  """
        self.test_meal_plan_info = (141414, 10, 'WEEKLY')
        self.test_meal_plan = MealPlan(*self.test_meal_plan_info)
        MealService.create_meal_plan(*self.test_meal_plan_info)

    def database_contains_test_meal_plan(self):
        """ Returns true if the database contains exactly the test meal plan, false otherwise """
        meal_list = self.db.query(MealPlan).filter(MealPlan.pin == self.test_meal_plan.pin).all()
        if len(meal_list) != 1:
            return False

        actual_meal_info = (meal_list[0].pin, meal_list[0].meal_plan, meal_list[0].plan_type)
        return actual_meal_info == self.test_meal_plan_info

    def test_create_meal_plan(self):
        """ Tests that meal plans can be created """
        self.assertTrue(self.database_contains_test_meal_plan())

    def test_create_meal_plan_duplicate(self):
        """ Tests that meal plans cannot be created with duplicate pins """
        duplicate_plan_created = MealService.create_meal_plan(self.test_meal_plan.pin, 14, 'WEEKLY')
        self.assertFalse(duplicate_plan_created)
        self.assertTrue(self.database_contains_test_meal_plan())

    def test_invalid_get_meal_plan_by_pin(self):
        """ Tests get_meal_plan_by_pin with a non-existent pin """
        meal_plan = MealService.get_meal_plan_by_pin(9999999)
        self.assertEqual(meal_plan, None)

    def test_use_meal(self):
        """ Tests that use_meal works for a new user """
        starting_meal_credits = self.test_meal_plan.credits
        self.assertTrue(MealService.use_meal(self.test_meal_plan.pin))

        meal_plan = MealService.get_meal_plan_by_pin(self.test_meal_plan.pin)
        self.assertEqual(starting_meal_credits - 1, meal_plan.credits)

        # Add 1 minute to the reset time to avoid any flaky tests right around the reset period
        self.assertTrue(datetime.utcnow() < meal_plan.reset_date.replace(minute=1))

    def test_use_meal_no_credits(self):
        """ Tests use_meal fails when no credits are available """
        # Test currently flaky if reset_date is between the first call and last call to use_meal
        for _ in range(self.test_meal_plan.meal_plan):
            self.assertTrue(MealService.use_meal(self.test_meal_plan.pin))

        # Account should have no credits and future use_meal calls should fail
        meal_plan = MealService.get_meal_plan_by_pin(self.test_meal_plan.pin)
        self.assertEqual(0, meal_plan.credits)
        self.assertFalse(MealService.use_meal(self.test_meal_plan.pin))

    def test_use_meal_invalid_pin(self):
        """ Tests that use_meal fails with an account that does not exist """
        self.assertFalse(MealService.use_meal(9999999))
