"""
The base test case for selenium that all other selenium tests should inherit from
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from ovs import DataGen
from ovs.tests.unittests.base_test import OVSBaseTestCase

class SeleniumBaseTestCase(OVSBaseTestCase):
    """
    The base test case for selenium that all other selenium tests should inherit from
    """

    def setUp(self):
        """ Creates a headless chrome instance for selenium and clears the DB """
        super().setUp()
        DataGen.create_defaults()

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.browser.implicitly_wait(1)
        self.base_url = 'http://localhost:5000'

    def tearDown(self):
        """ Closes selenium driver and OVSBaseTestCase clears the DB """
        self.browser.quit()
        super().tearDown()
