#!/bin/sh

gunicorn -w 1 -k uvicorn.workers.UvicornWorker src.main:app -b 0.0.0.0:80