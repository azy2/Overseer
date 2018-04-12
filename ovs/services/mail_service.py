"""
Send Mail functions.
"""
import logging
from http.client import HTTPException

from flask import current_app
from flask_sendgrid import SendGrid

mail = SendGrid()


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
        """
        try:
            if current_app.config['TEST_MAIL'] or current_app.config['PRODUCTION']:
                from_email = 'no-reply@{domain_name}'.format(domain_name=current_app.config['DOMAIN_NAME'])
                mail.send_email(
                    from_email=from_email,
                    to_email=to_email,
                    subject=subject,
                    text=text if not substitutions else text.format(**substitutions)
                )
        except HTTPException:
            logging.exception('Failed to send email.')
