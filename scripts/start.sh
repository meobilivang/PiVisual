#!/bin/bash
set -e

if [ -f .venv/bin/activate ]; then
    echo "Starting virtual env..."
    source ../.venv/bin/activate
fi

# runs gunicorn
exec "$@"
