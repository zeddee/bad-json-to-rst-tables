Bad JSON to rST tables converter
***********************************

Inelegantly converts JSON files to tables in rST files.

To run:

- Clone the repository: ``git clone https://github.com/zeddee/bad-json-to-rst-tables"
- Navigate to the cloned dir: ``cd bad-json-to-rst-tables``
- Run the Python package (because I am bad at packaging): ``python3 json2rst --input <inputdir> --output <outputdir>``

..  code-block::

    usage: python3 json2rst [-h] --input INFILES [--output OUTDIR]

    optional arguments:
      -h, --help       show this help message and exit
      --input INFILES  Input JSON file, or a directory containing JSON files.
      --output OUTDIR  Output directory. Defaults to current directory.

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

