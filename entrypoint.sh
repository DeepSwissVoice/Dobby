#!/usr/bin/env bash
set -e

if [ ! -e "/dobby/config.yml" ]; then
   echo "Creating config"
   cp /dobby/_config.yml /dobby/config.yml
fi