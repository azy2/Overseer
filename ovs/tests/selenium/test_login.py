""" Test whether users can log in """
from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from ovs import DataGen


class TestLogin(TestCase):
    """ Test whether users can log in """

    def setUp(self):
        """ Creates a headless chrome instance for selenium and clears the DB """
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.base_url = 'localhost:5000'
        DataGen.clear_db()
        DataGen.create_defaults()

    def tearDown(self):
        """ Closes selenium driver and clears the DB """
        self.browser.quit()
        DataGen.clear_db()

    def test_resident_login(self):
        """ Tests whether residents can log in or not """
        self.browser.get(self.base_url)
        self.assertIn('Overseer', self.browser.title)

        name_box = self.browser.find_element_by_name('email')
        name_box.send_keys("resident@gmail.com")
        pass_box = self.browser.find_element_by_name('password')
        pass_box.send_keys('abcd1234')
        pass_box.send_keys(Keys.ENTER)

        self.assertIn('John', self.browser.title)

    def test_manager_login(self):
        """ Tests whether managers can log in or not """
        self.browser.get(self.base_url)
        self.assertIn('Overseer', self.browser.title)

        name_box = self.browser.find_element_by_name('email')
        name_box.send_keys('admin@gmail.com')
        pass_box = self.browser.find_element_by_name('password')
        pass_box.send_keys('abcd1234')
        pass_box.send_keys(Keys.ENTER)

        self.assertIn('Super', self.browser.title)

    def test_bad_login(self):
        """ Tests whether a random email  can log in or not """
        self.browser.get(self.base_url)
        self.assertIn('Overseer', self.browser.title)

        name_box = self.browser.find_element_by_name('email')
        name_box.send_keys('testtesttest@gmail.com')
        pass_box = self.browser.find_element_by_name('password')
        pass_box.send_keys('abcd1234')
        pass_box.send_keys(Keys.ENTER)

        self.assertEqual('Overseer', self.browser.title)
