#!/usr/bin/python
################################################################################
# pdsparser.py
#
# Classes and methods to read, write and parse PDS labels.
#
# Mark R. Showalter, SETI Institute, January 2011
################################################################################
# Printing of 2-D sequences has not yet been tested.
# Tracking of comments has been stripped away.
# Tracking of substring locations has been stripped away for simplicity.
# This will need a lot of work if we eventually want to do more general writing
# of labels, but it implements the complete grammar for reading.
#
# Old notes follow...
#
# Structure generated supports basic dictionary-type indexing.
# 
# Node objects contain a single record, except the opening lines of OBJECT and
# GROUPs enclose their contents.
# 
# Comments are attached to the item before them unless this is impossible (such
# as due to intervening punctuation); then they are attached to the item after.
# 
# Every PdsItem has indices in the string to where the information begins and
# ends, as well as a pointer to the string.
# 
# Every PdsItem has a possible "eol" object which could be a newline, short
# comment or long comment. It also has a possible "eol_before" The only case of
# eol_before is in a sequence or set where the comment occurs after a comma; in
# this case, the comment is attached to the element that follows.
# 
# PdsValues only have attached comments if they appear inside the gaps within
# the definition, e.g., between a value and its units, or between the elements
# of a sequence or set.
# 
# Most comments are attached to statements instead. They are usually after the
# value but can also appear before or after the equal sign.
# 
# There is currently no organized way to locate comments except by an extensive
# tree search.
# 
# Still need an option to find and replace STRUCTURE pointers and re-parse.
# 
# Changing the label will throw off all the string pointers!
#
# MRS, July 26, 2009
################################################################################

from pyparsing import *
import decimal as dec
import datetime as dt

################################################################################
################################################################################
# PdsNode
################################################################################
################################################################################

PARSE_NODES = []        # The current list of nodes in the parse hierarchy.

class PdsNode(object):
    """Class for any statement or node of a PDS parsing tree."""

    def __init__(self, parent=None):
        self.parent = parent        # The parent of this node.
        self.children = []          # If it's an object, the child nodes.
        self.dict = {}              # A dictionary of the keyword, object and
                                    # group names.

        self.name = ""              # Name of keywords; values for OBJECTs or
                                    # GROUPs.
        self.type = ""              # "OBJECT", "GROUP", "ROOT", or "KEYWORD".

        self.keyword = None         # PdsKeyword before equal sign.
        self.pdsvalue = None        # PdsValue after equal sign.

    def __str__(self):
        return "".join(self.formatted_list(0))

    def __repr__(self): return str(self)

    def formatted_list(self, indent):

        # If this is root, out-dent and just print the children
        if (self.keyword is None and self.pdsvalue is None and
            self.name == "ROOT"):
                indent -= 1
                result = []
        else:
            # Print the keyword, indented properly
            result = indent * ["  "] + [str(self.keyword)]

            # Print the equal sign
            result += [" = "]

            # Print the value
            result += self.pdsvalue.formatted_list(indent + 1)

        # Print each child statement indented
        for c in self.children[:-1]:      # Stop before END_...
            result += ["\n"] + c.formatted_list(indent + 1)

        # Print the END_OBJECT/END_GROUP without indent if necessary
        if len(self.children) > 0:
            result += ["\n"] + self.children[-1].formatted_list(max(indent,0))

        return result

    def __getitem__(self, key):
        if type(key) == type(0):
            if self.children != []: return self.children[key]
            else:                   return self.pdsvalue[key]
        else:
            if self.dict[key].children != []: return self.dict[key]
            else:                             return self.dict[key].pdsvalue

    def __len__(self):
        if self.children != []: return len(self.children)
        else:                   return len(self.pdsvalue)

    @staticmethod
    def parse(s, l, tokens):

        global PARSE_NODES

        struct = PdsNode(PARSE_NODES[-1])
        struct.parent.children.append(struct)

        # Locate extra EOLs around equal sign
        struct.keyword = tokens[0]      # Keyword is always first
        struct.pdsvalue = tokens[1]     # Value is always second

        # This is an initial guess
        struct.type = "KEYWORD"
        struct.name = str(struct.keyword)

        # If a new object or group begins, update the node list
        if (struct.keyword.name == "OBJECT" or
            struct.keyword.name == "GROUP"):

            if (not isinstance(struct.pdsvalue, PdsText) or
                struct.pdsvalue.quote != ""):
                    raise SyntaxError('Invalid name for ' +
                        struct.keyword.name + ": " + str(struct.pdsvalue))

            struct.name = struct.pdsvalue.value
            struct.type = struct.keyword.name

            # Add the object/group to the parent's dictionary
            struct.parent.dict[struct.name] = struct

            # Add the new node to the current heirarchy
            PARSE_NODES.append(struct)

        # End of object or group...
        elif (struct.keyword.name == "END_OBJECT" or
              struct.keyword.name == "END_GROUP"):

            # Make sure types match
            if struct.keyword.name[4:] != PARSE_NODES[-1].type:
                raise SyntaxError("Nesting mismatch: " + PARSE_NODES[-1].type +
                        " vs. " + struct.keyword.name)

            # Make sure identifier is valid
            if (not isinstance(struct.pdsvalue, PdsText) or
                struct.pdsvalue.quote):
                    raise SyntaxError('Invalid name for END_' +
                        struct.keyword.name + ": " + str(struct.pdsvalue))

            # Make sure identifiers match
            if PARSE_NODES[-1].name != struct.pdsvalue.value:
                raise SyntaxError("Nesting mismatch: " + PARSE_NODES[-1].type +
                        " " + PARSE_NODES[-1].name + " vs. " +
                        struct.keyword.name + " " + struct.pdsvalue.value)

            # Go back to the parent node
            PARSE_NODES.pop()

        # If this is still a keyword, add it to the parent's dictionary
        else:
            struct.parent.dict[struct.name] = struct

        return

    @staticmethod
    def parse_end(s, l, tokens):

        global PARSE_NODES

        if len(PARSE_NODES) != 1:
            raise SyntaxError("Un-terminated " + PARSE_NODES[-1].type + ": " +
                PARSE_NODES[-1].name)

    @staticmethod
    def init_current_node():

        global PARSE_NODES

        PARSE_NODES = [PdsNode(None)]
        PARSE_NODES[0].name = "ROOT"
        PARSE_NODES[0].type = "ROOT"

################################################################################
# PdsItem
################################################################################

class PdsItem(object):
    """General class for any part of a PDS label."""

################################################################################
# BEGIN GRAMMAR
################################################################################
whites = " \t"
ParserElement.setDefaultWhitespaceChars(whites)
WHITE           = Word(whites)
#-----------------------------------------------------------------------
IDENTIFIER      = Combine(Word(alphas, alphanums + "_"))
IDENTIFIER.setName("IDENTIFIER")
#-----------------------------------------------------------------------
newline         = "\n"
NEWLINE         = Literal(newline)
NEWLINE.setName("NEWLINE")
#-----------------------------------------------------------------------
COMMENT         = (Combine("/*" + CharsNotIn(newline)) +  NEWLINE)
COMMENT.setName("COMMENT")
#-----------------------------------------------------------------------
EOL             = Suppress(COMMENT | NEWLINE)               # Order matters
################################################################################
################################################################################
# PdsValue classes
################################################################################
################################################################################

class PdsValue(PdsItem):
    """The generic class for anything that can appear on the right side of an
    equal sign in a PDS label."""

    def __init__(self, value=None, parser=None):
        PdsItem.__init__(self)
        self.value = value      # A representation for the value of the object
        self.parser = parser    # Currently unused

    # Default string is just a default formatting of the value
    def __str__(self): return str(self.value)

    def __repr__(self): return repr(self.value)

    def formatted_list(self, indent): return str(self)

    # Allow basic operations on PdsValue types
    def __add__(self, other): return self.value + other
    def __sub__(self, other): return self.value - other
    def __mul__(self, other): return self.value * other
    def __div__(self, other): return self.value / other

    def __radd__(self, other): return other + self.value
    def __rsub__(self, other): return other - self.value
    def __rmul__(self, other): return other * self.value
    def __rdiv__(self, other): return other / self.value

    def __neg__(self): return -self.value
    def __pos__(self): return +self.value

    # Basic type conversions
    def __int__(self): return int(self.value)
    def __float__(self): return float(self.value)

class PdsScalar(PdsValue):
    """The generic class for any single value that can appear on the right side
    of an equal sign in a PDS label."""

class PdsNumber(PdsScalar):
    """The generic class for any single numeric value that can appear on the
    right side of an equal sign in a PDS label."""

################################################################################
# PdsInteger
################################################################################
SIGN            = oneOf("+ -")
UNSIGNED_INT    = Word(nums)
SIGNED_INT      = Combine(Optional(SIGN) + UNSIGNED_INT)

INTEGER         = Combine(Optional(SIGN) + UNSIGNED_INT)
INTEGER.setName("INTEGER")
#-----------------------------------------------------------------------

class PdsInteger(PdsNumber):
    """An integer value."""

    def __init__(self):
        PdsValue.__init__(self, 0, INTEGER)

    # Interpret parser tokens
    @staticmethod
    def parse(s, l, tokens):
        struct = PdsInteger.from_int(int(tokens[0]))
        return struct

    # Create an object
    @staticmethod
    def from_int(value=0):
        """Returns a PdsInteger given an int."""

        struct = PdsInteger()
        struct.value = value

        return struct

#-----------------------------------------------------------------------
INTEGER.setParseAction(PdsInteger.parse)
################################################################################
# PdsBasedInteger
################################################################################
HEX_INT         = Word(hexnums)
SIGNED_HEX_INT  = Combine(Optional(SIGN) + HEX_INT)
BASED_INT       = (Suppress(Optional(WHITE))
                +  UNSIGNED_INT
                +  Suppress("#")
                +  SIGNED_HEX_INT
                +  Suppress("#"))
BASED_INT.setWhitespaceChars("")
BASED_INT.setName("BASED_INT")
#-----------------------------------------------------------------------

class PdsBasedInteger(PdsInteger):
    """An integer value in an alternative radix 2-16."""

    BASE_DIGITS = "0123456789ABCDEF"

    def __init__(self):
        PdsValue.__init__(self, 0, BASED_INT)

        self.radix = 0          # The radix of the based integer
        self.digits = ""        # The "digits" string of the based integer
        self.sign = ""          # The optional sign character

    def __str__(self):
        return str(self.radix) + "#" + self.sign + self.digits + "#"

    # Interpret parser tokens
    @staticmethod
    def parse(s, l, tokens):

        radix = int(tokens[0])
        (number, ndigits, use_plus) = PdsBasedInteger._number(tokens[1], radix)

        struct = PdsBasedInteger.from_int(number, radix, ndigits, use_plus)
        return struct

    # Create an object
    @staticmethod
    def from_int(number, radix, mindigits=1, use_plus=False):
        """Returns a new PdsBasedInteger given a number or string and a
        radix."""

        struct = PdsBasedInteger()

        if number < 0:
            struct.sign = "-"
        elif use_plus:
            struct.sign = "+"
        else:
            struct.sign = ""

        struct.value = number
        struct.radix = radix
        struct.digits = PdsBasedInteger._digits(abs(number), radix, mindigits)
        return struct

    # Internal methods
    @staticmethod
    def _digits(number, radix, mindigits=1, use_plus=False):
        """Converts a number to a string in the specified radix."""

        if radix < 2 or radix > 16: raise ValueError("radix out of range")

        is_neg = (number < 0)
        number = abs(number)

        result = ""
        while number != 0:
            number, digit = divmod(number, radix)
            result = PdsBasedInteger.BASE_DIGITS[digit] + result

        zeros = mindigits - len(result)
        if zeros > 0: result = "0" * zeros + result

        if is_neg:
            result = "-" + result
        elif use_plus:
            result = "+" + result

        return result

    @staticmethod
    def _number(digits, radix):
        """Converts a string to a number given the specified radix."""

        if radix < 2 or radix > 16: raise ValueError("radix out of range")

        digits = digits.strip()

        is_neg   = (digits[0] == "-")
        use_plus = (digits[0] == "+")
        if is_neg or use_plus: digits = digits[1:]
            
        value = 0
        for c in digits:
            i = "0123456789ABCDE".index(c)
            if i >= radix:
                raise ValueError("Digits are incompatible with radix")

            value = value * radix + i

        if is_neg: value = -value

        return (value, len(digits), use_plus)

#-----------------------------------------------------------------------
BASED_INT.setParseAction(PdsBasedInteger.parse)
################################################################################
# PdsReal
################################################################################
EXPONENT        = (oneOf("e E") + SIGNED_INT)
REAL_WITH_INT   = Combine(SIGNED_INT
                        + "."
                        + Optional(UNSIGNED_INT)
                        + Optional(EXPONENT))
REAL_WO_INT     = Combine(Optional(SIGN) 
                        + "."
                        + UNSIGNED_INT
                        + Optional(EXPONENT))
REAL_WO_DOT     = Combine(SIGNED_INT + EXPONENT)

REAL_NUMBER     = (REAL_WITH_INT
                ^  REAL_WO_INT
                ^  REAL_WO_DOT)
REAL_NUMBER.setName("REAL")
#-----------------------------------------------------------------------

class PdsReal(PdsNumber):
    """A real (floating-point) number."""

    def __init__(self):
        PdsValue.__init__(self, 0., REAL_NUMBER)

        self.decimal = None     # The value formatted as a decimal
        self.string  = ""       # The value as a string

    def __str__(self):
        return str(self.decimal)

    def __repr__(self):
        return self.string

    # Interpret parser tokens
    @staticmethod
    def parse(s, l, tokens):
        struct = PdsReal()

        struct.value = float(tokens[0])
        struct.decimal = dec.Decimal(tokens[0])
        return struct

    @staticmethod
    def from_value(value=0., format=""):
        """Returns a PdsReal given a double or decimal."""

        struct = PdsDouble()
        struct.value = double(value)

        if type(value) == type(dec.Decimal("0.")):
            struct.decimal = value
            struct.string  = repr(value)
        else:
            struct.string = format%value
            struct.decimal = dec.Decimal(struct.string)

#-----------------------------------------------------------------------
REAL_NUMBER.setParseAction(PdsReal.parse)
#-----------------------------------------------------------------------
NUMBER_WO_UNITS = REAL_NUMBER | BASED_INT | INTEGER     # Order matters here!
################################################################################
# PdsUnitsExpr
################################################################################
UNIT_EXPR     = Combine("<" + OneOrMore(CharsNotIn("\n >")) + ">")
#-----------------------------------------------------------------------

class PdsUnitExpr(PdsValue):
    """A unit expression."""

    def __init__(self):
        PdsValue.__init__(self, "", UNIT_EXPR)

    def __str__(self):
        return "<" + self.value + ">"

    @staticmethod
    def parse(s, l, tokens):

        struct = PdsUnitExpr()
        struct.value = tokens[0][1:-1]

        return struct

#-----------------------------------------------------------------------
UNIT_EXPR.setParseAction(PdsUnitExpr.parse)
################################################################################
# PdsNumberWithUnits
################################################################################
NUMBER_W_UNITS  = NUMBER_WO_UNITS + ZeroOrMore(EOL) + UNIT_EXPR
NUMBER_W_UNITS.setName("NUMBER_W_UNITS")
#-----------------------------------------------------------------------

class PdsNumberWithUnits(PdsNumber):
    """A number with units."""

    def __init__(self):
        PdsValue.__init__(self, 0., NUMBER_W_UNITS)
        self.pdsnumber = None   # The associated PdsNumber object
        self.pdsunits = None    # The PdsUnitExpr object

    def __str__(self):
        return str(self.pdsnumber) + " " + str(self.pdsunits)

    # Interpret parser tokens
    @staticmethod
    def parse(s, l, tokens):

        struct = PdsNumberWithUnits()
        struct.pdsnumber = tokens[0]
        struct.pdsunits  = tokens[1]
        struct.value     = struct.pdsnumber.value

        return struct

#-----------------------------------------------------------------------
NUMBER_W_UNITS.setParseAction(PdsNumberWithUnits.parse)
#-----------------------------------------------------------------------
NUMBER          = NUMBER_W_UNITS | NUMBER_WO_UNITS      # Order matters here!
################################################################################
# PdsTime: value is a string representation of the time
################################################################################

class PdsTime(PdsScalar): pass

################################################################################
# PdsHmsTime
################################################################################
HMS_TIME        = (UNSIGNED_INT
                +  Suppress(":")
                +  UNSIGNED_INT
                +  Optional(Suppress(":")
                         +  Combine(UNSIGNED_INT
                                  + Optional("."
                                  + Optional(UNSIGNED_INT)))))
HMS_TIME.setWhitespaceChars("")
HMS_TIME.setName("HMS_TIME")
#-----------------------------------------------------------------------

class PdsHmsTime(PdsTime):
    """A time of day, excluding a time zone."""

    def __init__(self):
        PdsValue.__init__(self, "", HMS_TIME)
        self.hour = 0
        self.minute = 0
        self.second = 0
        self.elapsed = 0

    def __str__(self):
        result = "%02d" % self.hour + ":" + "%02d" % self.minute + ":"

        if type(self.second) == type(0):
            return result + "%02d" % self.second

        if type(self.second) == type(dec.Decimal("0.")):
            secstr = str(self.second)
            if secstr[1] == ".": return result + "0" + secstr
            if secstr[2] == ".": return result + secstr

        return result + "%06.3f" % self.second

    # Interpret parser tokens
    @staticmethod
    def parse(s, l, tokens):

        if len(tokens) == 2:
            struct = PdsHmsTime.from_hms(int(tokens[0]), int(tokens[1]), 0)
            struct.index1 = l
            return struct

        try:
            second = int(tokens[2])
        except:
            second = dec.Decimal(tokens[2])

        struct = PdsHmsTime.from_hms(int(tokens[0]), int(tokens[1]), second)
        return struct

    @staticmethod
    def from_hms(hour, minute, second=0):
        """Returns a new PdsHmsTime given an hour, minute and optional second.
        "The second can be int, float or decimal."""

        struct = PdsHmsTime();

        struct.hour = hour
        struct.minute = minute
        struct.second = second
        struct.value = str(struct)
        struct.elapsed = 3600 * hour + 60 * minute + second

        if hour   < 0 or hour   > 23: raise ValueError("hour out of range")
        if minute < 0 or minute > 59: raise ValueError("minute out of range")
        if second < 0 or second > 60: raise ValueError("second out of range")

        if second == 60 and (hour != 23 or minute != 59):
            raise ValueError("second out of range")

        return struct

#-----------------------------------------------------------------------
HMS_TIME.setParseAction(PdsHmsTime.parse)
################################################################################
# PdsTimeZone (used only internally): value is a string representation
################################################################################
TIME_ZONE       = ("Z"
                ^ (SIGN
                 + UNSIGNED_INT
                 + Optional(Suppress(":") + UNSIGNED_INT)))
TIME_ZONE.setWhitespaceChars("")
TIME_ZONE.setName("TIME_ZONE")
#-----------------------------------------------------------------------

class PdsTimeZone(PdsValue):
    """Internally-used class to represent a time zone."""

    def __init__(self):
        PdsValue.__init__(self, "", TIME_ZONE)
        self.offset = 0         # minutes offset from GMT

    # Interpret parser tokens
    @staticmethod
    def parse(s, l, tokens):

        struct = PdsTimeZone()

        if tokens[0] == "Z":
            struct.value = "Z"
            struct.offset = 0
        else:
            struct.value = tokens[0] + tokens[1]
            struct.offset = 60 * int(tokens[1])

            if len(tokens) > 2:
                struct.value  += ":" + tokens[2]
                struct.offset += int(tokens[2])

            if tokens[0] == "-": struct.offset = -struct.offset

        return struct

#-----------------------------------------------------------------------
TIME_ZONE.setParseAction(PdsTimeZone.parse)
################################################################################
# PdsZonedTime
################################################################################
ZONED_TIME      = HMS_TIME + TIME_ZONE
ZONED_TIME.setWhitespaceChars("")
ZONED_TIME.setName("ZONED_TIME")
#-----------------------------------------------------------------------

class PdsZonedTime(PdsTime):
    """A time of day, including a time zone."""

    def __init__(self):
        PdsValue.__init__(self, "", ZONED_TIME)
        self.elapsed = 0.               # seconds elapsed since midnight GMT
        self.pdshms  = None             # PdsHmsTime object
        self.pdszone = None             # PdsTimeZone object

    def __str__(self):
        return str(self.pdshms) + str(self.pdszone)

    # Interpret parser tokens
    @staticmethod
    def parse(s, l, tokens):

        struct = PdsZonedTime()
        struct.pdshms  = tokens[0]
        struct.pdszone = tokens[1]

        struct.elapsed = struct.pdshms.elapsed - 60 * struct.pdszone.offset
        struct.value = str(struct)

        return struct

#-----------------------------------------------------------------------
ZONED_TIME.setParseAction(PdsZonedTime.parse)
#-----------------------------------------------------------------------
TIME_WO_WHITE   = ZONED_TIME | HMS_TIME                 # Order matters here!
TIME            = Suppress(Optional(WHITE)) + TIME_WO_WHITE
TIME.setName("TIME")
################################################################################
# PdsDate
################################################################################
DATE            = (Suppress(Optional(WHITE))
                +  UNSIGNED_INT
                +  Suppress("-")
                +  UNSIGNED_INT
                +  Optional(Suppress("-")
                          + UNSIGNED_INT))
DATE.setWhitespaceChars("")
DATE.setName("DATE")
#-----------------------------------------------------------------------

class PdsDate(PdsScalar):
    """A date as year, month and day or year and day-of-year."""

    def __init__(self):
        PdsValue.__init__(self, "", DATE)
        self.elapsed = 0        # days since January 1, 2000
        self.year  = 0          # year
        self.month = 0          # month number (0 for day-of-year format)
        self.day   = 0          # day of month
        self.date  = None       # date object from datetime module

    def __str__(self):
        if self.month:
            return ("%d"%self.year + "-" + "%02d"%self.month
                                   + "-" + "%02d"%self.day)
        else:
            return ("%d"%self.year + "-" + "%03d"%self.day)

    # Interpret parser tokens
    @staticmethod
    def parse(s, l, tokens):

        if len(tokens) == 2:
            struct = PdsDate.from_yd(int(tokens[0]), int(tokens[1]))
        else:
            struct = PdsDate.from_ymd(int(tokens[0]), int(tokens[1]),
                                                      int(tokens[2]))

        return struct

    @staticmethod
    def from_ymd(year, month, day):
        """Returns a new PdsDate given a year, month and day."""

        struct = PdsDate()

        struct.year = year
        struct.month = month
        struct.day = day

        struct.date = dt.date(year, month, day)
        struct.elapsed = (struct.date - dt.date(2000,1,1)).days
        struct.value = str(struct)

        return struct

    @staticmethod
    def from_yd(year, day):
        """Returns a new PdsDate given a year and day of year."""

        struct = PdsDate()

        struct.year = year
        struct.month = 0
        struct.day = day

        struct.date = dt.date(struct.year, 1, 1) + dt.timedelta(struct.day - 1)
        struct.elapsed = (struct.date - dt.date(2000,1,1)).days
        struct.value = str(struct)

        return struct

#-----------------------------------------------------------------------
DATE.setParseAction(PdsDate.parse)
################################################################################
# PdsDateTime
################################################################################
DATE_TIME       = (Suppress(Optional(WHITE))
                +  DATE
                +  Suppress(oneOf("T t"))
                +  TIME_WO_WHITE)
DATE_TIME.setWhitespaceChars("")
DATE_TIME.setName("DATE_TIME")
#-----------------------------------------------------------------------

class PdsDateTime(PdsScalar):

    def __init__(self):
        PdsValue.__init__(self, "", DATE_TIME)
        self.elapsed = 0.               # seconds since January 1, 2000, without
                                        # leapseconds
        self.pdsdate = None             # PdsDate object
        self.pdstime = None             # PdsTime object

    def __str__(self):
        return str(self.pdsdate) + "T" + str(self.pdstime)

    # Interpret parser tokens
    @staticmethod
    def parse(s, l, tokens):

        struct = PdsDateTime.from_dt(tokens[0], tokens[1])
        return struct

    @staticmethod
    def from_dt(pdsdate, pdstime):
        """Constructs a new PdsDateTime from PdsDate and PdsTime objects."""

        struct = PdsDateTime()

        struct.pdsdate = pdsdate
        struct.pdstime = pdstime

        struct.elapsed = pdsdate.value * 86400 + pdstime.value
        struct.value = str(struct)

        return struct

#-----------------------------------------------------------------------
DATE_TIME.setParseAction(PdsDateTime.parse)
################################################################################
# PdsText: value is the contents of the text string, quoted or not.
################################################################################
EMPTY_TEXT      = Combine('""')
NONEMPTY_TEXT   = Suppress('"') + Combine(CharsNotIn('"')) + Literal('"')
QUOTED_SYMBOL   = Suppress("'") + Combine(CharsNotIn("'\n")) + Literal("'")
UNQUOTED_TEXT   = Combine(IDENTIFIER)
TEXT_VALUE      = EMPTY_TEXT | NONEMPTY_TEXT | QUOTED_SYMBOL | UNQUOTED_TEXT
TEXT_VALUE.setName("TEXT_VALUE")
#-----------------------------------------------------------------------

class PdsText(PdsScalar):
    """A text string in single quotes, double quotes, or no quotes."""

    def __init__(self):
        PdsValue.__init__(self, "", TEXT_VALUE)
        self.quote = None       # Quote character surrounding the text, if any

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.quote + self.value + self.quote

    # Interpret parser tokens
    @staticmethod
    def parse(s, l, tokens):

        struct = PdsText()

        if len(tokens) == 1:
            if tokens[0] == '""':
                struct.value = ""
                struct.quote = '"'
            else:
                struct.value = tokens[0]
                struct.quote = ""

        else:
            struct.value = tokens[0]
            struct.quote = tokens[1]

        return struct

    @staticmethod
    def from_string(string, quote):
        """Return a new PdsText object containing the given string, which has
        been checked for suitability."""

        struct = PdsText()

        struct.value = string
        struct.quote = quote

        if quote not in " '\"": raise ValueError("illegal quote character")

        if quote != "" and quote in string:
            raise ValueError("text contains its own quote character")

        if quote == "" and " " in string:
            raise ValueError("unquoted text may not contain blanks")

        if quote != '"' and "\n" in string:
            raise ValueError("newline may not appear except in double-quotes")

        if quote != '"' and len(string) > 70:
            raise ValueError("long lines must be enclosed in double-quotes")

        # Strip \r from multi-line strings
        struct.value = "\n".join([s.strip("\r")
                               for s in struct.value.splitlines()])

        return struct

#-----------------------------------------------------------------------
TEXT_VALUE.setParseAction(PdsText.parse)
#-----------------------------------------------------------------------
PDS_SCALAR      = DATE_TIME | DATE | TIME | NUMBER | TEXT_VALUE # Order counts!
################################################################################
# PdsVector: value is a pointer to a 1-D or 2-D list structure.
################################################################################

class PdsVector(PdsValue):

    def __init__(self):
        PdsValue.__init__(self, [], VECTOR_VALUE)
        self.delim = ""         # "{}" for sets, "()" for 1-D arrays, "(())" for
                                # 2-D arrays.

    def __str__(self):
        list = [self.delim[0]]
        for v in self.value:
            list += [str(v), ", "]
        list[-1] = self.delim[-1]    # Replace final comma with a delimiter
        return "".join(list)

    def __repr__(self):
        list = [self.delim[0]]
        for v in self.value:
            list += [repr(v), ", "]
        list[-1] = self.delim[-1]    # Replace final comma with a delimiter
        return "".join(list)

    def __getitem__(self, key): return self.value[key]

    def __len__(self): return len(self.value)

################################################################################
# PdsSet
################################################################################
LBRACE          = Suppress(Literal("{"))
RBRACE          = Suppress(Literal("}"))
EMPTY_SET       = (Suppress(LBRACE) + ZeroOrMore(EOL) + Suppress(RBRACE))

NONEMPTY_SET    = (LBRACE                   + ZeroOrMore(EOL)
                +  PDS_SCALAR               + ZeroOrMore(EOL)
                +  ZeroOrMore(Suppress(Literal(","))
                                            + ZeroOrMore(EOL)
                                            + PDS_SCALAR
                                            + ZeroOrMore(EOL))
                +  RBRACE)
SET_VALUE       = EMPTY_SET | NONEMPTY_SET
SET_VALUE.setName("SET_VALUE")
#-----------------------------------------------------------------------

class PdsSet(PdsVector):
    """A set of scalar values in curly braces {}."""

    def __init__(self):
        PdsValue.__init__(self, [], SET_VALUE)
        self.delim = "{}"

    # Interpret parser tokens
    @staticmethod
    def parse(s, l, tokens):
        struct = PdsSet()
        struct.value = list(tokens)
        return struct

#-----------------------------------------------------------------------
SET_VALUE.setParseAction(PdsSet.parse)
################################################################################
# PdsSequence
################################################################################
LPAREN          = Suppress(Literal("("))
RPAREN          = Suppress(Literal(")"))
SEQUENCE        = (LPAREN                   + ZeroOrMore(EOL)
                +  PDS_SCALAR               + ZeroOrMore(EOL)
                +  ZeroOrMore(Suppress(Literal(","))
                                            + ZeroOrMore(EOL)
                                            + PDS_SCALAR
                                            + ZeroOrMore(EOL))
                +  RPAREN)
SEQUENCE.setName("SEQUENCE")
#-----------------------------------------------------------------------

class PdsSequence(PdsVector):
    """A 1-D set of scalar values in parentheses."""

    def __init__(self):
        PdsValue.__init__(self, [], SEQUENCE)
        self.delim = "()"

    # Interpret parser tokens
    @staticmethod
    def parse(s, l, tokens):
        struct = PdsSequence()
        struct.value = list(tokens)
        return struct

#-----------------------------------------------------------------------
SEQUENCE.setParseAction(PdsSequence.parse)
################################################################################
# PdsSequence2D
################################################################################
SEQUENCE_2D     = (LPAREN                   + ZeroOrMore(EOL)
                +  SEQUENCE                 + ZeroOrMore(EOL)
                +  ZeroOrMore(Suppress(Literal(","))
                                            + ZeroOrMore(EOL)
                                            + SEQUENCE
                                            + ZeroOrMore(EOL))
                +  RPAREN)
SEQUENCE_2D.setName("SEQUENCE_2D")
#-----------------------------------------------------------------------

class PdsSequence2D(PdsVector):
    """A 2-D set of scalar values in nested parentheses."""

    def __init__(self):
        PdsValue.__init__(self, [], SEQUENCE_2D)
        self.delim = "(())"

    # Interpret parser tokens
    @staticmethod
    def parse(s, l, tokens):
        struct = PdsSequence2D()
        struct.value = list(tokens)
        return struct

#-----------------------------------------------------------------------
SEQUENCE_2D.setParseAction(PdsSequence2D.parse)
#-----------------------------------------------------------------------
VECTOR_VALUE    = SET_VALUE | SEQUENCE | SEQUENCE_2D
#-----------------------------------------------------------------------
PDS_VALUE       = VECTOR_VALUE | PDS_SCALAR     # Order counts, no pointers!
################################################################################
################################################################################
# PdsPointer
################################################################################
################################################################################

class PdsPointer(PdsValue):
    """The general class describing simple pointers and pointers with
    offsets."""

################################################################################
# PdsSimplePointer
################################################################################
FILENAME        = Combine(Word(alphanums + "_")
                        + OneOrMore("." + Word(alphanums + "_")))
FILENAME.setName("FILENAME")

SIMPLE_POINTER  = (Suppress(Optional(WHITE))
                +  Suppress('"')
                +  FILENAME
                +  Suppress('"'))
SIMPLE_POINTER.setWhitespaceChars("")
SIMPLE_POINTER.setName("SIMPLE_POINTER")
#-----------------------------------------------------------------------

class PdsSimplePointer(PdsPointer):

    def __init__(self):
        PdsValue.__init__(self, "", SIMPLE_POINTER)

    def __str__(self): return '"' + self.value + '"'

    @staticmethod
    def parse(s, l, tokens):
        struct = PdsSimplePointer()
        struct.value = tokens[0]
        return struct

#-----------------------------------------------------------------------
SIMPLE_POINTER.setParseAction(PdsSimplePointer.parse)
################################################################################
# PdsOffsetPointer
################################################################################
BYTE_UNIT       = Literal("<BYTES>") | Literal("<bytes>")
ROW_OFFSET      = Combine(UNSIGNED_INT)
BYTE_OFFSET     = ROW_OFFSET + ZeroOrMore(EOL) + BYTE_UNIT

BYTE_UNIT.setParseAction(PdsUnitExpr.parse)
ROW_OFFSET.setParseAction(PdsInteger.parse)
BYTE_OFFSET.setParseAction(PdsNumberWithUnits.parse)
#-----------------------------------------------------------------------
OFFSET_POINTER  = (LPAREN                       + ZeroOrMore(EOL)
                +  SIMPLE_POINTER               + ZeroOrMore(EOL)
                +  Suppress(",")                + ZeroOrMore(EOL)
                +  (BYTE_OFFSET | ROW_OFFSET)   + ZeroOrMore(EOL)
                +  RPAREN)
OFFSET_POINTER.setName("OFFSET_POINTER")
#-----------------------------------------------------------------------

class PdsOffsetPointer(PdsPointer):

    def __init__(self):
        PdsValue.__init__(self, "", OFFSET_POINTER)
        self.offset = 0                 # numeric offset in rows or bytes
        self.unit = "ROWS"              # Unit of offset
        self.pdspointer = None          # Associated PdsSimplePointer
        self.pdsnumber = None           # Associated offset, perhaps with units

    def __str__(self):
        return "(" + str(self.pdspointer) + ", " + str(self.pdsnumber) + ")"

    @staticmethod
    def parse(s, l, tokens):

        struct = PdsOffsetPointer()
        struct.pdspointer = tokens[0]
        struct.pdsnumber = tokens[1]

        struct.value = tokens[0].value
        struct.offset = tokens[1].value

        if isinstance(tokens[1], PdsNumberWithUnits): struct.unit = "BYTES"

        return struct

#-----------------------------------------------------------------------
OFFSET_POINTER.setParseAction(PdsOffsetPointer.parse)
################################################################################
# PdsLocalPointer
################################################################################
LOCAL_POINTER   = BYTE_OFFSET | ROW_OFFSET
LOCAL_POINTER.setName("LOCAL_POINTER")
#-----------------------------------------------------------------------

class PdsLocalPointer(PdsPointer):

    def __init__(self):
        PdsValue.__init__(self, "", LOCAL_POINTER)
        self.offset = 0                 # numeric offset in rows or bytes
        self.unit = "ROWS"              # Unit of offset
        self.pdsnumber = None           # Associated offset, perhaps with units

    def __str__(self):
        return str(self.pdsnumber)

    @staticmethod
    def parse(s, l, tokens):
        struct = PdsLocalPointer()
        struct.pdsnumber = tokens[0]
        struct.value = tokens[0].value
        if isinstance(tokens[0], PdsNumberWithUnits): self.unit = "BYTES"

        return struct

#-----------------------------------------------------------------------
#LOCAL_POINTER.setParseAction(PdsLocalPointer.parse)
#-----------------------------------------------------------------------
POINTER_VALUE   = SIMPLE_POINTER | OFFSET_POINTER | LOCAL_POINTER
POINTER_VALUE.setName("POINTER_VALUE")
################################################################################
################################################################################
# PdsKeyword
################################################################################
################################################################################

class PdsKeyword(PdsItem):
    """The abstract class for anything on the left of an equal sign."""

    def __init__(self, pointer_char=""):
        self.name = ""                      # Name of the attribute
        self.namespace = ""                 # Optional namespace
        self.pointer_char = pointer_char    # Optional pointer indicator

    def __str__(self):
        if self.namespace:
            return self.pointer_char + self.namespace + ":" + self.name
        else:
            return self.pointer_char + self.name

################################################################################
# PdsAttributeID
################################################################################
SINGLE_ATTR_ID  = Combine(IDENTIFIER)

DOUBLE_ATTR_ID  = (Suppress(Optional(WHITE))
                +  IDENTIFIER
                +  Suppress(":")
                +  IDENTIFIER)
DOUBLE_ATTR_ID.setWhitespaceChars("")

ATTRIBUTE_ID    = DOUBLE_ATTR_ID | SINGLE_ATTR_ID               # Order counts
ATTRIBUTE_ID.setName("ATTRIBUTE_ID")
#-----------------------------------------------------------------------

class PdsAttributeID(PdsKeyword):
    """This class represents a simple attribute with option namespace
    prefix."""

    def __init__(self):
        PdsKeyword.__init__(self)

    # Interpret parser tokens
    @staticmethod
    def parse(s, l, tokens):

        struct = PdsAttributeID()
        struct.name = tokens[-1]

        if len(tokens) == 2: struct.namespace = tokens[0]

        return struct

#-----------------------------------------------------------------------
ATTRIBUTE_ID.setParseAction(PdsAttributeID.parse)
################################################################################
# PdsPointerID
################################################################################
POINTER_ID      = Suppress(Optional(WHITE) + Literal("^")) + ATTRIBUTE_ID
POINTER_ID.setWhitespaceChars("")
POINTER_ID.setName("POINTER_ID")
#-----------------------------------------------------------------------

class PdsPointerID(PdsKeyword):
    """This class represents a pointer."""

    def __init__(self):
        PdsKeyword.__init__(self, pointer_char="^")

    # Interpret parser tokens
    @staticmethod
    def parse(s, l, tokens):
        struct = PdsPointerID()
        struct.name = tokens[0].name
        struct.namespace = tokens[0].namespace
        struct.value = str(struct)

        return struct

#-----------------------------------------------------------------------
POINTER_ID.setParseAction(PdsPointerID.parse)
################################################################################
################################################################################
# Statements
################################################################################
################################################################################
POINTER_STMT    = (POINTER_ID           + ZeroOrMore(EOL)
                + Suppress("=")         + ZeroOrMore(EOL)
                + POINTER_VALUE         + OneOrMore(EOL))

ATTRIBUTE_STMT  = (ATTRIBUTE_ID         + ZeroOrMore(EOL)
                + Suppress("=")         + ZeroOrMore(EOL)
                + PDS_VALUE             + OneOrMore(EOL))

STATEMENT       = (POINTER_STMT | ATTRIBUTE_STMT)
STATEMENT.setName("STATEMENT")
STATEMENT.setParseAction(PdsNode.parse)

END_STATEMENT   = Suppress(Literal("END") + ZeroOrMore(NEWLINE))
END_STATEMENT.setParseAction(PdsNode.parse_end)
#-----------------------------------------------------------------------
PDS_LABEL       = OneOrMore(STATEMENT) + END_STATEMENT
################################################################################
# PdsLabel
################################################################################

class PdsLabel():
    """This class represents the entire contents of a PDS label."""

    def __init__(self):
        self.filename = ""      # The source of the label
        self.string = ""        # The complete contents of the label as read
        self.root = None        # The root node of the parse tree

    def __str__(self): return self.root.__str__()

    def __repr__(self): return str(self)

    def __getitem__(self, key): return self.root[key]

    def __len__(self): return len(self.root)

    @staticmethod
    def from_file(filename):
        """Loads and parses a PDS label."""

        lines = PdsLabel.load_file(filename)
        return PdsLabel.from_string(lines)

    @staticmethod
    def load_file(filename):
        """Loads a PDS label, returning a list of strings, one for each line.
        """

        # Open file for read; could be binary
        file = open(filename, "rb")

        # Create a list of lines
        lines = []
        quotes = 0              #...while counting quotes
        for line in file:

            # An empty string means end of file
            if line == "": raise SyntaxError("Missing END statement")

            # Remove the line terminators from each line
            line = line.strip("\r\n")
            lines.append(line)

            # Look for the END statement, but only outside quotes
            if quotes%2 == 0:
                if line == "END" or line[0:4] == "END ": break

            # Update the quote count
            quotes += line.count('"')

        # Close the file
        file.close()

        return lines

    @staticmethod
    def from_string(string):
        """Parses a string or list of strings containing the contents of a PDS
        label."""

        global PARSE_NODES

        this = PdsLabel()
        this.filename = None

        # If this is a list, concatenate the lines into a string
        if type(string) == type([]):
            string = "\n".join(string) + "\n"

        # Initialize the object status in the parsed label
        PdsNode.init_current_node()

        # Parse the label
        this.label = PDS_LABEL.parseString(string).asList()
        this.root = PARSE_NODES[0]

        return this

    @staticmethod
    def FromFile(filename):
        """Deprecated alternative name for from_file()"""

        return from_file(filename)

################################################################################
# Test program
################################################################################

def test2():

#     str(PDS_VALUE.parseString(" {\"17010011010101110\",3 <hh>} "))[0]
#    foo = PDS_VALUE.parseString(" ( (1, /* dfsdf */ \n /* more*/ \n2),/*  */\n (3))")
    foo = ATTRIBUTE_STMT.parseString(" A = 123 /* comment */ \n /* dddd */  \n")
#   foo = STATEMENT.parseString(" ^A= ( \"A.b\", 4 <bytes>) \n")
#    foo = POINTER_VALUE.parseString("(\"a.b\", 55 <bytes> )")
#   foo = EOL.parseString(" /* aa bb gifhfi   \n")

# Test program
def test():

    result = PdsLabel.FromFile("test.lbl")

#    result.PrintLabel()
    print result.nodename

    test = result.GetSubnode("IMAGE")
    print test.nodename
    test.PrintLabel()

    print test["LINE_SAMPLES"]
    print test["HORIZONTAL_PIXEL_FOV"]
    print result["START_TIME"]
    print result["IMAGE_TIME"]
    print result["^IMAGE"]

    print result["mask"]
    print result["oned"]
    print result["twod"]

# Execute the main test progam if this is not imported
if __name__ == "__main__": test()

