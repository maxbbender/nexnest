# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.network "forwarded_port", guest: 8000, host: 8000
  config.vm.provision :shell, path: "vagrant_config/ubuntu/ubuntu_dependencies_script.sh"
  config.vm.provision :shell, path: "vagrant_config/ubuntu/pyenv_install_script.sh", privileged: false
  config.vm.provision :shell, path: "vagrant_config/ubuntu/python_install_script.sh", privileged: false
  config.vm.provision :shell, path: "vagrant_config/ubuntu/postgres_config.sh"
end
