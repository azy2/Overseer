""" Test whether users can log in """
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ovs.tests.selenium.selenium_base_test import SeleniumBaseTestCase

class TestRegisterRoom(SeleniumBaseTestCase):
    """ Test whether managers can be registered"""

    def test_register_room(self):
        """ Tests whether all fields can be edited in a register room page """
        from ovs.datagen import DataGen
        DataGen.create_defaults()

        self.browser.get(self.base_url)
        self.assertIn('Overseer', self.browser.title)

        super().login_with_credentials('admin@gmail.com', 'abcd1234')

        # Click on Register Manager
        register_manager = self.browser.find_element_by_link_text('Register a Room')
        register_manager.click()

        # Verify page changed
        self.assertIn('Register Room', self.browser.title)

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
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'close')))

        # Handle successful notification popup
        notification_close_button = self.browser.find_element_by_class_name('close')
        notification_close_button.click()

        # Wait for successful notification popup to disappear
        wait = WebDriverWait(self.browser, 5)
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, 'close')))

        # Verify fields are empty and ready for new account registration

        self.assertEqual(self.browser.find_element_by_id('room_number').get_attribute('value'), '')
        self.assertEqual(self.browser.find_element_by_id('room_status').get_attribute('value'), '')
        self.assertEqual(self.browser.find_element_by_id('room_type').get_attribute('value'), '')
        self.assertEqual(self.browser.find_element_by_id('occupants').get_attribute('value'), '')
