""" Test whether users can log in """
from selenium.webdriver.common.keys import Keys
from ovs import app
from ovs.tests.selenium.selenium_base_test import SeleniumBaseTestCase

class TestLogin(SeleniumBaseTestCase):
    """ Test whether users can log in """

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

        self.assertIn(app.config['ADMIN']['first_name'], self.browser.title)

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
