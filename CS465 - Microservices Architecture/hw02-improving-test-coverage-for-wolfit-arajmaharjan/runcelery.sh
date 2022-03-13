#!/bin/bash
export WOLFIT_SETTINGS=$(pwd)/dev.settings
export ACT_URL=http://localhost:5001

celery -A app.celery worker --loglevel=info 
