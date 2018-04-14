Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"

  config.vm.synced_folder ".", "/overseer/", create: "true"

  config.vm.provider :virtualbox do |vb|
    vb.name = "overseer-dev"
  end

  config.vm.provision "shell", privileged: true, inline: <<-DEPENDENCIES
    onerror(){ echo "Command failed. Stopping execution..."; exit 1; }
    trap onerror ERR
    cd /tmp

    echo "Updating package lists (this may take a while)"
    export DEBIAN_FRONTEND=noninteractive
    apt-get update

    echo "Installing system packages (this may take a while)"
    apt-get -y -q install make g++ mysql-server-5.7 chromium-browser python3-dev

    echo "Configuring MySQL"
    mysql_ssl_rsa_setup --uid=mysql &>/dev/null
    service mysql restart
    mysql -u root -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'pass123'; FLUSH PRIVILEGES;"
    mysql -u root -p"pass123" -e "CREATE DATABASE ovs"
    mysql -u root -p"pass123" -e "create user 'root'@'10.0.2.2' identified by 'pass123';grant all privileges on *.* to 'root'@'10.0.2.2' with grant option;flush privileges;"
    printf "[mysqld]\nbind-address = 0.0.0.0\n" > /etc/mysql/mysql.conf.d/overseer.cnf
    service mysql restart
    
    echo "Installing pip3"
    wget https://bootstrap.pypa.io/get-pip.py && python3 get-pip.py

  DEPENDENCIES

  config.vm.provision "shell", inline: <<-SETUP
    onerror(){ echo "Command failed. Stopping execution..."; exit 1; }
    trap onerror ERR

    cd /overseer/

    echo "Installing Python Requirements"
    python3 -m pip install -r requirements.txt

    echo "Exporting DB environment variables"
    export DB_USERNAME=root
    export DB_PASSWORD=pass123
    export DB_HOSTNAME=127.0.0.1
    export DB_PORT=3306
    export DB_NAME=ovs

    echo "cd /overseer" >> /home/vagrant/.bashrc
    echo "Finishing Setup"
  SETUP

  # forward localhost:8080 to host
  config.vm.network "forwarded_port", guest: 8080, host: ENV['VAGRANT_APP_PORT'] || 8080
  config.vm.network "forwarded_port", guest: 3306, host: ENV['VAGRANT_DB_PORT'] || 3306
end
