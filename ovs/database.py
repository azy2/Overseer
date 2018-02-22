"""
Database interface code
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Database():
    """
    Database is the implementation for app.database and provides sqlalchemy
    with a target.
    """
    def __init__(self, app):
        database = app.config['DATABASE']
        url = 'mysql+pymysql://' +                    \
              database['primary']['user'] + ':' +     \
              database['primary']['password'] + '@' + \
              database['primary']['host'] + ':' +     \
              database['primary']['port'] + '/' +     \
              database['primary']['name']

        self._engine = create_engine(url, pool_size=database['pool']['size'],
                                     pool_timeout=
                                     database['pool']['idleTimeout'])
        self._db = sessionmaker(bind=self._engine)()

    def __del__(self):
        self._db.close()

    def instance(self):
        """ Get a handle to the database """
        return self._db

    def engine(self):
        """ Get a handle to the database engine """
        return self._engine
