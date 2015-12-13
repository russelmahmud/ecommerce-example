#!/usr/bin/env bash

pip install -r requirements.txt

rm db.sqlite3

./manage.py migrate

./manage.py loaddata account/fixtures/*.json
./manage.py loaddata product/fixtures/*.json
