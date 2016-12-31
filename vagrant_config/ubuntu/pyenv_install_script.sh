# Install pyenv
git clone https://github.com/yyuu/pyenv.git /home/vagrant/.pyenv
echo 'export PYENV_ROOT="/home/vagrant/.pyenv"' >> /home/vagrant/.bashrc
echo 'export PATH="/home/vagrant/.pyenv/bin:$PATH"' >> /home/vagrant/.bashrc
echo 'eval "$(pyenv init -)"' >> /home/vagrant/.bashrc
sudo chown -R vagrant /home/vagrant/.pyenv
exec $SHELL