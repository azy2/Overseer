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
    PRODUCTION = APP_ENV == 'PROD'
    if not DEVELOPMENT and not TESTING and not PRODUCTION:
        sys.exit('Please enter a valid environment')

    PORT = os.getenv('PORT', 8080)

    TEMPLATES_AUTO_RELOAD = True

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
        'password': os.getenv('SUPERUSER_PASSWORD', 'abcd1234')
    }
    RESIDENT = {
        'email': os.getenv('RESIDENT_EMAIL', 'resident@gmail.com'),
        'first_name': os.getenv('RESIDENT_FIRSTNAME', 'John'),
        'last_name': os.getenv('RESIDENT_LASTNAME', 'Smith'),
        'password': os.getenv('RESIDENT_PASSWORD', 'abcd1234')
    }
