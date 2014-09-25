#!/usr/bin/env bash

# Stop on the first error and unset variables are errors
set -eu

HOST_RESOURCES_DIR="resources"
PROJECTS_DIR=~/projects
DJANGO_DIR="${PROJECTS_DIR}/dontWasteTime/webapp/crawler_app"


echo "Start provisioning"

sudo apt-get update

echo "1. Scrapy dependencies installation"
sudo apt-get install -y python-pip python-dev libffi-dev libssl-dev libxml2-dev libxslt1-dev

echo "2. PostgreSQL installation"
sudo apt-get install -y postgresql postgresql-contrib pgadmin3 libpq-dev
PSQL_ROOT=/etc/postgresql
PSQL_VERSION=$(ls $PSQL_ROOT)
PSQL_DIR=${PSQL_ROOT}/${PSQL_VERSION}/main
sudo cp /vagrant/${HOST_RESOURCES_DIR}/postgresql.conf $PSQL_DIR
sudo cp /vagrant/${HOST_RESOURCES_DIR}/pg_hba.conf $PSQL_DIR
sudo service postgresql restart

# ignore errors, it means that provisioning is not run for the first time
sudo -u postgres psql -c "create user \"crawleruser\" with password 'crawl_lova'" 2> /dev/null || true
sudo -u postgres psql -c "create database \"crawlerdb\" with owner \"crawleruser\"" 2> /dev/null || true

echo "3. Git installation"
sudo apt-get install -y git

echo "4. Virtualenv installation"
sudo pip install virtualenv virtualenvwrapper

# virtualenvwrapper uses unbound variables
set +u
cp /vagrant/${HOST_RESOURCES_DIR}/bashrc /home/vagrant/.bashrc
source ~/.bashrc
export WORKON_HOME=~/Envs
source /usr/local/bin/virtualenvwrapper.sh
set -u

echo "5. Preparing virtual envrionment"
# virtualenvwrapper uses unbound variables
set +eu
mkvirtualenv dontWasteTime
set -eu
pip install scrapy ipython pytz django psycopg2


echo "6. Clone project repository"
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

echo "7. Set up webapp environment"
cd $DJANGO_DIR
./manage.py migrate


echo "Provisioning ended successfully"
