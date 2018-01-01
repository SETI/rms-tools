################################################################################
# spyce/unittester.py: global unit-tester
################################################################################

from spyce.unittests.unittester_errors     import *
from spyce.unittests.unittester_kernels    import *
from spyce.unittests.unittester_nokernels  import *

################################################################################
# To run all unittests...

import unittest

if __name__ == '__main__':

    unittest.main(verbosity=2)

################################################################################
