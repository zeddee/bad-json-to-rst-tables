#!/usr/bin/env python3

"""
Bad JSON rST tables parses a JSON files
and spits out rST ``list-table`` s inelegantly.
"""

import json
import os
from enum import Enum

FILENAME = os.path.join(os.path.abspath(os.path.curdir), 'data.json')

class TableNodes(Enum):
    INIT = '..  list-table::'
    ATTR_HEADERROWS = '    :header-rows: 1'
    ATTR_STUBCOLS   = '    :stub-columns: 1'
    FIRST_ITEM  = '    - * '
    ITEM        = '      * '
    LEFTPAD     = '        '

def render_table(json_data: str) -> str:
    """
    The Table constructor creates
    an rST table as an object

    Args:
        json_data (str): Expects a JSON string.
    """

    table_head = f"{TableNodes.INIT.value}\n" \
        f"{TableNodes.ATTR_HEADERROWS.value}\n" \
        f"{TableNodes.ATTR_STUBCOLS.value}\n" \
        "\n"

    output = table_head

    data = json.loads(json_data)

    if isinstance(data, list):
        pass

    if isinstance(data, dict):
        keys = data.keys()


    for k in keys:
        title = "{}{}\n".format(TableNodes.FIRST_ITEM.value,k)
        val = handle_newlines(data.get(k))

        item = f"{TableNodes.ITEM.value}{val}\n\n"
        output = output + title + item

    return output

def handle_newlines(data: str) -> str:
    if "\n" not in data:
        return data

    output = ""
    strlist = data.split("\n")

    for line in strlist:
        if strlist.index(line) == 0:
            output = line + "\n"
        else:
            output = output + TableNodes.LEFTPAD.value + line + "\n"

    return output

def write_file(filepath: str, data: str) -> None:
    with open(filepath,"w") as f:
        f.write(data)

if __name__ == "__main__":
    with open(FILENAME) as f:
        output = render_table(f.read())
        
        write_file(os.path.join(os.path.abspath(os.path.curdir),"EIQ-2021-1234.rst"), output)

