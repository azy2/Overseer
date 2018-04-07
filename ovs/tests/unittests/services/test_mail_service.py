"""Test for sending mail."""

import json
from flask import current_app

from mock import patch, ANY

from ovs.tests.unittests.base_test import OVSBaseTestCase
from ovs.mail import templates


class TestSendMail(OVSBaseTestCase):
    """Tests for sending mail."""

    def setUp(self):
        super().setUp()
        current_app.config['TEST_MAIL'] = True
        self.mail = current_app.extensions['mail']

    @patch('python_http_client.Client._make_request')
    def test_send_mail(self, mock_client):
        """Test that mail contains correct information."""
        from ovs.services.mail_service import MailService as mail_service

        mail_service.send_email(
            to_email='testEmail@test.com',
            subject='TestSubject',
            text='testText')
        mock_client.assert_called()
        self.assertEqual(json.dumps(self.mail.get(), sort_keys=True),
                         '{"content": [{"type": "text/plain", "value": "testText"}], "from": {"email": '
                         '"no-reply@ovs-overseer.azurewebsites.net"}, "personalizations": [{"to": [{"email": '
                         '"testEmail@test.com"}]}], "subject": "TestSubject"}')

    #pylint: disable=no-self-use
    @patch('ovs.services.mail_service.MailService.send_email')
    def test_create_user_sends_email(self, mock_mail):
        """ Tests that creating a user sends an email """
        from ovs.services.user_service import UserService

        test_user_info = ('test@gmail.com', 'Bob', 'Ross', 'ADMIN', 'testPassword')
        expected_substitutions = {
            'first_name': 'Bob',
            'last_name': 'Ross',
            'role': 'ADMIN',
            'password': 'testPassword'
        }

        UserService.create_user(*test_user_info)
        mock_mail.assert_called_once_with('test@gmail.com',
                                          'User Account Creation',
                                          templates['user_creation_email'],
                                          substitutions=expected_substitutions)
