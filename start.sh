#!/bin/bash

DB_USER=webtemp_user
DB_PASSWORD=webtemp_password
DB_NAME=webtemp_local


# DB
sudo apt-get install postgresql
sudo apt-get install python-psycopg2
sudo apt-get install libpq-dev


# Installing Python Package Manager
sudo pip3 install pipenv

# Activating Environment
pipenv shell

# Installing Dependencies
pipenv install

# Coping .env_default to .env
cp .env_default .env


# CREATING DATABASE
echo "Creating new Database"
sudo -u postgres createdb $DB_NAME


#CREATING NEW ROLE
echo "Creating new Role"
sudo -u postgres psql -c "CREATE USER $DB_USER WITH ENCRYPTED PASSWORD '$DB_PASSWORD'"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER"
