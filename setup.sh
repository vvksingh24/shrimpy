#!/bin/bash

# install redis
echo "installing redis server"

sudo apt install redis-server

echo "redis-server successfully installed"

echo "enter virtual environment name"

read venv_name

echo "creating virtual environment"

python3 -m venv "$venv_name"

echo "virtual environment created"
echo "activating virtual environment"


source "$venv_name"/bin/activate

echo "installing requirements"

pip install -r requirements.txt

echo "requirements installed"
python manage.py makemigrations

python manage.py migrate
