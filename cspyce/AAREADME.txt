================================================================================
                             CSPYCE MODULE OVERVIEW
                                  Version 0.9
                                 December, 2017

          Mark Showalter, PDS Ring-Moon Systems Node, SETI Institute
================================================================================

Spyce is a Python module that provides an interface to the CSPICE library. It
implements the most widely-used functions of CSPICE in a Python-like way. It
also supports numerous enhancements, including support for Python exceptions,
array inputs, and aliases.

PYTHONIZATION

This module has been designed to replicate the core features of CSPICE for
users who wish to translate a program that already exists. Function names in
cspyce match their CSPICE names.

However, it is also designed to behave as much as possible like a normal
Python module. To that end, it has the following features.

- The C language requires buffers to be allocated for output and it requires
  array sizes to be include for both input and output. The cspyce module,
  instead, eliminates all extraneous inputs, and all output arguments are
  returned as a list (or as a single object if the function only returns one
  item).

- The module has been fully integrated with Python's exception handling,
  programmers can still opt to use CSPICE's error handling mechanism if they
  wish to.

- All cspyce functions can handle positional arguments as well as arguments
  passed by name.

- All cspyce functions have informative docstrings, so typing
      help(function)
  provides useful information.

- Many cspyce functions take sensible default values if input arguments are
  omitted.

- The CSPICE concepts of "windows" and "cells" are not needed in Python. In 
  CSPICE, these allow a function to return a variable amount of information,
  which the program can then iterate through. The cspyce counterpart of each of
  these functions simply returns a complete list of the results.

ENHANCEMENTS

In addition, the cspyce module takes advantage of features of the Python
language to provide numerous options about how the functions perform their work.
These options include:

- Whether to return a CSPICE-style error condition or to raise a Python
  exception.

- How to handle CSPICE functions that return a status flag, e.g., "found" or
  "ok", instead of using the CSPICE toolkit's error handling mechanism.

- Whether to allow cspyce functions to accept arrays of inputs all at once,
  rather than looping through inputs in Python.

- Whether to automate the translation between SPICE body and frame IDs and their
  associated names.

- Whether to allow cspyce to support aliases, in which the same body or frame
  is associated with alternative names or IDs.

================================================================================
EXCEPTION HANDLING

As in CSPICE, the user can designate what to do in the event of an error
condition using function erract(). In CSPICE, those options are "RETURN",
"REPORT", "IGNORE", "ABORT", and "DEFAULT". This function adds new options
"EXCEPTION" and "RUNTIME" to the suite of error handling options supported by
CPICE.

- As usual, the user can select the exception handling mechanism to use by
  calling the function erract(). In cspyce, the default is "EXCEPTION".

- When using one of CSPICE's error handling methods, a call to failed() will
  reveal whethen an error has occurred, and a call to reset() is needed to
  clear the error.

- Care has been taken to reduce the chances that the "dangerous" options
  "IGNORE" and "REPORT" will cause a segmentation fault. However, this
  possibiliyt cannot be entirely ruled out, so caution is advised.

- Because it would be a highly questionable thing to do, the "ABORT" and
  "DEFAULT" options are overridden by "EXCEPTION" when the user is running
  cspyce from an interactive shell. However, they resume their standard effects
  during non-interactive runs.

- When using the "EXCEPTION" option, each CSPICE error condition raises a
  Python exception rather than setting the failed() flag. The exception
  contains the text of the CSPICE error, in the form (short message + " -- " +
  long message).

- The CSPICE error conditions are mapped to standard Python exception types in
  a sensible way:
  - KeyError indicates that a SPICE ID or name is unrecognized.
  - ValueError indicates that one of the inputs to a function had an invalid
    value.
  - TypeError indicates that one of the inputs to a function had an invalid
    type.
  - IndexError indicates that an integer index is out of range.
  - IOError indicates errors with reading and writing files, including SPICE
    kernels. IOError can also indicate that needed information was not in one
    of the furnished kernels.
  - MemoryError indicates that adequate memory could not be allocated, or
    that the defined size of a memory buffer in C is too small.
  - ZeroDivisionError indicates that a divide-by-zero has occurred.
  - RuntimeError indicates that an action is incompatible with some aspect
    of the CSPICE module's internal configuration.

- When using the "RUNTIME" option, each CSPICE error condition raises a
  Python RuntimeError exception rather than setting the failed() flag. This is
  similar to the "EXCEPTION" option except the type of exception is always the
  same.

- Certain out-of-memory conditions are beyond the control of the CSPICE
  library. These will always raise a MemoryError exception, regardless of the
  exception handling method chosen.

HANDLING OF ERROR FLAGS: Many CSPICE functions bypass the library's own error
handling mechanism; instead they return a status flag, sometimes called "found"
or "ok", or perhaps an empty response to indicate failure. The cspyce module
provides alternative options for these functions.

Within cspyce, functions that return error flags have an alternative
implementation with a suffix of "_error", which uses the CSPICE/cspyce error
handling mechanism instead.

Note that most _error versions of functions have fewer return values than the
associated non-error versions. The user should be certain which version is being
used before interpreting the returned value(s).

The cspyce module provides several ways to control which version of the function
to use:

- The function use_flags() takes a function name or list of names and designates
  the original version of each function as the default. If the input argument is
  missing.

- The function use_errors() takes a function name or list of names and
  designates the _error version of each function as the default. If the input
  argument is missing, _error versions are selected universally. With this
  option, for example, a call to cspyce1.bodn2c() will actually call
  cspyce1.bodn2c_error() instead.

For backward compatibilty with our original Python cspice library, the _error
versions of all cspice functions are selected by default.

You can also choose between the "flag" and "error" versions of a function using
cspyce function attributes, as discussed below.

================================================================================
VECTORS AND ARRAYS

VECTORIZATION: Nearly every function that takes floating-point input (be it a
scalar, 1-D array, or 2-D array) has a vectorized version, which allows you to
pass a vector of these items in place of a single value. The CSPICE function is
called for each of the provided inputs and the function returns a vector of
results.

- Vectorized versions have the same name but with "_vector" appended.

- In a vectorized function, you can replace any or all floating-point input
  parameters with a array having one extra leading dimension. Integer, boolean,
  and string inputs cannot be replaced by arrays.

- If no inputs have an extra dimension, then the result is the same as
  calling the original, un-vectorized function.

- Otherwise, all returned quantities are replaced by arrays having the size of
  the largest leading axis.

- Note that it is permissible to pass arrays with different leading axis sizes
  to the function. The vectorized function cycles through the elements of each
  array repeatedly if necessary. It may make sense to do this if each leading
  axis is an integer fraction of the largest axis size. For example, if the
  first input array has size 100 and the second has size 25, then the the
  returned arrays(s) will have 100 elements and the values of the second
  will each be used four times. However, caution is advised when using this
  capability.

- Some functions are not vectorized. These include:
  - Functions that have no floating-point inputs.
  - Functions that include strings among the returned quantities.
  - Functions athat already return arrays where the leading axis could be
    variable in size.

- In the two cases (ckgp and ckgpav) where a function can be both vectorized
  and either raise an error or return a flag, the "_vector" suffix comes
  before "_error".

ARRAYS: An optional import allows the cspyce module to support multidimensional
arrays:

import cspyce
import cspyce.arrays

The latter import creates a new function in which the suffix "_array" replaces
"_vector" for every vectorized function. Whereas _vector function support only
a single extra dimension, _array functions follow all the standard rules of
shape broadcasting as defined in NumPy. For example, if one input has leading
dimension (10,4) and another has dimension (4,), then the two shapes will be
broadcasted together and returned quantities will be arrays with shape (10,4).

You can choose between the scalar, vector, and array versions of a function by
using their explicit names, or by using cspyce function attributes, as discussed
below.

================================================================================
ALIASES

Aliases allow the user to associate multiple names or codes with the same CSPICE
body or frame. Aliases can be used for a variety of purposes.

- You can use names and codes interchangeably as input arguments to any cspyce
  function.
- You can use a body name or code in place of a frame name or code, and the
  primary frame associated with that identified body will be used.
- Strings that represent integers are equivalent to the integers themselves.

Most importantly, you can allow multiple names or codes to refer to the same
CPSICE body or frame. For bodies and frames that have multiple names or codes,
calls to a cspyce function will try each option in sequence until it finds one
that works. Options are always tried in the order of they were defined, so
higher-priority names and codes are tried first.

Example 1: Jupiter's moon Dia uses code = 553, but it previously used code
55076. With 55076 defined as an alias for 553, a cspyce call will return
information about Dia under either of its codes.

Example 2: The Earth's rotation is, by default, modeled by frame "IAU_EARTH".
However, "ITRF93" is the name of a much more precise description of Earth's
rotation. If you define "IAU_EARTH" as an alias for "ITRF93", then the cspyce
toolkit will use ITRF93 if it is available, and otherwise IAU_EARTH.

Immediately after a cspyce call involving aliases, you can find out what value
or values were actually used by looking at attributes of the function. For
example, the first input to cspyce function spkez is called "targ" and it
identifies the code of a target being observed. After a call to
  cspyce.spkez(553, ...
the value of cspyce.spkez.targ will be the code actually used, in this case
either 553 or 55076.

To enable aliases, you must import an additional module

import cspyce
import cspyce.aliases

(Note that cspyce.aliases and cspyce.arrays can both be imported, and in either
order. Note also that these are unconventional modules, in that they introduce
new functionality into the "cspyce" namespace rather than creating new
namespaces called "cspyce.aliases" and "cspyce.arrays".)

With this import, a new function is defined for every cspyce function that takes
a frame or body as input. The new function has the same name as the pre-existing
cspyce function, but with "_alias" inserted immediately after the original
cspyce name (and before any other suffix such as "_vector" or "_error").

You can make alias support the default for individual cspyce functions or for
the entire cspyce module by calling:
  cspyce.use_aliases()
These versions can subsequently be disabled as the default by calling:
  cspyce.use_noaliases()

To define a body alias or frame alias, call
  cspyce.define_body_aliases(name_or_code, name_or_code, ...)
  cspyce.define_frame_aliases(name_or_code, name_or_code, ...)
where the arguments are an arbitrary list of codes and names.

To determine the aliases associated with a name or code, call
  cspyce.get_body_aliases(name_or_code)
  cspyce.get_frame_aliases(name_or_code)
where the argument is either a name or a code.

You can also select between the alias-supporting and alias-nonsupporting
versions of a function using function attributes.

================================================================================
FUNCTION NAMES, VERSIONS AND SELECTION METHODS

A cspyce function can accumulate several suffixes, based on the particular
behavior, as so:
    basename[_alias][_vector|_array][_error]
Only functions that are truly distinct are defined. For example, if a function
does not have a vector option, then no function will exist containing the
"_vector" suffix.

Note that you can use these functions to set defaults:
    cspyce.use_flags()
    cspyce.use_errors()
    cspyce.use_scalars()
    cspyce.use_vectors()
    cspyce.use_arrays()
    cspyce.use_aliases()
    cspyce.use_noaliases()

FUNCTION ATTRIBUTES: These provide a simpler mechanism for choosing the needed
version of a function, without remembering the suffix rules. Every cspyce
function has these attributes, each of which identifies another (or possibly the
same) cspyce function:

func.flag       the equivalent function without the _error suffix, if any.
func.error      the equivalent function with the _error suffix, if any.
func.scalar     the equivalent function without _array or _vector suffixes.
func.vector     the equivalent function with the _vector suffix, if any.
func.array      the equivalent function with the _array suffix, if any.
func.alias      the equivalent function with the _alias suffix, if any.
func.noalias    the equivalent function without the _alias suffix, if any.

These attributes are always defined, even if the particular option is not
supported by that function. This saves the programmer the effort of remembering,
for example, which functions support aliases or which functions support flags.

Thus, if the programmer wishes to be sure s/he is using the error version of
function bodn2c, and wants the vector version if it exists (but it doesn't!),
can call
    cspyce.bodn2c.error.vector(args...)

Thus, it is never strictly necessary to refer to any function with its suffixes.

================================================================================
