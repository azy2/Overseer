""" Test whether profiles can be edited """
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ovs.tests.selenium.selenium_base_test import SeleniumBaseTestCase

class TestProfile(SeleniumBaseTestCase):
    """ Test whether profiles can be edited """

    def test_edit_preferred_name(self):
        """ Tests whether a preferred name can be edited in a resident profile """
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

        # Change preferred name
        preferred_name_text_field = self.browser.find_element_by_id('preferred_name')
        preferred_name_text_field.clear()
        preferred_name_text_field.send_keys('Megatron')

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

        # Verify preferred name changed in account dropdown
        # Dropdown reference must be refreshed because the page has changed after submitting
        account_dropdown = self.browser.find_element_by_id('accountDropdown')
        self.assertIn('Megatron', account_dropdown.text)
