################################################################################
# spyce/spyce2.py
################################################################################
# module spyce.spyce2
#
# This module re-declares every spyce1 function explicitly, with its list of
# argument names as used by CSPICE. The practical effect is that functions in
# spyce2 module can be called in a fully Python-like way, the rightmost inputs
# in any order and identified by their names.
#
# NOTE: This file is generated automatically using program make_spyce2.py:
#   python make_spyce2.py > spyce2.py
#
################################################################################

# This function makes spyce2 look the same as spyce1. It ensures that every
# location in the global dictionary and every function's internal link point
# a new function of the same name.

def relink_all(new_dict, old_dict):

    # Assign a new function to the dictionary at the same location as every
    # spyce function found in the old dictionary

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

    # Make sure each spyce function has the same properties and attributes as
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


import spyce.spyce1 as spyce1
from spyce.spyce1 import *

def axisar(axis, angle):
  return spyce1.axisar(axis, angle)

def axisar_vector(axis, angle):
  return spyce1.axisar_vector(axis, angle)

def b1900():
  return spyce1.b1900()

def b1950():
  return spyce1.b1950()

def bltfrm(frmcls):
  return spyce1.bltfrm(frmcls)

def bodc2n(code):
  return spyce1.bodc2n(code)

def bodc2n_error(code):
  return spyce1.bodc2n_error(code)

def bodc2s(code):
  return spyce1.bodc2s(code)

def boddef(name, code):
  return spyce1.boddef(name, code)

def bodfnd(body, item):
  return spyce1.bodfnd(body, item)

def bodn2c(name):
  return spyce1.bodn2c(name)

def bodn2c_error(name):
  return spyce1.bodn2c_error(name)

def bods2c(name):
  return spyce1.bods2c(name)

def bods2c_error(name):
  return spyce1.bods2c_error(name)

def bodvar(bodyid, item):
  return spyce1.bodvar(bodyid, item)

def bodvcd(bodyid, item):
  return spyce1.bodvcd(bodyid, item)

def bodvrd(bodynm, item):
  return spyce1.bodvrd(bodynm, item)

def ccifrm(frclss, clssid):
  return spyce1.ccifrm(frclss, clssid)

def ccifrm_error(frclss, clssid):
  return spyce1.ccifrm_error(frclss, clssid)

def cgv2el(center, vec1, vec2):
  return spyce1.cgv2el(center, vec1, vec2)

def cgv2el_vector(center, vec1, vec2):
  return spyce1.cgv2el_vector(center, vec1, vec2)

def chkin(module):
  return spyce1.chkin(module)

def chkout(module):
  return spyce1.chkout(module)

def cidfrm(cent):
  return spyce1.cidfrm(cent)

def cidfrm_error(cent):
  return spyce1.cidfrm_error(cent)

def ckcov(ck, idcode, needav, level, tol, timsys):
  return spyce1.ckcov(ck, idcode, needav, level, tol, timsys)

def ckcov_error(ck, idcode, needav, level, tol, timsys):
  return spyce1.ckcov_error(ck, idcode, needav, level, tol, timsys)

def ckgp(inst, sclkdp, tol, ref):
  return spyce1.ckgp(inst, sclkdp, tol, ref)

def ckgp_error(inst, sclkdp, tol, ref):
  return spyce1.ckgp_error(inst, sclkdp, tol, ref)

def ckgp_vector(inst, sclkdp, tol, ref):
  return spyce1.ckgp_vector(inst, sclkdp, tol, ref)

def ckgp_vector_error(inst, sclkdp, tol, ref):
  return spyce1.ckgp_vector_error(inst, sclkdp, tol, ref)

def ckgpav(inst, sclkdp, tol, ref):
  return spyce1.ckgpav(inst, sclkdp, tol, ref)

def ckgpav_error(inst, sclkdp, tol, ref):
  return spyce1.ckgpav_error(inst, sclkdp, tol, ref)

def ckgpav_vector(inst, sclkdp, tol, ref):
  return spyce1.ckgpav_vector(inst, sclkdp, tol, ref)

def ckgpav_vector_error(inst, sclkdp, tol, ref):
  return spyce1.ckgpav_vector_error(inst, sclkdp, tol, ref)

def ckobj(ck):
  return spyce1.ckobj(ck)

def clight():
  return spyce1.clight()

def clpool():
  return spyce1.clpool()

def cnmfrm(cname):
  return spyce1.cnmfrm(cname)

def cnmfrm_error(cname):
  return spyce1.cnmfrm_error(cname)

def conics(elts, et):
  return spyce1.conics(elts, et)

def conics_vector(elts, et):
  return spyce1.conics_vector(elts, et)

def convrt(x, in1, out):
  return spyce1.convrt(x, in1, out)

def convrt_vector(x, in1, out):
  return spyce1.convrt_vector(x, in1, out)

def cyllat(r, lonc, z):
  return spyce1.cyllat(r, lonc, z)

def cyllat_vector(r, lonc, z):
  return spyce1.cyllat_vector(r, lonc, z)

def cylrec(r, lon, z):
  return spyce1.cylrec(r, lon, z)

def cylrec_vector(r, lon, z):
  return spyce1.cylrec_vector(r, lon, z)

def cylsph(r, lonc, z):
  return spyce1.cylsph(r, lonc, z)

def cylsph_vector(r, lonc, z):
  return spyce1.cylsph_vector(r, lonc, z)

def dafbfs(handle):
  return spyce1.dafbfs(handle)

def dafcls(handle):
  return spyce1.dafcls(handle)

def daffna():
  return spyce1.daffna()

def dafgda(handle, begin, end):
  return spyce1.dafgda(handle, begin, end)

def dafgn(lenout):
  return spyce1.dafgn(lenout)

def dafgs():
  return spyce1.dafgs()

def dafopr(fname):
  return spyce1.dafopr(fname)

def dafus(sum, nd, ni):
  return spyce1.dafus(sum, nd, ni)

def dcyldr(x, y, z):
  return spyce1.dcyldr(x, y, z)

def dcyldr_vector(x, y, z):
  return spyce1.dcyldr_vector(x, y, z)

def deltet(epoch, eptype):
  return spyce1.deltet(epoch, eptype)

def deltet_vector(epoch, eptype):
  return spyce1.deltet_vector(epoch, eptype)

def det(m1):
  return spyce1.det(m1)

def det_vector(m1):
  return spyce1.det_vector(m1)

def dgeodr(x, y, z, re, f):
  return spyce1.dgeodr(x, y, z, re, f)

def dgeodr_vector(x, y, z, re, f):
  return spyce1.dgeodr_vector(x, y, z, re, f)

def diags2(symmat):
  return spyce1.diags2(symmat)

def diags2_vector(symmat):
  return spyce1.diags2_vector(symmat)

def dlatdr(x, y, z):
  return spyce1.dlatdr(x, y, z)

def dlatdr_vector(x, y, z):
  return spyce1.dlatdr_vector(x, y, z)

def dpgrdr(body, x, y, z, re, f):
  return spyce1.dpgrdr(body, x, y, z, re, f)

def dpgrdr_vector(body, x, y, z, re, f):
  return spyce1.dpgrdr_vector(body, x, y, z, re, f)

def dpmax():
  return spyce1.dpmax()

def dpmin():
  return spyce1.dpmin()

def dpr():
  return spyce1.dpr()

def drdcyl(r, lon, z):
  return spyce1.drdcyl(r, lon, z)

def drdcyl_vector(r, lon, z):
  return spyce1.drdcyl_vector(r, lon, z)

def drdgeo(lon, lat, alt, re, f):
  return spyce1.drdgeo(lon, lat, alt, re, f)

def drdgeo_vector(lon, lat, alt, re, f):
  return spyce1.drdgeo_vector(lon, lat, alt, re, f)

def drdlat(radius, lon, lat):
  return spyce1.drdlat(radius, lon, lat)

def drdlat_vector(radius, lon, lat):
  return spyce1.drdlat_vector(radius, lon, lat)

def drdpgr(body, lon, lat, alt, re, f):
  return spyce1.drdpgr(body, lon, lat, alt, re, f)

def drdpgr_vector(body, lon, lat, alt, re, f):
  return spyce1.drdpgr_vector(body, lon, lat, alt, re, f)

def drdsph(r, colat, lon):
  return spyce1.drdsph(r, colat, lon)

def drdsph_vector(r, colat, lon):
  return spyce1.drdsph_vector(r, colat, lon)

def dsphdr(x, y, z):
  return spyce1.dsphdr(x, y, z)

def dsphdr_vector(x, y, z):
  return spyce1.dsphdr_vector(x, y, z)

def dtpool(name):
  return spyce1.dtpool(name)

def dtpool_error(name):
  return spyce1.dtpool_error(name)

def ducrss(s1, s2):
  return spyce1.ducrss(s1, s2)

def ducrss_vector(s1, s2):
  return spyce1.ducrss_vector(s1, s2)

def dvcrss(s1, s2):
  return spyce1.dvcrss(s1, s2)

def dvcrss_vector(s1, s2):
  return spyce1.dvcrss_vector(s1, s2)

def dvdot(s1, s2):
  return spyce1.dvdot(s1, s2)

def dvdot_vector(s1, s2):
  return spyce1.dvdot_vector(s1, s2)

def dvhat(s1):
  return spyce1.dvhat(s1)

def dvhat_vector(s1):
  return spyce1.dvhat_vector(s1)

def dvnorm(state):
  return spyce1.dvnorm(state)

def dvnorm_vector(state):
  return spyce1.dvnorm_vector(state)

def dvpool(name):
  return spyce1.dvpool(name)

def dvsep(s1, s2):
  return spyce1.dvsep(s1, s2)

def dvsep_vector(s1, s2):
  return spyce1.dvsep_vector(s1, s2)

def edlimb(a, b, c, viewpt):
  return spyce1.edlimb(a, b, c, viewpt)

def edlimb_vector(a, b, c, viewpt):
  return spyce1.edlimb_vector(a, b, c, viewpt)

def edterm(trmtyp, source, target, et, fixref, abcorr, obsrvr, npts):
  return spyce1.edterm(trmtyp, source, target, et, fixref, abcorr, obsrvr, npts)

def el2cgv(ellipse):
  return spyce1.el2cgv(ellipse)

def el2cgv_vector(ellipse):
  return spyce1.el2cgv_vector(ellipse)

def eqncpv(et, epoch, eqel, rapol, decpol):
  return spyce1.eqncpv(et, epoch, eqel, rapol, decpol)

def eqncpv_vector(et, epoch, eqel, rapol, decpol):
  return spyce1.eqncpv_vector(et, epoch, eqel, rapol, decpol)

def erract(op, action):
  return spyce1.erract(op, action)

def errch(marker, string):
  return spyce1.errch(marker, string)

def errdev(op, device):
  return spyce1.errdev(op, device)

def errdp(marker, number):
  return spyce1.errdp(marker, number)

def errint(marker, number):
  return spyce1.errint(marker, number)

def errprt(op, list):
  return spyce1.errprt(op, list)

def et2lst(et, body, lon, type):
  return spyce1.et2lst(et, body, lon, type)

def et2utc(et, format, prec):
  return spyce1.et2utc(et, format, prec)

def etcal(et):
  return spyce1.etcal(et)

def eul2m(angle3, angle2, angle1, axis3, axis2, axis1):
  return spyce1.eul2m(angle3, angle2, angle1, axis3, axis2, axis1)

def eul2m_vector(angle3, angle2, angle1, axis3, axis2, axis1):
  return spyce1.eul2m_vector(angle3, angle2, angle1, axis3, axis2, axis1)

def eul2xf(eulang, axisa, axisb, axisc):
  return spyce1.eul2xf(eulang, axisa, axisb, axisc)

def eul2xf_vector(eulang, axisa, axisb, axisc):
  return spyce1.eul2xf_vector(eulang, axisa, axisb, axisc)

def expool(name):
  return spyce1.expool(name)

def failed():
  return spyce1.failed()

def fovray(inst, raydir, rframe, abcorr, observer, et):
  return spyce1.fovray(inst, raydir, rframe, abcorr, observer, et)

def fovray_vector(inst, raydir, rframe, abcorr, observer, et):
  return spyce1.fovray_vector(inst, raydir, rframe, abcorr, observer, et)

def fovtrg(inst, target, tshape, tframe, abcorr, obsrvr, et):
  return spyce1.fovtrg(inst, target, tshape, tframe, abcorr, obsrvr, et)

def fovtrg_vector(inst, target, tshape, tframe, abcorr, obsrvr, et):
  return spyce1.fovtrg_vector(inst, target, tshape, tframe, abcorr, obsrvr, et)

def frame(xin):
  return spyce1.frame(xin)

def frame_vector(xin):
  return spyce1.frame_vector(xin)

def frinfo(frcode):
  return spyce1.frinfo(frcode)

def frinfo_error(frcode):
  return spyce1.frinfo_error(frcode)

def frmchg(frame1, frame2, et):
  return spyce1.frmchg(frame1, frame2, et)

def frmchg_vector(frame1, frame2, et):
  return spyce1.frmchg_vector(frame1, frame2, et)

def frmnam(frcode):
  return spyce1.frmnam(frcode)

def frmnam_error(frcode):
  return spyce1.frmnam_error(frcode)

def furnsh(file):
  return spyce1.furnsh(file)

def gcpool(name, start):
  return spyce1.gcpool(name, start)

def gcpool_error(name, start):
  return spyce1.gcpool_error(name, start)

def gdpool(name, start):
  return spyce1.gdpool(name, start)

def gdpool_error(name, start):
  return spyce1.gdpool_error(name, start)

def georec(lon, lat, alt, re, f):
  return spyce1.georec(lon, lat, alt, re, f)

def georec_vector(lon, lat, alt, re, f):
  return spyce1.georec_vector(lon, lat, alt, re, f)

def getfov(instid):
  return spyce1.getfov(instid)

def getmsg(option):
  return spyce1.getmsg(option)

def gipool(name, start):
  return spyce1.gipool(name, start)

def gipool_error(name, start):
  return spyce1.gipool_error(name, start)

def gnpool(name, start):
  return spyce1.gnpool(name, start)

def gnpool_error(name, start):
  return spyce1.gnpool_error(name, start)

def halfpi():
  return spyce1.halfpi()

def ident():
  return spyce1.ident()

def illum(target, et, abcorr, obsrvr, spoint):
  return spyce1.illum(target, et, abcorr, obsrvr, spoint)

def illum_vector(target, et, abcorr, obsrvr, spoint):
  return spyce1.illum_vector(target, et, abcorr, obsrvr, spoint)

def illumf(method, target, ilusrc, et, fixref, abcorr, obsrvr, spoint):
  return spyce1.illumf(method, target, ilusrc, et, fixref, abcorr, obsrvr, spoint)

def illumf_vector(method, target, ilusrc, et, fixref, abcorr, obsrvr, spoint):
  return spyce1.illumf_vector(method, target, ilusrc, et, fixref, abcorr, obsrvr, spoint)

def illumg(method, target, ilusrc, et, fixref, abcorr, obsrvr, spoint):
  return spyce1.illumg(method, target, ilusrc, et, fixref, abcorr, obsrvr, spoint)

def illumg_vector(method, target, ilusrc, et, fixref, abcorr, obsrvr, spoint):
  return spyce1.illumg_vector(method, target, ilusrc, et, fixref, abcorr, obsrvr, spoint)

def ilumin(method, target, et, fixref, abcorr, obsrvr, spoint):
  return spyce1.ilumin(method, target, et, fixref, abcorr, obsrvr, spoint)

def ilumin_vector(method, target, et, fixref, abcorr, obsrvr, spoint):
  return spyce1.ilumin_vector(method, target, et, fixref, abcorr, obsrvr, spoint)

def inedpl(a, b, c, plane):
  return spyce1.inedpl(a, b, c, plane)

def inedpl_vector(a, b, c, plane):
  return spyce1.inedpl_vector(a, b, c, plane)

def inelpl(ellips, plane):
  return spyce1.inelpl(ellips, plane)

def inelpl_vector(ellips, plane):
  return spyce1.inelpl_vector(ellips, plane)

def inrypl(vertex, dir, plane):
  return spyce1.inrypl(vertex, dir, plane)

def inrypl_vector(vertex, dir, plane):
  return spyce1.inrypl_vector(vertex, dir, plane)

def intmax():
  return spyce1.intmax()

def intmin():
  return spyce1.intmin()

def invert(m1):
  return spyce1.invert(m1)

def invert_error(m1):
  return spyce1.invert_error(m1)

def invert_vector(m1):
  return spyce1.invert_vector(m1)

def invert_vector_error(m1):
  return spyce1.invert_vector_error(m1)

def invort(m):
  return spyce1.invort(m)

def invort_vector(m):
  return spyce1.invort_vector(m)

def isrot(m, ntol, dtol):
  return spyce1.isrot(m, ntol, dtol)

def isrot_vector(m, ntol, dtol):
  return spyce1.isrot_vector(m, ntol, dtol)

def j1900():
  return spyce1.j1900()

def j1950():
  return spyce1.j1950()

def j2000():
  return spyce1.j2000()

def j2100():
  return spyce1.j2100()

def jyear():
  return spyce1.jyear()

def kplfrm(frmcls):
  return spyce1.kplfrm(frmcls)

def latcyl(radius, lon, lat):
  return spyce1.latcyl(radius, lon, lat)

def latcyl_vector(radius, lon, lat):
  return spyce1.latcyl_vector(radius, lon, lat)

def latrec(radius, lon, lat):
  return spyce1.latrec(radius, lon, lat)

def latrec_vector(radius, lon, lat):
  return spyce1.latrec_vector(radius, lon, lat)

def latsph(radius, lon, lat):
  return spyce1.latsph(radius, lon, lat)

def latsph_vector(radius, lon, lat):
  return spyce1.latsph_vector(radius, lon, lat)

def latsrf(method, target, et, fixref, lonlat):
  return spyce1.latsrf(method, target, et, fixref, lonlat)

def ldpool(filename):
  return spyce1.ldpool(filename)

def limbpt(method, target, et, fixref, abcorr, corloc, obsrvr, refvec, rolstp, ncuts, schstp, soltol, maxn):
  return spyce1.limbpt(method, target, et, fixref, abcorr, corloc, obsrvr, refvec, rolstp, ncuts, schstp, soltol, maxn)

def lspcn(body, et, abcorr):
  return spyce1.lspcn(body, et, abcorr)

def lspcn_vector(body, et, abcorr):
  return spyce1.lspcn_vector(body, et, abcorr)

def ltime(etobs, obs, dir, targ):
  return spyce1.ltime(etobs, obs, dir, targ)

def ltime_vector(etobs, obs, dir, targ):
  return spyce1.ltime_vector(etobs, obs, dir, targ)

def m2eul(r, axis3, axis2, axis1):
  return spyce1.m2eul(r, axis3, axis2, axis1)

def m2eul_vector(r, axis3, axis2, axis1):
  return spyce1.m2eul_vector(r, axis3, axis2, axis1)

def m2q(r):
  return spyce1.m2q(r)

def m2q_vector(r):
  return spyce1.m2q_vector(r)

def mequ(m1):
  return spyce1.mequ(m1)

def mequ_vector(m1):
  return spyce1.mequ_vector(m1)

def mequg(m1):
  return spyce1.mequg(m1)

def mequg_vector(m1):
  return spyce1.mequg_vector(m1)

def mtxm(m1, m2):
  return spyce1.mtxm(m1, m2)

def mtxm_vector(m1, m2):
  return spyce1.mtxm_vector(m1, m2)

def mtxmg(m1, m2):
  return spyce1.mtxmg(m1, m2)

def mtxmg_vector(m1, m2):
  return spyce1.mtxmg_vector(m1, m2)

def mtxv(m1, vin):
  return spyce1.mtxv(m1, vin)

def mtxv_vector(m1, vin):
  return spyce1.mtxv_vector(m1, vin)

def mtxvg(m1, v2):
  return spyce1.mtxvg(m1, v2)

def mtxvg_vector(m1, v2):
  return spyce1.mtxvg_vector(m1, v2)

def mxm(m1, m2):
  return spyce1.mxm(m1, m2)

def mxm_vector(m1, m2):
  return spyce1.mxm_vector(m1, m2)

def mxmg(m1, m2):
  return spyce1.mxmg(m1, m2)

def mxmg_vector(m1, m2):
  return spyce1.mxmg_vector(m1, m2)

def mxmt(m1, m2):
  return spyce1.mxmt(m1, m2)

def mxmt_vector(m1, m2):
  return spyce1.mxmt_vector(m1, m2)

def mxmtg(m1, m2):
  return spyce1.mxmtg(m1, m2)

def mxmtg_vector(m1, m2):
  return spyce1.mxmtg_vector(m1, m2)

def mxv(m1, vin):
  return spyce1.mxv(m1, vin)

def mxv_vector(m1, vin):
  return spyce1.mxv_vector(m1, vin)

def mxvg(m1, v2):
  return spyce1.mxvg(m1, v2)

def mxvg_vector(m1, v2):
  return spyce1.mxvg_vector(m1, v2)

def namfrm(frname):
  return spyce1.namfrm(frname)

def namfrm_error(frname):
  return spyce1.namfrm_error(frname)

def nearpt(positn, a, b, c):
  return spyce1.nearpt(positn, a, b, c)

def nearpt_vector(positn, a, b, c):
  return spyce1.nearpt_vector(positn, a, b, c)

def npedln(a, b, c, linept, linedr):
  return spyce1.npedln(a, b, c, linept, linedr)

def npedln_vector(a, b, c, linept, linedr):
  return spyce1.npedln_vector(a, b, c, linept, linedr)

def npelpt(point, ellips):
  return spyce1.npelpt(point, ellips)

def npelpt_vector(point, ellips):
  return spyce1.npelpt_vector(point, ellips)

def nplnpt(linpt, lindir, point):
  return spyce1.nplnpt(linpt, lindir, point)

def nplnpt_vector(linpt, lindir, point):
  return spyce1.nplnpt_vector(linpt, lindir, point)

def nvc2pl(normal, constant):
  return spyce1.nvc2pl(normal, constant)

def nvc2pl_vector(normal, constant):
  return spyce1.nvc2pl_vector(normal, constant)

def nvp2pl(normal, point):
  return spyce1.nvp2pl(normal, point)

def nvp2pl_vector(normal, point):
  return spyce1.nvp2pl_vector(normal, point)

def occult(targ1, shape1, frame1, targ2, shape2, frame2, abcorr, obsrvr, et):
  return spyce1.occult(targ1, shape1, frame1, targ2, shape2, frame2, abcorr, obsrvr, et)

def occult_vector(targ1, shape1, frame1, targ2, shape2, frame2, abcorr, obsrvr, et):
  return spyce1.occult_vector(targ1, shape1, frame1, targ2, shape2, frame2, abcorr, obsrvr, et)

def oscelt(state, et, gm):
  return spyce1.oscelt(state, et, gm)

def oscelt_vector(state, et, gm):
  return spyce1.oscelt_vector(state, et, gm)

def oscltx(state, et, gm):
  return spyce1.oscltx(state, et, gm)

def oscltx_vector(state, et, gm):
  return spyce1.oscltx_vector(state, et, gm)

def pckcov(pck, idcode):
  return spyce1.pckcov(pck, idcode)

def pckcov_error(pck, idcode):
  return spyce1.pckcov_error(pck, idcode)

def pckfrm(pck):
  return spyce1.pckfrm(pck)

def pcpool(name, cvals):
  return spyce1.pcpool(name, cvals)

def pdpool(name, dvals):
  return spyce1.pdpool(name, dvals)

def pgrrec(body, lon, lat, alt, re, f):
  return spyce1.pgrrec(body, lon, lat, alt, re, f)

def pgrrec_vector(body, lon, lat, alt, re, f):
  return spyce1.pgrrec_vector(body, lon, lat, alt, re, f)

def phaseq(et, target, illmn, obsrvr, abcorr):
  return spyce1.phaseq(et, target, illmn, obsrvr, abcorr)

def phaseq_vector(et, target, illmn, obsrvr, abcorr):
  return spyce1.phaseq_vector(et, target, illmn, obsrvr, abcorr)

def pi():
  return spyce1.pi()

def pipool(name, ivals):
  return spyce1.pipool(name, ivals)

def pjelpl(elin, plane):
  return spyce1.pjelpl(elin, plane)

def pjelpl_vector(elin, plane):
  return spyce1.pjelpl_vector(elin, plane)

def pl2nvc(plane):
  return spyce1.pl2nvc(plane)

def pl2nvc_vector(plane):
  return spyce1.pl2nvc_vector(plane)

def pl2nvp(plane):
  return spyce1.pl2nvp(plane)

def pl2nvp_vector(plane):
  return spyce1.pl2nvp_vector(plane)

def pl2psv(plane):
  return spyce1.pl2psv(plane)

def pl2psv_vector(plane):
  return spyce1.pl2psv_vector(plane)

def pltar(vrtces, plates):
  return spyce1.pltar(vrtces, plates)

def pltexp(iverts, delta):
  return spyce1.pltexp(iverts, delta)

def pltexp_vector(iverts, delta):
  return spyce1.pltexp_vector(iverts, delta)

def pltnp(point, v1, v2, v3):
  return spyce1.pltnp(point, v1, v2, v3)

def pltnp_vector(point, v1, v2, v3):
  return spyce1.pltnp_vector(point, v1, v2, v3)

def pltvol(vrtces, plates):
  return spyce1.pltvol(vrtces, plates)

def prop2b(gm, pvinit, dt):
  return spyce1.prop2b(gm, pvinit, dt)

def prop2b_vector(gm, pvinit, dt):
  return spyce1.prop2b_vector(gm, pvinit, dt)

def psv2pl(point, span1, span2):
  return spyce1.psv2pl(point, span1, span2)

def psv2pl_vector(point, span1, span2):
  return spyce1.psv2pl_vector(point, span1, span2)

def pxform(fromfr, tofr, et):
  return spyce1.pxform(fromfr, tofr, et)

def pxform_vector(fromfr, tofr, et):
  return spyce1.pxform_vector(fromfr, tofr, et)

def pxfrm2(fromfr, tofr, etfrom, etto):
  return spyce1.pxfrm2(fromfr, tofr, etfrom, etto)

def pxfrm2_vector(fromfr, tofr, etfrom, etto):
  return spyce1.pxfrm2_vector(fromfr, tofr, etfrom, etto)

def q2m(q):
  return spyce1.q2m(q)

def q2m_vector(q):
  return spyce1.q2m_vector(q)

def qcktrc():
  return spyce1.qcktrc()

def qdq2av(q, dq):
  return spyce1.qdq2av(q, dq)

def qdq2av_vector(q, dq):
  return spyce1.qdq2av_vector(q, dq)

def qxq(q1, q2):
  return spyce1.qxq(q1, q2)

def qxq_vector(q1, q2):
  return spyce1.qxq_vector(q1, q2)

def radrec(range, ra, dec):
  return spyce1.radrec(range, ra, dec)

def radrec_vector(range, ra, dec):
  return spyce1.radrec_vector(range, ra, dec)

def rav2xf(rot, av):
  return spyce1.rav2xf(rot, av)

def rav2xf_vector(rot, av):
  return spyce1.rav2xf_vector(rot, av)

def raxisa(matrix):
  return spyce1.raxisa(matrix)

def raxisa_vector(matrix):
  return spyce1.raxisa_vector(matrix)

def reccyl(rectan):
  return spyce1.reccyl(rectan)

def reccyl_vector(rectan):
  return spyce1.reccyl_vector(rectan)

def recgeo(rectan, re, f):
  return spyce1.recgeo(rectan, re, f)

def recgeo_vector(rectan, re, f):
  return spyce1.recgeo_vector(rectan, re, f)

def reclat(rectan):
  return spyce1.reclat(rectan)

def reclat_vector(rectan):
  return spyce1.reclat_vector(rectan)

def recpgr(body, rectan, re, f):
  return spyce1.recpgr(body, rectan, re, f)

def recpgr_vector(body, rectan, re, f):
  return spyce1.recpgr_vector(body, rectan, re, f)

def recrad(rectan):
  return spyce1.recrad(rectan)

def recrad_vector(rectan):
  return spyce1.recrad_vector(rectan)

def recsph(rectan):
  return spyce1.recsph(rectan)

def recsph_vector(rectan):
  return spyce1.recsph_vector(rectan)

def refchg(frame1, frame2, et):
  return spyce1.refchg(frame1, frame2, et)

def refchg_vector(frame1, frame2, et):
  return spyce1.refchg_vector(frame1, frame2, et)

def repmc(instr, marker, value):
  return spyce1.repmc(instr, marker, value)

def repmct(instr, marker, value, repcase):
  return spyce1.repmct(instr, marker, value, repcase)

def repmd(instr, marker, value, sigdig):
  return spyce1.repmd(instr, marker, value, sigdig)

def repmf(instr, marker, value, sigdig, format):
  return spyce1.repmf(instr, marker, value, sigdig, format)

def repmi(instr, marker, value):
  return spyce1.repmi(instr, marker, value)

def repmot(instr, marker, value, repcase):
  return spyce1.repmot(instr, marker, value, repcase)

def reset():
  return spyce1.reset()

def rotate(angle, iaxis):
  return spyce1.rotate(angle, iaxis)

def rotate_vector(angle, iaxis):
  return spyce1.rotate_vector(angle, iaxis)

def rotmat(m1, angle, iaxis):
  return spyce1.rotmat(m1, angle, iaxis)

def rotmat_vector(m1, angle, iaxis):
  return spyce1.rotmat_vector(m1, angle, iaxis)

def rotvec(v1, angle, iaxis):
  return spyce1.rotvec(v1, angle, iaxis)

def rotvec_vector(v1, angle, iaxis):
  return spyce1.rotvec_vector(v1, angle, iaxis)

def rpd():
  return spyce1.rpd()

def rquad(a, b, c):
  return spyce1.rquad(a, b, c)

def rquad_vector(a, b, c):
  return spyce1.rquad_vector(a, b, c)

def saelgv(vec1, vec2):
  return spyce1.saelgv(vec1, vec2)

def saelgv_vector(vec1, vec2):
  return spyce1.saelgv_vector(vec1, vec2)

def scdecd(sc, sclkdp):
  return spyce1.scdecd(sc, sclkdp)

def sce2c(sc, et):
  return spyce1.sce2c(sc, et)

def sce2c_vector(sc, et):
  return spyce1.sce2c_vector(sc, et)

def sce2s(sc, et):
  return spyce1.sce2s(sc, et)

def sce2t(sc, et):
  return spyce1.sce2t(sc, et)

def sce2t_vector(sc, et):
  return spyce1.sce2t_vector(sc, et)

def scencd(sc, sclkch):
  return spyce1.scencd(sc, sclkch)

def scfmt(sc, ticks):
  return spyce1.scfmt(sc, ticks)

def scpart(sc):
  return spyce1.scpart(sc)

def scs2e(sc, sclkch):
  return spyce1.scs2e(sc, sclkch)

def sct2e(sc, sclkdp):
  return spyce1.sct2e(sc, sclkdp)

def sct2e_vector(sc, sclkdp):
  return spyce1.sct2e_vector(sc, sclkdp)

def sctiks(sc, clkstr):
  return spyce1.sctiks(sc, clkstr)

def setmsg(message):
  return spyce1.setmsg(message)

def sigerr(message):
  return spyce1.sigerr(message)

def sincpt(method, target, et, fixref, abcorr, obsrvr, dref, dvec):
  return spyce1.sincpt(method, target, et, fixref, abcorr, obsrvr, dref, dvec)

def sincpt_vector(method, target, et, fixref, abcorr, obsrvr, dref, dvec):
  return spyce1.sincpt_vector(method, target, et, fixref, abcorr, obsrvr, dref, dvec)

def spd():
  return spyce1.spd()

def sphcyl(radius, colat, lon):
  return spyce1.sphcyl(radius, colat, lon)

def sphcyl_vector(radius, colat, lon):
  return spyce1.sphcyl_vector(radius, colat, lon)

def sphlat(radius, colat, lon):
  return spyce1.sphlat(radius, colat, lon)

def sphlat_vector(radius, colat, lon):
  return spyce1.sphlat_vector(radius, colat, lon)

def sphrec(radius, colat, lon):
  return spyce1.sphrec(radius, colat, lon)

def sphrec_vector(radius, colat, lon):
  return spyce1.sphrec_vector(radius, colat, lon)

def spkacs(targ, et, ref, abcorr, obs):
  return spyce1.spkacs(targ, et, ref, abcorr, obs)

def spkacs_vector(targ, et, ref, abcorr, obs):
  return spyce1.spkacs_vector(targ, et, ref, abcorr, obs)

def spkapo(targ, et, ref, sobs, abcorr):
  return spyce1.spkapo(targ, et, ref, sobs, abcorr)

def spkapo_vector(targ, et, ref, sobs, abcorr):
  return spyce1.spkapo_vector(targ, et, ref, sobs, abcorr)

def spkapp(targ, et, ref, sobs, abcorr):
  return spyce1.spkapp(targ, et, ref, sobs, abcorr)

def spkapp_vector(targ, et, ref, sobs, abcorr):
  return spyce1.spkapp_vector(targ, et, ref, sobs, abcorr)

def spkaps(targ, et, ref, abcorr, stobs, accobs):
  return spyce1.spkaps(targ, et, ref, abcorr, stobs, accobs)

def spkaps_vector(targ, et, ref, abcorr, stobs, accobs):
  return spyce1.spkaps_vector(targ, et, ref, abcorr, stobs, accobs)

def spkcov(spk, idcode):
  return spyce1.spkcov(spk, idcode)

def spkcov_error(spk, idcode):
  return spyce1.spkcov_error(spk, idcode)

def spkez(targ, et, ref, abcorr, obs):
  return spyce1.spkez(targ, et, ref, abcorr, obs)

def spkez_vector(targ, et, ref, abcorr, obs):
  return spyce1.spkez_vector(targ, et, ref, abcorr, obs)

def spkezp(targ, et, ref, abcorr, obs):
  return spyce1.spkezp(targ, et, ref, abcorr, obs)

def spkezp_vector(targ, et, ref, abcorr, obs):
  return spyce1.spkezp_vector(targ, et, ref, abcorr, obs)

def spkezr(target, et, ref, abcorr, obsrvr):
  return spyce1.spkezr(target, et, ref, abcorr, obsrvr)

def spkezr_vector(target, et, ref, abcorr, obsrvr):
  return spyce1.spkezr_vector(target, et, ref, abcorr, obsrvr)

def spkgeo(targ, et, ref, obs):
  return spyce1.spkgeo(targ, et, ref, obs)

def spkgeo_vector(targ, et, ref, obs):
  return spyce1.spkgeo_vector(targ, et, ref, obs)

def spkgps(targ, et, ref, obs):
  return spyce1.spkgps(targ, et, ref, obs)

def spkgps_vector(targ, et, ref, obs):
  return spyce1.spkgps_vector(targ, et, ref, obs)

def spkltc(targ, et, ref, abcorr, stobs):
  return spyce1.spkltc(targ, et, ref, abcorr, stobs)

def spkltc_vector(targ, et, ref, abcorr, stobs):
  return spyce1.spkltc_vector(targ, et, ref, abcorr, stobs)

def spkobj(spk):
  return spyce1.spkobj(spk)

def spkpos(target, et, ref, abcorr, obsrvr):
  return spyce1.spkpos(target, et, ref, abcorr, obsrvr)

def spkpos_vector(target, et, ref, abcorr, obsrvr):
  return spyce1.spkpos_vector(target, et, ref, abcorr, obsrvr)

def spkssb(targ, et, ref):
  return spyce1.spkssb(targ, et, ref)

def spkssb_vector(targ, et, ref):
  return spyce1.spkssb_vector(targ, et, ref)

def srfc2s(code, bodyid):
  return spyce1.srfc2s(code, bodyid)

def srfc2s_error(code, bodyid):
  return spyce1.srfc2s_error(code, bodyid)

def srfcss(code, bodstr):
  return spyce1.srfcss(code, bodstr)

def srfcss_error(code, bodstr):
  return spyce1.srfcss_error(code, bodstr)

def srfnrm(method, target, et, fixref):
  return spyce1.srfnrm(method, target, et, fixref)

def srfrec(body, lon, lat):
  return spyce1.srfrec(body, lon, lat)

def srfrec_vector(body, lon, lat):
  return spyce1.srfrec_vector(body, lon, lat)

def srfs2c(srfstr, bodstr):
  return spyce1.srfs2c(srfstr, bodstr)

def srfs2c_error(srfstr, bodstr):
  return spyce1.srfs2c_error(srfstr, bodstr)

def srfscc(srfstr, bodyid):
  return spyce1.srfscc(srfstr, bodyid)

def srfscc_error(srfstr, bodyid):
  return spyce1.srfscc_error(srfstr, bodyid)

def srfxpt(method, target, et, abcorr, obsrvr, dref, dvec):
  return spyce1.srfxpt(method, target, et, abcorr, obsrvr, dref, dvec)

def srfxpt_vector(method, target, et, abcorr, obsrvr, dref, dvec):
  return spyce1.srfxpt_vector(method, target, et, abcorr, obsrvr, dref, dvec)

def stcf01(catnam, westra, eastra, sthdec, nthdec):
  return spyce1.stcf01(catnam, westra, eastra, sthdec, nthdec)

def stcg01(index):
  return spyce1.stcg01(index)

def stcl01(catfnm):
  return spyce1.stcl01(catfnm)

def stelab(pobj, vobs):
  return spyce1.stelab(pobj, vobs)

def stelab_vector(pobj, vobs):
  return spyce1.stelab_vector(pobj, vobs)

def stlabx(pobj, vobs):
  return spyce1.stlabx(pobj, vobs)

def stlabx_vector(pobj, vobs):
  return spyce1.stlabx_vector(pobj, vobs)

def stpool(item, nth, contin):
  return spyce1.stpool(item, nth, contin)

def stpool_error(item, nth, contin):
  return spyce1.stpool_error(item, nth, contin)

def str2et(str):
  return spyce1.str2et(str)

def subpnt(method, target, et, fixref, abcorr, obsrvr):
  return spyce1.subpnt(method, target, et, fixref, abcorr, obsrvr)

def subpnt_vector(method, target, et, fixref, abcorr, obsrvr):
  return spyce1.subpnt_vector(method, target, et, fixref, abcorr, obsrvr)

def subpt(method, target, et, abcorr, obsrvr):
  return spyce1.subpt(method, target, et, abcorr, obsrvr)

def subpt_vector(method, target, et, abcorr, obsrvr):
  return spyce1.subpt_vector(method, target, et, abcorr, obsrvr)

def subslr(method, target, et, fixref, abcorr, obsrvr):
  return spyce1.subslr(method, target, et, fixref, abcorr, obsrvr)

def subslr_vector(method, target, et, fixref, abcorr, obsrvr):
  return spyce1.subslr_vector(method, target, et, fixref, abcorr, obsrvr)

def subsol(method, target, et, abcorr, obsrvr):
  return spyce1.subsol(method, target, et, abcorr, obsrvr)

def subsol_vector(method, target, et, abcorr, obsrvr):
  return spyce1.subsol_vector(method, target, et, abcorr, obsrvr)

def surfnm(a, b, c, point):
  return spyce1.surfnm(a, b, c, point)

def surfpt(positn, u, a, b, c):
  return spyce1.surfpt(positn, u, a, b, c)

def surfpt_vector(positn, u, a, b, c):
  return spyce1.surfpt_vector(positn, u, a, b, c)

def surfpv(stvrtx, stdir, a, b, c):
  return spyce1.surfpv(stvrtx, stdir, a, b, c)

def surfpv_vector(stvrtx, stdir, a, b, c):
  return spyce1.surfpv_vector(stvrtx, stdir, a, b, c)

def sxform(fromfr, tofr, et):
  return spyce1.sxform(fromfr, tofr, et)

def sxform_vector(fromfr, tofr, et):
  return spyce1.sxform_vector(fromfr, tofr, et)

def termpt(method, ilusrc, target, et, fixref, abcorr, corloc, obsrvr, refvec, rolstp, ncuts, schstp, soltol, maxn):
  return spyce1.termpt(method, ilusrc, target, et, fixref, abcorr, corloc, obsrvr, refvec, rolstp, ncuts, schstp, soltol, maxn)

def timdef(action, item, value):
  return spyce1.timdef(action, item, value)

def timout(et, pictur):
  return spyce1.timout(et, pictur)

def tipbod(ref, body, et):
  return spyce1.tipbod(ref, body, et)

def tipbod_vector(ref, body, et):
  return spyce1.tipbod_vector(ref, body, et)

def tisbod(ref, body, et):
  return spyce1.tisbod(ref, body, et)

def tisbod_vector(ref, body, et):
  return spyce1.tisbod_vector(ref, body, et)

def tkvrsn(item):
  return spyce1.tkvrsn(item)

def tparse(string):
  return spyce1.tparse(string)

def tparse_error(string):
  return spyce1.tparse_error(string)

def tpictr(sample):
  return spyce1.tpictr(sample)

def tpictr_error(sample):
  return spyce1.tpictr_error(sample)

def trace(matrix):
  return spyce1.trace(matrix)

def trace_vector(matrix):
  return spyce1.trace_vector(matrix)

def trcdep():
  return spyce1.trcdep()

def trcnam(index):
  return spyce1.trcnam(index)

def trcoff():
  return spyce1.trcoff()

def tsetyr(year):
  return spyce1.tsetyr(year)

def twopi():
  return spyce1.twopi()

def twovec(axdef, indexa, plndef, indexp):
  return spyce1.twovec(axdef, indexa, plndef, indexp)

def twovec_vector(axdef, indexa, plndef, indexp):
  return spyce1.twovec_vector(axdef, indexa, plndef, indexp)

def tyear():
  return spyce1.tyear()

def ucrss(v1, v2):
  return spyce1.ucrss(v1, v2)

def ucrss_vector(v1, v2):
  return spyce1.ucrss_vector(v1, v2)

def unitim(epoch, insys, outsys):
  return spyce1.unitim(epoch, insys, outsys)

def unitim_vector(epoch, insys, outsys):
  return spyce1.unitim_vector(epoch, insys, outsys)

def unload(file):
  return spyce1.unload(file)

def unorm(v1):
  return spyce1.unorm(v1)

def unorm_vector(v1):
  return spyce1.unorm_vector(v1)

def unormg(v1):
  return spyce1.unormg(v1)

def unormg_vector(v1):
  return spyce1.unormg_vector(v1)

def utc2et(utcstr):
  return spyce1.utc2et(utcstr)

def vadd(v1, v2):
  return spyce1.vadd(v1, v2)

def vadd_vector(v1, v2):
  return spyce1.vadd_vector(v1, v2)

def vaddg(v1, v2):
  return spyce1.vaddg(v1, v2)

def vaddg_vector(v1, v2):
  return spyce1.vaddg_vector(v1, v2)

def vcrss(v1, v2):
  return spyce1.vcrss(v1, v2)

def vcrss_vector(v1, v2):
  return spyce1.vcrss_vector(v1, v2)

def vdist(v1, v2):
  return spyce1.vdist(v1, v2)

def vdist_vector(v1, v2):
  return spyce1.vdist_vector(v1, v2)

def vdistg(v1, v2):
  return spyce1.vdistg(v1, v2)

def vdistg_vector(v1, v2):
  return spyce1.vdistg_vector(v1, v2)

def vdot(v1, v2):
  return spyce1.vdot(v1, v2)

def vdot_vector(v1, v2):
  return spyce1.vdot_vector(v1, v2)

def vdotg(v1, v2):
  return spyce1.vdotg(v1, v2)

def vdotg_vector(v1, v2):
  return spyce1.vdotg_vector(v1, v2)

def vequ(vin):
  return spyce1.vequ(vin)

def vequ_vector(vin):
  return spyce1.vequ_vector(vin)

def vequg(vin):
  return spyce1.vequg(vin)

def vequg_vector(vin):
  return spyce1.vequg_vector(vin)

def vhat(v1):
  return spyce1.vhat(v1)

def vhat_vector(v1):
  return spyce1.vhat_vector(v1)

def vhatg(v1):
  return spyce1.vhatg(v1)

def vhatg_vector(v1):
  return spyce1.vhatg_vector(v1)

def vlcom(a, v1, b, v2):
  return spyce1.vlcom(a, v1, b, v2)

def vlcom3(a, v1, b, v2, c, v3):
  return spyce1.vlcom3(a, v1, b, v2, c, v3)

def vlcom3_vector(a, v1, b, v2, c, v3):
  return spyce1.vlcom3_vector(a, v1, b, v2, c, v3)

def vlcom_vector(a, v1, b, v2):
  return spyce1.vlcom_vector(a, v1, b, v2)

def vlcomg(a, v1, b, v2):
  return spyce1.vlcomg(a, v1, b, v2)

def vlcomg_vector(a, v1, b, v2):
  return spyce1.vlcomg_vector(a, v1, b, v2)

def vminug(vin):
  return spyce1.vminug(vin)

def vminug_vector(vin):
  return spyce1.vminug_vector(vin)

def vminus(v1):
  return spyce1.vminus(v1)

def vminus_vector(v1):
  return spyce1.vminus_vector(v1)

def vnorm(v1):
  return spyce1.vnorm(v1)

def vnorm_vector(v1):
  return spyce1.vnorm_vector(v1)

def vnormg(v1):
  return spyce1.vnormg(v1)

def vnormg_vector(v1):
  return spyce1.vnormg_vector(v1)

def vpack(x, y, z):
  return spyce1.vpack(x, y, z)

def vpack_vector(x, y, z):
  return spyce1.vpack_vector(x, y, z)

def vperp(v1, v2):
  return spyce1.vperp(v1, v2)

def vperp_vector(v1, v2):
  return spyce1.vperp_vector(v1, v2)

def vprjp(vin, plane):
  return spyce1.vprjp(vin, plane)

def vprjp_vector(vin, plane):
  return spyce1.vprjp_vector(vin, plane)

def vprjpi(vin, projpl, invpl):
  return spyce1.vprjpi(vin, projpl, invpl)

def vprjpi_vector(vin, projpl, invpl):
  return spyce1.vprjpi_vector(vin, projpl, invpl)

def vproj(v1, v2):
  return spyce1.vproj(v1, v2)

def vproj_vector(v1, v2):
  return spyce1.vproj_vector(v1, v2)

def vrel(v1, v2):
  return spyce1.vrel(v1, v2)

def vrel_vector(v1, v2):
  return spyce1.vrel_vector(v1, v2)

def vrelg(v1, v2):
  return spyce1.vrelg(v1, v2)

def vrelg_vector(v1, v2):
  return spyce1.vrelg_vector(v1, v2)

def vrotv(v, axis, theta):
  return spyce1.vrotv(v, axis, theta)

def vrotv_vector(v, axis, theta):
  return spyce1.vrotv_vector(v, axis, theta)

def vscl(s, v1):
  return spyce1.vscl(s, v1)

def vscl_vector(s, v1):
  return spyce1.vscl_vector(s, v1)

def vsclg(s, v1):
  return spyce1.vsclg(s, v1)

def vsclg_vector(s, v1):
  return spyce1.vsclg_vector(s, v1)

def vsep(v1, v2):
  return spyce1.vsep(v1, v2)

def vsep_vector(v1, v2):
  return spyce1.vsep_vector(v1, v2)

def vsepg(v1, v2):
  return spyce1.vsepg(v1, v2)

def vsepg_vector(v1, v2):
  return spyce1.vsepg_vector(v1, v2)

def vsub(v1, v2):
  return spyce1.vsub(v1, v2)

def vsub_vector(v1, v2):
  return spyce1.vsub_vector(v1, v2)

def vsubg(v1, v2):
  return spyce1.vsubg(v1, v2)

def vsubg_vector(v1, v2):
  return spyce1.vsubg_vector(v1, v2)

def vtmv(v1, matrix, v2):
  return spyce1.vtmv(v1, matrix, v2)

def vtmv_vector(v1, matrix, v2):
  return spyce1.vtmv_vector(v1, matrix, v2)

def vtmvg(v1, matrix, v2):
  return spyce1.vtmvg(v1, matrix, v2)

def vtmvg_vector(v1, matrix, v2):
  return spyce1.vtmvg_vector(v1, matrix, v2)

def vupack(v):
  return spyce1.vupack(v)

def vupack_vector(v):
  return spyce1.vupack_vector(v)

def vzero(v):
  return spyce1.vzero(v)

def vzero_vector(v):
  return spyce1.vzero_vector(v)

def vzerog(v):
  return spyce1.vzerog(v)

def vzerog_vector(v):
  return spyce1.vzerog_vector(v)

def xf2eul(xform, axisa, axisb, axisc):
  return spyce1.xf2eul(xform, axisa, axisb, axisc)

def xf2eul_vector(xform, axisa, axisb, axisc):
  return spyce1.xf2eul_vector(xform, axisa, axisb, axisc)

def xf2rav(xform):
  return spyce1.xf2rav(xform)

def xf2rav_vector(xform):
  return spyce1.xf2rav_vector(xform)

def xfmsta(instate, insys, outsys, body):
  return spyce1.xfmsta(instate, insys, outsys, body)

def xfmsta_vector(instate, insys, outsys, body):
  return spyce1.xfmsta_vector(instate, insys, outsys, body)

def xpose(m1):
  return spyce1.xpose(m1)

def xpose6(m1):
  return spyce1.xpose6(m1)

def xpose6_vector(m1):
  return spyce1.xpose6_vector(m1)

def xpose_vector(m1):
  return spyce1.xpose_vector(m1)

def xposeg(matrix):
  return spyce1.xposeg(matrix)

def xposeg_vector(matrix):
  return spyce1.xposeg_vector(matrix)

# Upon execution, re-connect all the lost attibutes and broken links...

relink_all(globals(), spyce1.__dict__)

################################################################################
