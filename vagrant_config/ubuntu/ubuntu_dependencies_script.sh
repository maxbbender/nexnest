sudo apt-get update

# Install Git
sudo apt-get install -y git

# Dependencies
sudo apt-get install -y make build-essential libssl-dev libpq-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils
sudo apt-get install -y graphviz libgraphviz-dev pkg-config

# Install Postgres
sudo apt-get install -y postgresql postgresql-contrib

# Environment Variables
echo 'export MAIL_USERNAME="no_reply@nexnest.com"'  >> /home/vagrant/.bashrc
echo 'export MAIL_PASSWORD="t6OtmrY77AEEeEn"'  >> /home/vagrant/.bashrc
echo 'export GOOGLE_MAPS_KEY="AIzaSyAaosOp5nB3yMtx8-k-_MbLwxS1MGnwg_c"'  >> /home/vagrant/.bashrc
echo 'export GOOGLE_CAPTCHA_KEY="6LcjSy0UAAAAAPJpuJ4r1uD2nwtDIshTgGkg9Ywa"'  >> /home/vagrant/.bashrc
echo 'export SECURITY_PASSWORD_SALT="domislove"'  >> /home/vagrant/.bashrc
echo 'export SECRET_KEY="domislove"'  >> /home/vagrant/.bashrc
echo 'export FLASK_CONFIG="development"'  >> /home/vagrant/.bashrc
echo 'export BRAINTREE_MERCHANT_ID="95d9g95dztdsgkkh"'  >> /home/vagrant/.bashrc
echo 'export BRAINTREE_PUBLIC_KEY="fdtk8w9qbpvqr6kn"'  >> /home/vagrant/.bashrc
echo 'export BRAINTREE_PRIVATE_KEY="ec367f7335d5e9c222656212e1ff78f2"'  >> /home/vagrant/.bashrc
echo 'export BRAINTREE_ENV="sandbox"'  >> /home/vagrant/.bashrc