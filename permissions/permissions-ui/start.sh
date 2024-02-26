#!/bin/bash

python3 permissions/permissions-ui/manage.py reset_db
python3 permissions/permissions-ui/manage.py migrate
python3 permissions/permissions-ui/manage.py runserver 0.0.0.0:8000