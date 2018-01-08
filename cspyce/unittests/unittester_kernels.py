################################################################################

import sys
import numpy as np
import numbers
import cspyce as s
import unittest

class Test_spyce1_kernels(unittest.TestCase):

  PATH = s.__path__[0] + '/unittest_support/'

  @staticmethod
  def furnish(PATH):
    s.furnsh(PATH + 'naif0012.tls')
    s.furnsh(PATH + 'pck00010.tpc')
    s.furnsh(PATH + 'de432s.bsp')
    s.furnsh(PATH + 'sat164.bsp')
    s.furnsh(PATH + 'earth_000101_180317_171224.bpc')

    s.furnsh(PATH + 'cas_v40.tf')
    s.furnsh(PATH + 'cas00171.tsc')
    s.furnsh(PATH + '17257_17262ra.bc')
    s.furnsh(PATH + '171106R_SCPSE_17224_17258.bsp')
    s.furnsh(PATH + 'cas_iss_v10.ti')

  @staticmethod
  def unload(PATH):
    s.unload(PATH + 'naif0012.tls')
    s.unload(PATH + 'pck00010.tpc')
    s.unload(PATH + 'de432s.bsp')
    s.unload(PATH + 'sat164.bsp')
    s.unload(PATH + 'earth_000101_180317_171224.bpc')

    s.unload(PATH + 'cas_v40.tf')
    s.unload(PATH + 'cas00171.tsc')
    s.unload(PATH + '17257_17262ra.bc')
    s.unload(PATH + '171106R_SCPSE_17224_17258.bsp')
    s.unload(PATH + 'cas_iss_v10.ti')

  def assertAllEqual(self, arg1, arg2, tol=1.e-15, frac=False):
    if type(arg1) == list:
        self.assertEqual(type(arg2), list)
        self.assertEqual(len(arg1), len(arg2))
        for (item1,item2) in zip(arg1,arg2):
            self.assertAllEqual(item1, item2, tol, frac)

    elif isinstance(arg1, np.ndarray):
        arg1 = np.array(arg1)
        arg2 = np.array(arg2)
        self.assertEqual(arg1.shape, arg2.shape)
        arg1 = arg1.flatten()
        arg2 = arg2.flatten()
        for (x1,x2) in zip(arg1,arg2):
            if isinstance(x1,numbers.Real):
                if frac:
                    if abs(x1 - x2) / (abs(x1 + x2)/2.) > tol:
                        print 22221, x1, x2, tol, abs(x1 - x2) / (abs(x1 + x2)/2.)
                    self.assertTrue(abs(x1 - x2) <= tol * abs(x1 + x2)/2.)
                else:
                    self.assertTrue(abs(x1 - x2) <= tol)
            else:
                self.assertEqual(x1, x2, tol)

    elif isinstance(arg1, numbers.Real):
        if frac:
            if abs(arg1 - arg2) / (abs(arg1 + arg2)/2.) > tol: print 22222, arg1, arg2, tol, abs(arg1 - arg2) / (abs(arg1 + arg2)/2.)
            self.assertTrue(abs(arg1 - arg2) <= tol * abs(arg1 + arg2)/2.)
        else:
            self.assertTrue(abs(arg1 - arg2) <= tol)

    else:
        self.assertEqual(arg1, arg2)

  def assertAllClose(self, arg1, arg2, tol=1.e-8):
        return self.assertAllEqual(arg1, arg2, tol, frac=True)

  def runTest(self):

    intmax = s.intmax()
    intmin = s.intmin()

    # Time inside Cassini kernels
    CASSINI_ET = 17.65 * 365.25 * 86400.

    # Times inside sat164.bsp
    Y2005 = 5 * 365.25 * 86400.
    Y2006 = 6 * 365.25 * 86400.
    Y2007 = 7 * 365.25 * 86400.

    #### Not tested: dafbfs, dafcls, dafgda, dafgn, dafgs, daffna, dafopr, dafus
    #### Not tested: stcf01, stcg01, stcl01, stcl01

    ### furnsh
    PATH = Test_spyce1_kernels.PATH
    self.furnish(PATH)

    #### pool functions

    # This test adapted from pipool_c.html
    s.pipool('FRAME_MYTOPO',            [1500000])
    s.pcpool('FRAME_1500000_NAME',      ['MYTOPO'])
    s.pipool('FRAME_1500000_CLASS',     [4])
    s.pipool('FRAME_1500000_CLASS_ID',  [1500000])
    s.pipool('FRAME_1500000_CENTER',    [300000])
    s.pcpool('OBJECT_300000_FRAME',     ['MYTOPO'])
    s.pcpool('TKFRAME_MYTOPO_RELATIVE', ['J2000'])
    s.pcpool('TKFRAME_MYTOPO_SPEC',     ['ANGLES'])
    s.pcpool('TKFRAME_MYTOPO_UNITS',    ['DEGREES'])
    s.pipool('TKFRAME_MYTOPO_AXES',     [3,2,3])
    s.pdpool('TKFRAME_MYTOPO_ANGLES',   [22.2, 0., -22.2])
    et = 0.

    rmat = s.pxform('J2000', 'MYTOPO', et)
    self.assertAllEqual(rmat, [[1,0,0],[0,1,0],[0,0,1]])

    et = 10.*365.*86400.
    rmat = s.pxform('J2000', 'MYTOPO', et)
    self.assertAllEqual(rmat, [[1,0,0],[0,1,0],[0,0,1]])

    s.pcpool('CTEST', ['LARRY', 'MOE', 'CURLY'])
    s.pipool('ITEST', [3141,186,282])
    s.pdpool('DTEST', [3.1415,186.282,.0175])

# This doesn't work, but calls to expool below work fine.
#     self.assertTrue(s.expool('CTEST'))
    self.assertTrue(s.expool('ITEST'))
    self.assertTrue(s.expool('DTEST'))
    self.assertFalse(s.expool('DTESTxxx'))

    self.assertEqual(s.dtpool('CTEST'), [3, 'C'])
    self.assertEqual(s.dtpool('ITEST'), [3, 'N'])
    self.assertEqual(s.dtpool('DTEST'), [3, 'N'])
    self.assertRaises(KeyError, s.dtpool, 'DTESTxxx')

    self.assertEqual(s.dtpool.flag('CTEST'), [True, 3, 'C'])
    self.assertEqual(s.dtpool.flag('ITEST'), [True, 3, 'N'])
    self.assertEqual(s.dtpool.flag('DTEST'), [True, 3, 'N'])
    self.assertEqual(s.dtpool.flag('DTESTxxx')[0], False)

    self.assertEqual(list(s.gipool('ITEST')), [3141,186,282])
    self.assertEqual(list(s.gdpool('DTEST')), [3.1415,186.282,.0175])
    self.assertEqual(s.gcpool('CTEST'), ['LARRY', 'MOE', 'CURLY'])

    self.assertEqual(list(s.gipool('ITEST',1)), [186,282])
    self.assertEqual(list(s.gdpool('DTEST',1)), [186.282,.0175])
    self.assertEqual(s.gcpool('CTEST',1), ['MOE', 'CURLY'])

    self.assertRaises(KeyError, s.gipool, 'ITESTxxx')
    self.assertRaises(KeyError, s.gdpool, 'DTESTxxx')
    self.assertRaises(KeyError, s.gcpool, 'CTESTxxx')

    self.assertEqual(len(s.gipool.flag('ITEST')), 2)
    self.assertEqual(len(s.gdpool.flag('DTEST')), 2)
    self.assertEqual(len(s.gcpool.flag('CTEST')), 2)

    self.assertTrue(s.gipool.flag('ITEST')[-1])
    self.assertTrue(s.gdpool.flag('DTEST')[-1])
    self.assertTrue(s.gcpool.flag('CTEST')[-1])
    self.assertFalse(s.gcpool.flag('CTESTxxx')[-1])

    #### clpool, ldpool
    self.assertTrue(s.bodfnd(599, 'RADII'))
    self.assertTrue(s.bodfnd(699, 'RADII'))
    s.clpool()
    self.assertFalse(s.bodfnd(699, 'RADII'))
    s.ldpool(PATH + 'pck00010.tpc')
    self.assertTrue(s.bodfnd(699, 'RADII'))
    self.furnish(PATH)

    #### expool, dtpool
    self.assertTrue(s.expool('BODY699_RADII'))
    self.assertFalse(s.expool('BODY699_RADIIxxx'))
    self.assertEqual(s.dtpool_error('BODY699_RADII'), [3, 'N'])
    self.assertEqual(s.dtpool.flag('BODY699_RADII'), [True, 3, 'N'])
    self.assertEqual(s.dtpool.flag('BODY699_RADIIxxx')[0], False)
    self.assertRaises(KeyError, s.dtpool_error, 'BODY699_RADIIxxx')

    #### gnpool
    self.assertEqual(set(s.gnpool('BODY699*RA*')), set(['BODY699_POLE_RA',
                                                        'BODY699_RADII']))
    self.assertRaises(KeyError, s.gnpool, 'BODY699*RAxxx*')

    self.assertEqual(set(s.gnpool.flag('BODY699*RA*')[0]),
                                    set(['BODY699_POLE_RA', 'BODY699_RADII']))
    self.assertTrue(s.gnpool.flag('BODY699*RA*')[1])
    self.assertFalse(s.gnpool.flag('BODY699*RAxxx*')[1])

    SPK_FILES = ['this_is_the_full_path_specification_*',
                 'of_a_file_with_a_long_name'           ,
                 'this_is_the_full_path_specification_*',
                 'of_a_second_file_with_a_very_long_*'  ,
                 'name']
    s.pcpool('SPK_FILES', SPK_FILES)

    self.assertEqual(s.stpool('SPK_FILES', 0, '*'), SPK_FILES[0][:-1] + SPK_FILES[1])
    self.assertEqual(s.stpool('SPK_FILES', 1, '*'), SPK_FILES[2][:-1] + SPK_FILES[3][:-1] + SPK_FILES[4])
    self.assertRaises(KeyError, s.stpool, 'SPK_FILES', 2, '*')

    self.assertEqual(s.stpool.flag('SPK_FILES', 0, '*'), [SPK_FILES[0][:-1] + SPK_FILES[1], True])
    self.assertEqual(s.stpool.flag('SPK_FILES', 1, '*'), [SPK_FILES[2][:-1] + SPK_FILES[3][:-1] + SPK_FILES[4], True])
    self.assertFalse(s.stpool.flag('SPK_FILES', 2, '*')[1])

    #### bodc2n, bodn2c, bodc2s, bods2c
    self.assertEqual(s.bodc2n.flag(699), ['SATURN',True])
    self.assertEqual(s.bodc2n_error(699), 'SATURN')
    self.assertEqual(s.bodc2n.flag(intmax)[1], False)
    self.assertRaises(Exception, s.bodc2n_error, intmax)

    self.assertEqual(s.bodn2c.flag('SATuRN '), [699, True])
    self.assertEqual(s.bodn2c_error('SATURN'), 699)
    self.assertEqual(s.bodn2c.flag('foobar')[1], False)
    self.assertRaises(Exception, s.bodn2c_error, 'foobar')

    self.assertEqual(s.bodc2s(699), 'SATURN')
    self.assertEqual(s.bodc2s(intmax), str(intmax))

    self.assertEqual(s.bods2c.flag('SATuRN '), [699, True])
    self.assertEqual(s.bods2c_error('SATURN'), 699)
    self.assertEqual(s.bods2c.flag('foobar')[1], False)
    self.assertRaises(Exception, s.bods2c_error, 'foobar')
    self.assertEqual(s.bods2c_error('  699 '), 699)
    self.assertEqual(s.bods2c_error(str(intmax)), intmax)

    self.assertAllEqual(s.bltfrm(1), range(1,22), 0)
    self.assertAllEqual(s.kplfrm(1), range(1,22), 0)

    #### boddef
    s.boddef('BIG!', intmax)

    self.assertEqual(s.bodc2n.flag(intmax), ['BIG!', True])
    self.assertEqual(s.bodc2n_error(intmax), 'BIG!')

    self.assertEqual(s.bodn2c.flag('BiG! '), [intmax, True])
    self.assertEqual(s.bodn2c_error('BIG!'), intmax)

    self.assertEqual(s.bodc2s(intmax), 'BIG!')
    self.assertEqual(s.bods2c.flag('BiG! '), [intmax, True])
    self.assertEqual(s.bods2c_error('BIG!'), intmax)

    #### bodfnd
    self.assertTrue(s.bodfnd(699, 'RADII'))
    self.assertFalse(s.bodfnd(699, 'RADIIxxx'))
    self.assertFalse(s.bodfnd(intmin, 'RADII'))

    #### bodvcd
    self.assertEqual(s.bodvcd(699, 'RADII')[0], 60268.)
    self.assertEqual(s.bodvcd(699, 'RADII')[1], 60268.)
    self.assertEqual(s.bodvcd(699, 'RADII')[2], 54364.)
    self.assertRaises(KeyError, s.bodvcd, 699, 'RADIIxxx')

    #### bodvrd
    self.assertEqual(s.bodvrd('SATURN', 'RADII')[0], 60268.)
    self.assertEqual(s.bodvrd('SATURN', 'RADII')[1], 60268.)
    self.assertEqual(s.bodvrd('SATURN', 'RADII')[2], 54364.)
    self.assertRaises(KeyError, s.bodvrd, 'SATURN', 'RADIIxxx')

    #### bodvrd
    self.assertEqual(s.bodvar(699, 'RADII')[0], 60268.)
    self.assertEqual(s.bodvar(699, 'RADII')[1], 60268.)
    self.assertEqual(s.bodvar(699, 'RADII')[2], 54364.)
    self.assertRaises(KeyError, s.bodvar, 699, 'RADIIxxx')

    # cidfrm
    self.assertEqual(s.cidfrm.flag(699), [10016, 'IAU_SATURN', True])
    self.assertEqual(s.cidfrm_error(699), [10016, 'IAU_SATURN'])
    self.assertEqual(s.cidfrm.flag(intmin)[2], False)
    self.assertRaises(KeyError, s.cidfrm_error, intmin)

    # ccifrm
    self.assertEqual(s.cidfrm.flag(intmin)[2], False)
    self.assertEqual(s.ccifrm.flag(2,699), [10016, 'IAU_SATURN',699,  True])
    self.assertEqual(s.ccifrm_error(2,699), [10016, 'IAU_SATURN', 699])
    self.assertEqual(s.ccifrm.flag(2,intmin)[3], False)
    self.assertRaises(ValueError, s.ccifrm_error, intmin, intmin)

    #### ckcov
    values = s.ckcov(PATH + '17257_17262ra.bc', -82000, False, 'INTERVAL', 1.,
                     'SCLK')
    self.assertEqual(values[0,0], 304593554335.0)
    self.assertEqual(values[0,1], 304610188193.0)
    self.assertEqual(values[1,0], 304610195359.0)
    self.assertEqual(values[1,1], 304622337377.0)
    self.assertEqual(values[2,0], 304622354271.0)
    self.assertEqual(values[2,1], 304625376609.0)

    values = s.ckcov.flag(PATH + '17257_17262ra.bc', 1, False, 'INTERVAL', 1.,
                          'SCLK')
    self.assertEqual(values.shape, (0,2))

    self.assertRaises(KeyError, s.ckcov_error, PATH + '17257_17262ra.bc', 1,
                                               False, 'INTERVAL', 1., 'SCLK')

    #### pckcov, pckfrm
    self.assertRaises(IOError, s.pckcov, PATH + 'pck00010.tpc', 10016)

    frames = s.pckfrm(PATH + 'earth_000101_180317_171224.bpc')

    limits = [-4.31358161e+04, 5.74516869e+08]
    self.assertAllClose(s.pckcov(PATH + 'earth_000101_180317_171224.bpc', 3000),
                            [limits])

    #### ckgp and ckgpav
    sclk = 304593554335.
    (array1a, sclk1,          found1) = s.ckgp.flag(  -82000, sclk, 1., 'J2000')
    (array2a, array2b, sclk2, found2) = s.ckgpav.flag(-82000, sclk, 1., 'J2000')

    self.assertTrue(found1)
    self.assertTrue(found2)

    (array1a, sclk1,        ) = s.ckgp(  -82000, sclk, 1., 'J2000')
    (array2a, array2b, sclk2) = s.ckgpav(-82000, sclk, 1., 'J2000')

    self.assertTrue(abs(sclk1 - sclk1) <= 1.)
    self.assertEqual(sclk1, sclk2)
    self.assertAllEqual(array1a, array2a, 0.)

    result2a = np.array([[-0.099802  , -0.37245036, -0.92267019],
                         [-0.03169184, -0.92563955,  0.37707699],
                         [-0.99450248,  0.06687415,  0.08057704]])

    result2b = np.array([3.46254953e-05, 5.05354838e-06, -1.12043171e-05])

    self.assertAllEqual(array2a, result2a, 5.e-9)
    self.assertAllEqual(array2b, result2b, 4.e-14)

    # sclk is 0.
    self.assertFalse(s.ckgp.flag(  -82000, 0., 1., 'J2000')[-1])
    self.assertFalse(s.ckgpav.flag(-82000, 0., 1., 'J2000')[-1])

    self.assertRaises(IOError, s.ckgp_error,   -82000, 0., 1., 'J2000')
    self.assertRaises(IOError, s.ckgpav_error, -82000, 0., 1., 'J2000')

    # sclk is 0.
    self.assertFalse(s.ckgp.flag(  -82000, 0., 1., 'J2000')[-1])
    self.assertFalse(s.ckgpav.flag(-82000, 0., 1., 'J2000')[-1])

    self.assertRaises(IOError, s.ckgp_error,   -82000, 0., 1., 'J2000')
    self.assertRaises(IOError, s.ckgpav_error, -82000, 0., 1., 'J2000')

    #### ckgp_vector and ckgpav_vector
    sclk = sclk + 100. * np.arange(10)
    (array1ax,           sclk1x) = s.ckgp_vector(  -82000, sclk, 1., 'J2000')
    (array2ax, array2bx, sclk2x) = s.ckgpav_vector(-82000, sclk, 1., 'J2000')

    self.assertEqual(array1ax.shape, (10,3,3))
    self.assertEqual(array2ax.shape, (10,3,3))
    self.assertEqual(array2bx.shape, (10,3))
    self.assertAllEqual(array1ax[0], array1a, 0)
    self.assertAllEqual(array2ax[0], array2a, 0)
    self.assertAllEqual(array2bx[0], array2b, 0)

    sclk = sclk + 100. * np.arange(10)
    (array1ax,           sclk1x, found1x) = s.ckgp_vector.flag(  -82000, sclk, 1., 'J2000')
    (array2ax, array2bx, sclk2x, found2x) = s.ckgpav_vector.flag(-82000, sclk, 1., 'J2000')

    self.assertEqual(array1ax.shape, (10,3,3))
    self.assertEqual(array2ax.shape, (10,3,3))
    self.assertEqual(array2bx.shape, (10,3))
    self.assertAllEqual(array1ax[0], array1a, 0)
    self.assertAllEqual(array2ax[0], array2a, 0)
    self.assertAllEqual(array2bx[0], array2b, 0)
    self.assertTrue(np.all(found1x))
    self.assertTrue(np.all(found2x))

    #### ckobj
    self.assertEqual(s.ckobj(PATH + '17257_17262ra.bc'), [-82000])

    #### cnmfrm
    self.assertEqual(s.cnmfrm('SATURN'), [10016, 'IAU_SATURN'])
    self.assertTrue( s.cnmfrm.flag('SATURN')[-1])
    self.assertFalse(s.cnmfrm.flag('foo')[-1])
    self.assertRaises(KeyError, s.cnmfrm_error, 'foo')

    #### dpgrdr, drdpgr
    self.assertAllEqual(s.dpgrdr('saturn',1.,0.,0.,1.,0.), [[0,-1,0],
                                                            [0,0,1],
                                                            [1,0,0]])
    self.assertAllEqual(s.drdpgr('saturn',1.,0.,0.,1.,0.),
                                        [[-0.84147098, 0., 0.54030231],
                                         [-0.54030231, 0.,-0.84147098],
                                         [ 0.        , 1., 0.        ]], 5e-9)
    self.assertEqual(s.dpgrdr_vector('saturn',1.,0.,[1,2,3,4],1.,0.).shape, (4,3,3))
    self.assertEqual(s.drdpgr_vector('saturn',1.,0.,0.,1.,[0.1,0.02,0.03,0.04]).shape, (4,3,3))

    #### deltet
    d = s.deltet(0., 'UTC')
    self.assertAllEqual(d - 64.1839272847, 0., 4.e-11)
    self.assertAllEqual(s.deltet_vector(np.arange(10), 'UTC'), 10*[d], 4.e-9)

    # edterm
    results = s.edterm('UMBRAL', 'SUN', 'EARTH', 0., 'IAU_EARTH', 'LT+S',
                       'MOON', 100)
    self.assertEqual(len(results), 3)
    self.assertEqual(np.shape(results[0]), ())
    self.assertEqual(results[1].shape, (3,))
    self.assertEqual(results[2].shape, (100,3))

    # et2lst
    self.assertEqual(s.et2lst(0., 399, 0., 'PLANETOCENTRIC'),
                     [11, 55, 27, '11:55:27', '11:55:27'])
    self.assertEqual(s.et2lst(0., 399, 43200., 'PLANETOCENTRIC'),
                     [23, 46, 9, '23:46:09', '11:46:09'])

    # et2utc, utc2et, str2et, etcal
    utc = '2000-01-01T11:58:55.816'
    self.assertEqual(s.et2utc(0., 'ISOC', 3), utc)
    self.assertTrue(abs(s.utc2et(utc)) < 0.5e-3)
    self.assertTrue(abs(s.str2et(utc)) < 0.5e-3)
    self.assertEqual(s.etcal(0.), '2000 JAN 01 12:00:00.000')

    # frmnam, namfrm, frinfo
    self.assertEqual(s.frmnam(10016), 'IAU_SATURN')
    self.assertEqual(s.frmnam.flag(10016), 'IAU_SATURN')
    self.assertEqual(s.frmnam.flag(intmax), '')
    self.assertRaises(KeyError, s.frmnam_error, intmax)

    self.assertEqual(s.namfrm('IAU_SATURN'), 10016)
    self.assertEqual(s.namfrm.flag('IAU_SATURN'), 10016)
    self.assertEqual(s.namfrm.flag('xxxxx'), 0)
    self.assertRaises(KeyError, s.namfrm_error, 'xxxxx')

    self.assertEqual(s.frinfo(10016), [699, 2, 699])
    self.assertEqual(s.frinfo.flag(10016), [699, 2, 699, True])
    self.assertFalse(s.frinfo.flag(intmax)[-1])
    self.assertRaises(KeyError, s.frinfo, intmax)

    # frmchg, sxform, pxform, xf2rav, pxfrm2, refchg
    sat0a = s.frmchg(1, 10016, 0.)
    sat1a = s.frmchg(1, 10016, 86400.)
    sat0b = s.sxform('IAU_SATURN', 'J2000', 0.)
    sat1b = s.sxform('IAU_SATURN', 'J2000', 86400.)
    sat0c = s.pxform('IAU_SATURN', 'J2000', 0.)
    sat1c = s.pxform('IAU_SATURN', 'J2000', 86400.)
    sat0d = s.pxfrm2('IAU_SATURN', 'J2000', 0., 0.)
    sat1d = s.pxfrm2('IAU_SATURN', 'J2000', 86400., 86400.)
    sat0e = s.refchg(1, 10016, 0.)
    sat1e = s.refchg(1, 10016, 86400.)

    self.assertAllEqual(sat0a[:3,:3], sat0b[:3,:3], 0)
    self.assertAllEqual(sat0a[:3,:3], sat0c, 0)
    self.assertAllEqual(sat0a[:3,:3], sat0d, 0)
    self.assertAllEqual(sat0a[:3,:3], sat0e, 0)
    self.assertAllEqual(sat0a[:3,:3], sat0a[3:,3:], 0)  # frmchg not rotating

    self.assertAllEqual(sat1a[:3,:3], sat1b[:3,:3], 0)
    self.assertAllEqual(sat1a[:3,:3], sat1c, 0)
    self.assertAllEqual(sat1a[:3,:3], sat1d, 0)
    self.assertAllEqual(sat1a[:3,:3], sat1e, 0)
    self.assertAllEqual(sat1a[:3,:3], sat1a[3:,3:], 0)

    (mat0a, vec0a) = s.xf2rav(sat0a)
    (mat1a, vec1a) = s.xf2rav(sat1a)
    (mat0b, vec0b) = s.xf2rav(sat0b)
    (mat1b, vec1b) = s.xf2rav(sat1b)

    self.assertAllEqual(sat0a[:3,:3], mat0a, 0)
    self.assertAllEqual(sat1a[:3,:3], mat1a, 0)
    self.assertAllEqual(sat0b[:3,:3], mat0b, 0)
    self.assertAllEqual(sat1b[:3,:3], mat1b, 0)

    self.assertAllEqual(vec0a, 3*[0.], 0.)
    self.assertAllEqual(vec1a, 3*[0.], 0.)

    self.assertAllEqual(vec0b, vec1b, 1.e-13)

    sat01a = s.frmchg_vector(1, 10016, [0.,86400.])
    sat01b = s.sxform_vector('IAU_SATURN', 'J2000', [0.,86400.])
    sat01c = s.pxform_vector('IAU_SATURN', 'J2000', [0.,86400.])
    sat01d = s.pxfrm2_vector('IAU_SATURN', 'J2000', [0.,86400.], [0.,86400.])
    sat01e = s.refchg_vector(1, 10016, [0.,86400.])

    self.assertAllEqual(sat01a, [sat0a,sat1a], 0)
    self.assertAllEqual(sat01b, [sat0b,sat1b], 0)
    self.assertAllEqual(sat01c, [sat0c,sat1c], 0)
    self.assertAllEqual(sat01d, [sat0d,sat1d], 0)
    self.assertAllEqual(sat01e, [sat0e,sat1e], 0)

    (mat01b, vec01b) = s.xf2rav_vector(sat01b)
    self.assertAllEqual(mat01b, [mat0b,mat1b], 0)
    self.assertAllEqual(vec01b, [vec0b,vec1b], 0)

    #### pgrrec, recpgr
    self.assertAllEqual(s.pgrrec('MIMAS',0,0,1,1,0.1), [2,0,0])
    self.assertAllEqual(s.recpgr('MIMAS',[2,0,0],1,0.1), [0,0,1])

    self.assertAllEqual(s.pgrrec_vector('MIMAS',[0,0],0,1,1,0.1), 2*[[2,0,0]])
    self.assertAllEqual(s.recpgr_vector('MIMAS',[2,0,0],[1,1],0.1), [[0,0],[0,0],[1,1]])

    #### lspcn
    self.assertAllEqual(s.lspcn('SATURN', Y2005, 'LT+S'), 5.23103124275, 1.e-11)
    self.assertAllEqual(s.lspcn('SATURN', Y2006, 'LT+S'), 5.46639556423, 1.e-11)
    self.assertAllEqual(s.lspcn_vector('SATURN', Y2006, 'LT+S'), 5.46639556423, 1.e-11)
    self.assertAllEqual(s.lspcn_vector('SATURN', [Y2005,Y2006], 'LT+S'),
                        [5.23103124275,5.46639556423], 1.e-11)

    #### latsrf (no vector version)
    mimas = s.bodn2c('MIMAS')
    (a,b,C) = s.bodvcd(mimas, 'RADII')
    lonlats = np.array([[0,0],[90,0],[180,0],[270,0],[0,-90],[0,90]]) * s.rpd()
    results5 = s.latsrf('ELLIPSOID', 'MIMAS', Y2005, 'IAU_MIMAS', lonlats)
    results6 = s.latsrf('ELLIPSOID', 'MIMAS', Y2006, 'IAU_MIMAS', lonlats)

    target = [[a,0,0],[0,b,0],[-a,0,0],[0,-b,0],[0,0,-C],[0,0,C]]
    self.assertAllEqual(results5, target, 4e-14)
    self.assertAllEqual(results6, target, 4e-14)

    #### ltime
    self.assertAllEqual(s.ltime(CASSINI_ET, -82, '->', 399),
                        [556996483.4720103, 4843.472010222729], 1.e-7)
    self.assertAllEqual(s.ltime(CASSINI_ET, -82, '<-', 399),
                        [556986797.4373786, 4842.562621312754], 1.e-7)
    self.assertAllEqual(s.ltime_vector(CASSINI_ET, -82, '<-', 399),
                        [556986797.4373786, 4842.562621312754], 1.e-7)
    self.assertAllEqual(s.ltime_vector(3*[CASSINI_ET], -82, '<-', 399),
                        [3*[556986797.4373786], 3*[4842.562621312754]], 1.e-7)

    #### spkcov, spkobj
    self.assertRaises(IOError, s.spkcov, 'foo.bsp', -82)

    spkpath = PATH + '171106R_SCPSE_17224_17258.bsp'
    self.assertRaises(KeyError, s.spkcov, spkpath, 401)

    limits = [5.55782400e+08, 5.58745200e+08]
    self.assertAllEqual(s.spkcov(spkpath, -82), [limits], 1.)
    self.assertAllEqual(s.spkcov(spkpath, 699), [limits], 1.)

    self.assertAllEqual(s.spkcov.flag(spkpath, 699), [limits], 1.)
    self.assertAllEqual(s.spkcov.flag(spkpath, 401), np.empty((0,2)))

    bodies = set([-82, 301, 399, 699] + range(1,11) + range(601,613) + range(615,618))
    self.assertEqual(set(s.spkobj(PATH + '171106R_SCPSE_17224_17258.bsp')), bodies)

    #### illum, illumf, illumg, ilumin, phaseq
    trgepc = 556991636.744989
    srfvec = [-898913.54085495, -158678.38639218, -344986.06074434]
    phase  = 2.3355683234002207
    incdnc = 2.6877326371660395
    emissn = 0.39969284462247634
    visibl = True
    lit    = False

    CASSINI_ET2 = CASSINI_ET + 86400.
    trgepc2 = 557078039.2141582
    srfvec2 = [-197119.85363806,   61957.21359249,  113170.06834279]
    phase2  = 3.0776373659048852
    incdnc2 = 2.6248933305972493
    emissn2 = 0.5795501233580607
    visibl2 = True
    lit2    = False

    eps = 5e-8
    self.assertAllEqual(s.illum('mimas', CASSINI_ET, 'lt+S', 'cassini',
                                [200,0,0]),
            [phase, incdnc, emissn], eps)
    self.assertAllEqual(s.illumf('ellipsoid', 'mimas', 'sun', CASSINI_ET,
                                 'iau_mimas', 'lt+s', 'cassini', [200,0,0]),
            [trgepc, srfvec, phase, incdnc, emissn, visibl, lit], eps)
    self.assertAllEqual(s.illumg('ellipsoid', 'mimas', 'sun', CASSINI_ET,
                                 'iau_mimas', 'lt+s', 'cassini', [200,0,0]),
            [trgepc, srfvec, phase, incdnc, emissn], eps)
    self.assertAllEqual(s.ilumin('ellipsoid', 'mimas', CASSINI_ET,
                                 'iau_mimas', 'lt+s', 'cassini', [200,0,0]),
            [trgepc, srfvec, phase, incdnc, emissn], eps)


    self.assertAllEqual(s.illum('mimas', CASSINI_ET2, 'lt+S', 'cassini',
                                [200,0,0]),
            [phase2, incdnc2, emissn2], eps)
    self.assertAllEqual(s.illumf('ellipsoid', 'mimas', 'sun', CASSINI_ET2,
                                 'iau_mimas', 'lt+s', 'cassini', [200,0,0]),
            [trgepc2, srfvec2, phase2, incdnc2, emissn2, visibl2, lit2], eps)
    self.assertAllEqual(s.illumg('ellipsoid', 'mimas', 'sun', CASSINI_ET2,
                                 'iau_mimas', 'lt+s', 'cassini', [200,0,0]),
            [trgepc2, srfvec2, phase2, incdnc2, emissn2], eps)
    self.assertAllEqual(s.ilumin('ellipsoid', 'mimas', CASSINI_ET2,
                                 'iau_mimas', 'lt+s', 'cassini', [200,0,0]),
            [trgepc2, srfvec2, phase2, incdnc2, emissn2], eps)


    self.assertAllEqual(s.illum_vector('mimas', CASSINI_ET, 'lt+S', 'cassini',
                                [200,0,0]),
            [phase, incdnc, emissn], eps)
    self.assertAllEqual(s.illumf_vector('ellipsoid', 'mimas', 'sun', CASSINI_ET,
                                 'iau_mimas', 'lt+s', 'cassini', [200,0,0]),
            [trgepc, srfvec, phase, incdnc, emissn, visibl, lit], eps)
    self.assertAllEqual(s.illumg_vector('ellipsoid', 'mimas', 'sun', CASSINI_ET,
                                 'iau_mimas', 'lt+s', 'cassini', [200,0,0]),
            [trgepc, srfvec, phase, incdnc, emissn], eps)
    self.assertAllEqual(s.ilumin_vector('ellipsoid', 'mimas', CASSINI_ET,
                                 'iau_mimas', 'lt+s', 'cassini', [200,0,0]),
            [trgepc, srfvec, phase, incdnc, emissn], eps)


    self.assertAllEqual(s.illum_vector('mimas', [CASSINI_ET], 'lt+S', 'cassini',
                                [200,0,0]),
            [[phase], [incdnc], [emissn]], eps)
    self.assertAllEqual(s.illumf_vector('ellipsoid', 'mimas', 'sun', [CASSINI_ET],
                                 'iau_mimas', 'lt+s', 'cassini', [200,0,0]),
            [[trgepc], [srfvec], [phase], [incdnc], [emissn], [visibl], [lit]], eps)
    self.assertAllEqual(s.illumg_vector('ellipsoid', 'mimas', 'sun', [CASSINI_ET],
                                 'iau_mimas', 'lt+s', 'cassini', [200,0,0]),
            [[trgepc], [srfvec], [phase], [incdnc], [emissn]], eps)
    self.assertAllEqual(s.ilumin_vector('ellipsoid', 'mimas', [CASSINI_ET],
                                 'iau_mimas', 'lt+s', 'cassini', [200,0,0]),
            [[trgepc], [srfvec], [phase], [incdnc], [emissn]], eps)


    self.assertAllEqual(s.illum_vector('mimas', [CASSINI_ET, CASSINI_ET2], 'lt+S', 'cassini',
                                [200,0,0]),
            [[phase,phase2], [incdnc,incdnc2], [emissn,emissn2]], eps)
    self.assertAllEqual(s.illumf_vector('ellipsoid', 'mimas', 'sun', [CASSINI_ET, CASSINI_ET2],
                                 'iau_mimas', 'lt+s', 'cassini', [200,0,0]),
            [[trgepc,trgepc2], [srfvec,srfvec2], [phase,phase2], [incdnc,incdnc2], [emissn,emissn2], [visibl,visibl2], [lit,lit2]], eps)
    self.assertAllEqual(s.illumg_vector('ellipsoid', 'mimas', 'sun', [CASSINI_ET, CASSINI_ET2],
                                 'iau_mimas', 'lt+s', 'cassini', [200,0,0]),
            [[trgepc,trgepc2], [srfvec,srfvec2], [phase,phase2], [incdnc,incdnc2], [emissn,emissn2]], eps)
    self.assertAllEqual(s.ilumin_vector('ellipsoid', 'mimas', [CASSINI_ET, CASSINI_ET2],
                                 'iau_mimas', 'lt+s', 'cassini', [200,0,0]),
            [[trgepc,trgepc2], [srfvec,srfvec2], [phase,phase2], [incdnc,incdnc2], [emissn,emissn2]], eps)

    #### phaseq
    phase  = 2.33564238748
    phase2 = 3.07809474673

    self.assertAllEqual(s.phaseq(CASSINI_ET, 'mimas', 'sun', 'cassini', 'lt+s'),
            phase, eps)
    self.assertAllEqual(s.phaseq(CASSINI_ET2, 'mimas', 'sun', 'cassini', 'lt+s'),
            phase2, eps)
    
    self.assertAllEqual(s.phaseq_vector(CASSINI_ET, 'mimas', 'sun', 'cassini', 'lt+s'),
            phase, eps)

    self.assertAllEqual(s.phaseq_vector([CASSINI_ET,CASSINI_ET2], 'mimas', 'sun', 'cassini', 'lt+s'),
            [phase,phase2], eps)

    #### sce2c, sce2s, sce2t, scdecd, sct2e, scencd, scs2e, sctiks, scfmt, scpart
    scdp  = 3.04176877635e+11
    scdp2 = 3.04198996178e+11
    sclk  = '1/1882414947.067'
    sclk2 = '1/1882501347.210'

    self.assertAllEqual(s.sce2c( -82, CASSINI_ET) , scdp , 1.)
    self.assertAllEqual(s.sce2c( -82, CASSINI_ET2), scdp2, 1.)
    self.assertAllEqual(s.sce2s( -82, CASSINI_ET) , sclk )
    self.assertAllEqual(s.sce2s( -82, CASSINI_ET2), sclk2)
    self.assertAllEqual(s.sce2t( -82, CASSINI_ET) , scdp , 1.)
    self.assertAllEqual(s.sce2t( -82, CASSINI_ET2), scdp2, 1.)
    self.assertAllEqual(s.scdecd(-82, scdp ), sclk )
    self.assertAllEqual(s.scdecd(-82, scdp2), sclk2)
    self.assertAllEqual(s.sct2e( -82, scdp ), CASSINI_ET , 1.)
    self.assertAllEqual(s.sct2e( -82, scdp2), CASSINI_ET2, 1.)
    self.assertAllEqual(s.scencd(-82, sclk ), scdp , 1.)
    self.assertAllEqual(s.scencd(-82, sclk2), scdp2, 1.)
    self.assertAllEqual(s.scs2e( -82, sclk ), CASSINI_ET , 1.)
    self.assertAllEqual(s.scs2e( -82, sclk2), CASSINI_ET2, 1.)

    self.assertAllEqual(s.sctiks(-82,"1.000"), 256.)
    self.assertAllEqual(s.sctiks(-82,"0.001"),   1.)

    self.assertAllEqual(s.scfmt(-82, scdp) , '1188190928.067')
    self.assertAllEqual(s.scfmt(-82, scdp2), '1188277328.210')

    parts = [1.77721349e+11, 1.09951163e+12]
    self.assertAllEqual(s.scpart(-82), [parts], 3000.)

    self.assertAllEqual(s.sce2c_vector( -82, CASSINI_ET) , scdp , 1.)
    self.assertAllEqual(s.sce2c_vector( -82, CASSINI_ET2), scdp2, 1.)
    self.assertAllEqual(s.sce2t_vector( -82, CASSINI_ET) , scdp , 1.)
    self.assertAllEqual(s.sce2t_vector( -82, CASSINI_ET2), scdp2, 1.)
    self.assertAllEqual(s.sct2e_vector( -82, scdp ), CASSINI_ET , 1.)
    self.assertAllEqual(s.sct2e_vector( -82, scdp2), CASSINI_ET2, 1.)

    self.assertAllEqual(s.sce2c_vector( -82, [CASSINI_ET ]), [scdp ], 1.)
    self.assertAllEqual(s.sce2c_vector( -82, [CASSINI_ET2]), [scdp2], 1.)
    self.assertAllEqual(s.sce2t_vector( -82, [CASSINI_ET ]), [scdp ], 1.)
    self.assertAllEqual(s.sce2t_vector( -82, [CASSINI_ET2]), [scdp2], 1.)
    self.assertAllEqual(s.sct2e_vector( -82, [scdp ]), [CASSINI_ET ], 1.)
    self.assertAllEqual(s.sct2e_vector( -82, [scdp2]), [CASSINI_ET2], 1.)

    self.assertAllEqual(s.sce2c_vector( -82, [CASSINI_ET,CASSINI_ET2]), [scdp,scdp2], 1.)
    self.assertAllEqual(s.sce2t_vector( -82, [CASSINI_ET,CASSINI_ET2]), [scdp,scdp2], 1.)
    self.assertAllEqual(s.sct2e_vector( -82, [scdp,scdp2]), [CASSINI_ET,CASSINI_ET2], 1.)

    #### spkssb, spkacs, spkapo, spkez, spkezr, spkpos
    xssb  = [-9.35325266e+07, -1.38980049e+09, -5.69362184e+08, 1.00994262e+01,
             5.57457613e+00, -1.32361199e+00]
    xssb2 = [-9.28933887e+07, -1.38916427e+09, -5.69894015e+08, -8.14701094e-01,
             -1.90665286e+01, -8.26491731e+00]

    ssb  = s.spkssb(-82, CASSINI_ET,  'J2000')
    ssb2 = s.spkssb(-82, CASSINI_ET2, 'J2000')
    self.assertAllClose(s.spkssb(-82, CASSINI_ET,  'J2000'), xssb)
    self.assertAllClose(s.spkssb(-82, CASSINI_ET2, 'J2000'), xssb2)

    xstate  = [-5.80013005e+04,   8.94350415e+05,  -3.86487455e+05,
               -1.49765896e+01,  -5.10106017e+00,   1.77874639e+00]
    xstate2  = [2.09801346e+04,   2.11762463e+05,   1.01477978e+05,
               -3.43826105e+00,   1.42982547e+01,   8.91877142e+00]
    xlt  = 3.255625500957274
    xdlt = -1.4972390244438447e-05
    xlt2  = 0.7864001637489081
    xdlt2 = 5.4624503604634114e-05

    (state,  lt,  dlt)  = s.spkaps(601, CASSINI_ET,  'J2000', 'lt', ssb, [0,0,0])
    (state2, lt2, dlt2) = s.spkaps(601, CASSINI_ET2, 'J2000', 'lt', ssb2, [0,0,0])

    self.assertAllClose([state,  lt,  dlt] , [xstate,  xlt,  xdlt ])
    self.assertAllClose([state2, lt2, dlt2], [xstate2, xlt2, xdlt2])

    self.assertAllEqual(s.spkacs(601, CASSINI_ET, 'J2000', 'lt', -82),
                    [state, lt, dlt], 0)
    self.assertAllEqual(s.spkacs(601, CASSINI_ET2, 'J2000', 'lt', -82),
                    [state2, lt2, dlt2], 0)

    self.assertAllEqual(s.spkapo(601, CASSINI_ET, 'J2000', ssb, 'lt'),
                    [state[:3], lt], 0)
    self.assertAllEqual(s.spkapo(601, CASSINI_ET2, 'J2000', ssb2, 'lt'),
                    [state2[:3], lt2], 0)

    self.assertAllEqual(s.spkez(601, CASSINI_ET, 'J2000', 'lt', -82),
                    [state, lt], 0)
    self.assertAllEqual(s.spkez(601, CASSINI_ET2, 'J2000', 'lt', -82),
                    [state2, lt2], 0)

    self.assertAllEqual(s.spkezp(601, CASSINI_ET, 'J2000', 'lt', -82),
                    [state[:3], lt], 0)
    self.assertAllEqual(s.spkezp(601, CASSINI_ET2, 'J2000', 'lt', -82),
                    [state2[:3], lt2], 0)

    self.assertAllEqual(s.spkezr('mimas', CASSINI_ET, 'J2000', 'lt', 'cassini'),
                    [state, lt], 0)
    self.assertAllEqual(s.spkezr('mimas', CASSINI_ET2, 'J2000', 'lt', 'cassini'),
                    [state2, lt2], 0)

    self.assertAllEqual(s.spkpos('mimas', CASSINI_ET, 'J2000', 'lt', 'cassini'),
                    [state[:3], lt], 0)
    self.assertAllEqual(s.spkpos('mimas', CASSINI_ET2, 'J2000', 'lt', 'cassini'),
                    [state2[:3], lt2], 0)

    self.assertAllEqual(s.spkltc(601, CASSINI_ET, 'J2000', 'lt', ssb),
                    [state, lt, dlt], 0)
    self.assertAllEqual(s.spkltc(601, CASSINI_ET2, 'J2000', 'lt', ssb2),
                    [state2, lt2, dlt2], 0)

    # spkapp gives an erroneous velocity
    temp  = s.spkapp(601, CASSINI_ET , 'J2000', ssb , 'lt')
    temp2 = s.spkapp(601, CASSINI_ET2, 'J2000', ssb2, 'lt')

    self.assertAllEqual(temp [0][:3], state [:3], 0)
    self.assertAllEqual(temp2[0][:3], state2[:3], 0)
    self.assertAllEqual(temp [1:], [lt ], 0)
    self.assertAllEqual(temp2[1:], [lt2], 0)
    self.assertAllEqual(temp [0][3:], state [3:], 3e-4)
    self.assertAllEqual(temp2[0][3:], state2[3:], 3e-4)

    # vector versions with scalar inputs
    self.assertAllEqual(s.spkaps_vector(601, CASSINI_ET, 'J2000', 'lt', ssb, [0,0,0]),
                    [state, lt, dlt], 0)
    self.assertAllEqual(s.spkaps_vector(601, CASSINI_ET2, 'J2000', 'lt', ssb2, [0,0,0]),
                    [state2, lt2, dlt2], 0)

    self.assertAllEqual(s.spkacs_vector(601, CASSINI_ET, 'J2000', 'lt', -82),
                    [state, lt, dlt], 0)
    self.assertAllEqual(s.spkacs_vector(601, CASSINI_ET2, 'J2000', 'lt', -82),
                    [state2, lt2, dlt2], 0)

    self.assertAllEqual(s.spkapo_vector(601, CASSINI_ET, 'J2000', ssb, 'lt'),
                    [state[:3], lt], 0)
    self.assertAllEqual(s.spkapo_vector(601, CASSINI_ET2, 'J2000', ssb2, 'lt'),
                    [state2[:3], lt2], 0)

    self.assertAllEqual(s.spkez_vector(601, CASSINI_ET, 'J2000', 'lt', -82),
                    [state, lt], 0)
    self.assertAllEqual(s.spkez_vector(601, CASSINI_ET2, 'J2000', 'lt', -82),
                    [state2, lt2], 0)

    self.assertAllEqual(s.spkezp_vector(601, CASSINI_ET, 'J2000', 'lt', -82),
                    [state[:3], lt], 0)
    self.assertAllEqual(s.spkezp_vector(601, CASSINI_ET2, 'J2000', 'lt', -82),
                    [state2[:3], lt2], 0)

    self.assertAllEqual(s.spkezr_vector('mimas', CASSINI_ET, 'J2000', 'lt', 'cassini'),
                    [state, lt], 0)
    self.assertAllEqual(s.spkezr_vector('mimas', CASSINI_ET2, 'J2000', 'lt', 'cassini'),
                    [state2, lt2], 0)

    self.assertAllEqual(s.spkpos_vector('mimas', CASSINI_ET, 'J2000', 'lt', 'cassini'),
                    [state[:3], lt], 0)
    self.assertAllEqual(s.spkpos_vector('mimas', CASSINI_ET2, 'J2000', 'lt', 'cassini'),
                    [state2[:3], lt2], 0)

    self.assertAllEqual(s.spkltc_vector(601, CASSINI_ET, 'J2000', 'lt', ssb),
                    [state, lt, dlt], 0)
    self.assertAllEqual(s.spkltc_vector(601, CASSINI_ET2, 'J2000', 'lt', ssb2),
                    [state2, lt2, dlt2], 0)

    temp  = s.spkapp_vector(601, CASSINI_ET , 'J2000', ssb , 'lt')
    temp2 = s.spkapp_vector(601, CASSINI_ET2, 'J2000', ssb2, 'lt')

    self.assertAllEqual(temp [0][:3], state [:3], 0)
    self.assertAllEqual(temp2[0][:3], state2[:3], 0)
    self.assertAllEqual(temp [1:], [lt ], 0)
    self.assertAllEqual(temp2[1:], [lt2], 0)
    self.assertAllClose(temp [0][3:], state [3:], 3e-4)
    self.assertAllClose(temp2[0][3:], state2[3:], 3e-4)

    # vector versions with vector inputs
    self.assertAllEqual(s.spkaps_vector(601, [CASSINI_ET, CASSINI_ET2], 'J2000', 'lt', [ssb,ssb2], 2*[[0,0,0]]),
                    [[state,state2], [lt,lt2], [dlt,dlt2]], 0)
    self.assertAllEqual(s.spkacs_vector(601, [CASSINI_ET, CASSINI_ET2], 'J2000', 'lt', -82),
                    [[state,state2], [lt,lt2], [dlt,dlt2]], 0)
    self.assertAllEqual(s.spkapo_vector(601, [CASSINI_ET, CASSINI_ET2], 'J2000', [ssb,ssb2], 'lt'),
                    [[state[:3],state2[:3]], [lt,lt2]], 0)
    self.assertAllEqual(s.spkez_vector(601, [CASSINI_ET, CASSINI_ET2], 'J2000', 'lt', -82),
                    [[state,state2], [lt,lt2]], 0)
    self.assertAllEqual(s.spkezp_vector(601, [CASSINI_ET, CASSINI_ET2], 'J2000', 'lt', -82),
                    [[state[:3],state2[:3]], [lt,lt2]], 0)
    self.assertAllEqual(s.spkezr_vector('mimas', [CASSINI_ET, CASSINI_ET2], 'J2000', 'lt', 'cassini'),
                    [[state,state2], [lt,lt2]], 0)
    self.assertAllEqual(s.spkpos_vector('mimas', [CASSINI_ET, CASSINI_ET2], 'J2000', 'lt', 'cassini'),
                    [[state[:3],state2[:3]], [lt,lt2]], 0)
    self.assertAllEqual(s.spkltc_vector(601, [CASSINI_ET, CASSINI_ET2], 'J2000', 'lt', [ssb,ssb2]),
                    [[state,state2], [lt,lt2], [dlt,dlt2]], 0)

    temp  = s.spkapp_vector(601, [CASSINI_ET, CASSINI_ET2], 'J2000', [ssb,ssb2], 'lt')
    self.assertAllEqual(temp[0][:,:3], [state[:3],state2[:3]], 0)
    self.assertAllEqual(temp[1], [lt,lt2], 0)
    self.assertAllEqual(temp[0][:,3:], [state[3:],state2[3:]], 3e-4)

    #### spkez, spkgeo, spkgps
    xstate  = [ -5.80171789e+04,   8.94351951e+05,  -3.86485973e+05,
                -1.49767494e+01,  -5.10452110e+00,   1.77892184e+00]
    xstate2  = [2.09767900e+04,   2.11758713e+05,   1.01478492e+05,
                -3.43824167e+00,   1.42971900e+01,   8.91882636e+00]
    xlt  = 3.2556313860561055
    xlt2  = 0.7863886730607871

    (state, lt) = s.spkez(601, CASSINI_ET, 'J2000', 'none', -82)
    (state2, lt2) = s.spkez(601, CASSINI_ET2, 'J2000', 'none', -82)

    self.assertAllClose(s.spkez(601, CASSINI_ET, 'J2000', 'none', -82),
                    [xstate, xlt])
    self.assertAllClose(s.spkez(601, CASSINI_ET2, 'J2000', 'none', -82),
                    [xstate2, xlt2])

    self.assertAllEqual(s.spkgeo(601, CASSINI_ET, 'J2000', -82),
                    [state, lt], 0)
    self.assertAllEqual(s.spkgeo(601, CASSINI_ET2, 'J2000', -82),
                    [state2, lt2], 0)

    self.assertAllEqual(s.spkgps(601, CASSINI_ET, 'J2000', -82),
                    [state[:3], lt], 0)
    self.assertAllEqual(s.spkgps(601, CASSINI_ET2, 'J2000', -82),
                    [state2[:3], lt2], 0)

    #### srfc2s, srfcss, srfs2c, srfscc
    s.furnsh(PATH + 'phobos_surface.tm')    # Example from srfc2s_c.html
    self.assertEqual(s.srfc2s(1,401), 'PHOBOS GASKELL Q512')
    self.assertEqual(s.srfcss(1,'phobos'), 'PHOBOS GASKELL Q512')
    self.assertEqual(s.srfs2c('PHOBOS GASKELL Q512','phobos'), 1)
    self.assertEqual(s.srfscc('PHOBOS GASKELL Q512',401), 1)

    self.assertRaises(KeyError, s.srfc2s, 2, 401)
    self.assertRaises(KeyError, s.srfc2s, 1, 402)
    self.assertRaises(KeyError, s.srfcss, 2, 'phobos')
    self.assertRaises(KeyError, s.srfcss, 1, 'deimos')
    self.assertRaises(KeyError, s.srfs2c, 'whatever', 'phobos')
    self.assertRaises(KeyError, s.srfs2c, 'PHOBOS GASKELL Q512', 'deimos')
    self.assertRaises(KeyError, s.srfscc, 'whatever', 401)
    self.assertRaises(KeyError, s.srfscc, 'PHOBOS GASKELL Q512', 402)

    self.assertAllEqual(s.srfc2s.flag(1,401), ['PHOBOS GASKELL Q512',True])
    self.assertAllEqual(s.srfcss.flag(1,'phobos'), ['PHOBOS GASKELL Q512',True])
    self.assertAllEqual(s.srfs2c.flag('PHOBOS GASKELL Q512','phobos'), [1,True])
    self.assertAllEqual(s.srfscc.flag('PHOBOS GASKELL Q512',401), [1,True])

    self.assertFalse(s.srfc2s.flag(2, 401)[1])
    self.assertFalse(s.srfc2s.flag(1, 402)[1])
    self.assertFalse(s.srfcss.flag(2, 'phobos')[1])
    self.assertFalse(s.srfcss.flag(1, 'deimos')[1])
    self.assertFalse(s.srfs2c.flag('whatever', 'phobos')[1])
    self.assertFalse(s.srfs2c.flag('PHOBOS GASKELL Q512', 'deimos')[1])
    self.assertFalse(s.srfscc.flag('whatever', 401)[1])
    self.assertFalse(s.srfscc.flag('PHOBOS GASKELL Q512', 402)[1])

    #### timdef
    self.assertEqual(s.timdef('get', 'calendar'), 'GREGORIAN')
    self.assertEqual(s.timdef('get', 'system'), 'UTC')
    self.assertEqual(s.timdef('get', 'zone'), '')

    self.assertEqual(s.timdef('set', 'calendar', 'mixed '), 'mixed ')
    self.assertEqual(s.timdef('get', 'calendar'), 'MIXED')
    
    self.assertEqual(s.timdef('set', 'system', 'utC'), 'utC')
    self.assertEqual(s.timdef('get', 'system'), 'UTC')

    self.assertEqual(s.timdef('set', 'zone', 'PDT'), 'PDT')
    self.assertEqual(s.timdef('get', 'zone'), 'UTC-7')
    s.timdef('set', 'zone', 'UTC-0')

    #### tparse
    self.assertEqual(s.tparse('Tue Aug  6 11:10:57  1996'), -107398143.0)
    self.assertEqual(s.tparse('JANUary 1, 2000 12:00'), 0.)

    self.assertRaises(ValueError, s.tparse, 'Tue Aug  6 11:10:57  1996g')
    try:
        _ = s.tparse('Tue Aug  6 11:10:57  1996g')
    except ValueError as e:
        fullmsg = str(e)
        msg = fullmsg.split(' -- ')[2]

    self.assertEqual(s.tparse.flag('Tue Aug  6 11:10:57  1996'), [-107398143.0,''])
    self.assertEqual(s.tparse.flag('JANUary 1, 2000 12:00'), [0.,''])
    self.assertEqual(s.tparse.flag('Tue Aug  6 11:10:57  1996g')[1], msg)

    #### tpictr, timout 
    time  = 'Tue Aug 06 11:10:57  1996'
    pictr = 'Wkd Mon DD HR:MN:SC  YYYY'
    secs  = -107398143.0
    self.assertEqual(s.tparse(time), secs)
    self.assertEqual(s.tpictr(time), pictr)
    self.assertEqual(s.timout(secs + s.deltet(secs, 'UTC'), pictr), time)

    time  = 'JANUARY 01, 2000 12:00'
    pictr = 'MONTH DD, YYYY HR:MN'
    secs  = 0.
    self.assertEqual(s.tparse(time), secs)
    self.assertEqual(s.tpictr(time), pictr)
    self.assertEqual(s.timout(secs + s.deltet(secs, 'UTC'), pictr), time)

    self.assertRaises(ValueError, s.tpictr, 'Tue Aug  6 11:10:57  1996g')
    try:
        _ = s.tpictr('Tue Aug  6 11:10:57  1996g')
    except ValueError as e:
        fullmsg = str(e)
        msg = fullmsg.split(' -- ')[2]

    self.assertAllEqual(s.tpictr.flag('Tue Aug  6 11:10:57  1996'), ['Wkd Mon  DD HR:MN:SC  YYYY', True, ''])
    self.assertAllEqual(s.tpictr.flag('JANUary 1, 2000 12:00'), ['MONTH DD, YYYY HR:MN', True, ''])
    self.assertAllEqual(s.tpictr.flag('Tue Aug  6 11:10:57  1996g')[1:], [False, msg])

    self.assertEqual(s.timout(0., 'xxx'), 'xxx')

    ### timdef
    self.assertEqual(s.timdef('get', 'zone'), 'UTC-0')
    self.assertEqual(s.timdef('zone'), 'UTC-0')
    self.assertEqual(s.timdef('zone', 'pdt'), 'pdt')
    s.timdef('zone', 'UTC-0')

    s.timdef('set', 'calendar', 'mixed')
    self.assertEqual(s.timdef('get', 'calendar', ''), 'MIXED')
    self.assertEqual(s.timdef('get', 'calendar'), 'MIXED')
    self.assertEqual(s.timdef('calendar', '', ''), 'MIXED')
    self.assertEqual(s.timdef('calendar', ''), 'MIXED')
    self.assertEqual(s.timdef('calendar'), 'MIXED')

    s.timdef('set', 'calendar', 'gregorian')
    self.assertEqual(s.timdef('calendar'), 'GREGORIAN')
    self.assertEqual(s.timdef('get', 'calendar'), 'GREGORIAN')

    s.timdef('set', 'system', 'tdb')
    self.assertEqual(s.timdef('system'), 'TDB')
    self.assertEqual(s.timdef('get', 'system'), 'TDB')
    s.timdef('system', 'utc')
    self.assertEqual(s.timdef('system'), 'UTC')
    self.assertEqual(s.timdef('get', 'system'), 'UTC')
    s.timdef('set', 'system', 'tdb')

    ### tsetyr
    s.tsetyr(2000)
    self.assertEqual(s.tparse('Dec 31, 99'), 3155630400.0)
    s.tsetyr(1950)
    self.assertEqual(s.tparse('Dec 31, 99'), -129600.0)

    ### unitim
    self.assertAllClose(s.unitim(0., 'TAI', 'TDB'), 32.183927274)
    self.assertAllClose(s.unitim(0., 'TAI', 'JED'), 2451545.00037)

    #### unload
#     et = 17.65 * 365.25 * 86400.
#     print s.spkez(-82, et, 'J2000', 'NONE', 699)
#     print s.dtpool('BODY699_RADII')
# 
#     self.unload(PATH)
#     print s.spkez(-82, et, 'J2000', 'NONE', 699)
#     print s.dtpool('BODY699_RADII')

################################################################################
#########################################
# CSPICE1_SIGNATURES["fovray"] = ["string", "float[3]", "frame_name", "string",
#                                 "body_name", "time"]
# CSPICE1_RETURNS   ["fovray"] = ["bool"]
# CSPICE1_DOCSTRINGS["fovray"] = """
# Determine if a specified ray is within the field-of-view (FOV) of a
# specified instrument at a given time.
# 
# fovray(<string> inst, <float[3]> raydir, <string> rframe,
#                       <string> abcorr, <string> observer, <float> et)
#         -> <bool> visible
# 
# inst     = Name or ID code string of the instrument.
# raydir   = Ray's direction vector.
# rframe   = Body-fixed, body-centered frame for target body.
# abcorr   = Aberration correction flag.
# observer = Name or ID code string of the observer.
# et       = Time of the observation (seconds past J2000).
# visible  = Visibility flag (True/False).
# """
# 
# #########################################
# CSPICE1_SIGNATURES["fovtrg"] = ["string", "body_name", "string", "frame_name",
#                                 "string", "body_name", "time"]
# CSPICE1_RETURNS   ["fovtrg"] = ["bool"]
# CSPICE1_DOCSTRINGS["fovtrg"] = """
# Determine if a specified ephemeris object is within the field-of-view (FOV)
# of a specified instrument at a given time.
# 
# fovtrg(<string> inst, <string> target, <string> tshape, <string> tframe,
#                       <string> abcorr, <string> obsrvr, <float> et)
#         -> <bool> visible
# 
# inst    = Name or ID code string of the instrument.
# target  = Name or ID code string of the target.
# tshape  = Type of shape model used for the target.
# tframe  = Body-fixed, body-centered frame for target body.
# abcorr  = Aberration correction flag.
# obsrvr  = Name or ID code string of the observer.
# et      = Time of the observation (seconds past J2000).
# visible = Visibility flag (True/False).
# """
# 
# #########################################
# CSPICE1_SIGNATURES["getfov"] = ["int"]
# CSPICE1_RETURNS   ["getfov"] = ["string", "string", "float[3]", "float[*,3]"]
# CSPICE1_DOCSTRINGS["getfov"] = """
# This subroutine returns the field-of-view (FOV) configuration for a
# specified instrument.
# 
# getfov(<int> instid)
#         -> [<string> shape, <string> frame,
#                             <float[3]> bsight, <float[*,3]> bounds]
# 
# instid = NAIF ID of an instrument.
# shape  = Instrument FOV shape.
# frame  = Name of the frame in which FOV vectors are defined.
# bsight = Boresight vector.
# bounds = FOV boundary vectors.
# """
# 
# #########################################
# CSPICE1_SIGNATURES["occult"] = 2*["body_name", "string", "frame_name"] + \
#                                ["string", "body_name", "time"]
# CSPICE1_RETURNS   ["occult"] = ["int"]
# CSPICE1_DOCSTRINGS["occult"] = """
# Determines the occultation condition (not occulted, partially, etc.) of one
# target relative to another target as seen by an observer at a given time.
# 
# The surfaces of the target bodies may be represented by triaxial ellipsoids
# or by topographic data provided by DSK files.
# 
# occult(<string> targ1, <string> shape1,  <string> frame1,
#         <string> targ2,  <string> shape2,  <string> frame2,
#         <string> abcorr, <string> obsrvr, <float> et)
#         -> <int> ocltid
# 
# targ1  = Name or ID of first target.
# shape1 = Type of shape model used for first target.
# frame1 = Body-fixed, body-centered frame for first body.
# targ2  = Name or ID of second target.
# shape2 = Type of shape model used for second target.
# frame2 = Body-fixed, body-centered frame for second body.
# abcorr = Aberration correction flag.
# obsrvr = Name or ID of the observer.
# et     = Time of the observation (seconds past J2000).
# ocltid = Occultation identification code.
# """
# 
# #########################################
# CSPICE1_SIGNATURES["pckcov"] = ["string", "frame_code"]
# CSPICE1_RETURNS   ["pckcov"] = ["float[*,2]"]
# CSPICE1_DOCSTRINGS["pckcov"] = """
# Find the coverage window for a specified reference frame in a specified
# binary PCK file.
# 
# pckcov(<string> pck, <int> idcode)
#         -> <float[:,2]> cover
# 
# pck    = Name of PCK file.
# idcode = Class ID code of PCK reference frame.
# cover  = An array of shape (n,2), where cover[:,0] are start times and
#          cover[:,1] are stop times.
# """
# 
# CSPICE1_SIGNATURES["pckcov_error"] = ["string", "frame_code"]
# CSPICE1_RETURNS   ["pckcov_error"] = ["float[*,2]"]
# CSPICE1_DOCSTRINGS["pckcov_error"] = """
# Find the coverage window for a specified reference frame in a specified
# binary PCK file.
# 
# pckcov(<string> pck, <int> idcode)
#         -> <float[:,2]> cover
# 
# pck    = Name of PCK file.
# idcode = Class ID code of PCK reference frame.
# cover  = An array of shape (n,2), where cover[:,0] are start times and
#          cover[:,1] are stop times.
# 
# Raise KeyError if the idcode is not found.
# """
# 
# #########################################
# CSPICE1_SIGNATURES["sincpt"] = ["string", "body_name", "time", "frame_name",
#                                 "string", "body_name", "frame_name", "float[3]"]
# CSPICE1_RETURNS   ["sincpt"] = ["float[3]", "time", "float[3]", "bool"]
# CSPICE1_DOCSTRINGS["sincpt"] = """
# Given an observer and a direction vector defining a ray, compute the
# surface intercept of the ray on a target body at a specified epoch,
# optionally corrected for light time and stellar aberration.
# 
# The surface of the target body may be represented by a triaxial ellipsoid
# or by topographic data provided by DSK files.
# 
# This routine supersedes srfxpt.
# 
# sincpt(<string> method, <string> target, <float> et, <string> fixref,
#        <string> abcorr, <string> obsrvr, dref, <float[3]> dvec)
#         -> [<float[3]> spoint, <float> trgepc,
#             <float[3]> srfvec, <bool> found]
# 
# method = Computation method.
# target = Name of target body.
# et     = Epoch in TDB seconds past J2000 TDB.
# fixref = Body-fixed, body-centered target body frame.
# abcorr = Aberration correction flag.
# obsrvr = Name of observing body.
# dref   = Reference frame of ray's direction vector.
# dvec   = Ray's direction vector.
# spoint = Surface intercept point on the target body.
# trgepc = Intercept epoch.
# srfvec = Vector from observer to intercept point.
# found  = Flag indicating whether intercept was found.
# """
# 
# #########################################
# CSPICE1_SIGNATURES["subpnt"] = ["string", "body_name", "time", "frame_name",
#                                 "string", "body_name"]
# CSPICE1_RETURNS   ["subpnt"] = ["float[3]", "time", "float[3]"]
# CSPICE1_DOCSTRINGS["subpnt"] = """
# Compute the rectangular coordinates of the sub-observer point on a target
# body at a specified epoch, optionally corrected for light time and stellar
# aberration.
# 
# The surface of the target body may be represented by a triaxial ellipsoid
# or by topographic data provided by DSK files.
# 
# This routine supersedes subpt.
# 
# subpnt(<string> method, <string> target, <float> et,
#        <string> fixref, <string> abcorr, <string> obsrvr)
#         -> [<float[3]> spoint, <float> trgepc, <float[3]> srfvec]
# 
# method = Computation method.
# target = Name of target body.
# et     = Epoch in TDB seconds past J2000 TDB.
# fixref = Body-fixed, body-centered target body frame.
# abcorr = Aberration correction flag.
# obsrvr = Name of observing body.
# spoint = Sub-observer point on the target body.
# trgepc = Sub-observer point epoch.
# srfvec = Vector from observer to sub-observer point.
# """
# 
# #########################################
# CSPICE1_SIGNATURES["subpt"] = ["string", "body_name", "time", "string",
#                                "body_name"]
# CSPICE1_RETURNS   ["subpt"] = ["float[3]", "float"]
# CSPICE1_DOCSTRINGS["subpt"] = """
# Compute the rectangular coordinates of the sub-observer point on a target
# body at a particular epoch, optionally corrected for planetary (light time)
# and stellar aberration.  Retur nn these coordinates expressed in the
# body-fixed frame associated with the target body.  Also, return the
# observer's altitude above the target body.
# 
# subpt(<string> method, <string> target, <float> et,
#       <string> abcorr, <string> obsrvr)
#         -> [<float[3]> spoint, <float> alt]
# 
# method = Computation method.
# target = Name of target body.
# et     = Epoch in ephemeris seconds past J2000 TDB.
# abcorr = Aberration correction.
# obsrvr = Name of observing body.
# spoint = Sub-observer point on the target body.
# alt    = Altitude of the observer above the target body.
# """
# 
# #########################################
# CSPICE1_SIGNATURES["subslr"] = ["string", "body_name", "time", "string",
#                                 "body_name"]
# CSPICE1_RETURNS   ["subslr"] = ["float[3]", "time", "float[3]"]
# CSPICE1_DOCSTRINGS["subslr"] = """
# Compute the rectangular coordinates of the sub-solar point on a target body
# at a specified epoch, optionally corrected for light time and stellar
# aberration.
# 
# The surface of the target body may be represented by a triaxial ellipsoid
# or by topographic data provided by DSK files.
# 
# This routine supersedes subsol.
# 
# subslr(<string> method, <string> target, <float> et,
#        <string> fixref, <string> abcorr, <string> obsrvr)
#         -> [<float[3]> spoint, <float> trgepc, <float[3]> srfvec]
# 
# method = Computation method.
# target = Name of target body.
# et     = Epoch in ephemeris seconds past J2000 TDB.
# fixref = Body-fixed, body-centered target body frame.
# abcorr = Aberration correction.
# obsrvr = Name of observing body.
# spoint = Sub-solar point on the target body.
# trgepc = Sub-solar point epoch.
# srfvec = Vector from observer to sub-solar point.
# """
# 
# #########################################
# CSPICE1_SIGNATURES["subsol"] = ["string", "body_name", "time", "string",
#                                 "body_name"]
# CSPICE1_RETURNS   ["subsol"] = ["float[3]"]
# CSPICE1_DOCSTRINGS["subsol"] = """
# Determine the coordinates of the sub-solar point on a target body as seen
# by a specified observer at a specified epoch, optionally corrected for
# planetary (light time) and stellar aberration.
# 
# subsol(<string> method, <string> target, <float> et,
#        <string> abcorr, <string> obsrvr)
#         -> <float[3]> spoint
# 
# method = Computation method.
# target = Name of target body.
# et     = Epoch in ephemeris seconds past J2000 TDB.
# abcorr = Aberration correction.
# obsrvr = Name of observing body.
# spoint = Sub-solar point on the target body.
# """
# 
# #########################################
# CSPICE1_SIGNATURES["surfnm"] = 3*["float"] + ["float[3]"]
# CSPICE1_RETURNS   ["surfnm"] = ["float[3]"]
# CSPICE1_DOCSTRINGS["surfnm"] = """
# This routine computes the outward-pointing, unit normal vector from a point
# on the surface of an ellipsoid.
# 
# surfnm(<float> a, <float> b, <float> s, <float[3]> point)
#         -> <float[3]> normal
# 
# a      = Length of the ellisoid semi-axis along the x-axis.
# b      = Length of the ellisoid semi-axis along the y-axis.
# s      = Length of the ellisoid semi-axis along the z-axis.
# point  = Body-fixed coordinates of a point on the ellipsoid
# normal = Outward pointing unit normal to ellipsoid at point
# """
# 
# #########################################
# CSPICE1_SIGNATURES["surfpt"] = 2*["float[3]"] + 3*["float"]
# CSPICE1_RETURNS   ["surfpt"] = ["float[3]", "bool"]
# CSPICE1_DOCSTRINGS["surfpt"] = """
# Determine the intersection of a line-of-sight vector with the surface of an
# ellipsoid.
# 
# surfpt(<float[3]> positn, <float[3]> u,
#        <float> a, <float> b, <float> s)
#         -> [<float[3]> point, <bool> found]
# 
# positn = Position of the observer in body-fixed frame.
# u      = Vector from the observer in some direction.
# a      = Length of the ellipsoid semi-axis along the x-axis.
# b      = Length of the ellipsoid semi-axis along the y-axis.
# s      = Length of the ellipsoid semi-axis along the z-axis.
# point  = Point on the ellipsoid pointed to by u.
# found  = Flag indicating if u points at the ellipsoid.
# """
# 
# #########################################
# CSPICE1_SIGNATURES["surfpv"] = 2*["float[6]"] + 3*["float"]
# CSPICE1_RETURNS   ["surfpv"] = ["float[6]", "bool"]
# CSPICE1_DOCSTRINGS["surfpv"] = """
# Find the state (position and velocity) of the surface intercept defined by a
# specified ray, ray velocity, and ellipsoid.
# 
# surfpv(<float[6]> stvrtx, <float[6]> stdir,
#        <float> a, <float> b, <float> s)
#         -> [<float[6]> stx, <bool> found]
# 
# stvrtx = State of ray's vertex.
# stdir  = State of ray's direction vector.
# a      = Length of ellipsoid semi-axis along the x-axis.
# b      = Length of ellipsoid semi-axis along the y-axis.
# s      = Length of ellipsoid semi-axis along the z-axis.
# stx    = State of surface intercept.
# found  = Flag indicating whether intercept state was found.
# """
# 
# #########################################
# SPYCE_SIGNATURES["termpt"] = ["string", "body_name", "body_name", "time",
#                               "frame_name", "string", "string", "body_name",
#                               "float[3]", "float", "int", "float", "float",
#                               "int"]
# SPYCE_ARGNAMES  ["termpt"] = ["method", "ilusrc", "target", "et", "fixref",
#                               "abcorr", "corloc", "obsrvr", "refvec",
#                               "rolstp", "ncuts", "schstp", "soltol", "maxn"]
# SPYCE_RETURNS   ["termpt"] = ["int[*]", "float[*,3]", "float[*]",
#                               "float[*,3]"]
# SPYCE_DOCSTRINGS["termpt"] = """
# Find terminator points on a target body. The caller specifies
# half-planes, bounded by the illumination source center-target center
# vector, in which to search for terminator points.
# 
# The terminator can be either umbral or penumbral. The umbral
# terminator is the boundary of the region on the target surface where
# no light from the source is visible. The penumbral terminator is the
# boundary of the region on the target surface where none of the light
# from the source is blocked by the target itself.
# 
# The surface of the target body may be represented either by a triaxial
# ellipsoid or by topographic data.
# 
# limbpt(<string> method, <string> ilusrc, <string> target, <float> et,
#                         <string> fixref, <string> abcorr, <string> corloc,
#                         <string> obsrvr, <float[3]> refvec, <float> rolstp,
#                         <int> ncuts, <float> schstp, <float> soltol,
#                         <int> maxn)
#     -> [<int[*]> npts, <float[*,3]> points, <float[*]> epochs,
#                        <float[*,3]> tangts]
# 
# method = Computation method.
# ilusrc = Illumination source.
# target = Name of target body.
# et     = Epoch in ephemeris seconds past J2000 TDB.
# fixref = Body-fixed, body-centered target body frame.
# abcorr = Aberration correction.
# corloc = Aberration correction locus.
# obsrvr = Name of observing body.
# refvec = Reference vector for cutting half-planes.
# rolstp = Roll angular step for cutting half-planes.
# ncuts  = Number of cutting planes.
# schstp = Angular step size for searching.
# soltol = Solution convergence tolerance.
# maxn   = Maximum number of entries in output arrays.
# npts   = Counts of terminator points corresponding to cuts.
# points = Terminator points.
# epochs = Times associated with terminator points.
# trmvcs = Terminator vectors emanating from the observer.
# 
# https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/termpt_c.html
# """
# 
# #########################################
# CSPICE1_SIGNATURES["tipbod"] = ["frame_code", "body_code", "time"]
# CSPICE1_RETURNS   ["tipbod"] = ["rotmat[3,3]"]
# CSPICE1_DOCSTRINGS["tipbod"] = """
# Return a 3x3 matrix that transforms positions in inertial coordinates to
# positions in body-equator-and-prime-meridian coordinates.
# 
# tipbod(<int> ref, <int> body, <float> et)
#         -> <float[3,3]> tipm
# 
# ref  = ID of inertial reference frame to transform from.
# body = ID code of body.
# et   = Epoch of transformation.
# tipm = Transformation (position), inertial to prime meridian.
# """
# 
# #########################################
# CSPICE1_SIGNATURES["tisbod"] = ["frame_code", "body_code", "time"]
# CSPICE1_RETURNS   ["tisbod"] = ["rotmat[6,6]"]
# CSPICE1_DOCSTRINGS["tisbod"] = """
# Return a 6x6 matrix that transforms states in inertial coordinates to
# states in body-equator-and-prime-meridian coordinates.
# 
# tisbod(<int> ref, <int> body, <float> et)
#         -> <float[6,6]> tsipm
# 
# ref   = ID of inertial reference frame to transform from
# body  = ID code of body
# et    = Epoch of transformation
# tsipm = Transformation (state), inertial to prime meridian
# """
# 
# 
# #########################################
# CSPICE1_SIGNATURES["unload"] = ["string"]
# CSPICE1_RETURNS   ["unload"] = []
# CSPICE1_DOCSTRINGS["unload"] = """
# Unload a SPICE kernel.
# 
# unload(<string> file)
# 
# file = The name of a kernel to unload.
# """
# 
# #########################################
# SPYCE_SIGNATURES["xfmsta"] = ["float[6]", "string", "string", "string"]
# SPYCE_ARGNAMES  ["xfmsta"] = ["input_state", "input_coord_sys",
#                               "output_coord_sys", "body"]
# SPYCE_RETURNS   ["xfmsta"] = ["float[6]"]
# SPYCE_DOCSTRINGS["xfmsta"] = """
# Transform a state between coordinate systems.
# 
# xfmsta(<float[6]> input_state, <string> input_coord_sys,
#                                <string> output_coord_sys)
#                                <string> body)
#     -> <float[6] output_state
# 
# input_state      = Input state.
# input_coord_sys  = Current (input) coordinate system.
# output_coord_sys = Desired (output) coordinate system.
# body             = Name or NAIF ID of body with which coordinates are
#                    associated (if applicable).
# output_state     = Converted output state.
# 
# https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/xfmsta_c.html
# """
# 
################################################################################

import unittest

if __name__ == '__main__':

    unittest.main(verbosity=2)

################################################################################
