################################################################################
# cspice/cspice2/handlers.py
################################################################################

import numpy as np
import cspice1
import aliases

HANDLERS = {}

# A handler is a dictionary keyed by the argument type. It returns the
#       function to use when pre-processing that argument. None indicates
#       that no pre-processing is to be performed.

# This is the complete list of array types used in CSPICE input
ARRAY_TYPES = [
    'float[*]',
    'float[3]',
    'float[4]',
    'float[6]',
    'float[8]',
    'float[9]',
    'float[*,*]',
    'float[*,3]',
    'float[2,2]',
    'float[3,3]',
    'float[6,6]',
    'int[*]',
    'string[*]'
]

# Associate an array type to legal values of np.dtype.kind
DTYPE_KINDS = {
    'float' : 'f',
    'int'   : 'ui',
    'string': 'S',
    'bool'  : 'b',
}

HANDLERS['NONE'] = {
    'int'       : None,
    'float'     : None,
    'string'    : None,
    'bool'      : None,
    'body_name' : None,
    'body_code' : None,
    'body_name_default': None,  # used to revert back from aliases to no aliases
    'body_code_default': None,
    'frame_name': None,         # frame aliases are not currently implemented
    'frame_code': None,
}

# Add a handler for each array type
for argtype in ARRAY_TYPES:
    HANDLERS['NONE'][argtype] = None

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


HANDLERS['CHECK'] = {
    'int'       : _check_int,
    'float'     : _check_float,
    'string'    : _check_string,
    'bool'      : _check_bool,
    'body_name' : _check_string,
    'body_code' : _check_int,
    'body_name_default': _check_string,
    'body_code_default': _check_int,
    'frame_name': _check_string,
    'frame_code': _check_int,
}

# Function to return a CHECK handler for each array type
def _check_array_func(argtype):
    """Returns a function that checks a particular array type."""

    (DTYPE, shapestr) = argtype.split('[')
    SHAPE = eval('(' + shapestr[:-1].replace('*','0') + ',)')

    RANK = len(SHAPE)
    KINDS = DTYPE_KINDS[DTYPE]

    def _check_array_wrapper(arg, k, func):

        # Allow for lists and tuples
        if isinstance(arg, (list,tuple)):
            arg = np.array(arg)

        # Confirm that this is an array
        if not isinstance(arg, np.ndarray):
            raise ValueError('Function %s argument %d ' % (func.__name__, k+1) +
                             'is not an array')

        # Confirm rank
        if len(arg.shape) != RANK:
            raise ValueError('Function %s argument %d ' % (func.__name__, k+1) +
                             'is not a %d-D array' % RANK)

        # Confirm shape
        for k in range(RANK):
          if SHAPE[k] != 0 and SHAPE[k] != arg.shape[k]:
            raise ValueError('Function %s argument %d ' % (func.__name__, k+1) +
                             'is not an array with shape %s' % SHAPE)

        # Confirm type
        if arg.dtype.kind not in KINDS:
            raise ValueError('Function %s argument %d ' % (func.__name__, k+1) +
                             'is not an array of dtype %s' % DTYPE)

        return arg

    return _check_array_wrapper

# Add a CHECK handler for each array type
for argtype in ARRAY_TYPES:
    HANDLERS['CHECK'][argtype] = _check_array_func(argtype)

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
            arg = np.asfarray(arg)

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

HANDLERS['CONVERT'] = {
    'int'       : _cast_to_int,
    'float'     : _cast_to_float,
    'string'    : _cast_to_string,
    'bool'      : _cast_to_bool,
    'body_name' : _cast_to_string,
    'body_code' : _cast_to_int,
    'body_name_default': _cast_to_string,
    'body_code_default': _cast_to_int,
    'frame_name': _cast_to_string,
    'frame_code': _cast_to_int,
}

# Function to return a CHECK handler for each array type
def _convert_array_func(argtype):
    """Returns a function that checks a particular array type."""

    (DTYPE, shapestr) = argtype.split('[')
    SHAPE = eval('(' + shapestr[:-1].replace('*','0') + ',)')

    RANK = len(SHAPE)
    KINDS = DTYPE_KINDS[DTYPE]

    def _convert_array_wrapper(arg, k, func):

        # Allow for lists and tuples
        if type(arg) in (list, tuple):
            arg = np.array(arg)

        # Convert a scalar to an array of shape (1,)
        if np.shape(arg) == ():
            arg = np.array([arg])

        # Make sure it is an array
        if not isinstance(arg, np.ndarray):
            raise ValueError('Function %s argument %d ' % (func.__name__, k+1) +
                             'is not an array')

        # Expand rank if necessary
        lshape = len(arg.shape)
        if lshape < RANK:
            newshape = tuple((RANK - lshape) * [1] + list(arg.shape))
            arg = arg.reshape(newshape)

        # Confirm rank
        if not len(arg.shape) != RANK:
            raise ValueError('Function %s argument %d ' % (func.__name__, k+1) +
                             'is not convertible to a %d-D array' % RANK)

        # Confirm shape
        for k in range(RANK):
          if SHAPE[k] != 0 and SHAPE[k] != arg.shape[k]:
            raise ValueError('Function %s argument %d ' % (func.__name__, k+1) +
                             'is not an array with shape %s' % SHAPE)

        # Convert type if necessary
        if arg.dtype.kind not in KINDS:
          try:
            if DTYPE == 'float':
                arg = np.asfarray(arg)
            else:
                arg = arg.astype(DTYPE)
          except Error:
            raise ValueError('Function %s argument %d ' % (func.__name__, k+1) +
                             'is not an array of dtype %s' % DTYPE)

        return arg

    return _convert_array_wrapper

# Add a CHECK handler for each array type
for argtype in ARRAY_TYPES:
    HANDLERS['CONVERT'][argtype] = _convert_array_func(argtype)

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

    arg = aliases._clean_name(str(arg))
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

    arg = aliases._clean_name(arg)
    raise ValueError('Function %s argument %d ' % (func.__name__, k+1) +
                     'does not identify a SPICE frame: %s' % arg)

HANDLERS['TRANSLATE'] = {
    'body_name' : _to_body_name,
    'body_code' : _to_body_code,
    'body_name_default': _to_body_name,
    'body_code_default': _to_body_code,
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

    results = aliases._bodn2c_for_aliases(arg)
    if results:
        if len(results) == 1:
            return results[0]
        else:
            return ('aliases', results)

    raise ValueError('Function %s argument %d ' % (func.__name__, k+1) +
                     'does not identify a SPICE body: %s' % str(arg))

def _to_body_names(arg, k, func):
    """Return a list of body names given an body code or name. Return a single
    value if the list length is 1."""

    results = aliases._bodc2n_for_aliases(arg)
    if results:
        if len(results) == 1:
            return results[0]
        else:
            return ('aliases', results)

    raise ValueError('Function %s argument %d ' % (func.__name__, k+1) +
                     'does not identify a SPICE body: %s' % str(arg))

HANDLERS['ALIASES'] = {
    'body_name': _to_body_names,
    'body_code': _to_body_codes,
}

################################################################################
################################################################################
################################################################################
# Functions that allow vectorized float arguments.
# If a float argument has an extra leading axis, it returns a tuple:
#   ('vectorized', arg, leading_shape)
################################################################################

def _cast_to_float_vectorized(arg, k, func):

    # Allow for lists and tuples
    if type(arg) in (list, tuple):
        arg = np.array(arg)

    try:
        if isinstance(arg, np.ndarray):
            if arg.shape == ():
                return float(arg[()])
            else:
                return ('vectorized', np.asfarray(arg), arg.shape)
        else:
            return float(arg)

    except ValueError:
        raise ValueError('Function %s argument %d ' % (func.__name__, k+1) +
                         'cannot be converted to type float')

HANDLERS['VECTORIZED'] = {
    'float': _cast_to_float_vectorized
}

# Function to return a VECTORIZE handler for array types
def _vectorize_array_func(argtype):
    """Returns a function that checks a particular array type."""

    (DTYPE, shapestr) = argtype.split('[')
    SHAPE = eval('(' + shapestr[:-1].replace('*','0') + ',)')

    RANK = len(SHAPE)
    KINDS = DTYPE_KINDS[DTYPE]

    def _vectorize_array_wrapper(arg, k, func):

        # Allow for lists and tuples
        if type(arg) in (list, tuple):
            arg = np.array(arg)

        # Convert a scalar to an array of shape (1,)
        if np.shape(arg) == ():
            arg = np.array([arg])

        # Make sure it is an array
        if not isinstance(arg, np.ndarray):
            raise ValueError('Function %s argument %d ' % (func.__name__, k+1) +
                             'is not an array')

        # Convert to float if necessary
        arg = np.asfarray(arg)

        # Expand rank if necessary
        lshape = len(arg.shape)
        if lshape < RANK:
            newshape = (RANK - lshape) * (1,) + arg.shape
            arg = arg.reshape(newshape)

        # Confirm trailing shape
        for k in range(1,RANK+1):
          if SHAPE[-k] != 0 and SHAPE[-k] != arg.shape[-k]:
            raise ValueError('Function %s argument %d ' % (func.__name__, k+1) +
                             'is not an array with trailing shape %s' % SHAPE)

        return ('vectorized', arg, arg.shape[:-RANK])

    return _vectorize_array_wrapper

# Add a CHECK handler for each floating array type
for argtype in ARRAY_TYPES:
    if argtype.startswith('float'):
        HANDLERS['VECTORIZED'][argtype] = _vectorize_array_func(argtype)

################################################################################
################################################################################

ORDERED_HANDLERS = ('NONE', 'CHECK', 'CONVERT', 'TRANSLATE', 'ALIASES',
                    'VECTORIZED')
EXTRA_OPTIONS = ('ERRORS', 'FLAGS', 'NOALIASES')

def select_options(*names):
    """Return a dictionary of handlers based on a list of keywords, plus any
    extra options."""

    # Make sure all rules are valid
    names = [n.upper() for n in names]
    for name in names:
        if name not in ORDERED_HANDLERS + EXTRA_OPTIONS:
            raise ValueError('Unrecognized rule "%s"' % name)

    # Convert to set
    names = set(names)

    # Remove 'NONE' if it appears
    try:
        names.remove('NONE')
    except KeyError:
        pass

    # Return None for an empty handler
    if not names:
        return None

    # Assemble the handlers
    handler_dict = HANDLERS['NONE'].copy()

    for handler in ORDERED_HANDLERS:
        if handler in names:
            # Remove handlers from list, but keep ALIASES because it also
            # indicates which versions of functions to use.
            if handler != 'ALIASES':
                names.remove(handler)

            # Copy functions in to handler dictionary
            for (key, value) in HANDLERS[handler].iteritems():
                handler_dict[key] = value

    return (handler_dict, names)

################################################################################

