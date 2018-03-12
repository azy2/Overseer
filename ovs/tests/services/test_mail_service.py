"""Test for sending mail."""

import json
from unittest import TestCase

from mock import patch

from ovs import app
from ovs.services import mail_service


class TestSendMail(TestCase):
    """Tests for sending mail."""

    def setUp(self):
        app.config['TESTING'] = True
        app.config['TEST_MAIL'] = True
        self.mail = app.mail

    def tearDown(self):
        app.config['TESTING'] = False
        app.config['TEST_MAIL'] = False

    @patch('python_http_client.Client._make_request')
    def test_send_mail(self, mock_client):
        """Test that mail contains correct information."""
        mail_service.send_email(
            to_email='testEmail@test.com',
            subject='TestSubject',
            text='testText')
        mock_client.assert_called()
        self.assertEqual(json.dumps(self.mail.get(), sort_keys=True),
                         '{"content": [{"type": "text/plain", "value": "testText"}], "from": {"email": "no-reply@ovs-overseer.azurewebsites.net"}, "personalizations": [{"to": [{"email": "testEmail@test.com"}]}], "subject": "TestSubject"}')  # pylint: disable=line-too-long

    # pylint: disable=no-self-use
    @patch('ovs.services.mail_service.send_email')
    def test_send_account_creation_email(self, mock_mail):
        """Test that account creation mail contain correct info."""
        mail_service.send_account_creation_email(
            to_email='testEmail@test.com',
            first_name='testFirstName',
            last_name='testLastName',
            role='testRole')
        mock_mail.assert_called_once_with(
            to_email='testEmail@test.com',
            subject='Your New Account',
            text='Hi testFirstName testLastName, thank you for creating your account!\nYour role is: testRole')
    # pylint: enable=no-self-use
