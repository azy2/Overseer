# pylint: disable=line-too-long
"""Contains the templates for sendgrid mailing"""
TEMPLATES = {
    'user_creation_email': 
        'Hi {first_name} {last_name},\n \
        Your {role} account was successfully created. Please click the link below<br>\n \
        to confirm your email address and activate your account:\n \
        <p><a href="{{ confirm_url }}">{{ confirm_url }}</a></p>'
}
