"""Test for sending mail."""

import json
from unittest import TestCase

from mock import patch

from ovs import app
from ovs.services.mail_service import MailService as mail_service
from ovs.services.user_service import UserService


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
                         '{"content": [{"type": "text/plain", "value": "testText"}], "from": {"email": '
                         '"no-reply@ovs-overseer.azurewebsites.net"}, "personalizations": [{"to": [{"email": '
                         '"testEmail@test.com"}]}], "subject": "TestSubject"}')

    #pylint: disable=no-self-use
    @patch('ovs.services.mail_service.send_email')
    def test_create_user_sends_email(self, mock_mail):
        """ Tests that creating a user sends an email """
        test_user_info = ('test@gmail.com', 'Bob', 'Ross', 'ADMIN')
        UserService.create_user(*test_user_info)
        mock_mail.assert_called_once_with(*test_user_info)
    # pylint: enable=no-self-use
