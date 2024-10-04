#!/bin/sh
export APP_MODULE=${APP_MODULE:-"app.main:app"}
export HOST=${HOST:-0.0.0.0}
export PORT=${PORT:-8000}
export WORKERS=${WORKERS:-1}
export TIMEOUT=${TIMEOUT:-60}
export LOG_LEVEL=${LOG_LEVEL:-debug}

exec gunicorn -b ${HOST}:${PORT} -w ${WORKERS} -t ${TIMEOUT} -k uvicorn.workers.UvicornWorker --log-level ${LOG_LEVEL} ${APP_MODULE}