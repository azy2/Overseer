""" Tests functionality related to registering rooms. """
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ovs.tests.selenium.selenium_base_test import SeleniumBaseTestCase

class TestRegisterRoom(SeleniumBaseTestCase):
    """ Tests functionality related to registering rooms. """

    def test_register_room(self):
        """ Tests whether all fields can be edited in the register room page. """
        self.browser.get(self.base_url)
        self.assertIn('Overseer', self.browser.title)
        super().login_default_admin()

        # Click on Register Manager
        register_manager = self.browser.find_element_by_link_text('Rooms')
        register_manager.click()

        # Verify page changed
        self.assertIn('Rooms', self.browser.title)

        # # Change all fields
        self.set_text_field_by_id('room_number', '429D')
        self.set_text_field_by_id('room_status', 'rented')
        self.set_text_field_by_id('room_type', 'single')
        self.set_text_field_by_id('occupants', 'resident@gmail.com')

        # Submit changes, need to "press enter" on button instead of clicking
        # because Selenium is wonderful, stable software
        submit_button = self.browser.find_element_by_id('register_room')
        submit_button.send_keys(Keys.ENTER)

        # Wait for successful notification popup to appear
        wait = WebDriverWait(self.browser, 5)
        wait.until(EC.visibility_of_element_located((By.ID, 'notification-message')))

        # Verify fields are empty and ready for new account registration
        self.assertEqual(self.browser.find_element_by_id('room_number').get_attribute('value'), '')
        self.assertEqual(self.browser.find_element_by_id('room_status').get_attribute('value'), '')
        self.assertEqual(self.browser.find_element_by_id('room_type').get_attribute('value'), '')
        self.assertEqual(self.browser.find_element_by_id('occupants').get_attribute('value'), '')
