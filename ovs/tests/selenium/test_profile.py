""" Tests functionality related to editing profiles. """
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ovs.tests.selenium.selenium_base_test import SeleniumBaseTestCase

class TestProfile(SeleniumBaseTestCase):
    """ Tests functionality related to editing profiles. """

    def go_to_resident_profile_page(self):
        """ Runs the Selenium steps necessary to navigate to the edit resident profile page. """
        super().login_default_resident()

        # Click on account dropdown and go to Profile link
        self.go_to_page_in_dropdown('Profile', 'accountDropdown')

        # Verify page changed
        self.assertIn('Edit', self.browser.title)

    def test_edit_profile(self):
        """ Tests whether all fields can be edited in a resident profile. """
        self.browser.get(self.base_url)
        self.assertIn('Overseer', self.browser.title)
        self.go_to_resident_profile_page()

        # Change all fields
        self.set_text_field_by_id('preferred_name', 'Megatron')
        self.set_text_field_by_id('phone_number', '202-456-1111')
        self.set_text_field_by_id('preferred_email', 'Megatron@mega.tron')
        self.set_text_field_by_id('race', 'Transformer')

        # Set 'Unspecified' gender to 'Male'
        male_gender_option = self.browser.find_element_by_id('gender-0')
        male_gender_option.click()

        # Submit changes, need to "press enter" on button instead of clicking
        #  because Selenium is wonderful, stable software
        submit_button = self.browser.find_element_by_id('submit_changes')
        submit_button.send_keys(Keys.ENTER)

        # Wait for successful notification popup to appear
        wait = WebDriverWait(self.browser, 5)
        wait.until(EC.visibility_of_element_located((By.ID, 'notification-message')))

        # Verify preferred name changed in account dropdown
        # Dropdown reference must be refreshed because the page has changed after submitting
        account_dropdown = self.browser.find_element_by_id('accountDropdown')
        self.assertIn('Megatron', account_dropdown.text)

        # Verify the info changed through the text fields, text is given by attribute 'value'
        name_text = self.browser.find_element_by_id('preferred_name').get_attribute('value')
        phone_text = self.browser.find_element_by_id('phone_number').get_attribute('value')
        email_text = self.browser.find_element_by_id('preferred_email').get_attribute('value')
        race_text = self.browser.find_element_by_id('race').get_attribute('value')
        self.assertEqual(name_text, 'Megatron')
        self.assertEqual(phone_text, '202-456-1111')
        self.assertEqual(email_text, 'Megatron@mega.tron')
        self.assertEqual(race_text, 'Transformer')

    def test_invalid_profile_picture(self):
        """ Tests that non-.png files cannot be uploaded as a profile picture. """
        self.browser.get(self.base_url)
        self.assertIn('Overseer', self.browser.title)
        self.go_to_resident_profile_page()

        # Choose the non-picture file to upload
        choose_profile_picture_upload = self.browser.find_element_by_id('profile_picture')
        non_picture_path = '/ovs/tests/selenium/data/not_a_picture.txt'
        choose_profile_picture_upload.send_keys(os.getcwd() + non_picture_path)

        upload_picture_button = self.browser.find_element_by_id('upload_picture')
        upload_picture_button.click()

        # Wait for error dialog to pop up, id='notification-message'
        wait = WebDriverWait(self.browser, 5)
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'invalid-feedback')))

        # Get error message on error dialog
        error_tag = self.browser.find_element_by_class_name('invalid-feedback')
        error_message = error_tag.text
        self.assertEqual(error_message, 'Please select a valid png.')

    def test_valid_profile_picture(self):
        """ Tests that .png files can be uploaded for a profile picture. """
        self.browser.get(self.base_url)
        self.assertIn('Overseer', self.browser.title)
        self.go_to_resident_profile_page()
        default_image_src = self.browser.find_element_by_id('profile_image').get_attribute('src')

        # Choose the picture file to upload
        choose_profile_picture_upload = self.browser.find_element_by_id('profile_picture')
        test_picture_path = '/ovs/tests/selenium/data/freshmanmods.png'
        choose_profile_picture_upload.send_keys(os.getcwd() + test_picture_path)

        upload_picture_button = self.browser.find_element_by_id('upload_picture')
        upload_picture_button.click()

        # Wait for picture to swap
        self.browser.implicitly_wait(1)

        # Verify picture changed
        new_image_src = self.browser.find_element_by_id('profile_image').get_attribute('src')
        self.assertNotEqual(new_image_src, default_image_src)
