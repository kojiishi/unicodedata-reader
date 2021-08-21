#!/bin/bash
set -e

yapf -ir -vv .
tox -p
pytype unicodedata_reader
