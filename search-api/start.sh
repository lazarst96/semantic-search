#!/bin/sh

export PYTHONPATH=./

python ./src/wait_for_deps.py
python ./src/init_db.py

gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.main:app -b 0.0.0.0:80
#uvicorn src.main:app --port 80 --host 0.0.0.0 --reload