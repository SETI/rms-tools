################################################################################
# cspice1/__init__.py
################################################################################
# PDS RMS Node CSPICE-Python interface
# Library cspice1
#
# This module provides a basic Python interface to the CSPICE library.
#
# - Access to CSPICE library functions are provided through SWIG wrappers.
# - Essentially every function that a user is likely to call directly is
#   included; lower-level functions are not.
# - No checking of argument types is performed, so it is possible for Python to
#   hit a segmenation fault and abort.
# - All functions have informative docstrings.
# - A few function arguments use sensible default values for missing arguments.
#       In gcpool, gdpool, gipool, and gnpool, start defaults to 1.
#       In erract, errdev, errprt, op defaults to 'GET' and action is set to ''.
# - Two vectorized functions are provided that allow a 1-D vector of et values
#       as input: spkez_vector and sxform_vector.
# - All conditions encountered by the toolkit raise RuntimErrors, which include
#   the complete text of the CSPICE error message.
#
# Additional Error Handling
#
# Several CSPICE function use non-Pythonic ways of raising exceptions. For
# example, a number of functions return a boolean flag value where True
# indicates success and False indicates failure. This interface to CSPICE gives
# the user control over how these situations are handled:
#
# - For every function that handles exceptions in a non-Pythonic way, there
#   exists a function with the same name but suffix "_error". This latter
#   function suppresses any status flags from the returned quantity and,
#   instead, raises an appropriate Python exception, which is typically
#   KeyError.
#
# - For every one of these functions, there also exists a function with the
#   same name but suffix "_flag", which returns the same flags as does the
#   associated C function.
#
# You can use these functions to switch the default behavior of any of these
# functions.
#   use_errors()
#   use_flags()
# For backwards compatibility, use_errors() is the default.
#
# Every function also has attributes error_version and flag_version, which
# return the version of the function that uses either of these options. For
# functions that do not have error and flag versions, these attributes return
# the function itself.
#
# Mark Showalter, PDS Ring-Moon Systems Node, December 4, 2017
################################################################################

from cspice_swig import *
import cspice_swig as swig

from cspice_info import CSPICE1_DOCSTRINGS, CSPICE1_SIGNATURES, CSPICE1_RETURNS
from cspice_info import CSPICE1_DEFAULTS

VERSION = 1

################################################################################
# Define _error versions of functions that raise exceptions rather than return
# status flags
################################################################################

def bodc2n_error(code):
    (name, found) = swig.bodc2n(code)
    if not found:
        raise KeyError('Error in bodc2n(): body code %d not found' % code)

    return name

def bodn2c_error(name):
    (code, found) = swig.bodn2c(name)
    if not found:
        raise KeyError('Error in bodn2c(): body name "%s" not found' % name)

    return code

def bods2c_error(name):
    (code, found) = swig.bods2c(name)
    if not found:
        raise KeyError('Error in bods2c(): body name "%s" not found' % name)

    return code

def ckcov_error(ck, code, *args):
    coverage = swig.ckcov(ck, code, *args)
    if coverage.size == 0:
        raise KeyError('Error in ckcov(): body code %d not found' % code)

    return coverage

def cidfrm_error(code):
    (frcode, name, found) = swig.cidfrm(code)
    if not found:
        raise KeyError('Error in cidfrm(): body code %d not found' % code)

    return [frcode, name]

def ckgp_error(*args):
    (cmat, clkout, found) = swig.ckgp(*args)
    if not found:
        raise ValueError('Error in ckgp(): C matrix not found')

    return [cmat, clkout]

def ckgpav_error(*args):
    (cmat, av, clkout, found) = swig.ckgpav(*args)
    if not found:
        raise ValueError('Error in ckgpav(): C matrix not found')

    return [cmat, av, clkout]

def cnmfrm_error(cname):
    (frcode, frname, found) = swig.cnmfrm(cname)
    if not found:
        raise KeyError('Error in cnmfrm(): body name "%s" not found' % cname)

    return [frcode, frname]

def dtpool_error(name):
    (found, n, vtype) = swig.dtpool(name)
    if not found:
        raise KeyError('Error in dtpool(): pool variable "%s" not found' % name)

    return [n, vtype]

def frinfo_error(frcode):
    (cent, frclss, clssid, found) = swig.frinfo(frcode)
    if not found:
        raise KeyError('Error in frinfo(): frame code %d not found' % frcode)

    return [cent, frclss, clssid]

def frmnam_error(frcode):
    frname = swig.frmnam(frcode)
    if frname == '':
        raise KeyError('Error in frmnam(): frame code %d not found' % frcode)

    return frname

def gcpool_error(name, start=1):
    (cvals, found) = swig.gcpool(name, start)
    if not found:
        raise KeyError('Error in gcpool(): pool variable "%s" not found' % name)

    return cvals

def gdpool_error(name, start=1):
    (values, found) = swig.gdpool(name, start)
    if not found:
        raise KeyError('Error in gdpool(): pool variable "%s" not found' % name)

    return values

def gipool_error(name, start=1):
    (ivals, found) = swig.gipool(name, start)
    if not found:
        raise KeyError('Error in gipool(): pool variable "%s" not found' % name)

    return ivals

def gnpool_error(name, start=1):
    (kvars, found) = swig.gnpool(name, start)
    if not found:
        raise KeyError('Error in gnpool(): pool variable "%s" not found' % name)

    return kvars

def namfrm_error(frname):
    frcode = swig.namfrm(frname)
    if frcode == 0:
        raise KeyError('Error in namfrm(): frame name "%s" not found' % frname)

    return frcode

def pckcov_error(pck, code):
    coverage = swig.pckcov(pck, code)
    if coverage.size == 0:
        raise KeyError('Error in pckcov(): frame code %d not found' % code)

    return coverage

def spkcov_error(spk, code):
    coverage = swig.spkcov(spk, code)
    if coverage.size == 0:
        raise KeyError('Error in spkcov(): body code %d not found' % code)

    return coverage

def srfc2s_error(code, bodyid):
    (srfstr, isname) = swig.srfc2s(code, bodyid)
    if not isname:
        raise KeyError('Error in srfc2s(): surface for ' +
                       '%d/%d not found' % (code, bodyid))

    return srfstr

def srfcss_error(code, bodstr):
    (srfstr, isname) = swig.srfcss(code, bodstr)
    if not isname:
        raise KeyError('Error in srfcss(): surface for ' +
                       '%d/"%s" not found' % (code, bodstr))

    return srfstr

def srfs2c_error(srfstr, bodstr):
    (code, found) = swig.srfs2c(srfstr, bodstr)
    if not found:
        raise KeyError('Error in srfs2c(): surface for ' +
                       '"%s"/"%s" not found' % (srfstr, bodstr))

    return code

def srfscc_error(srfstr, bodyid):
    (code, found) = swig.srfscc(srfstr, bodyid)
    if not found:
        raise KeyError('Error in srfscc(): surface for ' +
                       '"%s"/%d not found' % (srfstr, bodyid))

    return code

def stpool_error(item, nth, contin):
    (string, found) = swig.stpool(item, nth, contin)
    if not found:
        raise KeyError('Error in stpool(): pool variable "%s" not found' % item)

    return string

################################################################################
# Assign docstrings, signatures, return values and defaults
#
# Each cspice1 function has these additional attributes, which are used
# primarily by the cspice2 module.
#   SIGNATURE = a list indicating the type of each argument;
#   RETURN    = a list indicating the type of each return value;
################################################################################

# At initialization, apply docstrings, SIGNATURE, RETURNS and func_defaults
# attributes to all the cspice1 functions.

for name in CSPICE1_DOCSTRINGS:
    globals()[name].__doc__   = CSPICE1_DOCSTRINGS[name]
    globals()[name].SIGNATURE = CSPICE1_SIGNATURES[name]
    globals()[name].RETURNS   = CSPICE1_RETURNS[name]

    if name in CSPICE1_DEFAULTS:
        globals()[name].func_defaults = tuple(CSPICE1_DEFAULTS[name])

# At initialization, define a function *_flag for every function *_error.
#
# Also save...
#   CSPICE1_FUNC_NAMES      = a list of every function name.
#   CSPICE1_FUNC_BASENAMES  = a list of every unique function basename (without
#                             a _error or _flag suffix).
#   CSPICE1_ERROR_BASENAMES = a list of every basename that takes _error and
#                             _flag suffixes.

CSPICE1_FUNC_NAMES = CSPICE1_DOCSTRINGS.keys()
CSPICE1_FUNC_BASENAMES = []
CSPICE1_ERROR_BASENAMES = []

for name in CSPICE1_FUNC_NAMES:
    if name.endswith('_error'):
        short_name = name[:-6]
        flag_name = short_name + '_flag'

        globals()[flag_name] = globals()[short_name]

        CSPICE1_DOCSTRINGS[flag_name] = CSPICE1_DOCSTRINGS[short_name]
        CSPICE1_SIGNATURES[flag_name] = CSPICE1_SIGNATURES[short_name]
        CSPICE1_RETURNS   [flag_name] = CSPICE1_RETURNS   [short_name]

        if short_name in CSPICE1_DEFAULTS:
            CSPICE1_DEFAULTS[flag_name] = CSPICE1_DEFAULTS[short_name]

        CSPICE1_ERROR_BASENAMES.append(short_name)

    else:
        CSPICE1_FUNC_BASENAMES.append(name)

CSPICE1_FUNC_NAMES = CSPICE1_DOCSTRINGS.keys()
CSPICE1_FUNC_NAMES.sort()
CSPICE1_FUNC_BASENAMES.sort()
CSPICE1_ERROR_BASENAMES.sort()

################################################################################
# Define attributes error_version and flag_version for every function
################################################################################

def _strip_error_flag(name):
    """Remove '_error' or '_flag' from the end of a function name."""

    if name.endswith('_error'):
        name = name[:-6]
    elif name.endswith('_flag'):
        name = name[:-5]

    return name

for name in CSPICE1_FUNC_NAMES:
    func = globals()[name]
    short_key = _strip_error_flag(name)

    long_key = short_key + '_error'
    if long_key in globals():
        func.error_version = globals()[long_key]
        func.flag_version  = globals()[short_key + '_flag']
    else:
        func.error_version = func
        func.flag_version = func

################################################################################
# Define functions to select between *_error and *_flag versions of functions
################################################################################

def use_errors(*names):
    """Switch the named functions, or else all relevant cspice1 functions, to
    raise exceptions instead of returning flags."""

    if names:
        basenames = [_strip_error_flag(n) for n in names]
        for basename in basenames:
            if basename not in CSPICE1_FUNC_BASENAMES:
                raise ValueError('Unrecognized cspice function "%s"' % n)
        basenames = [n for n in basenames if n in CSPICE1_ERROR_BASENAMES]
        basenames = set(basenames)
    else:
        basenames = CSPICE1_ERROR_BASENAMES

    for basename in basenames:
        globals()[basename] = globals()[basename].error_version

def use_flags(*names):
    """Switch the named functions, or else all relevant cspice1 functions, to
    return flags instead of raising exceptions."""

    if names:
        basenames = [_strip_error_flag(n) for n in names]
        for basename in basenames:
            if basename not in CSPICE1_FUNC_BASENAMES:
                raise ValueError('Unrecognized cspice function "%s"' % n)
        basenames = [n for n in basenames if n in CSPICE1_ERROR_BASENAMES]
        basenames = set(basenames)
    else:
        basenames = CSPICE1_ERROR_BASENAMES

    for basename in basenames:
        globals()[basename] = globals()[basename].flag_version

################################################################################
# For backward compatibility, default is to use errors, not flags
################################################################################

use_errors()

################################################################################
