""" Test whether users can log in """
from ovs.tests.selenium.selenium_base_test import SeleniumBaseTestCase

class TestHomePage(SeleniumBaseTestCase):
    """ Test whether users can log in """

    def test_home_page_title(self):
        """ Tests the title of the home page """
        self.browser.get(self.base_url)
        self.assertIn('Overseer', self.browser.title)

    def test_home_page_jumbotron_text(self):
        """ Tests title of jumbotron on home page"""
        self.browser.get(self.base_url)
        jumbotron = self.browser.find_element_by_class_name('display-3')
        self.assertEqual(jumbotron.text, 'Overseer')
