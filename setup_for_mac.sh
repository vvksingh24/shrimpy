#!/bin/bash

# install redis
echo "installing redis server"

brew install redis

echo "redis-server successfully installed"

echo "creating virtual environment"

read venv_name

python3 -m venv "$venv_name"

echo "virtual environment created"
echo "activating virtual environment"


source "$venv_name"/bin/activate

echo "installing requirements"

pip install -r requirements.txt

echo "requirements installed"
python manage.py makemigrations

python manage.py migrate
