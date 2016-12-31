# Set up Database and Python Packages
cp /vagrant/vagrant_config/.pgpass /home/vagrant/.pgpass
sudo chown vagrant /home/vagrant/.pgpass
sudo chmod 600 /home/vagrant/.pgpass

# Postgres Permissions
sudo rm /etc/postgresql/9.3/main/pg_hba.conf
sudo cp /vagrant/vagrant_config/pg_hba.conf /etc/postgresql/9.3/main/pg_hba.conf
sudo chmod 644 /etc/postgresql/9.3/main/pg_hba.conf
sudo chown postgres /etc/postgresql/9.3/main/pg_hba.conf
sudo chgrp postgres /etc/postgresql/9.3/main/pg_hba.conf
sudo /etc/init.d/postgresql restart