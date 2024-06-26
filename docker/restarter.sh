#!/bin/bash

while true; do
  if [ -f ./restart.txt ]; then
    echo "Restarting containers..."

    rm -f ./restart.txt

    docker compose up -d

    echo "Containers restarted"
  fi
  sleep 5
done