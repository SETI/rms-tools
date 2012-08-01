################################################################################
# julian.py - The Julian Library
#
# This is a set of routines for handing date and time conversions. It handles
# three time systems:
#   UTC = Universal Coordinates Time, similar to Grenwich Mean Time
#   TAI = International Atomic Time, which is the same as UTC except that it
#         ignores leap seconds. UTC and TAI always differ by a whole number of
#         seconds. The SPICE LS kernel is read at run time to get the lastest
#         list of leap seconds.
#   TDB = Terrestrial Barycentric Time, which is adjusted for the relativistic
#         effects that cause a clock on the Earth to vary in speed relative to
#         one at the solar system barycenter.
#
#   The library also handles calendar conversions and both parses and formats
#   strings that express time in UTC.
#
#   This library duplicates much of the functionality of python's built-in
#   datetime library, but is separate from them because the datetime library
#   cannot handle leap seconds.
#
#   Aside from the I/O routines, every argument to every function can be either
#   a scalar or something array-like, i.e, a numpy array, a tuple or a list.
#   Arguments other than scalars are converted to numpy arrays, the arrays are
#   broadcasted to the same shape if necessary, and the complete array(s) of
#   results is/are returned.
#
# Mark R. Showalter
# PDS Rings Node
# August 2011
#
# 12/31/11 (MRS) - Removed julian_isoparser based on indications that its
#   performance was unacceptably slow. New ISO routines parse the strings
#   without resorting to pyparsing, and also support array-like arguments. Also
#   added routine tai_from_iso().
#
# 1/11/12 (MRS) - Added the new leap second for July 1, 2012.
#
# 1/17/12 (BSW) - subtracted 12 hours from tdb on tdb_from_tai (and added 12
#   hours for the reverse in tai_from_tdb) to deal with J2000 starting from
#   noon on 1/1/2000, not midnight.
################################################################################

import numpy as np
import textkernel as tk
import julian_dateparser as jdp
# import julian_isoparser as iso -- replaced by faster parser
import datetime as dt
import pyparsing
import unittest
import os

################################################################################
# Initialization
#
# At load time, this file looks for an environment variable SPICE_LSK_FILEPATH.
# If found, this file is used to initialize the module. Otherwise, the text
# defined internally as SPICE_LSK_TEXT is used.
################################################################################

# Define the text from the latest LSK file, naif0009.tls
SPICE_LSK_DICT = {
    "DELTA_T_A": 32.184,
    "K": 1.657e-3,
    "EB": 1.671e-2,
    "M": (6.239996, 1.99096871e-7),
    "DELTA_AT": (10, dt.date(1972,1,1),
                 11, dt.date(1972,7,1),
                 12, dt.date(1973,1,1),
                 13, dt.date(1974,1,1),
                 14, dt.date(1975,1,1),
                 15, dt.date(1976,1,1),
                 16, dt.date(1977,1,1),
                 17, dt.date(1978,1,1),
                 18, dt.date(1979,1,1),
                 19, dt.date(1980,1,1),
                 20, dt.date(1981,7,1),
                 21, dt.date(1982,7,1),
                 22, dt.date(1983,7,1),
                 23, dt.date(1985,7,1),
                 24, dt.date(1988,1,1),
                 25, dt.date(1990,1,1),
                 26, dt.date(1991,1,1),
                 27, dt.date(1992,7,1),
                 28, dt.date(1993,7,1),
                 29, dt.date(1994,7,1),
                 30, dt.date(1996,1,1),
                 31, dt.date(1997,7,1),
                 32, dt.date(1999,1,1),
                 33, dt.date(2006,1,1),
                 34, dt.date(2009,1,1),
                 35, dt.date(2012,7,1))}

# Define the static variables needed for TAI-ET conversions
global DELTET_T_A, DELTET_K, DELTET_EB, DELTET_M0, DELTET_M1
DELTET_T_A = 0.     # indicates un-initialized data
DELTET_K   = 0.
DELTET_EB  = 0.
DELTET_M0  = 0.
DELTET_M1  = 0.

# Define the static variables needed for UTC-TAI conversions
global LS_YEAR0, LS_YEARS, LS_ARRAY1D, LS_ARRAY2D
LS_YEAR0 = 0        # indicates un-initialized data
LS_YEARS = 0
LS_ARRAY1D = None
LS_ARRAY2D = None

def load_from_dict(dict):
    """Loads the SPICE LSK parameters from the given dictionary. The dictionary
    is that returned by textkernel.from_file()["DELTET"].
    """

    global DELTET_T_A, DELTET_K, DELTET_EB, DELTET_M0, DELTET_M1
    global LS_YEAR0, LS_YEARS, LS_ARRAY1D, LS_ARRAY2D

    # Look up the needed variables and save them as globals
    DELTET_T_A = dict["DELTA_T_A"]
    DELTET_K   = dict["K"]
    DELTET_EB  = dict["EB"]

    (DELTET_M0, DELTET_M1) = dict["M"]

    # Construct a static array of (TAI minus UTC), the number of elapsed leap
    # seconds, and save them indexed by [year,halfyear]...

    # Get the list of leapseconds from the kernel
    delta_at = dict["DELTA_AT"]
    LS_YEAR0 = delta_at[1].year - 1     # subtract one so the first tabulated
                                        # year has zero leapseconds.
    LS_YEARS = delta_at[-1].year - LS_YEAR0 + 1
                                        # add one so years indexed is inclusive

    # Construct an array indexed by halfyear
    LS_ARRAY1D = np.zeros(2*LS_YEARS, dtype="int")

    for i in range(0, len(delta_at), 2):
        date = delta_at[i+1]
        index = 2 * (date.year - LS_YEAR0) + (date.month - 1)/6
        LS_ARRAY1D[index:] = delta_at[i]

    # Convert to an array indexed by [year,halfyear]
    # These arrays share the same data
    LS_ARRAY2D = LS_ARRAY1D.reshape((LS_YEARS,2))

def load_from_kernel(filespec):
    """Loads the SPICE LSK parameters from the given text kernel."""

    # Load the kernel as a dictionary
    load_from_dict(tk.from_file(filespec)["DELTET"])

# INITIALIZE PARAMETERS...

load_from_dict(SPICE_LSK_DICT)

try:
    filespec = os.environ["SPICE_LSK_FILEPATH"]
    load_from_kernel(filespec)
except KeyError: pass

########################################
# UNIT TESTS
########################################

class Test_Initialize(unittest.TestCase):

    def runTest(self):
        self.assertEqual(DELTET_T_A, 32.184,
            'DELTET_T_A value is wrong')
        self.assertEqual(DELTET_M0, 6.239996,
            'DELTET_M0 value is wrong')
        self.assertEqual(LS_YEAR0, 1971,
            'Leapseconds list does not start in 1971')
        self.assertEqual(LS_ARRAY2D[0,0], 0,
            'LS_ARRAY2D does not start at zero')
        self.assertEqual(LS_ARRAY2D[1999 - LS_YEAR0,0], 32,
            'LS_ARRAY2D returns the wrong value for early 1999')
        self.assertEqual(LS_ARRAY2D[1998 - LS_YEAR0,1], 31,
            'LS_ARRAY2D returns the wrong value for late 1998')

################################################################################
# Calendar conversions
#   Algorithms from http://alcor.concordia.ca/~gpkatch/gdate-algorithm.html
#
# day     = number of days elapsed since January 1, 2000
# month   = number of months elapsed since January 2000
# (y,m,d) = year, month (1-12), day (1-31)
# (y,d)   = year and day-of-year (1-366)
# (y,m)   = year and month number (1-12)
#
# All function operate on either scalars or arrays. If given scalars, they
# return scalars; if given anything array-like, they return arrays.
################################################################################

def day_from_ymd(y, m, d):
    """Day number from year, month and day. All must be integers. Supports
    scalar or array arguments."""

    if np.shape(y) != () or np.shape(m) != () or np.shape(d) != ():
        (y, m, d) = np.broadcast_arrays(y, m, d)

    m = (m + 9) % 12
    y = y - m/10
    return 365*y + y/4 - y/100 + y/400 + (m*306 + 5)/10 + d - 730426

########################################

def ymd_from_day(day):
    """Year, month and day from day number. Supports scalar or array arguments.
    Inputs must be integers."""

    # Coerce to array if necessary
    shape = np.shape(day)
    if shape != (): day = np.asarray(day)

    # Execute the magic algorithm
    g = day + 730425
    y = (10000*g + 14780)/3652425
    ddd = g - (365*y + y/4 - y/100 + y/400)

    # Use scalar version of test...
    if shape == ():
        if ddd < 0:
            y -= 1
            ddd = g - (365*y + y/4 - y/100 + y/400)
    # ...or array version of test
    else:
        y[ddd < 0] -= 1
        ddd = g - (365*y + y/4 - y/100 + y/400)

    mi = (100*ddd + 52)/3060
    mm = (mi + 2)%12 + 1
    y = y + (mi + 2)/12
    dd = ddd - (mi*306 + 5)/10 + 1

    return (y, mm, dd)

########################################

def yd_from_day(day):
    """Year and day-of-year from day number. Supports scalar or array arguments.
    """

    (y,m,d) = ymd_from_day(day)
    return (y, day - day_from_ymd(y,1,1) + 1)

########################################

def day_from_yd(y, d):
    """Day number from year and day-of-year. Supports scalar or array arguments.
    """

    if np.shape(y) != () or np.shape(d) != ():
        (y, d) = np.broadcast_arrays(y, d)

    return day_from_ymd(y,1,1) + d - 1

########################################

def month_from_ym(y, m):
    """Number of elapsed months since January 2000. Supports scalar or array
    arguments."""

    if np.shape(y) != () or np.shape(m) != ():
        (y,m) = np.broadcast_arrays(y, m)

    return 12*(y - 2000) + (m - 1)

########################################

def ym_from_month(month):
    """Year and month from the number of elapsed months since January 2000.
    Supports scalar or array arguments."""

    # Coerce to an array if necessary
    if np.shape(month) != (): month = np.asarray(month)

    y = np.floor(month/12).astype("int")
    m = month - 12*y

    y += 2000
    m += 1

    # Convert back to scalar if necessary
    return (y, m)

########################################

def days_in_month(month):
    """Number of days in month. Supports scalar or array arguments.
    """

    if np.shape(month) != (): month = np.asarray(month)

    (y, m) = ym_from_month(month)
    day0 = day_from_ymd(y, m, 1)

    (y, m) = ym_from_month(month + 1)
    day1 = day_from_ymd(y, m, 1)

    return day1 - day0

########################################

def days_in_year(year):
    """Number of days in year. Supports scalar or array arguments.
    """

    if np.shape(year) != (): year = np.asarray(year)

    return day_from_ymd(year+1, 1, 1) - day_from_ymd(year, 1, 1)

########################################
# UNIT TESTS
########################################

class Test_Calendar(unittest.TestCase):

    def runTest(self):

        # day_from_ymd()
        self.assertEqual(day_from_ymd(2000,1,1), 0)
        self.assertEqual(day_from_ymd(2000,2,[27,28,29]).tolist(), [57,58,59])
        self.assertEqual(day_from_ymd(2000,[1,2,3],1).tolist(),    [ 0,31,60])
        self.assertEqual(day_from_ymd([2000,2001,2002],1,1).tolist(),
                                                                   [0,366,731])

        # ymd_from_day()
        self.assertEqual(ymd_from_day(0),   (2000,1,1))
        self.assertEqual(ymd_from_day(60),  (2000,3,1))
        self.assertEqual(ymd_from_day(365), (2000,12,31))
        self.assertEqual(ymd_from_day(366), (2001,1,1))

        # yd_from_day()
        self.assertEqual(yd_from_day(0), (2000,1))
        self.assertEqual(yd_from_day(365), (2000,366))

        # A large number of dates, spanning > 200 years
        daylist = range(-40000,40000,83)

        # Convert to ymd and back
        (ylist, mlist, dlist) = ymd_from_day(daylist)
        test_daylist = day_from_ymd(ylist, mlist, dlist)

        self.assertTrue(np.all(test_daylist == daylist),
            "Large-scale conversion from day to YMD and back failed")

        # Make sure every month is in range
        self.assertTrue(np.all(mlist >= 1), "Month-of-year < 1 found")
        self.assertTrue(np.all(mlist <= 12), "Month-of-year > 12 found")

        # Make sure every day is in range
        self.assertTrue(np.all(dlist >= 1), "Day < 1 found")
        self.assertTrue(np.all(dlist <= 31), "Day > 31 found")

        # Another large number of dates, spanning > 200 years
        daylist = range(-40001,40000,79)

        # Convert to yd and back
        (ylist, dlist) = yd_from_day(daylist)
        test_daylist = day_from_yd(ylist, dlist)

        self.assertTrue(np.all(test_daylist == daylist))

        # Make sure every day is in range
        self.assertTrue(np.all(dlist >= 1), "Day < 1 found")
        self.assertTrue(np.all(dlist <= 366), "Day > 366 found")

        # A large number of months, spanning > 200 years
        monthlist = range(-15002,15000,19)

        # Convert to ym and back
        (ylist, mlist) = ym_from_month(monthlist)
        test_monthlist = month_from_ym(ylist, mlist)

        self.assertTrue(np.all(test_monthlist == monthlist))

        # Make sure every month is in range
        self.assertTrue(np.all(mlist >= 1), "Month-of-year < 1 found")
        self.assertTrue(np.all(mlist <= 12), "Month-of-year > 12 found")

        # Check the days in each January
        mlist = range(month_from_ym(1980,1),month_from_ym(2220,1),12)
        self.assertTrue(np.all(days_in_month(mlist) == 31),
            "Not every January has 31 days")

        # Check the days in each April
        mlist = range(month_from_ym(1980,4),month_from_ym(2220,4),12)
        self.assertTrue(np.all(days_in_month(mlist) == 30),
            "Not every April has 30 days")

        # Check the days in each year
        ylist = np.arange(1890, 2210)
        dlist = days_in_year(ylist)
        self.assertTrue(np.all((dlist == 365) | (dlist == 366)),
            "Not every year has 365 or 366 days")

        # Every leap year is a multiple of four
        select = np.where(dlist == 366)
        self.assertTrue(np.all(ylist[select]%4 == 0),
            "Not every leapyear is a multiple of four")

        # February always has 29 days in a leapyear
        self.assertTrue(np.all(days_in_month(month_from_ym(ylist[select],2))
            == 29), "Not every leap year February has 29 days")

        # February always has 28 days otherwise
        select = np.where(dlist == 365)
        self.assertTrue(np.all(days_in_month(month_from_ym(ylist[select],2))
            == 28), "Not every non-leap year February has 28 days")

################################################################################
# Leapsecond routines
################################################################################

def leapsecs_from_ym(y, m):
    """Returns the number of elapsed leapseconds for a given year and month.
    Supports scalar or array arguments."""

    # Scalar version...
    if np.shape(y) == () and np.shape(m) == ():
        index = 2*(y - LS_YEAR0) + (m-1)/6
        if index <= 0:               return LS_ARRAY1D[0]
        if index >= LS_ARRAY1D.size: return LS_ARRAY1D[-1]
        return LS_ARRAY1D[index]

    # Array version...
    (y,m) = np.broadcast_arrays(y,m)

    index = 2*(y - LS_YEAR0) + (m-1)/6
    index[index < 0] = 0
    index[index >= LS_ARRAY1D.size] = LS_ARRAY1D.size - 1
    return LS_ARRAY1D[index]

########################################

def leapsecs_from_day(day):
    """Returns the number of elapsed leapseconds for a given number of days
    elapsed since January 1, 2000. Supports scalar or array arguments."""

    (y,m,d) = ymd_from_day(day)
    return leapsecs_from_ym(y,m)

########################################

def seconds_on_day(day, leapseconds=True):
    """Returns the number of seconds duration for the given day number since
    January 1, 2000. Supports scalar or array arguments."""

    if not leapseconds: return 86400    # This can be a scalar because it will
                                        # be casted to whatever shape is needed

    shape = np.shape(day)
    if shape != (): day = np.asarray(day)

    return 86400 + leapsecs_from_day(day+1) - leapsecs_from_day(day)

########################################
# UNIT TESTS
########################################

class Test_Leapseconds(unittest.TestCase):

    def runTest(self):

        # A large number of dates, spanning > 200 years
        daylist = range(-40001,40000,83)

        # Check all seconds are within the range
        self.assertTrue(np.all(seconds_on_day(daylist) >= 86400))
        self.assertTrue(np.all(seconds_on_day(daylist) <= 86401))

        self.assertEqual(seconds_on_day(day_from_ymd(1998,12,31)), 86401)

        # Check case where leap seconds are ignored
        self.assertTrue(np.all(seconds_on_day(daylist,False) == 86400))

        self.assertEqual(seconds_on_day(day_from_ymd(1998,12,31), False), 86400)

################################################################################
# TAI - UTC conversions
################################################################################

def day_sec_from_tai(tai):
    """Returns a number of integer days and the number of elapsed seconds into
    that day, given the number of elapsed seconds since January 1, 2000 TAI.
    Works for scalars or arrays."""

    # Coerce to array if necessary
    shape = np.shape(tai)
    if shape != (): tai = np.asfarray(tai)

    # Make an initial guess at the day and seconds
    day = np.floor(tai/86400).astype("int")     # Must round down
    leapsecs = leapsecs_from_day(day)
    sec = tai - 86400. * day - leapsecs

    # Update the day and seconds if necessary
    # ...scalar version...
    if shape == ():
        if sec < 0.:
            day -= 1
            sec += seconds_on_day(day)

    # ...array version...
    else:
        select = np.where(sec < 0.)
        day[select] -= 1
        sec[select] += seconds_on_day(day[select])

    return (day, sec)

########################################

def tai_from_day(day):
    """Returns a number of elapsed seconds since January 1, 2000 TAI, at the
    beginning of the specified day since January 1, 2000 UTC. Works for scalars
    or arrays."""

    if np.shape(day) != (): day = np.asarray(day)

    (y,m,d) = ymd_from_day(day)
    leapsecs = leapsecs_from_ym(y,m)

    return 86400 * day + leapsecs

########################################
# UNIT TESTS
########################################

class Test_TAI_UTC(unittest.TestCase):

    def runTest(self):

        # Check tai_from_day
        self.assertEqual(tai_from_day(0), 32)
        self.assertEqual(tai_from_day([0,1])[0],    32)
        self.assertEqual(tai_from_day([0,1])[1], 86432)

        #Check day_sec_from_tai
        self.assertEqual(day_sec_from_tai(32.), (0, 0.))
        self.assertEqual(day_sec_from_tai([35.,86435.])[0][0], 0)
        self.assertEqual(day_sec_from_tai([35.,86435.])[0][1], 1)
        self.assertEqual(day_sec_from_tai([35.,86435.])[1][0], 3.)
        self.assertEqual(day_sec_from_tai([35.,86435.])[1][1], 3.)

        # A large number of dates, spanning > 200 years
        daylist = range(-40000,40000,83)

        # Test as a loop
        for day in daylist:
            (test_day, test_sec) = day_sec_from_tai(tai_from_day(day))
            self.assertEqual(test_day, day, "Day mismatch at " + str(day))
            self.assertEqual(test_sec, 0,   "Sec mismatch at " + str(day))

        # Test as an array operation
        (test_day, test_sec) = day_sec_from_tai(tai_from_day(daylist))
        self.assertTrue(np.all(test_day == daylist))
        self.assertTrue(np.all(test_sec == 0))

################################################################################
# Time-of-day conversions
################################################################################

def hms_from_sec(sec):
    """Hour, minute and second from seconds into day. Supports scalar or array
    arguments. Input must be between 0 and 86410, where numbers above 86400 are
    treated as leap seconds."""

    # Coerce to an array if necessary
    shape = np.shape(sec)
    if shape != (): sec = np.asarray(sec)

    # Test for valid range
    if (np.any(sec < 0.)):     raise ValueError("seconds < 0")
    if (np.any(sec > 86410.)): raise ValueError("seconds > 86410")

    h = np.minimum(np.floor(sec/3600).astype("int"), 23)
    t = sec - 3600*h

    m = np.minimum(np.floor(t/60).astype("int"), 59)
    t -= 60*m

    return (h, m, t)

########################################

def sec_from_hms(h, m, s):
    """Seconds into day from hour, minute and second. Supports scalar or array
    arguments."""

    if np.shape(h) != () or np.shape(m) != () or np.shape(s) != 0:
        (h,m,s) = np.broadcast_arrays(h, m, s)

    return 3600*h + 60*m + s

########################################
# UNIT TESTS
########################################

class Test_Time_of_Day(unittest.TestCase):

    def runTest(self):

        #Check hms_from_sec
        self.assertEqual(hms_from_sec(0), (0, 0, 0),
                         "0 is not (0, 0, 0).")
        self.assertEqual(hms_from_sec(86400), (23, 59, 60),
                         "86400 is not (23, 59, 60).")
        self.assertEqual(hms_from_sec(86410), (23, 59, 70),
                         "86410 is not (23, 59, 70).")
        self.assertRaises(ValueError, hms_from_sec, 86410.0000001)
        self.assertRaises(ValueError, hms_from_sec, -1.e-300)

        # Check sec_from_hms
        self.assertEqual(sec_from_hms(0, 0, 0), 0,
                         "(0, 0, 0) is not 0 seconds.")
        self.assertEqual(sec_from_hms(23, 59, 60), 86400,
                         "(23, 59, 60) is not 86400 seconds.")

        # Array tests
        # This makes about 333,000 non-uniformly spaced transcendental numbers
        secs = 86410. * np.sqrt(np.arange(0., 1., 3.e-6))

        # Because HMS times carry extra precision, inversions should be exact
        (h,m,s) = hms_from_sec(secs)
        errors = (sec_from_hms(h,m,s) - secs)
        self.assertTrue(np.all(errors == 0.))

        # Test all seconds
        seclist = range(0,86410)

        # Convert to hms and back
        (h, m, t) = hms_from_sec(seclist)
        test_seclist = sec_from_hms(h, m, t)

        self.assertTrue(np.all(test_seclist == seclist),
            'Large-scale conversion from sec to hms and back failed')

################################################################################
# TDB - TAI conversions
#
# Extracted from naif0009.tls...
#
# [4]       ET - TAI  =  DELTA_T_A  + K sin E 
# 
# where DELTA_T_A and K are constant, and E is the eccentric anomaly of the 
# heliocentric orbit of the Earth-Moon barycenter. Equation [4], which ignores 
# small-period fluctuations, is accurate to about 0.000030 seconds.
# 
# The eccentric anomaly E is given by 
# 
# [5]       E = M + EB sin M
# 
# where M is the mean anomaly, which in turn is given by 
# 
# [6]       M = M  +  M t
#                0     1
# 
# where t is the number of ephemeris seconds past J2000.
#
# in the end, subtract 12 hours as J2000 starts at noon on 1/1/2000, not
# midnight
################################################################################

def tdb_from_tai(tai, iters=2):
    """Converts from TAI to TDB. Operates on either a single scalar or an
    arbitrary array of values. Accurate to about 30 microseconds but an exact
    inverse for function tai_from_tdb().

    The default value of 2 iterations appears to give full double-precision
    convergencec for every possible case."""

    if np.shape(tai) != (): tai = np.asfarray(tai)

    # Solve:
    #   tdb = tai + DELTA + K sin(E)
    #   E = M + EB sin(M)
    #   M = M0 + M1 * tdb

    # Solve for
    #   x == DELTA + K sin(E)
    # by iteration. It's fast.
    
    x = DELTET_T_A
    for iter in range(iters):
        m = DELTET_M0 + DELTET_M1 * (x + tai)
        e = m + DELTET_EB * np.sin(m)
        x = DELTET_T_A + DELTET_K * np.sin(e)

    return x + tai - 43200.

########################################

def tai_from_tdb(tdb):
    """Converts from TDB to TAI. Operates on either a single scalar or an
    arbitrary array of values. An exact solution(); no iteration required."""

    tdb += 43200.   # add 12 hours as tdb is respect to noon on 1/1/2000
    if np.shape(tdb) != (): tdb = np.asfarray(tdb)

    #   tai = tdb - DELTA - K sin(E)
    #   E = M + EB sin(M)
    #   M = M0 + M1 * tdb

    m = DELTET_M0 + DELTET_M1 * tdb
    return tdb - DELTET_T_A - DELTET_K * np.sin(m + DELTET_EB * np.sin(m))

########################################
# UNIT TESTS
########################################

class Test_TDB_TAI(unittest.TestCase):

    def runTest(self):

        # Check tdb_from_tai
        self.assertTrue(abs(tdb_from_tai(tai_from_day(0)) -
                            64.183927284731055) < 1.e-15)

        # Check tai_from_tdb
        self.assertTrue(abs(tai_from_tdb(64.183927284731055)
                                         - tai_from_day(0)) < 1.e15)

        # Test inversions around tdb = 0.
        # A list of two million small numbers spanning 2 sec
        secs = 2.
        tdbs = np.arange(-secs, secs, 1.e-6 * secs)
        errors = tdb_from_tai(tai_from_tdb(tdbs)) - tdbs
        self.assertTrue(np.all(errors <  1.e-14 * secs))
        self.assertTrue(np.all(errors > -1.e-14 * secs))

        # Now make sure we get the exact same results when we replace arrays by
        # scalars
        for i in range(0, tdbs.size, 1000):
            self.assertEqual(errors[i],
                             tdb_from_tai(tai_from_tdb(tdbs[i])) - tdbs[i])

        # A list of two million bigger numbers spanning ~ 20 days
        secs = 20. * 86400.
        tdbs = np.arange(-secs, secs, 1.e-6 * secs)
        errors = tdb_from_tai(tai_from_tdb(tdbs)) - tdbs
        self.assertTrue(np.all(errors <  1.e-15 * secs))
        self.assertTrue(np.all(errors > -1.e-15 * secs))

        # A list of two million still bigger numbers spanning ~ 2000 years
        secs = 2000. * 365. * 86400.
        tdbs = np.arange(-secs, secs, 1.e-6 * secs)
        errors = tdb_from_tai(tai_from_tdb(tdbs)) - tdbs
        self.assertTrue(np.all(errors <  1.e-15 * secs))
        self.assertTrue(np.all(errors > -1.e-15 * secs))

################################################################################
# Julian Date conversions
################################################################################

MJD_OF_EPOCH_2000 = 51544
JD_OF_EPOCH_2000 = 2451544.5
JD_MINUS_MJD = JD_OF_EPOCH_2000 - MJD_OF_EPOCH_2000

# Integer versions

def mjd_from_day(day):
    """Returns the Modified Julian Date for a specified day number relative to
    January 1, 2000. Works for scalars or arrays, expected to be integers."""

    if np.shape(day) != (): day = np.asarray(day)
    return day + MJD_OF_EPOCH_2000

def day_from_mjd(mjd):
    """Returns the day number relative to January 1, 2000 for the given Modified
    Julian Day. Works for scalars or arrays, expected to be integers."""

    if np.shape(mjd) != (): mjd = np.asarray(mjd)
    return mjd - MJD_OF_EPOCH_2000

# Floating-point versions

def jd_from_time(time):
    """Returns the Julian Date for a specified number of seconds relative to
    midnight on January 1, 2000. Works for scalars or arrays. This definition of
    Julian Date assumes every day contains 86400 seconds; it ignores leap
    seconds."""

    if np.shape(time) != (): tai = np.asfarray(time)
    return time/86400. + JD_OF_EPOCH_2000

def mjd_from_time(time):
    """Returns the Modified Julian Date for a specified number of seconds
    relative to midnight on January 1, 2000. Works for scalars or arrays. This
     definition of Julian Date assumes every day contains 86400 seconds; it
    ignores leap seconds."""

    if np.shape(time) != (): time = np.asfarray(time)
    return time/86400. + MJD_OF_EPOCH_2000

def time_from_jd(jd):
    """Returns the elapsed seconds relative to midnight on January 1, 2000 from
    the Julian Date. Works for scalars or arrays. This definition of Julian Date
    assumes every day contains 86400 seconds; it ignores leap seconds."""

    if np.shape(jd) != (): jd = np.asfarray(jd)
    return (jd - JD_OF_EPOCH_2000) * 86400.

def time_from_mjd(mjd):
    """Returns the elapsed seconds relative to midnight on January 1, 2000 from
    the Modified Julian Date. Works for scalars or arrays. This definition of
    MJD assumes every day contains 86400 seconds; it ignores leap seconds."""

    if np.shape(mjd) != (): mjd = np.asfarray(mjd)
    return (mjd - MJD_OF_EPOCH_2000) * 86400.

# Floating-point UTC versions

def jd_from_day_sec(day, sec, leapseconds=True):
    """Returns the Julian Date for a given UTC day and seconds. Works for
    scalars or arrays. This definition of Julian Date includes leap seconds, so
    some days are longer than others."""

    # Broadcast arrays to the same shape if necessary
    if np.shape(day) != () or np.shape(sec) != ():
        (day, sec) = np.broadcast_arrays(day, sec)
        sec = sec.astype("float")

    return day + sec/seconds_on_day(day, leapseconds) + JD_OF_EPOCH_2000

def mjd_from_day_sec(day, sec, leapseconds=True):
    """Returns the Modified Julian Date for a given UTC day and seconds. Works
    for scalars or arrays. This definition of MJD includes leap seconds, so some
    days are longer than others."""

    # Broadcast arrays to the same shape if necessary
    if np.shape(day) != () or np.shape(sec) != ():
        (day, sec) = np.broadcast_arrays(day, sec)
        sec = sec.astype("float")

    return day + sec/seconds_on_day(day, leapseconds) + MJD_OF_EPOCH_2000

def day_sec_from_jd(jd, leapseconds=True):
    """Returns a UTC day number and seconds based on a Julian Date. Works for
    scalars or arrays. This definition of Julian Date allows for leap seconds,
    so some days are longer than others."""

    # Coerce to array if array-like
    if np.shape(jd) != (): jd = np.asfarray(jd)

    delta = jd - JD_OF_EPOCH_2000
    day = np.floor(delta).astype("int")
    sec = seconds_on_day(day, leapseconds) * (delta - day)

    return (day, sec)

def day_sec_from_mjd(mjd, leapseconds=True):
    """Returns a UTC day number and seconds based on a Julian Date. Works for
    scalars or arrays. This definition of Julian Date allows for leap seconds,
    so some days are longer than others."""

    # Coerce to array if array-like
    if np.shape(mjd) != (): mjd = np.asfarray(mjd)

    delta = mjd - MJD_OF_EPOCH_2000
    day = np.floor(delta).astype("int")
    sec = seconds_on_day(day, leapseconds) * (delta - day)

    return (day, sec)

########################################
# UNIT TESTS
########################################

class Test_JD_MJD(unittest.TestCase):

    def runTest(self):

        # Test integer conversions...
        self.assertEqual(mjd_from_day(0), 51544)
        self.assertEqual(day_from_mjd(51545), 1)

        self.assertTrue(np.all(mjd_from_day(range(10)) ==
                               np.arange(10) + 51544))

        self.assertTrue(np.all(day_from_mjd(range(10)) ==
                               np.arange(10) - 51544))

        # Test MJD floating-point conversions spanning 1000 years
        span = 1000. * 365.25
        mjdlist = np.arange(-span, span, np.pi) + MJD_OF_EPOCH_2000

        test = mjd_from_time(time_from_mjd(mjdlist))
        error = np.max(np.abs(test - mjdlist))
        self.assertTrue(np.max(np.abs(test - mjdlist)) < span * 1.e-15)

        for mjd in mjdlist[:100]:
            error = abs(mjd_from_time(time_from_mjd(mjd)) - mjd)
            self.assertTrue(error < span * 1.e-15)

        (day,sec) = day_sec_from_mjd(mjdlist)
        test = mjd_from_day_sec(day,sec)
        error = np.abs(test - mjdlist)
        self.assertTrue(np.max(np.abs(test - mjdlist)) < span * 1.e-15)

        for mjd in mjdlist[:100]:
            (day,sec) = day_sec_from_mjd(mjd)
            error = abs(mjd_from_day_sec(day,sec) - mjd)
            self.assertTrue(error < span * 1.e-15)

        # Test JD floating-point conversions spanning 100 years
        span = 100. * 365.25
        jdlist = np.arange(-span, span, np.pi/10.) + JD_OF_EPOCH_2000

        test = jd_from_time(time_from_jd(jdlist))
        error = np.max(np.abs(test - jdlist))
        self.assertTrue(np.max(np.abs(test - jdlist)) < JD_OF_EPOCH_2000*1.e-15)

        for jd in jdlist[:100]:
            error = abs(jd_from_time(time_from_jd(jd)) - jd)
            self.assertTrue(error < span * 1.e-15)

        (day,sec) = day_sec_from_jd(jdlist)
        test = jd_from_day_sec(day,sec)
        error = np.abs(test - jdlist)
        self.assertTrue(np.max(np.abs(test - jdlist)) < JD_OF_EPOCH_2000*1.e-15)

        for jd in jdlist[:100]:
            (day,sec) = day_sec_from_jd(jd)
            error = abs(jd_from_day_sec(day,sec) - jd)
            self.assertTrue(error < span * 1.e-15)

################################################################################
# Time System conversions
#
# UTC day and second allow for leap seconds.
# TAI day and second does not allow for leapseconds. Every day has exactly 86400
#       seconds. TAI and UTC were equal prior to 1972.
# TDB is TAI plus an offset and allowance for relativistic effects.
################################################################################

def utc_from_day_sec_as_type(day, sec, time_type="UTC"):

    # Conversion UTC to UCT is easy
    if time_type == "UTC": return (day, sec)

    # Broadcast to arrays of the same shape if necessary
    if np.shape(day) != () or np.shape(sec) != ():
        (day,sec) = np.broadcast_arrays(day,sec)

    # Conversion from day and second to TAI ignores leap seconds
    if time_type == "TAI":
        tai = 86400. * day + sec
        return day_sec_from_tai(tai)

    # Conversion from TDB requires a relativistic correction to TAI
    if time_type == "TDB":
        tdb = 86400. * day + sec
        tai = tai_from_tdb(tdb)
        return day_sec_from_tai(tai)

    raise ValueError("Unrecognized time_type: " + time_type)

def day_sec_as_type_from_utc(day, sec, time_type="UTC"):

    # Conversion UTC to UCT is easy
    if time_type == "UTC": return (day, sec)

    # Broadcast to arrays of the same shape if necessary
    if np.shape(day) != () or np.shape(sec) != ():
        (day,sec) = np.broadcast_arrays(day,sec)

    # Conversion from TAI to day and second ignores leap seconds
    if time_type == "TAI":
        tai = tai_from_day(day) + sec
        day = np.floor(tai / 86400.)
        sec = tai - 86400. * day
        return (day, sec)

    # Conversion to TDB requires a relativistic correction to TAI
    if time_type == "TDB":
        tai = tai_from_day(day) + sec
        tdb = tdb_from_tai(tai)
        day = np.floor(tdb / 86400.)
        sec = tdb - 86400. * day
        return (day, sec)

    raise ValueError("Unrecognized time_type: " + time_type)

########################################
# UNIT TESTS
########################################

class Test_Conversions(unittest.TestCase):

    def runTest(self):

        # TAI tests...

        # TAI was 31-32 seconds ahead of UTC in 1999,2000,2001
        (day,sec) = day_sec_as_type_from_utc((-366,0,366),0.,"TAI")
        self.assertTrue(np.all(day == (-366,0,366)))
        self.assertTrue(np.all(sec == (31.,32.,32.)))

        # Inverse of the above
        (day,sec) = utc_from_day_sec_as_type((-366,0,366),32.,"TAI")
        self.assertTrue(np.all(day == (-366,0,366)))
        self.assertTrue(np.all(sec == (1.,0.,0.)))

        # TAI jumped 10 seconds ahead of UTC at the beginning of 1972
        (day,sec) = day_sec_as_type_from_utc(day_from_ymd(1972,1,1),0,"TAI")
        self.assertEqual(sec,10)
        (day,sec) = day_sec_as_type_from_utc(day_from_ymd(1971,12,31),0,"TAI")
        self.assertEqual(sec,0)

        # Inverses of the above
        (day,sec) = utc_from_day_sec_as_type(day_from_ymd(1972,1,1),10,"TAI")
        self.assertEqual(sec,0)
        (day,sec) = utc_from_day_sec_as_type(day_from_ymd(1971,12,31),0,"TAI")
        self.assertEqual(sec,0)

        # Now do a batch test 1971-2012. Conversions should be exact.
        daylist = range(day_from_ymd(1971,1,1),day_from_ymd(2012,1,1))

        (day,sec) = day_sec_as_type_from_utc(daylist,43200.,"TAI")
        (dtest,stest) = utc_from_day_sec_as_type(day,sec,"TAI")
        self.assertTrue(np.all(dtest == daylist))
        self.assertTrue(np.all(stest == 43200.))

        (day,sec) = day_sec_as_type_from_utc(daylist,0.,"TAI")
        (dtest,stest) = utc_from_day_sec_as_type(day,sec,"TAI")
        self.assertTrue(np.all(dtest == daylist))
        self.assertTrue(np.all(stest == 0.))

        (day,sec) = utc_from_day_sec_as_type(daylist,0.,"TAI")
        (dtest,stest) = day_sec_as_type_from_utc(day,sec,"TAI")
        self.assertTrue(np.all(dtest == daylist))
        self.assertTrue(np.all(stest == 0.))

        # TDB tests...

        self.assertTrue(abs(day_sec_as_type_from_utc(0,0,"TDB")[1]
                            - 64.183927284731055) < 1.e15)
        self.assertTrue(abs(utc_from_day_sec_as_type(0,0,"TDB")[1]
                            + 64.183927284731055) < 1.e15)

        (day,sec) = day_sec_as_type_from_utc(daylist,43200.,"TDB")
        (dtest,stest) = utc_from_day_sec_as_type(day,sec,"TDB")
        self.assertTrue(np.all(dtest == daylist))
        self.assertTrue(np.all(np.abs(stest - 43200.) < 1.e-6))

        (day,sec) = utc_from_day_sec_as_type(daylist,43200.,"TDB")
        (dtest,stest) = day_sec_as_type_from_utc(day,sec,"TDB")
        self.assertTrue(np.all(dtest == daylist))
        self.assertTrue(np.all(np.abs(stest - 43200.) < 1.e-6))

################################################################################
# Formatting Routines
################################################################################

def ymd_format_from_day(day, buffer=None):
    """Returns a date in 'yyyy-mm-dd' format. Supports scalars or arrays.

    Input:
        day         integer or arbitrary array of integers defining day numbers
                    relative to January 1, 2000.
        buffer      an optional string array into which to write the results.
                    Only used if day is an array. Must have sufficient length.
    """

    return _yxd_format_from_day(day, True, buffer)

def yd_format_from_day(day, buffer=None):
    """Returns a date in 'yyyy-ddd' format. Supports scalars or arrays.

    Input:
        day         integer or arbitrary array of integers defining day numbers
                    relative to January 1, 2000.
        buffer      an optional string array into which to write the results.
                    Only used if day is an array. Must have sufficient length.
    """

    return _yxd_format_from_day(day, False, buffer)

def _yxd_format_from_day(day, ymd=True, buffer=None):
    """Support function for ymd and yd ISO date formats."""

    # Translate the days and set up the formatting parameters
    if ymd:
        tuple = ymd_from_day(day)
        fmt = "{:04d}-{:02d}-{:02d}"
        dtype = "|S10"
        lstring = 10
    else:
        tuple = yd_from_day(day)
        fmt = "{:04d}-{:03d}"
        dtype = "|S8"
        lstring = 8

    # Return a scalar
    if np.shape(day) == ():
        return fmt.format(*tuple)   # "*tuple" expands the tuple into its parts

    # Create or check the buffer
    if buffer is None:
        buffer = np.empty(np.shape(day), dtype=dtype)
    else:
        if buffer.shape != np.shape(day):
            raise ValueError("buffer shape does not match day array")
        if lstring > buffer.dtype.itemsize:
            raise ValueError("buffer is too small for the ISO date format")

    # Fill the buffer
    if ymd:
        (y,m,d) = tuple
        for i,value in np.ndenumerate(day):
            buffer[i] = fmt.format(y[i], m[i], d[i])
    else:
        (y,d) = tuple
        for i,value in np.ndenumerate(day):
            buffer[i] = fmt.format(y[i], d[i])

    return buffer

########################################

def hms_format_from_sec(sec, digits=None, suffix="", buffer=None):
    """Returns a time in 'hh:mm:ss[.mmm][Z]' format. Supports scalars or arrays.

    Input:
        day         integer or arbitrary array of integers defining day numbers
                    relative to January 1, 2000.
        sec         the number of seconds into a day, or an arbitrary array
                    thereof; should be less than 86410.
        digits      the number of digits to include after the decimal point; use
                    a negative value or None for for seconds to be rounded to
                    integer.
        suffix      "Z" to include the Zulu time zone indicator.
        buffer      an optional string array into which to write the results.
                    Only used if day is an array. Must have sufficient length.
    """

    (h,m,s) = hms_from_sec(sec)

    if digits is None or digits < 0:
        secfmt = "{:02d}"
        lsec = 2

        # Round seconds to int if necessary
        if np.shape(s) == ():
            if type(s) != type(0):
                s = int((s + 0.5) // 1)
        else:
            if s.dtype != np.dtype("int"):
                s = np.floor(s + 0.5).astype("int")
    else:
        secfmt = "{:0" + str(digits+3) + "." + str(digits) + "f}"
        lsec = 3 + digits

    fmt = ("{:02d}:{:02d}:" + secfmt + "{:s}")

    if suffix != "Z": suffix = ""
    lstring = 6 + lsec + len(suffix)

    if np.shape(sec) == ():
        return fmt.format(h,m,s,suffix)

    if buffer is None:
        buffer = np.empty(np.shape(sec), dtype="|S" + str(lstring))
    else:
        if buffer.shape != np.shape(sec):
            raise ValueError("buffer shape does not match time array")
        if lstring > buffer.dtype.itemsize:
            raise ValueError("buffer is too small for the ISO time format")

    for i,value in np.ndenumerate(sec):
        buffer[i] = fmt.format(h[i], m[i], s[i], suffix)

    return buffer

########################################

def ymdhms_format_from_day_sec(day, sec, sep="T", digits=None, suffix="",
                               buffer=None):
    """Returns a date and time in ISO format 'yyyy-mm-ddThh:mm:ss....'. Works
    for both scalars and arrays.

    Input:
        day         integer or arbitrary array of integers defining day numbers
                    relative to January 1, 2000.
        sec         the number of seconds into a day; should be less than the
                    number of seconds on the associated day. Note that day and
                    sec need not have the same shape, but must be broadcastable
                    to the same shape.
        sep         the character to separate the date from the time. Default is
                    "T" but " " is also allowed.
        digits      the number of digits to include after the decimal point; use
                    a negative value or None for for seconds to be rounded to
                    integer.
        suffix      "Z" to include the Zulu time zone indicator.
        buffer      an optional string array into which to write the results.
                    Only used if day/sec are arrays. If the buffer is provided,
                    the elements must have sufficient length.
    """

    return _yxdhms_format_from_day_sec(day, sec, True, sep, digits, suffix,
                                       buffer)

def ydhms_format_from_day_sec(day, sec, sep="T", digits=None, suffix="",
                              buffer=None):
    """Returns a date and time in ISO format 'yyyy-dddThh:mm:ss....'. Works
    for both scalars and arrays.

    Input:
        day         integer or arbitrary array of integers defining day numbers
                    relative to January 1, 2000.
        sec         the number of seconds into a day; should be less than the
                    number of seconds on the associated day. Note that day and
                    sec need not have the same shape, but must be broadcastable
                    to the same shape.
        sep         the character to separate the date from the time. Default is
                    "T" but " " is also allowed.
        digits      the number of digits to include after the decimal point; use
                    a negative value or None for for seconds to be rounded to
                    integer.
        suffix      "Z" to include the Zulu time zone indicator.
        buffer      an optional string array into which to write the results.
                    Only used if day/sec are arrays. If the buffer is provided,
                    the elements must have sufficient length.
    """

    return _yxdhms_format_from_day_sec(day, sec, False, sep, digits, suffix,
                                       buffer)

def _yxdhms_format_from_day_sec(day, sec, ymd=True, sep="T", digits=None,
                                suffix="", buffer=None):
    """Support function for ymd and yd ISO date-time formats."""

    # Validate the extra characters
    if sep != " ": sep = "T"
    if suffix != "Z": suffix = ""

    # Return a scalar
    if np.shape(day) == () and np.shape(sec) == ():
        return (_yxd_format_from_day(day, ymd) + sep +
                hms_format_from_sec(sec, digits, suffix))

    # Coerce the day and second arrays to the same shape
    (day, sec) = np.broadcast_arrays(day, sec)

    # Determine the sizes of the fields
    if ymd: lday = 10
    else:   lday = 8

    if digits is None or digits < 0:
        lsec = 2
    else:
        lsec = 3 + digits

    lstring = lday + 1 + 6 + lsec + len(suffix)

    # Create or check the buffer
    if buffer is None:
        buffer = np.empty(day.shape, "|S" + str(lstring))
    else:
        if buffer.shape != np.shape(day):
            raise ValueError("buffer shape does not match day/sec arrays")
        if lstring > buffer.dtype.itemsize:
            raise ValueError("buffer is too small for ISO date-time format")
        lstring = buffer.dtype.itemsize

    # Define an alternative dtype that separates the date and the time
    dtype_dict = {"day": ("|S" + str(lday), 0),
                  "sep": ("|S1", lday),
                  "sec": ("|S" + str(lstring - lday - 1), lday+1)}

    b = buffer.view(np.dtype(dtype_dict))

    # Fill in the date, separator and time
    _yxd_format_from_day(day, ymd, buffer=b["day"])
    b["sep"] = sep
    hms_format_from_sec(sec, digits, suffix, buffer=b["sec"])

    return buffer

########################################

def ymdhms_format_from_tai(tai, sep="T", digits=None, suffix="",
                           buffer=None):
    """Returns a date and time in ISO format 'yyyy-mm-ddThh:mm:ss....' given
    seconds TAI. Works for both scalars and arrays.

    Input:
        tai         number of elapsed seconds from TAI January 1, 2000.
        sep         the character to separate the date from the time. Default is
                    "T" but " " is also allowed.
        digits      the number of digits to include after the decimal point; use
                    a negative value or None for for seconds to be rounded to
                    integer.
        suffix      "Z" to include the Zulu time zone indicator.
        buffer      an optional string array into which to write the results.
                    Only used if day/sec are arrays. If the buffer is provided,
                    the elements must have sufficient length.
    """

    (day, sec) = day_sec_from_tai(tai)
    return _yxdhms_format_from_day_sec(day, sec, True, sep, digits, suffix,
                                       buffer)

def ydhms_format_from_tai(tai, sep="T", digits=None, suffix="",
                          buffer=None):
    """Returns a date and time in ISO format 'yyyy-dddThh:mm:ss....'. given
    seconds TAI. Works for both scalars and arrays.

    Input:
        tai         number of elapsed seconds from TAI January 1, 2000.
        sep         the character to separate the date from the time. Default is
                    "T" but " " is also allowed.
        digits      the number of digits to include after the decimal point; use
                    a negative value or None for for seconds to be rounded to
                    integer.
        suffix      "Z" to include the Zulu time zone indicator.
        buffer      an optional string array into which to write the results.
                    Only used if day/sec are arrays. If the buffer is provided,
                    the elements must have sufficient length.
    """

    (day, sec) = day_sec_from_tai(tai)
    return _yxdhms_format_from_day_sec(day, sec, False, sep, digits, suffix,
                                       buffer)

########################################
# UNIT TESTS
########################################

class Test_Formatting(unittest.TestCase):

    def runTest(self):

        # ymd_format_from_day()
        self.assertEqual(ymd_format_from_day(0), "2000-01-01")

        self.assertTrue(np.all(ymd_format_from_day([-365,0,366]) ==
                        np.array(["1999-01-01", "2000-01-01", "2001-01-01"])))

        # yd_format_from_day()
        self.assertEqual(yd_format_from_day(0), "2000-001")

        self.assertTrue(np.all(yd_format_from_day([-365,0,366]) ==
                        np.array(["1999-001", "2000-001", "2001-001"])))
        
        # Check if yd_format_from_day start from 2000-001
        self.assertEqual(yd_format_from_day(0), "2000-001")
       
        # Check if one day is 86400 seconds
        self.assertEqual(hms_format_from_sec(86400), "23:59:60")

        # Check if hms_format_from_sec end with 86410
        self.assertEqual(hms_format_from_sec(86410), "23:59:70")
        
        # Check if hms_format_from_sec returns the correct format.
        self.assertEqual(hms_format_from_sec(0), "00:00:00")
        self.assertEqual(hms_format_from_sec(0,3), "00:00:00.000")
        self.assertEqual(hms_format_from_sec(0,3,'Z'), "00:00:00.000Z")
        
        # Check if hms_format_from_sec accepts seconds over 86410
        self.assertRaises(ValueError, hms_format_from_sec, 86411) #!!!

        # Check if ymdhms_format_from_day_sec returns the correct format.
        self.assertEqual(ymdhms_format_from_day_sec(0,0),
                         "2000-01-01T00:00:00")
        self.assertEqual(ymdhms_format_from_day_sec(0,0,'T',3),
                         "2000-01-01T00:00:00.000")
        self.assertEqual(ymdhms_format_from_day_sec(0,0,'T',3,'Z'),
                         "2000-01-01T00:00:00.000Z")
        self.assertEqual(ymdhms_format_from_day_sec(0,0,'T',None),
                         "2000-01-01T00:00:00")
        self.assertEqual(ymdhms_format_from_day_sec(0,0,'T',None,'Z'),
                         "2000-01-01T00:00:00Z")

        self.assertTrue(np.all(ymdhms_format_from_day_sec([0,366],[0,43200]) ==
                    np.array(("2000-01-01T00:00:00", "2001-01-01T12:00:00"))))

        # Check TAI formatting
        # The 32's below are for the offset between TAI and UTC
        self.assertTrue(np.all(ydhms_format_from_tai([32.,366.*86400.+32.]) ==
                    np.array(("2000-001T00:00:00", "2001-001T00:00:00"))))

################################################################################
# ISO format parsers
################################################################################

def day_from_iso(strings, validate=True):
    """Returns a day number based on a parsing of a date string in ISO format.
    The format is strictly required to be either yyyy-mm-dd or yyyy-ddd.

    Now revised to avoid the slow julian_isoparser routines. It should be very
    fast. It also works for lists or arrays of arbitrary shape, provided every
    item uses the same format. Note that syntax is no longer checked in detail.

    If validate=True, then the syntax and year/month/day values are checked more
    carefully.
    """

    # Old, slow procedure...
    #
    # Give the list a zero month entry for the year and day-of-year case
    # list = [["MONTH",0]] + iso.ISO_DATE.parseString(string).asList()
    # dict = _dict_from_parselist(list)
    # 
    # return _day_from_dict(dict)

    strings = np.array(strings)

    if validate:
        if " " in str(buffer(strings)):
            raise ValueError("blank character in ISO date")

    # yyyy-mm-dd case:
    if strings.dtype == np.dtype("|S10"):
        dtype_dict = {"y": ("|S4",0),
                      "m": ("|S2",5),
                      "d": ("|S2",8)}
        if validate:
            dtype_dict["dash1"] = ("|S1",4)
            dtype_dict["dash2"] = ("|S1",7)

        strings.dtype = np.dtype(dtype_dict)

        y = strings["y"].astype("int")
        m = strings["m"].astype("int")
        d = strings["d"].astype("int")

        if validate:
            if (np.any(strings["dash1"] != "-") or
                np.any(strings["dash2"] != "-")):
                    raise ValueError("invalid ISO date punctuation")

            if (np.any(y <  1) or
                np.any(m <  1) or
                np.any(m > 12) or
                np.any(d <  1) or
                np.any(d > days_in_month(month_from_ym(y,m)))):
                    raise ValueError("invalid numeric value in ISO date")

        return day_from_ymd(y,m,d)

    # yyyy-ddd case:
    if strings.dtype == np.dtype("|S8"):
        dtype_dict = {"y": ("|S4",0),
                      "d": ("|S3",5)}
        if validate:
            dtype_dict["dash"] = ("|S1",4)

        strings.dtype = np.dtype(dtype_dict)

        y = strings["y"].astype("int")
        d = strings["d"].astype("int")

        if validate:
            if np.any(strings["dash"] != "-"):
                raise ValueError("invalid ISO date punctuation")

            if (np.any(y < 1) or
                np.any(d < 1) or
                np.any(d > days_in_year(y))):
                    raise ValueError("invalid numeric value in ISO date")

        return day_from_yd(y,d)

    # Invalid string length
    raise ValueError("invalid ISO date format: " + strings.ravel()[0])

########################################

def sec_from_iso(strings, validate=True):
    """Returns a second value based on a parsing of a time string in ISO format.
    The format is strictly required to be hh:mm:ss[.s...][Z].

    Now revised to avoid the slow julian_isoparser routines. It should be very
    fast. It also works for lists or arrays of arbitrary shape, provided every
    item uses the same format. By default, the syntax is no longer checked in
    detail.

    If validate=True, then the syntax and hour/minute/second values are checked
    more carefully.
    """

    # Old, slow procedure...
    #
    # list = iso.ISO_TIME.parseString(string).asList()
    # dict = _dict_from_parselist(list)
    # 
    # return _sec_from_dict(dict)

    # Convert to an array of strings
    strings = np.array(strings)

    if validate:
        merged = str(buffer(strings))
        if " " in merged or "-" in merged:
            raise ValueError("blank character in ISO date")

    # Prepare a dictionary to define the string format
    dtype_dict = {"h": ("|S2",0),
                  "m": ("|S2",3),
                  "s": ("|S2",6)}

    if validate:
        dtype_dict["colon1"] = ("|S1", 2)
        dtype_dict["colon2"] = ("|S1", 5)

    # Get the first string. Every subsequent string is assumed to match in
    # format.
    first = str(strings.ravel()[0])
    lstring = len(first)

    # Check for a trailing "Z" to ignore
    has_z = first[-1] == "Z"
    if has_z:
        lstring -= 1
        dtype_dict["z"] = ("|S1", lstring)

    # Check for a period
    has_dot = (lstring > 8)
    if has_dot:
        dtype_dict["dot"] = ("|S1", 8)

    # Check for fractional seconds
    lfrac = lstring - 9
    has_frac = lfrac > 0
    if has_frac:
        dtype_dict["f"] = ("|S" + str(lfrac), 9)

    # Extract hours, minutes, seconds
    strings.dtype = np.dtype(dtype_dict)
    h = strings["h"].astype("int")
    m = strings["m"].astype("int")
    s = strings["s"].astype("int")

    # Extract the fractional part of the seconds if necessary
    if has_frac:
        f = strings["f"].astype("int")
        s = s + f / (10.**lfrac)
    elif has_dot:
        s = s.astype("float")

    if validate:
        if (np.any(strings["colon1"] != ":") or
            np.any(strings["colon2"] != ":")):
                raise ValueError("invalid ISO time punctuation")

        if has_z:
            if np.any(strings["z"] != "Z"):
                raise ValueError("invalid ISO time punctuation")

        if has_dot:
            if np.any(strings["dot"] != "."):
                raise ValueError("invalid ISO time punctuation")

        if (np.any(h >  23) or
            np.any(m >  59) or
            np.any(s >= 70)):
                raise ValueError("invalid numeric value in ISO time")

        if strings.shape == ():
            if s >= 60:
                if h != 23 or m != 59:
                    raise ValueError("invalid numeric value in ISO time")
        else:
            mask = (s >= 60)
            if np.any(h[mask] != 23) or np.any(m[mask] != 59):
                raise ValueError("invalid numeric value in ISO time")

    return sec_from_hms(h,m,s)

########################################

def day_sec_from_iso(strings, validate=True):
    """Returns a day and second based on a parsing of the string in ISO
    date-time format. The format is strictly enforced to be an ISO date plus an
    ISO time, separated by a single space or a "T"."""

    # Old, slow procedure...
    #
    # Give the default entries in case they are needed
    # list = [["MONTH",0]] + iso.ISO_DATETIME.parseString(string).asList()
    # dict = _dict_from_parselist(list)
    #
    # day = _day_from_dict(dict)
    # sec = _sec_from_dict(dict, day, True, validate)
    # 
    # return (day, sec)

    strings = np.array(strings)

    # Check for a T or blank separator
    first = str(strings.ravel()[0])

    csep = "T"
    isep = first.find(csep)

    if isep == -1:
        csep = " "
        isep = first.find(csep)

    # If no separator is found, assume it is just a date
    if isep == -1:
        return (day_from_iso(strings, validate), 0)

    # Otherwise, parse the date and time separately
    dtype_dict = {"day": ("|S" + str(isep), 0),
                  "sec": ("|S" + str(len(first) - isep - 1), isep+1)}

    if validate:
        dtype_dict["sep"] = ("|S1", isep)

    strings.dtype = np.dtype(dtype_dict)
    day = day_from_iso(strings["day"], validate)
    sec = sec_from_iso(strings["sec"], validate)

    if validate:
        if (np.any(strings["sep"] != csep)):
            raise ValueError("invalid ISO date-time punctuation")

        if np.any(sec >= seconds_on_day(day)):
            raise ValueError("seconds value is outside allowed range")

    return (day, sec)

########################################

def tai_from_iso(strings, validate=True):
    """Returns the elapsed seconds TAI from January 1, 2000 given an ISO date
    or date-time string. Works for scalars or arrays."""

    (day, sec) = day_sec_from_iso(strings, validate)
    return tai_from_day(day) + sec

########################################
# UNIT TESTS
########################################

class Test_ISO_Parsing(unittest.TestCase):

    def runTest(self):

        # day_from_iso()
        self.assertEqual(day_from_iso( "2001-01-01"), 366)

        strings = ["1999-01-01", "2000-01-01", "2001-01-01"]
        days    = [       -365 ,           0 ,         366 ]
        self.assertTrue(np.all(day_from_iso(strings) == np.array(days)))

        strings = [["2000-001", "2000-002"], ["2000-003", "2000-004"]]
        days    = [[        0 ,         1 ], [        2 ,         3 ]]
        self.assertTrue(np.all(day_from_iso(strings) == np.array(days)))

        strings = ["1999-01-01", "2000-01-01", "2001-01+01"]
        self.assertRaises(ValueError, day_from_iso, strings)

        strings = ["1999-01-01", "2000-01-01", "2001-01-aa"]
        self.assertRaises(ValueError, day_from_iso, strings)

        strings = ["1999-01-01", "2000-01-01", "2001-01- 1"]
        self.assertRaises(ValueError, day_from_iso, strings)

        strings = ["1999-01-01", "2000-01-01", "2001-01-00"]
        self.assertRaises(ValueError, day_from_iso, strings)

        strings = ["1999-01-01", "2000-01-01", "2001-00-01"]
        self.assertRaises(ValueError, day_from_iso, strings)

        strings = ["1999-01-01", "2000-01-01", "2001-13-01"]
        self.assertRaises(ValueError, day_from_iso, strings)

        strings = ["1999-01-01", "2000-01-01", "2001-02-29"]
        self.assertRaises(ValueError, day_from_iso, strings)

        # sec_from_iso()
        self.assertEqual(sec_from_iso("01:00:00"),     3600)
        self.assertEqual(sec_from_iso("23:59:60"),    86400)
        self.assertEqual(sec_from_iso("23:59:69"),    86409)
        self.assertEqual(sec_from_iso("23:59:69Z"),   86409)
        self.assertEqual(sec_from_iso("23:59:69.10"), 86409.10)
        self.assertEqual(sec_from_iso("23:59:69.5Z"), 86409.5)

        strings = ["00:00:00", "00:01:00", "00:02:00"]
        secs    = [        0 ,        60 ,       120 ]
        self.assertTrue(np.all(sec_from_iso(strings) == np.array(secs)))

        strings = [["00:02:00Z", "00:04:00Z"], ["00:06:00Z", "00:08:01Z"]]
        secs    = [[      120  ,       240  ], [       360 ,        481 ]]
        self.assertTrue(np.all(sec_from_iso(strings) == np.array(secs)))

        strings = ["00:00:00.01", "00:01:00.02", "23:59:69.03"]
        secs    = [        0.01 ,        60.02 ,     86409.03 ]
        self.assertTrue(np.all(sec_from_iso(strings) == np.array(secs)))

        strings = ["00:00:00.01", "00:01:00.02", "00:02+00.03"]
        self.assertRaises(ValueError, sec_from_iso, strings)

        strings = ["00:00:00.01", "00:01:00.02", "00:02: 0.03"]
        self.assertRaises(ValueError, sec_from_iso, strings)

        strings = ["00:02:00.1Z", "00:04:00.2Z", "00:06:00.3z"]
        self.assertRaises(ValueError, sec_from_iso, strings)

        strings = ["00:00:00.01", "00:01:00.02", "00:02:00+03"]
        self.assertRaises(ValueError, sec_from_iso, strings)

        strings = ["00:00:00.01", "00:01:00.02", "-0:02:00.03"]
        self.assertRaises(ValueError, sec_from_iso, strings)

        strings = ["00:00:00.01", "00:01:00.02", "24:02:00.03"]
        self.assertRaises(ValueError, sec_from_iso, strings)

        strings = ["00:00:00.01", "00:01:00.02", "00:60:00.03"]
        self.assertRaises(ValueError, sec_from_iso, strings)

        strings = ["00:00:00", "00:01:00", "00:00:70"]
        self.assertRaises(ValueError, sec_from_iso, strings)

        strings = ["00:00:00.01", "00:01:00.02", "00:00:69.00"]
        self.assertRaises(ValueError, sec_from_iso, strings)

        # day_sec_from_iso()
        self.assertEqual(day_sec_from_iso( "2001-01-01 01:00:00"), (366,3600))
        self.assertEqual(day_sec_from_iso( "2001-01-01T01:00:00"), (366,3600))

        self.assertEqual(day_sec_from_iso("1998-12-31 23:59:60"), (-366, 86400))

        self.assertRaises(ValueError, day_sec_from_iso, "2000-01-01 23:59:60")
        self.assertRaises(ValueError, day_sec_from_iso, "1999-12-31 23:59:61")

        strings = ["1999-01-01", "2000-01-01", "2001-01-01"]
        days    = [       -365 ,           0 ,         366 ]
        self.assertTrue(np.all(day_sec_from_iso(strings)[0] == np.array(days)))
        self.assertTrue(np.all(day_sec_from_iso(strings)[1] == 0))

        strings = [["2000-001", "2000-002"], ["2000-003", "2000-004"]]
        days    = [[        0 ,         1 ], [        2 ,         3 ]]
        self.assertTrue(np.all(day_sec_from_iso(strings)[0] == np.array(days)))
        self.assertTrue(np.all(day_sec_from_iso(strings)[1] == 0))

        strings = ["1998-12-31 23:59:60", "2001-01-01 01:00:01"]
        days    = [       -366          ,         366          ]
        secs    = [               86400 ,                 3601 ]
        self.assertTrue(np.all(day_sec_from_iso(strings)[0] == np.array(days)))
        self.assertTrue(np.all(day_sec_from_iso(strings)[1] == np.array(secs)))

        strings = ["1998-12-31T23:59:60", "2001-01-01T01:00:01"]
        days    = [       -366          ,         366          ]
        secs    = [               86400 ,                 3601 ]
        self.assertTrue(np.all(day_sec_from_iso(strings)[0] == np.array(days)))
        self.assertTrue(np.all(day_sec_from_iso(strings)[1] == np.array(secs)))

        strings = ["1998-12-31 23:59:60Z", "2001-01-01 01:00:01Z"]
        days    = [       -366           ,         366           ]
        secs    = [               86400  ,                 3601  ]
        self.assertTrue(np.all(day_sec_from_iso(strings)[0] == np.array(days)))
        self.assertTrue(np.all(day_sec_from_iso(strings)[1] == np.array(secs)))

        strings = ["1998-12-31 23:59:60Z", "2001-01-01x01:00:01Z"]
        self.assertRaises(ValueError, day_sec_from_iso, strings)

        strings = ["1998-12-31 23:59:60Z", "1998-12-31 23:59:61Z"]
        self.assertRaises(ValueError, day_sec_from_iso, strings)

################################################################################
# General Parsing Routines
#
# The grammar is defined in julian_dateparser.py, abbreviated jdp here.
#
# Note: Unlike all other julian library routines, these do not support
# array or arry-like arguments.
################################################################################

global DATE_PARSER_DICT, DATETIME_PARSER_DICT

DATE_PARSER_DICT = {"YMD":jdp.YMD_PREF_DATE + pyparsing.StringEnd(),
                    "MDY":jdp.MDY_PREF_DATE + pyparsing.StringEnd(),
                    "DMY":jdp.DMY_PREF_DATE + pyparsing.StringEnd()}

DATETIME_PARSER_DICT = {"YMD":jdp.YMD_PREF_DATETIME + pyparsing.StringEnd(),
                        "MDY":jdp.MDY_PREF_DATETIME + pyparsing.StringEnd(),
                        "DMY":jdp.DMY_PREF_DATETIME + pyparsing.StringEnd()}

########################################

def day_from_string(string, order="YMD"):
    """Returns a day number based on a parsing of the string. Input parameter
    order is one of 'YMD', 'MDY' or 'DMY', and defines the preferred order for
    date, month and year in situations where it might be ambiguous."""

    parser = DATE_PARSER_DICT[order]

    # Give the list a zero month entry for the year and day-of-year case
    list = [["MONTH",0]] + parser.parseString(string).asList()
    dict = _dict_from_parselist(list)

    return _day_from_dict(dict)

########################################

def sec_from_string(string):
    """Returns a second value based on a parsing of a time string."""

    # Give the list zero values for each parameter, in case they are missing
    # from the list returned
    parser = jdp.TIME + pyparsing.StringEnd()
    list = ([["HOUR",0],["MINUTE",0],["SECOND",0]] +
            parser.parseString(string).asList())
    dict = _dict_from_parselist(list)

    return _sec_from_dict(dict)

########################################

def day_sec_type_from_string(string, order="YMD", validate=True):
    """Returns a day and second based on a parsing of the string. Input
    parameter order is one of 'YMD', 'MDY' or 'DMY', and defines the preferred
    order for date, month and year in situations where it might be ambiguous.
    """

    parser = DATETIME_PARSER_DICT[order]

    # Give the default entries in case they are needed
    list = ([["TYPE","UTC"],["MONTH",0],["HOUR",0],["MINUTE",0],["SECOND",0]] +
            parser.parseString(string).asList())
    dict = _dict_from_parselist(list)

    # Get the time type
    time_type = dict["TYPE"]
    leapseconds = (time_type == "UTC")

    # Handle the case of a Julian date
    try:
        mjd = dict["MJD"]
        (day, sec) = day_sec_from_mjd(mjd)
        return (day, sec, time_type)
    except KeyError: pass

    # Handle the case of a fractional day
    dvalue = dict["DAY"]
    if type(dvalue) == type(0.):
        day = _day_from_dict(dict)
        dfrac = dvalue - day
        sec = (dvalue - day) * seconds_of_day(day, leapseconds)
        return (day, sec, time_type)

    # Otherwise, it is a calendar date plus time
    day = _day_from_dict(dict)
    sec = _sec_from_dict(dict, day, leapseconds, validate)

    return (day, sec, time_type)

####################
# internals...
####################

def _dict_from_parselist(list):
    dict = {}
    for pair in list:
        dict[pair[0]] = pair[1]

    return dict

####################

def _day_from_dict(dict):
    """Returns a day number based on the contents of a dictionary."""

    # First check for MJD date
    try:
        mjd = dict["MJD"]
        return day_from_mjd(mjd)
    except KeyError: pass

    # Look up year, month and day
    y = dict["YEAR"]
    m = dict["MONTH"]
    d = dict["DAY"]
    d = int(d)

    # Year and day-of-year case
    if m == 0:
        if d > days_in_year(y):
            raise ValueError("Day value out of range in year: " +
                              "{:04d}-{:03d}".format(y,d))

        return day_from_yd(y,d)

    # Year-month-day case
    else:
        month = month_from_ym(y,m)
        if d > days_in_month(month):
            raise ValueError("Day value out of range for month: "
                             "{:04d}-{:02d}-{:02d}".format(y,m,d))

    return day_from_ymd(y,m,d)

#####################

def _sec_from_dict(dict, day=None, leapseconds=True, validate=True):
    """Returns a seconds value based on the contents of a dictionary."""

    h = dict["HOUR"]
    m = dict["MINUTE"]
    s = dict["SECOND"]

    sec = h * 3600 + m * 60 + s

    if validate and (day is not None):
        if sec >= seconds_on_day(day, leapseconds):
            raise ValueError("Seconds value out of range on day " +
                             ymd_format_from_day(day) + ": " + str(sec))

    return sec

########################################
# UNIT TESTS
########################################

class Test_General_Parsing(unittest.TestCase):

    def runTest(self):

        # Note: julian_dateparser.py has more extensive unit tests

        # Check if day_from_string works like day_from_ymd
        self.assertEqual(day_from_string("2000-01-01"),
                         day_from_ymd(2000,01,01))
 
        # Check if other parsers work
        self.assertEqual(day_from_string("01-02-2000", "MDY"),
                         day_from_ymd(2000,01,02))
        self.assertEqual(day_from_string("01-02-00", "MDY"),
                         day_from_ymd(2000,01,02))
        self.assertEqual(day_from_string("02-01-2000", "DMY"),
                         day_from_ymd(2000,01,02))
        self.assertEqual(day_from_string("02-01-00", "DMY"),
                         day_from_ymd(2000,01,02))
        self.assertEqual(day_from_string("2000-02-29","DMY"),
                         day_from_ymd(2000,02,29))

        # Check date validator
        self.assertRaises(ValueError, day_from_string, "2001-11-31")
        self.assertRaises(ValueError, day_from_string, "2001-02-29")

        # Check sec_from_string
        self.assertEqual(sec_from_string("00:00:00.000"), 0.0)
        self.assertEqual(sec_from_string("00:00:00"), 0)
        self.assertEqual(sec_from_string("00:00:59.000"), 59.0)
        self.assertEqual(sec_from_string("00:00:59"), 59)

        # Check leap seconds
        self.assertEqual(sec_from_string("23:59:60.000"), 86400.0)
        self.assertEqual(sec_from_string("23:59:69.000"), 86409.0)
        self.assertRaises(pyparsing.ParseException, sec_from_string,
                                                    "23:59:70.000")

        # Check day_sec_type_from_string
        self.assertEqual(day_sec_type_from_string("2000-01-01 00:00:00.00"),
                         (0, 0.0, "UTC"))
        self.assertEqual(day_sec_type_from_string("2000-01-01 00:00:00.00 tai"),
                         (0, 0.0, "TAI"))
        self.assertEqual(day_sec_type_from_string("2000-01-01 00:00:00.00 Z"),
                         (0, 0.0, "UTC"))
        self.assertEqual(day_sec_type_from_string("2000-01-01 00:00:00.00 TDB"),
                         (0, 0.0, "TDB"))

        # Check if DMY is same as MDY
        self.assertEqual(day_sec_type_from_string("31-12-2000 12:34:56", "DMY"),
                         day_sec_type_from_string("12-31-2000 12:34:56", "MDY"))

        # Check leap second validator
        self.assertEqual(day_sec_type_from_string("1998-12-31 23:59:60"),
                         (-366, 86400, "UTC"))
        self.assertEqual(day_sec_type_from_string("1998-12-31 23:59:60.99"),
                         (-366, 86400.99, "UTC"))

        self.assertRaises(ValueError, day_sec_type_from_string,
                                      "1998-12-31 23:59:60 TDB")
        self.assertRaises(ValueError, day_sec_type_from_string,
                                      "1998-12-31 23:59:60.99 TAI")

        self.assertRaises(ValueError, day_sec_type_from_string,
                                      "2000-01-01 23:59:60")
        self.assertRaises(ValueError, day_sec_type_from_string,
                                      "1999-12-31 23:59:61")

################################################################################
# Perform unit testing if executed from the command line
################################################################################

if __name__ == '__main__':
    unittest.main()

################################################################################

