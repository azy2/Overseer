"""
config is for all the particular setup details such as
the app environment, database name and ip, super user account
details, etc...
"""
import os
import sys


def prod_env_load(key, _):
    """Forces production environment loads to set keys instead of using defaults"""
    if key not in os.environ:
        raise KeyError("Running in production, please override %s" % key)
    return os.environ[key]


class Config(object):
    """ The Config object stores all of the setup information """
    APP_ENV = os.getenv('APP_ENV', 'DEV')
    env_load = os.getenv
    if APP_ENV == 'PROD':
        env_load = prod_env_load

    SECRET_KEY = env_load('SECRET', 'VERY_SPECIAL_KEY')
    DEVELOPMENT = APP_ENV == 'DEV'
    TESTING = APP_ENV == 'TEST'
    TEST_MAIL = False
    PRODUCTION = APP_ENV == 'PROD'
    DOMAIN_NAME = env_load('DOMAIN_NAME', 'ovs-overseer.azurewebsites.net')
    SENDGRID_API_KEY = env_load('SENDGRID_API_KEY', 'FAKEAPIKEY')
    SENDGRID_DEFAULT_FROM = 'admin@{domain_name}'.format(
        domain_name=DOMAIN_NAME)

    if not DEVELOPMENT and not TESTING and not PRODUCTION:
        sys.exit('Please enter a valid environment')

    PORT = env_load('PORT', 8080)

    TEMPLATES_AUTO_RELOAD = True

    DATABASE = {
        'primary': {
            'host': env_load('DB_HOSTNAME', '127.0.0.1'),
            'name': env_load('DB_NAME', 'ovs'),
            'password': env_load('DB_PASSWORD', 'pass123'),
            'port': env_load('DB_PORT', '3306'),
            'user': env_load('DB_USER', 'root'),
        },
        'pool': {
            'size': os.getenv('DB_POOL_SIZE', 200),
            'idleTimeout': os.getenv('DB_POOL_TIMEOUT', 5)
        }
    }

    BLOB = {
        'account': env_load('BLOB_ACCOUNT', 'overseer'),
        'key': env_load('BLOB_KEY', ''),
        'default_picture_path': env_load('DEFAULT_PICTURE_PATH',
                                         'ovs/static/default_profile.png')
    }

    ADMIN = {
        'email': env_load('ADMIN_EMAIL', 'admin@gmail.com'),
        'first_name': env_load('ADMIN_FIRSTNAME', 'Admin'),
        'last_name': env_load('ADMIN_LASTNAME', 'User'),
        'password': env_load('ADMIN_PASSWORD', 'abcd1234')
    }
    BUILDING_MANAGER = {
        'email': 'building_manager@gmail.com',
        'first_name': 'Building',
        'last_name': 'Manager',
        'password': 'abcd1234'
    }
    OFFICE_MANAGER = {
        'email': 'office_manager@gmail.com',
        'first_name': 'Office',
        'last_name': 'Manager',
        'password': 'abcd1234'
    }
    STAFF = {
        'email': 'staff@gmail.com',
        'first_name': 'Staff',
        'last_name': 'Smith',
        'password': 'abcd1234'
    }
    RESIDENT_ADVISOR = {
        'email': 'resident_advisor@gmail.com',
        'first_name': 'Resident',
        'last_name': 'Advisor',
        'password': 'abcd1234'
    }
    RESIDENT = {
        'email': 'resident@gmail.com',
        'first_name': 'John',
        'last_name': 'Smith',
        'password': 'abcd1234'
    }
