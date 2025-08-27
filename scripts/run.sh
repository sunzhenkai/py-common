#!/bin/bash

PY_FILE=$1
if [[ -z "$PY_FILE" ]]; then
  echo "no python file to run"
  exit 1
fi

export PYTHONPATH=.:$PYTHONPATH
poetry run python "$PY_FILE"
