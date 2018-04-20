""" Tests functionality across routes. """
from mock import patch
from selenium.webdriver.support.ui import Select
from ovs.tests.selenium.selenium_base_test import SeleniumBaseTestCase
from ovs.services.mail_service import MailService
from ovs.utils import crypto

class TestCrossSystem(SeleniumBaseTestCase):
    """ Tests functionality across routes. """

    #@patch('ovs.services.mail_service.MailService.send_email')
    @patch('ovs.utils.crypto.generate_password')
    def test_preferred_name_meal_plan(self, mock_password):
        self.browser.get(self.base_url)
        self.assertIn('Overseer', self.browser.title)
        super().login_default_admin()

        # Create a new resident
        register_resident_link = self.browser.find_element_by_link_text('Residents')
        register_resident_link.click()

        # Set all fields and register resident
        self.set_text_field_by_id('register_form-email', 'testing123@gmail.com')
        self.set_text_field_by_id('register_form-first_name', 'Test')
        self.set_text_field_by_id('register_form-last_name', 'Testerson')
        register_button = self.browser.find_element_by_name('register_btn')
        register_button.click()

        # Create a meal plan for the new resident
        self.go_to_page_in_dropdown('Meal Plans', 'mealDropdown')

        # Make a 20 credit Semesterly meal plan for the created resident
        email_text_field = self.browser.find_element_by_id('email')
        email_text_field.send_keys('testing123@gmail.com')
        credits_text_field = self.browser.find_element_by_id('meal_plan')
        credits_text_field.send_keys('20')
        plan_type_selector = Select(self.browser.find_element_by_id('plan_type'))
        plan_type_selector.select_by_visible_text('Semesterly')
        register_button = self.browser.find_element_by_name('create_btn')
        register_button.click()

        # New meal plans get added to the bottom of the table, find last entry to get the pin
        meal_plan_table = self.browser.find_element_by_class_name('table-responsive')
        last_table_row = meal_plan_table.find_elements_by_tag_name('tr')[-1]
        resident_pin = last_table_row.find_elements_by_tag_name('td')[0].text.strip()

        # Use the meal plan
        self.go_to_page_in_dropdown('Meal login', 'mealDropdown')
        pin_text_field = self.browser.find_element_by_id('pin')
        pin_text_field.send_keys(resident_pin)
        sign_in_button = self.browser.find_element_by_class_name('btn-primary')
        sign_in_button.click()

        # Verify that the new resident's name is used in the confirmation
        # This element is likely to change on the page, really should have an ID attached
        confirmation_holder = self.browser.find_element_by_class_name('col-6')
        confirmation_text = confirmation_holder.find_element_by_tag_name('p').text
        self.assertIn('Test', confirmation_text)

        # Log in to new resident account and edit preferred name in profile
        self.go_to_page_in_dropdown('Logout', 'accountDropdown')
        #mock_email.assert_called()
