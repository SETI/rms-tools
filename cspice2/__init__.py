################################################################################
# cspice2/__init__.py
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
# - For some functions, the user has a choice about whether to return a status
#   flag or to raise an exception, typically a KeyError.
#
# In addition, cspice2 provides many additional options for how to processs the
# input arguments and returned quantities. Options are defined by keywords,
# using cspice2.set_options(keyword, ...).
#
#   'NONE'          no type checking of input args is performed.
#   'CHECK'         raises an exception of an arg is of the wrong type.
#   'CONVERT'       tries to convert each argument to the required type.
#   'TRANSLATE'     translates between SPICE codes and SPICE names, depending
#                   on what the function expects. With this option turned on,
#                   body/frame IDs and body/frame names can be used
#                   interchangeably.
#
#   'FLAGS'         the relevant functions return boolean flags, following their
#                   C counterparts.
#   'ERRORS'        the relevant functions raise exceptions instead.
#
#   'ALIASES'       this supports a local alias capability, where a single body
#                   can have multiple names or multiple SPICE IDs (typically due
#                   to historic changes).
#   'NOALIASES'     aliases are not supported.
#
#   'VECTORIZED'    arrays may have additional dimensions to the left of the
#                   shape required for the function. All arrays with additional
#                   dimensions have these dimensions broadcasted together, and
#                   arrays of results are returned. [NOT YET IMPLEMENTED]
#
# For functions that handle aliases, you can override the default to access the
# alternative version of the function by appending '_aliases' or '_noaliases' to
# its name.
#
# Similarly, you can overrride the default error handling by appending '_error'
# or '_flag' to the name of affected functions.
#
# You can also change the default alias handling, globally or on a case-by-case
# basis, using these methods:
#   use_aliases()
#   use_noaliases()
# Similarly, you can change the default error handling, globally or on a
# case-by-case basis, using these methods:
#   use_errors()
#   use_flags()
#
# Furthermore, each function has attributes noalias_version, alias_version,
# error_version and flag_version, which return the function with alternative
# inputs and returns.
#
# More About Aliases:
#
# With the alias option turned on, boddef can take as input a list of names or
# IDs in place of individual values. Values should be given starting with the
# preferred value and then in order of decreasing precedence. For example,
#   boddef(['DIA', 'S2000_J_11'], [553, 55076])
# indicates that the preferred SPICE ID for Jupiter's moon Dia is 553, but it
# was previously described by 55076. Also, it was previously named S2000_J_11.
#
# With the alias option turned on, these function can return multiple values
# instead of a single value:
#   bodn2c, bods2c, bodc2n, bods2n.
# For backward compatibility with older code, this behavior may not be what you
# want. In this case, you can specify these options, in order:
#   set_option(..., 'ALIASES')
#   use_noaliases()
# This first call indicates that aliases will be supported, but the second
# indicates that return values will be unchanged. In general, the preferred
# value of the name or ID will be returned.
#
# When a cspice2 function is called for a body that has aliases, that function
# will first call the equivalent cspice1 function with the preferred value. If
# that call fails, the cspice1 function will be called again with previous
# names or IDs. For example, a call to cspice2.spkez() for Dia will, in effect,
# execute this:
#   try:
#       return cspice1.spkez(553, ...)
#   except KeyError:
#       return cspice1.spkez(55076, ...)
#
# Mark Showalter, PDS Ring-Moon Systems Node, December 4, 2017
################################################################################

import numpy as np
import handlers

VERSION = 2

############################################
# Load info about all cspice1 functions
############################################

import cspice1

CSPICE2_DOCSTRINGS = cspice1.CSPICE1_DOCSTRINGS.copy()
CSPICE2_SIGNATURES = cspice1.CSPICE1_SIGNATURES.copy()
CSPICE2_RETURNS    = cspice1.CSPICE1_RETURNS.copy()
CSPICE2_DEFAULTS   = cspice1.CSPICE1_DEFAULTS.copy()

CSPICE1_FUNC_NAMES      = cspice1.CSPICE1_FUNC_NAMES
CSPICE1_FUNC_BASENAMES  = cspice1.CSPICE1_FUNC_BASENAMES
CSPICE1_ERROR_BASENAMES = cspice1.CSPICE1_ERROR_BASENAMES

############################################
# Load info about all alias functions
############################################

import aliases

ALIAS_FUNC_NAMES      = aliases.ALIAS_FUNC_NAMES
ALIAS_FUNC_BASENAMES  = aliases.ALIAS_FUNC_BASENAMES
ALIAS_ERROR_BASENAMES = aliases.ALIAS_ERROR_BASENAMES

CSPICE2_FUNC_NAMES = []
NEEDS_ALIASES = {}

############################################
# Construct a wrapped copy of the library
############################################

CSPICE2_FUNC_BASENAMES = cspice1.CSPICE1_FUNC_BASENAMES

# Handlers are global
GLOBAL_HANDLERS = None

def apply_default_handlers(func):
    """Wrapper function to apply the default handler to function inputs."""

    global GLOBAL_HANDLERS

    def wrapper(*args):
        return exec_with_handlers(func, GLOBAL_HANDLERS, *args)

    return wrapper

# Create a wrapper for every cspice1 function not in aliases
func_dict = cspice1.__dict__
for name in cspice1.CSPICE1_FUNC_NAMES:

    # aliases override cspice1
    if name in aliases.ALIAS_FUNC_NAMES:
        continue

    func1 = func_dict[name]
    func2 = apply_default_handlers(func1)
    func2.__name__   = name
    func2.__doc__    = func1.__doc__
    func2.func_defaults = func1.func_defaults
    func2.SIGNATURE  = func1.SIGNATURE
    func2.RETURNS    = func1.RETURNS
    globals()[name]  = func2

    CSPICE2_FUNC_NAMES.append(name)

    # Add the attributes alias_version and noalias_version to each function
    func2.alias_version = func2
    func2.noalias_version = func2

# Create a wrapper for every cspice function in aliases
func_dict = aliases.__dict__
for name in aliases.ALIAS_FUNC_NAMES:
    func1 = func_dict[name]
    func2 = apply_default_handlers(func1)
    func2.__name__ = name
    func2.__doc__  = func1.__doc__
    func2.func_defaults = func1.func_defaults
    func2.SIGNATURE = func1.SIGNATURE
    func2.RETURNS   = func1.RETURNS
    globals()[name] = func2

    CSPICE2_FUNC_NAMES.append(name)

CSPICE2_FUNC_NAMES.sort()

# Add the attributes alias_version and noalias_version to each alias function
CSPICE2_ALIAS_SHORTNAMES = []
for name in aliases.ALIAS_FUNC_NAMES:
    func = globals()[name]
    short_key = aliases._strip_aliases(name)
    CSPICE2_ALIAS_SHORTNAMES.append(short_key)

    long_key = aliases._insert_into_name(short_key, '_aliases')
    func.alias_version = globals()[long_key]

    long_key = aliases._insert_into_name(short_key, '_noaliases')
    func.noalias_version = globals()[long_key]

CSPICE2_ALIAS_SHORTNAMES = list(set(CSPICE2_ALIAS_SHORTNAMES))
CSPICE2_ALIAS_SHORTNAMES.sort()

CSPICE2_ALIAS_BASENAMES = [cspice1._strip_error_flag(n)
                           for n in CSPICE2_ALIAS_SHORTNAMES]
CSPICE2_ALIAS_BASENAMES = list(set(CSPICE2_ALIAS_BASENAMES))
CSPICE2_ALIAS_BASENAMES.sort()

# Add the attributes error_version and flag_version to each function
CSPICE2_ERROR_SHORTNAMES = []
for name in CSPICE2_FUNC_NAMES:

    func = globals()[name]
    short_key = cspice1._strip_error_flag(name)

    long_key = short_key + '_error'
    if long_key in globals():
        func.error_version = globals()[long_key]
        func.flag_version  = globals()[short_key + '_flag']
#         func.flag_version.__name__ = short_key + '_flag'    # assign fixed name
        CSPICE2_ERROR_SHORTNAMES.append(short_key)
    else:
        func.error_version = func
        func.flag_version = func

CSPICE2_ERROR_SHORTNAMES = list(set(CSPICE2_ERROR_SHORTNAMES))
CSPICE2_ERROR_SHORTNAMES.sort()

CSPICE2_ERROR_BASENAMES = [aliases._strip_aliases(n)
                           for n in CSPICE2_ERROR_SHORTNAMES]
CSPICE2_ERROR_BASENAMES = list(set(CSPICE2_ERROR_BASENAMES))
CSPICE2_ERROR_BASENAMES.sort()

################################################################################
# Functions to select between the *_error and *_flag versions of functions
################################################################################

def use_errors(*names):
    """Switch all functions, or just those listed, to raise exceptions instead
    of returning flags."""

    if names:
        short_names = [cspice1._strip_error_flag[n] for n in names]
        short_names = [n for n in short_names if n in CSPICE2_ERROR_SHORTNAMES]
        short_names = set(short_names)
    else:
        short_names = CSPICE2_ERROR_SHORTNAMES

    for short_name in short_names:
        globals()[short_name] = globals()[short_name].error_version
#         globals()[short_name].__name__ = short_name

def use_flags(*names):
    """Switch all functions, or just those listed, to return flags instead of
    raising exceptions."""

    if names:
        short_names = [cspice1._strip_error_flag[n] for n in names]
        short_names = [n for n in short_names if n in CSPICE2_ERROR_SHORTNAMES]
        short_names = set(short_names)
    else:
        short_names = CSPICE2_ERROR_SHORTNAMES

    for short_name in short_names:
        globals()[short_name] = globals()[short_name].flag_version
#         globals()[short_name].__name__ = short_name

################################################################################
# Functions to select between the *_aliases and *_noaliases versions of
# functions. These cannot be called externally because they also require
# extra handlers.
################################################################################

def use_aliases(*names):
    """Switch the named functions, or else all relevant alias functions, to use
    aliases."""

    if names:
        short_names = [cspice1._strip_error_flag(n) for n in names]
        basenames = [aliases._strip_aliases(n) for n in short_names]
        for basename in basenames:
            if basename not in CSPICE2_FUNC_BASENAMES:
                raise ValueError('Unrecognized cspice function "%s"' % n)
        basenames = [n for n in basenames if n in CSPICE2_ALIAS_BASENAMES]
        basenames = set(basenames)
    else:
        basenames = CSPICE2_ALIAS_BASENAMES

    for basename in basenames:
      for suffix in ('', '_error', '_flag'):
        short_name = basename + suffix
        if short_name in CSPICE2_FUNC_NAMES:
            long_name = aliases._insert_into_name(short_name, '_aliases')
            globals()[short_name] = globals()[long_name]
#             globals()[short_name].__name__ = short_name

def use_noaliases(*names):
    """Switch the named functions, or else all relevant alias functions, to
    ignore aliases."""

    if names:
        short_names = [cspice1._strip_error_flag(n) for n in names]
        basenames = [aliases._strip_aliases(n) for n in short_names]
        for basename in basenames:
            if basename not in CSPICE2_FUNC_BASENAMES:
                raise ValueError('Unrecognized cspice function "%s"' % n)
        basenames = [n for n in basenames if n in CSPICE2_ALIAS_BASENAMES]
        basenames = set(basenames)
    else:
        basenames = CSPICE2_ALIAS_BASENAMES

    for basename in basenames:
      for suffix in ('', '_error', '_flag'):
        short_name = basename + suffix
        if short_name in CSPICE2_FUNC_NAMES:
            long_name = aliases._insert_into_name(short_name, '_noaliases')
            globals()[short_name] = globals()[long_name]
#             globals()[short_name].__name__ = short_name

################################################################################
################################################################################
################################################################################
# How to select handlers and options
################################################################################

def set_options(*names):

    global GLOBAL_HANDLERS

    (handler_dict, extras) = handlers.select_options(*names)
    
    if 'ALIASES' in extras and 'NOALIASES' in extras:
        raise ValueError("The ALIASES and NOALIASES options are incompatible.")

    if 'ERRORS' in extras and 'FLAGS' in extras:
        raise ValueError("The ERRORS and FLAGS options are incompatible.")

    if 'ALIASES' in extras:
        use_aliases()
    elif 'NOALIASES' in extras:
        use_noaliases()

    if 'ERRORS' in extras:
        use_errors()
    elif 'FLAGS' in extras:
        use_flags()

    GLOBAL_HANDLERS = handler_dict

# Define default at startup
# - Errors, not flags
# - No handling of input arguments

set_options('ERRORS')

################################################################################
################################################################################
################################################################################
# Complete wrapper to execute a CSPICE function
################################################################################

def exec_with_handlers(func, handlers, *args):

    # Handle case of no checking quickly
    if handlers is None:
        return func.__call__(*args)

    # Locate the first optional argument
    signature = func.SIGNATURE
    first_optional = len(signature)
    if func.func_defaults:
        first_optional -= len(func.func_defaults)

    # Create an updated list of args
    vectorized_shapes = 0
    vectorized_indices = []
    aliased_indices = []

    args = list(args)
    for k in range(len(signature)):
        argtype = signature[k]
        arg = args[k]

        # Make sure we have enough args
        if k >= len(args):
            if k >= first_optional: break
            raise ValueError('Function %s argument %d ' % (func.__name__, k+1) +
                             'is missing')

        # Handle an arg
        handler = handlers[argtype]
        if handler:
            arg = handler.__call__(arg, k, func)

        # Look for vectorization and aliases
        if type(arg) == tuple:
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

    return _alias_iterator(func, args, aliased_indices, broadcast_shape,
                           vectorized_shapes, vectorized_indices)

def _broadcast_shapes(shapes):
    """Return the shape (as a list) resulting from broadcasting together all of
    the given shapes. Also update all shapes to the same rank."""

    broadcasted = []
    for shape in shapes:
        old_shape = shape
        old_broadcasted = broadcasted

        shape = list(shape)

        while len(shape) < len(broadcasted):
            shape = [1] + shape
        while len(broadcasted) < len(shape):
            broadcasted = [1] + broadcasted

        for k in range(len(shape)):
            if shape[k] != 1:
                if broadcasted[k] == 1:
                    broadcasted[k] = shape[k]
                elif broadcasted[k] != shape[k]:
                    raise ValueError('Array shapes cannot be broadcasted:' +
                                     ' %s, %s' % (str(old_shape),
                                                  str(tuple(old_broadcasted))))

    rank = len(broadcasted)
    new_shapes = []
    for shape in shapes:
        shape = list(shape)
        if len(shape) < rank:
            new_shape = (rank - len(shape)) * [1] + shape

        new_shapes.append(new_shape)

    return (broadcasted, new_shapes)

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
                    return func.error_version.__call__(*local_args)
                except Exception as e:
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

################################################################################
################################################################################
################################################################################
# Set up for backward compatibility
################################################################################

use_errors()

################################################################################
