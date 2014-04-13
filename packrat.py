import os
import sys
import numpy as np
import base64
import pickle
from xml.sax.saxutils import escape, unescape
import xml.etree.ElementTree as ET

class Packrat(object):
    """A class that supports the reading and writing of objects and their
    attributes.

    Attributes and their values are saved in a readable, reasonably compact XML
    file. When necessary, large objects are stored in a pickle file of the same
    name but extension '.pickle', with a pointer in the XML file.

    The procedure handles the reading and writing of all the standard Python
    types: int, float, bool, str, list, tuple, dict and set.

    The procedure also handles NumPy arrays of all dtypes except 'U' (Unicode)
    and 'o' (object).

    For other object classes, it looks for a class attribute 'PACKRAT_ARGS',
    containing a list of the names of attributes. When writing, the values of
    these attributes are written in the order listed. When reading, it calls
    the constructor using argument values in the order they appear in this
    list.

    For classes that do not have a PACKRAT_ARGS attribute, _all_ of the
    attributes are written to the XML file in alphabetical order. Reading
    returns a tuple (module_name, class_name, attribute_dictionary).

    Like standard files, Packrat files can be open for read ("r"), write ("w")
    or append ("a"). When open for write or append, each call to
        write(name, value)
    appends a new name/value to the end of the file. When open for read, each
    call to
        read()
    returns a tuple containing the name and value of the next object in the 
    file.
    """

    VERSION = '1.0'

    ENTITIES = {'"': '&quot;', "'": '&apos;'}
    UNENTITIES = {'&quot;':'"', '&apos;': "'"}

    def __init__(self, filename, access='w',  indent=2, savings=1.e5):
        """Create a Packrat object for write or append.

        It opens a new file of the given name. Use the close() method when
        finished. An associated pickle file is opened only if it is needed.

        Input:
            filename    the name of the file to open. It should end in ".xml"
            access      'w' to write a new file (replacing one if it already
                        exists); 'a' to append new objects to an existing file;
                        'r' to read an existing file.
            indent      the number of characters to indent entries in the XML
                        hierarchy.
            savings     a tuple containing two values:
                savings[0]  the approximate minimum number of bytes that need to
                            be saved before data values will be written using
                            base64 encoding.
                savings[1]  the approximate minimum number of bytes that need to
                            be saved before data values will be written into an
                            associated pickle file. None to prevent the use of a
                            pickle file.
                        Either value can be None to disable that option.
        """

        if not filename.lower().endswith('.xml'):
            raise ValueError('filename does not end in ".xml": ' + filename)

        if access not in ('w', 'a', 'r'):
            raise ValueError('access is not "w", "a" or "r"')

        self.filename = filename
        self.file = None
        self.access = access
        self._version = Packrat.VERSION
        self.tuples = ()
        self.tuple_no = 0

        self.pickle_filename = os.path.splitext(filename)[0] + '.pickle'
        self.pickle = None

        self.indent = indent

        try:
            if len(savings) == 1:
                savings = (savings[0], savings[0])
        except TypeError:
            savings = (savings, savings)

        self.base64_savings = savings[0] or np.inf
        self.pickle_savings = savings[1] or np.inf

        # When opening for read, load the whole file initially
        if access == 'r':
            self.file = None
            tree = ET.parse(filename)
            root = tree.getroot()

            # On read, use the file's Packrat version number
            self._version = root.attrib['version']

            if os.path.exists(self.pickle_filename):
                pf = open(self.pickle_filename, 'rb')
            else:
                pf = None

            self.tuples = []
            for node in root:
                self.tuples.append(Packrat._read_node(node, pf))

            if pf is not None: pf.close()

            # Emulate read operations by incrementing a pointer
            self.tuple_no = 0
            return

        # When opening for write, initialize the file
        if self.access == 'w':
            self.file = open(filename, 'w')

            self.file.write('<?xml version="1.0" encoding="ASCII"?>\n\n')
            self.file.write('<packrat version="%s">\n' % Packrat.VERSION)

            if os.path.exists(self.pickle_filename):
                os.remove(self.pickle_filename)

        # When opening for append, position before the last line
        else:
            self.file = open(filename, 'r+')

            # Jump to just before the last line of the file
            for line in self.file:
                pass

            self.file.seek(-len(line), 2)

    @staticmethod
    def open(filename, access='r', indent=2, savings=(1000,1000)):
        """Create and open a Packrat object for write or append.

        This is an alternative to calling the constructor directly.

        It opens a new file of the given name. Use the close() method when
        finished. An associated pickle file is opened only if it is needed.

        Input:
            filename    the name of the file to open. It should end in ".xml"
            access      'w' to write a new file (replacing one if it already
                        exists); 'a' to append new objects to an existing file;
                        'r' to read an existing file.
            indent      the number of characters to indent entries in the XML
                        hierarchy.
            savings     a tuple containing two values:
                savings[0]  the approximate minimum number of bytes that need to
                            be saved before data values will be written using
                            base64 encoding.
                savings[1]  the approximate minimum number of bytes that need to
                            be saved before data values will be written into an
                            associated pickle file. None to prevent the use of a
                            pickle file.
                        Either value can be None to disable that option.
        """

        return Packrat(filename, access, indent, savings)

    def close(self):
        """Close this Packrat file."""

        # Close a file open for write or append
        if self.file is not None:

            # Always terminate
            self.file.write('</packrat>\n')
            self.file.close()
            self.file = None

            if self.pickle:
                self.pickle.close
                self.pickle = None

        # Close a file open for read
        else:
            self.tuples = ()
            self.tuple_no = 0

    def _open_pickle(self):
        """Utility to open the pickle file associated with this object.

        This is only called when it is needed for writing or appending.
        """

        if self.pickle: return

        if self.access == 'w':
            self.pickle = open(self.pickle_filename, 'wb')
        elif self.access == 'a':
            self.pickle = open(self.pickle_filename, 'a+b')

    ############################################################################
    # Write methods
    ############################################################################

    def write(self, element, value, level=1, attributes=[]):
        """Write an object into a Packrat file.

        The object and its value is appended to this file.

        Input:
            element     name of the XML element.
            value       the value of the element.
            level       the indent level within the XML file.
            skip        True to skip a line before and after.
            attributes  a list of additional attributes to include as (name,
                        value) tuples.
        """

        close_element = True

        # Write a NumPy ndarray

        if type(value) == np.ndarray:
            self._write_element(element, level, 
                                [('type', 'array'),
                                 ('shape', str(value.shape)),
                                 ('dtype', value.dtype.str)] + attributes, '')

            raw_bytes = value.size * value.itemsize
            kind = value.dtype.kind
            flattened = value.ravel()

            if kind in ('S','c'): first = flattened[0]
            else:                 first = repr(flattened[0])

            # Estimate the size when formatted
            if kind == 'f':
                xml_bytes = value.size * 24
            elif kind in 'iu':
                median = np.median(flattened)
                xml_bytes = value.size * (len(str(median)) + 3)
            elif kind == 'b':
                xml_bytes = value.size
            elif kind == 'c' or value.dtype.str == '|S1':
                xml_bytes = value.size
            elif kind in 'S':
                xml_bytes = value.size * (value.itemsize + 3)
            else:
                raise ValueError('arrays of kind %s are not supported' % kind)

            b64_bytes = int(1.3 * raw_bytes)

            # Write data to a pickle file if the savings is large enough
            if min(xml_bytes, b64_bytes) > raw_bytes + self.pickle_savings:

                # Open the pickle file and append; create if necessary
                self._open_pickle()
                pickle.dump(value, self.pickle)

                self.file.write(' first="%s"' % first)
                self.file.write(' encoding="pickle"/>\n')
                close_element = False

            # Otherwise, write data as base64 if the savings is large enough
            elif xml_bytes > b64_bytes + self.base64_savings:
                if kind == 'S': first = escape(flattened[0], Packrat.ENTITIES)
                else:           first = repr(flattened[0])

                self.file.write(' first="%s"' % first)
                self.file.write(' encoding="base64">\n')

                string = base64.b64encode(value.tostring())
                self.file.write(string) # escape() not needed
                self.file.write('\n')
                self.file.write(self.indent * level * ' ')

            # Handle integers and floats
            elif kind in 'iuf':
                self.file.write(' encoding="text">')
                for v in flattened[:-1]:
                    self.file.write(repr(v))
                    self.file.write(', ')
                self.file.write(repr(flattened[-1]))

            # Handle booleans
            elif kind == 'b':
                self.file.write(' encoding="text">')
                for v in flattened:
                    self.file.write('FT'[v])

            # Handle characters or 1-bytes strings
            elif kind == 'c' or value.dtype.str == '|S1':
                self.file.write(' encoding="text">')
                for v in flattened:
                    self.file.write(escape(v, Packrat.ENTITIES))

            # Handle longer strings
            elif kind == 'S':
                self.file.write(' encoding="text">')

                for v in flattened[:-1]:
                    self.file.write('"')
                    self.file.write(escape(v, Packrat.ENTITIES))
                    self.file.write('", ')

                self.file.write('"')
                self.file.write(escape(flattened[-1], Packrat.ENTITIES))
                self.file.write('"')

            if close_element:
                self.file.write('</' + element + '>\n')

        # Write a standard Python class

        # int, float, bool
        elif type(value) in (int, float, bool):
            self._write_element(element, level,
                                [('type', type(value).__name__)] + attributes)
            self.file.write(repr(value))
            self.file.write('</' + element + '>\n')

        # str
        elif type(value) == str:
            self._write_element(element, level,
                                [('type', type(value).__name__)] + attributes)
            self.file.write('"')
            self.file.write(escape(value, Packrat.ENTITIES))
            self.file.write('"')
            self.file.write('</' + element + '>\n')

        # None
        elif value == None:
            self._write_element(element, level, [('type', 'None')] + attributes,
                                terminate='/>\n')

        # tuple, list
        elif type(value) in (tuple,list):
            self._write_element(element, level,
                                [('type', type(value).__name__)] + attributes)
            self.file.write('\n')

            for (i,item) in enumerate(value):
                self.write('item', item, level=level+1,
                           attributes=[('index',str(i))])

            self.file.write(self.indent * level * ' ')
            self.file.write('</' + element + '>\n')

        # set
        elif type(value) == set:
            self._write_element(element, level,
                                [('type', type(value).__name__)] + attributes)
            self.file.write('\n')

            for item in value:
                self.write('item', item, level=level+1)

            self.file.write(self.indent * level * ' ')
            self.file.write('</' + element + '>\n')

        # dict
        elif type(value) == dict:
            self._write_element(element, level,
                                [('type', type(value).__name__)] + attributes)
            self.file.write('\n')

            keys = value.keys()
            keys.sort()
            for key in keys:
                self._write_dict_pair(key, value[key], level=level+1)

            self.file.write(self.indent * level * ' ')
            self.file.write('</' + element + '>\n')

        # Otherwise write an object

        else:
            self._write_element(element, level,
                                [('type', 'object'),
                                 ('module', type(value).__module__),
                                 ('class', type(value).__name__)] + attributes)
            self.file.write('\n')

            # Use the special attribute list if available
            if hasattr(type(value), 'PACKRAT_ARGS'):
                attr_list = type(value).PACKRAT_ARGS
            else:
                attr_list = value.__dict__.keys()
                attr_list.sort()

            for key in attr_list:
                self.write(key, value.__dict__[key], level=level+1)

            self.file.write(self.indent * level * ' ')
            self.file.write('</' + element + '>\n')

    def _write_element(self, element, level, attributes, terminate='>'):
        """Internal method to write the beginning of one element."""

        self.file.write(self.indent * level * ' ')
        self.file.write('<' + element)

        for tuple in attributes:
            self.file.write(' ' + tuple[0] + '="' +
                            escape(tuple[1], Packrat.ENTITIES) + '"')

        self.file.write(terminate)

    def _write_dict_pair(self, key, value, level):
        """Internal write method for key/value pairs from dictionaries."""

        self.file.write(self.indent * level * ' ')
        self.file.write('<dict_pair>\n')

        self.write('key', key, level=level+1)
        self.write('value', value, level=level+1)

        self.file.write(self.indent * level * ' ')
        self.file.write('</dict_pair>\n')

    ############################################################################
    # Read methods
    ############################################################################

    def read(self):
        """Read the next item from the file.

        The read process is actually emulated, because all of the objects are
        read by the constructor when access is 'r'
        """

        if self.tuple_no >= len(self.tuples):
            return ()

        else:
            result = self.tuples[self.tuple_no]
            self.tuple_no += 1
            return result

    def read_list(self):
        """Return the complete contents as (element, value) pairs."""

        self.tuple_no = len(self.tuples)
        return self.tuples

    def read_dict(self):
        """Return the complete contents as a dictionary."""

        self.tuple_no = len(self.tuples)

        result = {}
        for (key, value) in self.tuples:
            result[key] = value

        return result

    @staticmethod
    def _read_node(node, pf):
        """Interprets one node of the XML tree recursively."""

        node_type = node.attrib['type']

        if node_type == 'int':
            return (node.tag, int(node.text))

        if node_type == 'float':
            return (node.tag, float(node.text))

        if node_type == 'bool':
            return (node.tag, eval(node.text))

        if node_type == 'None':
            return (node.tag, None)

        if node_type == 'str':
            assert node.text[0] == '"'
            assert node.text[-1] == '"'
            return (node.tag, unescape(node.text[1:-1], Packrat.UNENTITIES))

        if node_type in ('list', 'tuple', 'set'):
            result = []
            for subnode in node:
                result.append(Packrat._read_node(subnode, pf)[1])

            if node_type == 'tuple':
                return (node.tag, tuple(result))

            if node_type == 'set':
                return (node.tag, set(result))

            return (node.tag, result)

        if node_type == 'dict':
            result = {}
            for subnode in node:
                key = Packrat._read_node(subnode[0], pf)[1]
                value = Packrat._read_node(subnode[1], pf)[1]
                result[key] = value

            return (node.tag, result)

        if node_type == 'array':
            dtype = node.attrib['dtype']
            kind = np.dtype(dtype).kind
            shape = eval(node.attrib['shape'])
            source = None

            if 'first' in node.attrib:
                first = node.attrib['first']
                if kind in ('S','c'):
                    first = unescape(first, Packrat.UNENTITIES)
                else:
                    first = eval(first)
            else:
                first = None

            if node.attrib['encoding'] == 'pickle':
                result = pickle.load(pf)
                flattened = result.ravel()
                source = 'pickle file'

            elif node.attrib['encoding'] == 'base64':
                decoded = base64.b64decode(unescape(node.text,
                                                    Packrat.UNENTITIES))
                flattened = np.fromstring(decoded, dtype=dtype)
                result = flattened.reshape(shape)
                source = 'base64 string'

            elif kind == 'b':
                result = []
                for v in node.text:
                    result.append(v == 'T')
                result = np.array(result).reshape(shape)

            elif kind == 'c' or dtype == '|S1':
                result = []
                for v in unescape(node.text, Packrat.UNENTITIES):
                    result.append(v)
                result = np.array(result, dtype=dtype).reshape(shape)

            elif kind == 'S':
                result = eval('[' + node.text + ']')
                for (i,value) in enumerate(result):
                    if '&' in value:
                        result[i] = unescape(value, Packrat.UNENTITIES)
                result = np.array(result, dtype=dtype).reshape(shape)

            else:
                result = np.fromstring(node.text, sep=',', dtype=dtype)
                result = result.reshape(shape)

            if (first is not None and
                source is not None and
                flattened[0] != first):
                    raise IOError('error decoding %s: %s != %s' %
                                  (source, repr(first), repr(flattened[0])))

            return (node.tag, result)

        if node_type == 'object':
            module = node.attrib['module']
            classname = node.attrib['class']
            try:
                cls = sys.modules[module].__dict__[classname]
            except KeyError:
                cls = None

            # Create a dictionary of elements
            object_dict = {}
            for subnode in node:
                (key, value) = Packrat._read_node(subnode, pf)
                object_dict[key] = value

            # For an unrecognized class, just return the attribute dictionary
            if cls is None:
                return (node.tag, object_dict)

            # If the class has a PACKRAT_ARGS list, call the constructor
            if hasattr(cls, 'PACKRAT_ARGS'):
                args = []
                for key in cls.PACKRAT_ARGS:
                    args.append(object_dict[key])

                obj = object.__new__(cls)
                obj.__init__(*args)
                return (node.tag, obj)

            # Otherwise, create a new object and install the attributes.
            # This approach is not generally recommended but it will often work.
            obj = object.__new__(cls)
            obj.__dict__ = object_dict

            return (node.tag, obj)

################################################################################
# Unit tests
################################################################################

import unittest

class Foo(object):
    def __init__(self, a, b):
        self.ints = a
        self.floats = b
        self.sum = a + b

class Bar(object):
    PACKRAT_ARGS = ['ints', 'floats']
    def __init__(self, a, b):
        self.ints = a
        self.floats = b
        self.sum = a + b

class test_packrat(unittest.TestCase):

  def runTest(self):

    filename = 'packrat_unittests.xml'

    ####################
    f = Packrat.open(filename, access='w')
    f.write('two', 2)
    f.close()

    ####################
    f = Packrat.open(filename, access='r')
    rec = f.read()
    self.assertEqual(rec[0], 'two')
    self.assertEqual(rec[1], 2)
    self.assertEqual(type(rec[1]), int)

    rec = f.read()
    self.assertEqual(rec, ())
    f.close()

    ####################
    f = Packrat.open(filename, access='a')
    f.write('three', 3.)
    f.write('four', '4')
    f.write('five', (5,5.,'five'))
    f.write('six', [6,6.,'six'])
    f.write('seven', set([7,'7']))
    f.write('eight', {8:'eight', 'eight':8.})
    f.write('nine', True)
    f.write('ten', False)
    f.close()

    ####################
    f = Packrat.open(filename, access='r')
    rec = f.read()
    self.assertEqual(rec[0], 'two')
    self.assertEqual(rec[1], 2)
    self.assertEqual(type(rec[1]), int)

    rec = f.read()
    self.assertEqual(rec[0], 'three')
    self.assertEqual(rec[1], 3.)
    self.assertEqual(type(rec[1]), float)

    rec = f.read()
    self.assertEqual(rec[0], 'four')
    self.assertEqual(rec[1], '4')
    self.assertEqual(type(rec[1]), str)

    rec = f.read()
    self.assertEqual(rec[0], 'five')
    self.assertEqual(rec[1], (5,5.,'five'))
    self.assertEqual(type(rec[1]), tuple)
    self.assertEqual(type(rec[1][0]), int)
    self.assertEqual(type(rec[1][1]), float)
    self.assertEqual(type(rec[1][2]), str)

    rec = f.read()
    self.assertEqual(rec[0], 'six')
    self.assertEqual(rec[1], [6,6.,'six'])
    self.assertEqual(type(rec[1]), list)
    self.assertEqual(type(rec[1][0]), int)
    self.assertEqual(type(rec[1][1]), float)
    self.assertEqual(type(rec[1][2]), str)

    rec = f.read()
    self.assertEqual(rec[0], 'seven')
    self.assertEqual(rec[1], set([7,'7']))
    self.assertEqual(type(rec[1]), set)

    rec = f.read()
    self.assertEqual(rec[0], 'eight')
    self.assertEqual(rec[1], {8:'eight', 'eight':8.})
    self.assertEqual(rec[1][8], 'eight')
    self.assertEqual(rec[1]['eight'], 8.)

    rec = f.read()
    self.assertEqual(rec[0], 'nine')
    self.assertEqual(rec[1], True)
    self.assertEqual(type(rec[1]), bool)

    rec = f.read()
    self.assertEqual(rec[0], 'ten')
    self.assertEqual(rec[1], False)
    self.assertEqual(type(rec[1]), bool)

    ####################
    f = Packrat.open(filename, access='a')
    f.write('eleven', {'>11':'<=13', '>=11':12, '"elev"':"'11'"})
    f.write('twelve', 'eleven<"12"<<thirteen>')
    f.write('thirteen', None)
    f.close()

    ####################
    f = Packrat.open(filename, access='r')
    recs = f.read_list()

    self.assertEqual(recs[-4][0], 'ten')

    self.assertEqual(recs[-3][0], 'eleven')
    self.assertEqual(recs[-3][1], {'>11':'<=13', '>=11':12, '"elev"':"'11'"})
    self.assertEqual(recs[-3][1]['>11'], '<=13')
    self.assertEqual(recs[-3][1]['>=11'], 12)
    self.assertEqual(recs[-3][1]['"elev"'], "'11'")

    self.assertEqual(recs[-2][0], 'twelve')
    self.assertEqual(recs[-2][1], 'eleven<"12"<<thirteen>')

    self.assertEqual(recs[-1][0], 'thirteen')
    self.assertEqual(recs[-1][1], None)

    ####################
    f = Packrat.open(filename, access='a')

    bools = np.array([True, False, False, True]).reshape(2,1,2)
    ints = np.arange(20)
    floats = np.arange(20.)

    random = np.random.randn(20).reshape(2,2,5)
    random *= 10**(30. * np.random.randn(20).reshape(2,2,5))

    strings = np.array(['1', '22', '333', '4444']).reshape(2,2)
    uints = np.arange(40,60).astype('uint')
    chars = np.array([str(i) for i in (range(10) + list('<>"'))])

    f.write('bools', bools)
    f.write('ints', ints)
    f.write('floats', floats)

    f.write('random', random)

    f.write('strings', strings)
    f.write('uints', uints)
    f.write('chars', chars)
    f.close()

    ####################
    f = Packrat.open(filename, access='r')
    recs = f.read_dict()

    self.assertTrue(np.all(recs['bools'] == bools))
    self.assertTrue(np.all(recs['ints'] == ints))
    self.assertTrue(np.all(recs['floats'] == floats))
    self.assertTrue(np.all(recs['random'] == random))
    self.assertTrue(np.all(recs['strings'] == strings))
    self.assertTrue(np.all(recs['uints'] == uints))
    self.assertTrue(np.all(recs['chars'] == chars))
    f.close()

    #################### uses a pickle file
    f = Packrat.open(filename, access='a')

    more_ints = np.arange(10000).reshape(4,100,25)
    f.write('more_ints', more_ints)
    f.close()

    ####################
    f = Packrat.open(filename, access='r')
    recs = f.read_dict()

    self.assertTrue(np.all(recs['more_ints'] == more_ints))

    #################### uses base64
    f = Packrat.open(filename, access='a', savings=(1,1.e99))

    more_floats = np.arange(200.)
    f.write('more_floats', more_floats)

    more_randoms = np.random.randn(200).reshape(2,5,4,5)
    more_randoms *= 10**(30. * np.random.randn(200).reshape(2,5,4,5))

    f.write('more_floats', more_floats)
    f.write('more_randoms', more_randoms)
    f.write('more_randoms_msb', more_randoms.astype('>f8'))
    f.write('more_randoms_lsb', more_randoms.astype('<f8'))
    f.close()

    ####################
    f = Packrat.open(filename, access='r')
    recs = f.read_dict()

    self.assertTrue(np.all(recs['more_floats'] == more_floats))
    self.assertTrue(np.all(recs['more_randoms'] == more_randoms))
    self.assertTrue(np.all(recs['more_randoms_lsb'] == more_randoms))
    self.assertTrue(np.all(recs['more_randoms_msb'] == more_randoms))

    #################### uses a new class foo, without PACKRAT_ARGS
    f = Packrat.open(filename, access='a')
    f.write('foo', Foo(np.arange(10), np.arange(10.)))
    f.close()

    ####################
    f = Packrat.open(filename, access='r')
    recs = f.read_dict()

    self.assertEqual(type(recs['foo']), Foo)
    self.assertTrue(np.all(recs['foo'].ints == np.arange(10)))
    self.assertTrue(np.all(recs['foo'].floats == np.arange(10.)))
    self.assertTrue(np.all(recs['foo'].sum == 2.*np.arange(10)))

    #################### uses a new class bar, with PACKRAT_ARGS
    sample_bar = Bar(np.arange(10), np.arange(10.))
    f = Packrat.open(filename, access='a')
    f.write('bar', sample_bar)
    f.close()

    ####################
    f = Packrat.open(filename, access='r')
    recs = f.read_dict()

    self.assertEqual(type(recs['bar']), Bar)
    self.assertTrue(np.all(recs['bar'].ints   == sample_bar.ints))
    self.assertTrue(np.all(recs['bar'].floats == sample_bar.floats))
    self.assertTrue(np.all(recs['bar'].sum    == sample_bar.sum))

################################################################################
# Perform unit testing if executed from the command line
################################################################################

if __name__ == '__main__':
    unittest.main()

################################################################################
