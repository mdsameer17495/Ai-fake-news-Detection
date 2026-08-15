#!/usr/bin/env bash
# Render build script — installs system dependencies + Python packages

set -o errexit

# Install Tesseract OCR and Hindi language data
apt-get update && apt-get install -y tesseract-ocr tesseract-ocr-hin

# Install Python dependencies
pip install --upgrade pip
pip install -r backend/requirements.txt
