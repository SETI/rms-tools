#!/usr/bin/python
################################################################################
# pdstable.py
#
# Classes and methods to deal with PDS index and table files
#
# Mark R. Showalter, SETI Institute, December 2011
# Revised December 22, 2011 (BSW) - add ability to read, parse, and return data
#                                   that take multiple columns
# Revised December 23, 2011 (BSW) - add adaptation to seconds for TIME fields
# Revised January 3, 2012 (BSW) - changed conversion to floats to happen in one
#                                 step for entire column of TIMEs
#                               - fixed parsing of vectors that were not getting
#                                 all 3 values
#                               - implemented unit tests
#
# Revised 1/11/12 (MRS) - Added PdsTable methods dicts_by_row() and
#                         dicts_by_key(). The former is used by
#                         instrument.cassini.iss.
# Revised 1/17/12 (BSW) - Fixed ordering of values when PdsTable __init__ has
#                         more than one column indicated in the time_format_list
# 6/14/12 MRS - Added column selections in PdsTable() to reduce memory usage;
#   added a callback option to PdsTable() for repairing the values in a table
#   prior to other processing.
################################################################################

import numpy as np
import os
import pdsparser
import julian
import datetime as dt
import unittest

class PdsColumnInfo(object):
    """The PdsColumnInfo class holds the attributes of one column in a PDS
    label."""

    def __init__(self, node, column_no):
        """Constructor for a PdsColumn.

        Input:
            node        the pdsparser.PdsNode object defining the column.
            column_no   the index number of this column, starting at zero.
        """

        dict = node.as_python_value()
        self.name = dict["NAME"]
        self.colno = column_no

        data_type = dict["DATA_TYPE"]
        start_byte = dict["START_BYTE"]
        bytes = dict["BYTES"]

        # Handle the optional case of multiple items per column
        self.items = 1
        item_bytes = bytes
        item_offset = bytes

        try:
            self.items = dict["ITEMS"]
            item_bytes = dict["ITEM_BYTES"]

            item_offset = item_bytes        # Filled in in case next line fails
            item_offset = dict["ITEM_OFFSET"]
        except KeyError: pass

        # Define dtype0 to isolate each column in a record
        # The empty string is needed here even though it seems pointless
        self.dtype0 = ("S" + str(bytes), start_byte - 1)

        # Define dtype1 as a list of dtypes needed to isolate each item
        if self.items == 1:
            self.dtype1 = None
        else:
            self.dtype1 = {}
            byte0 = -item_offset
            for i in range(self.items):
                byte0 += item_offset
                self.dtype1["item_" + str(i)] = ("S" + str(item_bytes), byte0)

        # Define dtype2 to interpret the field based on its PDS data type
        if "INTEGER" in data_type:
            self.dtype2 = "int"
        elif "REAL" in data_type:
            self.dtype2 = "float"
        elif "TIME" in data_type or "DATE" in data_type or "CHAR" in data_type:
            self.dtype2 = None
        else:
            raise IOError("unsupported data type: " + data_type)

class PdsTableInfo(object):
    """The PdsTableInfo class holds the attributes of a PDS-labeled table."""

    def __init__(self, label_file_path, label_list=None):
        """Loads a PDS table based on its associated label file.

        Input:
            label_file      either a string containing the full path to a PDS
                            label file, or a list containing the all the records
                            of a PDS label.
        """

        # Parse the label
        if label_list is None:
            self.label = pdsparser.PdsLabel.from_file(label_file_path)
        else:
            self.label = pdsparser.PdsLabel.from_string(label_list)

        # Get the basic file info...
        assert self.label["RECORD_TYPE"].value == "FIXED_LENGTH"

        # Find the pointer to the table file
        # Confirm that the value is a PdsSimplePointer
        self.table_file_name = None
        for node in self.label:
            if node.name[0] == "^":
                pointer_name = node.name[1:]
                assert isinstance(node.pdsvalue, pdsparser.PdsSimplePointer)
                self.table_file_name = node.pdsvalue.value

        if self.table_file_name is None:
            raise IOerror("Pointer to a data file was not found in PDS label")

        # Locate the root of the table object
        table_node = self.label[pointer_name]

        # Save key info about the table
        assert table_node["INTERCHANGE_FORMAT"].value == "ASCII"

        self.rows = table_node["ROWS"].value
        self.columns = table_node["COLUMNS"].value
        self.row_bytes = table_node["ROW_BYTES"].value

        # Save the key info about each column in a list and a dictionary
        self.column_info_list = []
        self.column_info_dict = {}
        self.dtype0 = {}            # Also construct the dtype0 dictionary

        counter = 0
        for node in table_node:
            if node.pdsvalue.value == "COLUMN":
                pdscol = PdsColumnInfo(node, counter)
                counter += 1

                self.column_info_list.append(pdscol)
                self.column_info_dict[pdscol.name] = pdscol

                self.dtype0[pdscol.name] = pdscol.dtype0

        # Fill in the complete table file name
        self.table_file_path = os.path.join(os.path.dirname(label_file_path),
                                            self.table_file_name)

class PdsTable(object):
    """The PdsTable class holds the contents of a PDS-labeled table. It is
    represented by a list of Numpy arrays, one for each column.

    Current limitations:
        (1) ASCII tables only, no binary formats.
        (2) Detached PDS labels only.
        (3) Only one data file per label.
        (4) No row or record offsets in the label's pointer to the table file.
        (5) STRUCTURE fields in the label are not supported.
        (6) Columns containing multiple items are not loaded. MUST BE FIXED.
        (7) Time fields are represented as character strings at this stage.
    """

    def __init__(self, label_file, times=[], columns=[], nostrip=[],
                       callbacks={}):
        """Constructor for a PdsTable object.

        Input:
            label_file      the path to the PDS label of the table file, or else
                            the contents of the label as a list of strings.
            columns         an optional list of the names of the columns to
                            return. If the list is empty, then every column is
                            returned.
            times           an optional list of the names of time columns to be
                            stored as floats in units of seconds TAI rather than
                            as strings.
            nostrip         an optional list of the names of string columns that
                            are not to be stripped of surrounding whitespace.
            callbacks       an optional dictionary that returns a callback
                            function given the name of a column. If a callback
                            is provided for any column, then the function is
                            called on the string value of that column before it
                            is parsed. This can be used to update known syntax
                            errors in a particular table.
        """

        # Parse the label
        self.info = PdsTableInfo(label_file)

        # Select the columns
        if len(columns) == 0:
            keys = [info.name for info in self.info.column_info_list]
        else:
            keys = columns

        # Load the table data
        file = open(self.info.table_file_path, "r")
        lines = file.readlines()
        file.close()

        table = np.array(lines, dtype=self.info.dtype0)

        # Extract the substring arrays and save in a dictionary and list...
        self.column_list = []
        self.column_dict = {}

        for key in keys:
            column_info = self.info.column_info_dict[key]
            column = table[key]

            # For multiple items...
            if column_info.items > 1:

                # Replace the column substring with a list of sub-substrings
                column.dtype = np.dtype(column_info.dtype1)

                items = []
                for i in range(column_info.items):
                    item = column["item_" + str(i)]
                    items.append(item)

                # Apply the callback function if necessary for each tem
                if key in callbacks.keys():
                    old_items = items
                    items = []
                    callback = callbacks[key]
                    for item in old_items:
                      rows = []
                      for row in item:
                        rows.append(callback(str(row)))
                      rows = np.array(rows)
                      items.append(np.array(rows))

                # Strip strings...
                if column_info.dtype2 is None and key not in nostrip:
                    old_items = items
                    items = []
                    for item in old_items:
                      rows = []
                      for row in item:
                        rows.append(str(row).strip())
                      rows = np.array(rows)
                    items.append(np.array(rows))

                # ...or convert other data types
                else:
                    old_items = items
                    items = []
                    for item in old_items:
                        items.append(item.astype(column_info.dtype2))

                column = np.array(items).swapaxes(0,1)

            # Apply the callback function if necessary
            else:
                if key in callbacks.keys():
                    callback = callbacks[key]
                    rows = []
                    for row in column:
                        rows.append(callback(str(row)))
                    column = np.array(rows)

                # Strip strings...
                if column_info.dtype2 is None and key not in nostrip:
                    rows = []
                    for row in column:
                        rows.append(str(row).strip())
                    column = np.array(rows)

                # ...or convert other data types
                else:
                    try:
                        column = column.astype(column_info.dtype2)
                    except ValueError:
                        column.fill(1.)

                # Convert time columns if necessary
                if key in times:
                    column = julian.tai_from_iso(column)

            self.column_list.append(column)
            self.column_dict[key] = column

# To test...
#   test = pdstable.PdsTable("./test_data/cassini/ISS/index.lbl")
#   test.column_dict["FILE_SPECIFICATION_NAME"]
# or
#   test.column_dict["EXPOSURE_DURATION"]
#
# Right now it ignores columns with multiple "ITEMS". We need to fix that
# because some of those columns contain useful information we will need later.
# Please modify the code so that it can handle the case of multiple items,
# using a Numpy 2-D array instead of a 1-D array to hold the values in the
# column.

    def dicts_by_row(self):
        """Returns a list of dictionaries, one for each row in the table, and
        with each dictionaory containing all of the column values in that
        particular row."""

        # For each row...
        dicts = []
        for row in range(self.info.rows):

            # Create and append the dictionary
            dict = {}
            for key in self.column_dict.keys():
                dict[key] = self.column_dict[key][row]

            dicts.append(dict)

        return dicts

########################################
# UNIT TESTS
########################################

ERROR_TOLERANCE = 1.e-15

class Test_PdsTable(unittest.TestCase):
    
    def test_table_parse(self):
        
        # Testing different values parsed correctly...
        test_table_basic = PdsTable("./test_data/cassini/ISS/index.lbl")
        #test strings
        test_file_names = test_table_basic.column_dict['FILE_NAME']
        file_name_test_set = np.array(['N1573186009_1.IMG',
                                       'W1573186009_1.IMG',
                                       'N1573186041_1.IMG',
                                       'W1573186041_1.IMG'])
        self.assertTrue(np.all(file_name_test_set == test_file_names[0:4]))

        #test floats
        test_cbody_dists = test_table_basic.column_dict['CENTRAL_BODY_DISTANCE']
        cent_body_dist_test_set = np.array([2869736.9, 2869736, 2869707,
                                            2869706.9])
        self.assertTrue(np.all(cent_body_dist_test_set == test_cbody_dists[0:4]))

        #test vectors
        test_sc_vels = test_table_basic.column_dict['SC_TARGET_VELOCITY_VECTOR']
        sc_vels_test_set = np.array([[1.2223705, -1.1418157, -0.055303727],
                                     [1.2223749, -1.1418146, -0.055303917],
                                     [1.2225166, -1.1417793, -0.055309978],
                                     [1.2225173, -1.1417791, -0.055310007]])
        self.assertTrue(np.all(sc_vels_test_set == test_sc_vels[0:4]))

        #test times as strings
        test_start_time_strs = test_table_basic.column_dict['START_TIME']
        start_time_str_test_set = np.array(['2007-312T03:31:12.392',
                                            '2007-312T03:31:14.372',
                                            '2007-312T03:31:45.832',
                                            '2007-312T03:31:46.132'])
        self.assertTrue(np.all(start_time_str_test_set ==
                               test_start_time_strs[0:4]))

        test_table_secs = PdsTable("./test_data/cassini/ISS/index.lbl",
                                   ['START_TIME'])
        #test times as seconds (floats)
        test_start_times = test_table_secs.column_dict['START_TIME']
        start_time_test_set = np.array([247807905.392, 247807907.372,
                                        247807938.832, 247807939.132])
        self.assertTrue(np.all(start_time_test_set == test_start_times[0:4]))

        # Test dicts_by_row()
        rowdict = test_table_secs.dicts_by_row()
        for i in range(4):
            self.assertEqual(rowdict[i]["START_TIME"], start_time_test_set[i])

if __name__ == '__main__':
    unittest.main()

################################################################################
# End of file
################################################################################
