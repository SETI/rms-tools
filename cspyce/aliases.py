################################################################################
# cspyce/aliases.py
################################################################################
# Alias handler for the cspyce library
#
# Aliases allow the user to associate multiple names or codes with the same
# CSPICE body or frame. Aliases can be used for a variety of purposes.
#
# - You can use names and codes interchangeably as input arguments to any cspyce
#   function.
# - You can use a body name or code in place of a frame name or code, and the
#   primary frame associated with that identified body will be used.
# - Strings that represent integers are equivalent to the integers themselves.
#
# Most importantly, you can allow multiple names or codes to refer to the same
# CPSICE body or frame. For bodies and frames that have multiple names or codes,
# calls to a cspyce function will try each option in sequence until it finds one
# that works. Options are always tried in the order of they were defined, so
# higher-priority names and codes are tried first.
#
# Example 1: Jupiter's moon Dia uses code = 553, but it previously used code
# 55076. With 55076 defined as an alias for 553, a cspyce call will return
# information about Dia under either of its codes.
#
# Example 2: The Earth's rotation is, by default, modeled by frame "IAU_EARTH".
# However, "ITRF93" is the name of a much more precise description of Earth's
# rotation. If you define "IAU_EARTH" as an alias for "ITRF93", then the cspyce
# toolkit will use ITRF93 if it is available, and otherwise IAU_EARTH.
#
# Immediately after a cspyce call involving aliases, you can find out what value
# or values were actually used by looking at attributes of the function. For
# example, the first input to cspyce function spkez is called "targ" and it
# identifies the code of a target being observed. After a call to
#   cspyce.spkez(553, ...
# the value of cspyce.spkez.targ will be the code actually used, in this case
# either 553 or 55076.
#
# Upon importing this module, a new function is defined for every cspyce
# function that takes a frame or body as input. The new function has the same
# name as the pre-existing cspyce function, but with "_alias" inserted
# immediately after the original cspyce name (and before any other suffix such
# as "_vector" or "_error").
#
# You can make alias support the default for individual cspyce functions or for
# the entire cspyce module by calling:
#   cspyce.use_aliases()
# These versions can subsequently be disabled as the default by calling:
#   cspyce.use_noaliases()
#
# You can also select the specific version of the cspyce function via a function
# attribute. For example, after calling
#   cspyce.use_aliases('spkez')
# the function cspyce.spkez will support aliases. However, calling
#   cspyce.spkez.noalias(...)
# will use the un-aliased version. You can also use the aliased version
# explicitly by calling
#   cspyce.spkez.alias(...)
#
# To define a body alias or frame alias, call
#   cspyce.define_body_aliases(name_or_code, name_or_code, ...)
#   cspyce.define_frame_aliases(name_or_code, name_or_code, ...)
# where the arguments are an arbitrary list of codes and names.
#
# To determine the aliases associated with a name or code, call
#   cspyce.get_body_aliases(name_or_code)
#   cspyce.get_frame_aliases(name_or_code)
# where the argument is either a name or a code.
################################################################################

import cspyce
import cspyce.alias_support as support

if not hasattr(cspyce, 'ALIASES_IMPORTED'):

    # Upon import, define all missing alias versions
    support._define_all_alias_versions()

    # Also add new functions directly to the cspyce module
    cspyce.use_aliases = support.use_aliases
    cspyce.use_noaliases = support.use_noaliases
    cspyce.get_body_aliases = support.get_body_aliases
    cspyce.get_frame_aliases = support.get_frame_aliases
    cspyce.define_body_aliases = support.define_body_aliases
    cspyce.define_frame_aliases = support.define_frame_aliases

################################################################################
# Record the fact that this module was imported
################################################################################

cspyce.ALIASES_IMPORTED = True

cspyce.use_aliases()

################################################################################
