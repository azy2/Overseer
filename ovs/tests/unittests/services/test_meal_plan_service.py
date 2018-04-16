"""
Tests for meal plan services
"""
from ovs.tests.unittests.base_test import OVSBaseTestCase
from ovs.services.meal_service import MealService
from ovs.models.meal_plan_model import MealPlan

class TestMealPlanService(OVSBaseTestCase):
    """
    Tests for meal plan services
    """

    def setUp(self):
        """ Runs before every test and clears relevant tables """
        super().setUp()
        self.create_test_weekly_meal_plan()

    def create_test_weekly_meal_plan(self):
        """ Creates a meal plan of WEEKLY plan type for use in testing  """
        self.test_meal_plan_info = (10, 'WEEKLY')
        self.test_meal_plan = MealService.create_meal_plan(*self.test_meal_plan_info)

    def database_contains_test_meal_plan(self):
        """ Returns true if the database contains exactly the test meal plan, false otherwise """
        meal_list = self.db.session.query(MealPlan).filter(MealPlan.pin == self.test_meal_plan.pin).all()
        if len(meal_list) != 1:
            return False

        actual_meal_info = (meal_list[0].meal_plan, meal_list[0].plan_type)
        return actual_meal_info == self.test_meal_plan_info

    def test_create_meal_plan(self):
        """ Tests that meal plans can be created """
        self.assertTrue(self.database_contains_test_meal_plan())

    def test_invalid_get_meal_plan_by_pin(self):
        """ Tests get_meal_plan_by_pin with a non-existent pin """
        meal_plan = MealService.get_meal_plan_by_pin(9999999)
        self.assertEqual(meal_plan, None)

    def test_delete_meal_plan(self):
        """ Tests that meal plans can be deleted """
        expected = self.db.session.query(MealPlan).count() - 1

        # check if deletion successful
        self.assertTrue(MealService.delete_meal_plan(self.test_meal_plan.pin))

        self.assertEqual(self.db.session.query(MealPlan).count(), expected)

    def test_delete_meal_plan_null(self):
        """ Tests that nothing breaks when deleting a nonexistant meal plan """
        expected = self.db.session.query(MealPlan).count()

        # This pin is NOT the meal plan
        self.assertFalse(MealService.delete_meal_plan(9999999))

        self.assertEqual(self.db.session.query(MealPlan).count(), expected)

    def test_update_meal_plan(self):
        """ Tests that meal plans can be updated """
        MealService.edit_meal_plan(self.test_meal_plan.pin,
                                   credit=69,
                                   plan_meal_count=19,
                                   plan_type='LIFETIME')

        self.assertEqual(self.test_meal_plan.credits, 69)
        self.assertEqual(self.test_meal_plan.meal_plan, 19)
        self.assertEqual(self.test_meal_plan.plan_type, 'LIFETIME')
