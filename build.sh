#!/usr/bin/env bash

set -o errexit

apt-get update
apt-get install -y tesseract-ocr tesseract-ocr-hin

pip install --upgrade pip
pip install -r backend/requirements.txt
