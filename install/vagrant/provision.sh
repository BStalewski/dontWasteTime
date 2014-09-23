#!/usr/bin/env bash

PROJECTS_DIR=~/projects
DJANGO_DIR="${PROJECTS_DIR}/dontWasteTime/webapp/crawler_app"


echo "Start provisioning"

cp /vagrant/bashrc /home/vagrant/.bashrc
source ~/.bashrc

sudo apt-get update
sudo apt-get install -y python-pip python-dev libffi-dev libssl-dev libxml2-dev libxslt1-dev
sudo apt-get install -y git
sudo apt-get install -y postgresql postgresql-contrib pgadmin3
sudo pip install virtualenv virtualenvwrapper

export WORKON_HOME=~/Envs
source /usr/local/bin/virtualenvwrapper.sh

mkvirtualenv dontWasteTime

pip install scrapy ipython pytz django

if [ ! -d $PROJECTS_DIR ]; then
    mkdir $PROJECTS_DIR
fi

cd $PROJECTS_DIR

if [ ! -d "${PROJECTS_DIR}/dontWasteTime" ]; then
    git clone https://github.com/BStalewski/dontWasteTime.git
else
    cd dontWasteTime
    git pull
fi

cd $DJANGO_DIR
./manage.py migrate


echo "Provisioning ended successfully"
