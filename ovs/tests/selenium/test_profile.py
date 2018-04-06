""" Test whether profiles can be edited """
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ovs.tests.selenium.selenium_base_test import SeleniumBaseTestCase

class TestProfile(SeleniumBaseTestCase):
    """ Test whether profiles can be edited """

    def set_text_field_by_id(self, field_id, new_text):
        """ Sets the text in the given text field to the new text """
        text_field = self.browser.find_element_by_id(field_id)
        text_field.clear()
        text_field.send_keys(new_text)

    def test_edit_profile(self):
        """ Tests whether all fields can be edited in a resident profile """
        self.browser.get(self.base_url)
        self.assertIn('Overseer', self.browser.title)

        super().login_with_credentials('resident@gmail.com', 'abcd1234')

        # Click on account dropdown and go to Profile link
        account_dropdown = self.browser.find_element_by_id('accountDropdown')
        account_dropdown.click()
        profile_link = self.browser.find_element_by_link_text('Profile')
        profile_link.click()

        # Verify page changed
        self.assertIn('Edit', self.browser.title)

        # Change all fields
        self.set_text_field_by_id('preferred_name', 'Megatron')
        self.set_text_field_by_id('phone_number', '555-555-5555')
        self.set_text_field_by_id('preferred_email', 'Megatron@mega.tron')
        self.set_text_field_by_id('race', 'Transformer')

        # Currently 'Unspecified' gender is broken so need to set to Male
        male_gender_option = self.browser.find_element_by_id('gender-0')
        male_gender_option.click()

        # Submit changes, need to "press enter" on button instead of clicking
        #  because Selenium is wonderful, stable software
        submit_button = self.browser.find_element_by_id('submit_changes')
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

        # Verify preferred name changed in account dropdown
        # Dropdown reference must be refreshed because the page has changed after submitting
        account_dropdown = self.browser.find_element_by_id('accountDropdown')
        self.assertIn('Megatron', account_dropdown.text)

        # Verify the info changed through the text fields, text is given by attribute 'value'
        self.assertEqual(self.browser.find_element_by_id('preferred_name').get_attribute('value'), 'Megatron')
        self.assertEqual(self.browser.find_element_by_id('phone_number').get_attribute('value'), '555-555-5555')
        self.assertEqual(self.browser.find_element_by_id('preferred_email').get_attribute('value'), 'Megatron@mega.tron')
        self.assertEqual(self.browser.find_element_by_id('race').get_attribute('value'), 'Transformer')
