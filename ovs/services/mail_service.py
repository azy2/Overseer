"""
Send Mail functions.
"""
from ovs import app

mail = app.mail
DOMAIN_NAME = app.config['DOMAIN_NAME']


class MailService:
    """Contains methods related to the sendgrid mail provider"""
    @staticmethod
    def send_email(to_email, subject, text, substitutions=None):
        """Send an email to the recipient."""
        if app.config['TEST_MAIL'] or app.config['PRODUCTION']:
            from_email = 'no-reply@{domain_name}'.format(domain_name=DOMAIN_NAME)
            mail.send_email(
                from_email=from_email,
                to_email=to_email,
                subject=subject,
                text=text if not substitutions else text.format(**substitutions)
