#!/bin/bash
set -e
grep TWITTER ../setenvvars.sh | awk -F ' ' '{print $2}' > env.list
pylint *.py
docker build --tag waterstandtwitter .
