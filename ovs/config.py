"""
config is for all the particular setup details such as
the app environment, database name and ip, super user account
details, etc...
"""
import os
import sys

class Config(object):
    """ The Config object stores all of the setup information """
    APP_ENV = os.getenv('APP_ENV', 'DEV')
    SECRET_KEY = os.getenv('SECRET', 'VERY_SPECIAL_KEY')
    DEVELOPMENT = APP_ENV == 'DEV'
    TESTING = APP_ENV == 'TEST'
    TEST_MAIL = False
    PRODUCTION = APP_ENV == 'PROD'
    DOMAIN_NAME = 'ovs-overseer.azurewebsites.net'
    SENDGRID_API_KEY = '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'
    SENDGRID_DEFAULT_FROM = 'admin@{domain_name}'.format(domain_name=DOMAIN_NAME)

    if not DEVELOPMENT and not TESTING and not PRODUCTION:
        sys.exit('Please enter a valid environment')

    PORT = os.getenv('PORT', 8080)

    DATABASE = {
        'primary': {
            'host': os.getenv('DB_HOSTNAME', '127.0.0.1'),
            'name': os.getenv('DB_NAME', 'ovs'),
            'password': os.getenv('DB_PASSWORD', 'pass123'),
            'port': os.getenv('DB_PORT', '3306'),
            'user': os.getenv('DB_USER', 'root'),
        },
        'pool': {
            'size': os.getenv('DB_POOL_SIZE', 200),
            'idleTimeout': os.getenv('DB_POOL_TIMEOUT', 5)
        }
    }

    SUPERUSER = {
        'email': os.getenv('SUPERUSER_EMAIL', 'admin@example.com'),
        'first_name': os.getenv('SUPERUSER_FIRSTNAME', 'John'),
        'last_name': os.getenv('SUPERUSER_LASTNAME', 'Smith'),
        'password': os.getenv('SUPERUSER_PASSWORD', 'ABCD1234')
    }
