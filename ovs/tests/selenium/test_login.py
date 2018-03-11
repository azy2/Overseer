""" Test whether users can log in """
from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC

from ovs import app
from ovs.models.user_model import User
from ovs.models.resident_model import Resident
from ovs.models.room_model import Room
from ovs.models.profile_model import Profile


class TestLogin(TestCase):
    """ Test whether users can log in """

    def clear_db(self):
        """ Empty the DB for tests """
        self.db.query(Profile).delete()
        self.db.query(User).delete()
        self.db.query(Resident).delete()
        self.db.query(Room).delete()
        self.db.commit()

    def setUp(self):
        """ Creates a headless chrome instance for selenium and clears the DB """
        self.db = app.database.instance()
        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.base_url = 'localhost:5000'
        #self.clear_db()

    def tearDown(self):
        """ Closes selenium driver and clears the DB """
        self.browser.quit()
        #self.clear_db()

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
        """ Tests whether manageres can log in or not """
        self.browser.get(self.base_url)
        self.assertIn('Overseer', self.browser.title)

        name_box = self.browser.find_element_by_name('email')
        name_box.send_keys('admin@gmail.com')
        pass_box = self.browser.find_element_by_name('password')
        pass_box.send_keys('abcd1234')
        pass_box.send_keys(Keys.ENTER)

        self.assertIn('Super', self.browser.title)
