import argparse
from pathlib import Path
from typing import Tuple, Set

from . import utils

def _cli() -> any:
    """
    CLI helper.

    Returns:
        a argparse.Namespace object, that looks very much like a NamedTuple
    """

    parser = argparse.ArgumentParser()

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

    cmd_pivot = parser.add_argument_group("Pivot a directory of JSON files.")

    cmd_pivot.add_argument(
        "pivot",
        type=bool,
        nargs="?",
        default=False,
        help="""Specify 'pivot' to pivot JSON files.
Collects JSON files from --input,and
extract values from fields that match names in --header,
and puts them in rST tables.
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

Headers MUST BE UNIQUE (RFC8259 §4). Duplicate headers are discarded.

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

    return parser.parse_args()

def _convert_json_to_rst(infiles: str, outdir: str):
  infile_list = utils.smart_filepaths(infiles)
  outputdir = Path(outdir).absolute()

  for thisfile in infile_list:
      with open(thisfile) as f:
          output = utils.render_page(thisfile, f.read())


          utils.write_file(
              Path.joinpath(
                  outputdir,
                  Path(thisfile).stem + ".rst"),
                  output
                  )

def _pivot(args: any):
  pivot_headers = _parse_headers(args.pivot_headers)
  pass

def _parse_headers(raw_headers: str) -> Set[str]:
  """
  Args:
    raw_headers (str): Value from args.pivot_headers.

  Returns:
    A Set of headers. This automatically discards duplicate headers.
  """
  output = list()

  for header in raw_headers.split(sep=","):
    output.append(header.strip())

  final_headers = set(output)

  print("Pivoting JSON files using headers: {}".format(final_headers))

  return final_headers

def cmd():
  args = _cli()

  print("ARGS\n========\n{}\n========".format(args))

  if not args.pivot:
    _convert_json_to_rst(args.infiles, args.outdir)
  
  else:
    _pivot(args)
    print("YOU HAVE REACHED THE END OF EARLY ACCESS CONTENT.")
