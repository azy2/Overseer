""" Test whether users can log in """
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ovs.tests.selenium.selenium_base_test import SeleniumBaseTestCase

class TestRegisterManager(SeleniumBaseTestCase):
    """ Test whether managers can be registered"""

    def set_text_field_by_id(self, field_id, new_text):
        """ Sets the text in the given text field to the new text """
        text_field = self.browser.find_element_by_id(field_id)
        text_field.clear()
        text_field.send_keys(new_text)

    def test_register_manager(self):
        """ Tests whether all fields can be edited in a register manager page """
        from ovs.datagen import DataGen
        DataGen.create_defaults()

        self.browser.get(self.base_url)
        self.assertIn('Overseer', self.browser.title)

        super().login_with_credentials('admin@gmail.com', 'abcd1234')

        # Click on Register Manager
        register_manager = self.browser.find_element_by_link_text('Register Manager')
        register_manager.click()

        # Verify page changed
        self.assertIn('Register Manager', self.browser.title)

        # # Change all fields
        self.set_text_field_by_id('email', 'email@website.net')
        self.set_text_field_by_id('first_name', 'John')
        self.set_text_field_by_id('last_name', 'Smith')

        # Submit changes, need to "press enter" on button instead of clicking
        # because Selenium is wonderful, stable software
        submit_button = self.browser.find_element_by_id('register_manager')
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

        self.assertEqual(self.browser.find_element_by_id('email').get_attribute('value'), '')
        self.assertEqual(self.browser.find_element_by_id('first_name').get_attribute('value'), '')
        self.assertEqual(self.browser.find_element_by_id('last_name').get_attribute('value'), '')