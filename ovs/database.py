from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Database():
    def __init__(self, app):
        # TODO clean up, handle TEST mode
        database = app.config['DATABASE']
        url = 'mysql+pymysql://' +                    \
              database['primary']['user'] + ':' +     \
              database['primary']['password'] + '@' + \
              database['primary']['host'] + ':' +     \
              database['primary']['port'] + '/' +     \
              database['primary']['name']

        self._engine = create_engine(url, pool_size=database['pool']['size'], pool_timeout=database['pool']['idleTimeout'])
        self._db = sessionmaker(bind=self._engine)()

    def __del__(self):
        self._db.close()

    def instance(self):
        return self._db

    def engine(self):
        return self._engine
