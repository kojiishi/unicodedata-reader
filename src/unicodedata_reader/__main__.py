import pathlib
import sys

import unicodedata_reader.bidi_brackets as bidi_brackets
import unicodedata_reader.east_asian_width as ea
import unicodedata_reader.emoji as emoji
import unicodedata_reader.general_category as gc
import unicodedata_reader.line_break as lb
import unicodedata_reader.vertical_orientation as vo


def main():
    args = sys.argv
    sub_commands = {
        'bidi': lambda: bidi_brackets.dump_bidi_brackets(),
        'ea': lambda: ea.UnicodeEastAsianWidthDataCli().main(),
        'emoji': lambda: emoji.UnicodeEmojiDataCli().main(),
        'gc': lambda: gc.UnicodeGeneralCategoryDataCli().main(),
        'lb': lambda: lb.UnicodeLineBreakDataCli().main(),
        'vo': lambda: vo.UnicodeVerticalOrientationDataCli().main(),
    }
    if len(args) > 1:
        func = sub_commands.get(args[1])
        if func:
            del args[1]
            func()
            return

    name = pathlib.Path(args[0]).name
    sub_commands = '|'.join(sub_commands.keys())
    print(f'usage: {name} {sub_commands} [options...]', file=sys.stderr)


if __name__ == '__main__':
    main()
