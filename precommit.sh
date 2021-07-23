#!/bin/bash
set -e

yapf -ir -vv unicodedata_parser tests
pytest -v
