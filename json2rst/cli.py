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

    infile_list = utils.smart_filepaths(args.infiles)
    outputdir = Path(args.outdir).absolute()

    return (infile_list, outputdir)
