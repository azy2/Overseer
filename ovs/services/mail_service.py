"""
Send Mail functions.
"""
from ovs import app

mail = app.mail
DOMAIN_NAME = app.config['DOMAIN_NAME']


def send_email(to_email, subject, text):
    """Send an email to the recipient."""
    if app.config['TEST_MAIL'] or app.config['PRODUCTION']:
        from_email = 'no-reply@{domain_name}'.format(domain_name=DOMAIN_NAME)
        mail.send_email(
            from_email=from_email,
            to_email=to_email,
            subject=subject,
            text=text)


def send_account_creation_email(to_email, first_name, last_name, role):
    """Send account creation email to new user."""
    subject = 'Your New Account'
    text = 'Hi {first_name} {last_name}, thank you for creating your account!\nYour role is: {role}'.format(
        first_name=first_name, last_name=last_name, role=role)
    send_email(to_email=to_email, subject=subject, text=text)
