################################################################################
# vicar.py -- classes and methods to read and write VICAR image files.
#
# class VicarImage: Used to encapsulate a VICAR image.
# class VicarError: The exception raised by errors related to the format or
#                   content of a VICAR file.
#
# Mark R. Showalter, SETI Institute, June 2009
# December 2011: Functions renamed to conform to our preferred style.
#
# 6/9/12 MRS - prevented an error that arises when EOL == 1 but no extension
#   header is present.
# 6/14/12 MRS - added as_dict() method.
# 1/1/13 MRS - repaired bug where the extension header would not be parsed if
#   the initial header ended in ASCII null characters.
# 8/23/13 MRS - added support for returning binary headers, prefix bytes,
#   the raw VICAR header, and the raw VICAR extension header, from input files.
# 9/19/13 MRS - added method get_values().
# 12/29/19 MRS - compatible with Python 3 as well as Python 2.
# 12/30/21 MRS - added __contains__, option for dealing with extraneous trailing
#   bytes in Galileo SSI files.
# 8/17/22 MRS - added capability to read binary files in Vax floating-point
#   format.
################################################################################

import numpy as np
import re
import sys
import decimal as dec
import numbers
import warnings
import vax

################################################################################
# VicarImage class
################################################################################

class VicarImage():
    """This class defines the contents of a VICAR data file. It supports methods
    for reading and writing files and for accessing header information.

    The following attributes provide the contents of the data file:
        header              complete VICAR header (including extension if
                            present) as a text string. Trailing null characters
                            have been removed.
        header_bytes        the VICAR header bytes exactly as they appeared in
                            the file.
        extension_bytes     the VICAR extension header bytes exactly as they
                            appeared in the file, or an empty bytestring if not
                            present.
        extension_lblsize   the size in bytes of the VICAR extension header if
                            present; otherwise 0.
        data_2d             the data as a 2-D array. If it is actually a 3-D
                            array, the leading two axes (bands and lines) are
                            merged into one. The data type and byte order of
                            the source file is preserved.
        data_3d             the data as a 3-D array. If it is actually a 2-D
                            array, the leading axis is 1. ALWAYS returned in
                            band-sequential format, with axes (bands, lines,
                            samples). The data type and byte order of the source
                            file is preserved.
        prefix_2d           the row prefix bytes, using the same data type and
                            the same leading axis as data_2d. If the file does
                            not contain prefix bytes, the size of the array is
                            zero.
        prefix_3d           the row prefix bytes, using the same data type and
                            the same leading axes as data_3d. If the file does
                            not contain prefix bytes, the size of the array is
                            zero.
        binary_header       the binary header array, using the same data type
                            as the data arrays.

    Key functions:
        from_file()         load the contents of a VICAR file and return a
                            VicarImage object.
        to_file()           save an object to a new VICAR file; note that only a
                            limited subset of the VICAR standard is supported.
        as_dict()           returns the contents of the VICAR header as a
                            standard Python dictionary.
        set_array()         set the data array of a new VicarImage object, or
                            replace the array of one that already exists.

    Restrictions:
        - The TYPE must always be "IMAGE".
        - The library cannot write files containing VAX reals.
        - The number of prefix bytes must be a multiple of the array element
          size.
        - The NumPy dtype of the binary header array will be the same as that
          of data array, regardless of header values.
        - Files written by to_file() cannot contain binary headers.
        - Files written by to_file() cannot contain prefix bytes.
        - Files written by to_file() must use "BSQ" (band-sequential)
          organization.
    """

    # A dictionary to translate from VICAR FORMAT values to equivalent Python
    # dtypes.
    FORMAT_DICT = { "BYTE" : "u1",
                    "HALF" : "i2",
                    "FULL" : "i4",
                    "REAL" : "f4",
                    "DOUB" : "f8",
                    "COMP" : "c8",
                    "WORD" : "i2",
                    "LONG" : "i4" }

    # A dictionary to translate from Python dtypes (kind,itemsize) to their
    # equivalent VICAR FORMAT values.
    DTYPE_DICT = { ("u",1) : "BYTE",
                   ("i",2) : "HALF",
                   ("i",4) : "FULL",
                   ("f",4) : "REAL",
                   ("f",8) : "DOUB",
                   ("c",8) : "COMP" }

    # A dictionary of Python (platform,byteorder) values types paired with their
    # equivalent VICAR HOST values.
    HOST_DICT = { ("sunos3", "big"   ) : "SUN-3",
                  ("sunos4", "big"   ) : "SUN-4",
                  ("sunos5", "big"   ) : "SUN-SOLR",
                  ("sunos5", "little") : "X86-LINUX",
                  ("darwin", "big"   ) : "MAC-OSX",
                  ("darwin", "little") : "MAC-OSX",
                  ("linux2", "little") : "X86-LINUX",
                  ("win32" , "little") : "WIN-XP"     }

    # A dictionary of Python byteorder values types paired with their
    # equivalent VICAR INTFMT and REALFMT values. These are the byteorders
    # returned by sys.byteorder
    SYS_BYTEORDER_DICT = { "little" : ("LOW" , "RIEEE"),
                           "big"    : ("HIGH", "IEEE" ) }

    # These are the byteorders returned by numpy.dtype.byteorder
    INTFMT_REALFMT_DICT = { "<" : ("LOW" , "RIEEE"),
                            ">" : ("HIGH", "IEEE" ),
                            "=" : SYS_BYTEORDER_DICT[sys.byteorder],
                            "|" : SYS_BYTEORDER_DICT[sys.byteorder] }

    # Categories of keywords
    REQUIRED_KEYWORDS = ["LBLSIZE" ,
                         "FORMAT"  ,
                         "TYPE"    ,
                         "BUFSIZ"  ,
                         "DIM"     ,
                         "EOL"     ,
                         "RECSIZE" ,
                         "ORG"     ,
                         "NL"      ,
                         "NS"      ,
                         "NB"      ,
                         "N1"      ,
                         "N2"      ,
                         "N3"      ,
                         "N4"      ,
                         "NBB"     ,
                         "NLB"     ,
                         "HOST"    ,
                         "INTFMT"  ,
                         "REALFMT" ,
                         "BHOST"   ,
                         "BINTFMT" ,
                         "BREALFMT",
                         "BLTYPE"  ]

    IMMUTABLE_KEYWORDS = ["LBLSIZE" ,
                          "FORMAT"  ,
                          "TYPE"    ,
                          "DIM"     ,
                          "EOL"     ,
                          "RECSIZE" ,
                          "ORG"     ,
                          "NL"      ,
                          "NS"      ,
                          "NB"      ,
                          "N1"      ,
                          "N2"      ,
                          "N3"      ,
                          "N4"      ,
                          "NBB"     ,
                          "NLB"     ,
                          "INTFMT"  ,
                          "REALFMT" ,
                          "BINTFMT" ,
                          "BREALFMT"]

    ############################################################################
    # Constructor
    ############################################################################

    def __init__(self):
        """The constructor for a VicarImage object. It takes no arguments and
        returns an empty header.
        """

        # This contains the data as a numpy ndarray
        self.data_2d = None
        self.data_3d = None

        # This table contains VICAR (keyword,value) pairs in the order they
        # appear in the header. It is initialized with all the required keywords
        # and with a few fields initialized to their default values.
        self.table = [ ["LBLSIZE" , 0      ],
                       ["FORMAT"  , ""     ],
                       ["TYPE"    , "IMAGE"],   # Always
                       ["BUFSIZ"  , 20480  ],   # Always
                       ["DIM"     , 3      ],   # Always
                       ["EOL"     , 0      ],   # For all output files
                       ["RECSIZE" , 0      ],
                       ["ORG"     , "BSQ"  ],   # For all output files
                       ["NL"      , 0      ],
                       ["NS"      , 0      ],
                       ["NB"      , 0      ],
                       ["N1"      , 0      ],
                       ["N2"      , 0      ],
                       ["N3"      , 0      ],
                       ["N4"      , 0      ],   # Always
                       ["NBB"     , 0      ],   # For all output files
                       ["NLB"     , 0      ],   # For all output files
                       ["HOST"    , ""     ],
                       ["INTFMT"  , ""     ],
                       ["REALFMT" , ""     ],
                       ["BHOST"   , ""     ],
                       ["BINTFMT" , ""     ],
                       ["BREALFMT", ""     ],
                       ["BLTYPE"  , ""     ] ]  # For all output files

        # Keeps track of whether the VicarImage was read from a file or not.
        # If is_from_file is True, then we will need to revise the header before
        # it can be written, since the read routine supports more options than
        # the write routine does.
        self.is_from_file = False

    ############################################################################
    # from_file: Create VicarImage object from a file
    ############################################################################

    @staticmethod
    def from_file(filename, extraneous='error'):
        """Returns a VicarImage object given the name of an existing VICAR file.

        Inputs:
            filename        the name of the file to load.
            extraneous      how to handle extraneous bytes in the file:
                            'error' to raise ValueError;
                            'warn' to raise a UserWarning;
                            'print' to print a message;
                            'ignore' to ignore.

        Return:             a VicarImage object.
        """

        if extraneous not in ('error', 'warn', 'print', 'ignore'):
            raise ValueError('unrecognized value for extraneous option: ' +
                             extraneous)

        # Create the object
        this = VicarImage()
        this.is_from_file = True    # Remember that this file was read

        # Open the file for binary read
        with open(filename, "rb") as file:

            # Read the beginning of the VICAR file to get the label size
            file.seek(0)
            header = str(file.read(40).decode('latin1'))        # Python 2 and 3

            if header[0:8] != "LBLSIZE=":
                raise VicarError("Missing LBLSIZE keyword, file: " + filename)

            iblank = header.index(" ", 8)
            vicar_LBLSIZE = int(header[8:iblank])
            this.header_lblsize = vicar_LBLSIZE

            # Read the leading VICAR header
            file.seek(0)
            this.header_bytes = file.read(vicar_LBLSIZE)

            this.header = str(this.header_bytes.rstrip(b"\0").decode('latin1'))
                                                                # Python 2 and 3

            # Interpret the header
            this._load_table(this.header)

            # Extract the basic VICAR file properties that we need
            vicar_FORMAT   = this.get_value("FORMAT" )
            vicar_TYPE     = this.get_value("TYPE"   )
            vicar_EOL      = this.get_value("EOL"    )
            vicar_RECSIZE  = this.get_value("RECSIZE")
            vicar_ORG      = this.get_value("ORG"    , default="BSQ")
            vicar_NL       = this.get_value("NL"     )
            vicar_NS       = this.get_value("NS"     )
            vicar_NB       = this.get_value("NB"     , default=1    )
            vicar_N1       = this.get_value("N1"     )
            vicar_N2       = this.get_value("N2"     )
            vicar_N3       = this.get_value("N3"     )
            vicar_NBB      = this.get_value("NBB"    , default=0    )
            vicar_NLB      = this.get_value("NLB"    , default=0    )
            vicar_INTFMT   = this.get_value("INTFMT" , default="LOW")
            vicar_REALFMT  = this.get_value("REALFMT", default="VAX")

            # Interpret image properties
            if vicar_TYPE != "IMAGE":
                raise VicarError("VICAR file does not contain an image, file: "
                                 + filename)

            # Append the extension header, if present, and re-load the table
            this.extension_bytes = b""
            this.extension_lblsize = 0
            if vicar_EOL != 0:
                offset = (vicar_LBLSIZE + vicar_RECSIZE * vicar_NLB
                                        + vicar_RECSIZE * vicar_N2 * vicar_N3)
                file.seek(offset)
                temp = str(file.read(40).decode('latin1'))      # Python 2 and 3

                # Sometime EOL = 1 but the file has no extension
                if len(temp) == 0:
                    vicar_EOL = 0

            if vicar_EOL != 0:
                if temp[0:8] != "LBLSIZE=":
                    raise VicarError("Missing LBLSIZE keyword in extension, "  +
                                     "file: " + filename)

                iblank = temp.index(" ",8)
                this.extension_lblsize = int(temp[8:iblank])

                file.seek(offset)
                this.extension_bytes = file.read(this.extension_lblsize)

                this.header += \
                    str(this.extension_bytes.rstrip(b"\0").decode('latin1'))
                                                                # Python 2 and 3
                this._load_table(this.header)

            # Look up the numpy dtype corresponding to the VICAR FORMAT
            dtypename = VicarImage.FORMAT_DICT[vicar_FORMAT]

            # Check the item size and kind
            itemsize = np.dtype(dtypename).itemsize
            kind = np.dtype(dtypename).kind

            # Pre-pend the byte order character to the dtype name
            vax_flag = False
            if kind in ("i", "u"):
                if itemsize > 1:
                    if vicar_INTFMT == "LOW":
                        dtypename = "<" + dtypename
                    else:
                        dtypename = ">" + dtypename
            else:
                if vicar_REALFMT == "IEEE":
                    dtypename = ">" + dtypename
                elif vicar_REALFMT == "RIEEE":
                    dtypename = "<" + dtypename
                elif vicar_REALFMT == "VAX":
                    vax_flag = True
                    dtypename = "<" + dtypename
                    this.is_from_file = False

            dtype = np.dtype(dtypename)

            # Record size and prefix bytes must be multiples of the item size
            if vicar_RECSIZE % itemsize != 0:
                raise VicarError("RECSIZE must be a multiple of pixel size")

            if vicar_NBB % itemsize != 0:
                raise VicarError("Prefix size must be a multiple of pixel size")

            # Load the entire file as a 1-D array
            file.seek(0)
            vector = np.fromfile(file, dtype=dtype, sep="", count=-1)

            # Reshape into file records
            samples = vicar_RECSIZE // itemsize
            recs = vector.size // samples
            try:
                records = vector.reshape((recs, samples))
            except ValueError:
                if extraneous == 'error':
                    raise

                records = vector[:recs*samples].reshape((recs, samples))
                if extraneous in ('warn', 'print'):
                    trailing = vector[recs*samples:]
                    if np.all(trailing == 0):
                        message = ('%s has %d zero-valued trailing items' %
                                   (filename, len(trailing)))
                    else:
                        message = ('%s has %d trailing items' %
                                   (filename, len(trailing)))

                    if extraneous == 'print':
                        print(message)
                    else:
                        warnings.warn(message)

            # Slice out the binary header
            vicar_recs = vicar_LBLSIZE // vicar_RECSIZE
            this.binary_header = records[vicar_recs : vicar_recs + vicar_NLB]
            # Note that we assume BINTFMT == INTFMT. This is not checked.

            top_recs = vicar_recs + vicar_NLB
            left_pix = vicar_NBB // itemsize

            data_recs = vicar_N2 * vicar_N3
            this.prefix_2d = records[top_recs : top_recs + data_recs,
                                              : left_pix]

            this.data_2d = records[top_recs : top_recs + data_recs,
                                   left_pix : left_pix + vicar_N1]

            # Deal with Vax binary
            if vax_flag:
                this.set_array(vax.from_vax32(this.data_2d).copy())

            # Reshape to separate the bands
            this.data_3d = this.data_2d.reshape((vicar_N3, vicar_N2, vicar_N1))
            this.prefix_3d = this.prefix_2d.reshape((vicar_N3, vicar_N2,
                                                     this.prefix_2d.shape[-1]))

            # Re-position the band axis as first. The returned array is always
            # ordered (bands, lines, samples).
            if vicar_ORG == "BIP":
                this.data_3d = this.data_3d.rollaxis(2,0)
                this.prefix_3d = this.prefix_3d.rollaxis(2,0)

            elif vicar_ORG == "BIL":
                this.data_3d = this.data_3d.rollaxis(1,0)
                this.prefix_3d = this.prefix_3d.rollaxis(1,0)

        return this

    @staticmethod
    def FromFile(filename):
        """Deprecated, alternative name for from_file()"""
        return VicarImage.from_file(filename)

    ############################################################################
    # from_array: Create VicarImage object from a numpy ndarray
    ############################################################################

    @staticmethod
    def from_array(array):
        """Returns a VicarImage object given an array.

        Inputs:
            array       the array containing the data to use in the VicarImage
                        object.

        Return:         a VicarImage object.
        """

        this = VicarImage()
        this.set_array(array)
        this.is_from_file = False

        return this

    @staticmethod
    def FromArray(array):
        """Deprecated, alternative name for from_array()"""
        return VicarImage.from_array(array)

    ############################################################################
    # to_file(): Public Method to write a VICAR image file
    ############################################################################

    def to_file(self, filename):
        """Writes the VicarImage object into a file.

        Inputs:
            filename = The name of the file to write.
        """

        # Open the file for binary write
        with open(filename, "wb") as file:

            # Revise some VICAR header parameters if necessary
            if self.is_from_file:
                self.set_array(self.data_3d)
                self.is_from_file = False

            # Fill in any missing, required keywords

            # Write the header
            file.write(self.get_header().encode('ascii'))

            # Write the array
            self.data_3d.tofile(file, sep="")

        return

    def ToFile(self, filename):
        """Deprecated, alternative name for to_file()"""
        return self.to_file(filename)

    ############################################################################
    # Public Methods for manipulating VICAR (keyword,value) pairs
    ############################################################################

    def __len__(self):
        return self.keyword_count()

    def __getitem__(self, key):
        if isinstance(key, str):
            return self.get_value(keyword=key)
        if isinstance(key, numbers.Integral):
            return self.get_value(occurrence=key)
        if isinstance(key, (list,tuple)):
            if len(key) != 2:
                raise ValueError("Tuple must contain keyword and index")
            return self.get_value(keyword=key[0], occurrence=key[1])

        raise TypeError("Invalid index type")

    def __setitem__(self, key, value):
        if isinstance(key, str):
            i = self.keyword_index(keyword=key)
            self.set_value_by_index(i, value)
        if isinstance(key, numbers.Integral):
            i = self.keyword_index(occurrence=key)
            self.set_value_by_index(i, value)
        if isinstance(key, (list,tuple)):
            if len(key) != 2:
                raise ValueError("Tuple must contain keyword and index")
            i = self.keyword_index(keyword=key[0], occurrence=key[1])
            self.set_value_by_index(i, value)

        raise TypeError("Invalid index type")

    def __delitem__(self, key):
        if isinstance(key, str):
            i = self.keyword_index(keyword=key)
            self.delete_by_index(i)
        if isinstance(key, numbers.Integral):
            i = self.keyword_index(occurrence=key)
            self.delete_by_index(i)
        if isinstance(key, (list,tuple)):
            if len(key) != 2:
                raise ValueError("Tuple must contain keyword and index")
            i = self.keyword_index(keyword=key[0], occurrence=key[1])
            self.delete_by_index(i)

        raise TypeError("Invalid index type")

    def __contains__(self, key):
        if isinstance(key, str):
            return self.find_keyword(key) >= 0
        if isinstance(key, numbers.Integral):
            return key >= 0 and key < self.keyword_count()
        if isinstance(key, (list,tuple)):
            if len(key) != 2:
                raise ValueError("Tuple must contain keyword and index")
            return self.find_keyword(keyword=key[0], occurrence=key[1]) >= 0

        raise TypeError("Invalid index type")

    def find_keyword(self, keyword=".*", occurrence=0, start=0):
        """Returns the index of a keyword in the VICAR header. Returns -1 if the
        keyword is not found.

        Inputs:
            keyword         A regular expression to match the VICAR keyword(s).
                            Case is ignored.

            occurrence      An index defining which occurrence of the keyword to
                            return; provided because the same keyword can occur
                            multiple times. Use 0 for the first occurrence; this
                            is the default.

            start           The index of the keyword at which the search is to
                            begin. Optional; default is 0, which means that the
                            search will begin at the first keyword.

        Return:             The index of the matching keyword in the table;
                            -1 if the keyword is not found.
        """

        # Compile the regular expression
        pattern = re.compile(keyword, re.IGNORECASE)

        # Walk down the list...
        found = -1
        for i in range(start, len(self.table)):

            # Test this pattern
            k = self.table[i][0]
            test = pattern.match(k)
            if test is None:
                continue

            # If it matches the entire keyword...
            if test.end() == len(k):
                found = found + 1

                # And the occurrence is right, we're done
                if found == occurrence:
                    return i

            # Otherwise, try again

        # No match was found
        return -1

    def keyword_index(self, keyword=".*", occurrence=0, start=0):
        """Returns the index of a keyword in the VICAR header. Raises an error
        if the keyword is not found.

        Inputs:
            keyword         A regular expression to match the VICAR keyword(s).
                            Case is ignored.

            occurrence      An index defining which occurrence of the keyword to
                            return; provided because the same keyword can occur
                            multiple times. Use 0 for the first occurrence; this
                            is the default.

            start           The index of the keyword at which the search is to
                            begin. Optional; default is 0, which means that the
                            search will begin at the first keyword.

        Return:             the index of the matching keyword in the table.
        """

        # Compile the regular expression
        pattern = re.compile(keyword, re.IGNORECASE)

        # Walk down the list...
        found = -1
        for i in range(start, len(self.table)):

            # Test this pattern
            k = self.table[i][0]
            test = pattern.match(k)
            if test is None:
                continue

            # If it matches the entire keyword...
            if test.end() == len(k):
                found = found + 1

                # And the occurrence is right, we're done
                if found == occurrence:
                    return i

            # Otherwise, try again

        # No match was found

        # If the keyword was never matched, raise KeyError
        if found < 0:
            raise KeyError("No keyword found matching \"" + keyword + '"')

        # If there is no keyword, it's an index error
        if keyword == ".*":
            raise IndexError("Index out of range")

        # Otherwise, it's a value error
        message = "Missing keyword " + keyword
        if occurrence != 0:
            message = message + "[" + str(occurrence) + "]"
        if start != 0:
            message = message + " starting at index " + str(start)

        raise ValueError(message)

    def keyword_count(self):
        """Returns the number of keywords.
        """

        return len(self.table)

    def get_value_by_index(self, index):
        """Returns the value of the keyword at the given index.

        Inputs:
            index           The keyword index, as returned by find_keyword().

        Return:             The value of the keyword. The value type is that
                            given in the header: integer, float, decimal,
                            string, or list.
        """

        # Return the value of the keyword
        return self.table[index][1]

    def set_value_by_index(self, index, value, ignore=False, override=False):
        """Replaces the value of a keyword in the VICAR header.

        Inputs:
            index           The keyword index, as returned by find_keyword().

            value           The new value of the keyword.

            ignore          False (default) to raise an error when the user
                            attempts to modify an immutable keyword; True to
                            ignore these errors.
        """

        # The override option is intentionally undocumented above. A value of
        # True enables the modification of immutable keywords.

        # Raise an error if necessary
        immutable = self.table[index][0] in VicarImage.IMMUTABLE_KEYWORDS
        if immutable and not override:
            if ignore:
                return
            else:
                raise VicarError("The value of keyword " + self.table[index][0]
                               + " cannot be changed by the user")

        # Convert tuples to lists
        if isinstance(value, tuple):
            value = list(value)

        # Replace the value
        self.table[index][1] = value

    def delete_by_index(self, index, stop=None, ignore=False, override=False):
        """Deletes one or more keywords, starting at the specified location in
        the VICAR header.

        Inputs:
            index           The index of the first keyword to delete. Negative
                            indices count from the end of the keyword list; -1
                            is the last.

            stop            The index after the last keyword to delete. The
                            default, None, indicates that only one keyword
                            should be deleted. Use 0 to delete to the end of the
                            list.

            ignore          True to ignore attempts to delete required keywords;
                            otherwise, nothing is deleted and an exception is
                            raised.
        """

        # The override option is intentionally undocumented above. A value of
        # True enables the deletion of immutable keywords.

        # If stop value is unspecified, just delete one keyword
        if stop is None:
            stop = index + 1

        # Convert negative indices to positive and get the count
        if index < 0:
            index = len(self.table) + index
        if stop <= 0:
            stop  = len(self.table) + stop
        count = stop - index

        # On override, delete blindly
        if override:
            self.table[index:] = self.table[stop:]
            return

        # On ignore == False, check every keyword first
        if not ignore:
            for i in range(index, stop):
                if self.table[i][0] in VicarImage.REQUIRED_KEYWORDS:
                    raise VicarError("Required keyword " + self.table[i][0] +
                                     " cannot be deleted")

        # Delete the un-required keywords in reverse order
        for i in range(stop-1, index-1, -1):
            if not (self.table[i][0] in VicarImage.REQUIRED_KEYWORDS):
                self.table[i:] = self.table[i+1:]

    def copy_by_index(self, destination, index, stop=None, ignore=False,
                    override=False):
        """Copies one or more keywords and their values to the header of the
        destination VicarImage.

        Inputs:
            index           The index of the first keyword to copy. Negative
                            indices count from the end of the keyword list; -1
                            is the last.

            stop            The index after the last keyword to copy. The
                            default, None, indicates that only one keyword
                            should be deleted. Use 0 to delete to the end of the
                            list.

            ignore          True to ignore attempts to delete required keywords;
                            otherwise, nothing is deleted and an exception is
                            raised.
        """

        # The override option is intentionally undocumented above. A value of
        # True enables the copying of immutable keywords.

        # If stop value is unspecified, just copy one keyword
        if stop is None:
            stop = index + 1

        # Convert negative indices to positive and get the count
        if index < 0:
            index = len(self.table) + index
        if stop <= 0:
            stop = len(self.table) + stop
        count = stop - index

        # On ignore == False, check every keyword first
        if not ignore and not override:
            for i in range(index, count):
                keyword = self.table[i][0]
                if keyword in VicarImage.IMMUTABLE_KEYWORDS:
                    raise VicarError("Keyword " + keyword +
                                     " cannot be modified")

        # Copy one by one
        for i in range(index, count):
            keyword = self.table[i][0]
            value = self.table[i][1]

            required  = (keyword in VicarImage.REQUIRED_KEYWORDS)
            immutable = (keyword in VicarImage.IMMUTABLE_KEYWORDS)

            # Don't change immutable objects unless specifically requested
            if immutable and not override:
                continue

            # Replace the values of required keywords
            if required:
                destination.set_value(keyword, value, ignore=True,
                                                      override=override)
            # Otherwise just append a new keyword
            else:
                destination.append_keyword(keyword, value)

    def insert_keyword(self, keyword, value=None, index=-1, override=False):
        """Inserts a new keyword at the specified location in the VICAR header.

        Inputs:
            keyword         The keyword to insert into the header.

            value           The value of the keyword. Default is None, in which
                            case the value must be set later.

            index           The index of the new keyword in the list. Use -1 to
                            append to the end of the list.
        """

        # The override option is intentionally undocumented above. A value of
        # True enables the insertion of immutable keywords.

        # Make sure this keyword can be inserted
        if not override:
            if keyword.upper() in VicarImage.IMMUTABLE_KEYWORDS:
                raise VicarError("Required keyword " + keyword.upper()
                               + " cannot be inserted")

        # Convert tuples to lists
        if isinstance(value, tuple):
            value = list(value)

        # Insert the keyword at the specified location
        if index != -1:
            self.table.append([keyword.upper(), value])
        else:
            self.table.insert(index, [keyword.upper(), value])

    def append_keyword(self, keyword, value=None, override=False):
        """Appends a keyword and value to the VICAR header.

        Inputs:
            keyword         The keyword to append to the end of the header.

            value           The value of the keyword. Default is None, in which
                            case the value must be set afterward.

        """

        # The override option is intentionally undocumented above. A value of
        # True enables the appending of immutable keywords.

        # Make sure this keyword can be inserted
        if not override:
            if keyword.upper() in VicarImage.IMMUTABLE_KEYWORDS:
                raise VicarError("Required keyword " + keyword.upper()
                               + " cannot be appended")

        # Convert tuples to lists
        if isinstance(value, tuple):
            value = list(value)

        # Append keyword and set value
        self.table.append([keyword.upper(), value])

    def delete_keyword(self, keyword, occurrence=0, start=0, override=False):
        """Deletes one keyword by name and location.

        Inputs:
            keyword         A regular expression to match the VICAR keyword(s).
                            Case is ignored.

            occurrence      An index defining which occurrence of the keyword to
                            delete; provided because the same keyword can occur
                            multiple times. Use 0 for the first occurrence; this
                            is the default.

            start           index of the keyword at which the search is to
                            begin. Optional; default is 0, which means that the
                            search will begin at the first keyword.
        """

        # The override option is intentionally undocumented above. A value of
        # True enables the deletion of immutable keywords.

        # Locate the keyword
        i = self.keyword_index(keyword, occurrence, start)

        # Delete it
        self.delete_by_index(i, override)

    def get_value(self, keyword=".*", occurrence=0, start=0, default=None):
        """Returns the value of a keyword in the VICAR header.

        Inputs:
            keyword         A regular expression to match the VICAR keyword(s).
                            Case is ignored.

            occurrence      An index defining which occurrence of the keyword to
                            return; provided because the same keyword can occur
                            multiple times. Use 0 for the first occurrence; this
                            is the default.

            start           Index of the keyword at which the search is to
                            begin. Optional; default is 0, which means that the
                            search will begin at the first keyword.

            default         The value to return if the keyword is not found.
                            Optional; if not provided, the VicarKeywordMissing
                            exception will be raised.

        Return:             The value of the matching keyword in the table, or
                            the default value if provided. The value type is
                            that given in the header: integer, float, decimal,
                            string, or tuple.
        """

        # Find the keyword
        i = self.find_keyword(keyword, occurrence, start)

        # Return the value if found
        if i >= 0:
            return self.table[i][1]

        # Return the default if available
        if default is not None:
            return default

        # Otherwise raise the normal exception
        i = self.keyword_index(keyword, occurrence, start)

    def get_values(self, keyword=".*"):
        """Returns a list of values of a keyword in the VICAR header.

        Inputs:
            keyword         A regular expression to match the VICAR keyword(s).
                            Case is ignored.

        Return:             A list of the values of the matching keywords. The
                            value type is that given in the header: integer,
                            float, decimal, string, or tuple.
        """

        results = []
        i = -1           # start at the beginning
        while True:
            i = self.find_keyword(keyword, occurrence=0, start=i+1)
            if i < 0:
                return results

            results.append(self.table[i][1])

    def set_value(self, keyword, value, occurrence=0, start=0, ignore=False,
                                                              override=False):
        """Replaces the value of a keyword in the VICAR header, or inserts the
        new keyword if it was not found.

        Inputs:
            keyword         A regular expression to match the VICAR keyword(s).
                            Case is ignored.

            value           The replacement value of the keyword.

            occurrence      An index defining which occurrence of the keyword to
                            set; provided because the same keyword can occur
                            multiple times. Use 0 for the first occurrence; this
                            is the default.

            start           Index of the keyword at which the search is to
                            begin. Optional; default is 0, which means that the
                            search will begin at the first keyword.

            ignore          False (default) to raise an error when the user
                            attempts to modify an immutable keyword; True to
                            ignore these errors.
        """

        # The override option is intentionally undocumented above. A value of
        # True enables the setting of immutable keywords.

        # Find the keyword
        i = self.find_keyword(keyword, occurrence, start)

        # Set the value if found
        if i >= 0:
            self.set_value_by_index(i, value, ignore, override)
            return

        # Otherwise insert the new keyword
        self.insert_keyword(self, keyword, value, start)

    def get_header(self):
        """Returns a string containing the properly formatted keyword=value
        pairs currently in the VICAR header.
        """

        ### Internal method returns a value in VICAR header format
        def _value_string(value):

            # Anything but list or tuple
            if not isinstance(value, (list,tuple)):
                return _value_string1(value)

            # Add the individual elements to a list
            result = ["("]

            for v in value:
                result.append(_value_string1(v))
                result.append(", ")

            result[-1] = ")"

            # Join the results and return
            return "".join(result)

        ### Internal method returns a value in VICAR header format but does not
        ### deal with lists
        def _value_string1(value):

            if isinstance(value, str):
                return "'" + value + "'"
            if isinstance(value, dec.Decimal):
                return str(value)
            if isinstance(value, numbers.Integral):
                return str(value)
            if isinstance(value, numbers.Real):
                return repr(value)

            raise VicarError("Illegal value type for a VICAR keyword: " +
                             str(value) + " (" + str(type(value)) + ")")

        ### Actual method begins here

        # Prepare the header string as a list of short strings, then join them

        # Initialize the list of strings with the LBLSIZE keyword
        # We assume that LBLSIZE will never exceed five digits.
        result = ["LBLSIZE=", ""]
        length = len("LBLSIZE=")

        # Append each successive (keyword,value) pair to the list
        for i in range(1, len(self.table)):

            # Get the next pair
            (keyword,value) = self.table[i]

            # Format the value as a string
            value = _value_string(value)

            # Append individual pieces to the list of strings
            result.append("  ")
            result.append(keyword)
            result.append("=")
            result.append(value)

            # Update the running length
            length += 2 + len(keyword) + 1 + len(value)

        # Update the LBLSIZE value to accommodate the whole header

        digits = 8      # A practical upper limit on the digits of LBLSIZE!
        vicar_RECSIZE = self.get_value("RECSIZE")
        vicar_LBLSIZE = vicar_RECSIZE * ((length + digits + vicar_RECSIZE - 1)
                                        // vicar_RECSIZE)

        self.table[0] = ["LBLSIZE", vicar_LBLSIZE]
        result[1] = _value_string(vicar_LBLSIZE)

        # Iterate once to allow fewer digits in LBLSIZE, which might cut the
        # LBLSIZE by one whole record
        digits = len(result[1])
        self.LBLSIZE = vicar_RECSIZE * ((length + digits + vicar_RECSIZE - 1)
                                       // vicar_RECSIZE)

        self.table[0] = ["LBLSIZE", vicar_LBLSIZE]
        result[1] = _value_string(vicar_LBLSIZE)

        # Fill out the length with blanks
        result.append(" " * (vicar_LBLSIZE - length - digits))

        # Finally, return the joined strings
        return "".join(result)

    def as_dict(self):
        """Returns a dictionary object containing the contents of the VICAR
        header. Note that information about the order of the fields is lost,
        and duplicated keywords just take on their last value. Decimal values
        are converted to floats, and so they might no longer match their header
        values exactly.
        """

        mydict = {}
        for item in self.table:
            if type(item[1]) == dec.Decimal:
                value = float(item[1])
            else:
                value = item[1]

            mydict[item[0]] = value

        # Don't let LBLSIZE be overridden by the extension
        mydict['LBLSIZE'] = self.header_lblsize

        return mydict

    def FindKeyword(self, keyword=".*", occurrence=0, start=0):
        """Deprecated, alternative name for find_keyword()"""
        return self.find_keyword(keyword, occurrence, start)

    def KeywordIndex(self, keyword=".*", occurrence=0, start=0):
        """Deprecated, alternative name for keyword_index()"""
        return self.keyword_index(keyword, occurrence, start)

    def KeywordCount(self):
        """Deprecated, alternative name for keyword_count()"""
        return self.keyword_count()

    def GetValueByIndex(self, index):
        """Deprecated, alternative name for get_value_by_index()"""
        return self.get_value_by_index(index)

    def SetValueByIndex(self, index, value, ignore=False, override=False):
        """Deprecated, alternative name for set_value_by_index()"""
        self.set_value_by_index(index, value, ignore, override)

    def DeleteByIndex(self, index, stop=None, ignore=False, override=False):
        """Deprecated, alternative name for delete_by_index()"""
        self.delete_by_index(index, stop, ignore, override)

    def CopyByIndex(self, destination, index, stop=None, ignore=False,
                    override=False):
        """Deprecated, alternative name for copy_by_index()"""
        self.copy_by_index(destination, index, stop, ignore, override)

    def InsertKeyword(self, keyword, value=None, index=-1, override=False):
        """Deprecated, alternative name for insert_keyword()"""
        self.insert_keyword(keyword, value, index, override)

    def AppendKeyword(self, keyword, value=None, override=False):
        """Deprecated, alternative name for append_keyword()"""
        self.append_keyword(keyword, value, override)

    def DeleteKeyword(self, keyword, occurrence=0, start=0, override=False):
        """Deprecated, alternative name for delete_keyword()"""
        self.delete_keyword(keyword, occurrence, start, override)

    def GetValue(self, keyword=".*", occurrence=0, start=0, default=None):
        """Deprecated, alternative name for get_value()"""
        return self.get_value(keyword, occurrence, start, default)

    def SetValue(self, keyword, value, occurrence=0, start=0, ignore=False,
                                                              override=False):
        """Deprecated, alternative name for set_value()"""
        self.set_value(keyword, value, occurrence, start, ignore, override)

    def GetHeader(self):
        """Deprecated, alternative name for get_header()"""
        return self.get_header()

    ############################################################################
    # Public Methods for manipulating VICAR array data
    ############################################################################

    def get_3d_array(self):
        """Returns the image data as a 3-D ndarray. Deprecated; just access
        attribute data_3d."""

        return self.data_3d

    def get_2d_array(self):
        """Returns the first band of the image as a 2-D ndarray. Deprecated;
        just access attribute data_2d."""

        return self.data_2d

    def set_array(self, array):
        """Replaces the array data in a VicarImage. It also updates all the
        descriptive parameters in the VICAR header.

        Input:
            array           The numpy ndarray to replace.
        """

        # Get the shape and convert to a 2-D or 3-D, as needed
        shape = array.shape
        if len(array.shape) == 2:
            shape = (1,) + shape
            self.data_2d = array
            self.data_3d = array.reshape(shape)

        elif len(array.shape) == 3:
            self.data_2d = array.reshape((array.shape[0] * array.shape[1],
                                          array.shape[2]))
            self.data_3d = array

        else:
            raise VicarError("Only 2-D and 3-D arrays are supported.")

        (vicar_NB, vicar_NL, vicar_NS) = shape
        (vicar_N3, vicar_N2, vicar_N1) = shape

        # Get data type information
        dtype = array.dtype

        # Look up the VICAR FORMAT value
        try:
            vicar_FORMAT = VicarImage.DTYPE_DICT[(dtype.kind, dtype.itemsize)]
        except KeyError:
            raise VicarError("Unsupported data type for VICAR: " + str(dtype))

        # Fill in the byter ordering information
        (vicar_INTFMT,
         vicar_REALFMT) = VicarImage.INTFMT_REALFMT_DICT[dtype.byteorder]

        # Determine record size
        vicar_RECSIZE = dtype.itemsize * vicar_N1

        # Determine the HOST
        try:
            vicar_HOST = VicarImage.HOST_DICT[(sys.platform, sys.byteorder)]
        except KeyError:
            vicar_HOST = sys.platform.upper()

        # Update the required VICAR keywords
        self.set_value("LBLSIZE" , 0            , override=True)
        self.set_value("FORMAT"  , vicar_FORMAT , override=True)
        self.set_value("TYPE"    , "IMAGE"      , override=True)
        self.set_value("BUFSIZ"  , 20480        , override=True)
        self.set_value("DIM"     , 3            , override=True)
        self.set_value("EOL"     , 0            , override=True)
        self.set_value("RECSIZE" , vicar_RECSIZE, override=True)
        self.set_value("ORG"     , "BSQ"        , override=True)
        self.set_value("NL"      , vicar_NL     , override=True)
        self.set_value("NS"      , vicar_NS     , override=True)
        self.set_value("NB"      , vicar_NB     , override=True)
        self.set_value("N1"      , vicar_N1     , override=True)
        self.set_value("N2"      , vicar_N2     , override=True)
        self.set_value("N3"      , vicar_N3     , override=True)
        self.set_value("N4"      , 0            , override=True)
        self.set_value("HOST"    , vicar_HOST   , override=True)
        self.set_value("INTFMT"  , vicar_INTFMT , override=True)
        self.set_value("REALFMT" , vicar_REALFMT, override=True)

        return

    def Get3dArray(self):
        """Deprecated, alternative name for get_3d_array()"""
        return self.get_3d_array()

    def Get2dArray(self):
        """Deprecated, alternative name for get_2d_array()"""
        return self.get_2d_array()

    def SetArray(self, array):
        """Deprecated, alternative name for set_array()"""
        self.set_array(array)

    ############################################################################
    # Private methods
    ############################################################################

    def _load_table(self, header):
        """Creates a list of (keyword,value) pairs and saves them inside the
        VicarImage object.

        Inputs:
            header = the VICAR header string.

        Side effects: the table field of the VicarImage object gets updated.
        """

        ### Internal method to parse one item starting at index i
        def _parse_single(i):
            while header[i] == " ": i +=  1

            if header[i] == "'":
                i += 1
                j = i
                while header[j] != "'": j +=  1

                value = header[i:j]
                j += 1
            else:
                j = i
                is_float = False
                while True:

                    if header[j] in ",) ":
                        if is_float:
                            # Note use of decimal storage, so that printing a
                            # value afterward looks normal.
                            value = dec.Decimal(header[i:j])
                        else:
                            value = int(header[i:j])
                        break

                    if header[j] in ".Ee":
                        is_float = True
                    j += 1

            return (value, j)

        ### Internal method to parse one item starting at index i
        def _parse_group(i):
            value = []
            i +=  1
            while 1:
                (nextval, i) = _parse_single(i)

                value.append(nextval)

                while header[i] == " ":
                    i +=  1

                if header[i] == ")":
                    return (value, i+1)

                if header[i] == ",":
                    i += 1

        ### Execution begins here

        ikey = 0
        while True:

            # Extract the keyword
            jkey = header[ikey:].find("=") + ikey
            if jkey < ikey:
                break

            keyword = header[ikey:jkey].strip()

            # non-ASCII text indicates end of header
            if keyword[0] < " " or keyword[0] > "~":
                return

            # Look for beginning of value
            ivalue = jkey + 1
            while header[ivalue] == " ":
                ivalue = ivalue + 1

            # Interpret value
            if header[ivalue] == "(":
                (value, jvalue) = _parse_group(ivalue)
            else:
                (value, jvalue) = _parse_single(ivalue)

            # Update a required keyword or else append
            if keyword in self.REQUIRED_KEYWORDS:
                index = self.keyword_index(keyword)
                self.table[index][1] = value
            else:
                self.table.append([keyword, value])

            ikey = jvalue

        # Update required parameters as needed
        if not self.get_value("ORG"):
            self.set_value("ORG", "BSQ")

        if not self.get_value("INTFMT"):
            self.set_value("INTFMT", "LOW", override=True)

        if not self.get_value("REALFMT"):
            self.set_value("REALFMT", "VAX", override=True)

        if not self.get_value("BINTFMT"):
            self.set_value("BINTFMT", self.get_value("INTFMT"), override=True)

        if not self.get_value("BREALFMT"):
            self.set_value("BREALFMT", self.get_value("REALFMT"), override=True)

        if not self.get_value("HOST"):
            realfmt = self.get_value("REALFMT")
            if realfmt == "VAX":
                self.set_value("HOST", "VAX-VMS", override=True)
            elif realfmt == "RIEEE":
                self.set_value("HOST", "X86-64", override=True)
            else:
                self.set_value("HOST", "SUN_4", override=True)

        if not self.get_value("BHOST"):
            self.set_value("BHOST",  self.get_value("HOST"), override=True)

################################################################################
# VicarError class
################################################################################

class VicarError(Exception):
    pass
    # Nothing else is needed

################################################################################
# Test program -- no longer supported
################################################################################

# def test():
#         filename = sys.argv[1]
#         vic = VicarImage.from_file(filename)
#
#         print vic.get_value("LBLSIZE")
#         print vic.get_value("FORMAT")
#         print vic.get_value("DAT_TIM",occurrence=0)
#         print vic.get_value("DAT_TIM",occurrence=1)
#         print vic.get_value("FOOBAR",default=55)
#         print vic.get_value(".*",default=55)
#
# #       print "set RECSIZE..."
# #       vic.set_value("RecsizE", 999)
#
#         print "set HOST..."
#         vic.set_value("HOST", "Foobar")
#
# #       print "delete HOST..."
# #       vic.delete_keyword("Host")
#
#         a = vic.get_2d_array()
#         print a
#         print a.shape, a.min(), a.max()
#
#         a = vic.get_3d_array()
#         print a
#         print a.ndim, a.shape, a.min(), a.max()
#
# #        print vic.get_header()
# #        print len(vic.get_header())
# #
# #        vic.to_file("to_file.img")
# #
# #        print vic.get_header()
# #        print len(vic.get_header())
# #
# #        vic.delete_by_index(0,0,ignore=True)
#
#         print vic.get_header()
#         print len(vic.get_header())
#
#         test = VicarImage.from_array(a)
#         print test.get_header().strip()
#
#         vic.copy_by_index(test, 0, 0, ignore=True)
#         print test.get_header().strip()
#
# # Execute the main test progam if this is not imported
# if __name__ == "__main__": test()
#
