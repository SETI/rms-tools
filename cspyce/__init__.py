################################################################################
# cspyce/__init__.py
################################################################################
# SPYCE OVERVIEW
#
# Spyce is a Python module that provides an interface to the CSPICE library. It
# implements the most widely-used functions of CSPICE in a Python-like way. It
# also supports numerous enhancements, including support for Python exceptions,
# array inputs, and aliases.
#
# This version of the library has been built for the CSPICE toolkit v. 66.
#
# See the file AAREADME.txt for more information.
#
# Mark Showalter, PDS Ring-Moons Systems Node, SETI Institute, December 2017.
################################################################################

# We allow the import of cspyce2 to fail because, during development, there are
# times when cspyce2.py might be invalid. If that happens, we still want to be
# able to work inside the cspyce directory tree. Without allowing this
# exception, it could become impossible to work on and test cspyce functions
# inside this directory tree. This should never occur during a normal run.

try:
    from cspyce2 import *
except ImportError:
    pass

# A set of keywords listing options set globally across the cspyce functions
GLOBAL_STATUS = set()

################################################################################
# Define functions to select between error and flag versions of functions
################################################################################

def use_errors(*funcs):
    """Switch the listed functions or names of functions to use the "error"
    version by default. If the list is empty, apply this operation to all cspyce
    functions.

    Note that this operation applies to all versions of each function. Versions
    are cspyce functions with the same base name, before any suffixes.
    """

    global GLOBAL_STATUS
    if funcs:
        GLOBAL_STATUS.add('ERRORS')
        GLOBAL_STATUS.discard('FLAGS')
    else:
        GLOBAL_STATUS.discard('ERRORS')
        GLOBAL_STATUS.discard('FLAGS')

    for name in _get_func_names(funcs):
        if 'error' not in name and 'flag' not in name:
            globals()[name] = globals()[name].error

def use_flags(*funcs):
    """Switch the listed functions or names of functions to use the "flag"
    version by default. If the list is empty, apply this operation to all cspyce
    functions.

    Note that this operation applies to all versions of each function. Versions
    are cspyce functions with the same base name, before any suffixes.
    """

    global GLOBAL_STATUS
    if funcs:
        GLOBAL_STATUS.discard('ERRORS')
        GLOBAL_STATUS.add('FLAGS')
    else:
        GLOBAL_STATUS.discard('ERRORS')
        GLOBAL_STATUS.discard('FLAGS')

    for name in _get_func_names(funcs):
        if 'error' not in name and 'flag' not in name:
            globals()[name] = globals()[name].flag

################################################################################
# Define functions to select between vector and scalar versions of functions
################################################################################

def use_vectors(*funcs):
    """Switch the listed functions or names of functions to use the "vector"
    version by default. If the list is empty, apply this operation to all cspyce
    functions.

    Note that this operation applies to all versions of each function. Versions
    are cspyce functions with the same base name, before any suffixes.
    """

    global GLOBAL_STATUS
    if funcs:
        GLOBAL_STATUS.discard('ARRAYS')
        GLOBAL_STATUS.add('VECTORS')
        GLOBAL_STATUS.discard('SCALARS')
    else:
        GLOBAL_STATUS.discard('ARRAYS')
        GLOBAL_STATUS.discard('VECTORS')
        GLOBAL_STATUS.discard('SCALARS')

    for name in _get_func_names(funcs):
        if ('scalar' not in name and 'vector' not in name
                                 and 'array' not in name):
            globals()[name] = globals()[name].vector

def use_scalars(*funcs):
    """Switch the named functions, or else all relevant cspyce functions, to
    return flags instead of raising exceptions.

    Note that this operation applies to all versions of each function. Versions
    are cspyce functions with the same base name, before any suffixes.
    """

    global GLOBAL_STATUS
    if funcs:
        GLOBAL_STATUS.discard('ARRAYS')
        GLOBAL_STATUS.discard('VECTORS')
        GLOBAL_STATUS.add('SCALARS')
    else:
        GLOBAL_STATUS.discard('ARRAYS')
        GLOBAL_STATUS.discard('VECTORS')
        GLOBAL_STATUS.discard('SCALARS')

    for name in _get_func_names(funcs):
        if ('scalar' not in name and 'vector' not in name
                                 and 'array' not in name):
            globals()[name] = globals()[name].scalar

def _get_func_names(funcs=[], source=None):
    """Convert a list of cspyce functions or names to a set of unique names,
    including all versions.
    """

    source = source or globals()

    if funcs:
        validated = set()
        for func in funcs:
            # Convert names to funcs, assemble all versions
            validated |= set(get_all_versions(func, source).keys())
    else:
        validated = set(get_all_funcs(source).keys())

    return validated

################################################################################
# Functions to track down cspyce functions
################################################################################

def get_all_funcs(source=None, cspyce_dict=None):
    """Return a dictionary of all cspyce functions, keyed by their names.

    Inputs:
        source      the dictionary to search, which defaults to globals().
        cspyce_dict is used internally for recursion; it should not be
                    referenced in internal calls.
    """

    source = source or globals()

    if cspyce_dict is None:
        cspyce_dict = {}

    # Add names from this source
    names = source.keys()
    for name in names:
        func = source[name]
        if type(func).__name__ != 'function': continue
        if 'SIGNATURE' not in func.__dict__:  continue

        # Stop if this function was already found; break infinite recursion
        if func.__name__ in cspyce_dict: continue

        # Add this function to the dictionary
        cspyce_dict[func.__name__] = func

        # Use the internal dictionary of this function as a recursive source
        _ = get_all_funcs(func.__dict__, cspyce_dict)

    return cspyce_dict

def get_all_versions(func, source=None):
    """Return a dictionary of all cspyce functions associated with this one,
    keyed by their names.

    Inputs:
        func        a cspyce function or the name of a cspyce function.
        source      the dictionary to search if func is specified by name;
                    default is globals().
    """

    func = validate_func(func, source)
    return get_all_funcs(func.__dict__)

def validate_func(func, source=None):
    """Return the cspyce function if this is a valid cspyce function or the name
    of a cspyce function. Otherwise, raise an exception.

    Inputs:
        func        a cspyce function or the name of a cspyce function.
        source      the dictionary to search if func is specified by name;
                    default is globals().
    """

    if type(func) == str:
        full_name = func
        short_name = full_name.split('_')[0]
        source = source or globals()
        try:
            func = source[short_name]
        except KeyError:
            raise KeyError('Unrecognized function name "%s"' % full_name)

    if type(func).__name__ != 'function':
        raise ValueError('Not a function: "%s"' % full_name)

    if 'SIGNATURE' not in func.__dict__:
        raise ValueError('Not a cspyce function: "%s"' % func.__name__)

    return func

################################################################################

# This is the default at initialization
use_errors()

################################################################################
