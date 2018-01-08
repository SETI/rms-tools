################################################################################
# cspyce/cspyce1.py
################################################################################
# module cspyce.cspyce1
#
# This module provides several enhancements over the low-level cspyce0 interface
# to the CSPICE library. See cspyce/cspyce0/__init__.py for more information
# about cspyce0.
#
# To use cspyce1:
#   import cspyce.cspyce1
# or
#   import cspyce.cspyce1 as cspyce
#
# ADDED FEATURES
#
# DOCSTRINGS
# - All cspyce functions have informative docstrings, so typing
#       help(function)
#   provides useful information.
#
# DEFAULTS
# - Many cspyce functions take sensible default values if input arguments are
#   omitted.
#   - In gcpool, gdpool, gipool, and gnpool, start values default to 1.
#   - The functions that take "SET" or "GET" as their first argument (erract,
#     errdev, errprt, and timdef) have simplified calling options, which are
#     summarized in their docstrings.
#
# ERROR HANDLING
#
# In the CSPICE error handling mechanism, the programmer must check the value
# of function failed() regularly to determine if an error has occurred. However,
# Python's exception handling mechanism obviates the need for this approach.
#
# In the cspyce1 module, we introduce two new options to function erract, which
# is used in CSPICE to control the error handling options. The options are
# 'EXCEPTION' and 'RUNTIME'. When error handling is set to one of these values,
# Python exception handling takes over. Error conditions raise exceptions
# rather than changing the value of failed(). The difference is that 'RUNTIME'
# will consistently raise a RuntimeError exception, whereas 'EXCEPTION' will
# tailor the type of exception to the situation.
#
# CSPICE's other erract options are still supported, so programmers can continue
# to use CSPICE's error handling mechanism if they wish to.
#
# HANDLING OF ERROR FLAGS
#
# Many CSPICE functions bypass the library's own error handling mechanism;
# instead they return a status flag, sometimes called "found" or "ok", or an
# empty response to indicate failure. The cspyce module provides alternative
# options for these functions.
# 
# Within cspyce1, functions that return error flags have an alternative
# implementation with a suffix of "_error". This version uses the CSPICE/cspyce
# error handling mechanism instead.
#
# Note that most _error versions of functions have fewer return values than
# the associated non-error versions. The user should be certain which version is
# being used before interpreting the returned value(s).
#
# The cspyce1 module provides several ways to control which version of the
# function to use:
#
# - The function use_flags() takes a function name or list of names and
#   designates the original version of each function as the default. If the
#   input argument is missing.
#
# - The function use_errors() takes a function name or list of names and
#   designates the _error version of each function as the default. If the input
#   argument is missing, _error versions are selected universally. With this
#   option, for example, a call to cspyce1.bodn2c() will actuall call
#   cspyce1.bodn2c_error() instead.
#
# You can also close between the "flag" and "error" versions of a function using
# cspyce function attributes, as discussed below.
#
# FUNCTION ATTRIBUTES
#
# Like any other Python class, functions can have attributes. These are used to
# simplify the choices of function options in cspyce1. Every cspyce1 function
# has these attributes:
#
#   error   = the version of this function that raises errors intead of
#             returning flags.
#   flag    = the version that returns flags instead of raising errors.
#   vector  = the vectorized version of this function.
#   scalar  = the un-vectorized version of this function.
#
# If a particular option is not relevant to a function, the attribute still
# exists, and instead simply returns the function itself. This makes it trivial
# to choose a particular combination of features for a particular function call.
# For example:
#   ckgpav.vector()         ckgpav_vector()
#   ckgpav.vector.flag()    ckgpav_vector()
#   ckgpav.vector.error()   ckgpav_vector_error()
#   ckgpav.error.scalar()   ckgpav_error()
#   ckgpav.flag()           ckgpav()
#   bodn2c.vector()         bodn2c()
#   bodn2c.flag()           bodn2c()
#
################################################################################

import sys
import os
import numpy as np
import textwrap

import cspyce.cspyce0 as cspyce0
from cspyce.cspyce0 import *

from cspyce.cspyce_info import \
    CSPYCE_SIGNATURES, CSPYCE_ARGNAMES, CSPYCE_DEFAULTS, \
    CSPYCE_RETURNS, CSPYCE_RETNAMES, CSPYCE_DEFINITIONS, \
    CSPYCE_ABSTRACT, CSPYCE_PS, CSPYCE_URL

# Global variables used below
import __main__
INTERACTIVE = not hasattr(__main__, '__file__');
CSPYCE_ERRACT = 'EXCEPTION'         # A local copy of the requested erract.

################################################################################
# GET/SET handling
################################################################################

def erract(op, action):
    """Internal to CSPICE, action is always 'EXCEPTION', 'RUNTIME' or 'RETURN'
    in interactive mode."""

    global INTERACTIVE, CSPYCE_ERRACT

    traceback_name = 'erract_wrapper'

    # Clear an existing error first
    if failed(): return None

    # GET...
    op = op.upper().strip()
    if op == 'GET':
        return CSPYCE_ERRACT

    # SET...
    if op == 'SET':
        chkin(traceback_name)

        cspyce0.erract('SET', action)
        if failed():
            chkout(traceback_name)
            return

        # Save a local copy of the erract value
        CSPYCE_ERRACT = cspyce0.erract('GET', '')

        # In interactive mode, override certain modes internally
        if INTERACTIVE and CSPYCE_ERRACT in ('ABORT', 'DEFAULT'):
            cspyce0.erract('SET', 'RETURN')

        chkout(traceback_name)
        return CSPYCE_ERRACT

    # If it's not a recognized op, maybe it's an action and 'SET' is assumed
    # This call is recursive.
    else:
        return erract('SET', op)

def errdev(op, device):
    """Special argument handling."""

    traceback_name = 'errdev_wrapper'

    # GET or SET...
    cleaned_op = op.upper().strip()
    if cleaned_op in ('GET', 'SET'):
        chkin(traceback_name)
        result = cspyce0.errdev(op, device)
        chkout(traceback_name)
        return result

    # Try implied set (using recursive call)
    if device.strip() == '':
        return errdev('SET', op)

    # Otherwise, let default error handling take over
    chkin(traceback_name)
    result = cspyce0.errdev(op, device)
    chkout(traceback_name)
    return result

def errprt(op, list):
    """Special argument handling."""

    traceback_name = 'errprt_wrapper'

    # GET or SET...
    op = op.upper().strip()
    if op in ('GET', 'SET'):
        chkin(traceback_name)
        result = cspyce0.errprt(op, list)
        chkout(traceback_name)
        return result

    # Try implied set (using recursive call)
    if list.strip() == '':
        chkin(traceback_name)
        result = cspyce0.errprt('SET', op)
        chkout(traceback_name)
        return result

    # Otherwise, let default error handling take over
    chkin(traceback_name)
    result = cspyce0.errprt(op, list)
    chkout(traceback_name)
    return result

def timdef(action, item='', value=''):
    """Special argument handling."""

    traceback_name = 'timdef_wrapper'

    # GET or SET...
    action = action.upper().strip()
    if action in ('GET', 'SET'):
        chkin(traceback_name)
        result = cspyce0.timdef(action, item, value)
        chkout(traceback_name)
        return result

    # Try implied set or get
    if value == '':
        if action in ('CALENDAR', 'SYSTEM', 'ZONE'):
            chkin(traceback_name)
            if item:
                result = cspyce0.timdef('SET', action, item)
            else:
                result = cspyce0.timdef('GET', action, ' ')

            chkout(traceback_name)
            return result

    # Otherwise, let default error handling take over
    chkin(traceback_name)
    result = cspyce0.timdef(action, item, value)
    chkout(traceback_name)
    return result

################################################################################
# Define _error versions of functions that raise error conditions rather than
# return status flags.
#
# The code is written to work regardless of the type of error handling in use.
################################################################################

def bodc2n_error(code):
    (name, found) = cspyce0.bodc2n(code)
    if not found:
        chkin('bodc2n_error')
        setmsg('body code %s not found in kernel pool' % code)
        sigerr('SPICE(BODYIDNOTFOUND)')
        chkout('bodc2n_error')

    return name

def bodn2c_error(name):
    (code, found) = cspyce0.bodn2c(name)
    if not found:
        chkin('bodn2c_error')
        setmsg('body name "%s" not found in kernel pool' % name)
        sigerr('SPICE(BODYNAMENOTFOUND)')
        chkout('bodn2c_error')

    return code

def bods2c_error(name):
    (code, found) = cspyce0.bods2c(name)
    if not found:
        chkin('bods2c_error')
        setmsg('body name "%s" not found in kernel pool' % name)
        sigerr('SPICE(BODYNAMENOTFOUND)')
        chkout('bods2c_error')

    return code

def ccifrm_error(frclss, clssid):
    (frcode, frname, center, found) = cspyce0.ccifrm(frclss, clssid)
    if not found:
        chkin('ccifrm_error')
        setmsg('unrecognized frame description: class %s; ' % frclss +
               'class id %s' % clssid)
        sigerr('SPICE(INVALIDFRAMEDEF)')
        chkout('ccifrm_error')

    return [frcode, frname, center]

def cidfrm_error(code):
    (frcode, name, found) = cspyce0.cidfrm(code)
    if not found:
        chkin('cidfrm_error')
        setmsg('body code %s not found in kernel pool' % code)
        sigerr('SPICE(BODYIDNOTFOUND)')
        chkout('cidfrm_error')

    return [frcode, name]

def ckcov_error(ck, idcode, needav, level, tol, timsys):
    coverage = cspyce0.ckcov(ck, idcode, needav, level, tol, timsys)
    if coverage.size == 0:
        chkin('ckcov_error')
        setmsg('body code %s not found in C kernel file %s' % (idcode, ck))
        sigerr('SPICE(BODYIDNOTFOUND)')
        chkout('ckcov_error')

    return coverage

def ckgp_error(inst, sclkdp, tol, ref):
    (cmat, clkout, found) = cspyce0.ckgp(inst, sclkdp, tol, ref)
    if not found:
        name = cspyce0.frmnam(inst)
        if name:
            namestr = ' (' + name + ')'
        else:
            namestr = ''

        chkin('ckgp_error')
        setmsg('insufficient C kernel data to evaluate ' +
               'instrument/spacecraft %s%s ' % (inst, namestr) +
               'at spacecraft clock time %s ' % sclkdp +
               'with tolerance %s' % tol)
        sigerr('SPICE(CKINSUFFDATA)')
        chkout('ckgp_error')

    return [cmat, clkout]

def ckgpav_error(inst, sclkdp, tol, ref):
    (cmat, av, clkout, found) = cspyce0.ckgpav(inst, sclkdp, tol, ref)
    if not found:
        name = cspyce0.frmnam(inst)
        if name:
            namestr = ' (' + name + ')'
        else:
            namestr = ''

        chkin('ckgpav_error')
        setmsg('insufficient C kernel data to evaluate ' +
               'instrument/spacecraft %s%s ' % (inst, namestr) +
               'at spacecraft clock time %s ' % sclkdp +
               'with tolerance %s' % tol)
        sigerr('SPICE(CKINSUFFDATA)')
        chkout('ckgpav_error')

    return [cmat, av, clkout]

def cnmfrm_error(cname):
    (frcode, frname, found) = cspyce0.cnmfrm(cname)
    if not found:
        chkin('cnmfrm_error')
        setmsg('body name "%s" not found in kernel pool' % cname)
        sigerr('SPICE(BODYNAMENOTFOUND)')
        chkout('cnmfrm_error')

    return [frcode, frname]

def dtpool_error(name):
    (found, n, vtype) = cspyce0.dtpool(name)
    if not found:
        chkin('dtpool_error')
        setmsg('pool variable "%s" not found' % name)
        sigerr('SPICE(VARIABLENOTFOUND)')
        chkout('dtpool_error')

    return [n, vtype]

def frinfo_error(frcode):
    (cent, frclss, clssid, found) = cspyce0.frinfo(frcode)
    if not found:
        chkin('frinfo_error')
        setmsg('frame code %s not found in kernel pool' % frcode)
        sigerr('SPICE(FRAMEIDNOTFOUND)')
        chkout('frinfo_error')

    return [cent, frclss, clssid]

def frmnam1_error(frcode):  # change of name; frmnam_error is defined below
    frname = cspyce0.frmnam(frcode)
    if frname == '':
        chkin('frmnam_error')
        setmsg('frame code %s not found' % frcode)
        sigerr('SPICE(FRAMEIDNOTFOUND)')
        chkout('frmnam_error')

    return frname

def gcpool_error(name, start=0):
    (cvals, found) = cspyce0.gcpool(name, start)
    if not found:
        [ok, count, nctype] = cspyce0.dtpool(name)
        if not ok:
            chkin('gcpool_error')
            setmsg('pool variable "%s" not found' % name)
            sigerr('SPICE(VARIABLENOTFOUND)')
            chkout('gcpool_error')
            return []

    [ok, count, nctype] = cspyce0.dtpool(name)
    if nctype != 'C':
        chkin('gcpool_error')
        setmsg('string information not available; '
               'kernel pool variable "%s" has numeric values' % name)
        sigerr('SPICE(WRONGDATATYPE)')
        chkout('gcpool_error')
        return []

    if start > count:
        chkin('gcpool_error')
        setmsg('kernel pool has only %s ' % count +
               'values for variable "%s";' % name +
               'start index value %s is too large' % start)
        sigerr('SPICE(INDEXOUTOFRANGE)')
        chkout('gcpool_error')
        return []

    return cvals

def gdpool_error(name, start=0):
    (values, found) = cspyce0.gdpool(name, start)
    if not found:
        [ok, count, nctype] = cspyce0.dtpool(name)
        if not ok:
            chkin('gdpool_error')
            setmsg('pool variable "%s" not found' % name)
            sigerr('SPICE(VARIABLENOTFOUND)')
            chkout('gdpool_error')
            return []

    [ok, count, nctype] = cspyce0.dtpool(name)
    if nctype != 'N':
        chkin('gdpool_error')
        setmsg('numeric values are not available; '
               'kernel pool variable "%s" has string values' % name)
        sigerr('SPICE(WRONGDATATYPE)')
        chkout('gdpool_error')
        return []

    if start > count:
        chkin('gdpool_error')
        setmsg('kernel pool has only %s ' % count +
               'values for variable "%s";' % name +
               'start index value %s is too large' % start)
        sigerr('SPICE(INDEXOUTOFRANGE)')
        chkout('gdpool_error')
        return []

    return values

def gipool_error(name, start=0):
    (ivals, found) = cspyce0.gipool(name, start)
    if not found:
        [ok, count, nctype] = cspyce0.dtpool(name)
        if not ok:
            chkin('gipool_error')
            setmsg('pool variable "%s" not found' % name)
            sigerr('SPICE(VARIABLENOTFOUND)')
            chkout('gipool_error')
            return []

    [ok, count, nctype] = cspyce0.dtpool(name)
    if nctype != 'N':
        chkin('gipool_error')
        setmsg('numeric values are not available; '
               'kernel pool variable "%s" has string values' % name)
        sigerr('SPICE(WRONGDATATYPE)')
        chkout('gipool_error')
        return []

    if start > count:
        chkin('gipool_error')
        setmsg('kernel pool has only %s ' % count +
               'values for variable "%s";' % name +
               'start index value %s is too large' % start)
        sigerr('SPICE(INDEXOUTOFRANGE)')
        chkout('gipool_error')
        return []

    return ivals

def gnpool_error(name, start=0):
    (kvars, found) = cspyce0.gnpool(name, 0)
    if not found:
        chkin('gnpool_error')
        setmsg('no kernel pool variables found matching template "%s"' % name)
        sigerr('SPICE(VARIABLENOTFOUND)')
        chkout('gnpool_error')
        return []

    if start > len(kvars):
        setmsg('kernel pool has only %s ' % count +
               'variables matching template "%s";' % name +
               'start index value %s is too large' % start)
        sigerr('SPICE(INDEXOUTOFRANGE)')
        chkout('gnpool_error')
        return []

    return kvars[start:]

def namfrm1_error(frname):  # change of name; namfrm_error is defined below
    frcode = cspyce0.namfrm(frname)
    if frcode == 0:
        chkin('namfrm_error')
        setmsg('frame name %s not found in kernel pool' % frname)
        sigerr('SPICE(FRAMENAMENOTFOUND)')
        chkout('namfrm_error')

    return frcode

def pckcov_error(pck, code):
    coverage = cspyce0.pckcov(pck, code)
    if coverage.size == 0:
        chkin('pckcov_error')
        setmsg('frame code %s not found in binary PC kernel file %s' % (code,
                                                                       pck))
        sigerr('SPICE(FRAMEIDNOTFOUND)')
        chkout('pckcov_error')

    return coverage

def spkcov_error(spk, code):
    coverage = cspyce0.spkcov(spk, code)
    if coverage.size == 0:
        chkin('spkcov_error')
        setmsg('body code %s not found in SP kernel file %s' % (code, spk))
        sigerr('SPICE(BODYIDNOTFOUND)')
        chkout('spkcov_error')

    return coverage

def srfc2s_error(code, bodyid):
    (srfstr, isname) = cspyce0.srfc2s(code, bodyid)
    if not isname:
        chkin('srfc2s_error')
        setmsg('surface for %s/%s not found' % (code, bodyid))
        sigerr('SPICE(NOTRANSLATION)')
        chkout('srfc2s_error')

    return srfstr

def srfcss_error(code, bodstr):
    (srfstr, isname) = cspyce0.srfcss(code, bodstr)
    if not isname:
        chkin('srfcss_error')
        setmsg('surface for %s/"%s" not found' % (code, bodstr))
        sigerr('SPICE(NOTRANSLATION)')
        chkout('srfcss_error')

    return srfstr

def srfs2c_error(srfstr, bodstr):
    (code, found) = cspyce0.srfs2c(srfstr, bodstr)
    if not found:
        chkin('srfs2c_error')
        setmsg('surface for "%s"/"%s" not found' % (srfstr, bodstr))
        sigerr('SPICE(NOTRANSLATION)')
        chkout('srfs2c_error')

    return code

def srfscc_error(srfstr, bodyid):
    (code, found) = cspyce0.srfscc(srfstr, bodyid)
    if not found:
        chkin('srfscc_error')
        setmsg('"%s"/%s not found' % (srfstr, bodyid))
        sigerr('SPICE(NOTRANSLATION)')
        chkout('srfscc_error')

    return code

def stpool_error(item, nth, contin):
    (string, found) = cspyce0.stpool(item, nth, contin)
    if not found:
        [ok, count, nctype] = cspyce0.dtpool(name)
        if not ok:
            chkin('stpool_error')
            setmsg('pool variable "%s" not found' % name)
            sigerr('SPICE(VARIABLENOTFOUND)')
            chkout('stpool_error')
            return ''

        if nth != 0:
            (_, ok) = cspyce0.stpool(item, 0, contin)
            if ok:
                chkin('stpool_error')
                setmsg('index too large; '
                       'kernel pool has fewer than %s ' % nth +
                       'strings matching name "%s" ' % item +
                       'and continuation "%s"' % contin)
                sigerr('SPICE(INDEXOUTOFRANGE)')
                chkout('stpool_error')
                return ''

    [ok, count, nctype] = cspyce0.dtpool(item)
    if nctype != 'C':
        setmsg('string values are not available; '
               'kernel pool variable "%s" has numeric values' % item)
        sigerr('SPICE(WRONGDATATYPE)')
        chkout('stpool_error')
        return ''

    return string

def tparse_error(string):
    (sp2000, msg) = cspyce0.tparse(string)
    if msg:
        chkin('tparse_error')
        setmsg(msg)
        sigerr('SPICE(INVALIDTIMESTRING)')
        chkout('tparse_error')

    return sp2000

def tpictr_error(string):
    (pictur, ok, msg) = cspyce0.tpictr(string)
    if not ok:
        chkin('tpictr_error')
        setmsg(msg)
        sigerr('SPICE(INVALIDTIMESTRING)')
        chkout('tpictr_error')

    return pictur

#### These functions are both vectorized and have _error versions

def ckgp_vector_error(inst, sclkdp, tol, ref):
    (cmat, clkout, found) = cspyce0.ckgp_vector(inst, sclkdp, tol, ref)
    if not np.all(found):
        name = cspyce0.frmnam(inst)
        if name:
            namestr = ' (' + name + ')'
        else:
            namestr = ''

        sclkdp_min = np.min(sclkdp)
        sclkdp_max = np.max(sclkdp)
        if sclkdp_min == sclkdp_max:
            clockstr = str(sclkdp)
        else:
            clockstr = '%s to %s' % (sclkdp_min, sclkdp_max)

        chkin('ckgp_vector_error')
        setmsg('insufficient C kernel data to evaluate ' +
               'instrument/spacecraft %s%s ' % (inst, namestr) +
               'at spacecraft clock times %s ' % clockstr +
               'with tolerance %s' % np.min(tol))
        sigerr('SPICE(CKINSUFFDATA)')
        chkout('ckgp_vector_error')

    return [cmat, clkout]

def ckgpav_vector_error(inst, sclkdp, tol, ref):
    (cmat, av, clkout, found) = cspyce0.ckgpav_vector(inst, sclkdp, tol, ref)
    if not np.all(found):
        raise ValueError('Error in ckgpav_vector(): C matrix not found')

    return [cmat, av, clkout]

def ckgpav_vector_error(inst, sclkdp, tol, ref):
    (cmat, av, clkout, found) = cspyce0.ckgpav_vector(inst, sclkdp, tol, ref)
    if not np.all(found):
        name = cspyce0.frmnam(inst)
        if name:
            namestr = ' (' + name + ')'
        else:
            namestr = ''

        sclkdp_min = np.min(sclkdp)
        sclkdp_max = np.max(sclkdp)
        if sclkdp_min == sclkdp_max:
            clockstr = str(sclkdp)
        else:
            clockstr = '%s to %s' % (sclkdp_min, sclkdp_max)

        chkin('ckgpav_vector_error')
        setmsg('insufficient C kernel data to evaluate ' +
               'instrument/spacecraft %s%s ' % (inst, namestr) +
               'at spacecraft clock times %s ' % clockstr +
               'with tolerance %s' % np.min(tol))
        sigerr('SPICE(CKINSUFFDATA)')
        chkout('ckgpav_vector_error')

    return [cmat, av, clkout]

def invert_error(m1):
    inverse = cspyce0.invert(m1)
    if np.all(inverse == 0.):
        chkin('invert_error')
        setmsg('singular matrix encountered; inverse failed')
        sigerr('SPICE(SINGULARMATRIX)')
        chkout('invert_error')

    return inverse

def invert_vector_error(m1):
    inverses = cspyce0.invert_vector(m1)
    tests = np.all(inverses == 0., (-2,-1))
    if np.any(tests):
        chkin('invert_error')
        setmsg('singular matrix encountered; inverse failed')
        sigerr('SPICE(SINGULARMATRIX)')
        chkout('invert_error')

    return inverses

################################################################################
# Prepare for the possible use of aliases
################################################################################

FRAME_CODE_OVERRIDES = {}
FRAME_NAME_OVERRIDES = {}

def _name_as_key(name):
    """Uppercase, stripped, no repeated interior whitespace."""

    name = name.upper().strip()
    while '  ' in name:
        name = name.replace('  ', ' ')

    return name

def frmnam(frcode):
    return FRAME_NAME_OVERRIDES.get(frcode, cspyce0.frmnam(frcode))

def frmnam_error(frcode):
    return FRAME_NAME_OVERRIDES.get(frcode, frmnam1_error(frcode))

def namfrm(frname):
    return FRAME_CODE_OVERRIDES.get(_name_as_key(frname), cspyce0.namfrm(frname))

def namfrm_error(frname):
    return FRAME_CODE_OVERRIDES.get(_name_as_key(frname), namfrm1_error(frname))

################################################################################
# Assign support information about each function:
#   ABSTRACT    = a brief description of what the function does, formatted
#                 and wrapped at 72-column width. It should start and end with
#                 a newline.
#   SIGNATURE   = a list indicating the type of each argument
#   ARGNAMES    = a list of names of the input arguments
#   RETURNS     = a list indicating the type of each return value
#   RETNAMES    = a list of names of the return values
#   URL         = a URL for more information
#   PS          = an optional, final note.
#   DEFINITIONS = a dictionary describing each input and return values.
#   NOTES       = a list of one or more note strings, each formatted and
#                 wrapped at 72-column width. It should start and end with a
#                 newline.
#
# Note that the docstring and defaults will be constructed from this
# information.
################################################################################

def assign_docstring(func, note=""):
    """Assign a docstring to a cspyce function.

    An optional additional note string can provide version information. It must
    be pre-formatted, wrapped at 72 columns, and begin and end with a newline.
    """

    doclist = [func.ABSTRACT, '\n']

    if func.URL:
        doclist += [func.URL, '\n']

    if note:
        # We need to copy the note list so as not to affect other versions using
        # the same note list.
        func.NOTES = list(func.NOTES) + [note]

    doclist += func.NOTES

    lname = 0
    names = []
    for name in func.ARGNAMES + func.RETNAMES:
        lname = max(lname, len(name))
        names.append(name)

    ltype = 0
    types = []
    for type in func.SIGNATURE + func.RETURNS:
        type = type.replace('time','float').replace('rotmat','float')
        type = type.replace('body_code','int').replace('body_name','string')
        type = type.replace('frame_code','int').replace('frame_name','string')
        ltype = max(ltype, len(type))
        types.append(type)

    indent = 2 + ltype + 1 + lname + 3
    ldefs = 72 - indent
    tabstr = indent * ' '

    inputs = len(func.ARGNAMES)
    doclist += ['\nInputs:']
    if inputs == 0:
        doclist += [' none\n']
    else:
        doclist += ['\n']

    for (name, type) in zip(names[:inputs], types[:inputs]):
        desc = textwrap.wrap(func.DEFINITIONS[name], ldefs)
        doclist += ['  ', type, (ltype - len(type))*' ', ' ']
        doclist += [name, (lname - len(name))*' ', ' = ']
        doclist += [desc[0], '\n']
        for k in range(1, len(desc)):
            doclist += [tabstr, desc[k], '\n']

    doclist += ['\nReturns:']
    if len(func.RETNAMES) == 0:
        doclist += [' none\n']
    else:
        doclist += ['\n']

    for (name, type) in zip(names[inputs:], types[inputs:]):
        desc = textwrap.wrap(func.DEFINITIONS[name], ldefs)
        doclist += ['  ', type, (ltype - len(type))*' ', ' ']
        doclist += [name, (lname - len(name))*' ', ' = ']
        doclist += [desc[0], '\n']
        for k in range(1, len(desc)):
            doclist += [tabstr, desc[k], '\n']

    if func.PS:
        ps = textwrap.wrap('Note: ' + func.PS)
        doclist += ['\n', '\n'.join(ps)]

    doclist += ['\n']

    func.__doc__ = ''.join(doclist)

# Non-vector functions
for name in CSPYCE_SIGNATURES:
    func = globals()[name]
    func.ABSTRACT  = CSPYCE_ABSTRACT[name]
    func.SIGNATURE = CSPYCE_SIGNATURES[name]
    func.ARGNAMES  = CSPYCE_ARGNAMES[name]
    func.RETURNS   = CSPYCE_RETURNS[name]
    func.RETNAMES  = CSPYCE_RETNAMES[name]
    func.PS        = CSPYCE_PS.get(name, '')
    func.URL       = CSPYCE_URL.get(name, '')
    func.NOTES     = []
    func.DEFINITIONS = CSPYCE_DEFINITIONS[name]

    if name in CSPYCE_DEFAULTS:
        func.func_defaults = tuple(CSPYCE_DEFAULTS[name])

    assign_docstring(func)

# This is a set of every unique cspyce function's basename (before any suffix)
CSPYCE_BASENAMES = {n for n in CSPYCE_ABSTRACT.keys() if not n.endswith('_error')}

################################################################################
# Assign docstrings, signatures, etc. to the _vector functions
################################################################################

# type -> (type for input, type for output)
VECTORIZED_ARGS = {
    'time'       : ('time[*]'      , 'time[*]'      ),
    'float'      : ('float[*]'     , 'float[*]'     ),
    'float[2]'   : ('float[*,2]'   , 'float[*,2]'   ),
    'float[3]'   : ('float[*,3]'   , 'float[*,3]'   ),
    'float[4]'   : ('float[*,4]'   , 'float[*,4]'   ),
    'float[6]'   : ('float[*,6]'   , 'float[*,6]'   ),
    'float[8]'   : ('float[*,8]'   , 'float[*,8]'   ),
    'float[9]'   : ('float[*,9]'   , 'float[*,9]'   ),
    'float[2,2]' : ('float[*,2,2]' , 'float[*,2,2]' ),
    'float[3,3]' : ('float[*,3,3]' , 'float[*,3,3]' ),
    'float[6,6]' : ('float[*,6,6]' , 'float[*,6,6]' ),
    'rotmat[3,3]': ('rotmat[*,3,3]', 'rotmat[*,3,3]'),
    'rotmat[6,6]': ('rotmat[*,6,6]', 'rotmat[*,6,6]'),
    'int'        : ('int'          , 'int[*]'       ),
    'bool'       : ('bool'         , 'bool[*]'      ),
}

def _vectorize_signature(signature):
    """Convert a scalar signature to a vectorized signature."""
    return _vectorize_arglist(signature, 0)

def _vectorize_return(returns):
    """Convert a scalar return list to a vectorized return list."""
    return _vectorize_arglist(returns, 1)

def _vectorize_arglist(arglist, k):
    vectorized = []
    for arg in arglist:
        if arg in VECTORIZED_ARGS:
            vectorized.append(VECTORIZED_ARGS[arg][k])
        else:
            vectorized.append(arg)

    return vectorized

VECTOR_NOTE = """
In this vectorized version, any or all of the floating-point inputs can
have an extra leading dimension. The function will loop over this axis
and return arrays of the results. If no inputs have an extra dimension,
it returns results identical to the un-vectorized version.
"""

for basename in CSPYCE_BASENAMES:
    for suffix in ('', '_error'):
        vname = basename + '_vector' + suffix
        if vname not in globals(): continue

        name = basename + suffix
        func = globals()[name]
        vfunc = globals()[vname]

        vfunc.ABSTRACT  = func.ABSTRACT
        vfunc.SIGNATURE = _vectorize_signature(func.SIGNATURE)
        vfunc.ARGNAMES  = func.ARGNAMES
        vfunc.RETURNS   = _vectorize_signature(func.RETURNS)
        vfunc.RETNAMES  = func.RETNAMES
        vfunc.PS        = func.PS
        vfunc.URL       = func.URL
        vfunc.DEFINITIONS = func.DEFINITIONS
        vfunc.NOTES     = func.NOTES

        assign_docstring(vfunc, VECTOR_NOTE)

################################################################################
# Register _flag, _error, _scalar, and _vector versions of every function.
################################################################################

# The only options are:
#   func == func_error == func_vector
#   func == func_error != func_vector
#   func == func_vector != func_error
#   func != func_vector != func_error != func_vector_error

for name in CSPYCE_BASENAMES:
    ename  = name + '_error'
    vname  = name + '_vector'
    vename = name + '_vector_error'

    # Get up to four versions of the function
    func   = globals()[name]
    efunc  = globals().get(ename, func)
    vfunc  = globals().get(vname, func)

    if vename in globals():
        vefunc = globals()[vename]
    elif vfunc is func:
        vefunc = efunc
    elif efunc is func:
        vefunc = vfunc
    else:
        vefunc = func

    # Define them globally. They may already be defined, in which case this is
    # a harmless operation
# DISABLED! It creates too many symbols for the global dictionary
#     globals()[ ename] =  efunc
#     globals()[ vname] =  vfunc
#     globals()[vename] = vefunc

    # Define the links between the different versions.
    func.flag   =  func
    func.error  = efunc
    func.vector = vfunc
    func.scalar =  func

    efunc.flag   =   func
    efunc.error  =  efunc
    efunc.vector = vefunc
    efunc.scalar =  efunc

    vfunc.flag   =  vfunc
    vfunc.error  = vefunc
    vfunc.vector =  vfunc
    vfunc.scalar =   func

    vefunc.flag   =  vfunc
    vefunc.error  = vefunc
    vefunc.vector = vefunc
    vefunc.scalar =  efunc

    # Define the alternative names for these functions
# DISABLED! It creates too many symbols for the global dictionary
#     fname  = name + '_flag'
#     sname  = name + '_scalar'
#     sfname = name + '_scalar_flag'
#     sename = name + '_scalar_error'
#     vfname = name + '_vector_flag'
# 
#     globals()[ fname] =  func
#     globals()[ sname] =  func
#     globals()[sfname] =  func
#     globals()[sename] = efunc
#     globals()[vfname] = vfunc

################################################################################
# Set defaults at initialization
################################################################################

erract('SET', 'EXCEPTION')

################################################################################
