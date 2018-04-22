""" Tests functionality related to registering residents. """
from ovs.tests.selenium.table_test import TableTest, InputTextElement

class TestRegisterResident(TableTest):
    """ Tests functionality related to registering residents. """

    def setUp(self):
        super().setUp()
        self.form_text_field_ids.append('register_form-email')
        self.form_text_field_ids.append('register_form-first_name')
        self.form_text_field_ids.append('register_form-last_name')

        # Current format is [Email][First Name][Last Name][Room Number]
        self.table_text_field_types.append(InputTextElement())
        self.table_text_field_types.append(InputTextElement())
        self.table_text_field_types.append(InputTextElement())
        self.table_text_field_types.append(None)

    def navigate_to_table_page(self):
        self.browser.find_element_by_link_text('Residents').click()

    def test_register_resident(self):
        """ Tests whether residents can be registered. """
        self.add_table_test('testing123@gmail.com', 'Test', 'Testerson')

    def test_update_delete_resident(self):
        """ Tests that registered residents can be updated and deleted. """
        self.test_register_resident()
        self.update_delete_table_test(None, 'Jack', 'Sparrow', None)
