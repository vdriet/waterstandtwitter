#!/bin/bash
set -e
grep TWITTER ../setenvvars.sh | awk -F ' ' '{print $2}' > env.list
pip install -r requirements.txt
pip list --outdated
pylint *.py
docker build --tag waterstandtwitter .
