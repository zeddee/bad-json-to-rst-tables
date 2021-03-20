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

TODO:

- Handle rich nodes in csv content?

"""
import csv
import json
import operator
import sys, os
from typing import List, Dict

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

class Pivot:
    def __init__(self,
                 file_list: List[str],
                 header_list: List[str],
                 strict: bool,
                 csv_out: str,
                 sort_key: str,
                 sort_order: str) -> None:
        """
        Pivot object.

        Args:
            json_objects (List[Dict[str,str]]): Takes a list
                of JSON objects and pivots.
        """
        json_objects = list()

        for filepath in file_list:
            with open(filepath) as f:
                j = json.load(f)
                json_objects.append(j)

        assert(isinstance(json_objects, list)), \
            "Pivot only takes a list of JSON objects: {}"
        for obj in json_objects:
            assert(isinstance(obj, dict)), \
                "{} must be a dictionary.".format(obj)

        self.json_objects = json_objects
        self.header_list = header_list
        self.strict = strict
        self.csv_out = csv_out
        self.sort_key = sort_key
        self.sort_order = sort_order


    def pivot(self) -> None:
        """
        Returns:
            Returns the pivoted data in a CSV-formatted string
        """
        csvout = self.csv_out if self.csv_out else "pivot.csv"

        self._write_csv(csvout)

        if self.sort_key:
            self._sort_by_keys(csvout)

    def _write_csv(self, filename:str) -> None:
        with open(filename,"w") as csvfile:
            writer = csv.DictWriter(
                    csvfile,
                   fieldnames=self.header_list
                )
            
            writer.writeheader()

            for obj in self.json_objects:
                self._check_pivot_keys()
                writer.writerow(self._get_fields(obj))

    def _get_fields(self, obj: Dict[str, str]) -> Dict[str, str]:
        out = dict()
        for (k, v) in obj.items():
            if k in self.header_list:
                out[k] = v
            elif self.strict:
                raise Exception("{} key not found in {}".format(k, obj))
        return out

    def _check_pivot_keys(self) -> bool:
        """
        Checks if all important keys are
        available in JSON objects to pivot.

        """
        for obj in self.json_objects:
            for item in self.header_list:
                assert(item in list(obj.keys())), \
                    "Dictionaries used in Pivot must have '{}' key".format(item)

        return True

    def _sort_by_keys(self, filename: str) -> None:
        """
        Another crude function.
        Instead of getting the csv data to sort from a buffer,
        we're reading from a file and then writing back to it. 🙃
        """
        sort_types = ["ascending", "descending"]
        assert(self.sort_order in sort_types), "Sort order must be one of {}".format(sort_types)

        rev = True if self.sort_order == "descending" else False

        with open(filename, "r") as csvfile:
            tmp = csv.DictReader(csvfile)
            # sortedlist = sorted(spamreader, key=lambda row:(row['column_1'],row['column_2']), reverse=False)
            sortedlist = sorted(tmp, key=operator.itemgetter(self.sort_key), reverse=rev)


        with open(filename, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=self.header_list)
            writer.writeheader()
            for row in sortedlist:
                writer.writerow(row)
