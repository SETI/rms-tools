################################################################################
# cspice/cspice2/aliases.py
################################################################################

import re
import cspice1

################################################################################
# Alias support
#
# Alternative versions of boddef, bods2n, bodc2n, bodc2s, and bodn2c that
# support multiple codes and/or multiple names used for the same body. As
# inputs, each of these functions can take a list, tuple or vector of arguments
# in place of a single argument.
################################################################################

# Global dictionaries to track aliases
CODE_ALIASES = {}
NAME_ALIASES = {}

_VERSION_REGEX = re.compile('.* V[0-9]+$')

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
    for k in range(len(codes))[::-1]:   # reverse order; later boddef calls win
        cspice1.boddef(names[k], codes[k])

def _bodc2n_for_aliases(code):
    """Return a list of names given a code or name"""

    # Look up in table as a code or name
    try:
        key = int(code)
    except ValueError:
        key = _clean_name(str(code))

    if key in NAME_ALIASES:
        return NAME_ALIASES[key]

    # If it is an int, use the cspice1 call
    if type(key) == int:
        (name, found) = cspice1.bodc2n_flag(key)
        if found:
            return [name]
        else:
            return []

    # Otherwise, search for a code based on name
    (code, found) = cspice1.bodn2c_flag(key)
    if found:
        (name, found) = cspice1.bodc2n_flag(code)
        if found:
            return [name]

    return []

def _bodc2s_for_aliases(code):
    """Return a list of names given a code. If no translation, convert the code
    to a string."""

    results = _bodc2n_for_aliases(code)
    if results: return results

    if type(code) == int:
        return [str(code)]
    else:
        return []

def _bodn2c_for_aliases(name):
    """Return a list of codes given a name or code. Returned list may be empty.
    """

    # Look up in table as a code or name
    try:
        key = int(name)
    except ValueError:
        key = _clean_name(name)

    if key in CODE_ALIASES:
        return CODE_ALIASES[key]

    # If it is a string, use the cspice1 call
    if type(key) == str:
        (code, found) = cspice1.bodn2c_flag(key)
        if found:
            return [code]
        else:
            return []

    # Otherwise, see if it really is a body code
    (name, found) = cspice1.bodc2n_flag(key)
    if found: return [key]

    return []

def _bods2c_for_aliases(name):
    """Return a list of codes given a name. Returned list may be empty."""

    return _bodn2c_for_aliases(name)

################################################################################
# Definitions of CSPICE functions with alias variants
################################################################################

ALIAS_SIGNATURES = {}
ALIAS_RETURNS    = {}
ALIAS_DOCSTRINGS = {}

########################################

ALIAS_SIGNATURES["boddef_aliases"] = ["string[*]", "int[*]"]
ALIAS_RETURNS   ["boddef_aliases"] = []
ALIAS_DOCSTRINGS["boddef_aliases"] = """
Define a body name/ID code pair for later translation via bodn2c or bodc2n.

This version also supports aliases. Specify an array/list/tuple of multiple
names or codes, and they will all be treated as equivalent.

boddef(<string> name, <int> code)

name = Common name of some body, or an aliased array, list or tuple of names.
code = Integer code for that body, or an aliased array, list or tuple of codes.
"""

def boddef_aliases(name, code):
    _boddef_for_aliases(name, code)

boddef_aliases.__doc__   = ALIAS_DOCSTRINGS["boddef_aliases"]
boddef_aliases.SIGNATURE = ALIAS_SIGNATURES["boddef_aliases"]
boddef_aliases.RETURNS   = ALIAS_RETURNS   ["boddef_aliases"]

########################################

ALIAS_SIGNATURES["bodc2n_aliases"] = ["body_code"]
ALIAS_RETURNS   ["bodc2n_aliases"] = ["string[*]", "bool"]
ALIAS_DOCSTRINGS["bodc2n_aliases"] = """
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

bodc2n_aliases.__doc__   = ALIAS_DOCSTRINGS["bodc2n_aliases"]
bodc2n_aliases.SIGNATURE = ALIAS_SIGNATURES["bodc2n_aliases"]
bodc2n_aliases.RETURNS   = ALIAS_RETURNS   ["bodc2n_aliases"]

########################################

ALIAS_SIGNATURES["bodc2n_aliases_error"] = ["body_code"]
ALIAS_RETURNS   ["bodc2n_aliases_error"] = ["string[*]"]
ALIAS_DOCSTRINGS["bodc2n_aliases_error"] = """
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

bodc2n_aliases_error.__doc__   = ALIAS_DOCSTRINGS["bodc2n_aliases_error"]
bodc2n_aliases_error.SIGNATURE = ALIAS_SIGNATURES["bodc2n_aliases_error"]
bodc2n_aliases_error.RETURNS   = ALIAS_RETURNS   ["bodc2n_aliases_error"]

########################################

ALIAS_SIGNATURES["bodc2s_aliases"] = ["body_code"]
ALIAS_RETURNS   ["bodc2s_aliases"] = ["string[*]"]
ALIAS_DOCSTRINGS["bodc2s_aliases"] = """
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

bodc2s_aliases.__doc__   = ALIAS_DOCSTRINGS["bodc2s_aliases"]
bodc2s_aliases.SIGNATURE = ALIAS_SIGNATURES["bodc2s_aliases"]
bodc2s_aliases.RETURNS   = ALIAS_RETURNS   ["bodc2s_aliases"]

########################################

ALIAS_SIGNATURES["bodn2c_aliases"] = ["body_name"]
ALIAS_RETURNS   ["bodn2c_aliases"] = ["int[*]", "bool"]
ALIAS_DOCSTRINGS["bodn2c_aliases"] = """
Translate the name of a body or object to one or more corresponding SPICE
integer ID codes.

bodn2c(<string> name) -> [(<int> or <int[*]>) code, <bool> found]

name  = Body name to be translated into a SPICE ID code.
code  = One or more SPICE integer ID codes for the named body.
found = True if translated, otherwise False.
"""

def bodn2c_aliases(name):
    results = _bodn2c_for_aliases(name)
    if len(results) == 0:
        return [0, False]

    if len(results) == 1:
        return [results[0], True]
    else:
        return [results, True]

bodn2c_aliases.__doc__   = ALIAS_DOCSTRINGS["bodn2c_aliases"]
bodn2c_aliases.SIGNATURE = ALIAS_SIGNATURES["bodn2c_aliases"]
bodn2c_aliases.RETURNS   = ALIAS_RETURNS   ["bodn2c_aliases"]

########################################

ALIAS_SIGNATURES["bodn2c_aliases_error"] = ["body_name"]
ALIAS_RETURNS   ["bodn2c_aliases_error"] = ["int[*]"]
ALIAS_DOCSTRINGS["bodn2c_aliases_error"] = """
Translate the name of a body or object to one or more corresponding SPICE
integer ID codes.

bodn2c(<string> name) -> (<int> or <int[*]>) code

name  = Body name to be translated into a SPICE ID code.
code  = One or more SPICE integer ID codes for the named body.

Raise KeyError if name cound not be translated.
"""

def bodn2c_aliases_error(name):
    results = _bodn2c_for_aliases(name)
    if len(results) == 0:
        name = _clean_name(str(name))
        raise KeyError('Error in bodn2c(): body name "%s" not found' % name)

    if len(results) == 1:
        return results[0]
    else:
        return results

bodn2c_aliases_error.__doc__   = ALIAS_DOCSTRINGS["bodn2c_aliases_error"]
bodn2c_aliases_error.SIGNATURE = ALIAS_SIGNATURES["bodn2c_aliases_error"]
bodn2c_aliases_error.RETURNS   = ALIAS_RETURNS   ["bodn2c_aliases_error"]

########################################

ALIAS_SIGNATURES["bods2c_aliases"] = ["body_name"]
ALIAS_RETURNS   ["bods2c_aliases"] = ["int[*]", "bool"]
ALIAS_DOCSTRINGS["bods2c_aliases"] = """
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

bods2c_aliases.__doc__   = ALIAS_DOCSTRINGS["bods2c_aliases"]
bods2c_aliases.SIGNATURE = ALIAS_SIGNATURES["bods2c_aliases"]
bods2c_aliases.RETURNS   = ALIAS_RETURNS   ["bods2c_aliases"]

########################################

ALIAS_SIGNATURES["bods2c_aliases_error"] = ["body_name"]
ALIAS_RETURNS   ["bods2c_aliases_error"] = ["int[*]"]
ALIAS_DOCSTRINGS["bods2c_aliases_error"] = """
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
        name = _clean_name(str(name))
        raise KeyError('Error in bods2c(): body name "%s" not found' % name)

    if len(results) == 1:
        return results[0]
    else:
        return results

bods2c_aliases_error.__doc__   = ALIAS_DOCSTRINGS["bods2c_aliases_error"]
bods2c_aliases_error.SIGNATURE = ALIAS_SIGNATURES["bods2c_aliases_error"]
bods2c_aliases_error.RETURNS   = ALIAS_RETURNS   ["bods2c_aliases_error"]

################################################################################
################################################################################

# At initialization, define a function *_flag for every function *_error.
#
# Also save...
#   ALIAS_FUNC_NAMES      = a list of every function name.
#   ALIAS_FUNC_BASENAMES  = a list of every unique function basename (without a
#                           _error or _flag suffix).
#   ALIAS_ERROR_BASENAMES = a list of every basename that takes _error and _flag
#                           suffixes.

ALIAS_FUNC_NAMES = ALIAS_DOCSTRINGS.keys()
ALIAS_FUNC_BASENAMES = []
ALIAS_ERROR_BASENAMES = []

for name in ALIAS_FUNC_NAMES:
    error_name = name + '_error'
    short_name = name
    flag_name  = name + '_flag'

    if error_name in globals():
        globals()[flag_name] = globals()[short_name]
        ALIAS_DOCSTRINGS[flag_name] = ALIAS_DOCSTRINGS[short_name]
        ALIAS_SIGNATURES[flag_name] = ALIAS_SIGNATURES[short_name]
        ALIAS_RETURNS   [flag_name] = ALIAS_RETURNS   [short_name]

        ALIAS_ERROR_BASENAMES.append(short_name[:-8])

    if short_name in globals() and not short_name.endswith('_error'):
        ALIAS_FUNC_BASENAMES.append(short_name[:-8])

# At initialization, define a function *_noaliases* for every *_aliases*.

ALIAS_FUNC_NAMES = ALIAS_DOCSTRINGS.keys()
for name in ALIAS_FUNC_NAMES:
    long_name = name.replace('_aliases', '_noaliases')
    short_name = name.replace('_aliases', '')

    globals()[long_name] = cspice1.__dict__[short_name]
    ALIAS_DOCSTRINGS[long_name] = cspice1.CSPICE1_DOCSTRINGS[short_name]
    ALIAS_SIGNATURES[long_name] = cspice1.CSPICE1_SIGNATURES[short_name]
    ALIAS_RETURNS   [long_name] = cspice1.CSPICE1_RETURNS   [short_name]

ALIAS_FUNC_NAMES = ALIAS_DOCSTRINGS.keys()
ALIAS_FUNC_NAMES.sort()
ALIAS_FUNC_BASENAMES.sort()
ALIAS_ERROR_BASENAMES.sort()

################################################################################
# Define attributes alias_version, noalias_version, error_version and
# flag_version for every function.
################################################################################

def _strip_aliases(name):
    """Remove '_alias' or '_noalias' from a function name."""

    return name.replace('_aliases','').replace('_noaliases','')

def _insert_into_name(name, insert):
    if name.endswith('_error'):
        return name[:-6] + insert + '_error'
    elif name.endswith('_flag'):
        return name[:-5] + insert + '_flag'
    else:
        return name + insert

for name in ALIAS_FUNC_NAMES:
    func = globals()[name]
    short_key = _strip_aliases(name)

    long_key = _insert_into_name(short_key, '_aliases')
    func.alias_version = globals()[long_key]

    long_key = _insert_into_name(short_key, '_noaliases')
    func.noalias_version = globals()[long_key]

    short_key = cspice1._strip_error_flag(name)
    long_key = short_key + '_error'
    if long_key in globals():
        func.error_version = globals()[long_key]
        func.flag_version = globals()[short_key + '_flag']
#         func.flag_version.__name__ = [short_key + '_flag']
    else:
        func.error_version = func
        func.flag_version = func

################################################################################
# Define functions to select between *_alias and *_noalias versions of functions
################################################################################

ALIAS_FUNC_SHORTNAMES = [_strip_aliases(n) for n in ALIAS_FUNC_NAMES]
ALIAS_FUNC_SHORTNAMES = list(set(ALIAS_FUNC_SHORTNAMES))
ALIAS_FUNC_SHORTNAMES.sort()

ALIAS_FUNC_BASENAMES = [cspice1._strip_error_flag(n)
                        for n in ALIAS_FUNC_SHORTNAMES]
ALIAS_FUNC_BASENAMES = list(set(ALIAS_FUNC_BASENAMES))
ALIAS_FUNC_BASENAMES.sort()

def use_aliases(*names):
    """Make the _aliases version of the named functions, or else of every
    function, the default."""

    if names:
        short_names = [cspice1._strip_error_flag(n) for n in names]
        basenames = [_strip_aliases(n) for n in short_names]
        basenames = set(basenames)
        for n in basenames:
            if n not in ALIAS_FUNC_BASENAMES:
                raise ValueError('Unrecognized alias function "%s"' % n)
    else:
        basenames = ALIAS_FUNC_BASENAMES

    # Change the defaults for name, name_error and name_flag
    for basename in basenames:
      for suffix in ('', '_error', '_flag'):
        short_name = basename + suffix
        if short_name in globals():
            globals()[short_name] = globals()[short_name].alias_version

def use_noaliases(*names):
    """Make the _noaliases version of the named functions, or else of every
    function, the default."""

    if names:
        short_names = [cspice1._strip_error_flag(n) for n in names]
        basenames = [_strip_aliases(n) for n in short_names]
        basenames = set(basenames)
        for n in basenames:
            if n not in ALIAS_FUNC_BASENAMES:
                raise ValueError('Unrecognized alias function "%s"' % n)
    else:
        basenames = ALIAS_FUNC_BASENAMES

    # Change the defaults for name, name_error and name_flag
    for basename in basenames:
      for suffix in ('', '_error', '_flag'):
        short_name = basename + suffix
        if short_name in globals():
            globals()[short_name] = globals()[short_name].noalias_version

################################################################################
