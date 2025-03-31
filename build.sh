#!/bin/bash
set -e
pip install --quiet --no-cache-dir --requirement requirements.txt
pip list --outdated
pylint *.py
coverage run -m pytest
coverage report -m
docker build --tag waterstandtwitter .
