#!/usr/bin/env python3
import unicodedata

from unicodedata_reader import *


def dump_east_asian_width():
    reader = UnicodeDataReader.default
    blocks = reader.blocks().to_dict()
    bidi_brackets = reader.bidi_brackets().to_dict()
    scripts = reader.scripts().to_dict()
    script_extensions = reader.script_extensions().to_dict()
    gc = UnicodeDataReader.default.general_category()

    def bidi_brackets_type(code):
        bracket = bidi_brackets.get(code)
        return bracket.type if bracket else ""

    columns = {
        "Block": lambda code, ch: str(blocks.get(code)),
        "Code": lambda code, ch: "U+" + u_hex(code),
        "Char": lambda code, ch: chr(code),
        "GC": lambda code, ch: gc.value(code),
        "Bidi_Paired_Bracket_Type": lambda code, ch: bidi_brackets_type(code),
        "EAW": lambda code, ch: unicodedata.east_asian_width(ch),
        "Script": lambda code, ch: scripts.get(code),
        "ScriptExt":
        lambda code, ch: " ".join(script_extensions.get(code, [])),
    }
    sep = "\t"
    print(f"# {sep.join(columns.keys())},Name")
    for code in blocks.keys():
        ch = chr(code)
        eaw = unicodedata.east_asian_width(ch)
        if eaw is None or not (eaw == "F" or eaw == "W" or eaw == "H"):
            continue
        script = scripts.get(code)
        if script != "Common":
            continue
        values = (func(code, ch) for func in columns.values())
        output = sep.join(values)
        try:
            output += f"{sep}{unicodedata.name(chr(code))}"
        except:  # noqa: E722
            pass
        print(output)


if __name__ == "__main__":
    dump_east_asian_width()
