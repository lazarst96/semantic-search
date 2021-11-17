#!/bin/sh

#gunicorn -w 1 -k uvicorn.workers.UvicornWorker src.main:app -b 0.0.0.0:80
uvicorn src.main:app --port 80 --host 0.0.0.0 --reload