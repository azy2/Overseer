"""
The base test case for selenium that all other selenium tests should inherit from
"""
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from ovs.tests.unittests.base_test import OVSBaseTestCase

class SeleniumBaseTestCase(OVSBaseTestCase):
    """
    The base test case for selenium that all other selenium tests should inherit from
    """
    def setUp(self):
        """ Creates a headless chrome instance for selenium and clears the DB """
        super().setUp()

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("window-size=1980,960") # Make screenshots larger
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.browser.implicitly_wait(1)
        self.base_url = self.get_server_url()

    def tearDown(self):
        """ Closes selenium driver and OVSBaseTestCase clears the DB """
        # Take screenshot at end of every test because Python unittesting is deficient
        #  and has no non-hack way to detect a failed test case
        test_screenshot_dir = 'ovs/tests/selenium/Screenshots/' + type(self).__name__
        if not os.path.exists(test_screenshot_dir):
            os.makedirs(test_screenshot_dir)
        self.browser.save_screenshot(test_screenshot_dir + '/%s-last-test-run.png' % self._testMethodName)

        super().tearDown()

    def login_with_credentials(self, email, password):
        """ Logs in with the provided email and password, most selenium tests will call this """
        name_box = self.browser.find_element_by_name('email')
        name_box.send_keys(email)
        pass_box = self.browser.find_element_by_name('password')
        pass_box.send_keys(password)
        pass_box.send_keys(Keys.ENTER)

    def set_text_field_by_id(self, field_id, new_text):
        """ Sets the text in the given text field to the new text """
        text_field = self.browser.find_element_by_id(field_id)
        text_field.clear()
        text_field.send_keys(new_text)
