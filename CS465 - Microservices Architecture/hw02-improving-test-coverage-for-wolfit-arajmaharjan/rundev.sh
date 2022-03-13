#!/bin/bash
export WOLFIT_SETTINGS=$(pwd)/dev.settings
export ACT_URL=http://localhost:5001

flask run --host=0.0.0.0 
