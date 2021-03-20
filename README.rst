Bad JSON to rST tables converter
***********************************

Inelegantly converts JSON files to tables in rST files.

To run:

- Clone the repository: ``git clone https://github.com/zeddee/bad-json-to-rst-tables``
- Navigate to the cloned dir: ``cd bad-json-to-rst-tables``
- Run the Python package (because I am bad at packaging): ``python3 json2rst --input <inputdir> --output <outputdir>``

..  contents::
    :local:

Usage
========

..  code-block::

    usage: json2rst.py [-h] --input INFILES [--output OUTDIR] --headers
                   PIVOT_HEADERS [--strict] [--sort-by SORT_BY]
                   [--sort-order SORT_ORDER] [--csv-out CSV_OUT]
                   [pivot]

    optional arguments:
      -h, --help            show this help message and exit

    General options:
      --input INFILES       Input JSON file, or a directory containing JSON files.
      --output OUTDIR       Output directory. Defaults to current directory.

    Pivot a directory of JSON files:
      pivot                 Specify 'pivot' to pivot JSON files. Collects JSON
                            files from --input,and extract values from fields that
                            match names in --header, and write to a csv-table.
      --headers PIVOT_HEADERS
                            Required for pivot. Add a list of header names as
                            comma-separated values. JSON files from --input will
                            be pivoted against this list. Headers MUST BE UNIQUE
                            (RFC8259 §4). Duplicate headers are discarded.
                            
                            E.g.: --headers='key1,key2,key3'
      --strict              Strict mode for pivot. When set, JSON files must have
                            all fields specified with --headers.
      --sort-by SORT_BY     Sort the pivot table by a given key. Specify only one
                            key.
      --sort-order SORT_ORDER
                            Sort --sort-by in 'ascending' or 'descending' order.
      --csv-out CSV_OUT     Name of output CSV file saved in --output dir.


Page titles
=============

Page titles are crudely implemented for now.

A page title using the filename of the JSON file is
added to the top of each rST file.

For example, running ``python json2rst --input sample.json --output _output``
creates the file ``_output/sample.rst`` which has the following first few lines:

..  code-block:: text

    sample
    ********

    ..  list-table::

        //...

Rich content
=============

You can add rich content to a JSON field as a list of
dicts(key-value pairs):

..  code-block::

    {
      "this rich content field": [
              {"h1" : "Heading 1"},
              {"h2" : "Heading 2"},
              {"ul" : "this is an unordered list item"},
              {"ol" : "this is an ordered list item"},
              {"p" : "this is a paragraph"},
              {"code" : "print(\"this is a block of code (single-line)\")"},
              {"code-block": "print(\"this is a single line in a code block\")"},
              {"image" : "/img/sample.jpg"}
        ]
    }

Expected input
===============

..   code-block:: javascript

    {
        "ID": "this is a title",
        "CVE": "-",
        "Description": "This is a description",
        "Assessment": [
          {"heading": "This is a heading."},
          {"p": "This is a multi\nline field that can contain things like `links <#link>`_\nand code ``snippets``"},
          {"ul": "this is an unordered list item"},
          {"heading": "This is a heading."},
          {"ul": "this is an unordered list item"},
          {"ul": "this is an unordered list item"}
        ]
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
          * **This is a heading.**

            This is a multi
            line field that can contain things like `links <#link>`_
            and code ``snippets``


            - this is an unordered list item

            **This is a heading.**

            - this is an unordered list item

            - this is an unordered list item

Pivots
========

If you run ``python json2rst.py pivot ...``, you can pivot a
list of JSON files against field names specified with
``--headers "key1,key2,key3"`` and write it to a csv file
(default: ``./pivot.csv``).

- DOES NOT SUPPORT `Rich content`_. CSV files are simple creatures and we should let them be.
- You can sort the CSV list by specifying ``--sort-by "key_name"``.
- Sort by (``--sort-by``) ``descending`` or ``ascending`` order (default: ``ascending``).
- Apply ``--strict`` mode so the pivot fails if at least one JSON file
  does not contain all the keys specified in ``--headers``.

For example, running:

..  code-block::

    python json2rst.py \
      pivot \
      --input tests/samples \
      --headers="ID,Description" \
      --csv-out "test.csv" \
      --sort-by "ID" \
      --sort-order "descending"

Writes a pivot table named ``test.csv`` that looks like this:

..  code-block::

    ID,Description
    EIQ-2021-1235,This is a description
    EIQ-2021-1234,This is a description

You can embed it in an rST file like this:

..  code-block::

    .. csv-table::
       :header-rows: 1
       :file: ./test.csv
