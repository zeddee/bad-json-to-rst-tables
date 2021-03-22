import json
from pathlib import Path
from typing import List, Dict, Tuple

from . import nodes

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
    prev_key = ""
    next_key = ""

    for i in range(len(rich_content)):
        first = (i == 0) # type: bool
        line = rich_content[i]
        assert(isinstance(line, dict))

        keys = line.keys()
        assert(len(keys) == 1) #: Given the data structure, we expect only one key

        key = list(keys)[0] #: We have to cast type of keys from dict_keys to list
        assert(isinstance(key, str))

        if i < len(rich_content)-1:
            next_key = list(rich_content[i+1].keys())[0]

        output = output + nodes.RichNode(
            srcfile,
            key,
            line.get(key),
            first,
            prev_key,
            next_key,
            ).parse()

        prev_key = key


    return output


def render_page(srcfile: str, json_data: str) -> str:
    """
    The Table constructor creates
    an rST table as an object

    Args:
        srcfile (str): Filename is passed in here so if anything fails due to invalid content, we can construct an error message pointing to the offending file.
        json_data (str): Expects a JSON string.
    """

    page_title = "{}\n{}\n\n".format(
        Path(srcfile).stem, #: TODO: Use filename as page title for now. To implement something a bit more sophisticated later.
        "*" * (len(Path(srcfile).stem) + 2), #: Makes sure that rST heading marker is always longer than page title.
    )


    table_head = f"{nodes.Nodes.TABLE_INIT.value}" \
        f"{nodes.Nodes.ATTR_STUBCOLS.value}" \
        "\n"

    output = page_title + table_head

    data = json.loads(json_data)

    if isinstance(data, list):
        # TODO: to handle JSON strings wrapped in a list. e.g. ``[{"key": "value"}]``
        pass

    if isinstance(data, dict):
        keys = data.keys()


    for k in keys:
        title = "{}{}\n".format(nodes.Nodes.STUB_ITEM.value,k)
        val = str(data.get(k)) #: Coerce to str, because we should not need to handle any other data type.

        if isinstance(val, list):
            parsed_val = handle_rich_content(srcfile, val)
        else:
            parsed_val = handle_newlines(val)

        item = f"{nodes.Nodes.ITEM.value}{parsed_val}\n\n"
        output = output + title + item

    return output

def handle_newlines(data: str) -> str:
    assert(isinstance(data, str)), "{} must be str".format(data)
    if ("\n" not in data):
        return data

    output = ""
    strlist = data.split("\n")

    for line in strlist:
        if strlist.index(line) == 0:
            output = line + "\n"
        else:
            output = output + nodes.Nodes.LEFTPAD.value + line + "\n"

    return output

def smart_filepaths(filepath: str) -> List[str]:
    """
    Parses a filepath.
    - If it's a directory, return a list of filenames
    - If it's a single file, return list(filename)

    Args:
        filepath (str): Takes a filepath and:
            - Decides if it's a directory or file.

                - If it's a directory, returns the list of JSON files
                  in the directory as a string.
                - If it's a single file, returns the name of that
                  file in a list.
    """
    def is_json(filename: str) -> bool:
        return Path(filename).suffix == ".json"



    thispath = Path(filepath).absolute()

    if Path(thispath).is_dir():
        filelist = Path(thispath).iterdir()

        out_filelist = list()

        for f in filelist:
            if is_json(f):
                out_filelist.append(f)

        return out_filelist

    if Path(thispath).is_file():
        assert(is_json(thispath)), f"{thispath} is not a JSON file."

        outfile = list()
        outfile.append(Path(thispath))

        return outfile

def write_file(filepath: str, data: str) -> None:
    with open(filepath,"w") as f:
        f.write(data)
