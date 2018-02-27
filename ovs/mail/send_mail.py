"""
Send Mail functions.
"""
from flask_sendgrid import SendGrid
from ovs import app

app.config['SENDGRID_API_KEY'] = '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'
app.config['SENDGRID_DEFAULT_FROM'] = 'admin@ovs.com'
mail = SendGrid(app)


def send_email(to_email, subject, text):
    """Send an email to the recipient."""
    if app.config['TESTING'] or app.config['DEVELOPMENT']:
        return
    from_email = 'no-reply@ovs.com'
    mail.send_email(
        from_email=from_email,
        to_email=to_email,
        subject=subject,
        text=text)


def send_account_creation_email(to_email, first_name, last_name, role):
    """Send account creation email to new user."""
    subject = 'Your Account'
    text = 'Hi %s %s, thank you for creating your account!\nYour role is:%s' % (first_name, last_name, role)
    send_email(to_email, subject, text)
