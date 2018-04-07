"""
Send Mail functions.
"""
from flask import current_app

class MailService:
    """Contains methods related to the sendgrid mail provider"""
    @staticmethod
    def send_email(to_email, subject, text, substitutions=None):
        """Send an email to the recipient."""
        mail = current_app.extensions['mail']

        if current_app.config['TEST_MAIL'] or current_app.config['PRODUCTION']:
            from_email = 'no-reply@{domain_name}'.format(domain_name=current_app.config['DOMAIN_NAME'])
            mail.send_email(
                from_email=from_email,
                to_email=to_email,
                subject=subject,
                text=text if not substitutions else text.format(**substitutions)
            )
