import os, sys

# TODO force production to set env vals instead of using defaults
class Config(object):
	APP_ENV = os.getenv('APP_ENV', 'DEV')
	SECRET_KEY = os.getenv('SECRET', 'VERY_SPECIAL_KEY')
	DEVELOPMENT = APP_ENV == 'DEV'
	TESTING = APP_ENV == 'TEST'
	PRODUCTION = APP_ENV == 'PROD'
	if not DEVELOPMENT and not TESTING and not PRODUCTION:
		# TODO Add logging
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
		'password': os.getenv('SUPERUSER_PASSWORD', 'ABCD1234')
	}
