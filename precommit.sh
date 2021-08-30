#!/bin/bash
set -e

unicodedata-reader lb -vt js/template.js

yapf -ir -vv .
tox -p
pytype unicodedata_reader
