################################################################################
# cspice1/__init__.py
################################################################################
# PDS RMS Node CSPICE-Python interface
# Library cspice1
#
# This module provides a very basic Python interface to the CSPICE library.
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
# - For every function that handles exceptions in a non-Pythonic way, there
#   exists a function with the same name but suffix "_error". This latter
#   function suppresses any status flags from the returned quantity and,
#   instead, raises an appropriate Python exception, which is typically
#   KeyError.
# - For every one of these functions, there also exists a function with the
#   same name but suffix "_flag", which returns the same flags as does the
#   associated C function.
#
# You can use these functions to switch the default behavior of any of these
# functions.
#   use_exceptions_not_flags(names)
#   use_flags_not_exceptions(names)
#
# You can also obtain a particular version of any function using these
# functions, which return functions:
#   exception_version(func)
#   flag_version(func)
#
# November 2017
################################################################################

from cspice_swig import *
import cspice_swig as swig

from cspice_info import SPICE_DOCSTRINGS, SPICE_SIGNATURES, SPICE_RETURNS
from cspice_info import SPICE_DEFAULTS

SPICE_DOCSTRINGS = cspice_info.SPICE_DOCSTRINGS
SPICE_SIGNATURES = cspice_info.SPICE_SIGNATURES
SPICE_RETURNS    = cspice_info.SPICE_RETURNS
SPICE_DEFAULTS   = cspice_info.SPICE_DEFAULTS

################################################################################
# Define versions of functions that raise exceptions rather than set status
# flags
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

def cidfrm_error(name):
    (code, name, found) = swig.cidfrm(code)
    if not found:
        raise KeyError('Error in cidfrm(): body code %d not found' % code)

    return [code, name]

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

def _process_types(signature):
    """Validates the contents of a signature, and replaces array entries with
    a partially parsed representation as a tuple."""

    newsig = []

    # Loop through elements in the given signature
    # The signature of each function is defined in cspice_info.py
    for k in range(len(signature)):
        argtype = signature[k]

        # Interpret argtype if it is an array declaration
        # E.g., replace "float[*,3]" with ("float", (0,3))
        if '[' in argtype:
            parts = argtype.split('[')
            assert len(parts) == 2
            argtype = parts[0]
            assert argtype in ('float', 'int', 'bool', 'string')

            assert parts[1].endswith(']')
            shapestr = ('(' + parts[1][:-1] + ')').replace('*', '0')
            shape = eval(shapestr)

            newsig.append((argtype, shape))

        # Validate a scalar argtype
        else:
            assert argtype in ('float', 'int', 'bool', 'string',
                               'body_code', 'body_name',
                               'frame_code', 'frame_name')
            newsig.append(argtype)

    return newsig

# At runtime, apply docstrings, SIGNATURE, RETURNS and DEFAULTS attributes to
# all the cspice1 functions 
for key in SPICE_DOCSTRINGS:
    if key in globals():
        globals()[key].__doc__ = SPICE_DOCSTRINGS[key]

        signature = _process_types(SPICE_SIGNATURES[key])
        returns   = _process_types(SPICE_RETURNS[key])

        globals()[key].SIGNATURE = signature
        globals()[key].RETURNS   = returns

        if key in SPICE_DEFAULTS:
            globals()[key].func_defaults = tuple(SPICE_DEFAULTS[key])

# At runtime, save a function *_flag for every function *_error
keys = SPICE_DOCSTRINGS.keys()  # save keys first because dictionary changes
for key in keys:
    if key in globals():
        if not key.endswith('_error'): continue

        short_key = key[:-6]
        flag_key = short_key + '_flag'

        globals()[flag_key] = globals()[short_key]

        SPICE_DOCSTRINGS[flag_key] = SPICE_DOCSTRINGS[short_key]
        SPICE_SIGNATURES[flag_key] = SPICE_SIGNATURES[short_key]
        SPICE_RETURNS   [flag_key] = SPICE_RETURNS   [short_key]

        if short_key in SPICE_DEFAULTS:
            SPICE_DEFAULTS[flag_key] = SPICE_DEFAULTS[short_key]

################################################################################
# Define functions to select between *_error and *_flag versions of functions
################################################################################

def _strip_error_flag(name):
    if name.endswith('_error'):
        name = name[:-6]
    elif name.endswith('_flag'):
        name = name[:-5]

    return name

def use_errors(names=[]):
    """Switch all functions, or just those listed, to raise exceptions instead
    of returning flags."""

    if names:
        keys = [_strip_error_flag(n) for n in names]
    else:
        keys = [n[:-6] for n in SPICE_DOCSTRINGS if n.endswith('_error')]

    for key in keys:
        long_key = key + '_error'
        if key in globals() and long_key in globals():
            globals()[key] = globals()[long_key]

def use_flags(names=[]):
    """Switch all functions, or just those listed, to return flags instead of
    raising exceptions."""

    if names:
        keys = [_strip_error_flag(n) for n in names]
    else:
        keys = [n[:-6] for n in SPICE_DOCSTRINGS if not n.endswith('_error')]

    for key in keys:
        long_key = key + '_flag'
        if key in globals() and long_key in globals():
            globals()[key] = globals()[long_key]

def error_version(func):
    """Return the _error version of this function, if available."""

    long_key = _strip_error_flag(func.__name__) + '_error'
    if long_key in globals():
        return globals()[long_key]

    return func

def flag_version(func):
    """Return the flag version of this function."""

    long_key = _strip_error_flag(func.__name__) + '_flag'
    if long_key in globals():
        return globals()[long_key]

    return func

def function_lookup(name):
    """Return the cspice1 function with this name."""

    if name in SPICE_DOCSTRINGS:
        return globals()[name]

    short_name = _strip_error_flag(name)
    if short_name in SPICE_DOCSTRINGS:
        return globals()[short_name]

    raise KeyError('cspice1 function "%s" not found' % name)

################################################################################
