#!/bin/bash
if [[ -z "$VIRTUAL_ENV" ]]; then
  echo "Activating the virtual environment and rerunning..."
  uv run "$0" "$@"
  exit $?
fi

set -e

unicodedata-reader lb -fv -t js/template.js
unicodedata-reader gc -fv -t js/template.js

yapf -ir -vv .
tox -p
pytype src/unicodedata_reader
ruff check
