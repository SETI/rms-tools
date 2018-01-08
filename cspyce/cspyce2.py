################################################################################
# cspyce/cspyce2.py
################################################################################
# module cspyce.cspyce2
#
# This module re-declares every cspyce1 function explicitly, with its list of
# argument names as used by CSPICE. The practical effect is that functions in
# cspyce2 module can be called in a fully Python-like way, the rightmost inputs
# in any order and identified by their names.
#
# NOTE: This file is generated automatically using program make_cspyce2.py:
#   python make_cspyce2.py > cspyce2.py
#
################################################################################

# This function makes cspyce2 look the same as cspyce1. It ensures that every
# location in the global dictionary and every function's internal link point
# a new function of the same name.

def relink_all(new_dict, old_dict):

    # Assign a new function to the dictionary at the same location as every
    # cspyce function found in the old dictionary

    dict_names = {}     # maps each function name to its dictionary locations
    old_funcs = {}      # maps each function name to its old function
    for (dict_name, old_func) in old_dict.iteritems():
        if type(old_func).__name__ != 'function': continue
        if 'SIGNATURE' not in old_func.__dict__:  continue

        func_name = old_func.__name__
        old_funcs[func_name] = old_func

        if func_name not in dict_names:
            dict_names[func_name] = []

        dict_names[func_name].append(dict_name)

    for (name, keys) in dict_names.iteritems():
        func = new_dict[name]
        for key in keys:
            new_dict[key] = func

    # Make sure each cspyce function has the same properties and attributes as
    # the one in the old dictionary

    for (name, old_func) in old_funcs.iteritems():
        func = new_dict[name]

        # Copy function properties
        func.__doc__       = old_func.__doc__
        func.func_defaults = old_func.func_defaults

        # Copy attributes
        for (key, value) in old_func.__dict__.iteritems():
            if type(value).__name__ != 'function':
                func.__dict__[key] = value
            else:
                # If it's a function, locate a new one with the same name
                func.__dict__[key] = new_dict[value.__name__]


import cspyce.cspyce1 as cspyce1
from cspyce.cspyce1 import *

def axisar(axis, angle):
  return cspyce1.axisar(axis, angle)

def axisar_vector(axis, angle):
  return cspyce1.axisar_vector(axis, angle)

def b1900():
  return cspyce1.b1900()

def b1950():
  return cspyce1.b1950()

def bltfrm(frmcls):
  return cspyce1.bltfrm(frmcls)

def bodc2n(code):
  return cspyce1.bodc2n(code)

def bodc2n_error(code):
  return cspyce1.bodc2n_error(code)

def bodc2s(code):
  return cspyce1.bodc2s(code)

def boddef(name, code):
  return cspyce1.boddef(name, code)

def bodfnd(body, item):
  return cspyce1.bodfnd(body, item)

def bodn2c(name):
  return cspyce1.bodn2c(name)

def bodn2c_error(name):
  return cspyce1.bodn2c_error(name)

def bods2c(name):
  return cspyce1.bods2c(name)

def bods2c_error(name):
  return cspyce1.bods2c_error(name)

def bodvar(bodyid, item):
  return cspyce1.bodvar(bodyid, item)

def bodvcd(bodyid, item):
  return cspyce1.bodvcd(bodyid, item)

def bodvrd(bodynm, item):
  return cspyce1.bodvrd(bodynm, item)

def ccifrm(frclss, clssid):
  return cspyce1.ccifrm(frclss, clssid)

def ccifrm_error(frclss, clssid):
  return cspyce1.ccifrm_error(frclss, clssid)

def cgv2el(center, vec1, vec2):
  return cspyce1.cgv2el(center, vec1, vec2)

def cgv2el_vector(center, vec1, vec2):
  return cspyce1.cgv2el_vector(center, vec1, vec2)

def chkin(module):
  return cspyce1.chkin(module)

def chkout(module):
  return cspyce1.chkout(module)

def cidfrm(cent):
  return cspyce1.cidfrm(cent)

def cidfrm_error(cent):
  return cspyce1.cidfrm_error(cent)

def ckcov(ck, idcode, needav, level, tol, timsys):
  return cspyce1.ckcov(ck, idcode, needav, level, tol, timsys)

def ckcov_error(ck, idcode, needav, level, tol, timsys):
  return cspyce1.ckcov_error(ck, idcode, needav, level, tol, timsys)

def ckgp(inst, sclkdp, tol, ref):
  return cspyce1.ckgp(inst, sclkdp, tol, ref)

def ckgp_error(inst, sclkdp, tol, ref):
  return cspyce1.ckgp_error(inst, sclkdp, tol, ref)

def ckgp_vector(inst, sclkdp, tol, ref):
  return cspyce1.ckgp_vector(inst, sclkdp, tol, ref)

def ckgp_vector_error(inst, sclkdp, tol, ref):
  return cspyce1.ckgp_vector_error(inst, sclkdp, tol, ref)

def ckgpav(inst, sclkdp, tol, ref):
  return cspyce1.ckgpav(inst, sclkdp, tol, ref)

def ckgpav_error(inst, sclkdp, tol, ref):
  return cspyce1.ckgpav_error(inst, sclkdp, tol, ref)

def ckgpav_vector(inst, sclkdp, tol, ref):
  return cspyce1.ckgpav_vector(inst, sclkdp, tol, ref)

def ckgpav_vector_error(inst, sclkdp, tol, ref):
  return cspyce1.ckgpav_vector_error(inst, sclkdp, tol, ref)

def ckobj(ck):
  return cspyce1.ckobj(ck)

def clight():
  return cspyce1.clight()

def clpool():
  return cspyce1.clpool()

def cnmfrm(cname):
  return cspyce1.cnmfrm(cname)

def cnmfrm_error(cname):
  return cspyce1.cnmfrm_error(cname)

def conics(elts, et):
  return cspyce1.conics(elts, et)

def conics_vector(elts, et):
  return cspyce1.conics_vector(elts, et)

def convrt(x, in1, out):
  return cspyce1.convrt(x, in1, out)

def convrt_vector(x, in1, out):
  return cspyce1.convrt_vector(x, in1, out)

def cyllat(r, lonc, z):
  return cspyce1.cyllat(r, lonc, z)

def cyllat_vector(r, lonc, z):
  return cspyce1.cyllat_vector(r, lonc, z)

def cylrec(r, lon, z):
  return cspyce1.cylrec(r, lon, z)

def cylrec_vector(r, lon, z):
  return cspyce1.cylrec_vector(r, lon, z)

def cylsph(r, lonc, z):
  return cspyce1.cylsph(r, lonc, z)

def cylsph_vector(r, lonc, z):
  return cspyce1.cylsph_vector(r, lonc, z)

def dafbfs(handle):
  return cspyce1.dafbfs(handle)

def dafcls(handle):
  return cspyce1.dafcls(handle)

def daffna():
  return cspyce1.daffna()

def dafgda(handle, begin, end):
  return cspyce1.dafgda(handle, begin, end)

def dafgn(lenout):
  return cspyce1.dafgn(lenout)

def dafgs():
  return cspyce1.dafgs()

def dafopr(fname):
  return cspyce1.dafopr(fname)

def dafus(sum, nd, ni):
  return cspyce1.dafus(sum, nd, ni)

def dcyldr(x, y, z):
  return cspyce1.dcyldr(x, y, z)

def dcyldr_vector(x, y, z):
  return cspyce1.dcyldr_vector(x, y, z)

def deltet(epoch, eptype):
  return cspyce1.deltet(epoch, eptype)

def deltet_vector(epoch, eptype):
  return cspyce1.deltet_vector(epoch, eptype)

def det(m1):
  return cspyce1.det(m1)

def det_vector(m1):
  return cspyce1.det_vector(m1)

def dgeodr(x, y, z, re, f):
  return cspyce1.dgeodr(x, y, z, re, f)

def dgeodr_vector(x, y, z, re, f):
  return cspyce1.dgeodr_vector(x, y, z, re, f)

def diags2(symmat):
  return cspyce1.diags2(symmat)

def diags2_vector(symmat):
  return cspyce1.diags2_vector(symmat)

def dlatdr(x, y, z):
  return cspyce1.dlatdr(x, y, z)

def dlatdr_vector(x, y, z):
  return cspyce1.dlatdr_vector(x, y, z)

def dpgrdr(body, x, y, z, re, f):
  return cspyce1.dpgrdr(body, x, y, z, re, f)

def dpgrdr_vector(body, x, y, z, re, f):
  return cspyce1.dpgrdr_vector(body, x, y, z, re, f)

def dpmax():
  return cspyce1.dpmax()

def dpmin():
  return cspyce1.dpmin()

def dpr():
  return cspyce1.dpr()

def drdcyl(r, lon, z):
  return cspyce1.drdcyl(r, lon, z)

def drdcyl_vector(r, lon, z):
  return cspyce1.drdcyl_vector(r, lon, z)

def drdgeo(lon, lat, alt, re, f):
  return cspyce1.drdgeo(lon, lat, alt, re, f)

def drdgeo_vector(lon, lat, alt, re, f):
  return cspyce1.drdgeo_vector(lon, lat, alt, re, f)

def drdlat(radius, lon, lat):
  return cspyce1.drdlat(radius, lon, lat)

def drdlat_vector(radius, lon, lat):
  return cspyce1.drdlat_vector(radius, lon, lat)

def drdpgr(body, lon, lat, alt, re, f):
  return cspyce1.drdpgr(body, lon, lat, alt, re, f)

def drdpgr_vector(body, lon, lat, alt, re, f):
  return cspyce1.drdpgr_vector(body, lon, lat, alt, re, f)

def drdsph(r, colat, lon):
  return cspyce1.drdsph(r, colat, lon)

def drdsph_vector(r, colat, lon):
  return cspyce1.drdsph_vector(r, colat, lon)

def dsphdr(x, y, z):
  return cspyce1.dsphdr(x, y, z)

def dsphdr_vector(x, y, z):
  return cspyce1.dsphdr_vector(x, y, z)

def dtpool(name):
  return cspyce1.dtpool(name)

def dtpool_error(name):
  return cspyce1.dtpool_error(name)

def ducrss(s1, s2):
  return cspyce1.ducrss(s1, s2)

def ducrss_vector(s1, s2):
  return cspyce1.ducrss_vector(s1, s2)

def dvcrss(s1, s2):
  return cspyce1.dvcrss(s1, s2)

def dvcrss_vector(s1, s2):
  return cspyce1.dvcrss_vector(s1, s2)

def dvdot(s1, s2):
  return cspyce1.dvdot(s1, s2)

def dvdot_vector(s1, s2):
  return cspyce1.dvdot_vector(s1, s2)

def dvhat(s1):
  return cspyce1.dvhat(s1)

def dvhat_vector(s1):
  return cspyce1.dvhat_vector(s1)

def dvnorm(state):
  return cspyce1.dvnorm(state)

def dvnorm_vector(state):
  return cspyce1.dvnorm_vector(state)

def dvpool(name):
  return cspyce1.dvpool(name)

def dvsep(s1, s2):
  return cspyce1.dvsep(s1, s2)

def dvsep_vector(s1, s2):
  return cspyce1.dvsep_vector(s1, s2)

def edlimb(a, b, c, viewpt):
  return cspyce1.edlimb(a, b, c, viewpt)

def edlimb_vector(a, b, c, viewpt):
  return cspyce1.edlimb_vector(a, b, c, viewpt)

def edterm(trmtyp, source, target, et, fixref, abcorr, obsrvr, npts):
  return cspyce1.edterm(trmtyp, source, target, et, fixref, abcorr, obsrvr, npts)

def el2cgv(ellipse):
  return cspyce1.el2cgv(ellipse)

def el2cgv_vector(ellipse):
  return cspyce1.el2cgv_vector(ellipse)

def eqncpv(et, epoch, eqel, rapol, decpol):
  return cspyce1.eqncpv(et, epoch, eqel, rapol, decpol)

def eqncpv_vector(et, epoch, eqel, rapol, decpol):
  return cspyce1.eqncpv_vector(et, epoch, eqel, rapol, decpol)

def erract(op, action):
  return cspyce1.erract(op, action)

def errch(marker, string):
  return cspyce1.errch(marker, string)

def errdev(op, device):
  return cspyce1.errdev(op, device)

def errdp(marker, number):
  return cspyce1.errdp(marker, number)

def errint(marker, number):
  return cspyce1.errint(marker, number)

def errprt(op, list):
  return cspyce1.errprt(op, list)

def et2lst(et, body, lon, type):
  return cspyce1.et2lst(et, body, lon, type)

def et2utc(et, format, prec):
  return cspyce1.et2utc(et, format, prec)

def etcal(et):
  return cspyce1.etcal(et)

def eul2m(angle3, angle2, angle1, axis3, axis2, axis1):
  return cspyce1.eul2m(angle3, angle2, angle1, axis3, axis2, axis1)

def eul2m_vector(angle3, angle2, angle1, axis3, axis2, axis1):
  return cspyce1.eul2m_vector(angle3, angle2, angle1, axis3, axis2, axis1)

def eul2xf(eulang, axisa, axisb, axisc):
  return cspyce1.eul2xf(eulang, axisa, axisb, axisc)

def eul2xf_vector(eulang, axisa, axisb, axisc):
  return cspyce1.eul2xf_vector(eulang, axisa, axisb, axisc)

def expool(name):
  return cspyce1.expool(name)

def failed():
  return cspyce1.failed()

def fovray(inst, raydir, rframe, abcorr, observer, et):
  return cspyce1.fovray(inst, raydir, rframe, abcorr, observer, et)

def fovray_vector(inst, raydir, rframe, abcorr, observer, et):
  return cspyce1.fovray_vector(inst, raydir, rframe, abcorr, observer, et)

def fovtrg(inst, target, tshape, tframe, abcorr, obsrvr, et):
  return cspyce1.fovtrg(inst, target, tshape, tframe, abcorr, obsrvr, et)

def fovtrg_vector(inst, target, tshape, tframe, abcorr, obsrvr, et):
  return cspyce1.fovtrg_vector(inst, target, tshape, tframe, abcorr, obsrvr, et)

def frame(xin):
  return cspyce1.frame(xin)

def frame_vector(xin):
  return cspyce1.frame_vector(xin)

def frinfo(frcode):
  return cspyce1.frinfo(frcode)

def frinfo_error(frcode):
  return cspyce1.frinfo_error(frcode)

def frmchg(frame1, frame2, et):
  return cspyce1.frmchg(frame1, frame2, et)

def frmchg_vector(frame1, frame2, et):
  return cspyce1.frmchg_vector(frame1, frame2, et)

def frmnam(frcode):
  return cspyce1.frmnam(frcode)

def frmnam_error(frcode):
  return cspyce1.frmnam_error(frcode)

def furnsh(file):
  return cspyce1.furnsh(file)

def gcpool(name, start):
  return cspyce1.gcpool(name, start)

def gcpool_error(name, start):
  return cspyce1.gcpool_error(name, start)

def gdpool(name, start):
  return cspyce1.gdpool(name, start)

def gdpool_error(name, start):
  return cspyce1.gdpool_error(name, start)

def georec(lon, lat, alt, re, f):
  return cspyce1.georec(lon, lat, alt, re, f)

def georec_vector(lon, lat, alt, re, f):
  return cspyce1.georec_vector(lon, lat, alt, re, f)

def getfov(instid):
  return cspyce1.getfov(instid)

def getmsg(option):
  return cspyce1.getmsg(option)

def gipool(name, start):
  return cspyce1.gipool(name, start)

def gipool_error(name, start):
  return cspyce1.gipool_error(name, start)

def gnpool(name, start):
  return cspyce1.gnpool(name, start)

def gnpool_error(name, start):
  return cspyce1.gnpool_error(name, start)

def halfpi():
  return cspyce1.halfpi()

def ident():
  return cspyce1.ident()

def illum(target, et, abcorr, obsrvr, spoint):
  return cspyce1.illum(target, et, abcorr, obsrvr, spoint)

def illum_vector(target, et, abcorr, obsrvr, spoint):
  return cspyce1.illum_vector(target, et, abcorr, obsrvr, spoint)

def illumf(method, target, ilusrc, et, fixref, abcorr, obsrvr, spoint):
  return cspyce1.illumf(method, target, ilusrc, et, fixref, abcorr, obsrvr, spoint)

def illumf_vector(method, target, ilusrc, et, fixref, abcorr, obsrvr, spoint):
  return cspyce1.illumf_vector(method, target, ilusrc, et, fixref, abcorr, obsrvr, spoint)

def illumg(method, target, ilusrc, et, fixref, abcorr, obsrvr, spoint):
  return cspyce1.illumg(method, target, ilusrc, et, fixref, abcorr, obsrvr, spoint)

def illumg_vector(method, target, ilusrc, et, fixref, abcorr, obsrvr, spoint):
  return cspyce1.illumg_vector(method, target, ilusrc, et, fixref, abcorr, obsrvr, spoint)

def ilumin(method, target, et, fixref, abcorr, obsrvr, spoint):
  return cspyce1.ilumin(method, target, et, fixref, abcorr, obsrvr, spoint)

def ilumin_vector(method, target, et, fixref, abcorr, obsrvr, spoint):
  return cspyce1.ilumin_vector(method, target, et, fixref, abcorr, obsrvr, spoint)

def inedpl(a, b, c, plane):
  return cspyce1.inedpl(a, b, c, plane)

def inedpl_vector(a, b, c, plane):
  return cspyce1.inedpl_vector(a, b, c, plane)

def inelpl(ellips, plane):
  return cspyce1.inelpl(ellips, plane)

def inelpl_vector(ellips, plane):
  return cspyce1.inelpl_vector(ellips, plane)

def inrypl(vertex, dir, plane):
  return cspyce1.inrypl(vertex, dir, plane)

def inrypl_vector(vertex, dir, plane):
  return cspyce1.inrypl_vector(vertex, dir, plane)

def intmax():
  return cspyce1.intmax()

def intmin():
  return cspyce1.intmin()

def invert(m1):
  return cspyce1.invert(m1)

def invert_error(m1):
  return cspyce1.invert_error(m1)

def invert_vector(m1):
  return cspyce1.invert_vector(m1)

def invert_vector_error(m1):
  return cspyce1.invert_vector_error(m1)

def invort(m):
  return cspyce1.invort(m)

def invort_vector(m):
  return cspyce1.invort_vector(m)

def isrot(m, ntol, dtol):
  return cspyce1.isrot(m, ntol, dtol)

def isrot_vector(m, ntol, dtol):
  return cspyce1.isrot_vector(m, ntol, dtol)

def j1900():
  return cspyce1.j1900()

def j1950():
  return cspyce1.j1950()

def j2000():
  return cspyce1.j2000()

def j2100():
  return cspyce1.j2100()

def jyear():
  return cspyce1.jyear()

def kplfrm(frmcls):
  return cspyce1.kplfrm(frmcls)

def latcyl(radius, lon, lat):
  return cspyce1.latcyl(radius, lon, lat)

def latcyl_vector(radius, lon, lat):
  return cspyce1.latcyl_vector(radius, lon, lat)

def latrec(radius, lon, lat):
  return cspyce1.latrec(radius, lon, lat)

def latrec_vector(radius, lon, lat):
  return cspyce1.latrec_vector(radius, lon, lat)

def latsph(radius, lon, lat):
  return cspyce1.latsph(radius, lon, lat)

def latsph_vector(radius, lon, lat):
  return cspyce1.latsph_vector(radius, lon, lat)

def latsrf(method, target, et, fixref, lonlat):
  return cspyce1.latsrf(method, target, et, fixref, lonlat)

def ldpool(filename):
  return cspyce1.ldpool(filename)

def limbpt(method, target, et, fixref, abcorr, corloc, obsrvr, refvec, rolstp, ncuts, schstp, soltol, maxn):
  return cspyce1.limbpt(method, target, et, fixref, abcorr, corloc, obsrvr, refvec, rolstp, ncuts, schstp, soltol, maxn)

def lspcn(body, et, abcorr):
  return cspyce1.lspcn(body, et, abcorr)

def lspcn_vector(body, et, abcorr):
  return cspyce1.lspcn_vector(body, et, abcorr)

def ltime(etobs, obs, dir, targ):
  return cspyce1.ltime(etobs, obs, dir, targ)

def ltime_vector(etobs, obs, dir, targ):
  return cspyce1.ltime_vector(etobs, obs, dir, targ)

def m2eul(r, axis3, axis2, axis1):
  return cspyce1.m2eul(r, axis3, axis2, axis1)

def m2eul_vector(r, axis3, axis2, axis1):
  return cspyce1.m2eul_vector(r, axis3, axis2, axis1)

def m2q(r):
  return cspyce1.m2q(r)

def m2q_vector(r):
  return cspyce1.m2q_vector(r)

def mequ(m1):
  return cspyce1.mequ(m1)

def mequ_vector(m1):
  return cspyce1.mequ_vector(m1)

def mequg(m1):
  return cspyce1.mequg(m1)

def mequg_vector(m1):
  return cspyce1.mequg_vector(m1)

def mtxm(m1, m2):
  return cspyce1.mtxm(m1, m2)

def mtxm_vector(m1, m2):
  return cspyce1.mtxm_vector(m1, m2)

def mtxmg(m1, m2):
  return cspyce1.mtxmg(m1, m2)

def mtxmg_vector(m1, m2):
  return cspyce1.mtxmg_vector(m1, m2)

def mtxv(m1, vin):
  return cspyce1.mtxv(m1, vin)

def mtxv_vector(m1, vin):
  return cspyce1.mtxv_vector(m1, vin)

def mtxvg(m1, v2):
  return cspyce1.mtxvg(m1, v2)

def mtxvg_vector(m1, v2):
  return cspyce1.mtxvg_vector(m1, v2)

def mxm(m1, m2):
  return cspyce1.mxm(m1, m2)

def mxm_vector(m1, m2):
  return cspyce1.mxm_vector(m1, m2)

def mxmg(m1, m2):
  return cspyce1.mxmg(m1, m2)

def mxmg_vector(m1, m2):
  return cspyce1.mxmg_vector(m1, m2)

def mxmt(m1, m2):
  return cspyce1.mxmt(m1, m2)

def mxmt_vector(m1, m2):
  return cspyce1.mxmt_vector(m1, m2)

def mxmtg(m1, m2):
  return cspyce1.mxmtg(m1, m2)

def mxmtg_vector(m1, m2):
  return cspyce1.mxmtg_vector(m1, m2)

def mxv(m1, vin):
  return cspyce1.mxv(m1, vin)

def mxv_vector(m1, vin):
  return cspyce1.mxv_vector(m1, vin)

def mxvg(m1, v2):
  return cspyce1.mxvg(m1, v2)

def mxvg_vector(m1, v2):
  return cspyce1.mxvg_vector(m1, v2)

def namfrm(frname):
  return cspyce1.namfrm(frname)

def namfrm_error(frname):
  return cspyce1.namfrm_error(frname)

def nearpt(positn, a, b, c):
  return cspyce1.nearpt(positn, a, b, c)

def nearpt_vector(positn, a, b, c):
  return cspyce1.nearpt_vector(positn, a, b, c)

def npedln(a, b, c, linept, linedr):
  return cspyce1.npedln(a, b, c, linept, linedr)

def npedln_vector(a, b, c, linept, linedr):
  return cspyce1.npedln_vector(a, b, c, linept, linedr)

def npelpt(point, ellips):
  return cspyce1.npelpt(point, ellips)

def npelpt_vector(point, ellips):
  return cspyce1.npelpt_vector(point, ellips)

def nplnpt(linpt, lindir, point):
  return cspyce1.nplnpt(linpt, lindir, point)

def nplnpt_vector(linpt, lindir, point):
  return cspyce1.nplnpt_vector(linpt, lindir, point)

def nvc2pl(normal, constant):
  return cspyce1.nvc2pl(normal, constant)

def nvc2pl_vector(normal, constant):
  return cspyce1.nvc2pl_vector(normal, constant)

def nvp2pl(normal, point):
  return cspyce1.nvp2pl(normal, point)

def nvp2pl_vector(normal, point):
  return cspyce1.nvp2pl_vector(normal, point)

def occult(targ1, shape1, frame1, targ2, shape2, frame2, abcorr, obsrvr, et):
  return cspyce1.occult(targ1, shape1, frame1, targ2, shape2, frame2, abcorr, obsrvr, et)

def occult_vector(targ1, shape1, frame1, targ2, shape2, frame2, abcorr, obsrvr, et):
  return cspyce1.occult_vector(targ1, shape1, frame1, targ2, shape2, frame2, abcorr, obsrvr, et)

def oscelt(state, et, gm):
  return cspyce1.oscelt(state, et, gm)

def oscelt_vector(state, et, gm):
  return cspyce1.oscelt_vector(state, et, gm)

def oscltx(state, et, gm):
  return cspyce1.oscltx(state, et, gm)

def oscltx_vector(state, et, gm):
  return cspyce1.oscltx_vector(state, et, gm)

def pckcov(pck, idcode):
  return cspyce1.pckcov(pck, idcode)

def pckcov_error(pck, idcode):
  return cspyce1.pckcov_error(pck, idcode)

def pckfrm(pck):
  return cspyce1.pckfrm(pck)

def pcpool(name, cvals):
  return cspyce1.pcpool(name, cvals)

def pdpool(name, dvals):
  return cspyce1.pdpool(name, dvals)

def pgrrec(body, lon, lat, alt, re, f):
  return cspyce1.pgrrec(body, lon, lat, alt, re, f)

def pgrrec_vector(body, lon, lat, alt, re, f):
  return cspyce1.pgrrec_vector(body, lon, lat, alt, re, f)

def phaseq(et, target, illmn, obsrvr, abcorr):
  return cspyce1.phaseq(et, target, illmn, obsrvr, abcorr)

def phaseq_vector(et, target, illmn, obsrvr, abcorr):
  return cspyce1.phaseq_vector(et, target, illmn, obsrvr, abcorr)

def pi():
  return cspyce1.pi()

def pipool(name, ivals):
  return cspyce1.pipool(name, ivals)

def pjelpl(elin, plane):
  return cspyce1.pjelpl(elin, plane)

def pjelpl_vector(elin, plane):
  return cspyce1.pjelpl_vector(elin, plane)

def pl2nvc(plane):
  return cspyce1.pl2nvc(plane)

def pl2nvc_vector(plane):
  return cspyce1.pl2nvc_vector(plane)

def pl2nvp(plane):
  return cspyce1.pl2nvp(plane)

def pl2nvp_vector(plane):
  return cspyce1.pl2nvp_vector(plane)

def pl2psv(plane):
  return cspyce1.pl2psv(plane)

def pl2psv_vector(plane):
  return cspyce1.pl2psv_vector(plane)

def pltar(vrtces, plates):
  return cspyce1.pltar(vrtces, plates)

def pltexp(iverts, delta):
  return cspyce1.pltexp(iverts, delta)

def pltexp_vector(iverts, delta):
  return cspyce1.pltexp_vector(iverts, delta)

def pltnp(point, v1, v2, v3):
  return cspyce1.pltnp(point, v1, v2, v3)

def pltnp_vector(point, v1, v2, v3):
  return cspyce1.pltnp_vector(point, v1, v2, v3)

def pltvol(vrtces, plates):
  return cspyce1.pltvol(vrtces, plates)

def prop2b(gm, pvinit, dt):
  return cspyce1.prop2b(gm, pvinit, dt)

def prop2b_vector(gm, pvinit, dt):
  return cspyce1.prop2b_vector(gm, pvinit, dt)

def psv2pl(point, span1, span2):
  return cspyce1.psv2pl(point, span1, span2)

def psv2pl_vector(point, span1, span2):
  return cspyce1.psv2pl_vector(point, span1, span2)

def pxform(fromfr, tofr, et):
  return cspyce1.pxform(fromfr, tofr, et)

def pxform_vector(fromfr, tofr, et):
  return cspyce1.pxform_vector(fromfr, tofr, et)

def pxfrm2(fromfr, tofr, etfrom, etto):
  return cspyce1.pxfrm2(fromfr, tofr, etfrom, etto)

def pxfrm2_vector(fromfr, tofr, etfrom, etto):
  return cspyce1.pxfrm2_vector(fromfr, tofr, etfrom, etto)

def q2m(q):
  return cspyce1.q2m(q)

def q2m_vector(q):
  return cspyce1.q2m_vector(q)

def qcktrc():
  return cspyce1.qcktrc()

def qdq2av(q, dq):
  return cspyce1.qdq2av(q, dq)

def qdq2av_vector(q, dq):
  return cspyce1.qdq2av_vector(q, dq)

def qxq(q1, q2):
  return cspyce1.qxq(q1, q2)

def qxq_vector(q1, q2):
  return cspyce1.qxq_vector(q1, q2)

def radrec(range, ra, dec):
  return cspyce1.radrec(range, ra, dec)

def radrec_vector(range, ra, dec):
  return cspyce1.radrec_vector(range, ra, dec)

def rav2xf(rot, av):
  return cspyce1.rav2xf(rot, av)

def rav2xf_vector(rot, av):
  return cspyce1.rav2xf_vector(rot, av)

def raxisa(matrix):
  return cspyce1.raxisa(matrix)

def raxisa_vector(matrix):
  return cspyce1.raxisa_vector(matrix)

def reccyl(rectan):
  return cspyce1.reccyl(rectan)

def reccyl_vector(rectan):
  return cspyce1.reccyl_vector(rectan)

def recgeo(rectan, re, f):
  return cspyce1.recgeo(rectan, re, f)

def recgeo_vector(rectan, re, f):
  return cspyce1.recgeo_vector(rectan, re, f)

def reclat(rectan):
  return cspyce1.reclat(rectan)

def reclat_vector(rectan):
  return cspyce1.reclat_vector(rectan)

def recpgr(body, rectan, re, f):
  return cspyce1.recpgr(body, rectan, re, f)

def recpgr_vector(body, rectan, re, f):
  return cspyce1.recpgr_vector(body, rectan, re, f)

def recrad(rectan):
  return cspyce1.recrad(rectan)

def recrad_vector(rectan):
  return cspyce1.recrad_vector(rectan)

def recsph(rectan):
  return cspyce1.recsph(rectan)

def recsph_vector(rectan):
  return cspyce1.recsph_vector(rectan)

def refchg(frame1, frame2, et):
  return cspyce1.refchg(frame1, frame2, et)

def refchg_vector(frame1, frame2, et):
  return cspyce1.refchg_vector(frame1, frame2, et)

def repmc(instr, marker, value):
  return cspyce1.repmc(instr, marker, value)

def repmct(instr, marker, value, repcase):
  return cspyce1.repmct(instr, marker, value, repcase)

def repmd(instr, marker, value, sigdig):
  return cspyce1.repmd(instr, marker, value, sigdig)

def repmf(instr, marker, value, sigdig, format):
  return cspyce1.repmf(instr, marker, value, sigdig, format)

def repmi(instr, marker, value):
  return cspyce1.repmi(instr, marker, value)

def repmot(instr, marker, value, repcase):
  return cspyce1.repmot(instr, marker, value, repcase)

def reset():
  return cspyce1.reset()

def rotate(angle, iaxis):
  return cspyce1.rotate(angle, iaxis)

def rotate_vector(angle, iaxis):
  return cspyce1.rotate_vector(angle, iaxis)

def rotmat(m1, angle, iaxis):
  return cspyce1.rotmat(m1, angle, iaxis)

def rotmat_vector(m1, angle, iaxis):
  return cspyce1.rotmat_vector(m1, angle, iaxis)

def rotvec(v1, angle, iaxis):
  return cspyce1.rotvec(v1, angle, iaxis)

def rotvec_vector(v1, angle, iaxis):
  return cspyce1.rotvec_vector(v1, angle, iaxis)

def rpd():
  return cspyce1.rpd()

def rquad(a, b, c):
  return cspyce1.rquad(a, b, c)

def rquad_vector(a, b, c):
  return cspyce1.rquad_vector(a, b, c)

def saelgv(vec1, vec2):
  return cspyce1.saelgv(vec1, vec2)

def saelgv_vector(vec1, vec2):
  return cspyce1.saelgv_vector(vec1, vec2)

def scdecd(sc, sclkdp):
  return cspyce1.scdecd(sc, sclkdp)

def sce2c(sc, et):
  return cspyce1.sce2c(sc, et)

def sce2c_vector(sc, et):
  return cspyce1.sce2c_vector(sc, et)

def sce2s(sc, et):
  return cspyce1.sce2s(sc, et)

def sce2t(sc, et):
  return cspyce1.sce2t(sc, et)

def sce2t_vector(sc, et):
  return cspyce1.sce2t_vector(sc, et)

def scencd(sc, sclkch):
  return cspyce1.scencd(sc, sclkch)

def scfmt(sc, ticks):
  return cspyce1.scfmt(sc, ticks)

def scpart(sc):
  return cspyce1.scpart(sc)

def scs2e(sc, sclkch):
  return cspyce1.scs2e(sc, sclkch)

def sct2e(sc, sclkdp):
  return cspyce1.sct2e(sc, sclkdp)

def sct2e_vector(sc, sclkdp):
  return cspyce1.sct2e_vector(sc, sclkdp)

def sctiks(sc, clkstr):
  return cspyce1.sctiks(sc, clkstr)

def setmsg(message):
  return cspyce1.setmsg(message)

def sigerr(message):
  return cspyce1.sigerr(message)

def sincpt(method, target, et, fixref, abcorr, obsrvr, dref, dvec):
  return cspyce1.sincpt(method, target, et, fixref, abcorr, obsrvr, dref, dvec)

def sincpt_vector(method, target, et, fixref, abcorr, obsrvr, dref, dvec):
  return cspyce1.sincpt_vector(method, target, et, fixref, abcorr, obsrvr, dref, dvec)

def spd():
  return cspyce1.spd()

def sphcyl(radius, colat, lon):
  return cspyce1.sphcyl(radius, colat, lon)

def sphcyl_vector(radius, colat, lon):
  return cspyce1.sphcyl_vector(radius, colat, lon)

def sphlat(radius, colat, lon):
  return cspyce1.sphlat(radius, colat, lon)

def sphlat_vector(radius, colat, lon):
  return cspyce1.sphlat_vector(radius, colat, lon)

def sphrec(radius, colat, lon):
  return cspyce1.sphrec(radius, colat, lon)

def sphrec_vector(radius, colat, lon):
  return cspyce1.sphrec_vector(radius, colat, lon)

def spkacs(targ, et, ref, abcorr, obs):
  return cspyce1.spkacs(targ, et, ref, abcorr, obs)

def spkacs_vector(targ, et, ref, abcorr, obs):
  return cspyce1.spkacs_vector(targ, et, ref, abcorr, obs)

def spkapo(targ, et, ref, sobs, abcorr):
  return cspyce1.spkapo(targ, et, ref, sobs, abcorr)

def spkapo_vector(targ, et, ref, sobs, abcorr):
  return cspyce1.spkapo_vector(targ, et, ref, sobs, abcorr)

def spkapp(targ, et, ref, sobs, abcorr):
  return cspyce1.spkapp(targ, et, ref, sobs, abcorr)

def spkapp_vector(targ, et, ref, sobs, abcorr):
  return cspyce1.spkapp_vector(targ, et, ref, sobs, abcorr)

def spkaps(targ, et, ref, abcorr, stobs, accobs):
  return cspyce1.spkaps(targ, et, ref, abcorr, stobs, accobs)

def spkaps_vector(targ, et, ref, abcorr, stobs, accobs):
  return cspyce1.spkaps_vector(targ, et, ref, abcorr, stobs, accobs)

def spkcov(spk, idcode):
  return cspyce1.spkcov(spk, idcode)

def spkcov_error(spk, idcode):
  return cspyce1.spkcov_error(spk, idcode)

def spkez(targ, et, ref, abcorr, obs):
  return cspyce1.spkez(targ, et, ref, abcorr, obs)

def spkez_vector(targ, et, ref, abcorr, obs):
  return cspyce1.spkez_vector(targ, et, ref, abcorr, obs)

def spkezp(targ, et, ref, abcorr, obs):
  return cspyce1.spkezp(targ, et, ref, abcorr, obs)

def spkezp_vector(targ, et, ref, abcorr, obs):
  return cspyce1.spkezp_vector(targ, et, ref, abcorr, obs)

def spkezr(target, et, ref, abcorr, obsrvr):
  return cspyce1.spkezr(target, et, ref, abcorr, obsrvr)

def spkezr_vector(target, et, ref, abcorr, obsrvr):
  return cspyce1.spkezr_vector(target, et, ref, abcorr, obsrvr)

def spkgeo(targ, et, ref, obs):
  return cspyce1.spkgeo(targ, et, ref, obs)

def spkgeo_vector(targ, et, ref, obs):
  return cspyce1.spkgeo_vector(targ, et, ref, obs)

def spkgps(targ, et, ref, obs):
  return cspyce1.spkgps(targ, et, ref, obs)

def spkgps_vector(targ, et, ref, obs):
  return cspyce1.spkgps_vector(targ, et, ref, obs)

def spkltc(targ, et, ref, abcorr, stobs):
  return cspyce1.spkltc(targ, et, ref, abcorr, stobs)

def spkltc_vector(targ, et, ref, abcorr, stobs):
  return cspyce1.spkltc_vector(targ, et, ref, abcorr, stobs)

def spkobj(spk):
  return cspyce1.spkobj(spk)

def spkpos(target, et, ref, abcorr, obsrvr):
  return cspyce1.spkpos(target, et, ref, abcorr, obsrvr)

def spkpos_vector(target, et, ref, abcorr, obsrvr):
  return cspyce1.spkpos_vector(target, et, ref, abcorr, obsrvr)

def spkssb(targ, et, ref):
  return cspyce1.spkssb(targ, et, ref)

def spkssb_vector(targ, et, ref):
  return cspyce1.spkssb_vector(targ, et, ref)

def srfc2s(code, bodyid):
  return cspyce1.srfc2s(code, bodyid)

def srfc2s_error(code, bodyid):
  return cspyce1.srfc2s_error(code, bodyid)

def srfcss(code, bodstr):
  return cspyce1.srfcss(code, bodstr)

def srfcss_error(code, bodstr):
  return cspyce1.srfcss_error(code, bodstr)

def srfnrm(method, target, et, fixref):
  return cspyce1.srfnrm(method, target, et, fixref)

def srfrec(body, lon, lat):
  return cspyce1.srfrec(body, lon, lat)

def srfrec_vector(body, lon, lat):
  return cspyce1.srfrec_vector(body, lon, lat)

def srfs2c(srfstr, bodstr):
  return cspyce1.srfs2c(srfstr, bodstr)

def srfs2c_error(srfstr, bodstr):
  return cspyce1.srfs2c_error(srfstr, bodstr)

def srfscc(srfstr, bodyid):
  return cspyce1.srfscc(srfstr, bodyid)

def srfscc_error(srfstr, bodyid):
  return cspyce1.srfscc_error(srfstr, bodyid)

def srfxpt(method, target, et, abcorr, obsrvr, dref, dvec):
  return cspyce1.srfxpt(method, target, et, abcorr, obsrvr, dref, dvec)

def srfxpt_vector(method, target, et, abcorr, obsrvr, dref, dvec):
  return cspyce1.srfxpt_vector(method, target, et, abcorr, obsrvr, dref, dvec)

def stcf01(catnam, westra, eastra, sthdec, nthdec):
  return cspyce1.stcf01(catnam, westra, eastra, sthdec, nthdec)

def stcg01(index):
  return cspyce1.stcg01(index)

def stcl01(catfnm):
  return cspyce1.stcl01(catfnm)

def stelab(pobj, vobs):
  return cspyce1.stelab(pobj, vobs)

def stelab_vector(pobj, vobs):
  return cspyce1.stelab_vector(pobj, vobs)

def stlabx(pobj, vobs):
  return cspyce1.stlabx(pobj, vobs)

def stlabx_vector(pobj, vobs):
  return cspyce1.stlabx_vector(pobj, vobs)

def stpool(item, nth, contin):
  return cspyce1.stpool(item, nth, contin)

def stpool_error(item, nth, contin):
  return cspyce1.stpool_error(item, nth, contin)

def str2et(str):
  return cspyce1.str2et(str)

def subpnt(method, target, et, fixref, abcorr, obsrvr):
  return cspyce1.subpnt(method, target, et, fixref, abcorr, obsrvr)

def subpnt_vector(method, target, et, fixref, abcorr, obsrvr):
  return cspyce1.subpnt_vector(method, target, et, fixref, abcorr, obsrvr)

def subpt(method, target, et, abcorr, obsrvr):
  return cspyce1.subpt(method, target, et, abcorr, obsrvr)

def subpt_vector(method, target, et, abcorr, obsrvr):
  return cspyce1.subpt_vector(method, target, et, abcorr, obsrvr)

def subslr(method, target, et, fixref, abcorr, obsrvr):
  return cspyce1.subslr(method, target, et, fixref, abcorr, obsrvr)

def subslr_vector(method, target, et, fixref, abcorr, obsrvr):
  return cspyce1.subslr_vector(method, target, et, fixref, abcorr, obsrvr)

def subsol(method, target, et, abcorr, obsrvr):
  return cspyce1.subsol(method, target, et, abcorr, obsrvr)

def subsol_vector(method, target, et, abcorr, obsrvr):
  return cspyce1.subsol_vector(method, target, et, abcorr, obsrvr)

def surfnm(a, b, c, point):
  return cspyce1.surfnm(a, b, c, point)

def surfpt(positn, u, a, b, c):
  return cspyce1.surfpt(positn, u, a, b, c)

def surfpt_vector(positn, u, a, b, c):
  return cspyce1.surfpt_vector(positn, u, a, b, c)

def surfpv(stvrtx, stdir, a, b, c):
  return cspyce1.surfpv(stvrtx, stdir, a, b, c)

def surfpv_vector(stvrtx, stdir, a, b, c):
  return cspyce1.surfpv_vector(stvrtx, stdir, a, b, c)

def sxform(fromfr, tofr, et):
  return cspyce1.sxform(fromfr, tofr, et)

def sxform_vector(fromfr, tofr, et):
  return cspyce1.sxform_vector(fromfr, tofr, et)

def termpt(method, ilusrc, target, et, fixref, abcorr, corloc, obsrvr, refvec, rolstp, ncuts, schstp, soltol, maxn):
  return cspyce1.termpt(method, ilusrc, target, et, fixref, abcorr, corloc, obsrvr, refvec, rolstp, ncuts, schstp, soltol, maxn)

def timdef(action, item, value):
  return cspyce1.timdef(action, item, value)

def timout(et, pictur):
  return cspyce1.timout(et, pictur)

def tipbod(ref, body, et):
  return cspyce1.tipbod(ref, body, et)

def tipbod_vector(ref, body, et):
  return cspyce1.tipbod_vector(ref, body, et)

def tisbod(ref, body, et):
  return cspyce1.tisbod(ref, body, et)

def tisbod_vector(ref, body, et):
  return cspyce1.tisbod_vector(ref, body, et)

def tkvrsn(item):
  return cspyce1.tkvrsn(item)

def tparse(string):
  return cspyce1.tparse(string)

def tparse_error(string):
  return cspyce1.tparse_error(string)

def tpictr(sample):
  return cspyce1.tpictr(sample)

def tpictr_error(sample):
  return cspyce1.tpictr_error(sample)

def trace(matrix):
  return cspyce1.trace(matrix)

def trace_vector(matrix):
  return cspyce1.trace_vector(matrix)

def trcdep():
  return cspyce1.trcdep()

def trcnam(index):
  return cspyce1.trcnam(index)

def trcoff():
  return cspyce1.trcoff()

def tsetyr(year):
  return cspyce1.tsetyr(year)

def twopi():
  return cspyce1.twopi()

def twovec(axdef, indexa, plndef, indexp):
  return cspyce1.twovec(axdef, indexa, plndef, indexp)

def twovec_vector(axdef, indexa, plndef, indexp):
  return cspyce1.twovec_vector(axdef, indexa, plndef, indexp)

def tyear():
  return cspyce1.tyear()

def ucrss(v1, v2):
  return cspyce1.ucrss(v1, v2)

def ucrss_vector(v1, v2):
  return cspyce1.ucrss_vector(v1, v2)

def unitim(epoch, insys, outsys):
  return cspyce1.unitim(epoch, insys, outsys)

def unitim_vector(epoch, insys, outsys):
  return cspyce1.unitim_vector(epoch, insys, outsys)

def unload(file):
  return cspyce1.unload(file)

def unorm(v1):
  return cspyce1.unorm(v1)

def unorm_vector(v1):
  return cspyce1.unorm_vector(v1)

def unormg(v1):
  return cspyce1.unormg(v1)

def unormg_vector(v1):
  return cspyce1.unormg_vector(v1)

def utc2et(utcstr):
  return cspyce1.utc2et(utcstr)

def vadd(v1, v2):
  return cspyce1.vadd(v1, v2)

def vadd_vector(v1, v2):
  return cspyce1.vadd_vector(v1, v2)

def vaddg(v1, v2):
  return cspyce1.vaddg(v1, v2)

def vaddg_vector(v1, v2):
  return cspyce1.vaddg_vector(v1, v2)

def vcrss(v1, v2):
  return cspyce1.vcrss(v1, v2)

def vcrss_vector(v1, v2):
  return cspyce1.vcrss_vector(v1, v2)

def vdist(v1, v2):
  return cspyce1.vdist(v1, v2)

def vdist_vector(v1, v2):
  return cspyce1.vdist_vector(v1, v2)

def vdistg(v1, v2):
  return cspyce1.vdistg(v1, v2)

def vdistg_vector(v1, v2):
  return cspyce1.vdistg_vector(v1, v2)

def vdot(v1, v2):
  return cspyce1.vdot(v1, v2)

def vdot_vector(v1, v2):
  return cspyce1.vdot_vector(v1, v2)

def vdotg(v1, v2):
  return cspyce1.vdotg(v1, v2)

def vdotg_vector(v1, v2):
  return cspyce1.vdotg_vector(v1, v2)

def vequ(vin):
  return cspyce1.vequ(vin)

def vequ_vector(vin):
  return cspyce1.vequ_vector(vin)

def vequg(vin):
  return cspyce1.vequg(vin)

def vequg_vector(vin):
  return cspyce1.vequg_vector(vin)

def vhat(v1):
  return cspyce1.vhat(v1)

def vhat_vector(v1):
  return cspyce1.vhat_vector(v1)

def vhatg(v1):
  return cspyce1.vhatg(v1)

def vhatg_vector(v1):
  return cspyce1.vhatg_vector(v1)

def vlcom(a, v1, b, v2):
  return cspyce1.vlcom(a, v1, b, v2)

def vlcom3(a, v1, b, v2, c, v3):
  return cspyce1.vlcom3(a, v1, b, v2, c, v3)

def vlcom3_vector(a, v1, b, v2, c, v3):
  return cspyce1.vlcom3_vector(a, v1, b, v2, c, v3)

def vlcom_vector(a, v1, b, v2):
  return cspyce1.vlcom_vector(a, v1, b, v2)

def vlcomg(a, v1, b, v2):
  return cspyce1.vlcomg(a, v1, b, v2)

def vlcomg_vector(a, v1, b, v2):
  return cspyce1.vlcomg_vector(a, v1, b, v2)

def vminug(vin):
  return cspyce1.vminug(vin)

def vminug_vector(vin):
  return cspyce1.vminug_vector(vin)

def vminus(v1):
  return cspyce1.vminus(v1)

def vminus_vector(v1):
  return cspyce1.vminus_vector(v1)

def vnorm(v1):
  return cspyce1.vnorm(v1)

def vnorm_vector(v1):
  return cspyce1.vnorm_vector(v1)

def vnormg(v1):
  return cspyce1.vnormg(v1)

def vnormg_vector(v1):
  return cspyce1.vnormg_vector(v1)

def vpack(x, y, z):
  return cspyce1.vpack(x, y, z)

def vpack_vector(x, y, z):
  return cspyce1.vpack_vector(x, y, z)

def vperp(v1, v2):
  return cspyce1.vperp(v1, v2)

def vperp_vector(v1, v2):
  return cspyce1.vperp_vector(v1, v2)

def vprjp(vin, plane):
  return cspyce1.vprjp(vin, plane)

def vprjp_vector(vin, plane):
  return cspyce1.vprjp_vector(vin, plane)

def vprjpi(vin, projpl, invpl):
  return cspyce1.vprjpi(vin, projpl, invpl)

def vprjpi_vector(vin, projpl, invpl):
  return cspyce1.vprjpi_vector(vin, projpl, invpl)

def vproj(v1, v2):
  return cspyce1.vproj(v1, v2)

def vproj_vector(v1, v2):
  return cspyce1.vproj_vector(v1, v2)

def vrel(v1, v2):
  return cspyce1.vrel(v1, v2)

def vrel_vector(v1, v2):
  return cspyce1.vrel_vector(v1, v2)

def vrelg(v1, v2):
  return cspyce1.vrelg(v1, v2)

def vrelg_vector(v1, v2):
  return cspyce1.vrelg_vector(v1, v2)

def vrotv(v, axis, theta):
  return cspyce1.vrotv(v, axis, theta)

def vrotv_vector(v, axis, theta):
  return cspyce1.vrotv_vector(v, axis, theta)

def vscl(s, v1):
  return cspyce1.vscl(s, v1)

def vscl_vector(s, v1):
  return cspyce1.vscl_vector(s, v1)

def vsclg(s, v1):
  return cspyce1.vsclg(s, v1)

def vsclg_vector(s, v1):
  return cspyce1.vsclg_vector(s, v1)

def vsep(v1, v2):
  return cspyce1.vsep(v1, v2)

def vsep_vector(v1, v2):
  return cspyce1.vsep_vector(v1, v2)

def vsepg(v1, v2):
  return cspyce1.vsepg(v1, v2)

def vsepg_vector(v1, v2):
  return cspyce1.vsepg_vector(v1, v2)

def vsub(v1, v2):
  return cspyce1.vsub(v1, v2)

def vsub_vector(v1, v2):
  return cspyce1.vsub_vector(v1, v2)

def vsubg(v1, v2):
  return cspyce1.vsubg(v1, v2)

def vsubg_vector(v1, v2):
  return cspyce1.vsubg_vector(v1, v2)

def vtmv(v1, matrix, v2):
  return cspyce1.vtmv(v1, matrix, v2)

def vtmv_vector(v1, matrix, v2):
  return cspyce1.vtmv_vector(v1, matrix, v2)

def vtmvg(v1, matrix, v2):
  return cspyce1.vtmvg(v1, matrix, v2)

def vtmvg_vector(v1, matrix, v2):
  return cspyce1.vtmvg_vector(v1, matrix, v2)

def vupack(v):
  return cspyce1.vupack(v)

def vupack_vector(v):
  return cspyce1.vupack_vector(v)

def vzero(v):
  return cspyce1.vzero(v)

def vzero_vector(v):
  return cspyce1.vzero_vector(v)

def vzerog(v):
  return cspyce1.vzerog(v)

def vzerog_vector(v):
  return cspyce1.vzerog_vector(v)

def xf2eul(xform, axisa, axisb, axisc):
  return cspyce1.xf2eul(xform, axisa, axisb, axisc)

def xf2eul_vector(xform, axisa, axisb, axisc):
  return cspyce1.xf2eul_vector(xform, axisa, axisb, axisc)

def xf2rav(xform):
  return cspyce1.xf2rav(xform)

def xf2rav_vector(xform):
  return cspyce1.xf2rav_vector(xform)

def xfmsta(instate, insys, outsys, body):
  return cspyce1.xfmsta(instate, insys, outsys, body)

def xfmsta_vector(instate, insys, outsys, body):
  return cspyce1.xfmsta_vector(instate, insys, outsys, body)

def xpose(m1):
  return cspyce1.xpose(m1)

def xpose6(m1):
  return cspyce1.xpose6(m1)

def xpose6_vector(m1):
  return cspyce1.xpose6_vector(m1)

def xpose_vector(m1):
  return cspyce1.xpose_vector(m1)

def xposeg(matrix):
  return cspyce1.xposeg(matrix)

def xposeg_vector(matrix):
  return cspyce1.xposeg_vector(matrix)

# Upon execution, re-connect all the lost attibutes and broken links...

relink_all(globals(), cspyce1.__dict__)

################################################################################
