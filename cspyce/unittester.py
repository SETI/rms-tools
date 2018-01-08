################################################################################
# cspyce/unittester.py: global unit-tester
################################################################################

from cspyce.unittests.unittester_errors     import *
from cspyce.unittests.unittester_kernels    import *
from cspyce.unittests.unittester_nokernels  import *

################################################################################
# To run all unittests...

import unittest

if __name__ == '__main__':

    unittest.main(verbosity=2)

################################################################################
