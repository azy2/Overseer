# pylint: disable=line-too-long
"""Contains the templates for sendgrid mailing"""
TEMPLATES = {
    'user_creation_email':
        'Hi $first_name $last_name,\n \
        Your $role account was successfully created. Please click the link below\n \
        to confirm your email address and activate your account:\n \
        <html><p><a href="$confirm_url">Activate your account</a></p></html>',
    'user_reset_email':
        'Hi, you asked for a password reset email! Please click the link below\n \
        to reset your password:\n \
        <html><p><a href="$reset_url">Reset your password</a></p></html>'
}
