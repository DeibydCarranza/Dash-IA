#!/usr/bin/env bash
#
# Create a virtualenv. Note that python 3.6 is currently the minimal requirement
#
# Stop on error, rather than continue and trash the environment
set -e
#
# Default to 3.8 but allow override
DEFAULT_PYTHON_VER=3.10
PYTHON_VER=${1:-$DEFAULT_PYTHON_VER}
# Clean
find . -name '*.pyc' -delete
find . -name '__pycache__' -delete
find . -name 'poetry.lock' -delete
find . -name 'Pipefile.lock' -delete
find . -name '*.log' -delete
find . -name '.coverage' -delete
find . -wholename 'logs/*.json' -delete
find . -wholename '*/.pytest_cache' -delete
find . -wholename '**/.pytest_cache' -delete
find . -wholename './logs/*.json' -delete
find . -wholename '.webassets-cache/*' -delete
find . -wholename './logs' -delete
find . -wholename './.reports' -delete

#
python${PYTHON_VER} -m venv venv
#
source venv/bin/activate
#
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip install urllib3
./manage.py migrate
#
python manage.py runserver

