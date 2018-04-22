""" Tests functionality related to packages. """
from ovs.tests.selenium.table_test import TableTest, InputTextElement

class TestPackage(TableTest):
    """ Tests functionality related to packages. """

    def setUp(self):
        super().setUp()
        # Current form has [Recipient Email][Package Description]
        self.form_text_field_types.append(InputTextElement())
        self.form_text_field_types.append(InputTextElement())

        # Current table has [Recipient Name][Email][Checked By][Checked Time][Description]
        self.table_text_field_types.append(None)
        self.table_text_field_types.append(InputTextElement())
        self.table_text_field_types.append(None)
        self.table_text_field_types.append(None)
        self.table_text_field_types.append(InputTextElement())

    def navigate_to_table_page(self):
        self.browser.find_element_by_link_text('Packages').click()

    def test_add_package(self):
        """ Tests that packages can be added for a default resident. """
        self.add_table_test(self.default_resident_email, 'The Stuff')
        # Need to also verify resident name in index 0 added for package test
        last_row = self.get_last_table_row()
        resident_name = last_row[0].text.strip()
        self.assertIn(self.default_resident_name, resident_name)

    def test_update_delete_package(self):
        """ Tests that added packages can be updated and deleted. """
        self.test_add_package()
        self.update_delete_table_test(None, '429')
