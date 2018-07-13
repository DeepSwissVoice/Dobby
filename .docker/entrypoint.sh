#!/usr/bin/env bash
set -e

if [ ! -e "./config.yml" ]; then
   echo "Creating config"
   cp ./_config.yml ./config.yml
fi

echo "Starting Dobby!"

exec supervisord