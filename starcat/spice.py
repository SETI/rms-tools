################################################################################
# starcat/spice.py
################################################################################

from __future__ import print_function

try:
    from starcatalog import *
except:
    from .starcatalog import *
import numpy as np
import os.path
import cspyce

class SpiceStar(Star):
    """A holder for star attributes.

    This class includes attributes unique to the SPICE catalogs."""

    def __init__(self):
        # Initialize the standard fields
        Star.__init__(self)

        # Initialize the SPICE-specific fields
        self.spectral_class = None
        """The spectral class"""


class SpiceStarCatalog(StarCatalog):
    def __init__(self, name):
        self.filename = os.path.join(os.environ["SPICE_PATH"], "Stars", name+'.bdb')
        self.catalog = cspyce.stcl01(self.filename)[0]
        self.debug_level = 0

        # (ra, dec, ra_uncertainty, dec_uncertainty,
        #  catalog_number, spectral_type, v_magnitude)

    def _find_stars(self, ra_min, ra_max, dec_min, dec_max, **kwargs):
        """Yield the results for all stars in the RA,DEC range."""
        vmag_min = kwargs.get('vmag_min', None)
        vmag_max = kwargs.get('vmag_max', None)

        nstars = cspyce.stcf01(self.catalog, ra_min, ra_max, dec_min, dec_max)

        for i in range(nstars):
            star = SpiceStar()
            result = tuple(cspyce.stcg01(i))
            (star.ra, star.dec, star.ra_sigma, star.dec_sigma,
             star.unique_number, star.spectral_class, star.vmag) = result
            if vmag_min is not None and star.vmag < vmag_min:
                if self.debug_level:
                    print('SKIPPED VMAG', star.vmag)
                continue
            if vmag_max is not None and star.vmag > vmag_max:
                if self.debug_level:
                    print('SKIPPED VMAG', star.vmag)
                continue

            star.temperature = self.temperature_from_sclass(star.spectral_class)
            if self.debug_level:
                print('OK!')
            yield star



#===============================================================================
# UNIT TESTS
#===============================================================================

import unittest

class Test_SpiceStarCatalog(unittest.TestCase):

    def runTest(self):
        cat = SpiceStarCatalog('hipparcos')

        num_all = cat.count_stars()
        self.assertEqual(num_all, 117955)

        num_vmag_lim = cat.count_stars(vmag_max=10)
        self.assertGreater(num_all, num_vmag_lim)

        # Compare slicing directions
        num_dec = 0
        for idec in range(20):
            num_dec += cat.count_stars(dec_min=0.2*idec*RPD,
                                       dec_max=0.2*(idec+1)*RPD,
                                       ra_min=60*RPD, ra_max=70*RPD)
        num_ra = 0
        for ira in range(10):
            num_ra += cat.count_stars(dec_min=0., dec_max=4.*RPD,
                                      ra_min=(ira+60)*RPD, ra_max=((ira+1)+60)*RPD)
        self.assertEqual(num_dec, num_ra)


if __name__ == '__main__':
    unittest.main(verbosity=2)
