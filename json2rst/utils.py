import json
from typing import List, Dict, Tuple

import nodes

def handle_rich_content(rich_content: List[Dict[str, str]]) -> str:
    """
    Args:
        rich_content (List[Dict[str, str]]): Expects a string like "[{"key":"value"}]
    """
    if not isinstance(rich_content, list):
        # TODO: handle exception
        exit(1)

    output = ""

    for line in rich_content:
        first = (rich_content.index(line) == 0)
        assert(isinstance(line, dict))

        keys = line.keys()

        for key in keys: #: We expect only one key, but still need to iterate over iterator?
            output = output + nodes.RichNode(key, line.get(key), first).parse()

    return output


def render_table(json_data: str) -> str:
    """
    The Table constructor creates
    an rST table as an object

    Args:
        json_data (str): Expects a JSON string.
    """

    table_head = f"{nodes.Nodes.TABLE_INIT.value}\n" \
        f"{nodes.Nodes.ATTR_HEADERROWS.value}\n" \
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
            parsed_val = handle_rich_content(val)
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
