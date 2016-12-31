sudo apt-get update

# Install Git
sudo apt-get install -y git

# Dependencies
sudo apt-get install -y make build-essential libssl-dev libpq-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils
sudo apt-get install -y graphviz libgraphviz-dev pkg-config

# # Install pyenv
# git clone https://github.com/yyuu/pyenv.git /home/vagrant/.pyenv
# echo 'export PYENV_ROOT="/home/vagrant/.pyenv"' >> /home/vagrant/.bashrc
# echo 'export PATH="/home/vagrant/.pyenv/bin:$PATH"' >> /home/vagrant/.bashrc
# echo 'eval "$(pyenv init -)"' >> /home/vagrant/.bashrc
# sudo chown -R vagrant /home/vagrant/.pyenv
# source /home/vagrant/.bashrc
# # curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
# # pyenv update

# # Install Python 3.6.0
# pyenv install 3.6.0
# pyenv global 3.6.0
# source /home/vagrant/.bashrc

# # Install Postgres
# sudo apt-get install -y postgresql postgresql-contrib

# # Set up Database and Python Packages
# cp /vagrant/vagrant_config/.pgpass /home/vagrant/.pgpass
# sudo chmod 600 /home/vagrant/.pgpass

# # Postgres Permissions
# sudo rm /etc/postgresql/9.3/main/pg_hba.conf
# sudo cp /vagrant/vagrant_config/pg_hba.conf /etc/postgresql/9.3/main/pg_hba.conf
# sudo chmod 644 /etc/postgresql/9.3/main/pg_hba.conf
# sudo chown postgres /etc/postgresql/9.3/main/pg_hba.conf
# sudo chgrp postgres /etc/postgresql/9.3/main/pg_hba.conf

# cd /vagrant
# make user_setup
# make install


