#!/usr/bin/env bash

# Stop on the first error and unset variables are errors
set -eu

HOST_RESOURCES_DIR=/vagrant/resources
PROJECTS_DIR=~/projects
DJANGO_DIR=${PROJECTS_DIR}/dontWasteTime/webapp/crawler_app
LOGS_DIR=/var/log/dontWasteTime


echo "Start provisioning"

sudo apt-get update

echo "1. Scrapy dependencies installation"
sudo apt-get install -y python-pip python-dev libffi-dev libssl-dev libxml2-dev libxslt1-dev

echo "2. PostgreSQL installation"
sudo apt-get install -y postgresql postgresql-contrib pgadmin3 libpq-dev
PSQL_ROOT=/etc/postgresql
PSQL_VERSION=$(ls $PSQL_ROOT)
PSQL_DIR=${PSQL_ROOT}/${PSQL_VERSION}/main
sudo cp ${HOST_RESOURCES_DIR}/postgresql.conf $PSQL_DIR
sudo cp ${HOST_RESOURCES_DIR}/pg_hba.conf $PSQL_DIR
sudo service postgresql restart

# ignore errors, it means that provisioning is not run for the first time
sudo -u postgres psql -c "create user \"crawleruser\" with password 'crawl_lova'" 2> /dev/null || true
sudo -u postgres psql -c "create database \"crawlerdb\" with owner \"crawleruser\"" 2> /dev/null || true

echo "3. RabbitMQ installation and set up"
sudo apt-get install -y rabbitmq-server
# ignore errors, because commands may return nonzeroes
set +e
VHOSTS_COUNT=$(sudo rabbitmqctl list_vhosts | grep -c /crawler_app)
if [ $VHOSTS_COUNT -eq 0 ]; then
    sudo rabbitmqctl add_vhost /crawler_app
else
    echo "vhost /crawler_app currently exists"
fi

USERS_COUNT=$(sudo rabbitmqctl list_users | grep -c crawler_user)
if [ $USERS_COUNT -eq 0 ]; then
    sudo rabbitmqctl add_user crawler_user q6e56VH2eFXaE7D
else
    echo "user crawler_user currently exists"
fi

PERMISSIONS_COUNT=$(sudo rabbitmqctl list_permissions -p /crawler_app | grep -c crawler_user)
if [ $PERMISSIONS_COUNT -eq 0 ]; then
    sudo rabbitmqctl set_permissions -p /crawler_app crawler_user ".*" ".*" ".*"
else
    echo "permissions for /crawler_app vhost already set"
fi
set -e

echo "4. Git installation"
sudo apt-get install -y git

echo "5. Virtualenv installation"
sudo pip install virtualenv virtualenvwrapper

# virtualenvwrapper uses unbound variables
set +u
cp ${HOST_RESOURCES_DIR}/bashrc /home/vagrant/.bashrc
source ~/.bashrc
export WORKON_HOME=~/Envs
source /usr/local/bin/virtualenvwrapper.sh
set -u

echo "6. Preparing virtual envrionment"
# virtualenvwrapper uses unbound variables
set +eu
VIRTUALENVS_COUNT=$(lsvirtualenv | grep -c dontWasteTime)
if [ $VIRTUALENVS_COUNT -eq 0 ]; then
    mkvirtualenv dontWasteTime
fi
workon dontWasteTime
set -eu

pip install scrapy ipython pytz django psycopg2 celery gunicorn


echo "7. Clone project repository"
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

echo "8. Set up webapp environment"
cd $DJANGO_DIR
./manage.py migrate

echo "9. Set up supervisor"
sudo apt-get install -y supervisor
if [ ! -d $LOGS_DIR ]; then
    sudo mkdir $LOGS_DIR
fi
sudo supervisorctl stop all
SUPERVISOR_CONF_DIR=/etc/supervisor/conf.d
sudo cp $HOST_RESOURCES_DIR/supervisor/* $SUPERVISOR_CONF_DIR/
sudo supervisorctl update
sudo supervisorctl start all

echo "Provisioning ended successfully"
