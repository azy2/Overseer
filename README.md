# Windows Setup
### Install Vagrant: https://www.vagrantup.com/
### Install Virtual Box: https://www.virtualbox.org/

## Excuete in CMD
### First Time Only
- `vagrant up`

### Run the Webapp Locally
- `vagrant ssh`
- `cd \overseer`
- `FLASK_APP=main.py flask run --host=0.0.0.0 -p 8080`


# Ubuntu Setup
### First Time Only
```bash
#!/bin/bash
# Install Requirements
sudo apt update
sudo apt install -y make g++ mysql-server-5.7 python3 python3-virtualenv
# Set Up MySQL DB
sudo mysql -u root -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH
mysql_native_password BY 'pass123'; FUSH PRIVILEGES;"
mysql -u root -p"pass123" -e "CREATE DATABASE ovs"
# Create Python Virtual Environment
python3 -m venv ../venv
echo "export DB_USERNAME=root\nexport DB_PASSWORD=pass123\nexport DB_HOSTNAME=127.0.0.1\nexport DB_PORT=3306\nexport DB_NAME=ovs\nexport FLASK_APP=main.py" >> ../venv/bin/activate
source ../venv/bin/activate
pip install -r requirements.txt
```

### Run the Webapp Locally
* `source venv/bin/activate`
* `flask run`