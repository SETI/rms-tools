################################################################################
# cspyce/array_suppport.py
# Used internally by cspyce; not intended for direct import.
################################################################################

import numpy as np

import cspyce
import cspyce.cspyce1 as cspyce1
from cspyce.alias_support import alias_version

################################################################################
# cspyce array function wrapper
################################################################################

ARRAY_NOTE = """
This version supports array inputs in place of any floating-point inputs. Array
shapes are broadcasted following NumPy rules. This function vectorizes the call
so that any iteration is performed inside C code an is faster than Python
iteration.
"""

def _array_name(name):
    return name.replace('_vector', '_array')

def _arrayize_arglist(arglist):
    arrayized = []
    for arg in arglist:
        arrayized.append(arg.replace('[*', '[...'))

    return arrayized

def array_version(func):
    """Wrapper function to apply NumPy broadcasting rules to the vectorized
    inputs of any cspyce function.
    """

    if hasattr(func, 'array'):
        return func.array

    # Handle vector-free functions quickly
    if '_vector' not in func.__name__ and func.vector is func:
        func.array = func
        return func

    # Apply vector in front of alias option, via recursion
    # Note: repair alias links after all the array functions are defined
    if '_alias' in func.__name__:
        noalias_array_func = array_version(func.noalias)
        alias_array_func = alias_version(noalias_array_func)

        alias_array_func.array = alias_array_func
        func.array = alias_array_func
        return alias_array_func

    # Handle scalar versions of vector functions via recursion
    if '_vector' not in func.__name__:
        array_func = array_version(func.vector)
        func.array = array_func
        return func

    # Identify the names and locations of arguments that can be vectorized;
    # store their ranks in a dictionary
    if not hasattr(func, 'BROADCAST_RANKS'):
        broadcast_ranks = {}
        for k in range(len(func.ARGNAMES)):
            sig = func.SIGNATURE[k]
            parts = sig.split('[')
            if parts[0] in ('int', 'bool', 'string'): continue

            if len(parts) == 1:
                rank = 0
            else:
                rank = len(parts[1].split(','))

            broadcast_ranks[k] = rank
            broadcast_ranks[func.ARGNAMES[k]] = rank

        func.BROADCAST_RANKS = broadcast_ranks

    if not func.BROADCAST_RANKS:
        func.array = func.vector
        return func

    def wrapper(*args, **keywords):
        return _exec_with_broadcasting(func, *args, **keywords)

    # Copy type info but not function version links
    for (key, value) in func.__dict__.iteritems():
        if type(value).__name__ != 'function':
            wrapper.__dict__[key] = value

    # After copy, revise SIGNATURE, RETURNS, and NOTES
    wrapper.SIGNATURE = _arrayize_arglist(func.SIGNATURE)
    wrapper.RETURNS   = _arrayize_arglist(func.RETURNS)
    wrapper.NOTES     = [ARRAY_NOTE] + wrapper.NOTES[1:] # replace vector note

    # Save key attributes of the wrapper function before returning
    cspyce.assign_docstring(wrapper)
    wrapper.__name__ = _array_name(func.__name__)
    wrapper.func_defaults = func.func_defaults

    # Insert mutual links
    wrapper.array  = wrapper
    wrapper.vector = func
    wrapper.scalar = func.scalar

    func.array = wrapper

    return wrapper

def _exec_with_broadcasting(func, *args, **keywords):
    """Main function to broadcast together the shapes of the input arguments
    and return results with the broadcasted shape."""

    # Identify arguments needing broadcasting
    arg_ranks = []
    arg_indices = []

    for k in range(len(args)) + keywords.keys():

        rank = func.BROADCAST_RANKS.get(k, None)
        if rank is None: continue

        # Get argument
        if type(k) == int:
            arg = args[k]
        else:
            arg = keywords[k]

        # Ignore args that are not arrays
        if not isinstance(arg, np.ndarray): continue

        # Determine leading shape, if any
        if rank == 0:
            shape = arg.shape
        else:
            shape = arg.shape[:rank]

        if shape == (): continue
        if shape == (1,): continue

        arg_ranks.append(rank)
        arg_indices.append(k)

    # Call function now if iteration is not needed
    if not arg_indices:
        return func.__call__(*args, **keywords)

    # Broadcast the arrays
    cspyce1.chkin(func.array.__name__)
    (broadcasted_shape, reshaped_args) = _broadcast_arrays(arg_ranks, args)
    if cspyce1.failed():
        cspyce1.chkout(func.array.__name__)
        return None

    # Update the argument list with flattened arrays
    args = list(args)
    for (k,reshaped_arg) in zip(arg_indices, reshaped_args):
        flattened_arg = np.ravel(reshaped_arg)
        if type(k) == int:
            args[k] = flattened_arg
        else:
            keywords[k] = flattened_arg

    # Execute the function
    results = func.__call__(*args, **keywords)
    cspyce1.chkout(func.array.__name__)

    if cspyce1.failed():
        return results

    # Reshape the results
    if isinstance(results, np.ndarray):
        return np.reshape(results, broadcasted_shape)

    reshaped_results = []
    for result in results:
        reshaped_results.append(np.reshape(result, broadcasted_shape))

    return reshaped_results

def _broadcast_arrays(ranks, args):
    """Return the shape resulting from broadcasting together all of the given
    shapes. Also update all shapes to the same rank."""

    broadcasted = []
    lbroad = 0
    shapes = []
    for (array, rank) in zip(args, ranks):
        shape = array.shape
        if rank:
            shape = shape[:-rank]
        lshape = len(shape)
        shapes.append(shape)

        if lbroad < lshape:
            broadcasted = list(shape)[:(lshape - lbroad)] + broadcasted
            lbroad = lshape

        for i in range(1,lshape+1): # work starting from right
            broadcasted[-i] = max(broadcasted[-i], shape[-i])

    scaled_arrays = []
    scalings = []
    for (shape,array) in zip(shapes,args):
        scaling = []
        lshape = len(shape)

        for i in range(1,lshape+1): # work starting from right
          if (shape[-i] != 1 and broadcasted[-i] != shape[-i]):
            cspyce1.setmsg('Incompatible shapes for broadcasting: ' +
                          '%s, %s' %  (str(tuple(shape)),
                                       str(tuple(broadcasted))))
            cspyce1.sigerr('SPICE(INVALIDARRAYSHAPE)')
            return (None,None)

          scaling.append(broadcasted[-i] // shape[-i])
        scaling = scaling[::-1]

        # We do not need to scale the leading axis, because of how the _vector
        # methods cycle through the array indices.
        for i in range(lshape):
            if shape[i] == 1:
                scaling[i] = 1
                continue

            scaling[i] = 1
            break

        scalings.append(scaling)

        # Convert to contiguous arrays with compatible shapes
        if prod(scaling) == 1:
            array = np.ascontiguousarray(array)
        else:
            array = _reshaped_array(scaling, rank, array)

        scaled_arrays.append(array)

    return (broadcasted, scaled_arrays)

def _reshaped_array(scaling, rank, array):
    """Return an array that can safely be flattened in such a way that it will
    work inside a cspyce vectorized function."""

    # Save the original shape and core shape
    if rank == 0:
        old_shape = array.shape
        core_shape = []
    else:
        old_shape = array.shape[:-rank]
        core_shape = list(array.shape[-rank:])

    # Determine a new shape that will broadcast to the desired shape, allowing
    # for the _vector procedure to cycle through the leading axis if necessary.
    temp_shape = []
    new_shape = []
    for (axis, scale) in zip(old_shape, scaling):
        if scale == 1:
            temp_shape.append(axis)
            new_shape.append(axis)
        else:
            temp_shape.append(1)
            temp_shape.append(axis)
            new_shape.append(scale)
            new_shape.append(axis)

    # At this point, temp_shape has the same size as old_shape, but with added
    # an added unit axis in front of each axis that must be duplicated in
    # memory. It is safe to reshape the given array to this shape.
    array = np.reshape(array, temp_shape + core_shape)

    # At this point, new_shape has the same rank as temp_shape, but each new
    # axis of temp_shape is aligned with an axis in new_shape that contains the
    # axis scale factor. Broadcasting is now a safe operation.
    array = np.broadcast_to(array, new_shape + core_shape)

    # Conversion to a contiguous array ensures that any stride tricks are
    # eliminated; array elements are duplicated if necessary.
    array = np.ascontiguousarray(array)

    return array

################################################################################
# Define the alias function selector
################################################################################

SPYCE_DICT = cspyce.__dict__

def use_arrays(*funcs):
    """Switch the listed functions or names of functions to use the "array"
    version by default. This affects all versions of any given cspyce function.
    If the list is empty, apply this operation to all cspyce functions.
    """

    if funcs:
        cspyce.GLOBAL_STATUS.add('ARRAYS')
        cspyce.GLOBAL_STATUS.discard('VECTORS')
        cspyce.GLOBAL_STATUS.discard('SCALARS')
    else:
        cspyce.GLOBAL_STATUS.discard('ARRAYS')
        cspyce.GLOBAL_STATUS.discard('VECTORS')
        cspyce.GLOBAL_STATUS.discard('SCALARS')

    for name in cspyce._get_func_names(funcs, source=SPYCE_DICT):
        if 'alias' not in name:
            SPYCE_DICT[name] = SPYCE_DICT[name].alias

    for name in cspyce._get_func_names(funcs, source=SPYCE_DICT):
        if ('scalar' not in name and 'vector' not in name
                                 and 'array' not in name):
            SPYCE_DICT[name] = SPYCE_DICT[name].array

################################################################################
# Function to define array versions and links for all cspyce functions
################################################################################

def _define_all_array_versions():
    """Generate all missing array functions and set the "array" attributes for
    all cspyce functions.

    This routine can be run multiple times. At each run, it only creates
    whatever is missing.
    """

    # Define an _array function for each cspyce _vector function
    avpairs = []
    funcs = cspyce.get_all_funcs(SPYCE_DICT).values()

    # Do non-alias versions first; otherwise some .array attributes are broken
    for func in funcs:
        if 'alias' in func.__name__: continue

        afunc = array_version(func)
        if afunc is func: continue      # function could not use arrays

        aname = afunc.__name__
        SPYCE_DICT[aname] = afunc

        if '_vector' in func.__name__:
            avpairs.append((afunc, func))

    for func in funcs:
        if 'alias' not in func.__name__: continue

        afunc = array_version(func)
        if afunc is func: continue      # function could not use arrays

        aname = afunc.__name__
        SPYCE_DICT[aname] = afunc

        if '_vector' in func.__name__:
            avpairs.append((afunc, func))

    # At this point, every vector function has an array function counterpart.
    # Also, every function has an "array" attribute, which points to itself if
    # there is no array version. However, the new array functions still need
    # internal links to other associated versions.

    # Fill in missing version attributes for every array function
    for (afunc, func) in avpairs:
        _define_missing_versions_for_array(afunc, func)

def _define_missing_versions_for_array(afunc, vfunc):
    """Complete the missing version attributes for a given array function."""

    for (key, version) in vfunc.__dict__.iteritems():
        if type(version).__name__ != 'function': continue
        if afunc.__name__[:5] == 'vsclg': print key
        if key in ('vector','scalar','array'):
            if afunc.__name__[:5] == 'vsclg': print 'copied!'
            afunc.__dict__[key] = version
        else:
            version_name = version.__name__.replace('_vector','_array')
            if afunc.__name__[:5] == 'vsclg': print version_name, SPYCE_DICT[version_name]
            afunc.__dict__[key] = SPYCE_DICT[version_name]

################################################################################
