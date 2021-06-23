import pathlib
import sys

tests_dir = pathlib.Path(__file__).parent
root_dir = tests_dir.parent
sys.path.append(str(root_dir / 'unicodedata_parser'))
