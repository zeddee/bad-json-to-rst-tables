#!/usr/bin/env python3

"""
Bad JSON rST tables parses a JSON files
and spits out rST ``list-table`` s inelegantly.

TODO:

- Allow writing longform content to a single cell
  by implementing a ipynb-like dict format.

  E.g. parse the following:

  ..  WARNING::

      problem here! rich content blocks cannot be a single Dict.
      JSON keys must be unique.
      So a more suitable format might be a List[Tuple[str, str]]

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
import sys
from pathlib import Path
from typing import Tuple, List, Dict

import nodes
import utils

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

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
            output = utils.render_table(f.read())
            
            write_file(
                Path.joinpath(
                    outputdir,
                    Path(thisfile).stem + ".rst"),
                    output
                    )

