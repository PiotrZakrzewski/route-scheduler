#!/bin/bash
rm -rf env
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
docker-compose build
docker-compose up > /tmp/compose.out &
python utils/push-coordinates.py
python utils/test-consumer.py
docker-compose down
