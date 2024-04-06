#!/bin/bash
set -e

unicodedata-reader lb -fv -t js/template.js
unicodedata-reader gc -fv -t js/template.js

yapf -ir -vv .
tox -p
pytype unicodedata_reader
