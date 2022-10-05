################################################################################
# julian_dateparser.py
#
# This is a set of routines for parsing dates and times. It is a component of
# the Julian Library and is not really intended to be invoked separately,
# although it can be.
#
# Date grammars:
#
#   YMD_PREF_DATE   parses a date string, in which ambiguous dates are
#                   interpreted in year, month, day order first. "07/08/09" is
#                   interpreted as August 9, 2007.
#
#   MDY_PREF_DATE   same as above, but the favored order is month, day, year.
#                   "07/08/09" is July 8, 2009.
#
#   DMY_PREF_DATE   same as above, but the favored order is day, month, year.
#                   "07/08/09" is August 7, 2009.
#
#   DATE            equivalent to YMD_PREF_DATE.
#
# The components of a date can be separated by dashes, slashes, dots, or white
# space. In the case of white space, a comma can separate certain fields. Months
# can be names or numbers, possibly abbreviated. The date can begin with a
# weekday, which may also be abbreviated. The date can also be specified as a
# year and day-of-year.
#
# Alternatively, the date may be expressed as "MJD" followed by a Modified
# Julian day number.
#
# We also define "strict" grammars, which are similar to the above but go by the
# names YMD_PREF_DATE_STRICT, MDY_PREF_DATE_STRICT, DMY_PREF_DATE_STRICT, and
# DATE_STRICT. These can be used more reliably when seeking dates embedded
# within text strings; they are less likely to mis-identify random text or
# numbers as a date. For example, they do not recognize year/day-of-year
# formats.
#

#
# Time grammars:
#
#   TIME        a time string indicating the time into a day. Allowed formats
#               are:
#                   <hour>:<minute>:<second> [am|pm]
#                   <hour>:<minute> [am|pm|Z]
#                   <hours> H
#                   <minutes> M
#                   <seconds> S
#
#   TYPED_TIME  as above, but with an optional suffix of Z, UT, UTC, TAI, TDB,
#               ET, or TDT.
#
# The am/pm suffix is optional and implies a 12-hour clock; otherwise, a 24-hour
# clock is assumed. Seconds can have a fractional component. If seconds are not
# included, then the mintes can have a fractional component. The time can also
# be expressed exclusively in terms of hours, minutes or seconds, where a
# suffix "H", "M" or "S" indicates which. Time zones are not supported; all
# times are assumed GMT. An optional Z suffix indicates "Zulu" time (GMT) but is
# ignored.
#
# We also define "strict" grammars, which are similar to the above but go by the
# names TIME_STRICT, and TYPED_TIME_STRICT. These can be used more reliably when
# seeking dates embedded within text strings; they are less likely to
# mis-identify random text or numbers as a time.
#
# The seconds component at the end of a day can go as high as 69 to account for
# possible leap seconds.
#
# Date-time grammars:
#
#   YMD_PREF_DATETIME   a string integrating a date and time, using YMD
#                       preferred ordering.
#
#   MDY_PREF_DATETIME   same as above, but favoring month-day-year ordering.
#
#   DMY_PREF_DATETIME   same as above, but favoring day-month-year ordering.
#
#   DATETIME            same as YMD_PREF_DATETIME.
#
# The time can come before or after the date. The separator must be white space
# or a comma, colon, dash or slash. In the special case of yyyy-mm-dd or
# yyyy-ddd date formats, the separator can be a "T" to conform to ISO date
# format standards.
#
# As a special case, the date-time grammars also accept a date string with no
# time. In year-month-day or year-day formats, the day can be fractional in this
# case; otherwise the time is interpreted as midnight.
#
# Date-times can also have a suffix "TDB", "TDT", "TAI", "UTC", "UT" or "Z" to
# indicate the time system. Here, ET is treated as an alias for TDB, and UT and
# Z are aliases for UTC.
#
# Alternatively, the date and time can be expressed as a number, with explicit
# units of "JD", "MJD", "JED", "MJED", "ET", "TDB", "TDT", or "TAI". These units
# can appear before or after the number.
#
# The parsers return a list of 2-item lists, where the first item is the name
# of a component and the second is its value. The names are "YEAR", "MONTH",
# "DAY" and optional "WEEKDAY" for dates, "HOUR", "MINUTE" and "SECOND" for
# times. Numeric values can be integer or float, depending on what the string
# contained. Weekdays are given as upper case strings, abbreviated to three
# characters. "TYPE" indicates the time type if present; it is always one of
# "TDB", "TDT", "TAI" or "UTC". Numeric date-times are defined by a "UNIT" (one
# of "MJD", "JD", "MJED", "JED", "TAI", "ET", "TDB", or "TDT") and "NUMBER", a
# floating-point value.
#
# We also define "strict" grammars, which are similar to the above but go by the
# names YMD_PREF_DATETIME_STRICT, MDY_PREF_DATETIME_STRICT,
# DMY_PREF_DATETIME_STRICT, and DATE_STRICT. These can be used more reliably
# when seeking dates embedded within text strings; they are less likely to
# mis-identify random text or numbers as a date.
#
# Mark R. Showalter
# PDS Ring-Moon Systems Node, SETI Institute
# This software is licensed under Academic Free License ("AFL") v. 3.0.
# See https://opensource.org/licenses/afl-3.0.php
################################################################################

from pyparsing import *
import unittest

################################################################################
# BEGIN GRAMMAR
################################################################################

# Whitespace is ignored by default
ParserElement.setDefaultWhitespaceChars(" \t")

# Useful definitions...
SLASH           = Suppress(Literal("/"))
DASH            = Suppress(Literal("-"))
DOT             = Suppress(Literal("."))
COMMA           = Suppress(Literal(","))
COLON           = Suppress(Literal(":"))

WHITE           = Suppress(White())

################################################################################
# Integers with limited ranges
################################################################################
# A number 1-9
NONZERO         = srange("[1-9]")

# Useful definitions, used below
# Note that the order of options is critical here, because the "|" operator
# stops when it encounters its first match.

# A number 0-23, possibly zero-padded to 2 digits
ZERO_23_2DIGIT  = (   Word("01",nums,exact=2)
                    | Word("2","0123",exact=2)
                  ) + WordEnd(nums)

ZERO_23         = ZERO_23_2DIGIT | (Word(nums,exact=1) + WordEnd(nums))

# A number 0-59, possibly zero-padded to 2 digits
ZERO_59_2DIGIT  = Word("012345",nums,exact=2) + WordEnd(nums)
ZERO_59         = ZERO_59_2DIGIT | (Word(nums,exact=1) + WordEnd(nums))

# A number 0-1443, possibly zero-padded to 4 digits. 1440 minutes in a day.
ZERO_1439       = (   Word("0",nums,exact=4)
                    | Combine("1"  + Word("0123",nums,exact=3))
                    | Combine("14" + Word("0123",nums,exact=2))
                    | Word(NONZERO,nums,min=1,max=3)
                    | Keyword("0")
                  ) + WordEnd(nums)

# A number 0-86399, possibly zero-padded to 5 digits. 86400 seconds in a day.
ZERO_86399      = (   Word("0",nums,exact=5)
                    | Word("1234567",nums,exact=5)
                    | Combine("8"   + Word("012345",nums,exact=4))
                    | Combine("86"  + Word("0123",  nums,exact=3))
                    | Word(NONZERO,nums,min=1,max=4)
                    | Literal("0")
                  ) + WordEnd(nums)

# A number 1-12, possibly zero-padded to 2 digits.
ONE_12_2DIGIT   = (   Word("0",NONZERO,exact=2)
                    | Word("1","012",exact=2)
                  ) + WordEnd(nums)
ONE_12          = ONE_12_2DIGIT | (Word(NONZERO,exact=1) + WordEnd(nums))

# A number 1-31, possibly zero-padded to 2 digits.
ONE_31_2DIGIT   = (   Word("0",NONZERO,exact=2)
                    | Word("12",nums,exact=2)
                    | Word("3","01",exact=2)
                  ) + WordEnd(nums)
ONE_31          = ONE_31_2DIGIT | (Word(NONZERO,exact=1) + WordEnd(nums))

# A number 1-366, possibly zero-padded to 3 digits.
ONE_366_3DIGIT  = (   Combine(Literal("00") + Word(NONZERO,exact=1))
                    | Combine(Literal("0")  + Word(NONZERO,nums,exact=2))
                    | Word("12",nums,exact=3)
                    | Combine(Literal("3")  + Word("012345",nums,exact=2))
                    | Combine(Literal("36") + Word("0123456",exact=1))
                  ) + WordEnd(nums)
# This appears to have stopped working in Python 3.9 and 3.10
# ONE_366         = (ONE_366_3DIGIT |
#                     (Word(NONZERO,nums,max=2) + WordEnd(nums)))
ONE_366         = (ONE_366_3DIGIT |
                    (Word(NONZERO,exact=1) + WordEnd(nums)) |
                    (Word(NONZERO,nums,exact=2) + WordEnd(nums)))

# A number 60-69. For possible additional leapseconds at the end of a day.
SIXTY_69        = Combine("6" + Word(nums,exact=1)) + WordEnd(nums)

# A number 86400-86409. For possible additional leapseconds at the end of a day.
N86400_86409    = Combine("8640" + Word(nums,exact=1)) + WordEnd(nums)

########################################
# UNIT TESTS
########################################

class Test_Basics(unittest.TestCase):

    def runTest(self):

        # ZERO_23 matches
        parser = ZERO_23
        self.assertEqual(parser.parseString(" 0").asList()[0],   "0")
        self.assertEqual(parser.parseString("1 ").asList()[0],   "1")
        self.assertEqual(parser.parseString(" 23 ").asList()[0], "23")
        self.assertEqual(parser.parseString("00").asList()[0],   "00")
        self.assertEqual(parser.parseString("0a").asList()[0],   "0")
        for num in range(00, 24):
            self.assertEqual(parser.parseString(str(num)).asList()[0], str(num))

        # ...cannot complete match
        self.assertEqual(parser.parseString("0.1").asList()[0],  "0")
        self.assertEqual(parser.parseString("22a").asList()[0], "22")

        # ...doesn't recognize
        self.assertRaises(ParseException, parser.parseString, "24")
        self.assertRaises(ParseException, parser.parseString, "023")
        self.assertRaises(ParseException, parser.parseString, "222")
        self.assertRaises(ParseException, parser.parseString, "a")
        self.assertRaises(ParseException, parser.parseString, " ")
        self.assertRaises(ParseException, parser.parseString, "")
        self.assertRaises(ParseException, parser.parseString, ".1")

        # ZERO_59 matches
        parser = ZERO_59
        self.assertEqual(parser.parseString(" 0").asList()[0],   "0")
        self.assertEqual(parser.parseString("1 ").asList()[0],   "1")
        self.assertEqual(parser.parseString(" 59 ").asList()[0], "59")
        self.assertEqual(parser.parseString("00").asList()[0],   "00")
        for num in range(00, 60):
            self.assertEqual(parser.parseString(str(num)).asList()[0], str(num))

        # ...cannot complete match
        self.assertEqual(parser.parseString("0.1").asList()[0], "0")
        self.assertEqual(parser.parseString("0a").asList()[0],  "0")

        # ...doesn't recognize
        self.assertRaises(ParseException, parser.parseString, "60")
        self.assertRaises(ParseException, parser.parseString, "059")
        self.assertRaises(ParseException, parser.parseString, "a")
        self.assertRaises(ParseException, parser.parseString, " ")
        self.assertRaises(ParseException, parser.parseString, "")
        self.assertRaises(ParseException, parser.parseString, ".1")


        # ZERO_1439 matches
        parser = ZERO_1439
        self.assertEqual(parser.parseString("0 ").asList()[0],    "0")
        self.assertEqual(parser.parseString(" 1").asList()[0],    "1")
        self.assertEqual(parser.parseString("12 ").asList()[0],   "12")
        self.assertEqual(parser.parseString("123" ).asList()[0],  "123")
        self.assertEqual(parser.parseString("1234 ").asList()[0], "1234")
        self.assertEqual(parser.parseString("1439").asList()[0],  "1439")
        self.assertEqual(parser.parseString("0439").asList()[0],  "0439")
        self.assertEqual(parser.parseString("0000").asList()[0],  "0000")
        for num in range(00, 1440):
            self.assertEqual(parser.parseString(str(num)).asList()[0], str(num))

        # ...cannot complete match
        self.assertEqual(parser.parseString("1439.").asList()[0], "1439")
        self.assertEqual(parser.parseString("143aa").asList()[0], "143")

        # ...doesn't recognize
        self.assertRaises(ParseException, parser.parseString, "1440")
        self.assertRaises(ParseException, parser.parseString, "012")
        self.assertRaises(ParseException, parser.parseString, "01")
        self.assertRaises(ParseException, parser.parseString, " ")
        self.assertRaises(ParseException, parser.parseString, "a")
        self.assertRaises(ParseException, parser.parseString, "")
        self.assertRaises(ParseException, parser.parseString, ".1")

        # ZERO_86399 matches
        parser = ZERO_86399
        self.assertEqual(parser.parseString(" 0").asList()[0],      "0")
        self.assertEqual(parser.parseString("1 ").asList()[0],      "1")
        self.assertEqual(parser.parseString(" 86 ").asList()[0],    "86")
        self.assertEqual(parser.parseString(" 863 ").asList()[0],   "863")
        self.assertEqual(parser.parseString(" 8639 ").asList()[0],  "8639")
        self.assertEqual(parser.parseString(" 86399 ").asList()[0], "86399")
        for num in range(00, 86400):
            self.assertEqual(parser.parseString(str(num)).asList()[0], str(num))

        # ...cannot complete match
        self.assertEqual(parser.parseString("86399a").asList()[0], "86399")
        self.assertEqual(parser.parseString("86399.").asList()[0], "86399")
        self.assertEqual(parser.parseString("863 99").asList()[0], "863")

        # ...doesn't recognize
        self.assertRaises(ParseException, parser.parseString, "86400")
        self.assertRaises(ParseException, parser.parseString, "863990")
        self.assertRaises(ParseException, parser.parseString, " ")
        self.assertRaises(ParseException, parser.parseString, "a")
        self.assertRaises(ParseException, parser.parseString, "")
        self.assertRaises(ParseException, parser.parseString, ".1")

        # ONE_12 matches
        parser = ONE_12
        self.assertEqual(parser.parseString("1 ").asList()[0],   "1")
        self.assertEqual(parser.parseString(" 12 ").asList()[0], "12")
        self.assertEqual(parser.parseString("01").asList()[0],   "01")
        for num in range(1, 13):
            self.assertEqual(parser.parseString(str(num)).asList()[0], str(num))

        # ...cannot complete match
        self.assertEqual(parser.parseString("1a").asList()[0],  "1")
        self.assertEqual(parser.parseString("12a").asList()[0], "12")
        self.assertEqual(parser.parseString("1 2").asList()[0], "1")

        # ...doesn't recognize
        self.assertRaises(ParseException, parser.parseString, "13")
        self.assertRaises(ParseException, parser.parseString, "121")
        self.assertRaises(ParseException, parser.parseString, "0")
        self.assertRaises(ParseException, parser.parseString, "00")
        self.assertRaises(ParseException, parser.parseString, "")
        self.assertRaises(ParseException, parser.parseString, " ")
        self.assertRaises(ParseException, parser.parseString, "a")
        self.assertRaises(ParseException, parser.parseString, ".1")

        # ONE_31 matches
        parser = ONE_31
        self.assertEqual(parser.parseString("1 ").asList()[0],   "1")
        self.assertEqual(parser.parseString(" 31 ").asList()[0], "31")
        self.assertEqual(parser.parseString("01").asList()[0],   "01")
        for num in range(1, 32):
            self.assertEqual(parser.parseString(str(num)).asList()[0], str(num))

        # ...cannot complete match
        self.assertEqual(parser.parseString("3 1").asList()[0],  "3")
        self.assertEqual(parser.parseString("3a1").asList()[0],  "3")
        self.assertEqual(parser.parseString("1a").asList()[0],   "1")
        self.assertEqual(parser.parseString("31a").asList()[0],  "31")
        self.assertEqual(parser.parseString("3.5").asList()[0], "3")

        # ...doesn't recognize
        self.assertRaises(ParseException, parser.parseString, "32")
        self.assertRaises(ParseException, parser.parseString, "0")
        self.assertRaises(ParseException, parser.parseString, "00")
        self.assertRaises(ParseException, parser.parseString, "310")
        self.assertRaises(ParseException, parser.parseString, " ")
        self.assertRaises(ParseException, parser.parseString, "a")
        self.assertRaises(ParseException, parser.parseString, "0.5")

        # ONE_366 matches
        parser = ONE_366
        self.assertEqual(parser.parseString("1 ").asList()[0],   "1")
        self.assertEqual(parser.parseString(" 36 ").asList()[0], "36")
        self.assertEqual(parser.parseString("366").asList()[0],  "366")
        self.assertEqual(parser.parseString("001").asList()[0],  "001")
        self.assertEqual(parser.parseString("010").asList()[0],  "010")
        for num in range(1, 367):
            self.assertEqual(parser.parseString(str(num)).asList()[0], str(num))

        # ...cannot complete match
        self.assertEqual(parser.parseString("1a").asList()[0],   "1")
        self.assertEqual(parser.parseString("36a").asList()[0],  "36")
        self.assertEqual(parser.parseString("3 6").asList()[0],  "3")
        self.assertEqual(parser.parseString("3a6").asList()[0],  "3")
        self.assertEqual(parser.parseString("36,6").asList()[0], "36")
        self.assertEqual(parser.parseString("36.5").asList()[0], "36")

        # ...doesn't recognize
        self.assertRaises(ParseException, parser.parseString, "367")
        self.assertRaises(ParseException, parser.parseString, "0")
        self.assertRaises(ParseException, parser.parseString, "00")
        self.assertRaises(ParseException, parser.parseString, "000")
        self.assertRaises(ParseException, parser.parseString, "01")
        self.assertRaises(ParseException, parser.parseString, "0366")
        self.assertRaises(ParseException, parser.parseString, " ")
        self.assertRaises(ParseException, parser.parseString, "a")
        self.assertRaises(ParseException, parser.parseString, ".5")

        # SIXTY_69 matches
        parser = SIXTY_69
        self.assertEqual(parser.parseString("60 ").asList()[0],  "60")
        self.assertEqual(parser.parseString(" 69").asList()[0],  "69")
        for num in range(60, 70):
            self.assertEqual(parser.parseString(str(num)).asList()[0], str(num))

        # ...cannot complete match
        self.assertEqual(parser.parseString("60.0").asList()[0], "60")
        self.assertEqual(parser.parseString("60a").asList()[0],  "60")

        # ...doesn't recognize
        self.assertRaises(ParseException, parser.parseString, "59")
        self.assertRaises(ParseException, parser.parseString, "70")
        self.assertRaises(ParseException, parser.parseString, "600")
        self.assertRaises(ParseException, parser.parseString, "a")
        self.assertRaises(ParseException, parser.parseString, "6")
        self.assertRaises(ParseException, parser.parseString, "6 0")

        # N86400_86409 matches
        parser = N86400_86409
        self.assertEqual(parser.parseString(" 86400").asList()[0],  "86400")
        self.assertEqual(parser.parseString("86409 ").asList()[0],  "86409")
        self.assertEqual(parser.parseString("86409a").asList()[0],  "86409")
        self.assertEqual(parser.parseString("86409.5").asList()[0], "86409")
        for num in range(86400, 86410):
            self.assertEqual(parser.parseString(str(num)).asList()[0], str(num))

        # ...doesn't recognize
        self.assertRaises(ParseException, parser.parseString, " ")
        self.assertRaises(ParseException, parser.parseString, "a")
        self.assertRaises(ParseException, parser.parseString, "1")
        self.assertRaises(ParseException, parser.parseString, "12")
        self.assertRaises(ParseException, parser.parseString, "123")
        self.assertRaises(ParseException, parser.parseString, "1234")
        self.assertRaises(ParseException, parser.parseString, "12345")
        self.assertRaises(ParseException, parser.parseString, "123456")
        self.assertRaises(ParseException, parser.parseString, "864a09")
        self.assertRaises(ParseException, parser.parseString, "86 409")

################################################################################
# YEAR
#
# Preferably a 4-digit number beginning with 1 or 2
# Can be a 2-digit number, which is assumed to fall between 1970 and 2069.
################################################################################

YEAR_4DIGIT     = Word("12",nums,exact=4)
YEAR_2DIGIT     = Word(nums,exact=2)

# Parse actions save a list pair ["YEAR", number]
YEAR_4DIGIT.setParseAction(lambda s,l,t: [["YEAR", int(t[0])],
                                          ['~', l+len(t[0])]])
YEAR_2DIGIT.setParseAction(lambda s,l,t: [["YEAR", 2000 + int(t[0])
                                                   - 100 * (int(t[0])//70)],
                                          ['~', l+len(t[0])]])
# Two-digit years are interpreted as 1970-2069

YEAR            = (YEAR_4DIGIT | YEAR_2DIGIT) + WordEnd(nums)

########################################
# UNIT TESTS
########################################

class Test_YEAR(unittest.TestCase):

    def runTest(self):

        parser = YEAR

        # Matches...
        self.assertEqual(parser.parseString(" 2000 ")[0], ["YEAR",2000])
        self.assertEqual(parser.parseString(" 00 ")[0],   ["YEAR",2000])
        self.assertEqual(parser.parseString(" 70 ")[0],   ["YEAR",1970])
        self.assertEqual(parser.parseString(" 69 ")[0],   ["YEAR",2069])

        # ...cannot complete match
        self.assertEqual(parser.parseString("2000a ")[0], ["YEAR",2000])

        # Doesn't recognize...
        self.assertRaises(ParseException, parser.parseString, "3000")
        self.assertRaises(ParseException, parser.parseString, "0300")
        self.assertRaises(ParseException, parser.parseString, " ")
        self.assertRaises(ParseException, parser.parseString, "a")
        self.assertRaises(ParseException, parser.parseString, "0")
        self.assertRaises(ParseException, parser.parseString, "000")

################################################################################
# MONTH
#
# Option #1: A case-insensitive month name, possibly abbreviated to 3 letters.
# Option #2: A number 1-12, optionally zero-padded to 2 digits.
################################################################################

NAMED_JAN = CaselessKeyword("JAN") | CaselessKeyword("JANUARY")
NAMED_FEB = CaselessKeyword("FEB") | CaselessKeyword("FEBRUARY")
NAMED_MAR = CaselessKeyword("MAR") | CaselessKeyword("MARCH")
NAMED_APR = CaselessKeyword("APR") | CaselessKeyword("APRIL")
NAMED_MAY = CaselessKeyword("MAY")
NAMED_JUN = CaselessKeyword("JUN") | CaselessKeyword("JUNE")
NAMED_JUL = CaselessKeyword("JUL") | CaselessKeyword("JULY")
NAMED_AUG = CaselessKeyword("AUG") | CaselessKeyword("AUGUST")
NAMED_SEP = CaselessKeyword("SEP") | CaselessKeyword("SEPTEMBER")
NAMED_OCT = CaselessKeyword("OCT") | CaselessKeyword("OCTOBER")
NAMED_NOV = CaselessKeyword("NOV") | CaselessKeyword("NOVEMBER")
NAMED_DEC = CaselessKeyword("DEC") | CaselessKeyword("DECEMBER")

NAMED_JAN.setParseAction(lambda s,l,t: [["MONTH",  1], ['~', l+len(t[0])]])
NAMED_FEB.setParseAction(lambda s,l,t: [["MONTH",  2], ['~', l+len(t[0])]])
NAMED_MAR.setParseAction(lambda s,l,t: [["MONTH",  3], ['~', l+len(t[0])]])
NAMED_APR.setParseAction(lambda s,l,t: [["MONTH",  4], ['~', l+len(t[0])]])
NAMED_MAY.setParseAction(lambda s,l,t: [["MONTH",  5], ['~', l+len(t[0])]])
NAMED_JUN.setParseAction(lambda s,l,t: [["MONTH",  6], ['~', l+len(t[0])]])
NAMED_JUL.setParseAction(lambda s,l,t: [["MONTH",  7], ['~', l+len(t[0])]])
NAMED_AUG.setParseAction(lambda s,l,t: [["MONTH",  8], ['~', l+len(t[0])]])
NAMED_SEP.setParseAction(lambda s,l,t: [["MONTH",  9], ['~', l+len(t[0])]])
NAMED_OCT.setParseAction(lambda s,l,t: [["MONTH", 10], ['~', l+len(t[0])]])
NAMED_NOV.setParseAction(lambda s,l,t: [["MONTH", 11], ['~', l+len(t[0])]])
NAMED_DEC.setParseAction(lambda s,l,t: [["MONTH", 12], ['~', l+len(t[0])]])

NAMED_MONTH = ( NAMED_JAN | NAMED_FEB | NAMED_MAR | NAMED_APR
              | NAMED_MAY | NAMED_JUN | NAMED_JUL | NAMED_AUG
              | NAMED_SEP | NAMED_OCT | NAMED_NOV | NAMED_DEC ) \
              + WordEnd(alphanums)

JAN = Keyword("1") | Keyword("01")
FEB = Keyword("2") | Keyword("02")
MAR = Keyword("3") | Keyword("03")
APR = Keyword("4") | Keyword("04")
MAY = Keyword("5") | Keyword("05")
JUN = Keyword("6") | Keyword("06")
JUL = Keyword("7") | Keyword("07")
AUG = Keyword("8") | Keyword("08")
SEP = Keyword("9") | Keyword("09")
OCT = Keyword("10")
NOV = Keyword("11")
DEC = Keyword("12")

# Parse actions save a list pair ["MONTH", number 1-12]
JAN.setParseAction(lambda s,l,t: [["MONTH",  1], ['~', l+len(t[0])]])
FEB.setParseAction(lambda s,l,t: [["MONTH",  2], ['~', l+len(t[0])]])
MAR.setParseAction(lambda s,l,t: [["MONTH",  3], ['~', l+len(t[0])]])
APR.setParseAction(lambda s,l,t: [["MONTH",  4], ['~', l+len(t[0])]])
MAY.setParseAction(lambda s,l,t: [["MONTH",  5], ['~', l+len(t[0])]])
JUN.setParseAction(lambda s,l,t: [["MONTH",  6], ['~', l+len(t[0])]])
JUL.setParseAction(lambda s,l,t: [["MONTH",  7], ['~', l+len(t[0])]])
AUG.setParseAction(lambda s,l,t: [["MONTH",  8], ['~', l+len(t[0])]])
SEP.setParseAction(lambda s,l,t: [["MONTH",  9], ['~', l+len(t[0])]])
OCT.setParseAction(lambda s,l,t: [["MONTH", 10], ['~', l+len(t[0])]])
NOV.setParseAction(lambda s,l,t: [["MONTH", 11], ['~', l+len(t[0])]])
DEC.setParseAction(lambda s,l,t: [["MONTH", 12], ['~', l+len(t[0])]])

NUMERIC_MONTH = ( Word("0",NONZERO,exact=2)
                | Word("1","012",exact=2)
                | Word(NONZERO,exact=1) ) + WordEnd(alphanums)
NUMERIC_MONTH.setParseAction(lambda s,l,t: [["MONTH", int(t[0])],
                                            ['~', l+len(t[0])]])

JAN_ = CaselessKeyword("JAN") + DOT
FEB_ = CaselessKeyword("FEB") + DOT
MAR_ = CaselessKeyword("MAR") + DOT
APR_ = CaselessKeyword("APR") + DOT
JUN_ = CaselessKeyword("JUN") + DOT
JUL_ = CaselessKeyword("JUL") + DOT
AUG_ = CaselessKeyword("AUG") + DOT
SEP_ = CaselessKeyword("SEP") + DOT
OCT_ = CaselessKeyword("OCT") + DOT
NOV_ = CaselessKeyword("NOV") + DOT
DEC_ = CaselessKeyword("DEC") + DOT

JAN_.setParseAction(lambda s,l,t: [["MONTH",  1], ['~', l+len(t[0])]])
FEB_.setParseAction(lambda s,l,t: [["MONTH",  2], ['~', l+len(t[0])]])
MAR_.setParseAction(lambda s,l,t: [["MONTH",  3], ['~', l+len(t[0])]])
APR_.setParseAction(lambda s,l,t: [["MONTH",  4], ['~', l+len(t[0])]])
JUN_.setParseAction(lambda s,l,t: [["MONTH",  6], ['~', l+len(t[0])]])
JUL_.setParseAction(lambda s,l,t: [["MONTH",  7], ['~', l+len(t[0])]])
AUG_.setParseAction(lambda s,l,t: [["MONTH",  8], ['~', l+len(t[0])]])
SEP_.setParseAction(lambda s,l,t: [["MONTH",  9], ['~', l+len(t[0])]])
OCT_.setParseAction(lambda s,l,t: [["MONTH", 10], ['~', l+len(t[0])]])
NOV_.setParseAction(lambda s,l,t: [["MONTH", 11], ['~', l+len(t[0])]])
DEC_.setParseAction(lambda s,l,t: [["MONTH", 12], ['~', l+len(t[0])]])

MON_ = ( JAN_ | FEB_ | MAR_ | APR_ | JUN_
       | JUL_ | AUG_ | SEP_ | OCT_ | NOV_ | DEC_)

MONTH        = NAMED_MONTH | MON_ | NUMERIC_MONTH
MONTH_STRICT = NAMED_MONTH | MON_

########################################
# UNIT TESTS
########################################

class Test_MONTH(unittest.TestCase):

    def runTest(self):

        parser = MONTH

        # Matches...
        self.assertEqual(parser.parseString(" jAn ")[0],      ["MONTH",1])
        self.assertEqual(parser.parseString(" FebruarY ")[0], ["MONTH",2])
        self.assertEqual(parser.parseString(" 03 ")[0],       ["MONTH",3])
        self.assertEqual(parser.parseString(" 4 ")[0],        ["MONTH",4])
        self.assertEqual(parser.parseString(" Sep.")[0],      ["MONTH",9])

        # ...cannot complete match
        self.assertEqual(parser.parseString(" 6. ")[0],       ["MONTH",6])

        # Doesn't recognize...
        self.assertRaises(ParseException, parser.parseString, " ")
        self.assertRaises(ParseException, parser.parseString, "JANU")
        self.assertRaises(ParseException, parser.parseString, "JANU.")
        self.assertRaises(ParseException, parser.parseString, "a")
        self.assertRaises(ParseException, parser.parseString, "044")
        self.assertRaises(ParseException, parser.parseString, "0")
        self.assertRaises(ParseException, parser.parseString, ".")
        self.assertRaises(ParseException, parser.parseString, "13")

################################################################################
# DATE31 = a day number within a month
#
# A number 1-31, possibly zero-padded to 2 digits.
################################################################################

DATE31          = ONE_31.copy()

# The parse action saves ["DAY", number 1-31]
DATE31.setParseAction(lambda s,l,t: [["DAY", int(t[0])], ['~', l+len(t[0])]])

########################################
# UNIT TESTS
########################################

class Test_DATE31(unittest.TestCase):

    def runTest(self):

        parser = DATE31

        # Matches...
        for i in range(1,32):
            string = "{:02d}".format(i)
            self.assertEqual(parser.parseString(string).asList()[0],
                ["DAY", i], "Failed on string '" + string + "'")

        # ...cannot complete match
        self.assertEqual(parser.parseString("31a").asList()[0], ["DAY", 31])
        self.assertEqual(parser.parseString("30.").asList()[0], ["DAY", 30])

        # Doesn't recognize...
        self.assertRaises(ParseException, parser.parseString, " ")
        self.assertRaises(ParseException, parser.parseString, "300")
        self.assertRaises(ParseException, parser.parseString, "32")
        self.assertRaises(ParseException, parser.parseString, "a")
        self.assertRaises(ParseException, parser.parseString, "0")

################################################################################
# DAY366 = a day number within a year
#
# A number 1-366, zero-padded to 3 digits.
################################################################################

DAY366          = ONE_366_3DIGIT.copy()
DAY366.setParseAction(lambda s,l,t: [["DAY", int(t[0])], ['~', l+len(t[0])]])

########################################
# UNIT TESTS
########################################

class Test_DAY366(unittest.TestCase):

    def runTest(self):

        parser = DAY366

        # Matches...
        self.assertEqual(parser.parseString(" 366 ").asList()[0], ['DAY', 366])
        for i in range(1,367):
            string = "{:03d}".format(i)
            self.assertEqual(parser.parseString(string).asList()[0],
                ["DAY", i], "Failed on string '" + string + "'")

        # ...cannot complete match
        self.assertEqual(parser.parseString("366a").asList()[0], ["DAY", 366])
        self.assertEqual(parser.parseString("030.").asList()[0], ["DAY",  30])

        # Doesn't recognize...
        self.assertRaises(ParseException, parser.parseString, " ")
        self.assertRaises(ParseException, parser.parseString, "0366")
        self.assertRaises(ParseException, parser.parseString, "03")
        self.assertRaises(ParseException, parser.parseString, "a")
        self.assertRaises(ParseException, parser.parseString, "a")
        self.assertRaises(ParseException, parser.parseString, "0")
        self.assertRaises(ParseException, parser.parseString, "367")

################################################################################
# WEEKDAY
#
# A weekday is a case-insensitive name for the day of the week, possibly
# abbreviated to 3 characters. This is inserted into the parse list but is
# otherwise ignored. It is provided because some date formats (e.g., from SQL)
# include the day of the week, so the parser needs to deal with it.
################################################################################

WEEKDAY = ((CaselessKeyword("SUN") | CaselessKeyword("SUNDAY") |
            CaselessKeyword("MON") | CaselessKeyword("MONDAY") |
            CaselessKeyword("TUE") | CaselessKeyword("TUESDAY") |
            CaselessKeyword("WED") | CaselessKeyword("WEDNESDAY") |
            CaselessKeyword("THU") | CaselessKeyword("THURSDAY") |
            CaselessKeyword("FRI") | CaselessKeyword("FRIDAY") |
            CaselessKeyword("SAT") | CaselessKeyword("SATURDAY"))
                    + WordEnd(alphanums))

WEEKDAY_ = (CaselessKeyword("SUN") + DOT |
            CaselessKeyword("MON") + DOT |
            CaselessKeyword("TUE") + DOT |
            CaselessKeyword("WED") + DOT |
            CaselessKeyword("THU") + DOT |
            CaselessKeyword("FRI") + DOT |
            CaselessKeyword("SAT") + DOT)

WEEKDAY.setParseAction( lambda s,l,t: [["WEEKDAY", t[0][0:3]],
                                       ['~', l+len(t[0])]])
WEEKDAY_.setParseAction(lambda s,l,t: [["WEEKDAY", t[0][0:3]],
                                       ['~', l+len(t[0])]])

########################################
# UNIT TESTS
########################################

class Test_WEEKDAY(unittest.TestCase):

    def runTest(self):

        parser = WEEKDAY

        # Matches...
        self.assertEqual(parser.parseString("MoNdAy")[0], ["WEEKDAY","MON"])
        self.assertEqual(parser.parseString(" Tue ")[0],  ["WEEKDAY","TUE"])

        # ...cannot complete match
        self.assertEqual(parser.parseString(" FrI- ")[0], ["WEEKDAY","FRI"])

        # Doesn't recognize...
        self.assertRaises(ParseException, parser.parseString, " ")
        self.assertRaises(ParseException, parser.parseString, "WEDN")
        self.assertRaises(ParseException, parser.parseString, "a")
        self.assertRaises(ParseException, parser.parseString, "044")
        self.assertRaises(ParseException, parser.parseString, "ThUrSdaY1")
        self.assertRaises(ParseException, parser.parseString, "M")

################################################################################
# MJD_DAY
#
# A Modified Julian day is expressed as "MJD" followed by an unsigned integer.
################################################################################

MJD_DAY         = (Suppress(CaselessLiteral("MJD"))
                    + Word(nums)
                    + WordEnd(nums))

MJD_DAY.setParseAction(lambda s,l,t: [["MJD", int(t[0])], ['~', l+len(t[0])]])

########################################
# UNIT TESTS
########################################

class Test_MJD_Day(unittest.TestCase):

    def runTest(self):

        parser = MJD_DAY

        # Matches...
        self.assertEqual(parser.parseString("mjd 12345")[0],  ["MJD", 12345])
        self.assertEqual(parser.parseString("MJD12345")[0],   ["MJD", 12345])
        self.assertEqual(parser.parseString(" MJD12345 ")[0], ["MJD", 12345])
        self.assertEqual(parser.parseString("MJD12345")[0],   ["MJD", 12345])
        self.assertEqual(parser.parseString("MJD012345")[0],  ["MJD", 12345])

        # ...cannot complete match
        self.assertEqual(parser.parseString("MJD012345a")[0], ["MJD", 12345])
        self.assertEqual(parser.parseString("MJD0123.45")[0], ["MJD",   123])

        # Doesn't recognize...
        self.assertRaises(ParseException, parser.parseString, " ")
        self.assertRaises(ParseException, parser.parseString, "a")
        self.assertRaises(ParseException, parser.parseString, "-44")
        self.assertRaises(ParseException, parser.parseString, "MJD")
        self.assertRaises(ParseException, parser.parseString, "MJD-12345")

################################################################################
# DATE PARSER
#
# Year/month/day or year and day-of-year in some order.
# Tokens separated by dashes, slashes, dots or whitespace.
# A leading weekday is tolerated.
# Commas allowed in some cases.
################################################################################

# Year-month-day order, separated by dash, slash, dot or spaces.
DASH_YMD        = YEAR + DASH  + MONTH        + DASH  + DATE31
SLASH_YMD       = YEAR + SLASH + MONTH        + SLASH + DATE31
DOT_YMD         = YEAR + DOT   + MONTH        + DOT   + DATE31
SPACE_YMD       = YEAR         + MONTH        + DATE31
SPACE_YMD_STRICT= YEAR_4DIGIT  + MONTH_STRICT + DATE31

YMD_DATE        = DASH_YMD | SLASH_YMD | DOT_YMD | SPACE_YMD
YMD_DATE_STRICT = DASH_YMD | SLASH_YMD | DOT_YMD | SPACE_YMD_STRICT

# Month-day-year order, separated by dash, slash, dot or spaces.
DASH_MDY        = MONTH         + DASH  + DATE31 + DASH  + YEAR
SLASH_MDY       = MONTH         + SLASH + DATE31 + SLASH + YEAR
DOT_MDY         = MONTH         + DOT   + DATE31 + DOT   + YEAR
SPACE_MDY_STRICT= MONTH_STRICT  +         DATE31 + Optional(COMMA) + YEAR
SPACE_MDY       = SPACE_MDY_STRICT | NUMERIC_MONTH + DATE31 + YEAR

MDY_DATE        = DASH_MDY | SLASH_MDY | DOT_MDY | SPACE_MDY
MDY_DATE_STRICT = DASH_MDY | SLASH_MDY | DOT_MDY | SPACE_MDY_STRICT

# Day-month-year order, separated by dash, slash, dot or spaces.
DASH_DMY        = DATE31 + DASH  + MONTH        + DASH  + YEAR
SLASH_DMY       = DATE31 + SLASH + MONTH        + SLASH + YEAR
DOT_DMY         = DATE31 + DOT   + MONTH        + DOT   + YEAR
SPACE_DMY_STRICT= DATE31 +         MONTH_STRICT +         YEAR
SPACE_DMY       = SPACE_DMY_STRICT | DATE31 + NUMERIC_MONTH + YEAR

DMY_DATE        = DASH_DMY | SLASH_DMY | DOT_DMY | SPACE_DMY
DMY_DATE_STRICT = DASH_DMY | SLASH_DMY | DOT_DMY | SPACE_DMY_STRICT

# Year-day order, separated by dash, slash, dot or spaces.
YD_DATE         = YEAR + Optional(DASH | SLASH | DOT) + DAY366
YD_DATE_STRICT  = YEAR + (DASH | SLASH) + DAY366

# Date parsers in which one order is preferred but others are allowed
YMD_PREF        = YMD_DATE | MDY_DATE | DMY_DATE | YD_DATE | MJD_DAY
MDY_PREF        = MDY_DATE | YMD_DATE | DMY_DATE | YD_DATE | MJD_DAY
DMY_PREF        = DMY_DATE | MDY_DATE | YMD_DATE | YD_DATE | MJD_DAY

# These versions also tolerate a string beginning with an optional weekday.
OPTIONAL_WEEKDAY= Optional((WEEKDAY ^ WEEKDAY_) + Optional(COMMA))
YMD_PREF_DATE   = OPTIONAL_WEEKDAY + YMD_PREF
MDY_PREF_DATE   = OPTIONAL_WEEKDAY + MDY_PREF
DMY_PREF_DATE   = OPTIONAL_WEEKDAY + DMY_PREF
DATE            = YMD_PREF_DATE

# Date parsers in which one order is preferred but others are allowed
YMD_PREF_STRICT = ( YMD_DATE_STRICT | MDY_DATE_STRICT | DMY_DATE_STRICT
                  | YD_DATE_STRICT  | MJD_DAY)
MDY_PREF_STRICT = ( MDY_DATE_STRICT | YMD_DATE_STRICT | DMY_DATE_STRICT
                  | YD_DATE_STRICT  | MJD_DAY)
DMY_PREF_STRICT = ( DMY_DATE_STRICT | MDY_DATE_STRICT | YMD_DATE_STRICT
                  | YD_DATE_STRICT  | MJD_DAY)

YMD_PREF_DATE_STRICT = OPTIONAL_WEEKDAY + YMD_PREF_STRICT
MDY_PREF_DATE_STRICT = OPTIONAL_WEEKDAY + MDY_PREF_STRICT
DMY_PREF_DATE_STRICT = OPTIONAL_WEEKDAY + DMY_PREF_STRICT
DATE_STRICT     = YMD_PREF_DATE_STRICT

########################################
# UNIT TESTS
########################################

class Test_DATE(unittest.TestCase):

    def runTest(self):

        # Tests of individual parsers and delimiters
        self.assertEqual(DASH_YMD.parseString("1776-07-04").asList()[:6:2],
                [["YEAR",1776],["MONTH",7],["DAY",4]])

        self.assertEqual(SLASH_YMD.parseString("1776/JUL/4").asList()[:6:2],
                [["YEAR",1776],["MONTH",7],["DAY",4]])

        self.assertEqual(DOT_YMD.parseString("1776.7.4").asList()[:6:2],
                [["YEAR",1776],["MONTH",7],["DAY",4]])

        self.assertEqual(SPACE_YMD.parseString("1776   7   31").asList()[:6:2],
                [["YEAR",1776],["MONTH",7],["DAY",31]])

        self.assertEqual(DASH_MDY.parseString("JuLy - 4 - 76").asList()[:6:2],
                [["MONTH",7],["DAY",4],["YEAR",1976]])

        self.assertEqual(SPACE_MDY.parseString("JuLy 4,76").asList()[:6:2],
                [["MONTH",7],["DAY",4],["YEAR",1976]])

        self.assertEqual(SPACE_MDY.parseString("JuLy 4 76").asList()[:6:2],
                [["MONTH",7],["DAY",4],["YEAR",1976]])

        # Test YD_DATE
        parser = YD_DATE

        # Matches...
        YD_DATE_EXPECTED = [["YEAR", 2000], ["DAY", 366]]
        self.assertEqual(parser.parseString("2000 366").asList()[:4:2],
                         YD_DATE_EXPECTED)
        self.assertEqual(parser.parseString("2000-366 ").asList()[:4:2],
                         YD_DATE_EXPECTED)
        self.assertEqual(parser.parseString(" 2000/366").asList()[:4:2],
                         YD_DATE_EXPECTED)
        self.assertEqual(parser.parseString("2000.366").asList()[:4:2],
                         YD_DATE_EXPECTED)

        # Doesn't complete...
        self.assertEqual(parser.parseString("2000-366T").asList()[:4:2],
                         YD_DATE_EXPECTED)
        self.assertEqual(parser.parseString("2000-366:00:00").asList()[:4:2],
                         YD_DATE_EXPECTED)

        # Doesn't recognize...
        self.assertRaises(ParseException, parser.parseString, "2000-3666")
        self.assertRaises(ParseException, parser.parseString, " ")
        self.assertRaises(ParseException, parser.parseString, "a")
        self.assertRaises(ParseException, parser.parseString, "2000-367")
        self.assertRaises(ParseException, parser.parseString, "2000-01")

        # Tests of how an ambiguous date is interpreted
        parser = YMD_PREF_DATE
        self.assertEqual(parser.parseString("07.08.09").asList()[:6:2],
                [["YEAR",2007],["MONTH",8],["DAY",9]])
        self.assertEqual(parser.parseString("07 08 09").asList()[:6:2],
                [["YEAR",2007],["MONTH",8],["DAY",9]])
        self.assertEqual(parser.parseString("07-08-09").asList()[:6:2],
                [["YEAR",2007],["MONTH",8],["DAY",9]])
        self.assertEqual(parser.parseString("07/08/09").asList()[:6:2],
                [["YEAR",2007],["MONTH",8],["DAY",9]])

        parser = MDY_PREF_DATE
        self.assertEqual(parser.parseString("07.08.09").asList()[:6:2],
                [["MONTH",7],["DAY",8],["YEAR",2009]])
        self.assertEqual(parser.parseString("07 08 09").asList()[:6:2],
                [["MONTH",7],["DAY",8],["YEAR",2009]])
        self.assertEqual(parser.parseString("07-08-09").asList()[:6:2],
                [["MONTH",7],["DAY",8],["YEAR",2009]])
        self.assertEqual(parser.parseString("07/08/09").asList()[:6:2],
                [["MONTH",7],["DAY",8],["YEAR",2009]])

        parser = DMY_PREF_DATE
        self.assertEqual(parser.parseString("07.08.09").asList()[:6:2],
                [["DAY",7],["MONTH",8],["YEAR",2009]])
        self.assertEqual(parser.parseString("07 08 09").asList()[:6:2],
                [["DAY",7],["MONTH",8],["YEAR",2009]])
        self.assertEqual(parser.parseString("07-08-09").asList()[:6:2],
                [["DAY",7],["MONTH",8],["YEAR",2009]])
        self.assertEqual(parser.parseString("07/08/09").asList()[:6:2],
                [["DAY",7],["MONTH",8],["YEAR",2009]])

        # Matches to test rejection of invalid formats regardless of parser
        parser = MDY_PREF_DATE
        self.assertRaises(ParseException, parser.parseString, "July 004, 1776")
        self.assertRaises(ParseException, parser.parseString, "July4, 1776")
        self.assertRaises(ParseException, parser.parseString, "July 32, 1776")

        parser = DMY_PREF_DATE
        self.assertRaises(ParseException, parser.parseString, "July 004, 1776")
        self.assertRaises(ParseException, parser.parseString, "July4, 1776")
        self.assertRaises(ParseException, parser.parseString, "July 32, 1776")

        parser = YMD_PREF_DATE
        self.assertRaises(ParseException, parser.parseString, "July 004, 1776")
        self.assertRaises(ParseException, parser.parseString, "July4, 1776")
        self.assertRaises(ParseException, parser.parseString, "July 32, 1776")

        # Matches to test random unambiguous date formats
        parser = MDY_PREF_DATE
        self.assertEqual(parser.parseString("July 4, 1776").asList()[:6:2],
                [["MONTH",7],["DAY",4],["YEAR",1776]])
        self.assertEqual(parser.parseString("Sat July 4, 1776").asList()[:8:2],
                [["WEEKDAY","SAT"],["MONTH",7],["DAY",4],["YEAR",1776]])
        self.assertEqual(parser.parseString("Sat 1776-1-31").asList()[:8:2],
                [["WEEKDAY","SAT"],["YEAR",1776],["MONTH",1],["DAY",31]])
        self.assertEqual(parser.parseString("1776- 001").asList()[:4:2],
                [["YEAR",1776],["DAY",1]])
        self.assertEqual(parser.parseString("1776-366").asList()[:4:2],
                [["YEAR",1776],["DAY",366]])
        self.assertEqual(parser.parseString(" mJd 012345678").asList()[:1],
                [["MJD",12345678]])

        parser = YMD_PREF_DATE
        self.assertEqual(parser.parseString("1776-07-04").asList()[:6:2],
                [["YEAR",1776],["MONTH",7],["DAY",4]])
        self.assertEqual(parser.parseString("July 4, 1776").asList()[:6:2],
                [["MONTH",7],["DAY",4],["YEAR",1776]])
        self.assertEqual(parser.parseString("Sat July 4, 1776").asList()[:8:2],
                [["WEEKDAY","SAT"],["MONTH",7],["DAY",4],["YEAR",1776]])
        self.assertEqual(parser.parseString("1776-001").asList()[:4:2],
                [["YEAR",1776],["DAY",1]])
        self.assertEqual(parser.parseString("1776-366").asList()[:4:2],
                [["YEAR",1776],["DAY",366]])
        self.assertEqual(parser.parseString(" mJd 012345678").asList()[:1],
                [["MJD",12345678]])

        parser = DMY_PREF_DATE
        self.assertEqual(parser.parseString("July 4, 1776").asList()[:6:2],
                [["MONTH",7],["DAY",4],["YEAR",1776]])
        self.assertEqual(parser.parseString("Sat July 4, 1776").asList()[:8:2],
                [["WEEKDAY","SAT"],["MONTH",7],["DAY",4],["YEAR",1776]])
        self.assertEqual(parser.parseString("1776-011").asList()[:4:2],
                [["YEAR",1776],["DAY",11]])
        self.assertEqual(parser.parseString("1776-366").asList()[:4:2],
                [["YEAR",1776],["DAY",366]])
        self.assertEqual(parser.parseString(" mJd 012345678").asList()[:1],
                [["MJD",12345678]])

################################################################################
# HOURS
#
# A one or two digit number, possibly with zero padding up to 2 digits.
#
# Either a 24-hour clock (0-23) or a 12-hour clock (1-12) with am/pm suffixes is
# allowed. Return token is ["HOUR", number 0-23] where the hour number is always
# converted to a 24-hour clock. Below, we restrict the match requirements on the
# 12-hour clock so that the parse action always does the right time conversion.
#
# Fractional hours are tolerated in some situations below.
################################################################################

HOUR23          = ZERO_23.copy()
HOUR23.setParseAction(lambda s,l,t: [["HOUR", int(t[0])],
                                     ['~', l+len(t[0])]])

HOUR23_FLOAT    = Combine(ZERO_23 + "." + Optional(Word(nums)))
HOUR23_FLOAT.setParseAction(lambda s,l,t: [["HOUR", float(t[0])],
                                           ['~', l+len(t[0])]])

HOUR23_W_FRAC   = HOUR23_FLOAT | HOUR23
#-----------------------------------------------------------------------
HOUR12_AM       = ONE_12.copy()
HOUR12_AM.setParseAction(lambda s,l,t: [["HOUR", int(t[0])
                                                 - 12*(int(t[0])//12)],
                                        ['~', l+len(t[0])]])
# HOUR12_AM = 12 gets converted to 0

HOUR12_PM       = ONE_12.copy()
HOUR12_PM.setParseAction(lambda s,l,t: [["HOUR", 12 + int(t[0])
                                                 - 12*(int(t[0])//12)],
                                        ['~', l+len(t[0])]])
# HOUR12_PM = 12 gets converted to 12+0, not 12+12

########################################
# UNIT TESTS
########################################

class Test_Hours(unittest.TestCase):

    def runTest(self):

        parser = HOUR23

        # Matches...
        hour = [12,1,2,3,4,5,6,7,8,9,10,11,12,1,2,3,4,5,6,7,8,9,10,11]
        ampm_parser = HOUR12_AM

        for i in range(0,24):
            if i == 12: ampm_parser = HOUR12_PM

            string = str(i)
            self.assertEqual(HOUR23.parseString(string).asList()[0],
                ["HOUR", i], "Failed on string '" + string + "'")

            string = "{:02d}".format(i)
            self.assertEqual(HOUR23.parseString(string).asList()[0],
                ["HOUR", i], "Failed on string '" + string + "'")

            string = str(i)
            self.assertEqual(HOUR23_W_FRAC.parseString(string).asList()[0],
                ["HOUR", i], "Failed on string '" + string + "'")

            string = "{:02d}".format(i)
            self.assertEqual(HOUR23_W_FRAC.parseString(string).asList()[0],
                ["HOUR", float(i)], "Failed on string '" + string + "'")

            string = str(i) + ".1"
            self.assertEqual(HOUR23_FLOAT.parseString(string).asList()[0],
                ["HOUR", float(i) + 0.1], "Failed on string '" + string + "'")

            string = "{:02d}".format(i) + "."
            self.assertEqual(HOUR23_FLOAT.parseString(string).asList()[0],
                ["HOUR", float(i)], "Failed on string '" + string + "'")

            # Test AM and PM parsers...
            string = str(hour[i])
            self.assertEqual(ampm_parser.parseString(string).asList()[0],
                ["HOUR", i], "Failed on string '" + string + "'")

            string = "{:02d}".format(hour[i])
            self.assertEqual(ampm_parser.parseString(string).asList()[0],
                ["HOUR", i], "Failed on string '" + string + "'")

        # Does not complete...
        self.assertEqual(HOUR23.parseString("23a").asList()[0], ["HOUR", 23])

        # Doesn't recognize...
        self.assertRaises(ParseException, HOUR23.parseString, "24")
        self.assertRaises(ParseException, HOUR23.parseString, " ")
        self.assertRaises(ParseException, HOUR23.parseString, "a")

################################################################################
# MINUTE59
#
# A one or two digit number 0-59, possibly with zero padding up to 2 digits.
# Fractional minutes are tolerated in some situations below.
################################################################################

MINUTE59        = ZERO_59.copy()
MINUTE59.setParseAction(lambda s,l,t: [["MINUTE", int(t[0])],
                                       ['~', l+len(t[0])]])

MINUTE59_FLOAT  = Combine(ZERO_59 + "." + Optional(Word(nums)))
MINUTE59_FLOAT.setParseAction(lambda s,l,t: [["MINUTE", float(t[0])],
                                             ['~', l+len(t[0])]])

MINUTE59_W_FRAC = MINUTE59_FLOAT | MINUTE59

MIN59_STRICT    = ZERO_59_2DIGIT.copy()
MIN59_STRICT.setParseAction(lambda s,l,t: [["MINUTE", int(t[0])],
                                           ['~', l+len(t[0])]])

MIN59_FLOAT_STRICT = Combine(ZERO_59_2DIGIT + "." + Optional(Word(nums)))
MIN59_FLOAT_STRICT.setParseAction(lambda s,l,t: [["MINUTE", float(t[0])],
                                                 ['~', l+len(t[0])]])

MIN59_W_FRAC_STRICT = MIN59_FLOAT_STRICT | MIN59_STRICT

################################################################################
# MINUTE1439
#
# A number 0-14439 plus a possible fractional part, indicating the number of
# minutes into a day.
################################################################################

MINUTE1439_INT  = ZERO_1439.copy()
MINUTE1439_INT.setParseAction(lambda s,l,t: [["MINUTE", int(t[0])],
                                             ['~', l+len(t[0])]])

MINUTE1439_FLOAT = Combine(ZERO_1439 + "." + Optional(Word(nums)))
MINUTE1439_FLOAT.setParseAction(lambda s,l,t: [["MINUTE", float(t[0])],
                                               ['~', l+len(t[0])]])

MINUTE1439      = MINUTE1439_FLOAT | MINUTE1439_INT

################################################################################
# SECOND59
#
# A one or two digit number 0-59, possibly with zero padding up to 2 digits.
# Integer or floating-point seconds are allowed.
################################################################################

SECOND59_INT    = ZERO_59.copy()
SECOND59_INT.setParseAction(lambda s,l,t: [["SECOND", int(t[0])],
                                           ['~', l+len(t[0])]])

SECOND59_FLOAT  = Combine(ZERO_59 + "." + Optional(Word(nums)))
SECOND59_FLOAT.setParseAction(lambda s,l,t: [["SECOND", float(t[0])],
                                             ['~', l+len(t[0])]])

SECOND59        = SECOND59_FLOAT | SECOND59_INT

SEC59_INT_STRICT = ZERO_59_2DIGIT.copy()
SEC59_INT_STRICT.setParseAction(lambda s,l,t: [["SECOND", int(t[0])],
                                               ['~', l+len(t[0])]])

SEC59_FLOAT_STRICT  = Combine(ZERO_59_2DIGIT + "." + Optional(Word(nums)))
SEC59_FLOAT_STRICT.setParseAction(lambda s,l,t: [["SECOND", float(t[0])],
                                                 ['~', l+len(t[0])]])

SEC59_STRICT    = SEC59_FLOAT_STRICT | SEC59_INT_STRICT

################################################################################
# SECOND86399
#
# A number 0-86399 plus a possible fractional part, indicating the number of
# seconds into a day.
################################################################################

SEC86399_INT    = ZERO_86399.copy()
SEC86399_INT.setParseAction(lambda s,l,t: [["SECOND", int(t[0])],
                                           ['~', l+len(t[0])]])

SEC86399_FLOAT  = Combine(ZERO_86399 + "." + Optional(Word(nums)))
SEC86399_FLOAT.setParseAction(lambda s,l,t: [["SECOND", float(t[0])],
                                             ['~', l+len(t[0])]])

SECOND86399     = SEC86399_FLOAT | SEC86399_INT

################################################################################
# LEAPSEC69
#
# A number 60-69 plus a possible fractional part, indicating the number of
# leap seconds attached onto the end of a day.
################################################################################

LEAPSEC69_INT   = SIXTY_69.copy()
LEAPSEC69_INT.setParseAction(lambda s,l,t: [["HOUR",23], ["MINUTE",59],
                                            ["SECOND", int(t[0])],
                                            ['~', l+len(t[0])]])

LEAPSEC69_FLOAT = Combine(SIXTY_69 + "." + Optional(Word(nums)))
LEAPSEC69_FLOAT.setParseAction(lambda s,l,t: [["HOUR",23], ["MINUTE",59],
                                              ["SECOND", float(t[0])],
                                              ['~', l+len(t[0])]])

LEAPSEC69       = LEAPSEC69_FLOAT | LEAPSEC69_INT

################################################################################
# LEAPSEC86409
#
# A number 86400-86409 indicating the number of seconds into a day that
# apparently has leap seconds.
################################################################################

LEAPSEC86409_INT    = N86400_86409.copy()
LEAPSEC86409_INT.setParseAction(lambda s,l,t: [["SECOND", int(t[0])],
                                               ['~', l+len(t[0])]])

LEAPSEC86409_FLOAT  = Combine(N86400_86409 + "." + Optional(Word(nums)))
LEAPSEC86409_FLOAT.setParseAction(lambda s,l,t: [["SECOND", float(t[0])],
                                                 ['~', l+len(t[0])]])

LEAPSEC86409        = LEAPSEC86409_FLOAT | LEAPSEC86409_INT

########################################
# UNIT TESTS
########################################

class Test_Time_Parts(unittest.TestCase):

    def runTest(self):

        parser = MINUTE59_W_FRAC
        # Matches...
        self.assertEqual(parser.parseString(" 59 ").asList()[0], ["MINUTE", 59])
        for i in range(0,60):
            string = str(i)
            self.assertEqual(parser.parseString(string).asList()[0],
                ["MINUTE", i], "Failed on '" + string + "'")

            string = "{:02d}".format(i)
            self.assertEqual(parser.parseString(string).asList()[0],
                ["MINUTE", i], "Failed on '" + string + "'")

            string = str(i) + "."
            self.assertEqual(parser.parseString(string).asList()[0],
                ["MINUTE", float(i)], "Failed on '" + string + "'")

            string = "{:02d}".format(i) + "."
            self.assertEqual(parser.parseString(string).asList()[0],
                ["MINUTE", float(i)], "Failed on '" + string + "'")

        # Doesn't complete...
        self.assertEqual(parser.parseString("59a").asList()[0], ["MINUTE", 59])

        # Doesn't recognize...
        self.assertRaises(ParseException, parser.parseString, " ")
        self.assertRaises(ParseException, parser.parseString, "a")
        self.assertRaises(ParseException, parser.parseString, "60")
        self.assertRaises(ParseException, parser.parseString, "001")

        parser = MINUTE1439
        # Matches...
        self.assertEqual(parser.parseString(" 1439 ").asList()[0],
                         ["MINUTE", 1439])
        for i in range(0,1440):
            string = str(i)
            self.assertEqual(parser.parseString(string).asList()[0],
                ["MINUTE",i], "Failed on '" + string + "'")

            string = "{:04d}".format(i)
            self.assertEqual(parser.parseString(string).asList()[0],
                ["MINUTE",i], "Failed on '" + string + "'")

            string = str(i) + "."
            self.assertEqual(parser.parseString(string).asList()[0],
                ["MINUTE", float(i)], "Failed on '" + string + "'")

            string = "{:04d}".format(i) + "."
            self.assertEqual(parser.parseString(string).asList()[0],
                ["MINUTE", float(i)], "Failed on '" + string + "'")


        # Doesn't complete...
        self.assertEqual(parser.parseString("1439a").asList()[0],
                ["MINUTE", 1439])

        # Doesn't recognize...
        self.assertRaises(ParseException, parser.parseString, " ")
        self.assertRaises(ParseException, parser.parseString, "a")
        self.assertRaises(ParseException, parser.parseString, "1440")

        parser = SECOND59
        # Matches...
        self.assertEqual(parser.parseString(" 59 ").asList()[0],
            ["SECOND", 59])

        for i in range(0,60):
            string = str(i)
            self.assertEqual(parser.parseString(string).asList()[0],
                ["SECOND", i], "Failed on '" + string + "'")

            string = "{:02d}".format(i)
            self.assertEqual(parser.parseString(string).asList()[0],
                ["SECOND", i], "Failed on '" + string + "'")

            string = str(i) + "."
            self.assertEqual(parser.parseString(string).asList()[0],
                ["SECOND", float(i)], "Failed on '" + string + "'")

            string = "{:02d}".format(i) + "."
            self.assertEqual(parser.parseString(string).asList()[0],
                ["SECOND", float(i)], "Failed on '" + string + "'")

        # Doesn't complete...
        self.assertEqual(parser.parseString("59a").asList()[0], ["SECOND", 59])

        # Doesn't recognize...
        self.assertRaises(ParseException, parser.parseString, " ")
        self.assertRaises(ParseException, parser.parseString, "a")
        self.assertRaises(ParseException, parser.parseString, "60")
        self.assertRaises(ParseException, parser.parseString, "001")

        parser = SECOND86399
        # Matches...
        for i in range(0,86400,432):
            string = str(i)
            self.assertEqual(parser.parseString(string).asList()[0],
                ["SECOND", i], "Failed on '" + string + "'")

            string = "{:05d}".format(i)
            self.assertEqual(parser.parseString(string).asList()[0],
                ["SECOND", i], "Failed on '" + string + "'")

            string = str(i) + "."
            self.assertEqual(parser.parseString(string).asList()[0],
                ["SECOND", float(i)], "Failed on '" + string + "'")

            string = "{:05d}".format(i) + "."
            self.assertEqual(parser.parseString(string).asList()[0],
                ["SECOND", float(i)], "Failed on '" + string + "'")

        # Doesn't complete...
        self.assertEqual(parser.parseString("86 399").asList()[0],
                ["SECOND", 86])
        self.assertEqual(parser.parseString("86399A").asList()[0],
                ["SECOND", 86399])

        # Doesn't recognize...
        self.assertRaises(ParseException, parser.parseString, " ")
        self.assertRaises(ParseException, parser.parseString, "a")
        self.assertRaises(ParseException, parser.parseString, "86400")

        parser = LEAPSEC69
        # Matches...
        for i in range(60,70):
            string = str(i)
            self.assertEqual(parser.parseString(string).asList()[:3],
                [['HOUR', 23], ['MINUTE', 59], ["SECOND", i]],
                "Failed on '" + string + "'")

            string = "{:02d}".format(i)
            self.assertEqual(parser.parseString(string).asList()[:3],
                [['HOUR', 23], ['MINUTE', 59], ["SECOND", i]],
                "Failed on '" + string + "'")

            string = str(i) + "."
            self.assertEqual(parser.parseString(string).asList()[:3],
                [['HOUR', 23], ['MINUTE', 59], ["SECOND", float(i)]],
                "Failed on '" + string + "'")

            string = "{:02d}".format(i) + "."
            self.assertEqual(parser.parseString(string).asList()[:3],
                [['HOUR', 23], ['MINUTE', 59], ["SECOND", float(i)]],
                "Failed on '" + string + "'")

        # Doesn't complete...
        self.assertEqual(parser.parseString("65a").asList()[:3],
                [['HOUR', 23], ['MINUTE', 59], ["SECOND", 65]])

        # Doesn't recognize...
        self.assertRaises(ParseException, parser.parseString, " ")
        self.assertRaises(ParseException, parser.parseString, "a")
        self.assertRaises(ParseException, parser.parseString, "70")
        self.assertRaises(ParseException, parser.parseString, "59")

        parser = LEAPSEC86409
        # Matches...
        for i in range(86400,86410):
            string = str(i)
            self.assertEqual(parser.parseString(string).asList()[0],
                ["SECOND", i], "Failed on '" + string + "'")

            string = "{:02d}".format(i)
            self.assertEqual(parser.parseString(string).asList()[0],
                ["SECOND", i], "Failed on '" + string + "'")

            string = str(i) + "."
            self.assertEqual(parser.parseString(string).asList()[0],
                ["SECOND", float(i)], "Failed on '" + string + "'")

            string = "{:02d}".format(i) + "."
            self.assertEqual(parser.parseString(string).asList()[0],
                ["SECOND", float(i)], "Failed on '" + string + "'")

        # Doesn't complete...
        self.assertEqual(parser.parseString("86409a").asList()[0],
                ["SECOND", 86409])

        # Doesn't recognize...
        self.assertRaises(ParseException, parser.parseString, " ")
        self.assertRaises(ParseException, parser.parseString, "a")
        self.assertRaises(ParseException, parser.parseString, "86410")

################################################################################
# TIME_TYPE
#
# Times can be in UTC, TAI or TDB. A suffix of "UTC", "UT" or "Z" implies UTC;
# "TAI" implies TAI, "TDB" or "ET" implies TDB, "TDT" implies TDT.
################################################################################

UTC_TYPE        = (CaselessKeyword("UTC") |
                    CaselessKeyword("UT") |
                    Literal("Z"))
UTC_TYPE.setParseAction(lambda s, l, t: [["TYPE", "UTC"],
                                         ['~', l+len(t[0])]])

TAI_TYPE        = CaselessKeyword("TAI")
TAI_TYPE.setParseAction(lambda s, l, t: [["TYPE", "TAI"],
                                         ['~', l+len(t[0])]])

TDB_TYPE        = (CaselessKeyword("TDB") |
                    CaselessKeyword("ET"))
TDB_TYPE.setParseAction(lambda s, l, t: [["TYPE", "TDB"],
                                         ['~', l+len(t[0])]])

TDT_TYPE        = CaselessKeyword("TDT")
TDT_TYPE.setParseAction(lambda s, l, t: [["TYPE", "TDT"],
                                         ['~', l+len(t[0])]])

TIME_TYPE       = UTC_TYPE | TDB_TYPE | TDT_TYPE | TAI_TYPE

########################################
# UNIT TESTS
########################################

class Test_TIME_TYPE(unittest.TestCase):

    def runTest(self):

        parser = TIME_TYPE

        # Matches...
        self.assertEqual(parser.parseString(" UTC").asList()[0], ["TYPE", "UTC"])
        self.assertEqual(parser.parseString("UT").asList()[0],   ["TYPE", "UTC"])
        self.assertEqual(parser.parseString("Z").asList()[0],    ["TYPE", "UTC"])
        self.assertEqual(parser.parseString("utc").asList()[0],  ["TYPE", "UTC"])
        self.assertEqual(parser.parseString("TAI ").asList()[0], ["TYPE", "TAI"])
        self.assertEqual(parser.parseString("tai").asList()[0],  ["TYPE", "TAI"])
        self.assertEqual(parser.parseString(" TDB").asList()[0], ["TYPE", "TDB"])
        self.assertEqual(parser.parseString("ET").asList()[0],   ["TYPE", "TDB"])
        self.assertEqual(parser.parseString("tdt").asList()[0],  ["TYPE", "TDT"])
        self.assertEqual(parser.parseString("et").asList()[0],   ["TYPE", "TDB"])

        # Doesn't complete...
        self.assertEqual(parser.parseString("UT c").asList()[0], ["TYPE", "UTC"])

        # Doesn't recognize...
        self.assertRaises(ParseException, parser.parseString, " ")
        self.assertRaises(ParseException, parser.parseString, "a")
        self.assertRaises(ParseException, parser.parseString, "0")
        self.assertRaises(ParseException, parser.parseString, "U")
        self.assertRaises(ParseException, parser.parseString, "utc1")
        self.assertRaises(ParseException, parser.parseString, "u t c")
        self.assertRaises(ParseException, parser.parseString, "u.t.c")
        self.assertRaises(ParseException, parser.parseString, "TA I")
        self.assertRaises(ParseException, parser.parseString, "TD T")
        self.assertRaises(ParseException, parser.parseString, "E T")

################################################################################
# TIME PARSER
################################################################################

# Useful definitions...
AM              = Suppress(CaselessLiteral("AM"))
PM              = Suppress(CaselessLiteral("PM"))
S               = Suppress(CaselessLiteral("S"))
M               = Suppress(CaselessLiteral("M"))
H               = Suppress(CaselessLiteral("H"))
D               = Suppress(CaselessLiteral("D"))

ELEVEN          = Suppress(Literal("11"))
TWENTYTHREE     = Suppress(Literal("23"))
FIFTYNINE       = Suppress(Literal("59"))

# A colon plus a conventional number of seconds
OPTIONAL_S      = Optional(COLON + SECOND59)
OPTIONAL_S_STRICT = Optional(COLON + SEC59_STRICT)

# A colon plus a conventional number of minutes, and optional seconds
OPTIONAL_MS     = Optional(COLON + MINUTE59 + OPTIONAL_S)
OPTIONAL_MS_STRICT = Optional(COLON + MIN59_STRICT + OPTIONAL_S_STRICT)

# Options in order...
# number + "S" to express time as seconds into a day
# number + "M" to express time as minutes into a day
# hour:minutes with optional fraction minutes
# number + "H" to express time as hours into a day
# hour[:minute[:second] am for morning time
# hour[:minute[:second] pm for afternoon time
# hour[:minute[:second] as 24 hour clock

AMPM_NORMAL_TIME = ( HOUR12_AM + OPTIONAL_MS + AM
                   | HOUR12_PM + OPTIONAL_MS + PM)
AMPM_LEAP_TIME  = ELEVEN + COLON + FIFTYNINE + COLON + LEAPSEC69 + PM

AMPM_TIME       = AMPM_LEAP_TIME | AMPM_NORMAL_TIME

NORMAL_TIME     = (   HOUR23 + COLON + MINUTE59 + OPTIONAL_S
                    | HOUR23 + COLON + MINUTE59_FLOAT  # Float doesn't work. !!!(1)
                    | HOUR23_W_FRAC + H
                    | MINUTE1439  + M
                    | SECOND86399 + S
                  )
LEAP_TIME_HMS   = TWENTYTHREE + COLON + FIFTYNINE + COLON + LEAPSEC69
LEAP_TIME       = LEAP_TIME_HMS | LEAPSEC86409 + S

# Any time expression
TIME            = AMPM_TIME | LEAP_TIME | NORMAL_TIME

# A time expression with optional type
TYPED_TIME      = (   AMPM_TIME
                    | LEAP_TIME + Optional(TIME_TYPE)
                    | NORMAL_TIME + Optional(TIME_TYPE)
                  )

#### Strict version:
#### - minutes are always required
#### - no fractional hours or minutes

AMPM_STRICT     = ( HOUR12_AM + COLON + MIN59_STRICT + OPTIONAL_S_STRICT + AM
                  | HOUR12_PM + COLON + MIN59_STRICT + OPTIONAL_S_STRICT + PM
                  | AMPM_LEAP_TIME
                  )

TIME_STRICT     = ( AMPM_STRICT
                  | LEAP_TIME_HMS
                  | HOUR23 + COLON + MIN59_STRICT + OPTIONAL_S_STRICT
                  )

TYPED_TIME_STRICT = ( AMPM_STRICT
                    | LEAP_TIME_HMS + Optional(TIME_TYPE)
                    | HOUR23 + COLON + MIN59_STRICT + OPTIONAL_S_STRICT
                                    + Optional(TIME_TYPE)
                    )

########################################
# UNIT TESTS
########################################

class Test_TYPED_TIME(unittest.TestCase):

    def runTest(self):

        parser = TYPED_TIME + StringEnd()

       # Test AMPM_NORMAL_TIME
        self.assertEqual(parser.parseString(" 1AM ").asList()[0], ["HOUR", 1])
        self.assertEqual(parser.parseString("12 AM").asList()[0], ["HOUR", 0])
        self.assertEqual(parser.parseString("12 PM").asList()[0], ["HOUR", 12])

        self.assertEqual(parser.parseString("01:01 AM").asList()[:3:2],
                        [["HOUR", 1], ["MINUTE", 1]])
        self.assertEqual(parser.parseString("01: 1 AM").asList()[:3:2],
                        [["HOUR", 1], ["MINUTE", 1]])
        self.assertEqual(parser.parseString("01:01:01 AM").asList()[:6:2],
                        [["HOUR", 1], ["MINUTE", 1], ["SECOND", 1]])
        self.assertEqual(parser.parseString("01:1:01 AM").asList()[:6:2],
                        [["HOUR", 1], ["MINUTE", 1], ["SECOND", 1]])
        self.assertEqual(parser.parseString("01:01:01.5 AM").asList()[:6:2],
                        [["HOUR", 1], ["MINUTE", 1], ["SECOND", 1.5]])

        # Test AMPM_LEAP_TIME
        self.assertEqual(parser.parseString("11:59:69 PM").asList()[:3],
                        [["HOUR", 23], ["MINUTE", 59], ["SECOND", 69]])

        # Test NORMAL_TIME
        self.assertEqual(parser.parseString("01:01:01.000").asList()[:6:2],
                        [["HOUR", 1], ["MINUTE", 1], ["SECOND", 1.0]])
        self.assertEqual(parser.parseString("01:01:01").asList()[:6:2],
                        [["HOUR", 1], ["MINUTE", 1], ["SECOND", 1]])
        self.assertEqual(parser.parseString("01:01").asList()[:4:2],
                        [["HOUR", 1], ["MINUTE", 1]])
        self.assertEqual(parser.parseString("01:01").asList()[:4:2],
                        [["HOUR", 1], ["MINUTE", 1]])
        self.assertEqual(parser.parseString("15.5H").asList()[0],
                        ["HOUR", 15.5])
        self.assertEqual(parser.parseString("15.5 H").asList()[0],
                        ["HOUR", 15.5])
        self.assertEqual(parser.parseString("1234M").asList()[0],
                        ["MINUTE", 1234])
        self.assertEqual(parser.parseString("1234 M").asList()[0],
                        ["MINUTE", 1234])
        self.assertEqual(parser.parseString("12345S").asList()[0],
                        ["SECOND", 12345])
        self.assertEqual(parser.parseString("12345 S").asList()[0],
                        ["SECOND", 12345])

        # Test LEAP_TIME
        for i in range(60,70):
            string = str(i)
            self.assertEqual(parser.parseString("23:59:" + string).asList()[:3],
                        [["HOUR", 23], ["MINUTE", 59], ["SECOND", int(string)]])
        self.assertEqual(parser.parseString(" 86400S ").asList()[0],
                         ["SECOND", 86400 ])
        self.assertEqual(parser.parseString("86409 s").asList()[0],
                         ["SECOND", 86409])

        self.assertRaises(ParseException, parser.parseString, "23:59:70")

################################################################################
# NUMERIC_DATE
#
# A number combined with one of "MJD", "JD", MJED", "JED", "TAI", "TDB", "ET",
# or "TDT".
################################################################################

DOT_FLOAT       = Combine(Optional("-") + Optional(Word(nums)) + Literal(".") +
                          Word(nums))
INT_FLOAT       = Combine(Optional("-") + Word(nums) + Optional("."))
FLOAT           = DOT_FLOAT | INT_FLOAT
FLOAT.setParseAction(lambda s,l,t: [["NUMBER", float(t[0])],
                                    ['~', l+len(t[0])]])

DATE_UNIT_ET    = CaselessLiteral("ET")
DATE_UNIT_ET.setParseAction(lambda s,l,t: [["UNIT", "TDB"],
                                           ['~', l+len(t[0])]])

DATE_UNIT_NOT_ET  = (CaselessLiteral("MJD")
                    | CaselessLiteral("JD")
                    | CaselessLiteral("MJED")
                    | CaselessLiteral("JED")
                    | CaselessLiteral("TAI")
                    | CaselessLiteral("TDB")
                    | CaselessLiteral("TDT")
                  )
DATE_UNIT_NOT_ET.setParseAction(lambda s,l,t: [["UNIT", t[0]],
                                               ['~', l+len(t[0])]])

DATE_UNIT       = DATE_UNIT_NOT_ET | DATE_UNIT_ET

NUMERIC_DATE    = (DATE_UNIT + FLOAT
                    | FLOAT + DATE_UNIT
                    | FLOAT + Suppress(Literal("(")) + DATE_UNIT +
                        Suppress(Literal(")"))
                  )

########################################
# UNIT TESTS
########################################

class Test_NUMERIC_DATE(unittest.TestCase):

    def runTest(self):

        # Test NUMERIC_DATE
        parser = NUMERIC_DATE + StringEnd()

        self.assertEqual(parser.parseString(" MJD0").asList()[:4:2],
                         [['UNIT', 'MJD'], ['NUMBER', 0.]])
        self.assertEqual(parser.parseString("JD .5 ").asList()[:4:2],
                         [['UNIT', 'JD'], ['NUMBER', 0.5]])
        self.assertEqual(parser.parseString(" JED0.5 ").asList()[:4:2],
                         [['UNIT', 'JED'], ['NUMBER', 0.5]])
        self.assertEqual(parser.parseString(" 1234567 JED ").asList()[:4:2],
                         [['NUMBER', 1234567.], ['UNIT', 'JED']])
        self.assertEqual(parser.parseString(" -1234567 (TAI ) ").asList()[:4:2],
                         [['NUMBER', -1234567.], ['UNIT', 'TAI']])
        self.assertEqual(parser.parseString("TDT-0  ").asList()[:4:2],
                         [['UNIT', 'TDT'], ['NUMBER', 0.]])

        # Doesn't recognize...
        self.assertRaises(ParseException, parser.parseString, " ")
        self.assertRaises(ParseException, parser.parseString, "a")
        self.assertRaises(ParseException, parser.parseString, "0")
        self.assertRaises(ParseException, parser.parseString, "MJED 0-")

################################################################################
# FRACTIONAL_DATE
#
# Any form of date in which the day comes last and includes an optional
# decimal point and fractional part.
################################################################################

DATE31_FLOAT    = Combine(ONE_31 + "." + Optional(Word(nums)))
DATE31_FLOAT.setWhitespaceChars("")
DATE31_FLOAT.setParseAction(lambda s,l,t: [["DAY", float(t[0])],
                                           ['~', l+len(t[0])]])

DASH_YMD_FLOAT  = YEAR + DASH  + MONTH + DASH  + DATE31_FLOAT
SLASH_YMD_FLOAT = YEAR + SLASH + MONTH + SLASH + DATE31_FLOAT
SPACE_YMD_FLOAT = YEAR + WHITE + MONTH + WHITE + DATE31_FLOAT

DAY366_FLOAT    = Combine(ONE_366_3DIGIT + "." + Optional(Word(nums)))
DAY366_FLOAT.setParseAction(lambda s,l,t: [["DAY", float(t[0])],
                                           ['~', l+len(t[0])]])

YD_FLOAT        = YEAR + Optional(DASH | SLASH) + DAY366_FLOAT

FRACTIONAL_DATE = ((  DASH_YMD_FLOAT
                    | SLASH_YMD_FLOAT
                    | SPACE_YMD_FLOAT
                    | YD_FLOAT)
                    + Optional(TIME_TYPE)
                  )

########################################
# UNIT TESTS
########################################

class Test_FRACTIONAL_DATE(unittest.TestCase):

    def runTest(self):

        # YMD_FLOATs
        Expected = [["YEAR", 2000], ["MONTH", 1], ["DAY", 1.0]]
        self.assertEqual(DASH_YMD_FLOAT.parseString(" 2000-01-01. ").asList()[:6:2],
                         Expected)
        self.assertEqual(DASH_YMD_FLOAT.parseString(" 00-1-1. ").asList()[:6:2],
                         Expected)
        self.assertEqual(SLASH_YMD_FLOAT.parseString(" 2000/01/01. ").asList()[:6:2],
                         Expected)
        self.assertEqual(SLASH_YMD_FLOAT.parseString(" 00/1/1. ").asList()[:6:2],
                         Expected)
        self.assertEqual(SPACE_YMD_FLOAT.parseString(" 2000 01 01. ").asList()[:6:2],
                         Expected)
        self.assertEqual(SPACE_YMD_FLOAT.parseString(" 00 1 1. ").asList()[:6:2],
                         Expected)

        # Test YD_FLOAT
        parser = YD_FLOAT
        Expected = [["YEAR", 2000], ["DAY", 1.0]]
        self.assertEqual(parser.parseString("2000- 001.").asList()[:4:2], Expected)
        self.assertEqual(parser.parseString("2000/ 001.").asList()[:4:2], Expected)
        self.assertEqual(parser.parseString("2000 001.").asList()[:4:2],  Expected)
        self.assertEqual(parser.parseString("2000-366.").asList()[:4:2],
                         [["YEAR", 2000], ["DAY", 366.0]])
        self.assertEqual(parser.parseString("2000-366.5").asList()[:4:2],
                         [["YEAR", 2000], ["DAY", 366.5]])

        # Doesn't recognize....
        self.assertRaises(ParseException, parser.parseString, "2000/01.")
        self.assertRaises(ParseException, parser.parseString, "2000 -01.")
        self.assertRaises(ParseException, parser.parseString, "2000 01.0")
        self.assertRaises(ParseException, parser.parseString, "2000-01-1")
        self.assertRaises(ParseException, parser.parseString, "2000 - 01 - 1.")
        self.assertRaises(ParseException, parser.parseString, "2000\01\1")
        self.assertRaises(ParseException, parser.parseString, "2000 \ 01 \ 1.")
        self.assertRaises(ParseException, parser.parseString, "2000 01 1")
        self.assertRaises(ParseException, parser.parseString, " ")
        self.assertRaises(ParseException, parser.parseString, "a")
        self.assertRaises(ParseException, parser.parseString, "2000-1")
        self.assertRaises(ParseException, parser.parseString, "2000/1")
        self.assertRaises(ParseException, parser.parseString, "2000 1")
        self.assertRaises(ParseException, parser.parseString, "2000-01")
        self.assertRaises(ParseException, parser.parseString, "2000/01")
        self.assertRaises(ParseException, parser.parseString, "2000 01")
        self.assertRaises(ParseException, parser.parseString, "2000-001")
        self.assertRaises(ParseException, parser.parseString, "2000/001")
        self.assertRaises(ParseException, parser.parseString, "2000 001")
        self.assertRaises(ParseException, parser.parseString, "2000-1")
        self.assertRaises(ParseException, parser.parseString, "2000/1")
        self.assertRaises(ParseException, parser.parseString, "2000 1")
        self.assertRaises(ParseException, parser.parseString, "2000-367")
        self.assertRaises(ParseException, parser.parseString, "2000-3666")

        # Test FRACTIONAL_DATE
        parser = FRACTIONAL_DATE
        self.assertEqual(parser.parseString("2000-01-01.").asList()[:6:2],
                        [["YEAR", 2000], ["MONTH", 1], ["DAY", 1.0]])
        self.assertEqual(parser.parseString("2000-001.").asList()[:4:2],
                        [["YEAR", 2000], ["DAY", 1.0]])
        self.assertEqual(parser.parseString("2000-01-01.UTC").asList()[:8:2],
                        [["YEAR", 2000], ["MONTH", 1], ["DAY", 1.0],
                         ["TYPE", "UTC"]])
        self.assertEqual(parser.parseString("2000/01/01. TAI").asList()[:8:2],
                        [["YEAR", 2000], ["MONTH", 1], ["DAY", 1.0],
                         ["TYPE", "TAI"]])
        self.assertEqual(parser.parseString("2000 01 01. TDT").asList()[:8:2],
                        [["YEAR", 2000], ["MONTH", 1], ["DAY", 1.0],
                         ["TYPE", "TDT"]])
        self.assertEqual(parser.parseString("2000-001.Z").asList()[:6:2],
                         [["YEAR", 2000], ["DAY", 1.0], ["TYPE", "UTC"]])

        # Doesn't complete...
        self.assertEqual(parser.parseString("2000 01 01.-Z").asList()[:6:2],
                        [["YEAR", 2000], ["MONTH", 1], ["DAY", 1.0]])

        # Doesn't recognize....
        self.assertRaises(ParseException, parser.parseString, " ")
        self.assertRaises(ParseException, parser.parseString, "a")
        self.assertRaises(ParseException, parser.parseString, "0")
        self.assertRaises(ParseException, parser.parseString, "2000-1UTC")
        self.assertRaises(ParseException, parser.parseString, "2000/1UT")
        self.assertRaises(ParseException, parser.parseString, "2000 1Z")
        self.assertRaises(ParseException, parser.parseString, "2000\01\1TAI")
        self.assertRaises(ParseException, parser.parseString, "2000 01 1TDB")
        self.assertRaises(ParseException, parser.parseString, "2000-01-1 UTC")

################################################################################
# DATE-TIME PARSERS
################################################################################

# Separator between date and time is comma, colon or whitespace
SEPARATOR       = (COMMA | COLON | DASH | SLASH)
T               = Suppress(Literal("T"))

# Options in order...
# A date, separator, time, and optional type
# A time, optional type, separator and a date
# A date involving a fractional day

# Three variants depend on the preferred order of year, month and date, to be
# used when a date expression is ambiguous.

YMD_PREF_DATETIME = ( YMD_PREF_DATE + Optional(SEPARATOR) + TYPED_TIME
                    | TYPED_TIME + Optional(SEPARATOR) + YMD_PREF_DATE
                    | (YMD_DATE | YD_DATE) + T + TYPED_TIME
                    | FRACTIONAL_DATE | NUMERIC_DATE
                    | YMD_PREF_DATE
                    )

MDY_PREF_DATETIME = ( MDY_PREF_DATE + Optional(SEPARATOR) + TYPED_TIME
                    | TYPED_TIME + Optional(SEPARATOR) + MDY_PREF_DATE
                    | (YMD_DATE | YD_DATE) + T + TYPED_TIME
                    | FRACTIONAL_DATE | NUMERIC_DATE
                    | MDY_PREF_DATE
                    )

DMY_PREF_DATETIME = ( DMY_PREF_DATE + Optional(SEPARATOR) + TYPED_TIME
                    | TYPED_TIME + Optional(SEPARATOR) + DMY_PREF_DATE
                    | (YMD_DATE | YD_DATE) + T + TYPED_TIME
                    | FRACTIONAL_DATE | NUMERIC_DATE
                    | DMY_PREF_DATE
                    )

# Default is YMD
DATETIME        = YMD_PREF_DATETIME

YMD_PREF_DATETIME_STRICT = \
                    ( YMD_PREF_DATE_STRICT + Optional(SEPARATOR) + TYPED_TIME
                    | TYPED_TIME + Optional(SEPARATOR) + YMD_PREF_DATE_STRICT
                    | (YMD_DATE | YD_DATE) + T + TYPED_TIME
                    | YMD_PREF_DATE_STRICT
                    )

MDY_PREF_DATETIME_STRICT = \
                    ( MDY_PREF_DATE_STRICT + Optional(SEPARATOR) + TYPED_TIME
                    | TYPED_TIME + Optional(SEPARATOR) + MDY_PREF_DATE_STRICT
                    | (YMD_DATE | YD_DATE) + T + TYPED_TIME
                    | MDY_PREF_DATE_STRICT
                    )

DMY_PREF_DATETIME_STRICT = \
                    ( DMY_PREF_DATE_STRICT + Optional(SEPARATOR) + TYPED_TIME
                    | TYPED_TIME + Optional(SEPARATOR) + DMY_PREF_DATE_STRICT
                    | (YMD_DATE | YD_DATE) + T + TYPED_TIME
                    | DMY_PREF_DATE_STRICT
                    )

# Default is YMD
DATETIME_STRICT  = YMD_PREF_DATE_STRICT

########################################
# UNIT TESTS
########################################

class Test_DATETIME(unittest.TestCase):

    def runTest(self):

        parser = DATETIME

        # Test SEPARATOR
        # Date first
        case1 = [['YEAR', 2000], ['MONTH', 1], ['DAY', 1],
                 ['HOUR', 0], ['MINUTE', 0], ['SECOND', 0.0]]
        self.assertEqual(parser.parseString("2000-01-01,00:00:00.000").asList()[:12:2],
                         case1)
        self.assertEqual(parser.parseString("2000-JAN-01:00:00:00.00").asList()[:12:2],
                         case1)
        self.assertEqual(parser.parseString("2000-JAN-01/00:00:00.00").asList()[:12:2],
                         case1)
        self.assertEqual(parser.parseString("2000/JAN/01/00:00:00.00").asList()[:12:2],
                         case1)
        self.assertEqual(parser.parseString("2000-01-01 00:00:00.000").asList()[:12:2],
                         case1)

        # Time first
        case2 = [['HOUR', 0], ['MINUTE', 0], ['SECOND', 0.0],
                 ['YEAR', 2000], ['MONTH', 1], ['DAY', 1]]
        self.assertEqual(parser.parseString("00:00:00.000,2000-01-01").asList()[:12:2],
                         case2)
        self.assertEqual(parser.parseString("00:00:00.00:2000-jan-01").asList()[:12:2],
                         case2)
        self.assertEqual(parser.parseString("00:00:00.000 2000-01-01").asList()[:12:2],
                         case2)

        # Check floating seconds
        self.assertEqual(parser.parseString("2000-01-01,00:00:00").asList()[:12:2],
                    [['YEAR', 2000], ['MONTH', 1], ['DAY', 1],
                     ['HOUR', 0], ['MINUTE', 0], ['SECOND', 0]])
        self.assertEqual(parser.parseString("00:00:00,2000-01-01").asList()[:12:2],
                    [['HOUR', 0], ['MINUTE', 0], ['SECOND', 0],
                     ['YEAR', 2000], ['MONTH', 1], ['DAY', 1]])

        # Test T
        self.assertEqual(parser.parseString("2000-12-31T12:34:56.789").asList()[:12:2],
                    [['YEAR', 2000], ['MONTH', 12], ['DAY', 31],
                     ['HOUR', 12], ['MINUTE', 34], ['SECOND', 56.789]])
        self.assertEqual(parser.parseString(" 2000-366T00:00:00.000 ").asList()[:10:2],
                    [['YEAR', 2000], ['DAY', 366],
                     ['HOUR', 0], ['MINUTE', 0], ['SECOND', 0.0]])
        self.assertEqual(parser.parseString("2000-001 T 00:00:00").asList()[:10:2],
                    [['YEAR', 2000], ['DAY', 1],
                     ['HOUR', 0], ['MINUTE', 0], ['SECOND', 0.0]])

        # Test FRACTIONAL_DATE and NUMERIC_DATE
        self.assertEqual(parser.parseString("2000-01-01.UTC").asList()[:8:2],
                    [["YEAR", 2000], ["MONTH", 1], ["DAY", 1.0],
                     ["TYPE", "UTC"]])
        self.assertEqual(parser.parseString("2000-01-01.").asList()[:6:2],
                    [["YEAR", 2000], ["MONTH", 1], ["DAY", 1.0]])
        self.assertEqual(parser.parseString("2000-001.UTC").asList()[:6:2],
                    [["YEAR", 2000], ["DAY", 1.0],
                     ["TYPE", "UTC"]])
        self.assertEqual(parser.parseString("2000-001.5").asList()[:4:2],
                    [["YEAR", 2000], ["DAY", 1.5]])

################################################################################
# Perform unit testing if executed from the command line
################################################################################

if __name__ == "__main__":
    unittest.main()

################################################################################

