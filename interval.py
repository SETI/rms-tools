################################################################################
# interval.py
#
# Deukkwon Yoon & Mark Showalter, PDS Rings Node, SETI Institute, November 2011
################################################################################

import numpy as np
import unittest

class Interval(object):
    """The interval class behaves like a dictionary keyed by ranges of
    floating-point numbers. Each value of the dictionary applies for any key
    value within the numeric range. Later entries into the dictionary can
    partially or completely replace earlier values."""

    def __init__(self, min=-np.inf, max=np.inf, value=None):

        # convert interger to float
        min = float(min)
        max = float(max)

        self.count  = 0             # Latest sequence number added
        self.values = [value]       # Value at each sequence number
        self.counts = {min:0}       # Sequence number at each lower end point
        self.xlist = [min, max]     # List of all numeric endpoints

    def __str__(self):
        """Returns a string representation of the Interval object."""

        strlist = ["Interval{"]
        for i in range(len(self.xlist)-1):
            xlo = self.xlist[i]
            xhi = self.xlist[i+1]

            value = self.values[self.counts[xlo]]

            # Brackets mean the limit is included; parentheses mean it is not
            if self[xlo] == value:
                delim_lo = "["
            else:                 
                delim_lo = "("

            if self[xhi] == value:
                delim_hi = "]"
            else:
                delim_hi = ")"

            # Erase a trailing zero on integer-valued limits. It looks better
            str_xlo = str(xlo)
            if str_xlo.endswith(".0"):
                str_xlo = str_xlo[:-1]

            str_xhi = str(xhi)
            if str_xhi.endswith(".0"):
                str_xhi = str_xhi[:-1]

            strlist += [delim_lo, str_xlo, ",", str_xhi, delim_hi, ": ",
                        repr(value), ", "]

        strlist[-1] = "}"
        return "".join(strlist)

    def __repr__(self): return str(self)

    def __setitem__(self, xlimits, value):
        """Overlays the given value within the limit s (xlo,xhi)"""

        (xlo, xhi) = xlimits

        # Ignore ranges completely outside the interval
        if xhi <= self.xlist[0]:  return
        if xlo >= self.xlist[-1]: return
        if xhi <= xlo: return

        # Limit each range to the designated interval
        if xlo < self.xlist[0]:  xlo = self.xlist[0]
        if xhi > self.xlist[-1]: xhi = self.xlist[-1]

        # Convert to floating-point if necessary
        xlo = float(xlo)
        xhi = float(xhi)

        # Insert new upper endpoint into the interval
        self.count += 1
        if xhi not in self.xlist:
            self.xlist.append(xhi)
            self.xlist.sort()

            # Assign the value to be that of the point immediately below
            xbelow = self.xlist[self.xlist.index(xhi) - 1]
            self.counts[xhi] = self.counts[xbelow]

        # Insert new lower endpoint and value into the interval
        if xlo not in self.xlist:
            self.xlist.append(xlo)
            self.xlist.sort()

        self.counts[xlo] = self.count
        self.values.append(value)

        # Remove intermediate points, if any (working DOWNWARD!)
        ilo = self.xlist.index(xlo)
        ihi = self.xlist.index(xhi)
        for i in range(ihi-1, ilo, -1):
            del(self.counts[self.xlist[i]])
            ignore = self.xlist.pop(i)

    def _index(self, x, bias=0):
        """Returns the index into self.xlist identifying the lower end of the
        range within which value x falls.

        Input:
            x           an x value.

            bias        defines what to do when x lands on an exact boundary
                        between ranges.
                            bias < 0: choose the lower range
                            bias > 0: choose the upper range
                            bias == 0: choose range defined last.
        """

        if x < self.xlist[0] or x > self.xlist[-1]:
            raise ValueError("value outside range of Interval: " + str(x))

        if x > self.xlist[-2]: return len(self.xlist) - 2

        for i in range(1,len(self.xlist)-1):
            if x > self.xlist[i]: continue
            if x < self.xlist[i]: return i - 1

            # On exact match of boundary, decide which entry takes precedence
            if bias < 0: return i - 1
            if bias > 0: return i

            clo = self.counts[self.xlist[i-1]]
            chi = self.counts[self.xlist[i]]
            if clo > chi:
                return i - 1
            else:
                return i

        # This is where we end up if you ask for the lower limit exactly
        return 0

    def __getitem__(self, x):
        """For a single value, this returns the value of the Interval at the
        requested location. For a tuple (xlo,xhi), this returns the list of
        values found within the range, given in the order they were originally
        inserted into the Interval"""

        # For a single value, one quick lookup will do
        if type(x) != type([]) and type(x) != type(()):
            return self.values[self.counts[self.xlist[self._index(x)]]]

        # Otherwise, make an ordered xlist of counts within the range
        ilo = self._index(x[0], bias=1)
        ihi = self._index(x[1], bias=-1)

        counts = []
        for i in range(ilo, ihi+1):
            count = self.counts[self.xlist[i]]
            if count not in counts: counts.append(count)

        counts.sort()

        # Convert to an ordered list of values
        values = []
        for count in counts:
            value = self.values[count]

            # A duplicate value gets moved to the end of the list
            if value in values:
                ignore = values.pop(values.index(value))

            values.append(value)

        return values

################################################################################
# UNIT TESTS
################################################################################

class test_interval_integers(unittest.TestCase):

    def runTest(self):

        interval = Interval(0,100)

        with self.assertRaises(ValueError): interval[101]
        with self.assertRaises(ValueError): interval[-1]

        self.assertEqual(Interval.__str__(interval),
                         "Interval{[0.,100.]: None}")
        self.assertEqual(interval[(0,100)], [None])
        interval[(11,30)] = "a"
        interval[(31,60)] = "b"
        interval[(61,90)] = "c"
        self.assertEqual(Interval.__str__(interval),
                         "Interval{[0.,11.): None, [11.,30.]: 'a', " +
                         "(30.,31.): None, [31.,60.]: 'b', " +
                         "(60.,61.): None, [61.,90.]: 'c', " + 
                         "(90.,100.]: None}")

        self.assertEqual(interval[(0,100)], [None, "a", "b", "c"])
        for i in range(0,101):
            if i < 11:
                self.assertEqual(interval[i], None)
            elif i > 10 and i <31:
                self.assertEqual(interval[i], "a")
            elif i > 30 and i < 61:
                self.assertEqual(interval[i], "b")
            elif i > 60 and i < 91:
                self.assertEqual(interval[i], "c")
            else:
                self.assertEqual(interval[i], None)

        interval[(15,45)] = "d"
        self.assertEqual(Interval.__str__(interval),
                         "Interval{[0.,11.): None, [11.,15.): 'a', " +
                         "[15.,45.]: 'd', (45.,60.]: 'b', " +
                         "(60.,61.): None, [61.,90.]: 'c', " + 
                         "(90.,100.]: None}")

        self.assertEqual(interval[(0,100)], [None, "a", "b", "c", "d"])
        self.assertEqual(interval[(10,40)], [None, "a", "d"])
        for i in range(0,101):
            if i < 11:
                self.assertEqual(interval[i], None)
            elif i > 10 and i < 15:
                self.assertEqual(interval[i], "a")
            elif i > 14 and i < 46:
                self.assertEqual(interval[i], "d")
            elif i > 45 and i < 61:
                self.assertEqual(interval[i], "b")
            elif i > 60 and i < 91:
                self.assertEqual(interval[i], "c")
            else:
                self.assertEqual(interval[i], None)

        interval[(45,100)] = "e"
        self.assertEqual(interval[(0,100)], [None, "a", "d", "e"])
        for i in range(0,101):
            if i < 11:
                self.assertEqual(interval[i], None)
            elif i > 10 and i < 15:
                self.assertEqual(interval[i], "a")
            elif i > 14 and i < 45:
                self.assertEqual(interval[i], "d")
            elif i > 44 and i < 101:
                self.assertEqual(interval[i], "e")

        interval[(50,60)] = "c"
        self.assertEqual(interval[(0,100)], [None, "a", "d", "e", "c"])
        for i in range(0,101):
            if i < 11:
                self.assertEqual(interval[i], None)
            elif i > 10 and i < 15:
                self.assertEqual(interval[i], "a")
            elif i > 14 and i < 45:
                self.assertEqual(interval[i], "d")
            elif i > 44 and i < 50:
                self.assertEqual(interval[i], "e")
            elif i > 50 and i < 61:
                self.assertEqual(interval[i], "c")
            elif i > 60 and i < 101:
                self.assertEqual(interval[i], "e")

        interval[(-20,20)] = "f"
        self.assertEqual(interval[(0,100)], ["d", "e", "c", "f"])
        self.assertEqual(Interval.__str__(interval),
                         "Interval{[0.,20.]: 'f', (20.,45.): 'd', " +
                         "[45.,50.): 'e', [50.,60.]: 'c', (60.,100.]: 'e'}")

        interval[(90, 110)] = "g"
        self.assertEqual(interval[(0,100)], ["d", "e", "c", "f", "g"])
        self.assertEqual(Interval.__str__(interval),
                         "Interval{[0.,20.]: 'f', (20.,45.): 'd', " +
                         "[45.,50.): 'e', [50.,60.]: 'c', (60.,90.): 'e', " + 
                         "[90.,100.]: 'g'}")

        self.assertEqual(interval[(55.5,70.5)], ["e", "c"])

        interval = Interval(0,10)
        interval[(5.1,5.5)] = "a"
        self.assertEqual(interval[(0,10)], [None, "a"])
        self.assertEqual(Interval.__str__(interval),
                         "Interval{[0.,5.1): None, [5.1,5.5]: 'a', " + 
                         "(5.5,10.]: None}")

        for i in np.arange(0.0, 10.0, 0.1).tolist():
            if i >= 5.1 and i <= 5.5:
                self.assertEqual(interval[i], "a")
            else:
                self.assertEqual(interval[i], None)

        interval[(5.6,6.1)] = "b"
        self.assertEqual(interval[(0,10)], [None, "a", "b"])
        self.assertEqual(Interval.__str__(interval),
                         "Interval{[0.,5.1): None, [5.1,5.5]: 'a', " +
                         "(5.5,5.6): None, [5.6,6.1]: 'b', (6.1,10.]: None}")

        for i in np.arange(0.0, 10.0, 0.1).tolist():
            if i >= 5.1 and i <= 5.5:
                self.assertEqual(interval[i], "a")
            elif i >= 5.6 and i <= 6.1:
                self.assertEqual(interval[i], "b")
            else:
                self.assertEqual(interval[i], None)


        interval[(5.3,5.8)] = "c"

        self.assertEqual(interval[(0,10)], [None, "a", "b", "c"])
        self.assertEqual(interval[(5.3,5.8)], ["c"])
        self.assertEqual(interval[(5.1,5.9)], ["a", "b", "c"])
        self.assertEqual(interval[(5,6)], [None, "a","b","c"])
        self.assertEqual(interval[(6,7)], [None, "b"])
        self.assertEqual(interval[(5.05,5.06)], [None])

        self.assertEqual(Interval.__str__(interval),
                         "Interval{[0.,5.1): None, [5.1,5.3): 'a', " +
                         "[5.3,5.8]: 'c', (5.8,6.1]: 'b', (6.1,10.]: None}")

        for i in np.arange(0.0, 10.0, 0.1).tolist():
            if i >= 5.1 and i < 5.3:
                self.assertEqual(interval[i], "a")
            elif i >= 5.3 and i <= 5.8:
                self.assertEqual(interval[i], "c")
            elif i > 5.8 and i <= 6.1:
                self.assertEqual(interval[i], "b")
            else:
                self.assertEqual(interval[i], None)

################################################################################
# Perform unit testing if executed from the command line
################################################################################

if __name__ == '__main__':
    unittest.main()

################################################################################
