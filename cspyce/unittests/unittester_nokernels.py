################################################################################
# Unit tests for all the supported spyce functions that do not involve kernels.
################################################################################

import sys
import numpy as np
import numbers
import cspyce as s
import unittest

class Test_spyce1_nokernels(unittest.TestCase):

  PATH = s.__path__[0] + '/../unittest_support/'

  def assertAllEqual(self, arg1, arg2, tol=1.e-15):
    if type(arg1) == list:
        self.assertEqual(type(arg2), list)
        self.assertEqual(len(arg1), len(arg2))
        for (item1,item2) in zip(arg1,arg2):
            self.assertAllEqual(item1, item2)

    elif isinstance(arg1, np.ndarray):
        arg1 = np.array(arg1)
        arg2 = np.array(arg2)
        self.assertEqual(arg1.shape, arg2.shape)
        arg1 = arg1.flatten()
        arg2 = arg2.flatten()
        for (x1,x2) in zip(arg1,arg2):
            if isinstance(x1,numbers.Real):
                self.assertTrue(abs(x1 - x2) <= tol)
            else:
                self.assertEqual(x1, x2)

    elif isinstance(arg1, numbers.Real):
        self.assertTrue(abs(arg1 - arg2) <= tol)

    else:
        self.assertEqual(arg1, arg2)

  def runTest(self):

    #### constants
    halfpi = s.halfpi()
    pi = s.pi()
    twopi = s.twopi()
    self.assertEqual(pi, np.pi)
    self.assertEqual(halfpi, np.pi/2.)
    self.assertEqual(twopi, 2*np.pi)

    intmin = s.intmin()
    intmax = s.intmax()
    self.assertEqual(intmin, -2**31)
    self.assertEqual(intmax,  2**31-1)

    self.assertEqual(s.dpmin(), -1.7976931348623157e+308)
    self.assertEqual(s.dpmax(),  1.7976931348623157e+308)

    self.assertEqual(s.b1900(), 2415020.31352)
    self.assertEqual(s.b1950(), 2433282.42345905)
    self.assertEqual(s.clight(), 299792.458)

    self.assertEqual(s.dpr(), 180./pi)
    self.assertEqual(s.rpd(), 1./s.dpr())

    self.assertEqual(s.j1900(), 2415020.0)
    self.assertEqual(s.j1950(), 2433282.5)
    self.assertEqual(s.j2000(), 2451545.0)
    self.assertEqual(s.j2100(), 2488070.0)
    self.assertEqual(s.jyear(), 31557600.0)
    self.assertEqual(s.tyear(), 31556925.9747)
    self.assertEqual(s.spd(),   86400.0)

    #### axisar
    self.assertAllEqual(s.axisar([0,0,1],0.), [[ 1,0,0],[0, 1,0],[0,0,1]])
    self.assertAllEqual(s.axisar([0,0,1],pi), [[-1,0,0],[0,-1,0],[0,0,1]])

    self.assertAllEqual(s.axisar_vector([0,0,1],[0.,pi]), [[[ 1,0,0],[0, 1,0],[0,0,1]],
                                                           [[-1,0,0],[0,-1,0],[0,0,1]]])

    #### cgv2el, el2cgv
    ellipse = s.cgv2el([0,0,0], [1,0,0], [0,1,0])
    self.assertAllEqual(ellipse, [0, 0, 0, 1, 0, 0, 0, 1, 0])

    self.assertAllEqual(s.el2cgv(ellipse), [[0,0,0],[1,0,0],[0,1,0]])

    ellipse = s.cgv2el_vector([0,0,0], [[1,0,0],[2,0,0]], [0,1,0])
    self.assertAllEqual(ellipse, [[0, 0, 0, 1, 0, 0, 0, 1, 0],
                                  [0, 0, 0, 2, 0, 0, 0, 1, 0]])

    reverse = s.el2cgv_vector(ellipse)
    self.assertAllEqual(s.el2cgv_vector(ellipse), [[[0,0,0],[0,0,0]],
                                                   [[1,0,0],[2,0,0]],
                                                   [[0,1,0],[0,1,0]]])

    #### conics
    elem1 = [1.,0.,0.,0.,0.,0.,0.,1.]
    elem4 = [4.,0.,0.,0.,0.,0.,0.,1.]
    state10 = s.conics(elem1, 0.)
    state11 = s.conics(elem1, pi)
    state40 = s.conics(elem4, 0.)
    state48 = s.conics(elem4, 8*pi)

    self.assertAllEqual(state10, [ 1,0,0,0, 1  ,0.])
    self.assertAllEqual(state11, [-1,0,0,0,-1  ,0.])
    self.assertAllEqual(state40, [ 4,0,0,0, 0.5,0.])
    self.assertAllEqual(state48, [-4,0,0,0,-0.5,0.])

    test1 = s.conics_vector(elem1, [0., pi, twopi])
    self.assertAllEqual(test1, [[ 1,0,0,0, 1,0.],
                                [-1,0,0,0,-1,0.],
                                [ 1,0,0,0, 1,0.]])

    test1 = s.conics_vector([elem1, elem1, elem4, elem4], [0., pi, 0, 8*pi])
    self.assertAllEqual(test1, [[ 1,0,0,0, 1,  0.],
                                [-1,0,0,0,-1,  0.],
                                [ 4,0,0,0, 0.5,0.],
                                [-4,0,0,0,-0.5,0.]])

    #### convrt
    self.assertAllEqual(s.convrt( 1., 'inches', 'feet'), 1/12.)
    self.assertAllEqual(s.convrt(12., 'inches', 'feet'), 1.)

    self.assertAllEqual(s.convrt_vector([1.,12.], 'inches', 'feet'), [1/12.,1.])

    #### cyllat, cylrec, cylsph, radrec, reclat, reccyl, etc.
    self.assertAllEqual(s.cyllat(1,0,0), [1,0,0])
    self.assertAllEqual(s.cylrec(1,0,0), [1,0,0])
    self.assertAllEqual(s.cylsph(1,0,0), [1,halfpi,0])
    self.assertAllEqual(s.radrec(1,0,0), [1,0,0])

    self.assertAllEqual(s.reclat([1,0,0]), [1,0,0])
    self.assertAllEqual(s.reccyl([1,0,0]), [1,0,0])
    self.assertAllEqual(s.recsph([1,0,0]), [1,halfpi,0])
    self.assertAllEqual(s.recrad([1,0,0]), [1,0,0])

    self.assertAllEqual(s.sphlat(1,0,0), [1,0,halfpi])
    self.assertAllEqual(s.sphcyl(1,0,0), [0,0,1])
    self.assertAllEqual(s.sphrec(1,0,0), [0,0,1])

    self.assertAllEqual(s.latcyl(1,0,0), [1,0,0])
    self.assertAllEqual(s.latrec(1,0,0), [1,0,0])
    self.assertAllEqual(s.latsph(1.,0.,0.), [1,halfpi,0])

    self.assertAllEqual(s.cyllat_vector([1,2,3,4],0,0), [[1,2,3,4],
                                                         [0,0,0,0],
                                                         [0,0,0,0]])
    self.assertAllEqual(s.cylrec_vector([1,2,3,4],0,0), [[1,0,0],
                                                         [2,0,0],
                                                         [3,0,0],
                                                         [4,0,0]])
    self.assertAllEqual(s.cylsph_vector(0,0,[1,2,3,4]), [[1,2,3,4],
                                                         [0,0,0,0],
                                                         [0,0,0,0]])

    self.assertAllEqual(s.reclat_vector(5*[[1,0,0]]), [5*[1],5*[0],5*[0]])
    self.assertAllEqual(s.reccyl_vector(5*[[1,0,0]]), [5*[1],5*[0],5*[0]])
    self.assertAllEqual(s.recsph_vector(5*[[1,0,0]]), [5*[1],5*[halfpi],5*[0]])
    self.assertAllEqual(s.recrad_vector(5*[[1,0,0]]), [5*[1],5*[0],5*[0]])
    self.assertAllEqual(s.sphlat_vector([1,1],0,0), [[1,1],[0,0],2*[halfpi]])
    self.assertAllEqual(s.sphcyl_vector([1,1],0,0), [[0,0],[0,0],[1,1]])
    self.assertAllEqual(s.sphrec_vector([1,1],0,0), 2*[[0,0,1]])
    self.assertAllEqual(s.latcyl_vector(1.,0.,[0,0]), [[1,1],[0,0],[0,0]])
    self.assertAllEqual(s.latrec_vector(1.,[0,0],0), 2*[[1,0,0]])
    self.assertAllEqual(s.latsph_vector([1,2],0.,0.), [[1,2],2*[halfpi],[0,0]])

    #### dcyldr, dgeodr, dlatdr, drdcyl, etc.
    self.assertAllEqual(s.dcyldr(1.,0.,0.), [[1,0,0],[0,1,0],[0,0,1]])
    self.assertAllEqual(s.dgeodr(1.,0.,0.,1.,0.), [[0,1,0],[0,0,1,],[1,0,0]])
    self.assertAllEqual(s.dlatdr(1.,0.,0.), [[1,0,0],[0,1,0],[0,0,1]])
    self.assertAllEqual(s.drdcyl(1.,0.,0.), [[1,0,0],[0,1,0],[0,0,1]])
    self.assertAllEqual(s.drdgeo(1.,0.,0.,1.,0.),
                                        [[-0.84147098, 0., 0.54030231],
                                         [ 0.54030231, 0., 0.84147098],
                                         [ 0.        , 1., 0.        ]], 5e-9)
    self.assertAllEqual(s.drdlat(1.,0.,0.), [[1,0,0],[0,1,0],[0,0,1]])
    self.assertAllEqual(s.drdsph(1.,0.,0.), [[0,1,0],[0,0,0],[1,0,0]])
    self.assertAllEqual(s.dsphdr(1.,0.,0.), [[1,0,0],[0,0,-1],[0,1,0]])

    self.assertEqual(s.dcyldr_vector([1,2,3,4],0.,0.).shape, (4,3,3))
    self.assertEqual(s.dgeodr_vector(1.,0.,0.,[1,2,3,4],0.1).shape, (4,3,3))
    self.assertEqual(s.dlatdr_vector(1.,[1,2,3,4],0.).shape, (4,3,3))
    self.assertEqual(s.drdcyl_vector(1.,0.,[1,2,3,4]).shape, (4,3,3))
    self.assertEqual(s.drdgeo_vector([1,2,3,4],0.,0.,1.,0.).shape, (4,3,3))
    self.assertEqual(s.drdlat_vector(1.,0.,[1,2,3,4]).shape, (4,3,3))
    self.assertEqual(s.drdsph_vector(1.,0.,[1,2,3,4]).shape, (4,3,3))
    self.assertEqual(s.dsphdr_vector([1,2,3,4],0.,0.).shape, (4,3,3))

    #### det
    ident = np.array([[1,0,0],[0,1,0],[0,0,1]]).astype('float')
    self.assertEqual(s.det(ident), 1.)

    idents = np.arange(20).reshape(20,1,1) * ident
    self.assertAllEqual(s.det_vector(idents), np.arange(20)**3)

    #### diags
    result1 = np.array([[0,0],[0,2]])
    result2 = np.array([[1,1],[-1,1]]) * np.sqrt(0.5)
    self.assertAllEqual(s.diags2([[1,1],[1,1]])[0], result1)
    self.assertAllEqual(s.diags2([[1,1],[1,1]])[1], result2)

    self.assertTrue(s.diags2_vector([[[1,2],[2,1]],[[3,1],[1,3]]])[0].shape, (2,2,2))
    self.assertTrue(s.diags2_vector([[[1,2],[2,1]],[[3,1],[1,3]]])[1].shape, (2,2,2))

    # ducrss, dvcrss
    self.assertAllEqual(s.ducrss([1,0,0,1,0,0],[1,1,0,1,1,0]), [0,0,1,0,0,0])
    self.assertAllEqual(s.dvcrss([1,0,0,1,0,0],[1,1,0,1,1,0]), [0,0,1,0,0,2])

    self.assertAllEqual(s.ducrss_vector(2*[[1,0,0,1,0,0]],[1,1,0,1,1,0]), 2*[[0,0,1,0,0,0]])
    self.assertAllEqual(s.dvcrss_vector(2*[[1,0,0,1,0,0]],[1,1,0,1,1,0]), 2*[[0,0,1,0,0,2]])

    # dvdot
    self.assertEqual(s.dvdot(6*[1],6*[1]), 6)
    self.assertAllEqual(s.dvdot_vector(6*[1],[6*[1],6*[2]]), [6,12])

    # dvhat
    self.assertAllEqual(s.dvhat(6*[1]), (3*[np.sqrt(1./3.)] + 3*[0.]))
    self.assertAllEqual(s.dvhat_vector([6*[1],6*[2]]), 2*[3*[np.sqrt(1./3.)] + 3*[0.]])

    # dvnorm
    self.assertAllEqual(s.dvnorm(6*[1]), np.sqrt(3.))
    self.assertAllEqual(s.dvnorm_vector([6*[1],6*[2]]), [np.sqrt(3.),np.sqrt(12.)])

    # dvsep
    self.assertEqual(s.dvsep([1,0,0,0,1,0],[0,1,0,0,0,1]), -1)
    self.assertEqual(s.dvsep_vector([[1,0,0,0,1,0],[2,0,0,0,2,0]],[0,1,0,0,0,1]).shape, (2,))

    # edlimb
    results = s.edlimb(1., 2., 3., [4., 4., 4.])
    self.assertEqual(results.shape, ( 9,))

    results = s.edlimb_vector(1., 2., [3.,2.5,2.1,1.8], [4., 4., 4.])
    self.assertEqual(results.shape, (4,9))

    # eqncpv
    elem = (1.e5, 0.01, 0., 0., 0., 0.01, 0.1, 1., -0.1)
    state = s.eqncpv(0., 100., elem, 0., halfpi)
    self.assertTrue(np.all(np.abs(state) < 1.1e5))

    ra = np.arange(1000.)
    states = s.eqncpv_vector(0., 100., elem, ra, halfpi)
    for i in range(1000):
        self.assertTrue(np.all(np.abs(states[i]) < 1.1e5))

    # eul2m, m2eul
    mat1 = [[0,-1,0],[1,0,0],[0,0,1]]
    self.assertAllEqual(s.eul2m(pi,halfpi,pi,2,3,2), mat1)

    mat2 = [[0,0,-1],[0,-1,0],[-1,0,0]]
    self.assertAllEqual(s.eul2m(pi,pi,halfpi,2,3,2), mat2)

    self.assertAllEqual(s.eul2m_vector(pi, [halfpi,pi], [pi,halfpi], 2,3,2), [mat1,mat2])

    self.assertAllEqual(s.m2eul(mat1,2,3,2), [pi,halfpi,pi])
    self.assertAllEqual(s.m2eul(mat2,2,3,2), [0,pi,-halfpi])

    self.assertAllEqual(s.m2eul_vector([mat1,mat2],2,3,2), [[pi,0],[halfpi,pi],[pi,-halfpi]])

    # eul2xf, xf2eul
    angles1 = np.array([pi, halfpi, pi, 1, 0, -1])
    mat1 = np.array([[0,0,-1,0,0,0],[0,1,0,0,0,0],[1,0,0,0,0,0],
                     [0,0,0,0,0,-1],[2,0,0,0,1,0],[0,-2,0,1,0,0]])

    self.assertTrue(np.max(np.abs(s.eul2xf(angles1,1,2,3) - mat1)) < 3.e-16)

    angles2 = np.array([pi, pi, pi, 1, -1, 0])
    mat2 = np.array([[1,0,0,0,0,0],[0,1,0,0,0,0],[0,0,1,0,0,0],
                     [0,0,-1,1,0,0],[0,0,1,0,1,0],[1,-1,0,0,0,1]])

    self.assertAllEqual(s.eul2xf(angles2,1,2,3), mat2)

    angles = np.array([angles1, angles2])
    self.assertAllEqual(s.eul2xf_vector(angles,1,2,3), [mat1,mat2])

    angles1 = [0,halfpi,0,0,0,-2]
    self.assertAllEqual(s.xf2eul(mat1,1,2,3), [angles1,False])

    angles2 = [0,0,0,1,1,0]
    self.assertAllEqual(s.xf2eul(mat2,1,2,3), [angles2,True])

    self.assertAllEqual(s.xf2eul_vector([mat1,mat2],1,2,3), [[angles1,angles2],[False,True]])

    #### frame
    self.assertAllEqual(s.frame([1,0,0]), [[1,0,0],[0,0,-1],[0,1,0]])
    self.assertAllEqual(s.frame([0,1,0]), [[0,1,0],[0,0,1],[1,0,0]])

    # ident
    self.assertTrue(np.all(s.ident() == [[1,0,0],[0,1,0],[0,0,1]]))

    #### georec, recgeo
    self.assertAllEqual(s.georec(0,0,1,1,0.1), [2,0,0])
    self.assertAllEqual(s.recgeo([2,0,0],1,0.1), [0,0,1])

    self.assertAllEqual(s.georec_vector([0,0],0,1,1,0.1), 2*[[2,0,0]])

    self.assertAllEqual(s.recgeo_vector([2,0,0],[1,1],0.1), [[0,0],[0,0],[1,1]])

    #### repmc, etc.
    self.assertEqual(s.repmc('pi = ##!', '##', '3.14159'), 'pi = 3.14159!')
    self.assertEqual(s.repmct('On one, two, #', '#', 3, 'L'), 'On one, two, three')
    self.assertEqual(s.repmd('pi = #!', '#', pi, 6), 'pi = 3.14159E+00!')
    self.assertEqual(s.repmf('pi = #!', '#', pi, 6, 'F'), 'pi = 3.14159!')
    self.assertEqual(s.repmi('On 1, 2, #', '#', 3), 'On 1, 2, 3')
    self.assertEqual(s.repmot('On # base', '#', 3, 'L'), 'On third base')

    #### q2m, m2q, qxq
    self.assertAllEqual(s.q2m([1,0,0,0]), [[1,0,0],[0,1,0],[0,0,1]] ,0)
    self.assertAllEqual(s.m2q([[1,0,0],[0,1,0],[0,0,1]]), [1,0,0,0], 0)

    self.assertAllEqual(s.q2m_vector(2*[[1,0,0,0]]), 2*[[[1,0,0],[0,1,0],[0,0,1]]], 0)
    self.assertAllEqual(s.m2q_vector(3*[[[1,0,0],[0,1,0],[0,0,1]]]), 3*[[1,0,0,0]], 0)

    self.assertAllEqual(s.qxq([1,1,1,1],[1,0,0,0]), [1,1,1,1], 0)
    self.assertAllEqual(s.qxq_vector([1,1,1,1],2*[[1,0,0,0]]), 2*[4*[1]], 0)

    #### vequ, vequg
    self.assertAllEqual(s.vequ([1,2,3]), [1,2,3], 0)
    self.assertAllEqual(s.vequ_vector([[1,2,3],[4,5,6]]), [[1,2,3],[4,5,6]], 0)

    self.assertAllEqual(s.vequg([1,2,3]), [1,2,3], 0)
    self.assertAllEqual(s.vequg([4,5,6,7]), [4,5,6,7], 0)
    self.assertAllEqual(s.vequg_vector([1,2,3]), [1,2,3], 0)  # drop one dim
    self.assertAllEqual(s.vequg_vector([[1,2,3]]), [[1,2,3]], 0)  # retain dim
    self.assertAllEqual(s.vequg_vector([[1,2,3],[4,5,6]]), [[1,2,3],[4,5,6]], 0)

    #### mequ, mequg
    mat1 = np.arange(9).reshape(3,3)
    mat2 = mat1[::-1]
    self.assertAllEqual(s.mequ(mat1), mat1, 0)
    self.assertAllEqual(s.mequ_vector([mat1,mat2]), [mat1,mat2], 0)
    self.assertAllEqual(s.mequg(mat1), mat1, 0)
    self.assertAllEqual(s.mequg_vector([mat1,mat2]), [mat1,mat2], 0)

    #### mtxm, mtxmg
    mmat1 = np.matrix(mat1)
    mmat2 = np.matrix(mat2)
    prod = mmat1.T * mmat2
    self.assertAllEqual(s.mtxm(mat1, mat2), prod, 0)
    self.assertAllEqual(s.mtxm_vector(2*[mat1],mat2), 2*[prod], 0)
    self.assertAllEqual(s.mtxmg(mat1, mat2), prod, 0)
    self.assertAllEqual(s.mtxmg_vector(2*[mat1],mat2), 2*[prod], 0)

    #### mxm, mxmg
    prod = mmat1 * mmat2
    self.assertAllEqual(s.mxm(mat1, mat2), prod, 0)
    self.assertAllEqual(s.mxm_vector(2*[mat1],mat2), 2*[prod], 0)
    self.assertAllEqual(s.mxmg(mat1, mat2), prod, 0)
    self.assertAllEqual(s.mxmg_vector(2*[mat1],mat2), 2*[prod], 0)

    #### mxmt, mxmtg
    prod = mmat1 * mmat2.T
    self.assertAllEqual(s.mxmt(mat1, mat2), prod, 0)
    self.assertAllEqual(s.mxmt_vector(2*[mat1],mat2), 2*[prod], 0)
    self.assertAllEqual(s.mxmtg(mat1, mat2), prod, 0)
    self.assertAllEqual(s.mxmtg_vector(2*[mat1],mat2), 2*[prod], 0)

    #### mtxv, mtxvg
    vec = np.array([3,1,2])
    prod = np.dot(mat1.T,vec)
    self.assertAllEqual(s.mtxv(mat1, vec), prod, 0)
    self.assertAllEqual(s.mtxv_vector(2*[mat1],vec), 2*[prod], 0)
    self.assertAllEqual(s.mtxvg(mat1, vec), prod, 0)
    self.assertAllEqual(s.mtxvg_vector(2*[mat1],vec), 2*[prod], 0)

    #### mxv, mxvg
    vec = np.array([3,1,2])
    prod = np.dot(mat1,vec)
    self.assertAllEqual(s.mxv(mat1, vec), prod, 0)
    self.assertAllEqual(s.mxv_vector(2*[mat1],vec), 2*[prod], 0)
    self.assertAllEqual(s.mxvg(mat1, vec), prod, 0)
    self.assertAllEqual(s.mxvg_vector(2*[mat1],vec), 2*[prod], 0)

    #### vtmv, vtmvg
    vecT = np.array([vec])
    prod = np.dot(np.dot(vecT,mat1),vec)[0]
    self.assertAllEqual(s.vtmv(vec, mat1, vec), prod, 0)
    self.assertAllEqual(s.vtmv_vector(vec, 2*[mat1], vec), 2*[prod], 0)
    self.assertAllEqual(s.vtmvg(vec, mat1, vec), prod, 0)
    self.assertAllEqual(s.vtmvg_vector(vec, 2*[mat1], vec), 2*[prod], 0)

    #### xpose, xpose6, xposeg
    mat = np.arange(9).reshape(3,3)
    self.assertAllEqual(s.xpose(mat), np.swapaxes(mat,0,1), 0)

    mat = np.arange(18).reshape(2,3,3)
    self.assertAllEqual(s.xpose_vector(mat), np.swapaxes(mat,1,2), 0)

    mat = np.arange(36).reshape(6,6)
    self.assertAllEqual(s.xpose6(mat), np.swapaxes(mat,0,1), 0)

    mat = np.arange(72).reshape(2,6,6)
    self.assertAllEqual(s.xpose6_vector(mat), np.swapaxes(mat,1,2), 0)

    mat = np.arange(6).reshape(2,3)
    self.assertAllEqual(s.xposeg(mat), np.swapaxes(mat,0,1), 0)

    mat = np.arange(24).reshape(4,2,3)
    self.assertAllEqual(s.xposeg_vector(mat), np.swapaxes(mat,1,2), 0)

    # tkvrsn
    self.assertEqual(s.tkvrsn('toolkit'), 'CSPICE_N0066')

    # unorm, unormg, vhat, vhatg, vnorm, vnormg
    vec = np.array([1,2,3])
    vec2 = np.array([1,-3,2])
    mag = np.sqrt(np.sum(vec**2))
    unit = vec / mag

    self.assertAllEqual(s.unorm(vec), [unit,mag])
    self.assertAllEqual(s.unormg(vec), [unit,mag])
    self.assertAllEqual(s.unorm_vector([vec,vec2]), [[unit,vec2/mag], 2*[mag]])
    self.assertAllEqual(s.unormg_vector([vec,vec2]), [[unit,vec2/mag], 2*[mag]])

    self.assertAllEqual(s.vhat(vec), unit)
    self.assertAllEqual(s.vhatg(vec), unit)
    self.assertAllEqual(s.vhat_vector([vec,vec2]), [unit,vec2/mag])
    self.assertAllEqual(s.vhatg_vector([vec,vec2]), [unit,vec2/mag])

    self.assertAllEqual(s.vnorm(vec), mag)
    self.assertAllEqual(s.vnormg(vec), mag)
    self.assertAllEqual(s.vnorm_vector([vec,vec2]), [mag,mag])
    self.assertAllEqual(s.vnormg_vector([vec,vec2]), [mag,mag])

    # vequ, vequg, vminus, vminug, vadd, vaddg, vsub, vsubg, vlcom*, vzero, vscl
    vec1 = np.array([1,2,3])
    vec2 = np.array([2,4,6])
    vec3 = np.array([3,1,3])

    self.assertAllEqual(s.vequ(vec1), vec1, 0)
    self.assertAllEqual(s.vequg(vec1), vec1, 0)
    self.assertAllEqual(s.vequ_vector([vec1,vec2]), [vec1,vec2], 0)
    self.assertAllEqual(s.vequg_vector([vec1,vec2]), [vec1,vec2], 0)

    self.assertAllEqual(s.vequ_vector(vec1), vec1, 0) # drop one dim

    self.assertAllEqual(s.vminus(vec1), -vec1, 0)
    self.assertAllEqual(s.vminug(vec1), -vec1, 0)
    self.assertAllEqual(s.vminus_vector([vec1,vec2]), [-vec1,-vec2], 0)
    self.assertAllEqual(s.vminug_vector([vec1,vec2]), [-vec1,-vec2], 0)

    self.assertAllEqual(s.vadd(vec1,vec2), vec1+vec2, 0)
    self.assertAllEqual(s.vaddg(vec1,vec2), vec1+vec2, 0)
    self.assertAllEqual(s.vadd_vector([vec1,vec3],vec2), [vec1+vec2,vec3+vec2], 0)
    self.assertAllEqual(s.vaddg_vector([vec1,vec3],vec2), [vec1+vec2,vec3+vec2], 0)

    self.assertAllEqual(s.vsub(vec1,vec2), vec1-vec2, 0)
    self.assertAllEqual(s.vsubg(vec1,vec2), vec1-vec2, 0)
    self.assertAllEqual(s.vsub_vector([vec1,vec3],vec2), [vec1-vec2,vec3-vec2], 0)
    self.assertAllEqual(s.vsubg_vector([vec1,vec3],vec2), [vec1-vec2,vec3-vec2], 0)

    self.assertAllEqual(s.vlcom(2,vec1,3,vec2), 2*vec1 + 3*vec2, 0)
    self.assertAllEqual(s.vlcomg(2,vec1,3,vec2), 2*vec1 + 3*vec2, 0)
    self.assertAllEqual(s.vlcom_vector(2,[vec1,vec3],3,vec2), [2*vec1+3*vec2,2*vec3+3*vec2], 0)
    self.assertAllEqual(s.vlcomg_vector(2,[vec1,vec3],3,vec2), [2*vec1+3*vec2,2*vec3+3*vec2], 0)
    self.assertAllEqual(s.vlcom_vector([1,2],vec1,3,vec2), [1*vec1+3*vec2,2*vec1+3*vec2], 0)
    self.assertAllEqual(s.vlcomg_vector([1,2],vec1,3,vec2), [1*vec1+3*vec2,2*vec1+3*vec2], 0)

    self.assertAllEqual(s.vlcom3(2,vec1,3,vec2,4,vec3), 2*vec1 + 3*vec2 + 4*vec3, 0)
    self.assertAllEqual(s.vlcom3_vector([1,2],vec1,3,vec2,4,vec3),
                    [1*vec1 + 3*vec2 + 4*vec3,2*vec1 + 3*vec2 + 4*vec3], 0)

    self.assertTrue(s.vzero([0,0,0]))
    self.assertFalse(s.vzero([0,0,1.e-99]))
    self.assertTrue(s.vzerog([0,0,0,0]))
    self.assertFalse(s.vzerog([0,0,0,1.e-99]))

    self.assertAllEqual(s.vzero_vector([[0,0,0],[0,0,1]]), [True,False])
    self.assertAllEqual(s.vzerog_vector([[0,0,0,0],[0,0,0,1]]), [True,False])

    self.assertAllEqual(s.vscl(2,vec), 2*vec, 0)
    self.assertAllEqual(s.vsclg(2,vec), 2*vec, 0)
    self.assertAllEqual(s.vscl_vector([2,3],[vec,vec2]), [2*vec, 3*vec2], 0)
    self.assertAllEqual(s.vsclg_vector([2,3],[vec,vec2]), [2*vec, 3*vec2], 0)

    #### vpack, vupack
    self.assertAllEqual(s.vpack(1,2,3), [1,2,3], 0)
    self.assertAllEqual(s.vupack([2,3,4]), [2,3,4], 0)
    self.assertAllEqual(s.vpack_vector([0,1],2,3), [[0,2,3],[1,2,3]], 0)
    self.assertAllEqual(s.vupack_vector([[1,3,4],[2,3,4]]), [[1,2],[3,3],[4,4]], 0)

    self.assertAllEqual(s.vpack_vector(0,2,3), [0,2,3], 0)
    self.assertAllEqual(s.vpack_vector([0],2,3), [[0,2,3]], 0)

    #### vsep, vsepg
    self.assertAllEqual(s.vsep([1,0,0],[0,2,0]), halfpi, 0)
    self.assertAllEqual(s.vsepg([1,0,0,0],[0,0,2,0]), halfpi, 0)

    self.assertAllEqual(s.vsep([1,0,0],[2,2,0]), halfpi/2., 0)
    self.assertAllEqual(s.vsepg([1,0,0,0],[2,0,2,0]), halfpi/2., 0)

    self.assertAllEqual(s.vsep_vector( [1,0,0],[[0,2,0],[2,2,0]]), [halfpi,pi/4], 0)
    self.assertAllEqual(s.vsepg_vector([1,0,0],[[0,2,0],[2,2,0]]), [halfpi,pi/4], 0)

    #### vdot, vdotg
    self.assertAllEqual(s.vdot(vec,vec2),  np.dot(vec,vec2), 0)
    self.assertAllEqual(s.vdotg(vec,vec2), np.dot(vec,vec2), 0)

    self.assertAllEqual(s.vdot_vector(vec,[vec2,vec3]),  [np.dot(vec,vec2),np.dot(vec,vec3)], 0)
    self.assertAllEqual(s.vdotg_vector(vec,[vec2,vec3]), [np.dot(vec,vec2),np.dot(vec,vec3)], 0)

    self.assertAllEqual(s.vdotg_vector(vec,vec2), np.dot(vec,vec2), 0)

    #### vcrss, ucrss
    vec2 = [2,4,7] #can't be parallel to vec

    cross12 = np.cross(vec,vec2)
    cross13 = np.cross(vec,vec3)
    norm12 = np.sqrt(np.sum(cross12**2))
    norm13 = np.sqrt(np.sum(cross13**2))


    self.assertAllEqual(s.vcrss(vec,vec2), cross12, 0)
    self.assertAllEqual(s.ucrss(vec,vec2), cross12/norm12)

    self.assertAllEqual(s.vcrss_vector(vec,[vec2,vec3]), [cross12,cross13], 0)
    self.assertAllEqual(s.ucrss_vector(vec,[vec2,vec3]), [cross12/norm12,cross13/norm13])

    #### twovec
    self.assertAllEqual(s.twovec([1,0,0],1,[0,1,0],2), [[1,0,0],[0,1,0],[0,0,1]], 0)
    self.assertAllEqual(s.twovec([1,0,0],1,[1,1,0],2), [[1,0,0],[0,1,0],[0,0,1]], 0)

    self.assertAllEqual(s.twovec_vector([1,0,0],1,[[0,1,0],[1,1,0]],2),
                2*[[[1,0,0],[0,1,0],[0,0,1]]], 0)

    #### vperp, vproj
    self.assertAllEqual(s.vperp([1,2,3],[2,0,0]), [0,2,3], 0)
    self.assertAllEqual(s.vperp([1,2,3],[0,4,0]), [1,0,3], 0)
    self.assertAllEqual(s.vperp_vector([1,2,3],[[2,0,0],[0,4,0]]), [[0,2,3],[1,0,3]], 0)

    self.assertAllEqual(s.vproj([1,2,3],[2,0,0]), [1,0,0], 0)
    self.assertAllEqual(s.vproj([1,2,3],[0,4,0]), [0,2,0], 0)
    self.assertAllEqual(s.vproj_vector([1,2,3],[[2,0,0],[0,4,0]]), [[1,0,0],[0,2,0]], 0)

    #### vdist, vdistg
    self.assertAllEqual(s.vdist( vec,vec2), s.vnorm( vec - vec2), 0)
    self.assertAllEqual(s.vdistg(vec,vec2), s.vnormg(vec - vec2), 0)
    self.assertAllEqual(s.vdist_vector(vec,[vec2,vec3]),
                    [s.vnorm(vec - vec2),s.vnorm(vec - vec3)], 0)
    self.assertAllEqual(s.vdistg_vector(vec,[vec2,vec3]),
                    [s.vnorm(vec - vec2),s.vnorm(vec - vec3)], 0)

    #### vprjp
    self.assertAllEqual(s.vprjp([0,0,1],[1,1,1,1]), [0,0,1], 0)
    self.assertAllEqual(s.vprjp_vector(2*[[0,0,1]],[1,1,1,1]), 2*[[0,0,1]], 0)
    
    #### vprjpi
    self.assertAllEqual(s.vprjpi([0,0,1], [1,1,1,1], [1,0,0,1]),
                                    [[1,1,2], True], 0)
    self.assertAllEqual(s.vprjpi_vector(2*[[0,0,1]], [1,1,1,1], 4*[[1,0,0,1]]),
                                    [4*[[1,1,2]], 4*[True]], 0)

    #### vrel, vrelg
    self.assertAllEqual(s.vrel([1,0,0],[0,0,1]), np.sqrt(2), 0)
    self.assertAllEqual(s.vrel([2,0,0],[0,0,2]), np.sqrt(2), 0)
    self.assertAllEqual(s.vrel_vector([[1,0,0],[2,0,0]],
                                      [[0,1,0],[0,0,2]]), 2*[np.sqrt(2)], 0)
    
    self.assertAllEqual(s.vrelg([1,0,0],[0,0,1]), np.sqrt(2), 0)
    self.assertAllEqual(s.vrelg([2,0,0],[0,0,2]), np.sqrt(2), 0)
    self.assertAllEqual(s.vrelg_vector([[1,0,0],[2,0,0]],
                                       [[0,1,0],[0,0,2]]), 2*[np.sqrt(2)], 0)

    #### vrotv
    self.assertAllEqual(s.vrotv([1,1,0],[0,0,1],pi),   [-1,-1,0])
    self.assertAllEqual(s.vrotv([1,1,0],[0,0,1],pi/2), [-1, 1,0])
    self.assertAllEqual(s.vrotv_vector([1,1,0],[0,0,1],[pi,pi/2]),
                                            [[-1,-1,0],[-1,1,0]])

    #### isrot
    self.assertTrue(s.isrot([[1,0,0],[0,1,0],[0,0,1]],0,0))
    self.assertFalse(s.isrot([[1,0,0],[0,1,0],[0,0,0.9999999999]],0,0))
    self.assertTrue(s.isrot([[1,0,0],[0,1,0],[0,0,0.9999999999]],0.00001,0))

    self.assertAllEqual(s.isrot_vector([[1,0,0],[0,1,0],[0,0,0.9999999999]],
                                       [0,0.00001],0), [False,True])

    self.assertAllEqual(s.isrot_vector([[1,0,0],[0,1,0],[0,0,1]],0,0), True)

    #### invert
    ident = [[1,0,0],[0,1,0],[0,0,1]]
    self.assertAllEqual(s.invert(ident), ident, 0)

    mat = [[2,0,0],[0,0,-1],[0,1,0]]
    inv = s.invert(mat)
    self.assertAllEqual(np.dot(mat,inv), ident, 0)
    self.assertAllEqual(s.invert_vector([ident,mat]), [ident,inv], 0)

    #### invort
    mat = (np.arange(9) - 4.).reshape(3,3)
    inv = np.array([[-0.19047619, -0.04761905,  0.0952381 ],
                    [-0.16666667,  0.        ,  0.16666667],
                    [-0.0952381 ,  0.04761905,  0.19047619]])

    self.assertAllEqual(s.invort(mat), inv, 1.e-7)
    self.assertAllEqual(s.invort_vector(3*[mat]), 3*[inv], 1.e-7)

    #### indedpl
    self.assertAllEqual(s.inedpl(1.,1.,1.,[1,0,0,0]),
                        [[0,0,0,0,0,-1,0,1,0], True], 0)
    self.assertAllEqual(s.inedpl_vector(1.,1.,1.,[1,0,0,0]),
                        [[0,0,0,0,0,-1,0,1,0],True], 0)
    self.assertAllEqual(s.inedpl_vector([1.],1.,1.,[1,0,0,0]),
                        [[[0,0,0,0,0,-1,0,1,0]],[True]], 0)
    self.assertAllEqual(s.inedpl_vector(1.,1.,[1,1],[1,0,0,0]),
                        [2*[[0,0,0,0,0,-1,0,1,0]], 2*[True]], 0)

    #### inelpl
    self.assertAllEqual(s.inelpl([0,0,0,1,0,0,0,1,0],[1,0,0,0]),
                        [2,[0,-1,0],[0,1,0]])
    self.assertAllEqual(s.inelpl_vector([0,0,0,1,0,0,0,1,0],[1,0,0,0]),
                        [2,[0,-1,0],[0,1,0]])
    self.assertAllEqual(s.inelpl_vector([0,0,0,1,0,0,0,1,0],[[1,0,0,0]]),
                        [[2],[[0,-1,0]],[[0,1,0]]])
    self.assertAllEqual(s.inelpl_vector(4*[[0,0,0,1,0,0,0,1,0]],2*[[1,0,0,0]]),
                        [4*[2],4*[[0,-1,0]],4*[[0,1,0]]])

    #### inrypl
    self.assertAllEqual(s.inrypl([0,0,0],[1,0,0],[1,0,0,0]),
                        [1,[0,0,0]], 0)
    self.assertAllEqual(s.inrypl_vector([0,0,0],[1,0,0],[1,0,0,0]),
                        [1,[0,0,0]], 0)
    self.assertAllEqual(s.inrypl_vector([[0,0,0]],[1,0,0],[1,0,0,0]),
                        [[1],[[0,0,0]]], 0)
    self.assertAllEqual(s.inrypl_vector([0,0,0],[1,0,0],[[1,0,0,0],[2,0,0,0]]),
                        [2*[1],2*[[0,0,0]]], 0)

    #### nplnpt
    self.assertAllEqual(s.nplnpt([0,0,0],[0,0,7],[0,1,1]),
                        [[0,0,1], 1], 0)
    self.assertAllEqual(s.nplnpt([0,0,0],[0,0,7],[2,0,2]),
                        [[0,0,2], 2], 0)
    self.assertAllEqual(s.nplnpt_vector([0,0,0],[0,0,7],[0,1,1]),
                        [[0,0,1], 1], 0)
    self.assertAllEqual(s.nplnpt_vector([0,0,0],[[0,0,7]],[0,1,1]),
                        [[[0,0,1]], [1]], 0)
    self.assertAllEqual(s.nplnpt_vector([0,0,0],[0,0,7],[[0,1,1],[2,0,2]]),
                        [[[0,0,1],[0,0,2]], [1,2]], 0)

    #### nvc2pl
    self.assertAllEqual(s.nvc2pl([0,0,1],1), [0,0,1,1], 0)
    self.assertAllEqual(s.nvc2pl_vector([0,0,1],1), [0,0,1,1], 0)
    self.assertAllEqual(s.nvc2pl_vector([0,0,1],3*[1]),
                        3*[[0,0,1,1]], 0)

    #### nvp2pl
    self.assertAllEqual(s.nvp2pl([0,0,7],[2,0,0]), [0,0,1,0], 0)
    self.assertAllEqual(s.nvp2pl_vector([0,0,7],[2,0,0]), [0,0,1,0], 0)
    self.assertAllEqual(s.nvp2pl_vector([0,0,7],9*[[2,0,0]]),
                        9*[[0,0,1,0]], 0)

    #### npedln
    self.assertAllEqual(s.npedln(3,2,1,[6,0,0],[-1,0,0]), [[3,0,0],0])
    self.assertAllEqual(s.npedln(3,2,1,[6,0,6],[-1,0,0]), [[0,0,1],5])
    self.assertAllEqual(s.npedln_vector(3,2,1,[6,0,0],[-1,0,0]), [[3,0,0],0])
    self.assertAllEqual(s.npedln_vector(3,2,1,[[6,0,0],[6,0,6]],[-1,0,0]),
                        [[[3,0,0],[0,0,1]],[0,5]])

    #### npelpt
    self.assertAllEqual(s.npelpt([5,0,4],[0,0,0,2,0,0,0,3,0]), [[2,0,0],5])
    self.assertAllEqual(s.npelpt([0,7,3],[0,0,0,2,0,0,0,3,0]), [[0,3,0],5])
    self.assertAllEqual(s.npelpt_vector([5,0,4],[0,0,0,2,0,0,0,3,0]),
                        [[2,0,0],5])
    self.assertAllEqual(s.npelpt_vector([[5,0,4],[0,7,3]],[0,0,0,2,0,0,0,3,0]),
                        [[[2,0,0],[0,3,0]],[5,5]])

    #### oscelt
    self.assertAllEqual(s.oscelt([1,0,0,0,1,0], 0, 1),
                        [1,0,0,0,0,0,0,1])
    self.assertAllEqual(s.oscelt([1,0,0,0,1,0], 0, 0.25),
                        [1,3,0,0,0,0,0,0.25])
    self.assertAllEqual(s.oscelt_vector([1,0,0,0,1,0], 0, 1),
                        [1,0,0,0,0,0,0,1])
    self.assertAllEqual(s.oscelt_vector([1,0,0,0,1,0], 0, [1]),
                        [[1,0,0,0,0,0,0,1]])
    self.assertAllEqual(s.oscelt_vector([1,0,0,0,1,0], 0, [1,0.25]),
                        [[1,0,0,0,0,0,0,1],[1,3,0,0,0,0,0,0.25]])

    #### oscltx
    self.assertAllEqual(s.oscltx([1,0,0,0,1,0], 0, 1),
                        [1,0,0,0,0,0,0,1,0,1,twopi,0,0,0,0,0,0,0,0,0])
    self.assertAllEqual(s.oscltx([1,0,0,0,1,0], 0, 0.25),
                        [1,3,0,0,0,0,0,0.25,0,-0.5,0,0,0,0,0,0,0,0,0,0])
    self.assertAllEqual(s.oscltx_vector([1,0,0,0,1,0], 0, 1),
                        [1,0,0,0,0,0,0,1,0,1,twopi,0,0,0,0,0,0,0,0,0])
    self.assertAllEqual(s.oscltx_vector([1,0,0,0,1,0], [0],[1]),
                        [[1,0,0,0,0,0,0,1,0,1,twopi,0,0,0,0,0,0,0,0,0]])
    self.assertAllEqual(s.oscltx_vector([1,0,0,0,1,0], 0, [1,0.25]),
                        [[1,0,0,0,0,0,0,1,0,1,twopi,0,0,0,0,0,0,0,0,0],
                         [1,3,0,0,0,0,0,0.25,0,-0.5,0,0,0,0,0,0,0,0,0,0]])

    #### pjelpj
    self.assertAllEqual(s.pjelpl([0,0,0,2,0,0,0,3,0], [0,0,1,0]),
                        [0,0,0,0,3,0,2,0,0])
    self.assertAllEqual(s.pjelpl([0,0,0,2,0,0,0,4,0], [0,0,1,0]),
                        [0,0,0,0,4,0,2,0,0])
    self.assertAllEqual(s.pjelpl_vector([0,0,0,2,0,0,0,3,0], [0,0,1,0]),
                        [0,0,0,0,3,0,2,0,0])
    self.assertAllEqual(s.pjelpl_vector([0,0,0,2,0,0,0,3,0], [[0,0,1,0]]),
                        [[0,0,0,0,3,0,2,0,0]])
    self.assertAllEqual(s.pjelpl_vector([[0,0,0,2,0,0,0,3,0],
                                         [0,0,0,2,0,0,0,4,0]], [0,0,1,0]),
                        [[0,0,0,0,3,0,2,0,0],
                         [0,0,0,0,4,0,2,0,0]])

    #### pl2nvc
    self.assertAllEqual(s.pl2nvc([0,0,1,0]), [[0,0,1],0])
    self.assertAllEqual(s.pl2nvc([0,0,0,1]), [[0,0,0],1])
    self.assertAllEqual(s.pl2nvc_vector([0,0,1,0]), [[0,0,1],0])
    self.assertAllEqual(s.pl2nvc_vector([[0,0,1,0]]), [[[0,0,1]],[0]])
    self.assertAllEqual(s.pl2nvc_vector([[0,0,1,0],[0,0,0,1]]),
                        [[[0,0,1],[0,0,0]],[0,1]])

    #### pl2nvp
    self.assertAllEqual(s.pl2nvp([0,0,1,0]), [[0,0,1],[0,0,0]])
    self.assertAllEqual(s.pl2nvp([0,1,0,0]), [[0,1,0],[0,0,0]])
    self.assertAllEqual(s.pl2nvp_vector([0,0,1,0]), [[0,0,1],[0,0,0]])
    self.assertAllEqual(s.pl2nvp_vector([[0,0,1,0],[0,1,0,0]]),
                        [[[0,0,1],[0,1,0]],2*[[0,0,0]]])

    #### pl2psv
    self.assertAllEqual(s.pl2psv([0,0,1,0]), [[0,0,0],[0,-1,0],[1,0,0]])
    self.assertAllEqual(s.pl2psv([0,1,0,0]), [[0,0,0],[0,0,1],[1,0,0]])
    self.assertAllEqual(s.pl2psv_vector([0,0,1,0]), [[0,0,0],[0,-1,0],[1,0,0]])
    self.assertAllEqual(s.pl2psv_vector([[0,0,1,0],[0,1,0,0]]),
                        [2*[[0,0,0]],[[0,-1,0],[0,0,1]],2*[[1,0,0]]])

    #### psv2pl
    self.assertAllEqual(s.psv2pl([0,0,0],[2,0,0],[0,3,0]), [0,0,1,0])
    self.assertAllEqual(s.psv2pl([0,0,0],[2,0,0],[0,1,0]), [0,0,1,0])
    self.assertAllEqual(s.psv2pl_vector([0,0,0],[2,0,0],[0,3,0]), [0,0,1,0])
    self.assertAllEqual(s.psv2pl_vector([0,0,0],[2,0,0],[[0,3,0],[0,1,0]]),
                        2*[[0,0,1,0]])

    #### raxisa
    self.assertAllEqual(s.raxisa([[0,1,0],[1,0,0],[0,0,-1]]),
                        [[-np.sqrt(0.5), -np.sqrt(0.5), 0.], pi])
    self.assertAllEqual(s.raxisa([[1,0,0],[0,0,1],[0,-1,0]]),
                        [[-1,0,0], halfpi])
    self.assertAllEqual(s.raxisa_vector([[0,1,0],[1,0,0],[0,0,-1]]),
                        [[-np.sqrt(0.5), -np.sqrt(0.5), 0.], pi])
    self.assertAllEqual(s.raxisa_vector([[[0,1,0],[1,0,0],[0,0,-1]],
                                         [[1,0,0],[0,0,1],[0,-1,0]]]),
                        [[[-np.sqrt(0.5),-np.sqrt(0.5),0],[-1,0,0]],
                         [pi,halfpi]])

    #### prop2b
    self.assertAllEqual(s.prop2b(1,[1,0,0,0,1,0],pi/2), [0,1,0,-1,0,0])
    self.assertAllEqual(s.prop2b(1,[1,0,0,0,1,0],pi/4),
                        np.array([1,1,0,-1,1,0]) / np.sqrt(2))
    self.assertAllEqual(s.prop2b_vector(1,[1,0,0,0,1,0],pi/2), [0,1,0,-1,0,0])
    self.assertAllEqual(s.prop2b_vector(1,[1,0,0,0,1,0],[pi/2,pi/4]),
                        [[0,1,0,-1,0,0],np.array([1,1,0,-1,1,0]) / np.sqrt(2)])

    #### nearpt
    self.assertAllEqual(s.nearpt([3,0,0],2,3,1), [[2,0,0],1])
    self.assertAllEqual(s.nearpt([0,0,3],2,3,1), [[0,0,1],2])
    self.assertAllEqual(s.nearpt_vector([3,0,0],2,3,1), [[2,0,0],1])
    self.assertAllEqual(s.nearpt_vector([[3,0,0],[0,0,3]],2,3,1),
                        [[[2,0,0],[0,0,1]],[1,2]])

    #### qdq2av
    self.assertAllEqual(s.qdq2av([1,0,0,0],[0,0,0,0]), [ 0,0,0])
    self.assertAllEqual(s.qdq2av([1,0,0,0],[0,1,0,0]), [-2,0,0])
    self.assertAllEqual(s.qdq2av_vector([1,0,0,0],[0,0,0,0]), [ 0,0,0])
    self.assertAllEqual(s.qdq2av_vector([1,0,0,0],[[0,0,0,0],[0,1,0,0]]),
                        [[0,0,0],[-2,0,0]])

    #### rav2xf
    mat1 = [[0,1,0],[-1,0,0],[0,0,-1]]
    result1 = [[ 0, 1, 0, 0, 0, 0.],
               [-1, 0, 0, 0, 0, 0.],
               [ 0, 0,-1, 0, 0, 0.],
               [ 0, 0, 0, 0, 1, 0.],
               [ 0, 0, 0,-1, 0, 0.],
               [ 0, 0, 0, 0, 0,-1.]]
    result2 = [[ 0, 1, 0, 0, 0, 0.],
               [-1, 0, 0, 0, 0, 0.],
               [ 0, 0,-1, 0, 0, 0.],
               [ 0, 0, 1, 0, 1, 0.],
               [ 0, 0, 0,-1, 0, 0.],
               [ 0, 1, 0, 0, 0,-1.]]

    self.assertAllEqual(s.rav2xf(mat1,[0,0,0]), result1)
    self.assertAllEqual(s.rav2xf(mat1,[1,0,0]), result2)
    self.assertAllEqual(s.rav2xf_vector(mat1,[0,0,0]), result1)
    self.assertAllEqual(s.rav2xf_vector([mat1],[0,0,0]), [result1])
    self.assertAllEqual(s.rav2xf_vector(mat1,[[0,0,0],[1,0,0]]),
                                        [result1,result2])

    self.assertAllEqual(s.rotate(0,1), ident)
    self.assertAllEqual(s.rotate(pi,1), [[1,0,0],[0,-1,0],[0,0,-1]])
    self.assertAllEqual(s.rotate(halfpi,1), [[1,0,0],[0,0,1],[0,-1,0]])
    self.assertAllEqual(s.rotate_vector(0,1), ident)
    self.assertAllEqual(s.rotate_vector([0],1), [ident])
    self.assertAllEqual(s.rotate_vector(3*[0],1), 3*[ident])

    #### rotmat
    self.assertAllEqual(s.rotmat(ident,0,1), ident)
    self.assertAllEqual(s.rotmat(ident,pi,1), [[1,0,0],[0,-1,0],[0,0,-1]])
    self.assertAllEqual(s.rotmat_vector(ident,0,1), ident)
    self.assertAllEqual(s.rotmat_vector(ident,[0],1), [ident])
    self.assertAllEqual(s.rotmat_vector(ident,[0,pi],1),
                                [ident, [[1,0,0],[0,-1,0],[0,0,-1]]])

    #### rotvec
    self.assertAllEqual(s.rotvec([1,0,0],0,2), [1,0,0])
    self.assertAllEqual(s.rotvec([1,0,0],pi,2), [-1,0,0])
    self.assertAllEqual(s.rotvec_vector([1,0,0],pi,2), [-1,0,0])
    self.assertAllEqual(s.rotvec_vector([[1,0,0]],[pi],2), [[-1,0,0]])
    self.assertAllEqual(s.rotvec_vector([[1,0,0]],[pi,0],2), [[-1,0,0],[1,0,0]])

    ##### rquad
    self.assertAllEqual(s.rquad(1,0,-1), [[1,0],[-1,0]])
    self.assertAllEqual(s.rquad(1,0, 1), [[0,1],[0,-1]])
    self.assertAllEqual(s.rquad_vector(1,0,-1), [[1,0],[-1,0]])
    self.assertAllEqual(s.rquad_vector(1,0,[-1]), [[[1,0]],[[-1,0]]])
    self.assertAllEqual(s.rquad_vector(1,0,[-1,1]),
                            [[[1,0],[0,1]],[[-1,0],[0,-1]]])

    ##### saelgv
    self.assertAllEqual(s.saelgv([2,0,0],[0,3,0]), [[0,3,0],[2,0,0]])
    self.assertAllEqual(s.saelgv_vector([2,0,0],[0,3,0]), [[0,3,0],[2,0,0]])
    self.assertAllEqual(s.saelgv_vector([2,0,0],[[0,3,0]]),
                            [[[0,3,0]],[[2,0,0]]])
    self.assertAllEqual(s.saelgv_vector([2,0,0],[[0,3,0],[0,1,0]]),
                            [[[0,3,0],[2,0,0]],[[2,0,0],[0,1,0]]])

    cxx = s.clight() / 100.
    eps = 2.e-9
    self.assertAllEqual(s.stelab([1,0,0],[cxx,0,0]), [1,0,0])
    self.assertAllEqual(s.stelab([1,0,0],[0,cxx,0]), [0.99995, 0.01, 0], eps)
    self.assertAllEqual(s.stelab_vector([1,0,0],[cxx,0,0]), [1,0,0])
    self.assertAllEqual(s.stelab_vector([[1,0,0]],[cxx,0,0]), [[1,0,0]])
    self.assertAllEqual(s.stelab_vector([1,0,0],[[cxx,0,0],[0,cxx,0]]),
                            [[1,0,0],[0.99995,0.01,0]], eps)

    self.assertAllEqual(s.stlabx([1,0,0],[cxx,0,0]), [1,0,0])
    self.assertAllEqual(s.stlabx([1,0,0],[0,cxx,0]), [0.99995,-0.01, 0], eps)
    self.assertAllEqual(s.stlabx_vector([1,0,0],[cxx,0,0]), [1,0,0])
    self.assertAllEqual(s.stlabx_vector([[1,0,0]],[cxx,0,0]), [[1,0,0]])
    self.assertAllEqual(s.stlabx_vector([1,0,0],[[cxx,0,0],[0,cxx,0]]),
                            [[1,0,0],[0.99995,-0.01,0]], eps)

    #### trace
    self.assertAllEqual(s.trace(ident), 3.)
    self.assertAllEqual(s.trace(np.arange(9).reshape(3,3)), 12.)
    self.assertAllEqual(s.trace_vector(np.arange(9).reshape(3,3)), 12.)
    self.assertAllEqual(s.trace_vector(np.arange(9).reshape(1,3,3)), [12.])
    self.assertAllEqual(s.trace_vector(np.arange(36).reshape(4,3,3)),
                            [12,39,66,93.])

    ##### pltarr, pltvol, pltexp, pltnp
    vertices = [[0,0,0],[0,0,1],[0,1,0],[1,0,0]]
    indices = [[1,2,3],[1,4,2],[1,3,4],[2,4,3]]

    self.assertAllEqual(s.pltar( vertices,indices), 1.5 + np.sqrt(3)/2.)
    self.assertAllEqual(s.pltvol(vertices,indices), 1/6.)

    self.assertAllEqual(s.pltexp([[0,0,0],[0,1,0],[1,0,0]], 0.),
                            [[0,0,0],[0,1,0],[1,0,0]])
    self.assertAllEqual(s.pltexp([[0,0,0],[0,1,0],[1,0,0]], 3.),
                            [[-1,-1,0],[-1,3,0],[3,-1,0]])

    self.assertAllEqual(s.pltnp([1,0,0],[0,0,0],[0,0,1],[0,1,0]),
                            [[0,0,0],1])
    self.assertAllEqual(s.pltnp([1,-1,0],[0,0,0],[0,0,1],[0,1,0]),
                            [[0,0,0],np.sqrt(2)])
    self.assertAllEqual(s.pltnp([1,1,1],[0,0,0],[0,0,1],[0,1,0]),
                            [[0,0.5,0.5],np.sqrt(1.5)])

################################################################################

import unittest

if __name__ == '__main__':

    unittest.main(verbosity=2)

################################################################################
