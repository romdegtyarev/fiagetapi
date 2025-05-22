#!/bin/bash

# Пример: ./run.sh --year 2024 --gp Monaco --type R --summary

docker compose run --rm fastf1-bot python bot/cli.py "$@"