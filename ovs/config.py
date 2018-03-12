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
        raise KeyError("Running in production, please override %s" % (key))
    return os.environ[key]

class Config(object):
    """ The Config object stores all of the setup information """
    APP_ENV = os.getenv('APP_ENV', 'DEV')
    env_load = os.getenv
    if APP_ENV == 'prod':
        env_load = prod_env_load

    SECRET_KEY = env_load('SECRET', 'VERY_SPECIAL_KEY')
    DEVELOPMENT = APP_ENV == 'DEV'
    TESTING = APP_ENV == 'TEST'
    PRODUCTION = APP_ENV == 'PROD'
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

    SUPERUSER = {
        'email': os.getenv('SUPERUSER_EMAIL', 'admin@gmail.com'),
        'first_name': os.getenv('SUPERUSER_FIRSTNAME', 'Super'),
        'last_name': os.getenv('SUPERUSER_LASTNAME', 'User'),
        'password': os.getenv('SUPERUSER_PASSWORD', 'abcd1234')
    }
    RESIDENT = {
        'email': os.getenv('RESIDENT_EMAIL', 'resident@gmail.com'),
        'first_name': os.getenv('RESIDENT_FIRSTNAME', 'John'),
        'last_name': os.getenv('RESIDENT_LASTNAME', 'Smith'),
        'password': os.getenv('RESIDENT_PASSWORD', 'abcd1234')
    }
