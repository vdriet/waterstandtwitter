#!/bin/bash
set -e
export PYTHONPATH=.
pip install --no-cache-dir -r requirements.txt
pip list --outdated
pylint *.py
coverage run -m pytest
coverage report -m
docker build --tag waterstandtwitter .
