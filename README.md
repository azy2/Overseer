This is Overseer.
# Setup
Vagrant
-------
One time setup: `vagrunt up`

Using dev env post setup: `vagrant ssh`, `python3 main.py`

Local
-----
Example setup using ubuntu:

One time setup:
```bash
#!/bin/bash
sudo apt update
sudo apt install -y make g++ mysql-server-5.7 python3 python3-virtualenv
sudo service mysql restart
sudo mysql -u root -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH
mysql_native_password BY 'pass123'; FUSH PRIVILEGES;"
mysql -u root -p"pass123" -e "CREATE DATABASE ovs"
echo "[mysqld]\nbind-address = localhost\n" > sudo tee
/etc/mysql/mysql.conf.d/overseer.cnf
sudo service mysql restart
python3 -m venv ../venv
source ../venv/bin/activate
pip install -r requirements.txt
export DB_USERNAME=root
export DB_PASSWORD=pass123
export DB_HOSTNAME=127.0.0.1
export DB_PORT=3306
export DB_NAME=ovs
cd database
alembic upgrade head
```

Run `source ../venv/bin/activate` everytime you start coding.

Manual env configuration
------------------------
| Environment Variable | Config                                    |
| -------------        | :-------------:                           |
| APP_ENV              | config['APP_ENV']                         |
| SECRET_KEY           | config['SECRET']                          |
| DB_HOSTNAME          | config['DATABASE']['primary']['host']     |
| DB_NAME              | config['DATABASE']['primary']['name']     |
| DB_PASSWORD          | config['DATABASE']['primary']['password'] |
| DB_PORT              | config['DATABASE']['primary']['port']     |
| DB_USER              | config['DATABASE']['primary']['user']     |
| DB_POOL_SIZE         | config['DATABASE']['pool']['size']        |
| DB_POOL_TIMEOUT      | config['DATABASE']['pool']['idleTimeout'] |
| SUPERUSER_EMAIL      | config['SUPERUSER']['email']              |
| SUPERUSER_PASSWORD   | config['SUPERUSER']['password']           |
