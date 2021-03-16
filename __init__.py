#!/usr/bin/env python3

"""
Bad JSON rST tables parses a JSON files
and spits out rST ``list-table`` s inelegantly.

TODO:

- Allow writing longform content to a single cell
  by implementing a ipynb-like dict format.

  E.g. parse the following:

  ..  code-block::

      "Assessment" : {
          "h1" : "Heading 1",
          "h2" : "Heading 2",
          "ul-item" : "this is an unordered list item",
          "ol-item" : "this is an ordered list item",
          "p" : "this is a paragraph",
          "code" : "print(\"this is a block of code (single-line)\")",
          "code-block-item": "print(\"this is a single line in a code block\")",
          "image" : "/img/sample.jpg"
      }
- Set filename write to from command line args.
- By default, write to files named after the ``ID`` key in JSON. This is to capture the SA name as the filename.
- Write proper example.json file.
- Write tests
- Take list of files or a dir from command line args.

"""

import json
import os
from enum import Enum

FILENAME = os.path.join(os.path.abspath(os.path.curdir), 'data.json')

class Nodes(Enum):
    """Enum type for rst nodes"""
    TABLE_INIT = '..  list-table::' #: Start of rst list-table node.
    ATTR_HEADERROWS = '    :header-rows: 1' #: Node for the list-table attribute ``:header-rows: 1``. Always set to ``1``.
    ATTR_STUBCOLS   = '    :stub-columns: 1' #: Node for the list-table attribute ``:stub-columns: 1``. Always set to ``1``.
    STUB_ITEM  = '    - * ' #: Node for first item in a table row.
    ITEM        = '      * ' #: Node for item in a table row.
    LEFTPAD     = '        '
    """Pads 6 \s characters. Used to pad content in tables so that
they match the indentation of their parent table nodes.
Works only if the root table is at col 0
(told ya this is an inelegant repo)."""

def render_table(json_data: str) -> str:
    """
    The Table constructor creates
    an rST table as an object

    Args:
        json_data (str): Expects a JSON string.
    """

    table_head = f"{Nodes.TABLE_INIT.value}\n" \
        f"{Nodes.ATTR_HEADERROWS.value}\n" \
        f"{Nodes.ATTR_STUBCOLS.value}\n" \
        "\n"

    output = table_head

    data = json.loads(json_data)

    if isinstance(data, list):
        pass

    if isinstance(data, dict):
        keys = data.keys()


    for k in keys:
        title = "{}{}\n".format(Nodes.STUB_ITEM.value,k)
        val = handle_newlines(data.get(k))

        item = f"{Nodes.ITEM.value}{val}\n\n"
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
            output = output + Nodes.LEFTPAD.value + line + "\n"

    return output

def write_file(filepath: str, data: str) -> None:
    with open(filepath,"w") as f:
        f.write(data)

if __name__ == "__main__":
    with open(FILENAME) as f:
        output = render_table(f.read())
        
        write_file(os.path.join(os.path.abspath(os.path.curdir),"EIQ-2021-1234.rst"), output)

