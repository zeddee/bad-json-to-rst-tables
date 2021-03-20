import argparse
from pathlib import Path
from typing import Tuple, List

from . import utils

def cli() -> Tuple[List[str], str]:
    """
    CLI helper.

    Returns:
        Tuple[List[str],str]:
            (List[str]): A list of filenames to process.
            (str): Directory to write rST files to.
    """

    parser = argparse.ArgumentParser(add_help=True)

    cmd_pivot = parser.add_argument_group("Pivot a directory of JSON files.")

    cmd_pivot.add_argument(
        "pivot",
        type=bool,
        nargs="?",
        default=False,
        help="""Specify 'pivot' to pivot JSON files.
Collects JSON files from a directory and
extract values from fields that have these header names
to put them in rST tables.
"""
     )

    cmd_pivot.add_argument(
        "--headers",
        dest="pivot_headers",
        type=str,
        required=True,
        help="""Required for pivot.
Add a list of header names as comma-separated values.
JSON files from --input will be pivoted against this list.

E.g.: --headers='key1,key2,key3'
"""
    )
    cmd_pivot.add_argument(
        "--strict",
        action="store_true",
        required=False,
        help="""Strict mode for pivot.
        When set, JSON files must have all fields specified with --headers.
        """
    )


    cmd_rst = parser.add_argument_group("General options")
    cmd_rst.add_argument(
        "--input",
        dest="infiles",
        required=True,
        help="Input JSON file, or a directory containing JSON files.")
    cmd_rst.add_argument(
        "--output",
        dest="outdir",
        default=".",
        help="Output directory. Defaults to current directory.")

    return parser.parse_args()

def cmd():
  args = cli()

  print("ARGS\n========\n{}\n========".format(args))

  infile_list = utils.smart_filepaths(args.infiles)
  outputdir = Path(args.outdir).absolute()

  for thisfile in infile_list:
      with open(thisfile) as f:
          output = utils.render_page(thisfile, f.read())


          utils.write_file(
              Path.joinpath(
                  outputdir,
                  Path(thisfile).stem + ".rst"),
                  output
                  )
