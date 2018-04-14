""" Test whether users can log in """
from flask import current_app
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ovs.tests.selenium.selenium_base_test import SeleniumBaseTestCase

class TestRegisterManager(SeleniumBaseTestCase):
    """ Test whether managers can be registered"""

    def test_register_manager(self):
        """ Tests whether all fields can be edited in a register manager page """
        self.browser.get(self.base_url)
        self.assertIn('Overseer', self.browser.title)

        default_admin = current_app.config['USERS']['ADMIN']
        default_admin_email = default_admin['email']
        default_admin_password = default_admin['password']
        super().login_with_credentials(default_admin_email, default_admin_password)

        # Click on Register Manager
        register_manager = self.browser.find_element_by_link_text('Register Manager')
        register_manager.click()

        # Verify page changed
        self.assertIn('Register Manager', self.browser.title)

        # Change all fields
        self.set_text_field_by_id('email', 'email@website.net')
        self.set_text_field_by_id('first_name', 'John')
        self.set_text_field_by_id('last_name', 'Smith')

        # Submit changes, need to "press enter" on button instead of clicking
        # because Selenium is wonderful, stable software
        submit_button = self.browser.find_element_by_id('register_manager')
        submit_button.send_keys(Keys.ENTER)

        # Wait for successful notification popup to appear
        wait = WebDriverWait(self.browser, 5)
        wait.until(EC.visibility_of_element_located((By.ID, 'notification-message')))

        # Verify fields are empty and ready for new account registration
        self.assertEqual(self.browser.find_element_by_id('email').get_attribute('value'), '')
        self.assertEqual(self.browser.find_element_by_id('first_name').get_attribute('value'), '')
        self.assertEqual(self.browser.find_element_by_id('last_name').get_attribute('value'), '')
