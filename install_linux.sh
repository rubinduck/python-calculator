#!/bin/bash
python -m venv venv
source venv/bin/activate
pip install --upgrade pip # without this line PyQt5 install gives error
pip install -r requirements.txt
