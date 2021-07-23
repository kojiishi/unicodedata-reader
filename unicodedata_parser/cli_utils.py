import argparse
import itertools
import re


def _to_unicodes_from_str(text):
    while text:
        match = re.match(r'([uU]\+?)?([0-9a-fA-F]+),?\s*', text)
        if match:
            prefix = match.group(1)
            hex = match.group(2)
            if prefix or (len(hex) >= 2 and len(hex) <= 5):
                yield int(hex, 16)
                text = text[match.end():]
                continue
        yield ord(text[0])
        text = text[1:]


def to_unicodes(text):
    if isinstance(text, str):
        return _to_unicodes_from_str(text)
    return itertools.chain(*(_to_unicodes_from_str(item) for item in text))


def get_unicodes_from_args(default=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('text', nargs='*' if default else '+')
    args = parser.parse_args()
    if args.text:
        return to_unicodes(args.text)
    return default
