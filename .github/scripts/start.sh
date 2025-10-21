#!/bin/sh
if [ "$1" = "--version" ]; then
    echo "Backend version $APP_VERSION"
else
    echo "Starting Backend version $APP_VERSION"
    exec uvicorn app.main:app --host 0.0.0.0 --port 8000
fi