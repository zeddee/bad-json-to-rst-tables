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
- allow inserting images using base64 uri? e.g. ``.. |image2| image:: data:image/png;base64,iVBORw0KGgoAAAANSUhEU<lots more>``

"""
import argparse
import json
import os
from pathlib import Path
from enum import Enum
from typing import Tuple, List

FILENAME = os.path.join(
    os.path.abspath(os.path.curdir),
    'tests/sample.json'
    )

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


def cli() -> Tuple[List[str], str]:
    """
    CLI helper.

    Returns:
        Tuple[List[str],str]:
            (List[str]): A list of filenames to process.
            (str): Directory to write rST files to.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        dest="infiles",
        required=True,
        help="Input JSON file, or a directory containing JSON files.")
    parser.add_argument(
        "--output",
        dest="outdir",
        default=".",
        help="Output directory. Defaults to current directory.")

    args = parser.parse_args()

    infile_list = smart_filepaths(args.infiles)
    outputdir = Path(args.outdir).absolute()

    return (infile_list, outputdir)

def smart_filepaths(filepath: str) -> List[str]:
    """
    Parses a filepath.
    - If it's a directory, return a list of filenames
    - If it's a single file, return list(filename)
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
        if not is_json(thispath):
            print(f"{thispath} is not a JSON file.")
            exit(1)
        return list(thispath)

if __name__ == "__main__":
    infile_list, outputdir = cli()

    for thisfile in infile_list:
        with open(thisfile) as f:
            output = render_table(f.read())
            
            write_file(
                Path.joinpath(
                    outputdir,
                    Path(thisfile).stem + ".rst"),
                    output
                    )

