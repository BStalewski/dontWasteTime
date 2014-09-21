#!/usr/bin/env bash

echo "Start provisioning"

cp /vagrant/bashrc /home/vagrant/.bashrc
source ~/.bashrc

sudo apt-get update
sudo apt-get install -y python-pip python-dev libffi-dev libssl-dev libxml2-dev libxslt1-dev
sudo apt-get install -y git
sudo pip install virtualenv virtualenvwrapper

export WORKON_HOME=~/Envs
source /usr/local/bin/virtualenvwrapper.sh

mkvirtualenv dontWasteTime

pip install scrapy ipython

if [ ! -d ~/projects/ ]; then
    mkdir ~/projects
fi

cd ~/projects

if [ ! -d ~/projects/dontWasteTime ]; then
    git clone https://github.com/BStalewski/dontWasteTime.git
else
    cd dontWasteTime
    git pull
fi

echo "Provisioning ended successfully"
