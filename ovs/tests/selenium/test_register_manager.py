""" Test functionality related to registering managers. """
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ovs.tests.selenium.selenium_base_test import SeleniumBaseTestCase

class TestRegisterManager(SeleniumBaseTestCase):
    """ Test functionality related to registering managers. """

    def test_register_manager(self):
        """ Tests whether a manager can be registered. """
        self.browser.get(self.base_url)
        self.assertIn('Overseer', self.browser.title)
        super().login_default_admin()

        # Click on Register Manager link
        register_manager_link = self.browser.find_element_by_link_text('Managers')
        register_manager_link.click()

        # Verify page changed
        self.assertIn('Managers', self.browser.title)

        # Register a manager
        self.set_text_field_by_id('email', 'email@website.net')
        self.set_text_field_by_id('first_name', 'John')
        self.set_text_field_by_id('last_name', 'Smith')
        submit_button = self.browser.find_element_by_id('register_manager')
        submit_button.send_keys(Keys.ENTER)

        # Wait for successful notification popup to appear
        wait = WebDriverWait(self.browser, 5)
        wait.until(EC.visibility_of_element_located((By.ID, 'notification-message')))

        # Verify fields are empty and ready for new account registration
        self.assertEqual(self.browser.find_element_by_id('email').get_attribute('value'), '')
        self.assertEqual(self.browser.find_element_by_id('first_name').get_attribute('value'), '')
        self.assertEqual(self.browser.find_element_by_id('last_name').get_attribute('value'), '')
