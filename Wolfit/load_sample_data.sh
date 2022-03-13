#!/bin/bash
export FLASK_ENV=development
export FLASK_DEBUG=0
export WOLFIT_SETTINGS=$(pwd)/dev.settings
python load_reddit_posts.py
