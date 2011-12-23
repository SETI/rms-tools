################################################################################
# pdstable.py
#
# Classes and methods to deal with PDS index and table files
#
# Mark R. Showalter, SETI Institute, December 2011
# Revised December 22, 2011 (BSW) - add ability to read, parse, and return data
#                                   that take multiple columns
# Revised December 23, 2011 (BSW) - add adaptation to seconds for TIME fields
################################################################################
import numpy as np
import os
import pdsparser
import julian
import datetime as dt

class PdsColumnInfo(object):
    """The PdsColumnInfo class holds the attributes of one column in a PDS
    label."""

    def __init__(self, node, index):
        """Constructor for a PdsColumn.

        Input:
            node        the pdsparser.PdsNode object defining the column.
            index       the index number of this column, starting at zero.
        """

        self.name = node["NAME"].value
        self.data_type = node["DATA_TYPE"].value
        self.start_byte = node["START_BYTE"].value
        self.bytes = node["BYTES"].value
        self.index = index

        # Handle the optional case of multiple items per column
        self.items = 1
        self.item_bytes = self.bytes
        self.item_offset = self.bytes

        try:
            self.items = node["ITEMS"].value
            self.item_bytes = node["ITEM_BYTES"].value

            # The default value of the offset is the item_bytes
            # This makes sure it gets defined if ITEM_OFFSET is missing
            self.item_offset = self.item_bytes
            self.item_offset = node["ITEM_OFFSET"].value

        except KeyError:
            pass

class PdsTableInfo(object):
    """The PdsTableInfo class holds the attributes of a PDS-labeled table."""

    def __init__(self, label_file_path):
        """Loads a PDS table based on its associated label file."""

        # Parse the label
        self.label_file_path = label_file_path
        self.label = pdsparser.PdsLabel.from_file(label_file_path)

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
            raise IOerror("PDS pointer to data file was not found in label")

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

        counter = 0
        for node in table_node:
            if node.pdsvalue.value == "COLUMN":
                pdscol = PdsColumnInfo(node, counter)
                counter += 1

                self.column_info_list.append(pdscol)
                self.column_info_dict[pdscol.name] = pdscol

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

    def __init__(self, label_file_path, time_format_list=[]):
        """Constructor for a PdsTable object given the path to the detached
        label file.

        Input:
            label_file_path     the path to the PDS label of the table file.
        """

        # Parse the label
        self.info = PdsTableInfo(label_file_path)

        self.column_list = []
        self.column_dict = {}
        k0 = []                 # start_byte in record for each column
        k1 = []                 # end_byte in record for each column

        # Construct the empty buffers for the table data
        for column_info in self.info.column_info_list:
            data_type = column_info.data_type

            if "INT" in data_type:
                dtype = "int"
            elif "REAL" in data_type:
                dtype = "float"
            elif "TIME" in data_type or "DATE" in data_type:
                if column_info.name in time_format_list:
                    dtype = "float"
                else:
                    dtype = "S" + str(column_info.bytes)
            elif "CHAR" in data_type:
                dtype = "S" + str(column_info.bytes)
                    #elif ("CHAR" in data_type or "TIME" in data_type
                #                          or "DATE" in data_type):
                    #    dtype = "S" + str(column_info.bytes)
            else:
                raise IOError("unsupported data type: " + data_type)

            if dtype is None:
                buffer = None
            elif column_info.items != 1:
                buffer = np.empty((self.info.rows,column_info.items),
                                  dtype=dtype)
            else:
                buffer = np.empty((self.info.rows,), dtype=dtype)

            self.column_list.append(buffer)
            self.column_dict[column_info.name] = buffer

            k0.append(column_info.start_byte - 1)
            k1.append(column_info.start_byte + column_info.bytes - 1)

        # Load the table data into the buffers
        file = open(self.info.table_file_path, "r")

        row = 0
        for record_string in file:
            for c in range(self.info.columns):
                if self.column_list[c] == None: continue

                substring = record_string[k0[c]:k1[c]]
                column_info = self.info.column_info_list[c]
                if column_info.items == 1:
                    data_type = column_info.data_type
                    if "TIME" in data_type or "DATE" in data_type:
                        (day,sec) = julian.day_sec_from_iso(substring.strip())
                        tai = julian.tai_from_day(day) + sec
                        self.column_list[c][row] = tai
                    else:
                        self.column_list[c][row] = substring.strip()
                else:
                    offset = column_info.item_offset
                    for i in range(column_info.items):
                        end = offset + column_info.item_bytes
                        self.column_list[c][row][i] = substring[offset:end]

            row += 1

        file.close()

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
#
# Also needs some good unit testing.
