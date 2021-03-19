"""
JSON Pivot takes a bunch of JSON files with the same fields
and:

#.  Creates a pivoted table that has the field names as
    headings
#.  Lists selected contents of all JSON files in that table.

For example, running jsonpivot on a series of JSON files
with the following fields:

..  code-block:: javascript

    {
        "ID": "this is an ID",
        "Description": this is a description",
        "Other attribute": "this is a dummy field",
    }

will create an rst file containing the following table:

+----+-------------+-----------------+
| ID | Description | Other attribute |
+----+-------------+-----------------+
| .. | ...         | ...             |.
+----+-------------+-----------------+
| .. | ...         | ...             |
+----+-------------+-----------------+

"""
import sys, os
from typing import List, Dict

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

class Pivot:
    def __init__(self,
                 json_objects: List(Dict[str, str]),
                 header_list: List[str],
                 ) -> None:
        """
        Pivot object.

        Args:
            json_objects (List[Dict[str,str]]): Takes a list
                of JSON objects and pivots.
        """
        assert(isinstance(json_objects, list)), \
            "Pivot only takes a list of JSON objects: {}"
        for obj in json_objects:
            assert(isinstance(obj, dict)), \
                "{} must be a dictionary.".format(obj)

        self.json_objects = json_objects
        self.header_list = header_list

    def pivot(self) -> str:
        """
        Returns:
            Returns the pivoted data in a CSV-formatted string
        """

        return ""

    def _check_pivot_keys(self) -> bool:
        """
        Checks if all important keys are
        available in JSON objects to pivot.

        """

        for obj in self.json_objects:
            for item in self.header_list:
                assert(item in list(obj.keys())), \
                    "All dictionaries used in Pivot must have {} key".format(item)

        return True
