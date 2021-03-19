#!/usr/bin/env python3

"""
Bad JSON rST tables parses a JSON files
and spits out rST ``list-table`` s inelegantly.

TODO:

- ✅ Allow writing longform content to a single cell
  by implementing a ipynb-like dict format.

  E.g. parse the following:

  ..  code-block::

      "Assessment" : [
          {"h1" : "Heading 1"},
          {"h2" : "Heading 2"},
          {"ul" : "this is an unordered list item"},
          {"ol" : "this is an ordered list item"},
          {"p" : "this is a paragraph"},
          {"code" : "print(\"this is a block of code (single-line)\")"},
          {"code-block": "print(\"this is a single line in a code block\")"},
          {"image" : "/img/sample.jpg"}
      ]

- ✅ HAHAH. FIXME ``sample_rich.rst:16: (SEVERE/4)
  Unexpected section title.``
- ✅ headers are not being properly indented by LEFTPAD
- ✅ implement positional awareness e.g. ``prev`` and
  ``next``, so that we can detect consecutive "ul", "ol",
  and "code-block" nodes
- allow users to select whether to embed images as base64,
  or resolve and keep their paths. This also means we have
  to package the output together with the images.
- ✅ Set filename write to from command line args.
- By default, write to files named after the ``ID`` key in
  JSON. This is to capture the SA name as the filename.
- ✅ Write proper example.json file.
- ✅ Write example.json file for rich content
- Write tests
- ✅ Take list of files or a dir from command line args.
- ✅ allow inserting images using base64 uri? e.g. ``..
  |image2| image::
  data:image/png;base64,iVBORw0KGgoAAAANSUhEU<lots more>``

"""
import argparse
import json
import os
import sys
from pathlib import Path
from typing import Tuple, List, Dict

from . import cli
from . import nodes
from . import utils

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

if __name__ == "__main__":
    infile_list, outputdir = cli.cli()

    for thisfile in infile_list:
        with open(thisfile) as f:
            output = utils.render_page(thisfile, f.read())


            utils.write_file(
                Path.joinpath(
                    outputdir,
                    Path(thisfile).stem + ".rst"),
                    output
                    )

