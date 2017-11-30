################################################################################
# cspice/cspice2/__init__.py
################################################################################
# PDS RMS Node CSPICE-Python interface
# Library cspice2
#
# This version of the Python/CSPICE interface overlays many useful capabilities
# on the lower-level cspice1 module.
#
# This library provides a Python interface to all the primary functions of the
# CSPICE library. It does not provide an interface to lower-level functions that
# a typical user is not likely to use directly.
#
# This library inherits all of the features of cspice1, including:
# - All functions have informative docstrings.
# - Sensible default values for some missing arguments.
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
# - For every function, whether this feature is relevant or not, a function
#   with the same name but an "_error" suffix will suppress any status flags
#   and instead raise a Python error condition, typically KeyError.
# - For every function, whether this feature is relevant or not, a function
#   with the same name but a "_flag" suffix will perform the default behavior.

#
# You can use these functions to switch the default behavior of any of these
# functions.
#   use_exceptions_not_flags(names)
#   use_flags_not_exceptions(names)
#
# You can also obtain one of these versions using these functions, which return
# functions:
#   exception_version(func)
#   flag_version(func)
#
# Before calling a function, you select the set of rules to follow.
#
# rules = select_rules(type_handler, spice_id_handler=None, vectorized=None):
#
# type_handler =
#   None or 'none'  no type checking of input args is performed.
#   'check'         raises an exception of an arg is of the wrong type.
#   'convert'       tries to convert each argument to the required type.
# 
# spice_id_handler =
#   None            uses the above type handler for SPICE numeric codes and
#                   names.
#   'none'          no type checking of SPICE ID input args is performed.
#   'check'         raises an exception of an arg is of the wrong type.
#   'convert'       tries to convert each argument to the required type.
#   'translate'     translates between SPICE codes and SPICE names, depending
#                   on what the function expects.
#   'aliases'       supports the local alias capability, where a body can have
#                   multiple names or multiple SPICE IDs (typically due to
#                   historic changes).
#
# vectorized =
#   None            no vectorization is supported; input arrays must have the
#                   exact shape that the function expects.
#   'vectorized'    arrays may have additional dimensions to the left of the
#                   shape required for the function. All arrays with additional
#                   dimensions have these dimensions broadcasted together, and
#                   arrays of results are returned.
#
# After defining a set of rules,
#   exec_with_rules(func, rules, args)
#                   will perform the function as requested.
#
#   rules_version(func, rules)
#                   returns a version of the function for which these rules will
#                   be applied by default.
#
#   apply_rules(rules, names)
#                   will force subsequent calls to the functions to use these
#                   rules by default. The default rules can be specified on a
#                   function-by-function basis and can be changed at any time.
#
# November 2017
################################################################################

import re
import numpy as np
import cspice1

SPICE_DOCSTRINGS = cspice1.SPICE_DOCSTRINGS.copy()
SPICE_SIGNATURES = cspice1.SPICE_SIGNATURES.copy()
SPICE_RETURNS    = cspice1.SPICE_RETURNS.copy()
SPICE_DEFAULTS   = cspice1.SPICE_DEFAULTS.copy()

# Create a copy of each cspice1 function with new rules to follow
def apply_default_rules(func):
    def wrapper(*args):
        return exec_with_rules(func, func.RULES, *args)
    return wrapper

cspice1_dict = cspice1.__dict__
for key in SPICE_SIGNATURES:

    func1 = cspice1_dict[key]
    func1.RULES = None

    func2 = apply_default_rules(func1)

    func2.__name__ = key
    func2.__doc__  = func1.__doc__
    func2.func_defaults = func1.func_defaults

    func2.SIGNATURE = func1.SIGNATURE
    func2.RETURNS   = func1.RETURNS
    func2.RULES     = func1.RULES
    globals()[key]  = func2

# Save a function *_flag and for every function with a *_error version
# Save a global list of function names and also one with _error versions
CSPICE_FUNC_NAMES = []
ERROR_FUNC_NAMES = []
for key in SPICE_SIGNATURES:
    if not key.endswith('_error'):
        if not key.endswith('_flag'):
            CSPICE_FUNC_NAMES.append(key)
        continue

    short_key = key[:-6]
    func2 = globals()[short_key]

    flag_key = short_key + '_flag'
    globals()[flag_key] = func2

    SPICE_DOCSTRINGS[flag_key] = SPICE_DOCSTRINGS[short_key]
    SPICE_SIGNATURES[flag_key] = SPICE_SIGNATURES[short_key]
    SPICE_RETURNS   [flag_key] = SPICE_RETURNS[short_key]

    if short_key in SPICE_DEFAULTS:
        SPICE_DEFAULTS[flag_key] = SPICE_DEFAULTS[short_key]

    ERROR_FUNC_NAMES.append(short_key)

CSPICE_FUNC_NAMES.sort()
ERROR_FUNC_NAMES.sort()
ALL_FUNC_NAMES = SPICE_SIGNATURES.keys()
ALL_FUNC_NAMES.sort()

################################################################################
################################################################################
################################################################################
# Alias support
#
# Alternative versions of boddef, bods2n, bodc2n, bodc2s, and bodn2c that
# support multiple codes and/or multiple names used for the same body.
################################################################################

# Global dictionaries to track aliases
CODE_ALIASES = {}
NAME_ALIASES = {}

_VERSION_REGEX = re.compile('.* V[0-9]+$')

# Identify the functions that have _alias versions
ALIAS_FUNC_NAMES = ['boddef', 'bodn2c', 'bodc2n', 'bodc2s', 'bods2c']

def _clean_name(name):
    """Convert name to upper case and replace duplicated spaces with one."""

    name = name.upper().strip()
    while ('  ' in name):
        name = name.replace('  ', ' ')

    return name

def _boddef_for_aliases(names, codes):
    """Define one or more names or codes that are aliases for the same body."""

    if type(names) == str:
        names = [names]

    names = [_clean_name(n) for n in names]

    if type(codes) == int:
        codes = [codes]

    # Expand the set of associated names and codes
    while True:
        more_names = []
        more_codes = []
        for c in codes:
            extra_names = _bodc2n_for_aliases(c)
            for n in extra_names:
                if n not in names and n not in more_names:
                    more_names.append(n)

        for n in names + more_names:
            extra_codes = _bodn2c_for_aliases(n)
            for c in extra_codes:
                if c not in codes and c not in more_codes:
                    more_codes.append(c)

        if len(more_names) == 0 and len(more_codes) == 0:
            break

        names += more_names
        codes += more_codes

    # We require at least as many names as codes, so we can cover all cases
    # when a function expects a name

    # Remove versioned names (ending with " Vn" for integer n)
    unversioned_names = []
    for n in names:
        if _VERSION_REGEX.match(n) is None:
            unversioned_names.append(n)

    names = unversioned_names

    # Append versions of the first name in reverse order
    names = unversioned_names
    for k in range(len(codes) - len(names))[::-1]:
        names.append(names[0] + ' V%d' % k)

    # Save dicts of code and name lists, keyed by individual codes and names
    for x in codes + names:
        CODE_ALIASES[x] = codes
        NAME_ALIASES[x] = names

    # Now use the CSPICE mechanism for associating one name and one code
    for k in range(len(codes)):
        cspice1.boddef(names[k], codes[k])

def _bodc2n_for_aliases(code):
    """Return a list of names given a code"""

    if code in CODE_ALIASES:
        return NAME_ALIASES[code]

    (name, found) = cspice1.bodc2n_flag(code)
    if found:
        return [name]
    else:
        return []

def _bodc2s_for_aliases(code):
    """Return a list of names given a code. If no translation, convert the code
    to a string."""

    if code in CODE_ALIASES:
        return NAME_ALIASES[code]

    return [cspice1.bodc2s(code)]

def _bodn2c_for_aliases(name):
    """Return a list of codes given a name. Returned list may be empty."""

    name = _clean_name(name)
    if name in CODE_ALIASES:
        return CODE_ALIASES[name]

    (code, found) = cspice1.bodn2c_flag(name)
    if found:
        return [code]
    else:
        return []

def _bods2c_for_aliases(name):
    """Return a list of codes given a name. Returned list may be empty."""

    name = _clean_name(name)
    if name in CODE_ALIASES:
        return CODE_ALIASES[name]

    (code, found) = cspice1.bods2c_flag(name)
    if found:
        return [code]
    else:
        return []

############################################################
# Definitions of CSPICE functions with alias variants
############################################################

SPICE_SIGNATURES["boddef_aliases"] = ["string[*]", "int[*]"]
SPICE_RETURNS   ["boddef_aliases"] = []
SPICE_DOCSTRINGS["boddef_aliases"] = """
Define a body name/ID code pair for later translation via bodn2c or bodc2n.

This version also supports aliases. Specify an array/list/tuple of multiple
names or codes, and they will all be treated as equivalent.

boddef(<string> name, <int> code)

name = Common name of some body, or an aliased array, list or tuple of names.
code = Integer code for that body, or an aliased array, list or tuple of codes.
"""

def boddef_aliases(name, code):
    _boddef_for_aliases(name, code)

boddef_aliases.__doc__   = SPICE_DOCSTRINGS["boddef_aliases"]
boddef_aliases.SIGNATURE = SPICE_SIGNATURES["boddef_aliases"]
boddef_aliases.RETURNS   = SPICE_RETURNS   ["boddef_aliases"]

#########################################

SPICE_SIGNATURES["bodc2n_aliases"] = ["body_code"]
SPICE_RETURNS   ["bodc2n_aliases"] = ["string[*]", "bool"]
SPICE_DOCSTRINGS["bodc2n_aliases"] = """
Translate the SPICE integer code of a body into one or more common names for
that body.

bodc2n(<int> code) -> [(<string> or <string[*]>) name, <bool> found]

code  = Integer ID code to be translated into a name.
name  = One or more common names for the body identified by code.
found = True if translated, otherwise False.
"""

def bodc2n_aliases(code):
    results = _bodc2n_for_aliases(code)
    if len(results) == 0:
        return ['', False]

    if len(results) == 1:
        return [results[0], True]
    else:
        return [results, True]

bodc2n_aliases.__doc__   = SPICE_DOCSTRINGS["bodc2n_aliases"]
bodc2n_aliases.SIGNATURE = SPICE_SIGNATURES["bodc2n_aliases"]
bodc2n_aliases.RETURNS   = SPICE_RETURNS   ["bodc2n_aliases"]

#########################################

SPICE_SIGNATURES["bodc2n_aliases_error"] = ["body_code"]
SPICE_RETURNS   ["bodc2n_aliases_error"] = ["string[*]"]
SPICE_DOCSTRINGS["bodc2n_aliases_error"] = """
Translate the SPICE integer code of a body into one or more common names for
that body.

bodc2n(<int> code) -> (<string> or <string[*]>) name

code  = Integer ID code to be translated into a name.
name  = One or more common names for the body identified by code.

Raise KeyError if code cound not be translated.
"""

def bodc2n_aliases_error(code):
    results = _bodc2n_for_aliases(code)
    if len(results) == 0:
        raise KeyError('Error in bodc2n(): body code %d not found' % code)

    if len(results) == 1:
        return results[0]
    else:
        return results

bodc2n_aliases_error.__doc__   = SPICE_DOCSTRINGS["bodc2n_aliases_error"]
bodc2n_aliases_error.SIGNATURE = SPICE_SIGNATURES["bodc2n_aliases_error"]
bodc2n_aliases_error.RETURNS   = SPICE_RETURNS   ["bodc2n_aliases_error"]

#########################################

SPICE_SIGNATURES["bodc2s_aliases"] = ["body_code"]
SPICE_RETURNS   ["bodc2s_aliases"] = ["string[*]"]
SPICE_DOCSTRINGS["bodc2s_aliases"] = """
Translate a body ID code to either one or more corresponding names or, if no
name to ID code mapping exists, the string representation of the body ID value.

bodc2s(<int> code) -> (<string> or string[*]>) name

code = Integer ID code to translate to a string.
name = One or more strings corresponding to 'code'.
"""

def bodc2s_aliases(code):
    results = _bodc2s_for_aliases(code)
    if len(results) == 1:
        return results[0]
    else:
        return results

bodc2s_aliases.__doc__   = SPICE_DOCSTRINGS["bodc2s_aliases"]
bodc2s_aliases.SIGNATURE = SPICE_SIGNATURES["bodc2s_aliases"]
bodc2s_aliases.RETURNS   = SPICE_RETURNS   ["bodc2s_aliases"]

#########################################

SPICE_SIGNATURES["bodn2c_aliases"] = ["body_name"]
SPICE_RETURNS   ["bodn2c_aliases"] = ["int[*]", "bool"]
SPICE_DOCSTRINGS["bodn2c_aliases"] = """
Translate the name of a body or object to one or more corresponding SPICE
integer ID codes.

bodn2c(<string> name) -> [(<int> or <int[*]>) code, <bool> found]

name  = Body name to be translated into a SPICE ID code.
code  = One or more SPICE integer ID codes for the named body.
found = True if translated, otherwise False.
"""

def bodn2c_aliases(name):
    results = _bodn2c_for_aliases(code)
    if len(results) == 0:
        return [0, False]

    if len(results) == 1:
        return [results[0], True]
    else:
        return [results, True]

bodn2c_aliases.__doc__   = SPICE_DOCSTRINGS["bodn2c_aliases"]
bodn2c_aliases.SIGNATURE = SPICE_SIGNATURES["bodn2c_aliases"]
bodn2c_aliases.RETURNS   = SPICE_RETURNS   ["bodn2c_aliases"]

#########################################

SPICE_SIGNATURES["bodn2c_aliases_error"] = ["body_name"]
SPICE_RETURNS   ["bodn2c_aliases_error"] = ["int[*]"]
SPICE_DOCSTRINGS["bodn2c_aliases_error"] = """
Translate the name of a body or object to one or more corresponding SPICE
integer ID codes.

bodn2c(<string> name) -> (<int> or <int[*]>) code

name  = Body name to be translated into a SPICE ID code.
code  = One or more SPICE integer ID codes for the named body.

Raise KeyError if name cound not be translated.
"""

def bodn2c_aliases_error(name):
    results = _bodn2c_for_aliases(code)
    if len(results) == 0:
        name = _clean_name(name)
        raise KeyError('Error in bodn2c(): body name "%s" not found' % name)

    if len(results) == 1:
        return results[0]
    else:
        return results

bodn2c_aliases_error.__doc__   = SPICE_DOCSTRINGS["bodn2c_aliases_error"]
bodn2c_aliases_error.SIGNATURE = SPICE_SIGNATURES["bodn2c_aliases_error"]
bodn2c_aliases_error.RETURNS   = SPICE_RETURNS   ["bodn2c_aliases_error"]

#########################################

SPICE_SIGNATURES["bods2c_aliases"] = ["body_name"]
SPICE_RETURNS   ["bods2c_aliases"] = ["int[*]", "bool"]
SPICE_DOCSTRINGS["bods2c_aliases"] = """
Translate a string containing a body name or ID code to one or more integer
codes.

bods2c(<string> name) -> [(<int> or <int[*]>) code, <bool> found]

name  = String to be translated to an ID code.
code  = One or more integer ID codes corresponding to `name'.
found = True if translated, otherwise False.
"""

def bods2c_aliases(name):
    results = _bods2c_for_aliases(code)
    if len(results) == 0:
        return [0, False]

    if len(results) == 1:
        return [results[0], True]
    else:
        return [results, True]

bods2c_aliases.__doc__   = SPICE_DOCSTRINGS["bods2c_aliases"]
bods2c_aliases.SIGNATURE = SPICE_SIGNATURES["bods2c_aliases"]
bods2c_aliases.RETURNS   = SPICE_RETURNS   ["bods2c_aliases"]

#########################################

SPICE_SIGNATURES["bods2c_aliases_error"] = ["body_name"]
SPICE_RETURNS   ["bods2c_aliases_error"] = ["int[*]"]
SPICE_DOCSTRINGS["bods2c_aliases_error"] = """
Translate a string containing a body name or ID code to one or more integer
codes.

bods2c(<string> name) -> (<int> or <int[*]>) code

name  = String to be translated to an ID code.
code  = One or more integer ID codes corresponding to `name'.

Raise KeyError if name cound not be translated.
"""

def bods2c_aliases_error(name):
    results = _bods2c_for_aliases(code)
    if len(results) == 0:
        name = _clean_name(name)
        raise KeyError('Error in bods2c(): body name "%s" not found' % name)

    if len(results) == 1:
        return results[0]
    else:
        return results

bods2c_aliases_error.__doc__   = SPICE_DOCSTRINGS["bods2c_aliases_error"]
bods2c_aliases_error.SIGNATURE = SPICE_SIGNATURES["bods2c_aliases_error"]
bods2c_aliases_error.RETURNS   = SPICE_RETURNS   ["bods2c_aliases_error"]

################################################################################

# For every _aliases[_error] function above, define _noaliases[_error]
for name in ALIAS_FUNC_NAMES:
  for suffix in ('', '_error'):

    alias_key   = name + '_aliases'   + suffix
    short_key   = name +                suffix
    noalias_key = name + '_noaliases' + suffix

    if alias_key in globals():
        globals()[noalias_key] = globals()[short_key]
        SPICE_DOCSTRINGS[noalias_key] = SPICE_DOCSTRINGS[short_key]
        SPICE_SIGNATURES[noalias_key] = SPICE_SIGNATURES[short_key]
        SPICE_RETURNS   [noalias_key] = SPICE_RETURNS   [short_key]

# For every _[no]aliases_error function above, define _[no]aliases_flag
for name in ALIAS_FUNC_NAMES:
  for prefix in ('_aliases', '_noaliases'):

    error_key = name + prefix + '_error'
    short_key = name + prefix
    flag_key  = name + prefix + '_flag'

    if error_key in globals():
        globals()[flag_key] = globals()[short_key]
        SPICE_DOCSTRINGS[flag_key] = SPICE_DOCSTRINGS[short_key]
        SPICE_SIGNATURES[flag_key] = SPICE_SIGNATURES[short_key]
        SPICE_RETURNS   [flag_key] = SPICE_RETURNS   [short_key]

        ERROR_FUNC_NAMES.append(short_key)

ERROR_FUNC_NAMES.sort()

ALL_FUNC_NAMES = SPICE_SIGNATURES.keys()
ALL_FUNC_NAMES.sort()

################################################################################
################################################################################
################################################################################
# Version Management
################################################################################
# Methods to select between _aliases and _noaliases versions of functions
################################################################################

def _use_aliases(names=[]):
    """Switch all functions, or just those listed, to handle aliases."""

    if names:
        keys = [_strip_aliases(n) for n in names]
    else:
        keys = ALIAS_FUNC_NAMES

    for key in keys:
        key_plus = key + '_aliases'
        if key in globals() and key_plus in globals():
            globals()[key] = globals()[key_plus]

def _use_noaliases(names=[]):
    """Switch all functions, or just those listed, to ignore aliases."""

    if names:
        keys = [_strip_aliases(n) for n in names]
    else:
        keys = ALIAS_FUNC_NAMES

    for key in keys:
        key_plus = key + '_noaliases'
        if key in globals() and key_plus in globals():
            globals()[key] = globals()[key_plus]

def _aliases_version(func):
    """Return the aliases version of this function."""

    name = func.__name__

    suffix = ''
    if name.endswith('_error'):
        suffix = '_error'
        name = name[:-6]
    elif name.endswith('_flag'):
        suffix = '_flag'
        name = name[:-5]

    name = _strip_aliases(name)
    if name not in ALIAS_FUNC_NAMES: return func

    name += '_aliases' + suffix
    if name in globals():
        return globals()[name]

    return func

def _noaliases_version(func):
    """Return the flag version of this function."""

    name = func.__name__

    suffix = ''
    if name.endswith('_error'):
        suffix = '_error'
        name = name[:-6]
    elif name.endswith('_flag'):
        suffix = '_flag'
        name = name[:-5]

    name = _strip_aliases(name)
    if name not in ALIAS_FUNC_NAMES: return func

    name += '_noaliases' + suffix
    if name in globals():
        return globals()[name]

    return func

def _strip_aliases(name):
    if name.endswith('_aliases'):
        name = name[:-8]
    elif name.endswith('_noaliases'):
        name = name[:-10]

    return name

################################################################################
# Methods to select between the *_error and *_flag versions of functions
################################################################################

def _use_errors(names=[]):
    """Switch all functions, or just those listed, to raise exceptions instead
    of returning flags."""

    if names:
        keys = [cspice1._strip_error_flag(n) for n in names]
    else:
        keys = ERROR_FUNC_NAMES

    for key in keys:
        long_key = key + '_error'
        if key in globals() and long_key in globals():
            globals()[key] = globals()[long_key]

def _use_flags(names=[]):
    """Switch all functions, or just those listed, to return flags instead of
    raising exceptions."""

    if names:
        keys = [cspice1._strip_error_flag(n) for n in names]
    else:
        keys = ERROR_FUNC_NAMES

    for key in keys:
        long_key = key + '_flag'
        if key in globals() and long_key in globals():
            globals()[key] = globals()[long_key]

def _error_version(func):
    """Return the _error version of this function, if available."""

    long_key = cspice1._strip_error_flag(func.__name__) + '_error'
    if long_key in globals():
        return globals()[long_key]

    return func

def _flag_version(func):
    """Return the flag version of this function."""

    long_key = cspice1._strip_error_flag(func.__name__) + '_flag'
    if long_key in globals():
        return globals()[long_key]

    return func

def _error_version_cspice1(func):
    """Return the _error version of this function, if available."""

    long_key = cspice1._strip_error_flag(func.__name__) + '_error'
    if long_key in cspice1.__dict__:
        return cspice1.__dict__[long_key]

    return func

def _flag_version_cspice1(func):
    """Return the flag version of this function."""

    long_key = cspice1._strip_error_flag(func.__name__) + '_flag'
    if long_key in cspice1.__dict__:
        return cspice1.__dict__[long_key]

    return func

################################################################################
# Define a global dictionary of versions
################################################################################

_error_version_funcs = [_flag_version, _error_version]
_alias_version_funcs = [_noaliases_version, _aliases_version]

# Indexing is [error, aliases][name]
# error == -1: default; error == 0: use flags; error == 1: use errors
# aliases == -1: default; aliases == 0: no aliases; aliases == 1: use aliases

ALL_CSPICE1_VERSIONS = {}
ALL_CSPICE2_VERSIONS = {}

for error in (-1, 0, 1):
  for aliases in (-1, 0, 1):
    ALL_CSPICE1_VERSIONS[error, aliases] = {}
    ALL_CSPICE2_VERSIONS[error, aliases] = {}

for name in ALL_FUNC_NAMES:
    func0 = globals()[name]
    for error in (-1, 0, 1):
        if error == -1:
            func1 = func0
        else:
            func1 = _error_version_funcs[error](func0)

        for aliases in (-1, 0, 1):
            if aliases == -1:
                func2 = func1
            else:
                func2 = _alias_version_funcs[aliases](func1)

            ALL_CSPICE2_VERSIONS[error, aliases][name] = func2

_error_version_cspice1 = [_flag_version_cspice1, _error_version_cspice1]

for name in ALL_FUNC_NAMES:
    key = name.replace('_aliases','').replace('_noaliases', '')
    func0 = cspice1.__dict__[key]

    for error in (-1, 0, 1):
        if error == -1:
            func1 = func0
        else:
            func1 = _error_version_cspice1[error](func0)

        for aliases in (-1, 0, 1):
            ALL_CSPICE1_VERSIONS[error, aliases][name] = func1

################################################################################
################################################################################
################################################################################
# handler = 'CHECK'
#
# These functions check argument types and raise ValueError on mismatch.
################################################################################

def _check_int(arg, k, func):
    """Return arg; raise ValueError if it is not compatible with type int"""

    if not isinstance(arg, int):
        raise ValueError('Function %s argument %d ' % (func.__name__, k+1) +
                         'is not of type int')
    return arg

def _check_float(arg, k, func):
    """Return arg; raise ValueError if it is not compatible with type float"""

    if not isinstance(arg, float):
        raise ValueError('Function %s argument %d ' % (func.__name__, k+1) +
                         'is not of type float')
    return arg

def _check_string(arg, k, func):
    """Return arg; raise ValueError if it is not compatible with type int"""

    if not isinstance(arg, str):
        raise ValueError('Function %s argument %d ' % (func.__name__, k+1) +
                         'is not of type string')
    return arg

def _check_bool(arg, k, func):
    """Return arg; raise ValueError if it is not compatible with type int"""

    if not isinstance(arg, (bool, np.bool_)):
        raise ValueError('Function %s argument %d ' % (func.__name__, k+1) +
                         'is not of type bool')
    return arg

def _check_array(arg, dtype, shape, k, func):
    """Return arg; raise ValueError if it is not compatible with type int"""

    # Allow for lists and tuples
    if type(arg) in (list, tuple):
        arg = np.array(arg)

    # Make sure it is an array
    if not isinstance(arg, np.ndarray):
        raise ValueError('Function %s argument %d ' % (func.__name__, k+1) +
                         'is not an array')

    # Check the array rank
    if len(shape) != len(arg.shape):
        raise ValueError('Function %s argument %d ' % (func.__name__, k+1) +
                         'is not an array of rank %d' % len(shape))

    # Check the shape
    bad_shape = False
    if shape[0] != 0 and shape[0] != arg.shape[0]:
        bad_shape = True
    if len(shape) > 1 and shape[1] != 0 and shape[1] != arg.shape[1]:
        bad_shape = True
    if len(shape) == 3 and shape[2] != 0 and shape[2] != arg.shape[2]:
        bad_shape = True

    if bad_shape:
        good_shape = str(shape).replace('0','*')
        raise ValueError('Function %s argument %d ' % (func.__name__, k+1) +
                         'is not an array with shape %s' % good_shape)

    # Check the array dtype
    bad_dtype = False
    if dtype == 'float' and arg.dtype.kind != 'f':
        bad_dtype = True

    if dtype == 'int' and arg.dtype.kind not in 'ui':
        bad_dtype = True

    if dtype == 'bool' and arg.dtype.kind != 'b':
        bad_dtype = True

    if dtype == 'string' and arg.dtype.kind != 'S':
        bad_dtype = True

    if bad_dtype:
        raise ValueError('Function %s argument %d ' % (func.__name__, k+1) +
                         'is not an array of dtype %s' % dtype)

    return arg

HANDLERS_FOR_CHECK = {
    'int'       : _check_int,
    'float'     : _check_float,
    'string'    : _check_string,
    'bool'      : _check_bool,
    'body_name' : _check_string,
    'body_code' : _check_int,
    'frame_name': _check_string,
    'frame_code': _check_int,
    'array'     : _check_array,
}

################################################################################
################################################################################
################################################################################
# handler = 'CONVERT'
#
# These functions cast arguments to the expected type, if possible
################################################################################

def _cast_to_int(arg, k, func):
    try:
        return int(arg)
    except ValueError:
        raise ValueError('Function %s argument %d ' % (func.__name__, k+1) +
                         'cannot be converted to type int')

def _cast_to_float(arg, k, func):
    try:
        return float(arg)
    except ValueError:
        raise ValueError('Function %s argument %d ' % (func.__name__, k+1) +
                         'cannot be converted to type float')

def _cast_to_string(arg, k, func):
    try:
        return str(arg)
    except ValueError:
        raise ValueError('Function %s argument %d ' % (func.__name__, k+1) +
                         'cannot be converted to type string')

def _cast_to_bool(arg, k, func):
    try:
        return bool(arg)
    except ValueError:
        raise ValueError('Function %s argument %d ' % (func.__name__, k+1) +
                         'cannot be converted to type bool')

def _cast_to_array(arg, dtype, shape, k, func):

    # Allow for lists and tuples
    if type(arg) in (list, tuple):
        arg = np.array(arg)

    # Convert any scalar to an array of size one
    if shape in [(0,), (0,0), (0,0,0)] and not isinstance(arg, np.ndarray):
        arg = np.array([arg])

    # Extend rank of array if needed
    if len(arg.shape) < len(shape):
        new_shape = tuple((len(shape) - len(arg.shape)) * [1] + list(arg.shape))
        arg = arg.reshape(new_shape)

    # Validate shape
    for k in range(1,len(shape)+1):
        if shape[-k] != 0 and shape[-k] != arg.shape[-k]:
            shapestr = str(shape).replace('0','*')
            raise ValueError('Function %s ' % func.__name__ +
                             'argument %d is not an array ' % (k+1) +
                             'with shape %s' % shapestr)

    # Check the array rank
    if len(shape) != len(arg.shape):
        raise ValueError('Function %s argument %d ' % (func.__name__, k+1) +
                         'is not an array of rank %d' % len(shape))

    # Attempt to convert the array dtype if necessary
    try:
        if dtype == 'float' and arg.dtype.kind != 'f':
            arg = arg.asfarray()

        if dtype == 'int' and arg.dtype.kind not in 'ui':
            arg = arg.astype('int')

        if dtype == 'bool' and arg.dtype.kind != 'b':
            arg = arg.astype('bool')

        if dtype == 'string' and arg.dtype.kind != 'S':
            arg = arg.astype('string')

    except Error:
        raise ValueError('Function %s argument %d ' % (func.__name__, k+1) +
                         'cannot be converted to dtype %s' % dtype)

    return arg

HANDLERS_FOR_CONVERT = {
    'int'       : _cast_to_int,
    'float'     : _cast_to_float,
    'string'    : _cast_to_string,
    'bool'      : _cast_to_bool,
    'body_name' : _cast_to_string,
    'body_code' : _cast_to_int,
    'frame_name': _cast_to_string,
    'frame_code': _cast_to_int,
    'array'     : _cast_to_array,
}

################################################################################
################################################################################
################################################################################
# type_handler = 'TRANSLATE'
#
# These functions translate body/frame names and codes to the required type.
################################################################################

def _to_body_code(arg, k, func):
    """Return the body code given a body code or name."""

    # int case
    try:
        return int(arg)
    except ValueError:
        pass

    # string case
    (code, found) = cspice1.bodn2c_flag(str(arg))
    if found: return code

    raise ValueError('Function %s argument %d ' % (func.__name__, k+1) +
                     'does not identify a SPICE body: %s' % str(arg))

def _to_body_name(arg, k, func):
    """Return the body name given an body code or name."""

    # int case
    try:
        arg = int(arg)
        (name, found) = cspice1.bodc2n_flag(arg)
        if found: return name

    except ValueError:
        pass

    # string case
    arg = str(arg)
    (code, found) = cspice1.bodn2c_flag(arg)
    if found: return arg

    raise ValueError('Function %s argument %d ' % (func.__name__, k+1) +
                     'does not identify a SPICE body: %s' % str(arg))

def _to_frame_code(arg, k, func):
    """Return the frame code given a frame code or name."""

    # int case
    try:
        return int(arg)
    except ValueError:
        pass

    # string case
    code = cspice1.namfrm_flag(str(arg))
    if code != 0: return code

    arg = _clean_name(str(arg))
    raise ValueError('Function %s argument %d ' % (func.__name__, k+1) +
                     'does not identify a SPICE frame: %s' % arg)

def _to_frame_name(arg, k, func):
    """Return the frame name given a frame code or name."""

    # int case
    try:
        arg = int(arg)
        name = cspice1.frmnam_flag(arg)
        if name: return name
    except ValueError:
        pass

    # string case
    arg = str(arg)
    code = cspice1.namfrm_flag(str(arg))
    if code != 0: return arg

    arg = _clean_name(arg)
    raise ValueError('Function %s argument %d ' % (func.__name__, k+1) +
                     'does not identify a SPICE frame: %s' % arg)

HANDLERS_FOR_TRANSLATE = {
    'body_name' : _to_body_name,
    'body_code' : _to_body_code,
    'frame_name': _to_frame_name,
    'frame_code': _to_frame_code,
}

################################################################################
################################################################################
################################################################################
# handler = 'ALIASES'
#
# These functions support multiple names or codes for the same body or frame.
# If aliases are needed in the function call, these functions return a tuple:
#   ('aliases', list_of_names_or_ids)
################################################################################

def _to_body_codes(arg, k, func):
    """Return a list of body codes given a body code or name. Return a single
    value if the list length is 1."""

    # int case
    try:
        arg = int(arg)
        if arg in CODE_ALIASES:
            results = CODE_ALIASES[arg]
            if len(results) == 1:
                return results[0]
            else:
                return ('aliases', results)
        else:
            return arg
    except ValueError:
        pass

    # string case
    results = bodn2c_aliases(str(arg))
    if len(results) == 0:
        raise ValueError('Function %s argument %d ' % (func.__name__, k+1) +
                         'does not identify a SPICE body: %s' % str(arg))
    elif len(results) == 1:
        return results[0]
    else:
        return ('aliases', results)

def _to_body_names(arg, k, func):
    """Return a list of body names given an body code or name. Return a single
    value if the list length is 1."""

    # Test for int
    try:
        arg = int(arg)
    except ValueError:
        arg = _clean_name(str(arg))

    # string case
    if type(arg) == str:
        if arg in NAME_ALIASES:
            return NAME_ALIASES[arg]

        return arg

    # int case
    results = bodc2n_aliases(arg)
    if len(results) == 0:
        raise ValueError('Function %s argument %d ' % (func.__name__, k+1) +
                         'does not identify a SPICE body: %d' % arg)
    elif len(results) == 1:
        return results[0]
    else:
        return ('aliases', results)

HANDLERS_FOR_ALIASES = {
    'body_name' : _to_body_names,
    'body_code' : _to_body_codes,
    'frame_name': _to_frame_name,
    'frame_code': _to_frame_code,
}

# ################################################################################
# # Functions that allow vectorized float arguments.
# # If a float argument has an extra leading axis, it returns a tuple:
# #   ('vectorized', arg, leading_shape)
# ################################################################################
# 
# def _cast_to_float_vectorized(arg, k, func)
# 
#     try:
#         if isinstance(arg, np.ndarray):
#             if arg.shape == ():
#                 return float(arg[()])
#             else:
#                 return ('vectorized', arg.asfarray(arg), arg.shape)
#         else:
#             return float(arg)
# 
#     except ValueError:
#         raise ValueError('Function %s argument %d ' % (func.__name__, k+1) +
#                          'cannot be converted to type float')
# 
# def _cast_to_array_vectorized(arg, dtype, shape, k, func):
# 
#     # Only float arrays can be vectorized
#     if dtype != 'float':
#         raise ValueError('Function %s argument %d ' % (func.__name__, k+1) +
#                          'cannot be vectorized' % dtype)
# 
#     # Convert any scalar to an array of size one
#     if not isinstance(arg, np.ndarray):
#         arg = np.array([arg])
# 
#     # Extend rank of array if needed
#     while len(arg.shape) < len(shape):
#         arg = arg.reshape((1,) + arg.shape)
# 
#     # Validate shape
#     for k in range(1,len(shape)+1):
#         if shape[-k] != 0 and shape[-k] != arg.shape[-k]:
#             shapestr = str(shape).replace('0','*')
#             raise ValueError('Function %s ' % func.__name__
#                              'argument %d is not an array ' % (k+1) +
#                              'with trailing shape %s' % shapestr)
# 
#     if len(shape) == len(arg.shape):
#         return arg
#     else:
#         return ('vectorized', arg, arg.shape[:-len(shape)])
# 
# VECTORIZED_HANDLERS = {
#     'float': _cast_to_float_vectorized
#     'array': _cast_to_array_vectorized
# }
# 
# # A needed utility
# 
# def _broadcast_shapes(shapes):
#     """Return the shape (as a list) resulting from broadcasting together all of
#     the given shapes. Also update all shapes to the same rank."""
# 
#     broadcasted = []
#     for shape in shapes:
#         old_shape = shape
#         old_broadcasted = broadcasted
# 
#         shape = list(shape)
# 
#         while len(shape) < len(broadcasted):
#             shape = [1] + shape
#         while len(broadcasted) < len(shape)
#             broadcasted = [1] + broadcasted
# 
#         for k in range(len(shape)):
#             if shape[k] != 1:
#                 if broadcasted[k] == 1:
#                     broadcasted[k] = shape[k]
#                 elif broadcasted[k] != shape[k]:
#                     raise ValueError('Array shapes cannot be broadcasted:' +
#                                      ' %s, %s' % (str(old_shape),
#                                                   str(tuple(old_broadcasted))))
# 
#     rank = len(broadcasted)
#     new_shapes = []
#     for shape in shapes:
#         shape = list(shape)
#         if len(shape) < rank:
#             new_shape = (rank - len(shape) * [1] + shape
# 
#         new_shapes.append(new_shape)
# 
#     return (broadcasted, new_shapes)

################################################################################
# Option selections
################################################################################

HANDLERS_FOR_NONE = {
    'int'       : None,
    'float'     : None,
    'string'    : None,
    'bool'      : None,
    'body_name' : None,
    'body_code' : None,
    'frame_name': None,
    'frame_code': None,
    'array'     : None,
}

HANDLERS = {
    'NONE'     : HANDLERS_FOR_NONE,
    'CHECK'    : HANDLERS_FOR_CHECK,
    'CONVERT'  : HANDLERS_FOR_CONVERT,
    'TRANSLATE': HANDLERS_FOR_TRANSLATE,
    'ALIASES'  : HANDLERS_FOR_ALIASES,
#     'vectorized': HANDLERS_FOR_VECTORIZED,
}

ORDERED_HANDLERS = ('NONE', 'CHECK', 'CONVERT', 'TRANSLATE', 'ALIASES')#,
#                     'VECTORIZED')

RULE_NAMES = set(ORDERED_HANDLERS + ('FLAGS', 'ERRORS', 'ALIASES', 'NOALIASES'))

def select_rules(*names):

    # Make sure all rules are valid
    names = [n.upper() for n in names]
    for name in names:
        if name not in RULE_NAMES:
            raise ValueError('Unrecognized rule "%s"' % name)

    # Convert to set
    names = set(names)

    # Remove 'NONE' if it appears
    try:
        names.remove('NONE')
    except KeyError:
        pass

    # Assemble the rules
    handlers = HANDLERS['NONE'].copy()
    using_none_handler = True

    for handler in ORDERED_HANDLERS:
        if handler in names:
            using_none_handler = False
            for (key, value) in HANDLERS[handler].iteritems():
                handlers[key] = value

    if using_none_handler:
        handlers = None

    # Check versions
    if 'FLAGS' in names and 'ERRORS' in names:
        raise ValueError('Incompatible rules: FLAGS and ERRORS')

    if 'NOALIASES' in names and 'ALIASES' in names:
        raise ValueError('Incompatible rules: ALIASES and NOALIASES')

    error_index = -1
    if 'FLAGS'  in names: error_index = 0
    if 'ERRORS' in names: error_index = 1

    alias_index = -1
    if 'NOALIASES' in names: alias_index = 0
    if 'ALIASES'   in names: alias_index = 1

    return (handlers, error_index, alias_index)

################################################################################
# Complete wrapper to execute a CSPICE function
################################################################################

def exec_with_rules(func, rules, *args):

    (handlers, error_index, alias_index) = rules
    func = ALL_CSPICE1_VERSIONS[error_index, alias_index][func.__name__]

    args = list(args)

    # Handle case of no checking quickly
    if handlers is None:
        return func.__call__(*args)

    signature = func.SIGNATURE
    if func.func_defaults:
        first_optional -= len(func.func_defaults)

    # Create an updated list of args
    vectorized_shapes = 0
    vectorized_indices = []
    aliased_indices = []

    for k in range(len(signature)):
        argtype = signature[k]
        arg = args[k]

        # Make sure we have enough args
        if k >= len(args):
            if k >= first_optional: break
            raise ValueError('Function %s argument %d ' % (func.__name__, k+1) +
                             'is missing')

        # Handle an array arg
        if type(argtype) == tuple:
            rule_func = handlers['array']
            if rule_func:
                arg = rule_func.__call__(arg, argtype[0], argtype[1], k, func)

        # Handle a scalar arg
        else:
            rule_func = handlers[argtype]
            if rule_func:
                arg = rule_func.__call__(arg, k, func)

        # Look for vectorization and aliases
        if type(arg) == tuple:
            assert arg[0] in ('vectorized', 'aliases')
            if arg[0] == 'vectorized':
                vectorized_shapes.append(arg[2])
                vectorized_indices.append(k)
                arg = arg[1]
            else:
                aliased_indices.append(k)
                arg = arg[1]

        args[k] = arg

    # Make sure we don't have any extra args
    if len(args) > len(signature):
        raise ValueError('Function %s has too many arguments' % func.__name__)

    # Call function now if iteration is not needed
    if not vectorized_indices and not aliased_indices:
        return func.__call__(*args)

    # Broadcast the vector shapes
    if vectorized_shapes:
        (broadcast_shape, new_shapes) = _broadcast_shapes(vectorized_shapes)

        for k in range(len(vectorized_indices)):
            indx = vectorized_indices[k]
            full_shape = new_shapes[k] + list(signature[indx][1])
            args[indx] = args[indx].reshape(full_shape)
    else:
        broadcast_shape = []

def _alias_iterator(func, args, aliased_indices,
                    broadcast_shape, vectorized_shapes, vectorized_indices):

    # Make a local copy of the arguments
    local_args = []
    for arg in args:
        local_args.append(arg)

    # Pop the next index
    indx = aliased_indices[0]
    values = args[indx]
    aliased_indices = aliased_indices[1:]

    # If this is the last alias...
    if not aliased_indices:
        for value in values:
            local_args[indx] = value

            # Vectorized case
            if broadcast_shape:
                return _vector_iterator(func, local_args,
                                        broadcast_shape, vectorized_shapes,
                                        vectorized_indices)
            # Unvectorized case
            else:
                try:
                    return cspice1.exception_version(func).__call__(*local_args)
                except Error as e:
                    pass

        raise e

    # Otherwise, recurse
    else:
        for value in values:
            local_args[indx] = value
            try:
                return _alias_iterator(func, local_args, aliased_indices,
                                       broadcast_shape, vectorized_shapes,
                                       vectorized_indices)
            except Error as e:
                pass

        raise e

def _vector_iterator(func, args, broadcast_shape, vectorized_indices):

    # Create an empty buffer for the results
    results = []
    for argtype in func.RETURNS:
        if type(argtype) == str:
            results.append(np.empty(broadcast_shape, dtype=argtype))
        else:
            full_shape = broadcast_shape + list(argtype[1])
            results.append(np.empty(full_shape, dtype=argtype))

    # Iterate to fill buffer
    _vector_iterator1(func, args, results, broadcast_shape,
                                           vectorized_indices)

    # Return buffer as a single array or list of arrays
    if len(results) == 1:
        return results[0]
    else:
        return results

def _vector_iterator1(func, args, results, broadcast_shape, vectorized_indices):

    # Make a local copy of the arguments
    local_args = []
    for arg in args:
        local_args.append(arg)

    # Pop the top index
    axis = broadcast_shape[0]
    broadcast_shape = broadcast_shape[1:]

    # Iterate along the top axis
    for k in range(axis):

        # Prepare one slice of each input array
        for j in vectorized_indices:
            if args[j].shape[0] == axis:
                local_args[j] = args[j][k]
            else:
                local_args[j] = args[j][0]

        # Prepare one slice of the output buffer
        local_results = []
        for array in local_results:
            local_results.append(array[k])

        # Continue iteration if this is not the last axis
        if broadcast_shape:
            _vector_iterator1(func, local_args, local_results,
                                    broadcast_shape, vectorized_indices)

        # Otherwise, evaluate the function and save in the buffer
        else:
            result_k = func.__call__(*local_args)
            if type(result_k) != list:
                result_k = [result_k]

            for p in range(len(local_results)):
                local_results[p][k] = result_k[p]


def rules_version(func, rules):
    """Return a function that applies the selected rules to the selected
    cspice1 function."""

    def wrapper(*args):
        return exec_with_rules(func, rules, *args)

    wrapper.__doc__   = func.__doc__
    wrapper.__name__  = func.__name__
    wrapper.SIGNATURE = func.SIGNATURE
    wrapper.RETURNS   = func.RETURNS
    wrapper.RULES     = rules

    return wrapper

def apply_rules(rules, names=[]):
    """Apply a particular set of rules to a list of named functions or, by
    default, every cspice function."""

    if type(names) == str:
        names = [names]

    if not names:
        names = CSPICE_FUNC_NAMES

    for name in names:
        cspice1.__dict__[name].RULES = rules

################################################################################
