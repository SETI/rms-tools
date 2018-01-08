################################################################################
# cspyce/arrays.py
################################################################################
# Array handler for the cspyce library
#
# This module implements support for multidimensional arrays by building upon
# all of the vectorized functions in the cspyce module. Upon importing this
# module, a new function is defined with for each "_vector" function, with
# "_array" replacing "_vector".

TBD
#  a more powerful overlay onThe low-level "_vector" versions of cspyce routines allow a CSPICE function to
# be called iteratively with 1-D list of inputs. Calling the _vector version of
# a cspyce function can be much faster than looping through the calls in Python.
# However, the _vector versions only allow one extra dimension on each floating-
# point input.
#
# Upon importing this module, a new function is defined for every cspyce
# "_vector" function. The new function has the same name as the
# pre-existing function, but with "_array" replacing "_vector".
#
# The key difference is that the "_array" functions follow all of the standard
# NumPy rules for array broadcasting. Input arguments to cspyce _array functions
# can have arbitrary additional dimensions, as long as all those dimensions
# broadcast together properly. The returned arrays will all have the
# broadcasted shape.
################################################################################

import cspyce
import cspyce.array_support as support

# Upon import, define all array versions
support._define_all_array_versions()

if not hasattr(cspyce, 'ARRAYS_IMPORTED'):

    # Upon import, define all missing alias versions
    support._define_all_array_versions()

    # Also add a new function directly to the cspyce module
    cspyce.use_arrays = support.use_arrays

################################################################################
# Record the fact that this module was imported
################################################################################

cspyce.ARRAYS_IMPORTED = True

################################################################################

