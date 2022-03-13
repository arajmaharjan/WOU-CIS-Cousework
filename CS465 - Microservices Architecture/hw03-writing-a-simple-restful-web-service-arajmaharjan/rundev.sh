#!/bin/bash
export FLASK_APP=app.py
export FLASK_ENV=development
export SLEEP_TIME=${2:-0}


set -a
. ./sett.settings
set +a

flask run --host=0.0.0.0 --port $@ 