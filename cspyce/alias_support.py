################################################################################
# cspyce/alias_support.py
# Used internally by cspyce; not intended for direct import.
################################################################################

import re
import cspyce
import cspyce.cspyce1 as cspyce1

# Global dictionaries used to track aliases
BODY_CODE_ALIASES = {}
BODY_NAME_ALIASES = {}
FRAME_CODE_ALIASES = {}
FRAME_NAME_ALIASES = {}
FRAME_CODE_OVERRIDES = {}
FRAME_NAME_OVERRIDES = {}

def get_body_aliases(item):
    """Return a tuple containing the list of equivalent codes and the list of
    equivalent names for a given body name or code."""

    try:
        key = _as_key(item)
        return (BODY_CODE_ALIASES[key], BODY_NAME_ALIASES[key])
    except KeyError:
        pass

    try:
        if type(item) == str:
            item = cspyce1.bodn2c_error(item)

        return ([item], [cspyce1.bodc2n_error(item)]) # this corrects name case
    except KeyError:
        pass

    try:
        if type(item) == str:
            item = int(item)

        return ([item], [cspyce1.bodc2n_error(item)])
    except (KeyError, ValueError):
        pass

    return ([], [])

def get_frame_aliases(item):
    """Return a tuple containing the list of equivalent codes and the list of
    equivalent names for a given frame name or code. If the argument
    identifies a body instead of a frame, then return the aliases of the
    associated frame."""

    try:
        key = _as_key(item)
        return (FRAME_CODE_ALIASES[key], FRAME_NAME_ALIASES[key])
    except KeyError:
        pass

    try:
        if type(item) == str:
            item = cspyce1.namfrm_error(item)

        return ([item], [cspyce1.frmnam_error(item)]) # this corrects name case
    except KeyError:
        pass

    try:
        if type(item) == str:
            item = int(item)

        return ([item], [cspyce1.frmnam_error(item)])
    except (KeyError, ValueError):
        pass

    # If it's not a frame, see if it's a body with an associated frame
    body_codes = get_body_aliases(item)[0]
    for body_code in body_codes:
        frame_code = cspyce.cidfrm_error(body_code)[0]
        results = get_frame_aliases(frame_code)
        if results[0]:
            return results

    return ([], [])

########################################

def define_body_aliases(*items):
    """Define a list of items (integer codes or strings) as aliases of the same
    body or spacecraft.

    The item list will be expanded to include other the names and codes already
    associated with each listed item. Higher-priority codes and names should
    come first. Note that name strings can be defined in mixed case, so they
    should be given exactly as you wish them to appear.
    """

    queue = list(items) # Make a copy
    code_list = []
    name_list = []  # Stripped of surrounding whitespace; not otherwise modified
    aliases = set()

    # Expand lists to include everything
    while len(queue) > 0:
        item = queue[0]
        queue = queue[1:]

        if item in aliases: continue

        (codes, names) = get_body_aliases(item)
        queue += codes + names

        if type(item) == int:
            code_list.append(item)
            aliases.add(item)

        else:
            key = _as_key(item)
            aliases.add(key)

            item = _clean_name(item)
            name_list.append(item)
            aliases.add(item)

    # Expand name list and generate associated keys (capitalized)
    name_list = _expand_name_list(code_list, name_list)
    key_list = [_as_key(n) for n in name_list]

    # Save lists in the global dictionary, keyed by each code, name and key
    for item in code_list + name_list + key_list:
        BODY_CODE_ALIASES[item] = code_list
        BODY_NAME_ALIASES[item] = name_list

    # Expand the code list length to match that of the name list, if necessary
    needed = len(name_list) - len(code_list)
    if needed > 0:
        code_list = code_list + needed * [code_list[-1]]

    # Update the kernel pool
    for (name, code) in zip(name_list, code_list):
        cspyce1.boddef(name, code)

def define_frame_aliases(*items):
    """Define a list of items (integer codes or strings) as aliases of the same
    coordinate frame.

    The item list will be expanded to include other the names and codes already
    associated with each listed item. Higher-priority codes and names should
    come first. Note that name strings can be defined in mixed case, so they
    should be given exactly as you wish them to appear.
    """

    queue = list(items) # Make a copy
    code_list = []
    name_list = []  # Stripped of surrounding whitespace; not otherwise modified
    aliases = set()

    # Expand lists to include everything
    while len(queue) > 0:
        item = queue[0]
        queue = queue[1:]

        if item in aliases: continue

        (codes, names) = get_frame_aliases(item)
        queue += codes + names

        if type(item) == int:
            code_list.append(item)
            aliases.add(item)

        else:
            key = _as_key(item)
            aliases.add(key)

            item = _clean_name(item)
            name_list.append(item)
            aliases.add(item)

    # Expand name list and generate associated keys (capitalized)
    name_list = _expand_name_list(code_list, name_list)
    key_list = [_as_key(n) for n in name_list]

    # Save lists in the global dictionary, keyed by each code, name and key
    for item in code_list + name_list + key_list:
        FRAME_CODE_ALIASES[item] = code_list
        FRAME_NAME_ALIASES[item] = name_list

    # Expand the code list length to match that of the name list, if necessary
    needed = len(name_list) - len(code_list)
    if needed > 0:
        code_list = code_list + needed * [code_list[-1]]

    # Otherwise, add these pairs to the dictionary of frame overrides
    else:
        for (name, code) in zip(name_list, code_list):
            key = _as_key(name)
            spice1.FRAME_NAME_OVERRIDES[code] = name
            spice1.FRAME_NAME_OVERRIDES[name] = name
            spice1.FRAME_NAME_OVERRIDES[key ] = name
            spice1.FRAME_CODE_OVERRIDES[code] = code
            spice1.FRAME_CODE_OVERRIDES[name] = code
            spice1.FRAME_CODE_OVERRIDES[key ] = code

def _as_key(name):
    """Convert names to upper case and replace duplicated spaces with one;
    return ints unchanged.
    """

    if type(name) == int: return name

    name = name.upper().strip()
    while ('  ' in name):
        name = name.replace('  ', ' ')

    return name

def _clean_name(name):
    """Strip surrounding whitespace."""

    return name.strip()

_VERSION_REGEX = re.compile('(.*) +V[0-9]+$')

def _expand_name_list(code_list, name_list):
    """Make sure there is at least one name for each code."""

    lcodes = len(code_list)
    if lcodes <= len(name_list): return name_list

    # Remove versioned names (ending with " Vn" for integer n)
    unversioned_names = []
    for name in name_list:
        matchobj = _VERSION_REGEX.match(name)
        if matchobj is None:
            unversioned_names.append(name)
        else:
            unversioned_names.append(matchobj.group(1))

    # Create multiple versions of lowest-priority name
    name_list = unversioned_names
    needed = lcodes - len(name_list)
    last_name = name_list[-1]
    for v in range(needed,0,-1):
        name_list.append(last_name + ' V' + str(v))

    return name_list

################################################################################
# cspyce alias function wrapper
################################################################################

ALIAS_NOTE = """
This version supports aliases, meaning that any input identifying a
SPICE body or frame can be specified using any of its aliases (integer
or name). The cspyce function will try each of the aliases in their order
of priority, and the first valid results will be returned.

**These inputs can be given as either a name or an integer code.
"""

def _alias_signature(func):
    """Add "**" to the end of body and frame input definitions."""

    for (sig, name) in zip(func.SIGNATURE, func.ARGNAMES):
        if sig in ('body_name', 'body_code', 'frame_name', 'frame_code'):
            definition = func.DEFINITIONS[name]
            if not definition.endswith('**'):
                func.DEFINITIONS[name] = definition + '**'

def _alias_name(name):
    parts = name.split('_')
    if len(parts) > 1 and parts[1] == 'alias': return name

    parts = [parts[0], 'alias'] + parts[1:]
    return '_'.join(parts)

def alias_version(func):
    """Wrapper function to support aliasing of SPICE body names or codes.
    """

    if hasattr(func, 'alias'):
        return func.alias

    if not hasattr(func, 'ALIAS_ARGS'):
        alias_args = {}
        for k in range(len(func.ARGNAMES)):
            sig = func.SIGNATURE[k]
            if sig not in ('body_name', 'body_code',
                           'frame_name', 'frame_code'): continue

            alias_args[k] = sig
            alias_args[func.ARGNAMES[k]] = sig

        func.ALIAS_ARGS = alias_args

    if not func.ALIAS_ARGS:
        func.alias   = func
        func.noalias = func
        return func

    def wrapper(*args, **keywords):
        return _exec_with_aliases(wrapper, func, *args, **keywords)

    # Copy type info but not function version links
    for (key, value) in func.__dict__.iteritems():
        if type(value).__name__ != 'function':
            wrapper.__dict__[key] = value

    _alias_signature(wrapper)   # Add asterisks on aliased inputs

    # Save key attributes of the wrapper function before returning
    cspyce.assign_docstring(wrapper, ALIAS_NOTE)
    wrapper.__name__ = _alias_name(func.__name__)
    wrapper.func_defaults = func.func_defaults

    # Insert mutual links
    wrapper.alias   = wrapper
    wrapper.noalias = func

    func.alias   = wrapper
    func.noalias = func

    return wrapper

ALIAS_LOOKUP_DICT = {    # returns (function, index)
    'body_code'  : (get_body_aliases , 0),
    'body_name'  : (get_body_aliases , 1),
    'frame_code' : (get_frame_aliases, 0),
    'frame_name' : (get_frame_aliases, 1),
}

def _getarg(indx, args, keywords):
    if type(indx) == int:
        return args[indx]
    else:
        return keywords[indx]

def _setarg(indx, value, args, keywords):
    if type(indx) == int:
        args[indx] = value
    else:
        keywords[indx] = value

def _exec_with_aliases(wrapper, func, *args, **keywords):
    """Main function to handle a list of aliases in place of a single body name
    or code."""

    # Identify arguments that might have aliases
    alias_indices = []
    alias_args = list(args)     # Make copies
    alias_keywords = keywords.copy()
    for indx in range(len(args)) + keywords.keys():

        if indx not in func.ALIAS_ARGS: continue

        # Get argument type and translate
        arg = _getarg(indx, alias_args, alias_keywords)

        argtype = func.ALIAS_ARGS[indx]
        (lookup_func, code_or_name) = ALIAS_LOOKUP_DICT[argtype]
        options = lookup_func(arg)[code_or_name]

        # Interpret list of options
        if len(options) == 0:
            value = arg
        elif len(options) == 1:
            value = options[0]
        else:
            value = options     # using aliases here
            alias_indices.append(indx)

        _setarg(indx, value, alias_args, alias_keywords)

    # Call function now if iteration is not needed
    if not alias_indices:
        return func.__call__(*alias_args, **alias_keywords)

    # Iterate through the the last optional index; return if the call does not
    # fail.
    temp_args = list(alias_args)
    temp_keywords = alias_keywords.copy()
    wrapper.__name__ = _alias_name(func.__name__)

    indx = alias_indices[0]
    options = _getarg(indx, temp_args, temp_keywords)
    for option in options:
        _setarg(indx, option, temp_args, temp_keywords)

        try:
            results = _exec_with_one_alias(alias_indices[1:], wrapper, func,
                                           *temp_args, **temp_keywords)

            # On success, attach the value of the code or name that worked
            argname = func.ARGNAMES[indx]
            wrapper.__dict__[argname] = option
            return results

        except NotImplementedError: # an exception used for no other purpose
            continue

    # Nothing worked. Raise error from a call using original inputs, after
    # translation to the correct type

    args = list(args)   # make a mutable copy
    keywords = keywords.copy()

    # Use each original argument unless it is the wrong type
    for indx in alias_indices:
        argtype = func.ALIAS_ARGS[indx]
        value = _getarg(indx, args, keywords)
        if type(value) == int and argtype.endswith('_code'): continue
        if type(value) == str and argtype.endswith('_name'): continue

        options = _getarg(indx, alias_args, alias_keywords)
        _setarg(indx, options[0], args, keywords)

    # Call the function
    cspyce.chkin(wrapper.__name__)
    results = func.__call__(*args, **keywords)
    cspyce.chkout(wrapper.__name__)

    return results

def _exec_with_one_alias(alias_indices, wrapper, func, *args, **keywords):
    """Recursive function to evaluate the function using multiple aliases.

    At each call, the first alias index is used, and this function is called
    called recursively with each optional value of that input argument. It
    repeats until a NotImpementedError (a type of error not used elsewhere) is
    NOT raised. The absence of this error condition indicates success.

    On success, it saves the aliased value that worked as an attribute of the
    wrapper function, and then returns the successful value.

    If the list of alias indices is empty, then recursion stops and this
    evaluates the function with the given set of alias values. On success, it
    returns the result. On failure, it raises a NotImplementedError, which will
    cause the "parent" of this function to try again its next possible value
    of the alias.
    """

    # Handle multiple aliased indices by recursion
    if alias_indices:

      indx = alias_indices[0]
      options = _getarg(indx, args, keywords)
      for option in options:
        _setarg(indx, option, args, keywords)

        try:
            result = _exec_with_one_alias(alias_indices[1:], wrapper, func,
                                          *args, **keywords)

            # On success, attach the value of the code or name that worked
            argname = func.ARGNAMES[indx]
            wrapper.__dict__[argname] = option
            return result

        except NotImplementedError:
            continue

    # Recursion is done, so execute the function
    try:
        cspyce.chkin(wrapper.__name__)
        results = func.error.__call__(*args, **keywords)
        if cspyce.failed():
            cspyce.reset()
            cspyce.chkout(wrapper.__name__)
            raise NotImplementedError()

    except Exception:
        raise NotImplementedError()

    # Make sure the results correspond to the proper version of the function
    if func is func.error:
        return results

    return func.__call__(*args, **keywords)

################################################################################
# Define the alias function selector
################################################################################

SPYCE_DICT = cspyce.__dict__

def use_aliases(*funcs):
    """Switch the listed functions or names of functions to use the "alias"
    version by default. This affects all versions of any given cspyce function.
    If the list is empty, apply this operation to all cspyce functions.
    """

    if funcs:
        cspyce.GLOBAL_STATUS.add('ALIASES')
        cspyce.GLOBAL_STATUS.discard('NOALIASES')
    else:
        cspyce.GLOBAL_STATUS.discard('ALIASES')
        cspyce.GLOBAL_STATUS.discard('NOALIASES')

    for name in cspyce._get_func_names(funcs, source=SPYCE_DICT):
        if 'alias' not in name:
            SPYCE_DICT[name] = SPYCE_DICT[name].alias

def use_noaliases(*funcs):
    """Switch the listed functions or names of functions to use the "noalias"
    version by default. This affects all versions of any given cspyce function.
    If the list is empty, apply this operation to all cspyce functions.
    """

    if funcs:
        cspyce.GLOBAL_STATUS.discard('ALIASES')
        cspyce.GLOBAL_STATUS.add('NOALIASES')
    else:
        cspyce.GLOBAL_STATUS.discard('ALIASES')
        cspyce.GLOBAL_STATUS.discard('NOALIASES')

    for name in cspyce._get_func_names(funcs, source=SPYCE_DICT):
        if 'alias' not in name:
            SPYCE_DICT[name] = SPYCE_DICT[name].noalias

################################################################################
# Function to define alias versions and links for all cspyce functions
################################################################################

def _define_all_alias_versions():
    """Generate all missing alias functions and set the "alias" and "noalias"
    attribute for all cspyce functions.

    This routine can be run multiple times. At each run, it only creates
    whatever is missing.
    """

    # Create an alias version of each function that needs one
    alias_pairs = []
    funcs = cspyce.get_all_funcs(SPYCE_DICT).values()
    for func in funcs:
        if hasattr(func, 'alias'): continue

        alias_func = alias_version(func)
        if alias_func is func: continue     # function could not use aliases

        alias_name = alias_func.__name__
        SPYCE_DICT[alias_name] = alias_func

        alias_pairs.append((alias_func, func))

    # At this point, every alias function exists and every cspyce function has
    # "alias" and "noalias" attributes. However, links to other associated
    # cspyce functions still need to be filled in.

    for (afunc, func) in alias_pairs:
        _define_missing_versions_for_alias(afunc, func)

def _define_missing_versions_for_alias(afunc, func):
    """Complete the missing version attributes for a given alias function."""

    for (key, version) in func.__dict__.iteritems():
        if type(version).__name__ != 'function': continue

        if 'noalias' in key:
            afunc.__dict__[key] = version
        else:
            version_name = _alias_name(version.__name__)
            afunc.__dict__[key] = SPYCE_DICT[version_name]

################################################################################
