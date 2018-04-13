"""
Send Mail functions.
"""
import logging

from flask import current_app
from python_http_client.exceptions import HTTPError
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Content, Email, Mail


class MailService:
    """Contains methods related to the sendgrid mail provider"""

    @staticmethod
    def send_email(to_email, subject, text, substitutions=None):
        """
        Send an email to the recipient.

        Args:
            to_email: Recipient email address.
            subject: Email subject.
            text: Email body.
            substitutions: Text substitution that should be applied.

        Returns:
            A (mail, response) tuple.
        """
        sg = SendGridAPIClient(apikey=current_app.config['SENDGRID']['API_KEY'])

        from_email = Email(
            'no-reply@{domain_name}'.format(domain_name=current_app.config['SENDGRID']['DOMAIN_NAME']))
        to_email = Email(to_email)
        content = Content(
            'text/plain', text if not substitutions else text.format(**substitutions))
        mail = Mail(from_email=from_email,
                    subject=subject,
                    to_email=to_email,
                    content=content)

        try:
            if current_app.config['TEST_MAIL'] or current_app.config['PRODUCTION']:
                response = sg.client.mail.send.post(request_body=mail.get())
                if current_app.config['PRODUCTION'] and response.status_code != 202:
                    logging.error('%s Failed to send email: %s',
                                  response.status_code, mail.get())
                    return None
                return mail, response
            return None
        except HTTPError:
            logging.exception('Failed to send email.')
            return None
