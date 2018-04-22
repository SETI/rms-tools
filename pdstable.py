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
# 8/20/12 MRS - A warning now is raised when a column of a table contains one or
#   more badly-formatted entries. The column values are left in string format.
# 4/2/19 MRS & RSF - Many revisions:
#   - Compatible with Python 3. Strings returned are now of the standard str
#     type Python 2 (one-byte ASCII) and in Python 3 (4-byte Unicode).
#   - Still quite fast, because all operations that can be handled via array
#     operations are still handled via array operations.
#   - Each returned column now has an associated boolean mask that identifies
#     invalid values.
#   - Values in the PDS3 label that identify the valid range or that identify
#     invalid, missing, etc. values are used to populate each column's mask.
#   - New input options for replacements, invalid values and valid ranges can be
#     specified for each column. These can be used to augment information in the
#     in the PDS3 label.
#   - Invalid values (e.g., -1.e32) can also be defined globally.
#   - Lots of new unit tests.
################################################################################

from __future__ import print_function

import sys
import os
import datetime as dt
import warnings
import numpy as np
import numbers

import pdsparser
import julian

# STR_DTYPE is 'S' for Python 2; 'U' for Python 3
STR_DTYPE = np.array(['x']).dtype.kind
PYTHON2 = (sys.version_info[0] == 2)
PYTHON3 = not PYTHON2

# This is an exhaustive tuple of string-like types
STRING_TYPES = (str, bytes, bytearray, np.str_, np.bytes_, np.unicode_)

# Needed because the default value of strip is False
def tai_from_iso(string):
    return julian.tai_from_iso(string, strip=True)

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

    def __init__(self, label_file, label_contents=None, times=[], columns=[],
                       nostrip=[], callbacks={}, ascii=False, replacements={},
                       invalid={}, valid_ranges={}, table_callback=None):
        """Constructor for a PdsTable object.

        Input:
            label_file      the path to the PDS label of the table file. Must be
                            supplied to get proper relative path resolution.
            label_contents  The contents of the label as a list of strings if
                            we shouldn't read it from the file.
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
            ascii           True to interpret the callbacks as translating
                            ASCII byte strings; False to interpret them as
                            translating the default str type, which is 1-byte
                            ASCII in Python 2 but 4-byte Unicode in Python 3.
                            This parameter is ignored in Python 2.
            replacements    an optional dictionary that returns a replacement
                            dictionary given the name of a column. If a
                            replacement dictionary is provided for any column,
                            then any value in that column (as a string or as its
                            native value) that matches a key in the dictionary
                            is replaced by the value resulting from the
                            dictionary lookup.
            invalid         an optional dictionary keyed by column name. The
                            returned value must be a list or set of values that
                            are to be treated as invalid, missing or unknown.
                            An optional entry keyed by "default" can be a list
                            or set of values that are invalid by default; these
                            are used for any column whose name does not apppear
                            as a key in the dictionary..
            valid_ranges    an optional dictionary keyed by column name. The
                            returned value must be a tuple or list containing
                            the minimum and maximum numeric values in that
                            column.
            table_callback  an optional function to be called after reading
                            the data table contents before processing them. Note
                            that this callback must handle bytestrings in Python
                            3.

        Notes: If both a replacement and a callback are provided for the same
        column, the callback is applied first. The invalid and valid_ranges
        parameters are applied afterward.

        Note that, in Python 3, performance will be slightly faster if
        ascii=True.
        """

        # Parse the label
        if label_contents is not None:
            self.info = PdsTableInfo(label_file, label_list=label_contents,
                                     invalid=invalid, valid_ranges=valid_ranges)
        else:
            self.info = PdsTableInfo(label_file,
                                     invalid=invalid, valid_ranges=valid_ranges)

        # Select the columns
        if len(columns) == 0:
            self.keys = [info.name for info in self.info.column_info_list]
        else:
            self.keys = columns
        # self.keys is an ordered list containing the name of every column to be
        # returned

        # Load the table data in binary
        with open(self.info.table_file_path, "rb") as f:
            lines = f.readlines()

        if table_callback is not None:
            lines = table_callback(lines)

        table = np.array(lines, dtype='S')
        table.dtype = np.dtype(self.info.dtype0)
        # table is now a 1-D array in which the ASCII content of each column
        # can be accessed by name. In Python 3, these are bytes, not strings

        # Extract the substring arrays and save in a dictionary...
        self.column_values = {}
        self.column_masks = {}
        for key in self.keys:
            column_info = self.info.column_info_dict[key]
            column = table[key]
            # column is now a 1-D array containing the ASCII content of this
            # column within each row.

            # For multiple items...
            if column_info.items > 1:

                # Replace the column substring with a list of sub-substrings
                column.dtype = np.dtype(column_info.dtype1)

                items = []
                masks = []
                for i in range(column_info.items):
                    item = column["item_" + str(i)]
                    items.append(item)
                    masks.append(False)
                # items is now a list containing one 1-D array for each item in
                # this column.

                self.column_values[key] = items

            else:
                self.column_values[key] = [column]

        # self.column_values now contains a list with one element for each item in
        # that column. Each element is a 1-D array of ASCII strings, one for
        # each row.

        if STR_DTYPE == 'S': ascii = False

        # Replace each 1-D array of items from ASCII strings to the proper type
        for key in self.keys:
            column_info  = self.info.column_info_dict[key]
            column_items = self.column_values[key]

            data_type = column_info.data_type
            dtype     = column_info.dtype2
            func      = column_info.scalar_func
            callback  = callbacks.get(key, None)
            repdict   = replacements.get(key, {})
            strip     = (key not in nostrip)

            invalid_values = column_info.invalid_values
            valid_range    = column_info.valid_range

            error_count    = 0
            error_example  = None

            # For each item in the column...
            new_column_items = []
            new_column_masks = []
            for items in column_items:
                invalid_mask = np.zeros(len(items), dtype='bool')

                # Apply the callback if any
                if callback:

                    # Convert string to input format for callback
                    if PYTHON3 and not ascii:
                       items = items.astype(STR_DTYPE)

                    # Apply the callback row by row
                    new_items = []
                    for item in items:
                        new_item = callback(item)
                        new_items.append(new_item)

                    items = np.array(new_items)

                # Apply the replacement dictionary if any pairs are strings
                for (before, after) in repdict.items():
                    if not isinstance(before, STRING_TYPES): continue
                    if not isinstance(after,  STRING_TYPES): continue

                    # The file is read as binary, so the replacements have
                    # to be applied as ASCII byte strings

                    if PYTHON3 and isinstance(before, (str, np.str_)):
                        before = before.encode()

                    if PYTHON3 and isinstance(after, (str, np.str_)):
                        after  = after.encode()

                    # Replace values (suppressing FutureWarning)
                    items = items.astype('S')
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        items[items == before] = after

                # Handle the data type...

                # Handle a string
                if data_type == 'string' or (data_type == 'time' and
                                             key not in times):
                    items = items.astype(STR_DTYPE)

                    if strip:
                        items = [i.strip() for i in items]
                        items = np.array(items)

                # If this is an int, float or time...

                # Try to convert array dtype
                else:
                    try:
                        items = items.astype(dtype)

                        # Apply the replacements for pairs of this type
                        for (before, after) in repdict.items():
                            with warnings.catch_warnings():
                                warnings.simplefilter("ignore")
                                items[items == before] = after

                        # Convert times if necessary
                        if key in times:
                            items = tai_from_iso(items)

                    # If something went wrong, array processing won't work.
                    # Convert to list and process row by row
                    except Exception:

                        # Process row by row
                        new_items = []
                        for k in range(len(items)):
                            item = items[k]
                            try:
                                # Translate the item
                                item = func(item)

                                # Apply a possible replacement
                                item = repdict.get(item, item)

                            # If something went wrong...
                            except Exception:
                                invalid_mask[k] = True

                                error_count += 1
                                if not isinstance(item, str):
                                    item = item.decode()

                                if strip:
                                    item = item.strip()

                                if error_example is None:
                                    error_example = item

                            # Apply validity criteria to this row
                            invalid_mask[k] |= (item in invalid_values)
                            if valid_range:
                                invalid_mask[k] |= (item < valid_range[0])
                                invalid_mask[k] |= (item > valid_range[1])

                            new_items.append(item)

                        items = new_items

                # Determine validity mask if not already done
                if type(items) == np.ndarray:
                    for invalid_value in invalid_values:

                        # Hide FutureWarning for comparisons of different types
                        with warnings.catch_warnings():
                            warnings.simplefilter("ignore")
                            invalid_mask |= (items == invalid_value)

                    if valid_range:

                        # Hide FutureWarning for comparisons of different types
                        with warnings.catch_warnings():
                            warnings.simplefilter("ignore")
                            invalid_mask |= (items < valid_range[0])
                            invalid_mask |= (items > valid_range[1])

                new_column_items.append(items)
                new_column_masks.append(invalid_mask)

            # Swap indices for multiple items
            if len(new_column_items) == 1:
                self.column_values[key] = new_column_items[0]
                self.column_masks[key]  = new_column_masks[0]

            else:
                theyre_all_arrays = np.all([type(c) == np.ndarray
                                            for c in new_column_items])

                if theyre_all_arrays:
                    array = np.stack(new_column_items, axis=1)
                    if array.dtype.kind in ('S', 'U'):
                        array = [tuple(x) for x in array]
                    self.column_values[key] = array
                else:
                    self.column_values[key] = list(zip(*new_column_items))

                self.column_masks[key] = np.any(np.stack(new_column_masks),
                                                axis=0)

            # Report errors as warnings
            if error_count:
                if error_count == 1:
                    template = 'Illegally formatted %s value in column %s: %s'
                else:
                    template = (str(error_count) +
                                ' illegally formatted %s values in column ' +
                                '%s; first example is "%s"')

                warnings.warn(template % (column_info.data_type,
                                          column_info.name,
                                          error_example.strip()))

    def dicts_by_row(self):
        """Returns a list of dictionaries, one for each row in the table, and
        with each dictionary containing all of the column values in that
        particular row. The dictionary keys are the column names; append "_mask"
        to the key to get the mask value, which is True if the column value is
        invalid; False otherwise."""

        # For each row...
        rowdicts = []
        for row in range(self.info.rows):

            # Create and append the dictionary
            rowdict = {}
            for (key, items) in self.column_values.items():
                rowdict[key] = items[row]
                rowdict[key + "_mask"] = self.column_masks[key][row]

            rowdicts.append(rowdict)

        return rowdicts

    def get_column(self, name):
        """Return the values in the specified column as a list or 1-D array."""

        return self.column_values[name]

    def get_column_mask(self, name):
        """Return the masks for the specified column as a list or 1-D array."""

        return self.column_masks[name]

    def get_keys(self):
        return list(self.keys)

################################################################################
# Class PdsTableInfo
################################################################################

class PdsTableInfo(object):
    """The PdsTableInfo class holds the attributes of a PDS-labeled table."""

    def __init__(self, label_file_path, label_list=None, invalid={},
                                                         valid_ranges={}):
        """Loads a PDS table based on its associated label file.

        Input:
            label_file_path path to the label file
            label_list      if provided, a list containing all the records of
                            the PDS label; otherwise, the label file is read.
            invalid         an optional dictionary keyed by column name. The
                            returned value must be a list or set of values that
                            are to be treated as invalid, missing or unknown.
            valid_ranges    an optional dictionary keyed by column name. The
                            returned value must be a tuple or list containing
                            the minimum and maximum numeric values in that
                            column.
        """

        # Parse the label
        if label_list is None:
            self.label = pdsparser.PdsLabel.from_file(label_file_path)
        else:
            self.label = pdsparser.PdsLabel.from_string(label_list)

        # Get the basic file info...
        if self.label["RECORD_TYPE"].value != "FIXED_LENGTH":
            raise IOError('PDS table does not contain fixed-length records')

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
        if table_node["INTERCHANGE_FORMAT"].value != "ASCII":
            raise IOError('PDS table is not in ASCII format')

        self.rows = table_node["ROWS"].value
        self.columns = table_node["COLUMNS"].value
        self.row_bytes = table_node["ROW_BYTES"].value

        # Save the key info about each column in a list and a dictionary
        self.column_info_list = []
        self.column_info_dict = {}

        # Construct the dtype0 dictionary
        self.dtype0 = {'crlf': ('|S2', self.row_bytes-2)}

        default_invalid = set(invalid.get("default", []))
        counter = 0
        for node in table_node:
            if node.pdsvalue.value == "COLUMN":
                node_dict = node.as_python_value()
                name = node_dict["NAME"]
                pdscol = PdsColumnInfo(node_dict, counter,
                            invalid = invalid.get(name, default_invalid),
                            valid_range = valid_ranges.get(name, None))
                counter += 1

                self.column_info_list.append(pdscol)
                self.column_info_dict[pdscol.name] = pdscol
                self.dtype0[pdscol.name] = pdscol.dtype0

        # Fill in the complete table file name
        self.table_file_path = os.path.join(os.path.dirname(label_file_path),
                                            self.table_file_name)

################################################################################
# class PdsColumnInfo
################################################################################

class PdsColumnInfo(object):
    """The PdsColumnInfo class holds the attributes of one column in a PDS
    label."""

    def __init__(self, node_dict, column_no, invalid=set(), valid_range=None):
        """Constructor for a PdsColumn.

        Input:
            node_dict   the dictionary associated with the pdsparser.PdsNode
                        object defining the column.
            column_no   the index number of this column, starting at zero.
            invalid     an optional set of discrete values that are to be
                        treated as invalid, missing or unknown.
            valid_range an optional tuple or list identifying the lower and
                        upper limits of the valid range for a numeric column.
        """

        self.name = node_dict["NAME"]
        self.colno = column_no

        self.start_byte = node_dict["START_BYTE"]
        self.bytes      = node_dict["BYTES"]

        self.items = node_dict.get("ITEMS", 1)
        self.item_bytes = node_dict.get("ITEM_BYTES", self.bytes)
        self.item_offset = node_dict.get("ITEM_OFFSET", self.bytes)

        # Define dtype0 to isolate each column in a record
        self.dtype0 = ("S" + str(self.bytes), self.start_byte - 1)

        # Define dtype1 as a list of dtypes needed to isolate each item
        if self.items == 1:
            self.dtype1 = None
        else:
            self.dtype1 = {}
            byte0 = 0
            for i in range(self.items):
                self.dtype1["item_" + str(i)] = ("S" + str(self.item_bytes),
                                                 byte0)
                byte0 += self.item_offset

        # Define dtype2 as the intended dtype of the values in the column
        self.data_type = node_dict["DATA_TYPE"]
        if "INTEGER" in self.data_type:
            self.data_type = "int"
            self.dtype2 = "int"
            self.scalar_func = int
        elif "REAL" in self.data_type:
            self.data_type = "float"
            self.dtype2 = "float"
            self.scalar_func = float
        elif "TIME" in self.data_type or "DATE" in self.data_type:
            self.data_type = "time"
            self.dtype2 = 'S'
            self.scalar_func = tai_from_iso
        elif "CHAR" in self.data_type:
            self.data_type = "string"
            self.dtype2 = STR_DTYPE
            self.scalar_func = None
        else:
            raise IOError("unsupported data type: " + data_type)

        # Identify validity criteria
        self.valid_range = valid_range or node_dict.get("VALID_RANGE", None)

        if isinstance(invalid, (numbers.Real,) + STRING_TYPES):
            invalid = set([invalid])

        self.invalid_values = set(invalid)

        self.invalid_values.add(node_dict.get("INVALID_CONSTANT", None))
        self.invalid_values.add(node_dict.get("MISSING_CONSTANT", None))
        self.invalid_values.add(node_dict.get("UNKNOWN_CONSTANT", None))
        self.invalid_values.add(node_dict.get("NULL_CONSTANT", None))
        self.invalid_values.add(node_dict.get("INVALID", None))
        self.invalid_values.add(node_dict.get("MISSING", None))
        self.invalid_values.add(node_dict.get("UNKNOWN", None))
        self.invalid_values.add(node_dict.get("NULL", None))
        self.invalid_values -= {None}

################################################################################
# UNIT TESTS
################################################################################

import unittest

class Test_PdsTable(unittest.TestCase):

  def runTest(self):

    # Testing different values parsed correctly...
    INDEX_PATH = os.path.join(os.environ["OOPS_TEST_DATA_PATH"],
                              "cassini/ISS/index.lbl")
    EDITED_INDEX_PATH = os.path.join(os.environ["OOPS_TEST_DATA_PATH"],
                              "cassini/ISS/index_edited.lbl")

    test_table_basic = PdsTable(INDEX_PATH)

    # Test strings
    test_file_names = test_table_basic.column_values['FILE_NAME']
    file_name_test_set = np.array(['N1573186009_1.IMG',
                                   'W1573186009_1.IMG',
                                   'N1573186041_1.IMG',
                                   'W1573186041_1.IMG'])
    self.assertTrue(np.all(file_name_test_set == test_file_names[0:4]))

    # Test floats
    test_cbody_dists = test_table_basic.column_values['CENTRAL_BODY_DISTANCE']
    cent_body_dist_test_set = np.array([2869736.9, 2869736, 2869707,
                                        2869706.9])
    self.assertTrue(np.all(cent_body_dist_test_set == test_cbody_dists[0:4]))

    # test vectors
    test_sc_vels = test_table_basic.column_values['SC_TARGET_VELOCITY_VECTOR']
    sc_vels_test_set = np.array([[1.2223705, -1.1418157, -0.055303727],
                                 [1.2223749, -1.1418146, -0.055303917],
                                 [1.2225166, -1.1417793, -0.055309978],
                                 [1.2225173, -1.1417791, -0.055310007]])
    self.assertTrue(np.all(sc_vels_test_set == test_sc_vels[0:4]))

    # Test times as strings
    test_start_time_strs = test_table_basic.column_values['START_TIME']
    start_time_str_test_set = ['2007-312T03:31:12.392',
                               '2007-312T03:31:14.372',
                               '2007-312T03:31:45.832',
                               '2007-312T03:31:46.132']
    self.assertEqual(start_time_str_test_set[0], test_start_time_strs[0])
    self.assertEqual(start_time_str_test_set[1], test_start_time_strs[1])
    self.assertEqual(start_time_str_test_set[2], test_start_time_strs[2])
    self.assertEqual(start_time_str_test_set[3], test_start_time_strs[3])

    self.assertTrue(isinstance(test_start_time_strs, np.ndarray))
    self.assertTrue(isinstance(test_start_time_strs[0], np.str_))

    # Test dicts_by_row()
    rowdict = test_table_basic.dicts_by_row()
    for i in range(4):
        self.assertEqual(rowdict[i]["START_TIME"], test_start_time_strs[i])

    rowvals = test_table_basic.get_column("START_TIME")
    rowmasks = test_table_basic.get_column_mask("START_TIME")
    for i in range(10):
        self.assertEqual(rowdict[i]["START_TIME"], rowvals[i])
        self.assertFalse(rowmasks[i])

    ####################################
    # Test times as seconds (floats)
    ####################################

    test_table_secs = PdsTable(INDEX_PATH, times=['START_TIME'])

    test_start_times = test_table_secs.column_values['START_TIME']
    start_time_test_set = np.array([247807905.392, 247807907.372,
                                    247807938.832, 247807939.132])
    self.assertTrue(np.all(start_time_test_set == test_start_times[0:4]))
    self.assertTrue(isinstance(start_time_test_set, np.ndarray))

    # Test dicts_by_row()
    rowdict = test_table_secs.dicts_by_row()
    for i in range(4):
        self.assertEqual(rowdict[i]["START_TIME"], start_time_test_set[i])

    rowvals = test_table_secs.get_column("START_TIME")
    rowmask = test_table_secs.get_column_mask("START_TIME")
    for i in range(10):
        self.assertEqual(rowdict[i]["START_TIME"], rowvals[i])
        self.assertFalse(rowmask[i])

    ####################################
    # Invalids
    ####################################

    test_table = PdsTable(INDEX_PATH, times=['START_TIME'],
                          invalid={'default': [-1.e32, -2147483648]})

    rowdict = test_table_secs.dicts_by_row()
    for key in test_table.get_keys():
        if key.endswith('_mask'): continue

        rowmasks = test_table_secs.get_column_mask(key)
        self.assertFalse(np.any(rowmasks))
        self.assertTrue(isinstance(rowmasks, np.ndarray))

    results = {
        'BIAS_STRIP_MEAN': 0,
        'COMMAND_SEQUENCE_NUMBER': 0,
        'DARK_STRIP_MEAN': 0,
        'DETECTOR_TEMPERATURE': 0,
        'ELECTRONICS_BIAS': 0,
        'EXPECTED_PACKETS': 0,
        'EXPOSURE_DURATION': 0,
        'FILTER_TEMPERATURE': 0,
        'INSTRUMENT_DATA_RATE': 0,
        'INST_CMPRS_RATIO': 0,
        'MISSING_LINES': 1102,
        'ORDER_NUMBER': 0,
        'PARALLEL_CLOCK_VOLTAGE_INDEX': 0,
        'PREPARE_CYCLE_INDEX': 0,
        'READOUT_CYCLE_INDEX': 0,
        'RECEIVED_PACKETS': 0,
        'SENSOR_HEAD_ELEC_TEMPERATURE': 0,
        'SEQUENCE_NUMBER': 0,
        'SPACECRAFT_CLOCK_CNT_PARTITION': 0,
        'START_TIME': 0,
        'CENTRAL_BODY_DISTANCE': 0,
        'DECLINATION': 0,
        'EMISSION_ANGLE': 1563,
        'INCIDENCE_ANGLE': 1563,
        'LOWER_LEFT_LATITUDE': 3426,
        'LOWER_LEFT_LONGITUDE': 3426,
        'LOWER_RIGHT_LATITUDE': 3279,
        'LOWER_RIGHT_LONGITUDE': 3279,
        'MAXIMUM_RING_RADIUS': 110,
        'MINIMUM_RING_RADIUS': 110,
        'NORTH_AZIMUTH_CLOCK_ANGLE': 1563,
        'PHASE_ANGLE': 236,
        'PIXEL_SCALE': 236,
        'RIGHT_ASCENSION': 0,
        'RING_CENTER_LATITUDE': 3612,
        'RING_CENTER_LONGITUDE': 3612,
        'RING_EMISSION_ANGLE': 3612,
        'RING_INCIDENCE_ANGLE': 3612,
        'SUB_SOLAR_LATITUDE': 236,
        'SUB_SOLAR_LONGITUDE': 236,
        'SUB_SPACECRAFT_LATITUDE': 236,
        'SUB_SPACECRAFT_LONGITUDE': 236,
        'CENTER_LATITUDE': 1563,
        'CENTER_LONGITUDE': 1563,
        'TARGET_DISTANCE': 236,
        'TARGET_EASTERNMOST_LONGITUDE': 1006,
        'TARGET_NORTHERNMOST_LATITUDE': 1006,
        'TARGET_SOUTHERNMOST_LATITUDE': 1006,
        'TARGET_WESTERNMOST_LONGITUDE': 1006,
        'TWIST_ANGLE': 0,
        'UPPER_LEFT_LATITUDE': 3144,
        'UPPER_LEFT_LONGITUDE': 3144,
        'UPPER_RIGHT_LATITUDE': 3102,
        'UPPER_RIGHT_LONGITUDE': 3102,
    }

    rowdict = test_table_secs.dicts_by_row()
    for key in test_table_secs.get_keys():
        if key.endswith('_mask'): continue

        rowvals = test_table.get_column(key)
        if np.shape(rowvals[0]) != (): continue

        rowmask = test_table.get_column_mask(key)
        if rowvals.dtype.kind == 'f':
            countv = np.sum(rowvals == -1.e32)
            countm = np.sum(rowmask)
            self.assertEqual(countv, countm)
            self.assertEqual(countv, results[key])

        elif rowvals.dtype.kind == 'i':
            countv = np.sum(rowvals == -2147483648)
            countm = np.sum(rowmask)
            self.assertEqual(countv, countm)
            self.assertEqual(countv, results[key])

        else:
            self.assertEqual(np.sum(rowmask), 0)

    # 22.5 is a common value in column BIAS_STRIP_MEAN
    test_table = PdsTable(INDEX_PATH, times=['START_TIME'],
                          invalid={'default': [-1.e32, -2147483648, 22.5]})

    key = 'BIAS_STRIP_MEAN'
    rowmask = test_table.get_column_mask(key)
    self.assertEqual(np.sum(rowmask), 511)

    test_table = PdsTable(INDEX_PATH, times=['START_TIME'],
                          invalid={'default': [-1.e32, -2147483648], key: 22.5})

    rowmask = test_table.get_column_mask(key)
    self.assertEqual(np.sum(rowmask), 511)

    ####################################
    # Replacements
    ####################################

    # Replacement as a number
    key = 'BIAS_STRIP_MEAN'
    test_table = PdsTable(INDEX_PATH, times=['START_TIME'],
                          invalid={'default': [-1.e32, -2147483648]},
                          replacements={key: {22.5: -1.e32}})
    rowvals = test_table.get_column(key)
    self.assertEqual(np.sum(rowvals == 22.5), 0)
    self.assertEqual(np.sum(rowvals == -1.e32), 511)

    rowmask = test_table.get_column_mask(key)
    self.assertEqual(np.sum(rowmask), 511)

    # Replacement as a string
    test_table = PdsTable(INDEX_PATH, times=['START_TIME'],
                          invalid={'default': [-1.e32, -2147483648]},
                          replacements={key: {'       22.5': '     -1.e32'}})
    rowvals = test_table.get_column(key)
    self.assertEqual(np.sum(rowvals == 22.5), 0)
    self.assertEqual(np.sum(rowvals == -1.e32), 511)

    rowmask = test_table.get_column_mask(key)
    self.assertEqual(np.sum(rowmask), 511)

    # Replacement via a callback
    def test_callback_as_str(arg):
        if arg.strip() == '22.5': return '-1e32'
        return arg

    test_table = PdsTable(INDEX_PATH, times=['START_TIME'],
                          invalid={'default': [-1.e32, -2147483648]},
                          callbacks={key: test_callback_as_str})
    rowvals = test_table.get_column(key)
    self.assertEqual(np.sum(rowvals == 22.5), 0)
    self.assertEqual(np.sum(rowvals == -1.e32), 511)

    rowmask = test_table.get_column_mask(key)
    self.assertEqual(np.sum(rowmask), 511)

    # Replacement via an ASCII byte string callback
    def test_callback_as_bytes(arg):
        if arg.strip() == b'22.5': return b'-1e32'
        return arg

    test_table = PdsTable(INDEX_PATH, times=['START_TIME'],
                          invalid={'default': [-1.e32, -2147483648]},
                          callbacks={key: test_callback_as_bytes}, ascii=True)
    rowvals = test_table.get_column(key)
    self.assertEqual(np.sum(rowvals == 22.5), 0)
    self.assertEqual(np.sum(rowvals == -1.e32), 511)

    rowmask = test_table.get_column_mask(key)
    self.assertEqual(np.sum(rowmask), 511)

    ####################################
    # "UNK" values replace 22.5 in BIAS_STRIP_MEAN
    # "NULL" in second row of table for CALIBRATION_LAMP_STATE_FLAG
    # "UNK" in the first row for IMAGE_MID_TIME
    # Label says INVALID_CONSTANT = 19.5 for DARK_STRIP_MEAN
    # Label says VALID_RANGE = (2,3) for INST_CMPRS_RATE
    # Manually disallow negative values for FILTER_TEMPERATURE
    # Every value of INSTRUMENT_DATA_RATE is exactly 182.783997 except one.
    ####################################

#     print('')
#     print('Two UserWarnings should follow...')
#     print('')
#     print('25 illegally formatted float values in column BIAS_STRIP_MEAN; ' +
#           'first example is "UNK"')
#     print('Illegally formatted time value in column IMAGE_MID_TIME: UNK')
#     print('')

    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        test_table = PdsTable(EDITED_INDEX_PATH, times=['IMAGE_MID_TIME'],
                              invalid={'default': [-1.e32, -2147483648]},
                              replacements={'INSTRUMENT_DATA_RATE':
                                            {182.783997: 1.}},
                              valid_ranges={'FILTER_TEMPERATURE': [0., 1.e99]})

#     print('')
#     print('')

    image_mid_time = test_table.get_column('IMAGE_MID_TIME')
    bias_strip_mean = test_table.get_column('BIAS_STRIP_MEAN')
    self.assertEqual(type(image_mid_time), list)
    self.assertEqual(type(image_mid_time), list)

    self.assertEqual(image_mid_time[0], 'UNK')
    self.assertEqual(type(image_mid_time[0]), str)
    for value in image_mid_time[1:]:
        self.assertTrue(isinstance(value, float))

    for value in bias_strip_mean:
        self.assertTrue((value == 'UNK') or isinstance(value, float))

    dark_strip_mean = test_table.get_column('DARK_STRIP_MEAN')
    dsm_mask = test_table.get_column_mask('DARK_STRIP_MEAN')
    for (value, flag) in zip(dark_strip_mean, dsm_mask):
        self.assertTrue(flag == (value == 19.5))

    inst_cmprs_rate = test_table.get_column('INST_CMPRS_RATE')
    icr_mask = test_table.get_column_mask('INST_CMPRS_RATE')
    for (value, flag) in zip(inst_cmprs_rate, icr_mask):
        self.assertTrue(flag == (value[0] < 2 or value[0] > 3 or
                                 value[1] < 2 or value[1] > 3))

    filter_temperature = test_table.get_column('FILTER_TEMPERATURE')
    ft_mask = test_table.get_column_mask('FILTER_TEMPERATURE')
    for (value, flag) in zip(filter_temperature, ft_mask):
        self.assertTrue(flag == (value < 0.))

    instrument_data_rate = test_table.get_column('INSTRUMENT_DATA_RATE')
    idr_mask = test_table.get_column_mask('INSTRUMENT_DATA_RATE')
    self.assertTrue(np.sum(instrument_data_rate == 1.) == 99)
    self.assertTrue(np.all(instrument_data_rate != 182.783997))
    self.assertTrue(not np.any(idr_mask))

########################################

if __name__ == '__main__':
    unittest.main()

################################################################################
