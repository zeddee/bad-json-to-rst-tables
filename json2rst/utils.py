import json
from typing import List, Dict, Tuple

import nodes

def handle_rich_content(srcfile: str, rich_content: List[Dict[str, str]]) -> str:
    """
    Args:
        rich_content (List[Dict[str, str]]): Expects a string like "[{"key":"value"}]
        srcfile (str): Name of file where the data comes from, for naming an offending file when data validation fails.
    """
    if not isinstance(rich_content, list):
        # TODO: handle exception
        exit(1)

    output = ""

    for i in range(len(rich_content)):
        first = (i == 0) # type: bool
        line = rich_content[i]
        assert(isinstance(line, dict))

        keys = line.keys()

        for key in keys: #: We expect only one key, but still need to iterate over iterator?
            assert(isinstance(key, str))
            output = output + nodes.RichNode(
                srcfile,
                key,
                line.get(key),
                first
                ).parse()

    return output


def render_table(srcfile: str, json_data: str) -> str:
    """
    The Table constructor creates
    an rST table as an object

    Args:
        srcfile (str): Filename is passed in here so if anything fails due to invalid content, we can construct an error message pointing to the offending file.
        json_data (str): Expects a JSON string.
    """

    table_head = f"{nodes.Nodes.TABLE_INIT.value}\n" \
        f"{nodes.Nodes.ATTR_STUBCOLS.value}\n" \
        "\n"

    output = table_head

    data = json.loads(json_data)

    if isinstance(data, list):
        # TODO: to handle JSON strings wrapped in a list. e.g. ``[{"key": "value"}]``
        pass

    if isinstance(data, dict):
        keys = data.keys()


    for k in keys:
        title = "{}{}\n".format(nodes.Nodes.STUB_ITEM.value,k)
        val = data.get(k)

        if isinstance(val, list):
            parsed_val = handle_rich_content(srcfile, val)
        else:
            parsed_val = handle_newlines(val)

        item = f"{nodes.Nodes.ITEM.value}{parsed_val}\n\n"
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
            output = output + nodes.Nodes.LEFTPAD.value + line + "\n"

    return output
