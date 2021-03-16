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
- ✅ Set filename write to from command line args.
- By default, write to files named after the ``ID`` key in JSON. This is to capture the SA name as the filename.
- ✅ Write proper example.json file.
- Write example.json file for rich content
- Write tests
- ✅ Take list of files or a dir from command line args.
- allow inserting images using base64 uri? e.g. ``.. |image2| image:: data:image/png;base64,iVBORw0KGgoAAAANSUhEU<lots more>``

"""
import argparse
import json
import os
from pathlib import Path
from enum import Enum
from typing import Tuple, List, Dict

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
    UL_ITEM = '- '
    OL_ITEM = '#.  '
    # CODE #: Omit. Because we need to surround the content of
    # <code> nodes with double backticks, as opposed to prefixing
    # the node (like with the other Nodes here)
    CODE_BLOCK_INIT = '..  code-block::'
    CODE_BLOCK_PAD = '    '
    IMAGE = '..  image:: '

class RichNode:
    RICH_NODE_TYPES = [
        "h1",
        "h2",
        "h3",
        "p",
        "ul-item",
        "ol-item",
        "code",
        "code-block-item",
        "image",
    ]

    def __init__(self, node_type: str, content: str) -> None:
        self.content = handle_newlines(content)
        self.n = node_type
        
        self._is_rich_node()

    def parse(self) -> str:
        return f"{self._handle_node()}\n\n"

    def _is_rich_node(self) -> bool:
        if self.n not in self.RICH_NODE_TYPES:
            print(f"Invalid node type: {node_type}: {content}.\n" \
                  "JSON key should be one of {self.RICH_NODE_TYPES}")
            exit(1) # TODO: exception handling.
            # return False

        return True

    def _handle_node(self) -> str:
        """
        Would *really* love to have Python 3.10 pattern matching
        syntax here right now :(

        Args:
            n (str): Node type. Must be one of self.RICH_NODE_TYPES.
        Returns:
            An rST-formatted string ready to plug into our output file.
        """


        if self.n == "h1":
            H1_rst = "*" * (len(self.content) + 2) # Make sure that heading marker is slightly longer than len(self.content)
            return f"{self.content}\n{H1_rst}"

        elif self.n == "h2":
            H2_rst = "=" * (len(self.content) + 2) # Make sure that heading marker is slightly longer than len(self.content)
            return f"{self.content}\n{H2_rst}"

        elif self.n == "h2":
            H3_rst = "-" * (len(self.content) + 2) # Make sure that heading marker is slightly longer than len(self.content)
            return f"{self.content}\n{H3_rst}"

        elif self.n == "p":
            return self.content

        elif self.n == "ul-item":
            return f"{Nodes.UL_ITEM.value}{self.content}"

        elif self.n == "ol-item":
            return f"{Nodes.OL_ITEM.value}{self.content}"

        elif self.n == "code":
            return f"``{self.content}``"

        elif self.n == "code-block-item":
            # this needs more complex handling. Need to know if there are multiple code-block-items in sequence.
            pass

        elif self.n == "image":
            # might need to embed as base64 image.
            return f"{Nodes.IMAGE.value}{content}"

    def _code_block_start() -> str:
        return f"{Nodes.CODE_BLOCK_INIT.value}\n\n"

    def _code_block_body() -> str:
        return f"{Nodes.CODE_BLOCK_PAD.value}{self.content}"


def handle_rich_content(rich_content: Dict[str, str]) -> str:
    """
    Args:
        rich_content (Dict[str, str]): A dictionary of rich content nodes.
    """
    if not isinstance(rich_content, dict):
        # TODO: handle exception
        exit(1)

    keys = rich_content.keys()
    output = ""

    for key in keys:
        output = output + RichNode(key, rich_content.get(key)).parse()

    return output


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
        # TODO: to handle JSON strings wrapped in a list. e.g. ``[{"key": "value"}]``
        pass

    if isinstance(data, dict):
        keys = data.keys()


    for k in keys:
        title = "{}{}\n".format(Nodes.STUB_ITEM.value,k)
        val = data.get(k)

        if isinstance(val, dict):
            parsed_val = handle_rich_content(val)
        else:
            parsed_val = handle_newlines(val)

        item = f"{Nodes.ITEM.value}{parsed_val}\n\n"
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

