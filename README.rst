Bad JSON to rST tables converter
***********************************

Inelegantly converts JSON files to rST tables.

..  code-block::

    usage: __init__.py [-h] --input INFILES [--output OUTDIR]

    optional arguments:
      -h, --help       show this help message and exit
      --input INFILES  Input JSON file, or a directory containing JSON files.
      --output OUTDIR  Output directory. Defaults to current directory.

Expected input
===============

..  code-block:: javascript

    {
        "ID": "this is a title",
        "CVE": "-",
        "Description": "This is a description",
        "Assessment": "This is a multi\nline field that can contain things like `links <#link>`_\nand code ``snippets``"
    }

Expected output
================

..  code-block:: rst

    ..  list-table::
        :header-rows: 1
        :stub-columns: 1

        - * ID
          * this is a title

        - * CVE
          * -

        - * Description
          * This is a description

        - * Assessment
          * This is a multi
            line field that can contain things like `links <#link>`_
            and code ``snippets``


