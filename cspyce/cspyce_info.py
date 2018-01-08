################################################################################
# A dictionary of docstrings and call signatures, keyed by the name of the
# CSPICE function name
################################################################################

CSPYCE_SIGNATURES  = {}
CSPYCE_ARGNAMES    = {}
CSPYCE_DEFAULTS    = {}
CSPYCE_RETURNS     = {}
CSPYCE_RETNAMES    = {}
CSPYCE_ABSTRACT    = {}
CSPYCE_DEFINITIONS = {}
CSPYCE_PS          = {}
CSPYCE_URL         = {}

CSPYCE_SIGNATURES ["axisar"] = ["int", "float"]
CSPYCE_ARGNAMES   ["axisar"] = ["axis", "angle"]
CSPYCE_RETURNS    ["axisar"] = ["rotmat[3,3]"]
CSPYCE_RETNAMES   ["axisar"] = ["rotmat"]
CSPYCE_ABSTRACT   ["axisar"] = """
Construct a rotation matrix that rotates vectors by a specified angle
about a specified axis.
"""
CSPYCE_DEFINITIONS["axisar"] = {
"axis": "Rotation axis.",
"angle": "Rotation angle, in radians.",
"rotmat": "Rotation matrix corresponding to axis and angle.",
}
CSPYCE_URL["axisar"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/axisar_c.html"

#########################################
CSPYCE_SIGNATURES ["b1900"] = []
CSPYCE_ARGNAMES   ["b1900"] = []
CSPYCE_RETURNS    ["b1900"] = ["float"]
CSPYCE_RETNAMES   ["b1900"] = ["jd"]
CSPYCE_ABSTRACT   ["b1900"] = """
Return the Julian Date corresponding to Besselian Date 1900.0.
"""
CSPYCE_DEFINITIONS["b1900"] = {
"jd": "JD of Besselian Date 1900.0",
}
CSPYCE_URL["b1900"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/b1900_c.html"

#########################################
CSPYCE_SIGNATURES ["b1950"] = []
CSPYCE_ARGNAMES   ["b1950"] = []
CSPYCE_RETURNS    ["b1950"] = ["float"]
CSPYCE_RETNAMES   ["b1950"] = ["jd"]
CSPYCE_ABSTRACT   ["b1950"] = """
Return the Julian Date corresponding to Besselian Date 1950.0.
"""
CSPYCE_DEFINITIONS["b1950"] = {
"jd": "JD of Besselian Date 1950.0",
}
CSPYCE_URL["b1950"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/b1950_c.html"

#########################################
CSPYCE_SIGNATURES ["bltfrm"] = ["int"]
CSPYCE_ARGNAMES   ["bltfrm"] = ["frmcls"]
CSPYCE_RETURNS    ["bltfrm"] = ["int[*]"]
CSPYCE_RETNAMES   ["bltfrm"] = ["idset"]
CSPYCE_ABSTRACT   ["bltfrm"] = """
Return a list containing all the frame IDs of all built-in frames of a
specified class.
"""
CSPYCE_DEFINITIONS["bltfrm"] = {
"frmcls": "Frame class (-1 = all; 1 = built-in inertial; 2 = PCK-based; 3 = CK-based; 4 = fixed rotational; 5 = dynamic).",
"idset": "List of ID codes of frames of the specified class.",
}
CSPYCE_URL["bltfrm"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bltfrm_c.html"

#########################################
CSPYCE_SIGNATURES ["bodc2n"] = ["body_code"]
CSPYCE_ARGNAMES   ["bodc2n"] = ["code"]
CSPYCE_RETURNS    ["bodc2n"] = ["body_name", "bool"]
CSPYCE_RETNAMES   ["bodc2n"] = ["name", "found"]
CSPYCE_ABSTRACT   ["bodc2n"] = """
Translate the SPICE integer code of a body into a common name for that
body.
"""
CSPYCE_DEFINITIONS["bodc2n"] = {
"code": "Integer ID code to be translated into a name.",
"name": "A common name for the body identified by code.",
"found": "True if translated, otherwise False.",
}
CSPYCE_URL["bodc2n"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bodc2n_c.html"

CSPYCE_SIGNATURES ["bodc2n_error"] = ["body_code"]
CSPYCE_ARGNAMES   ["bodc2n_error"] = ["code"]
CSPYCE_RETURNS    ["bodc2n_error"] = ["body_name"]
CSPYCE_RETNAMES   ["bodc2n_error"] = ["name"]
CSPYCE_ABSTRACT   ["bodc2n_error"] = """
Translate the SPICE integer code of a body into a common name for that
body.
"""
CSPYCE_DEFINITIONS["bodc2n_error"] = {
"code": "Integer ID code to be translated into a name.",
"name": "A common name for the body identified by code.",
}
CSPYCE_PS ["bodc2n_error"] = "Raise SPICE(BODYIDNOTFOUND) condition if code cound not be translated."
CSPYCE_URL["bodc2n_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bodc2n_c.html"

#########################################
CSPYCE_SIGNATURES ["bodc2s"] = ["body_code"]
CSPYCE_ARGNAMES   ["bodc2s"] = ["code"]
CSPYCE_RETURNS    ["bodc2s"] = ["body_name"]
CSPYCE_RETNAMES   ["bodc2s"] = ["name"]
CSPYCE_ABSTRACT   ["bodc2s"] = """
Translate a body ID code to either the corresponding name or if no name
to ID code mapping exists, the string representation of the body ID
value.
"""
CSPYCE_DEFINITIONS["bodc2s"] = {
"code": "Integer ID code to translate to a string.",
"name": "String corresponding to 'code'.",
}
CSPYCE_URL["bodc2s"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bodc2s_c.html"

#########################################
CSPYCE_SIGNATURES ["boddef"] = ["string", "int"]
CSPYCE_ARGNAMES   ["boddef"] = ["name", "code"]
CSPYCE_RETURNS    ["boddef"] = []
CSPYCE_RETNAMES   ["boddef"] = []
CSPYCE_ABSTRACT   ["boddef"] = """
Define a body name/ID code pair for later translation via bodn2c or
bodc2n.
"""
CSPYCE_DEFINITIONS["boddef"] = {
"name": "Common name of some body.",
"code": "Integer code for that body.",
}
CSPYCE_URL["boddef"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/boddef_c.html"

#########################################
CSPYCE_SIGNATURES ["bodfnd"] = ["body_code", "string"]
CSPYCE_ARGNAMES   ["bodfnd"] = ["body", "item"]
CSPYCE_RETURNS    ["bodfnd"] = ["bool"]
CSPYCE_RETNAMES   ["bodfnd"] = ["found"]
CSPYCE_ABSTRACT   ["bodfnd"] = """
Determine whether values exist for some item for any body in the kernel
pool.
"""
CSPYCE_DEFINITIONS["bodfnd"] = {
"body": "ID code of body.",
"item": "Item to find (\"RADII\", \"NUT_AMP_RA\", etc.).",
"found": "True if the item is in the kernel pool; False if it is not.",
}
CSPYCE_URL["bodfnd"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bodfnd_c.html"

#########################################
CSPYCE_SIGNATURES ["bodn2c"] = ["body_name"]
CSPYCE_ARGNAMES   ["bodn2c"] = ["name"]
CSPYCE_RETURNS    ["bodn2c"] = ["body_code", "bool"]
CSPYCE_RETNAMES   ["bodn2c"] = ["code", "found"]
CSPYCE_ABSTRACT   ["bodn2c"] = """
Translate the name of a body or object to the corresponding SPICE
integer ID code.
"""
CSPYCE_DEFINITIONS["bodn2c"] = {
"name": "Body name to be translated into a SPICE ID code.",
"code": "SPICE integer ID code for the named body.",
"found": "True if translated, otherwise False.",
}
CSPYCE_URL["bodn2c"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bodn2c_c.html"

CSPYCE_SIGNATURES ["bodn2c_error"] = ["body_name"]
CSPYCE_ARGNAMES   ["bodn2c_error"] = ["name"]
CSPYCE_RETURNS    ["bodn2c_error"] = ["body_code"]
CSPYCE_RETNAMES   ["bodn2c_error"] = ["code"]
CSPYCE_ABSTRACT   ["bodn2c_error"] = """
Translate the name of a body or object to the corresponding SPICE
integer ID code.
"""
CSPYCE_DEFINITIONS["bodn2c_error"] = {
"name": "Body name to be translated into a SPICE ID code.",
"code": "SPICE integer ID code for the named body.",
}
CSPYCE_PS ["bodn2c_error"] = "Raise SPICE(BODYNAMENOTFOUND) condition if name cound not be translated."
CSPYCE_URL["bodn2c_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bodn2c_c.html"

#########################################
CSPYCE_SIGNATURES ["bods2c"] = ["body_name"]
CSPYCE_ARGNAMES   ["bods2c"] = ["name"]
CSPYCE_RETURNS    ["bods2c"] = ["body_code", "bool"]
CSPYCE_RETNAMES   ["bods2c"] = ["code", "found"]
CSPYCE_ABSTRACT   ["bods2c"] = """
Translate a string containing a body name or ID code to an integer code.
"""
CSPYCE_DEFINITIONS["bods2c"] = {
"name": "String to be translated to an ID code.",
"code": "Integer ID code corresponding to `name'.",
"found": "True if translated, otherwise False.",
}
CSPYCE_URL["bods2c"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bods2c_c.html"

CSPYCE_SIGNATURES ["bods2c_error"] = ["body_name"]
CSPYCE_ARGNAMES   ["bods2c_error"] = ["name"]
CSPYCE_RETURNS    ["bods2c_error"] = ["body_code"]
CSPYCE_RETNAMES   ["bods2c_error"] = ["code"]
CSPYCE_ABSTRACT   ["bods2c_error"] = """
Translate a string containing a body name or ID code to an integer code.
"""
CSPYCE_DEFINITIONS["bods2c_error"] = {
"name": "String to be translated to an ID code.",
"code": "Integer ID code corresponding to `name'.",
}
CSPYCE_PS ["bods2c_error"] = "Raise SPICE(BODYNAMENOTFOUND) condition if name cound not be translated."
CSPYCE_URL["bods2c_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bods2c_c.html"

#########################################
CSPYCE_SIGNATURES ["bodvar"] = ["body_code", "string"]
CSPYCE_ARGNAMES   ["bodvar"] = ["bodyid", "item"]
CSPYCE_RETURNS    ["bodvar"] = ["float[*]"]
CSPYCE_RETNAMES   ["bodvar"] = ["values"]
CSPYCE_ABSTRACT   ["bodvar"] = """
Deprecated: This routine has been superseded by bodvcd and bodvrd. This
routine is supported for purposes of backward compatibility only.

Return the values of some item for any body in the kernel pool.
"""
CSPYCE_DEFINITIONS["bodvar"] = {
"bodyid": "ID code of body.",
"item"  : "Item for which values are desired. (\"RADII\", \"NUT_PREC_ANGLES\", etc.)",
"values": "Values.",
}
CSPYCE_URL["bodvar"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bodvar_c.html"

#########################################
CSPYCE_SIGNATURES ["bodvcd"] = ["body_code", "string"]
CSPYCE_ARGNAMES   ["bodvcd"] = ["bodyid", "item"]
CSPYCE_RETURNS    ["bodvcd"] = ["float[*]"]
CSPYCE_RETNAMES   ["bodvcd"] = ["values"]
CSPYCE_ABSTRACT   ["bodvcd"] = """
Fetch from the kernel pool the float values of an item associated with a
body, where the body is specified by an integer ID code.
"""
CSPYCE_DEFINITIONS["bodvcd"] = {
"bodyid": "Body ID code.",
"item"  : "Item for which values are desired. (\"RADII\", \"NUT_PREC_ANGLES\", etc.).",
"values": "Values as an array.",
}
CSPYCE_URL["bodvcd"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bodvcd_c.html"

#########################################
CSPYCE_SIGNATURES ["bodvrd"] = ["body_name", "string"]
CSPYCE_ARGNAMES   ["bodvrd"] = ["bodynm", "item"]
CSPYCE_RETURNS    ["bodvrd"] = ["float[*]"]
CSPYCE_RETNAMES   ["bodvrd"] = ["values"]
CSPYCE_ABSTRACT   ["bodvrd"] = """
Fetch from the kernel pool the double precision values of an item
associated with a body.
"""
CSPYCE_DEFINITIONS["bodvrd"] = {
"bodynm": "Body name.",
"item"  : "Item for which values are desired. (\"RADII\", \"NUT_PREC_ANGLES\", etc.).",
"values": "Values as an array.",
}
CSPYCE_URL["bodvrd"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bodvrd_c.html"

#########################################
CSPYCE_SIGNATURES ["ccifrm"] = ["int", "int"]
CSPYCE_ARGNAMES   ["ccifrm"] = ["frclss", "clssid"]
CSPYCE_RETURNS    ["ccifrm"] = ["int", "string", "int", "bool"]
CSPYCE_RETNAMES   ["ccifrm"] = ["frcode", "frname", "center", "found"]
CSPYCE_ABSTRACT   ["ccifrm"] = """
Return the frame name, frame ID, and center associated with a given
frame class and class ID.
"""
CSPYCE_DEFINITIONS["ccifrm"] = {
"frclss": "Class of frame.",
"clssid": "Class ID of frame.",
"frcode": "ID code of the frame.",
"frname": "Name of the frame.",
"center": "ID code of the center of the frame.",
"found": "True if the requested information is available.",
}
CSPYCE_URL["ccifrm"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ccifrm_c.html"

CSPYCE_SIGNATURES ["ccifrm_error"] = ["int", "int"]
CSPYCE_ARGNAMES   ["ccifrm_error"] = ["frclss", "clssid"]
CSPYCE_RETURNS    ["ccifrm_error"] = ["int", "string", "int"]
CSPYCE_RETNAMES   ["ccifrm_error"] = ["frcode", "frname", "center"]
CSPYCE_ABSTRACT   ["ccifrm_error"] = """
Return the frame name, frame ID, and center associated with a given
frame class and class ID.
"""
CSPYCE_DEFINITIONS["ccifrm_error"] = {
"frclss": "Class of frame.",
"clssid": "Class ID of frame.",
"frcode": "ID code of the frame.",
"frname": "Name of the frame.",
"center": "ID code of the center of the frame.",
}
CSPYCE_PS ["ccifrm_error"] = "Raise SPICE(INVALIDFRAMEDEF) condition if frame is not found."
CSPYCE_URL["ccifrm_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ccifrm_c.html"

#########################################
CSPYCE_SIGNATURES ["cgv2el"] = 3*["float[3]"]
CSPYCE_ARGNAMES   ["cgv2el"] = ["center", "vec1", "vec2"]
CSPYCE_RETURNS    ["cgv2el"] = ["float[9]"]
CSPYCE_RETNAMES   ["cgv2el"] = ["ellipse"]
CSPYCE_ABSTRACT   ["cgv2el"] = """
Form a CSPICE ellipse from a center vector and two generating vectors.
"""
CSPYCE_DEFINITIONS["cgv2el"] = {
"center" : "center vector",
"vec1"   : "two generating vectors for an ellipse.",
"vec2"   : "two generating vectors for an ellipse.",
"ellipse": "the CSPICE ellipse defined by the input vectors.",
}
CSPYCE_URL["cgv2el"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cgv2el_c.html"

#########################################
CSPYCE_SIGNATURES ["chkin"] = ["string"]
CSPYCE_ARGNAMES   ["chkin"] = ["module"]
CSPYCE_RETURNS    ["chkin"] = []
CSPYCE_RETNAMES   ["chkin"] = []
CSPYCE_ABSTRACT   ["chkin"] = """
Inform the CSPICE error handling mechanism of entry into a routine.
"""
CSPYCE_DEFINITIONS["chkin"] = {
"module": "The name of the calling routine.",
}
CSPYCE_URL["chkin"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/chkin_c.html"

#########################################
CSPYCE_SIGNATURES ["chkout"] = ["string"]
CSPYCE_ARGNAMES   ["chkout"] = ["module"]
CSPYCE_RETURNS    ["chkout"] = []
CSPYCE_RETNAMES   ["chkout"] = []
CSPYCE_ABSTRACT   ["chkout"] = """
Inform the CSPICE error handling mechanism of exit from a routine.
"""
CSPYCE_DEFINITIONS["chkout"] = {
"module": "The name of the calling routine.",
}
CSPYCE_URL["chkout"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/chkout_c.html"

#########################################
CSPYCE_SIGNATURES ["cidfrm"] = ["body_code"]
CSPYCE_ARGNAMES   ["cidfrm"] = ["cent"]
CSPYCE_RETURNS    ["cidfrm"] = ["frame_code", "frame_name", "bool"]
CSPYCE_RETNAMES   ["cidfrm"] = ["frcode", "frname", "found"]
CSPYCE_ABSTRACT   ["cidfrm"] = """
Retrieve frame ID code and name to associate with a frame center.
"""
CSPYCE_DEFINITIONS["cidfrm"] = {
"cent": "An object ID to associate a frame with.",
"frcode": "The ID code of the frame associated with cent.",
"frname": "The name of the frame with ID frcode.",
"found": "True if the requested information is available.",
}
CSPYCE_PS ["cidfrm"] = "Raise SPICE(CKINSUFFDATA) condition if the requested information is unavailable."
CSPYCE_URL["cidfrm"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cidfrm_c.html"

CSPYCE_SIGNATURES ["cidfrm_error"] = ["body_code"]
CSPYCE_ARGNAMES   ["cidfrm_error"] = ["cent"]
CSPYCE_RETURNS    ["cidfrm_error"] = ["frame_code", "frame_name"]
CSPYCE_RETNAMES   ["cidfrm_error"] = ["frcode", "frname"]
CSPYCE_ABSTRACT   ["cidfrm_error"] = """
Retrieve frame ID code and name to associate with a frame center.
"""
CSPYCE_DEFINITIONS["cidfrm_error"] = {
"cent": "An object ID to associate a frame with.",
"frcode": "The ID code of the frame associated with cent.",
"frname": "The name of the frame with ID frcode.",
}
CSPYCE_PS ["cidfrm_error"] = "Raise SPICE(BODYIDNOTFOUND) condition if the requested information is unavailable."
CSPYCE_URL["cidfrm_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cidfrm_c.html"

#########################################
CSPYCE_SIGNATURES ["ckcov"] = ["string", "body_code", "bool", "string", "float", "string"]
CSPYCE_ARGNAMES   ["ckcov"] = ["ck", "idcode", "needav", "level", "tol", "timsys"]
CSPYCE_RETURNS    ["ckcov"] = ["float[*,2]"]
CSPYCE_RETNAMES   ["ckcov"] = ["cover"]
CSPYCE_ABSTRACT   ["ckcov"] = """
Find the coverage window for a specified object in a specified CK file.
"""
CSPYCE_DEFINITIONS["ckcov"] = {
"ck": "Name of CK file.",
"idcode": "ID code of object.",
"needav": "Flag indicating whether angular velocity is needed.",
"level": "Coverage level: \"SEGMENT\" OR \"INTERVAL\".",
"tol": "Tolerance in ticks.",
"timsys": "Time system used to represent coverage.",
"cover":  "array of shape (intervals,2) where cover[:,0] are start times and cover[:,1] are stop times.",
}
CSPYCE_URL["ckcov"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckcov_c.html"

CSPYCE_SIGNATURES ["ckcov_error"] = ["string", "body_code", "bool", "string", "float", "string"]
CSPYCE_ARGNAMES   ["ckcov_error"] = ["ck", "idcode", "needav", "level", "tol", "timsys"]
CSPYCE_RETURNS    ["ckcov_error"] = ["float[*,2]"]
CSPYCE_RETNAMES   ["ckcov_error"] = ["cover"]
CSPYCE_ABSTRACT   ["ckcov_error"] = """
Find the coverage window for a specified object in a specified CK file.
"""
CSPYCE_DEFINITIONS["ckcov_error"] = {
"ck": "Name of CK file.",
"idcode": "ID code of object.",
"needav": "Flag indicating whether angular velocity is needed.",
"level": "Coverage level: \"SEGMENT\" or \"INTERVAL\".",
"tol": "Tolerance in ticks.",
"timsys": "Time system used to represent coverage.",
"cover": "array of shape (intervals,2) where cover[:,0] are start times and cover[:,1] are stop times.",
}
CSPYCE_PS ["ckcov_error"] = "Raise SPICE(BODYIDNOTFOUND) if the body code is not found in the C kernel."
CSPYCE_URL["ckcov_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckcov_c.html"

#########################################
CSPYCE_SIGNATURES ["ckgp"] = ["body_code", "float", "float", "frame_name"]
CSPYCE_ARGNAMES   ["ckgp"] = ["inst", "sclkdp", "tol", "ref"]
CSPYCE_RETURNS    ["ckgp"] = ["rotmat[3,3]", "float", "bool"]
CSPYCE_RETNAMES   ["ckgp"] = ["cmat", "clkout", "found"]
CSPYCE_ABSTRACT   ["ckgp"] = """
Get pointing(attitude) for a specified spacecraft clock time.
"""
CSPYCE_DEFINITIONS["ckgp"] = {
"inst": "NAIF ID of instrument, spacecraft, or structure.",
"sclkdp": "Encoded spacecraft clock time.",
"tol": "Time tolerance.",
"ref": "Reference frame.",
"cmat": "C-matrix pointing data.",
"clkout": "Output encoded spacecraft clock time.",
"found": "True when requested pointing is available.",
}
CSPYCE_URL["ckgp"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckgp_c.html"

CSPYCE_SIGNATURES ["ckgp_error"] = ["body_code", "float", "float", "frame_name"]
CSPYCE_ARGNAMES   ["ckgp_error"] = ["inst", "sclkdp", "tol", "ref"]
CSPYCE_RETURNS    ["ckgp_error"] = ["rotmat[3,3]", "float"]
CSPYCE_RETNAMES   ["ckgp_error"] = ["cmat", "clkout"]
CSPYCE_ABSTRACT   ["ckgp_error"] = """
Get pointing (attitude) for a specified spacecraft clock time.
"""
CSPYCE_DEFINITIONS["ckgp_error"] = {
"inst": "NAIF ID of instrument, spacecraft, or structure.",
"sclkdp": "Encoded spacecraft clock time.",
"tol": "Time tolerance.",
"ref": "Reference frame.",
"cmat": "C-matrix pointing data.",
"clkout": "Output encoded spacecraft clock time.",
}
CSPYCE_PS ["ckgp_error"] = "Raise SPICE(CKINSUFFDATA) condition if the requested information is unavailable."
CSPYCE_URL["ckgp_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckgp_c.html"

#########################################
CSPYCE_SIGNATURES ["ckgpav"] = ["body_code", "float", "float", "frame_name"]
CSPYCE_ARGNAMES   ["ckgpav"] = ["inst", "sclkdp", "tol", "ref"]
CSPYCE_RETURNS    ["ckgpav"] = ["rotmat[3,3]", "float[3]", "float", "bool"]
CSPYCE_RETNAMES   ["ckgpav"] = ["cmat", "av", "clkout", "found"]
CSPYCE_ABSTRACT   ["ckgpav"] = """
Get pointing(attitude) and angular velocity for a spacecraft clock time.
"""
CSPYCE_DEFINITIONS["ckgpav"] = {
"inst": "NAIF ID of instrument, spacecraft, or structure.",
"sclkdp": "Encoded spacecraft clock time.",
"tol": "Time tolerance.",
"ref": "Reference frame.",
"cmat": "C-matrix pointing data.",
"av": "Angular velocity vector.",
"clkout": "Output encoded spacecraft clock time.",
"found": "True when requested pointing is available.",
}
CSPYCE_URL["ckgpav"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckgpav_c.html"

CSPYCE_SIGNATURES ["ckgpav_error"] = ["body_code", "float", "float", "frame_name"]
CSPYCE_ARGNAMES   ["ckgpav_error"] = ["inst", "sclkdp", "tol", "ref"]
CSPYCE_RETURNS    ["ckgpav_error"] = ["rotmat[3,3]", "float[3]", "float"]
CSPYCE_RETNAMES   ["ckgpav_error"] = ["cmat", "av", "clkout"]
CSPYCE_ABSTRACT   ["ckgpav_error"] = """
Get pointing (attitude) and angular velocity for a spacecraft clock
time.
"""
CSPYCE_DEFINITIONS["ckgpav_error"] = {
"inst": "NAIF ID of instrument, spacecraft, or structure.",
"sclkdp": "Encoded spacecraft clock time.",
"tol": "Time tolerance.",
"ref": "Reference frame.",
"cmat": "C-matrix pointing data.",
"av": "Angular velocity vector.",
"clkout": "Output encoded spacecraft clock time.",
}
CSPYCE_PS ["ckgpav_error"] = "Raise SPICE(CKINSUFFDATA) condition if the requested information is unavailable."
CSPYCE_URL["ckgpav_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckgpav_c.html"

#########################################
CSPYCE_SIGNATURES ["ckobj"] = ["string"]
CSPYCE_ARGNAMES   ["ckobj"] = ["ck"]
CSPYCE_RETURNS    ["ckobj"] = ["int[*]"]
CSPYCE_RETNAMES   ["ckobj"] = ["ids"]
CSPYCE_ABSTRACT   ["ckobj"] = """
Find the set of ID codes of all objects in a specified CK file.
"""
CSPYCE_DEFINITIONS["ckobj"] = {
"ck": "Name of CK file.",
"ids": "Array of ID codes of objects in CK file.",
}
CSPYCE_URL["ckobj"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckobj_c.html"

#########################################
CSPYCE_SIGNATURES ["clight"] = []
CSPYCE_ARGNAMES   ["clight"] = []
CSPYCE_RETURNS    ["clight"] = ["float"]
CSPYCE_RETNAMES   ["clight"] = ["c"]
CSPYCE_ABSTRACT   ["clight"] = """
Return the speed of light in a vacuum (IAU official value, in km/sec).
"""
CSPYCE_DEFINITIONS["clight"] = {
"c": "speed of light",
}
CSPYCE_URL["clight"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/clight_c.html"

#########################################
CSPYCE_SIGNATURES ["clpool"] = []
CSPYCE_ARGNAMES   ["clpool"] = []
CSPYCE_RETURNS    ["clpool"] = []
CSPYCE_RETNAMES   ["clpool"] = []
CSPYCE_ABSTRACT   ["clpool"] = """
Remove all variables from the kernel pool.
"""
CSPYCE_DEFINITIONS["clpool"] = {}
CSPYCE_URL["clpool"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/clpool_c.html"

#########################################
CSPYCE_SIGNATURES ["cnmfrm"] = ["body_name"]
CSPYCE_ARGNAMES   ["cnmfrm"] = ["cname"]
CSPYCE_RETURNS    ["cnmfrm"] = ["frame_code", "frame_name", "bool"]
CSPYCE_RETNAMES   ["cnmfrm"] = ["frcode", "frname", "found"]
CSPYCE_ABSTRACT   ["cnmfrm"] = """
Retrieve frame ID code and name to associate with an object.
"""
CSPYCE_DEFINITIONS["cnmfrm"] = {
"cname": "Name of the object to find a frame for.",
"frcode": "The ID code of the frame associated with cname.",
"frname": "The name of the frame with ID frcode.",
"found": "True if the requested information is available.",
}
CSPYCE_URL["cnmfrm"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cnmfrm_c.html"

CSPYCE_SIGNATURES ["cnmfrm_error"] = ["body_name"]
CSPYCE_ARGNAMES   ["cnmfrm_error"] = ["cname"]
CSPYCE_RETURNS    ["cnmfrm_error"] = ["frame_code", "frame_name"]
CSPYCE_RETNAMES   ["cnmfrm_error"] = ["frcode", "frname"]
CSPYCE_ABSTRACT   ["cnmfrm_error"] = """
Retrieve frame ID code and name to associate with an object.
"""
CSPYCE_DEFINITIONS["cnmfrm_error"] = {
"cname": "Name of the object to find a frame for.",
"frcode": "The ID code of the frame associated with cname.",
"frname": "The name of the frame with ID frcode.",
}
CSPYCE_PS ["cnmfrm_error"] = "Raise SPICE(BODYNAMENOTFOUND) condition if the requested information is unavailable."
CSPYCE_URL["cnmfrm_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cnmfrm_c.html"

#########################################
CSPYCE_SIGNATURES ["conics"] = ["float[8]", "time"]
CSPYCE_ARGNAMES   ["conics"] = ["elts", "et"]
CSPYCE_RETURNS    ["conics"] = ["float[6]"]
CSPYCE_RETNAMES   ["conics"] = ["state"]
CSPYCE_ABSTRACT   ["conics"] = """
Determine the state (position, velocity) of an orbiting body from a set
of elliptic, hyperbolic, or parabolic orbital elements.
"""
CSPYCE_DEFINITIONS["conics"] = {
"elts": "Conic elements.",
"et": "Input time.",
"state": "State of orbiting body at et.",
}
CSPYCE_URL["conics"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/conics_c.html"

#########################################
CSPYCE_SIGNATURES ["convrt"] = ["float", "string", "string"]
CSPYCE_ARGNAMES   ["convrt"] = ["x", "in1", "out"]
CSPYCE_RETURNS    ["convrt"] = ["float"]
CSPYCE_RETNAMES   ["convrt"] = ["y"]
CSPYCE_ABSTRACT   ["convrt"] = """
Take a measurement X, the units associated with X, and units to which X
should be converted; return Y, the value of the measurement in the output
units.
"""
CSPYCE_DEFINITIONS["convrt"] = {
"x": "Number representing a measurement in some units.",
"in1": "The units in which x is measured.",
"out": "Desired units for the measurement.",
"y": "The measurment in the desired units.",
}
CSPYCE_URL["convrt"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/convrt_c.html"

#########################################
CSPYCE_SIGNATURES ["cyllat"] = 3*["float"]
CSPYCE_ARGNAMES   ["cyllat"] = ["r", "lonc", "z"]
CSPYCE_RETURNS    ["cyllat"] = 3*["float"]
CSPYCE_RETNAMES   ["cyllat"] = ["radius", "lon", "lat"]
CSPYCE_ABSTRACT   ["cyllat"] = """
Convert from cylindrical to latitudinal coordinates.
"""
CSPYCE_DEFINITIONS["cyllat"] = {
"r": "Distance of point from z axis.",
"lonc": "Cylindrical angle of point from XZ plane (radians).",
"z": "Height of point above XY plane.",
"radius": "Distance of point from origin.",
"lon": "Longitude of point (radians).",
"lat": "Latitude of point  (radians).",
}
CSPYCE_URL["cyllat"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cyllat_c.html"

#########################################
CSPYCE_SIGNATURES ["cylrec"] = 3*["float"]
CSPYCE_ARGNAMES   ["cylrec"] = ["r", "lon", "z"]
CSPYCE_RETURNS    ["cylrec"] = ["float[3]"]
CSPYCE_RETNAMES   ["cylrec"] = ["rectan"]
CSPYCE_ABSTRACT   ["cylrec"] = """
Convert from cylindrical to rectangular coordinates.
"""
CSPYCE_DEFINITIONS["cylrec"] = {
"r": "Distance of a point from z axis.",
"lon": "Angle (radians) of a point from xZ plane",
"z": "Height of a point above xY plane.",
"rectan": "Rectangular coordinates of the point.",
}
CSPYCE_URL["cylrec"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cylrec_c.html"

#########################################
CSPYCE_SIGNATURES ["cylsph"] = 3*["float"]
CSPYCE_ARGNAMES   ["cylsph"] = ["r", "lonc", "z"]
CSPYCE_RETURNS    ["cylsph"] = 3*["float"]
CSPYCE_RETNAMES   ["cylsph"] = ["radius", "colat", "lon"]
CSPYCE_ABSTRACT   ["cylsph"] = """
Convert from cylindrical to spherical coordinates.
"""
CSPYCE_DEFINITIONS["cylsph"] = {
"r": "Distance of point from z axis.",
"lonc": "Angle (radians) of point from XZ plane.",
"z": "Height of point above XY plane.",
"radius": "Distance of point from origin.",
"colat": "Polar angle (co-latitude in radians) of point.",
"lon": "Azimuthal angle (longitude) of point (radians).",
}
CSPYCE_URL["cylsph"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cylsph_c.html"

#########################################
CSPYCE_SIGNATURES ["dafbfs"] = ["int"]
CSPYCE_ARGNAMES   ["dafbfs"] = ["handle"]
CSPYCE_RETURNS    ["dafbfs"] = []
CSPYCE_RETNAMES   ["dafbfs"] = []
CSPYCE_ABSTRACT   ["dafbfs"] = """
Begin a forward search for arrays in a DAF.
"""
CSPYCE_DEFINITIONS["dafbfs"] = {
"handle": "Handle of file to be searched.",
}
CSPYCE_URL["dafbfs"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafbfs_c.html"

#########################################
CSPYCE_SIGNATURES ["dafcls"] = ["int"]
CSPYCE_ARGNAMES   ["dafcls"] = ["handle"]
CSPYCE_RETURNS    ["dafcls"] = []
CSPYCE_RETNAMES   ["dafcls"] = []
CSPYCE_ABSTRACT   ["dafcls"] = """
Close the DAF associated with a given handle.
"""
CSPYCE_DEFINITIONS["dafcls"] = {
"handle": "Handle of DAF to be closed.",
}
CSPYCE_URL["dafcls"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafcls_c.html"

#########################################
CSPYCE_SIGNATURES ["dafgda"] = 3*["int"]
CSPYCE_ARGNAMES   ["dafgda"] = ["handle", "begin", "end"]
CSPYCE_RETURNS    ["dafgda"] = ["float[*]"]
CSPYCE_RETNAMES   ["dafgda"] = ["data"]
CSPYCE_ABSTRACT   ["dafgda"] = """
Read the double precision data bounded by two addresses within a DAF.
"""
CSPYCE_DEFINITIONS["dafgda"] = {
"handle": "Handle of a DAF.",
"begin": "Initial address within file.",
"end": "Final address within file.",
"data": "Data contained between `begin' and `end'.",
}
CSPYCE_URL["dafgda"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafgda_c.html"

#########################################
CSPYCE_SIGNATURES ["dafgn"] = ["int"]
CSPYCE_ARGNAMES   ["dafgn"] = ["lenout"]
CSPYCE_RETURNS    ["dafgn"] = ["string"]
CSPYCE_RETNAMES   ["dafgn"] = ["name"]
CSPYCE_ABSTRACT   ["dafgn"] = """
Return (get) the name for the current array in the current DAF.
"""
CSPYCE_DEFINITIONS["dafgn"] = {
"lenout": "Length of array name string.",
"name": "Name of current array.",
}
CSPYCE_URL["dafgn"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafgn_c.html"

#########################################
CSPYCE_SIGNATURES ["dafgs"] = []
CSPYCE_ARGNAMES   ["dafgs"] = []
CSPYCE_RETURNS    ["dafgs"] = ["float[128]"]
CSPYCE_RETNAMES   ["dafgs"] = ["sum"]
CSPYCE_ABSTRACT   ["dafgs"] = """
Return (get) the summary for the current array in the current DAF.
"""
CSPYCE_DEFINITIONS["dafgs"] = {
"sum": "Summary for current array.",
}
CSPYCE_URL["dafgs"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafgs_c.html"

#########################################
CSPYCE_SIGNATURES ["daffna"] = []
CSPYCE_ARGNAMES   ["daffna"] = []
CSPYCE_RETURNS    ["daffna"] = ["bool"]
CSPYCE_RETNAMES   ["daffna"] = ["found"]
CSPYCE_ABSTRACT   ["daffna"] = """
Find the next (forward) array in the current DAF.
"""
CSPYCE_DEFINITIONS["daffna"] = {
"found": "True if an array was found.",
}
CSPYCE_URL["daffna"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/daffna_c.html"

#########################################
CSPYCE_SIGNATURES ["dafopr"] = ["string"]
CSPYCE_ARGNAMES   ["dafopr"] = ["fname"]
CSPYCE_RETURNS    ["dafopr"] = ["int"]
CSPYCE_RETNAMES   ["dafopr"] = ["handle"]
CSPYCE_ABSTRACT   ["dafopr"] = """
Open a DAF for subsequent read requests.
"""
CSPYCE_DEFINITIONS["dafopr"] = {
"fname": "Name of DAF to be opened.",
"handle": "Handle assigned to DAF.",
}
CSPYCE_URL["dafopr"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafopr_c.html"

#########################################
CSPYCE_SIGNATURES ["dafus"] = ["float[*]", "int", "int"]
CSPYCE_ARGNAMES   ["dafus"] = ["sum", "nd", "ni"]
CSPYCE_RETURNS    ["dafus"] = ["float[*]", "int[*]"]
CSPYCE_RETNAMES   ["dafus"] = ["dc", "ic"]
CSPYCE_ABSTRACT   ["dafus"] = """
Unpack an array summary into its double precision and integer
components.
"""
CSPYCE_DEFINITIONS["dafus"] = {
"sum": "Array summary.",
"nd": "Number of double precision components.",
"ni": "Number of integer components.",
"dc": "Double precision components.",
"ic": "Integer components.",
}
CSPYCE_URL["dafus"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafus_c.html"

#########################################
CSPYCE_SIGNATURES ["dcyldr"] = 3*["float"]
CSPYCE_ARGNAMES   ["dcyldr"] = ["x", "y", "z"]
CSPYCE_RETURNS    ["dcyldr"] = ["float[3,3]"]
CSPYCE_RETNAMES   ["dcyldr"] = ["jacobi"]
CSPYCE_ABSTRACT   ["dcyldr"] = """
This routine computes the Jacobian of the transformation from
rectangular to cylindrical coordinates.
"""
CSPYCE_DEFINITIONS["dcyldr"] = {
"x": "X-coordinate of point.",
"y": "Y-coordinate of point.",
"z": "Z-coordinate of point.",
"jacobi": "Matrix of partial derivatives.",
}
CSPYCE_URL["dcyldr"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dcyldr_c.html"

#########################################
CSPYCE_SIGNATURES ["deltet"] = ["time", "string"]
CSPYCE_ARGNAMES   ["deltet"] = ["epoch", "eptype"]
CSPYCE_RETURNS    ["deltet"] = ["float"]
CSPYCE_RETNAMES   ["deltet"] = ["delta"]
CSPYCE_ABSTRACT   ["deltet"] = """
Return the value of Delta ET (ET-UTC) for an input epoch.
"""
CSPYCE_DEFINITIONS["deltet"] = {
"epoch": "Input epoch (seconds past J2000).",
"eptype": "Type of input epoch (\"UTC\" or \"ET\").",
"delta": "Delta ET (ET-UTC) at input epoch.",
}
CSPYCE_URL["deltet"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/deltet_c.html"

#########################################
CSPYCE_SIGNATURES ["det"] = ["float[3,3]"]
CSPYCE_ARGNAMES   ["det"] = ["m1"]
CSPYCE_RETURNS    ["det"] = ["float"]
CSPYCE_RETNAMES   ["det"] = ["value"]
CSPYCE_ABSTRACT   ["det"] = """
Compute the determinant of a double precision 3x3 matrix.
"""
CSPYCE_DEFINITIONS["det"] = {
"m1": "Matrix whose determinant is to be found.",
"value": "value of determinant.",
}
CSPYCE_URL["det"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/det_c.html"

#########################################
CSPYCE_SIGNATURES ["dgeodr"] = 5*["float"]
CSPYCE_ARGNAMES   ["dgeodr"] = ["x", "y", "z", "re", "f"]
CSPYCE_RETURNS    ["dgeodr"] = ["float[3,3]"]
CSPYCE_RETNAMES   ["dgeodr"] = ["jacobi"]
CSPYCE_ABSTRACT   ["dgeodr"] = """
This routine computes the Jacobian of the transformation from
rectangular to geodetic coordinates.
"""
CSPYCE_DEFINITIONS["dgeodr"] = {
"x": "X-coordinate of point.",
"y": "Y-coordinate of point.",
"z": "Z-coordinate of point.",
"re": "Equatorial radius of the reference spheroid.",
"f": "Flattening coefficient.",
"jacobi": "Matrix of partial derivatives.",
}
CSPYCE_URL["dgeodr"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dgeodr_c.html"

#########################################
CSPYCE_SIGNATURES ["diags2"] = ["float[2,2]"]
CSPYCE_ARGNAMES   ["diags2"] = ["symmat"]
CSPYCE_RETURNS    ["diags2"] = 2*["float[2,2]"]
CSPYCE_RETNAMES   ["diags2"] = ["diag", "rotate"]
CSPYCE_ABSTRACT   ["diags2"] = """
Diagonalize a symmetric 2x2 matrix.
"""
CSPYCE_DEFINITIONS["diags2"] = {
"symmat": "A symmetric 2x2 matrix.",
"diag": "A diagonal matrix similar to symmat.",
"rotate": "A rotation used as the similarity transformation.",
}
CSPYCE_URL["diags2"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/diags2_c.html"

#########################################
CSPYCE_SIGNATURES ["dlatdr"] = 3*["float"]
CSPYCE_ARGNAMES   ["dlatdr"] = ["x", "y", "z"]
CSPYCE_RETURNS    ["dlatdr"] = ["float[3,3]"]
CSPYCE_RETNAMES   ["dlatdr"] = ["jacobi"]
CSPYCE_ABSTRACT   ["dlatdr"] = """
This routine computes the Jacobian of the transformation from
rectangular to latitudinal coordinates.
"""
CSPYCE_DEFINITIONS["dlatdr"] = {
"x": "X-coordinate of point.",
"y": "Y-coordinate of point.",
"z": "Z-coordinate of point.",
"jacobi": "Matrix of partial derivatives.",
}
CSPYCE_URL["dlatdr"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dlatdr_c.html"

#########################################
CSPYCE_SIGNATURES ["dpgrdr"] = ["body_name"] + 5*["float"]
CSPYCE_ARGNAMES   ["dpgrdr"] = ["body", "x", "y", "z", "re", "f"]
CSPYCE_RETURNS    ["dpgrdr"] = ["float[3,3]"]
CSPYCE_RETNAMES   ["dpgrdr"] = ["jacobi"]
CSPYCE_ABSTRACT   ["dpgrdr"] = """
This routine computes the Jacobian matrix of the transformation from
rectangular to planetographic coordinates.
"""
CSPYCE_DEFINITIONS["dpgrdr"] = {
"body": "Body with which coordinate system is associated.",
"x": "X-coordinate of point.",
"y": "Y-coordinate of point.",
"z": "Z-coordinate of point.",
"re": "Equatorial radius of the reference spheroid.",
"f": "Flattening coefficient.",
"jacobi": "Matrix of partial derivatives.",
}
CSPYCE_URL["dpgrdr"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dpgrdr_c.html"

#########################################
CSPYCE_SIGNATURES ["dpmax"] = []
CSPYCE_ARGNAMES   ["dpmax"] = []
CSPYCE_RETURNS    ["dpmax"] = ["float"]
CSPYCE_RETNAMES   ["dpmax"] = ["value"]
CSPYCE_ABSTRACT   ["dpmax"] = """
Return the value of the largest (positive) number representable in a
double precision variable.
"""
CSPYCE_DEFINITIONS["dpmax"] = {
"value": "maximum respresentable double-precision number",
}
CSPYCE_URL["dpmax"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dpmax_c.html"

#########################################
CSPYCE_SIGNATURES ["dpmin"] = []
CSPYCE_ARGNAMES   ["dpmin"] = []
CSPYCE_RETURNS    ["dpmin"] = ["float"]
CSPYCE_RETNAMES   ["dpmin"] = ["value"]
CSPYCE_ABSTRACT   ["dpmin"] = """
Return the value of the smallest (negative) number representable in a
double precision variable.
"""
CSPYCE_DEFINITIONS["dpmin"] = {
"value": "minimum respresentable double-precision number (negative)",
}
CSPYCE_URL["dpmin"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dpmin_c.html"

#########################################
CSPYCE_SIGNATURES ["dpr"] = []
CSPYCE_ARGNAMES   ["dpr"] = []
CSPYCE_RETURNS    ["dpr"] = ["float"]
CSPYCE_RETNAMES   ["dpr"] = ["value"]
CSPYCE_ABSTRACT   ["dpr"] = """
Return the number of degrees per radian.
"""
CSPYCE_DEFINITIONS["dpr"] = {
"value": "degrees per radian"
}
CSPYCE_URL["dpr"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dpr_c.html"

#########################################
CSPYCE_SIGNATURES ["drdcyl"] = 3*["float"]
CSPYCE_ARGNAMES   ["drdcyl"] = ["r", "lon", "z"]
CSPYCE_RETURNS    ["drdcyl"] = ["float[3,3]"]
CSPYCE_RETNAMES   ["drdcyl"] = ["jacobi"]
CSPYCE_ABSTRACT   ["drdcyl"] = """
This routine computes the Jacobian of the transformation from
cylindrical to rectangular coordinates.
"""
CSPYCE_DEFINITIONS["drdcyl"] = {
"r": "Distance of a point from the origin.",
"lon": "Angle of the point from the xz plane in radians.",
"z": "Height of the point above the xy plane.",
"jacobi": "Matrix of partial derivatives.",
}
CSPYCE_URL["drdcyl"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/drdcyl_c.html"

#########################################
CSPYCE_SIGNATURES ["drdgeo"] = 5*["float"]
CSPYCE_ARGNAMES   ["drdgeo"] = ["lon", "lat", "alt", "re", "f"]
CSPYCE_RETURNS    ["drdgeo"] = ["float[3,3]"]
CSPYCE_RETNAMES   ["drdgeo"] = ["jacobi"]
CSPYCE_ABSTRACT   ["drdgeo"] = """
This routine computes the Jacobian of the transformation from geodetic
to rectangular coordinates.
"""
CSPYCE_DEFINITIONS["drdgeo"] = {
"lon": "Geodetic longitude of point (radians).",
"lat": "Geodetic latitude of point (radians).",
"alt": "Altitude of point above the reference spheroid.",
"re": "Equatorial radius of the reference spheroid.",
"f": "Flattening coefficient.",
"jacobi": "Matrix of partial derivatives.",
}
CSPYCE_URL["drdgeo"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/drdgeo_c.html"

#########################################
CSPYCE_SIGNATURES ["drdlat"] = 3*["float"]
CSPYCE_ARGNAMES   ["drdlat"] = ["radius", "lon", "lat"]
CSPYCE_RETURNS    ["drdlat"] = ["float[3,3]"]
CSPYCE_RETNAMES   ["drdlat"] = ["jacobi"]
CSPYCE_ABSTRACT   ["drdlat"] = """
Compute the Jacobian of the transformation from latitudinal to
rectangular coordinates.
"""
CSPYCE_DEFINITIONS["drdlat"] = {
"radius": "Distance of a point from the origin.",
"lon": "Angle of the point from the XZ plane in radians.",
"lat": "Angle of the point from the XY plane in radians.",
"jacobi": "Matrix of partial derivatives.",
}
CSPYCE_URL["drdlat"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/drdlat_c.html"

#########################################
CSPYCE_SIGNATURES ["drdpgr"] = ["body_name"] + 5*["float"]
CSPYCE_ARGNAMES   ["drdpgr"] = ["body", "lon", "lat", "alt", "re", "f"]
CSPYCE_RETURNS    ["drdpgr"] = ["float[3,3]"]
CSPYCE_RETNAMES   ["drdpgr"] = ["jacobi"]
CSPYCE_ABSTRACT   ["drdpgr"] = """
This routine computes the Jacobian matrix of the transformation from
planetographic to rectangular coordinates.
"""
CSPYCE_DEFINITIONS["drdpgr"] = {
"body": "Name of body with which coordinates are associated.",
"lon": "Planetographic longitude of a point (radians).",
"lat": "Planetographic latitude of a point (radians).",
"alt": "Altitude of a point above reference spheroid.",
"re": "Equatorial radius of the reference spheroid.",
"f": "Flattening coefficient.",
"jacobi": "Matrix of partial derivatives.",
}
CSPYCE_URL["drdpgr"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/drdpgr_c.html"

#########################################
CSPYCE_SIGNATURES ["drdsph"] = 3*["float"]
CSPYCE_ARGNAMES   ["drdsph"] = ["r", "colat", "lon"]
CSPYCE_RETURNS    ["drdsph"] = ["float[3,3]"]
CSPYCE_RETNAMES   ["drdsph"] = ["jacobi"]
CSPYCE_ABSTRACT   ["drdsph"] = """
This routine computes the Jacobian of the transformation from spherical
to rectangular coordinates.
"""
CSPYCE_DEFINITIONS["drdsph"] = {
"r": "Distance of a point from the origin.",
"colat": "Angle of the point from the positive z-axis.",
"lon": "Angle of the point from the xy plane.",
"jacobi": "Matrix of partial derivatives.",
}
CSPYCE_URL["drdsph"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/drdsph_c.html"

#########################################
CSPYCE_SIGNATURES ["dsphdr"] = 3*["float"]
CSPYCE_ARGNAMES   ["dsphdr"] = ["x", "y", "z"]
CSPYCE_RETURNS    ["dsphdr"] = ["float[3,3]"]
CSPYCE_RETNAMES   ["dsphdr"] = ["jacobi"]
CSPYCE_ABSTRACT   ["dsphdr"] = """
This routine computes the Jacobian of the transformation from
rectangular to spherical coordinates.
"""
CSPYCE_DEFINITIONS["dsphdr"] = {
"x": "x-coordinate of point.",
"y": "y-coordinate of point.",
"z": "z-coordinate of point.",
"jacobi": "Matrix of partial derivatives.",
}
CSPYCE_URL["dsphdr"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dsphdr_c.html"

#########################################
CSPYCE_SIGNATURES ["dtpool"] = ["string"]
CSPYCE_ARGNAMES   ["dtpool"] = ["name"]
CSPYCE_RETURNS    ["dtpool"] = ["bool", "int", "string"]
CSPYCE_RETNAMES   ["dtpool"] = ["found", "n", "vtype"]
CSPYCE_ABSTRACT   ["dtpool"] = """
Return the data about a kernel pool variable.
"""
CSPYCE_DEFINITIONS["dtpool"] = {
"name": "Name of the variable whose value is to be returned.",
"found": "True if variable is in pool.",
"n": "Number of values returned for name.",
"vtype": "Type of the variable: \"C\", \"N\", or \"X\"",
}
CSPYCE_URL["dtpool"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dtpool_c.html"

CSPYCE_SIGNATURES ["dtpool_error"] = ["string"]
CSPYCE_ARGNAMES   ["dtpool_error"] = ["name"]
CSPYCE_RETURNS    ["dtpool_error"] = ["int", "string"]
CSPYCE_RETNAMES   ["dtpool_error"] = ["n", "vtype"]
CSPYCE_ABSTRACT   ["dtpool_error"] = """
Return the data about a kernel pool variable.
"""
CSPYCE_DEFINITIONS["dtpool_error"] = {
"name": "Name of the variable whose value is to be returned.",
"n": "Number of values returned for name.",
"vtype": "Type of the variable: \"C\", \"N\", or \"X\"",
}
CSPYCE_PS ["dtpool_error"] = "Raise SPICE(VARIABLENOTFOUND) if the requested variable is not in the kernel pool."
CSPYCE_URL["dtpool_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dtpool_c.html"

#########################################
CSPYCE_SIGNATURES ["ducrss"] = 2*["float[6]"]
CSPYCE_ARGNAMES   ["ducrss"] = ["s1", "s2"]
CSPYCE_RETURNS    ["ducrss"] = ["float[6]"]
CSPYCE_RETNAMES   ["ducrss"] = ["sout"]
CSPYCE_ABSTRACT   ["ducrss"] = """
Compute the unit vector parallel to the cross product of two
3-dimensional vectors and the derivative of this unit vector.
"""
CSPYCE_DEFINITIONS["ducrss"] = {
"s1": "Left hand state for cross product and derivative.",
"s2": "Right hand state for cross product and derivative.",
"sout": "Unit vector and derivative of the cross product.",
}
CSPYCE_URL["ducrss"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ducrss_c.html"

#########################################
CSPYCE_SIGNATURES ["dvcrss"] = 2*["float[6]"]
CSPYCE_ARGNAMES   ["dvcrss"] = ["s1", "s2"]
CSPYCE_RETURNS    ["dvcrss"] = ["float[6]"]
CSPYCE_RETNAMES   ["dvcrss"] = ["sout"]
CSPYCE_ABSTRACT   ["dvcrss"] = """
Compute the cross product of two 3-dimensional vectors and the
derivative of this cross product.
"""
CSPYCE_DEFINITIONS["dvcrss"] = {
"s1": "Left hand state for cross product and derivative.",
"s2": "Right hand state for cross product and derivative.",
"sout": "State associated with cross product of positions.",
}
CSPYCE_URL["dvcrss"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dvcrss_c.html"

#########################################
CSPYCE_SIGNATURES ["dvdot"] = 2*["float[6]"]
CSPYCE_ARGNAMES   ["dvdot"] = ["s1", "s2"]
CSPYCE_RETURNS    ["dvdot"] = ["float[6]"]
CSPYCE_RETNAMES   ["dvdot"] = ["value"]
CSPYCE_ABSTRACT   ["dvdot"] = """
Compute the derivative of the dot product of two double precision
position vectors.
"""
CSPYCE_DEFINITIONS["dvdot"] = {
"s1": "First state vector in the dot product.",
"s2": "Second state vector in the dot product.",
"value": "The derivative of the dot product <s1,s2>",
}
CSPYCE_URL["dvdot"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dvdot_c.html"

#########################################
CSPYCE_SIGNATURES ["dvhat"] = ["float[6]"]
CSPYCE_ARGNAMES   ["dvhat"] = ["s1"]
CSPYCE_RETURNS    ["dvhat"] = ["float"]
CSPYCE_RETNAMES   ["dvhat"] = ["sout"]
CSPYCE_ABSTRACT   ["dvhat"] = """
Find the unit vector corresponding to a state vector and the derivative
of the unit vector.
"""
CSPYCE_DEFINITIONS["dvhat"] = {
"s1": "State to be normalized.",
"sout": "Unit vector s1 / |s1|, and its time derivative.",
}
CSPYCE_URL["dvhat"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dvhat_c.html"

#########################################
CSPYCE_SIGNATURES ["dvnorm"] = ["float[6]"]
CSPYCE_ARGNAMES   ["dvnorm"] = ["state"]
CSPYCE_RETURNS    ["dvnorm"] = ["float[6]"]
CSPYCE_RETNAMES   ["dvnorm"] = ["value"]
CSPYCE_ABSTRACT   ["dvnorm"] = """
Function to calculate the derivative of the norm of a 3-vector.
"""
CSPYCE_DEFINITIONS["dvnorm"] = {
"state": "A 6-vector composed of three coordinates and their derivatives.",
"value": "derivative of the norm",
}
CSPYCE_URL["dvnorm"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dvnorm_c.html"

#########################################
CSPYCE_SIGNATURES ["dvpool"] = ["string"]
CSPYCE_ARGNAMES   ["dvpool"] = ["name"]
CSPYCE_RETURNS    ["dvpool"] = []
CSPYCE_RETNAMES   ["dvpool"] = []
CSPYCE_ABSTRACT   ["dvpool"] = """
Delete a variable from the kernel pool.
"""
CSPYCE_DEFINITIONS["dvpool"] = {
"name": "Name of the kernel variable to be deleted.",
}
CSPYCE_URL["dvpool"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dvpool_c.html"

#########################################
CSPYCE_SIGNATURES ["dvsep"] = 2*["float[6]"]
CSPYCE_ARGNAMES   ["dvsep"] = ["s1", "s2"]
CSPYCE_RETURNS    ["dvsep"] = ["float"]
CSPYCE_RETNAMES   ["dvsep"] = ["value"]
CSPYCE_ABSTRACT   ["dvsep"] = """
Calculate the time derivative of the separation angle between two input
states, S1 and S2.
"""
CSPYCE_DEFINITIONS["dvsep"] = {
"s1": "State vector of the first body",
"s2": "State vector of the second  body",
"value": "derivate of the separation angle between state vectors.",
}
CSPYCE_URL["dvsep"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dvsep_c.html"

#########################################
CSPYCE_SIGNATURES ["edlimb"] = 3*["float"] + ["float[3]"]
CSPYCE_ARGNAMES   ["edlimb"] = ["a", "b", "c", "viewpt"]
CSPYCE_RETURNS    ["edlimb"] = ["float[9]"]
CSPYCE_RETNAMES   ["edlimb"] = ["limb"]
CSPYCE_ABSTRACT   ["edlimb"] = """
Find the limb of a triaxial ellipsoid, viewed from a specified point.
"""
CSPYCE_DEFINITIONS["edlimb"] = {
"a": "Length of ellipsoid semi-axis lying on the x-axis.",
"b": "Length of ellipsoid semi-axis lying on the y-axis.",
"c": "Length of ellipsoid semi-axis lying on the z-axis.",
"viewpt": "Location of viewing point.",
"limb": "Limb of ellipsoid as seen from viewing point.",
}
CSPYCE_URL["edlimb"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/edlimb_c.html"

#########################################
CSPYCE_SIGNATURES ["edterm"] = ["string", "body_name", "body_name", "time", "frame_name", "string", "body_name", "int"]
CSPYCE_ARGNAMES   ["edterm"] = ["trmtyp", "source", "target", "et", "fixref", "abcorr", "obsrvr", "npts"]
CSPYCE_RETURNS    ["edterm"] = ["time", "float[3]", "float[*,3]"]
CSPYCE_RETNAMES   ["edterm"] = ["trgepc", "obspos", "trmpts"]
CSPYCE_ABSTRACT   ["edterm"] = """
Compute a set of points on the umbral or penumbral terminator of a
specified target body, where the target shape is modeled as an
ellipsoid.
"""
CSPYCE_DEFINITIONS["edterm"] = {
"trmtyp": "Terminator type, \"UMBRAL\" or \"PENUMBRAL\".",
"source": "Light source.",
"target": "Target body.",
"et": "Observation epoch.",
"fixref": "Body-fixed frame associated with target.",
"abcorr": "Aberration correction, \"NONE\", \"LT\", \"LT+S\", \"CN\", or \"CN+S\".",
"obsrvr": "Observer.",
"npts": "Number of points in terminator set.",
"trgepc": "Epoch associated with target center.",
"obspos": "Position of observer in body-fixed frame.",
"trmpts": "Terminator point set.",
}
CSPYCE_URL["edterm"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/edterm_c.html"

#########################################
CSPYCE_SIGNATURES ["el2cgv"] = ["float[9]"]
CSPYCE_ARGNAMES   ["el2cgv"] = ["ellipse"]
CSPYCE_RETURNS    ["el2cgv"] = 3*["float[3]"]
CSPYCE_RETNAMES   ["el2cgv"] = ["center", "smajor", "sminor"]
CSPYCE_ABSTRACT   ["el2cgv"] = """
Convert a CSPICE ellipse to a center vector and two generating vectors.
The selected generating vectors are semi-axes of the ellipse.
"""
CSPYCE_DEFINITIONS["el2cgv"] = {
"ellipse": "A CSPICE ellipse.",
"center": "Center of ellipse.",
"smajor": "Semi-major axis of ellipse.",
"sminor": "Semi-minor axes of ellipse.",
}
CSPYCE_URL["el2cgv"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/el2cgv_c.html"

#########################################
CSPYCE_SIGNATURES ["eqncpv"] = ["time", "time", "float[9]", "float", "float"]
CSPYCE_ARGNAMES   ["eqncpv"] = ["et", "epoch", "eqel", "rapol", "decpol"]
CSPYCE_RETURNS    ["eqncpv"] = ["float[6]"]
CSPYCE_RETNAMES   ["eqncpv"] = ["state"]
CSPYCE_ABSTRACT   ["eqncpv"] = """
Compute the state (position and velocity of an object whose trajectory
is described via equinoctial elements relative to some fixed plane
(usually the equatorial plane of some planet).
"""
CSPYCE_DEFINITIONS["eqncpv"] = {
"et": "Epoch in seconds past J2000 to find state",
"epoch": "Epoch of elements in seconds past J2000",
"eqel": "Array of equinoctial elements",
"rapol": "Right Ascension of the pole of the reference plane",
"decpol": "Declination of the pole of the reference plane",
"state": "State of the object described by eqel.",
}
CSPYCE_URL["eqncpv"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/eqncpv_c.html"

#########################################
CSPYCE_SIGNATURES ["erract"] = ["string", "string"]
CSPYCE_ARGNAMES   ["erract"] = ["op", "action"]
CSPYCE_DEFAULTS  ["erract"] = ["GET", ""]
CSPYCE_RETURNS    ["erract"] = ["string"]
CSPYCE_RETNAMES   ["erract"] = ["action2"]
CSPYCE_ABSTRACT   ["erract"] = """
Retrieve or set the default error action.
"""
CSPYCE_DEFINITIONS["erract"] = {
"op": "Operation: \"GET\" or \"SET\"; default is \"GET\".",
"action": "Error response action for \"SET\"; ignored on \"GET\". Options are \"ABORT\", \"REPORT\", \"RETURN\", \"IGNORE\", \"DEFAULT\", \"EXCEPTION\", or \"RUNTIME\" to use the Python exception system.",
"action2": "Current or new error response action.",
}
CSPYCE_PS ["erract"] = "As a special case, if a single argument is provided and it is one of the allowed actions, then \"SET\" is assumed and the argument is interpreted as the action."
CSPYCE_URL["erract"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/erract_c.html"

#########################################
CSPYCE_SIGNATURES ["errch"] = 2*["string"]
CSPYCE_ARGNAMES   ["errch"] = ["marker", "string"]
CSPYCE_RETURNS    ["errch"] = []
CSPYCE_RETNAMES   ["errch"] = []
CSPYCE_ABSTRACT   ["errch"] = """
Substitute a character string for the first occurrence of a marker in
the current long error message.
"""
CSPYCE_DEFINITIONS["errch"] = {
"marker": "A substring of the error message to be replaced.",
"string": "The character string to substitute for marker.",
}
CSPYCE_URL["errch"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/errch_c.html"

#########################################
CSPYCE_SIGNATURES ["errdev"] = ["string", "string"]
CSPYCE_ARGNAMES   ["errdev"] = ["op", "device"]
CSPYCE_DEFAULTS  ["errdev"] = ["GET", ""]
CSPYCE_RETURNS    ["errdev"] = ["string"]
CSPYCE_RETNAMES   ["errdev"] = ["device2"]
CSPYCE_ABSTRACT   ["errdev"] = """
Retrieve or set the name of the current output device for error
messages.
"""
CSPYCE_DEFINITIONS["errdev"] = {
"op": "The operation: \"GET\" or \"SET\"; default is \"GET\".",
"device": "The device name; ignored on \"GET\". Options are a file name, \"SCREEN\" and \"NULL\".",
"device2": "Current or new output device.",
}
CSPYCE_PS ["erract"] = "As a special case, if a single argument is provided, \"SET\" is assumed and the argument is interpreted as the device."
CSPYCE_URL["errdev"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/errdev_c.html"

#########################################
CSPYCE_SIGNATURES ["errdp"] = ["string", "float"]
CSPYCE_ARGNAMES   ["errdp"] = ["marker", "number"]
CSPYCE_RETURNS    ["errdp"] = []
CSPYCE_RETNAMES   ["errdp"] = []
CSPYCE_ABSTRACT   ["errdp"] = """
Substitute a double precision number for the first occurrence of a
marker found in the current long error message.
"""
CSPYCE_DEFINITIONS["errdp"] = {
"marker": "A substring of the error message to be replaced.",
"number": "The d.p. number to substitute for marker.",
}
CSPYCE_URL["errdp"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/errdp_c.html"

#########################################
CSPYCE_SIGNATURES ["errint"] = ["string", "int"]
CSPYCE_ARGNAMES   ["errint"] = ["marker", "number"]
CSPYCE_RETURNS    ["errint"] = []
CSPYCE_RETNAMES   ["errint"] = []
CSPYCE_ABSTRACT   ["errint"] = """
Substitute an integer for the first occurrence of a marker found in the
current long error message.
"""
CSPYCE_DEFINITIONS["errint"] = {
"marker": "A substring of the error message to be replaced.",
"number": "The integer to substitute for marker.",
}
CSPYCE_URL["errint"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/errint_c.html"

#########################################
CSPYCE_SIGNATURES ["errprt"] = ["string", "string"]
CSPYCE_ARGNAMES   ["errprt"] = ["op", "list"]
CSPYCE_DEFAULTS  ["errprt"] = ["GET", ""]
CSPYCE_RETURNS    ["errprt"] = ["string"]
CSPYCE_RETNAMES   ["errprt"] = ["list2"]
CSPYCE_ABSTRACT   ["errprt"] = """
Retrieve or set the list of error message items to be output when an
error is detected.
"""
CSPYCE_DEFINITIONS["errprt"] = {
"op": "The operation: \"GET\" or \"SET\"; default is \"GET\"",
"list": "Specification of error messages to be output on \"SET\"; ignored on \"GET\". Options are \"SHORT\", \"LONG\", \"EXPLAIN\", \"TRACEBACK\", \"ALL\", \"NONE\" and \"DEFAULT\". Specified options add to current set; use \"NONE\" to clear and start over.",
"list2": "The current or new list.",
}

CSPYCE_PS ["errprt"] = "As a special case, if a single argument is provided and is not \"GET\", then \"SET\" is assumed and this argument is interpreted as the list."
CSPYCE_URL["errprt"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/errprt_c.html"

#########################################
CSPYCE_SIGNATURES ["et2lst"] = ["time", "body_code", "float", "string"]
CSPYCE_ARGNAMES   ["et2lst"] = ["et", "body", "lon", "type"]
CSPYCE_RETURNS    ["et2lst"] = 3*["float"] + 2*["string"]
CSPYCE_RETNAMES   ["et2lst"] = ["hr", "mn", "sc", "time", "ampm"]
CSPYCE_ABSTRACT   ["et2lst"] = """
Given an ephemeris epoch, compute the local solar time for an object on
the surface of a body at a specified longitude.
"""
CSPYCE_DEFINITIONS["et2lst"] = {
"et": "Epoch in seconds past J2000 epoch.",
"body": "ID-code of the body of interest.",
"lon": "Longitude of surface point (radians).",
"type": "Type of longitude \"PLANETOCENTRIC\", etc.",
"hr": "Local hour on a \"24 hour\" clock.",
"mn": "Minutes past the hour.",
"sc": "Seconds past the minute.",
"time": "String giving local time on 24 hour clock.",
"ampm": "String giving time on A.M./ P.M. scale.",
}
CSPYCE_URL["et2lst"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/et2lst_c.html"

#########################################
CSPYCE_SIGNATURES ["et2utc"] = ["time", "string", "int"]
CSPYCE_ARGNAMES   ["et2utc"] = ["et", "format", "prec"]
CSPYCE_RETURNS    ["et2utc"] = ["string"]
CSPYCE_RETNAMES   ["et2utc"] = ["utcstr"]
CSPYCE_ABSTRACT   ["et2utc"] = """
Convert an input time from ephemeris seconds past J2000 to Calendar,
Day-of-Year, or Julian Date format, UTC.
"""
CSPYCE_DEFINITIONS["et2utc"] = {
"et": "Input epoch, given in ephemeris seconds past J2000.",
"format": "Format of output epoch: \"C\" for calendar format; \"D\" for day-of-year format; \"J\" for Julian date; \"ISOC\" for ISO calendar format; \"ISOD\" for ISO day-of-year format.",
"prec": "Digits of precision in fractional seconds or days.",
"utcstr": "Output time string, UTC.",
}
CSPYCE_URL["et2utc"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/et2utc_c.html"

#########################################
CSPYCE_SIGNATURES ["etcal"] = ["time"]
CSPYCE_ARGNAMES   ["etcal"] = ["et"]
CSPYCE_RETURNS    ["etcal"] = ["string"]
CSPYCE_RETNAMES   ["etcal"] = ["string"]
CSPYCE_ABSTRACT   ["etcal"] = """
Convert from an ephemeris epoch measured in seconds past the epoch of
J2000 to a calendar string format using a formal calendar free of
leapseconds.
"""
CSPYCE_DEFINITIONS["etcal"] = {
"et": "Ephemeris time measured in seconds past J2000.",
"string": "A standard calendar representation of et.",
}
CSPYCE_URL["etcal"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/etcal_c.html"

#########################################
CSPYCE_SIGNATURES ["eul2m"] = 3*["float"] + 3*["int"]
CSPYCE_ARGNAMES   ["eul2m"] = ["angle3", "angle2", "angle1", "axis3", "axis2", "axis1"]
CSPYCE_RETURNS    ["eul2m"] = ["rotmat[3,3]"]
CSPYCE_RETNAMES   ["eul2m"] = ["rotmat"]
CSPYCE_ABSTRACT   ["eul2m"] = """
Construct a rotation matrix from a set of Euler angles.
"""
CSPYCE_DEFINITIONS["eul2m"] = {
"angle3": "Rotation angle about the third axis (radians).",
"angle2": "Rotation angle about the second axis (radians).",
"angle1": "Rotation angles about the first axis (radians).",
"axis3" : "Axis number (1,2, or 3) of the third rotation axis.",
"axis2" : "Axis number (1,2, or 3) of the second rotation axis.",
"axis1" : "Axis number (1,2, or 3) of the first rotation axis.",
"rotmat": "Product of the 3 rotations.",
}
CSPYCE_URL["eul2m"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/eul2m_c.html"

#########################################
CSPYCE_SIGNATURES ["eul2xf"] = ["float[6]"] + 3*["int"]
CSPYCE_ARGNAMES   ["eul2xf"] = ["eulang", "axisa", "axisb", "axisc"]
CSPYCE_RETURNS    ["eul2xf"] = ["rotmat[6,6]"]
CSPYCE_RETNAMES   ["eul2xf"] = ["xform"]
CSPYCE_ABSTRACT   ["eul2xf"] = """
This routine computes a state transformation from an Euler angle
factorization of a rotation and the derivatives of those Euler angles.
"""
CSPYCE_DEFINITIONS["eul2xf"] = {
"eulang": "An array of Euler angles and their derivatives.",
"axisa": "Axis A of the Euler angle factorization.",
"axisb": "Axis B of the Euler angle factorization.",
"axisc": "Axis C of the Euler angle factorization.",
"xform": "A state transformation matrix.",
}
CSPYCE_URL["eul2xf"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/eul2xf_c.html"

#########################################
CSPYCE_SIGNATURES ["expool"] = ["string"]
CSPYCE_ARGNAMES   ["expool"] = ["name"]
CSPYCE_RETURNS    ["expool"] = ["bool"]
CSPYCE_RETNAMES   ["expool"] = ["found"]
CSPYCE_ABSTRACT   ["expool"] = """
Confirm the existence of a kernel variable in the kernel pool.
"""
CSPYCE_DEFINITIONS["expool"] = {
"name": "Name of the variable whose value is to be returned.",
"found": "True if the variable is in the pool; False othewise.",
}
CSPYCE_URL["expool"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/expool_c.html"

#########################################
CSPYCE_SIGNATURES ["failed"] = []
CSPYCE_ARGNAMES   ["failed"] = []
CSPYCE_RETURNS    ["failed"] = ["bool"]
CSPYCE_RETNAMES   ["failed"] = ["value"]
CSPYCE_ABSTRACT   ["failed"] = """
True if an error condition has been signalled via sigerr. failed is the
CSPICE status indicator.
"""
CSPYCE_DEFINITIONS["failed"] = {
"value": "True if an error condition was detected; it is False otherwise.",
}
CSPYCE_URL["failed"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/failed_c.html"

#########################################
CSPYCE_SIGNATURES ["fovray"] = ["string", "float[3]", "frame_name", "string", "body_name", "time"]
CSPYCE_ARGNAMES   ["fovray"] = ["inst", "raydir", "rframe", "abcorr", "observer", "et"]
CSPYCE_RETURNS    ["fovray"] = ["bool"]
CSPYCE_RETNAMES   ["fovray"] = ["visible"]
CSPYCE_ABSTRACT   ["fovray"] = """
Determine if a specified ray is within the field-of-view (FOV) of a
specified instrument at a given time.
"""
CSPYCE_DEFINITIONS["fovray"] = {
"inst": "Name or ID code string of the instrument.",
"raydir": "Ray's direction vector.",
"rframe": "Body-fixed, body-centered frame for target body.",
"abcorr": "Aberration correction, \"NONE\", \"LT\", \"LT+S\", \"CN\", or \"CN+S\".",
"observer": "Name or ID code string of the observer.",
"et": "Time of the observation (seconds past J2000).",
"visible": "Visibility flag (True/False).",
}
CSPYCE_URL["fovray"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/fovray_c.html"

#########################################
CSPYCE_SIGNATURES ["fovtrg"] = ["string", "body_name", "string", "frame_name", "string", "body_name", "time"]
CSPYCE_ARGNAMES   ["fovtrg"] = ["inst", "target", "tshape", "tframe", "abcorr", "obsrvr", "et"]
CSPYCE_RETURNS    ["fovtrg"] = ["bool"]
CSPYCE_RETNAMES   ["fovtrg"] = ["visible"]
CSPYCE_ABSTRACT   ["fovtrg"] = """
Determine if a specified ephemeris object is within the field-of-view
(FOV) of a specified instrument at a given time.
"""
CSPYCE_DEFINITIONS["fovtrg"] = {
"inst": "Name or ID code string of the instrument.",
"target": "Name or ID code string of the target.",
"tshape": "Type of shape model used for the target.",
"tframe": "Body-fixed, body-centered frame for target body.",
"abcorr": "Aberration correction, \"NONE\", \"LT\", \"LT+S\", \"CN\", or \"CN+S\".",
"obsrvr": "Name or ID code string of the observer.",
"et": "Time of the observation (seconds past J2000).",
"visible": "Visibility flag (True/False).",
}
CSPYCE_URL["fovtrg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/fovtrg_c.html"

#########################################
CSPYCE_SIGNATURES ["frame"] = ["float[3]"]
CSPYCE_ARGNAMES   ["frame"] = ["xin"]
CSPYCE_RETURNS    ["frame"] = 3*["float[3]"]
CSPYCE_RETNAMES   ["frame"] = ["x", "y", "z"]
CSPYCE_ABSTRACT   ["frame"] = """
Given a vector x, this routine builds a right handed orthonormal frame
x,y,z where the output x is parallel to the input x.
"""
CSPYCE_DEFINITIONS["frame"] = {
"xin": "Input vector.",
"x": "A unit vector parallel to xin.",
"y": "Unit vector in the plane orthogonal to x.",
"z": "Unit vector given by x X y.",
}
CSPYCE_URL["frame"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/frame_c.html"

#########################################
CSPYCE_SIGNATURES ["frinfo"] = ["frame_code"]
CSPYCE_ARGNAMES   ["frinfo"] = ["frcode"]
CSPYCE_RETURNS    ["frinfo"] = 3*["int"] + ["bool"]
CSPYCE_RETNAMES   ["frinfo"] = ["cent", "frclss", "clssid", "found"]
CSPYCE_ABSTRACT   ["frinfo"] = """
Retrieve the minimal attributes associated with a frame needed for
converting transformations to and from it.
"""
CSPYCE_DEFINITIONS["frinfo"] = {
"frcode": "the idcode for some frame",
"cent": "the center of the frame",
"frclss": "the class (type) of the frame",
"clssid": "the idcode for the frame within its class.",
"found": "True if the requested information is available.",
}
CSPYCE_URL["frinfo"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/frinfo_c.html"

CSPYCE_SIGNATURES ["frinfo_error"] = ["frame_code"]
CSPYCE_ARGNAMES   ["frinfo_error"] = ["frcode"]
CSPYCE_RETURNS    ["frinfo_error"] = 3*["int"]
CSPYCE_RETNAMES   ["frinfo_error"] = ["cent", "frclss", "clssid"]
CSPYCE_ABSTRACT   ["frinfo_error"] = """
Retrieve the minimal attributes associated with a frame needed for
converting transformations to and from it.
"""
CSPYCE_DEFINITIONS["frinfo_error"] = {
"frcode": "the idcode for some frame",
"cent"  : "the center of the frame",
"frclss": "the class (type) of the frame",
"clssid": "the idcode for the frame within its class.",
}
CSPYCE_PS ["frinfo_error"] = "Raise SPICE(FRAMEIDNOTFOUND) condition if the requested information is unavailable."
CSPYCE_URL["frinfo_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/frinfo_c.html"

#########################################
CSPYCE_SIGNATURES ["frmchg"] = ["frame_code", "frame_code", "time"]
CSPYCE_ARGNAMES   ["frmchg"] = ["frame1", "frame2", "et"]
CSPYCE_RETURNS    ["frmchg"] = ["rotmat[6,6]"]
CSPYCE_RETNAMES   ["frmchg"] = ["xform"]
CSPYCE_ABSTRACT   ["frmchg"] = """
Return the state transformation matrix from one frame to another.
"""
CSPYCE_DEFINITIONS["frmchg"] = {
"frame1": "the frame id-code for some reference frame",
"frame2": "the frame id-code for some reference frame",
"et"    : "an epoch in TDB seconds past J2000.",
"xform" : "a state transformation matrix",
}
CSPYCE_URL["frmchg"] = ""

#########################################
CSPYCE_SIGNATURES ["frmnam"] = ["frame_code"]
CSPYCE_ARGNAMES   ["frmnam"] = ["frcode"]
CSPYCE_RETURNS    ["frmnam"] = ["frame_name"]
CSPYCE_RETNAMES   ["frmnam"] = ["frname"]
CSPYCE_ABSTRACT   ["frmnam"] = """
Retrieve the name of a reference frame associated with a SPICE ID code.
"""
CSPYCE_DEFINITIONS["frmnam"] = {
"frcode": "an integer code for a reference frame",
"frname": "the name associated with the reference frame; blank on error.",
}
CSPYCE_URL["frmnam"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/frmnam_c.html"

CSPYCE_SIGNATURES ["frmnam_error"] = ["frame_code"]
CSPYCE_ARGNAMES   ["frmnam_error"] = ["frcode"]
CSPYCE_RETURNS    ["frmnam_error"] = ["frame_name"]
CSPYCE_RETNAMES   ["frmnam_error"] = ["frname"]
CSPYCE_ABSTRACT   ["frmnam_error"] = """
Retrieve the name of a reference frame associated with a SPICE ID code.
"""
CSPYCE_DEFINITIONS["frmnam_error"] = {
"frcode": "an integer code for a reference frame",
"frname": "the name associated with the reference frame.",
}
CSPYCE_PS ["frmnam_error"] = "Raise SPICE(FRAMEIDNOTFOUND) if not found."
CSPYCE_URL["frmnam_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/frmnam_c.html"

#########################################
CSPYCE_SIGNATURES ["furnsh"] = ["string"]
CSPYCE_ARGNAMES   ["furnsh"] = ["file"]
CSPYCE_RETURNS    ["furnsh"] = []
CSPYCE_RETNAMES   ["furnsh"] = []
CSPYCE_ABSTRACT   ["furnsh"] = """
Load one or more SPICE kernels into a program.
"""
CSPYCE_DEFINITIONS["furnsh"] = {
"file": "Name of SPICE kernel file.",
}
CSPYCE_URL["furnsh"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/furnsh_c.html"

#########################################
CSPYCE_SIGNATURES ["gcpool"] = ["string", "int"]
CSPYCE_ARGNAMES   ["gcpool"] = ["name", "start"]
CSPYCE_DEFAULTS   ["gcpool"] = [0]
CSPYCE_RETURNS    ["gcpool"] = ["string[*]", "bool"]
CSPYCE_RETNAMES   ["gcpool"] = ["cvals", "found"]
CSPYCE_ABSTRACT   ["gcpool"] = """
Return the character value of a kernel variable from the kernel pool.
"""
CSPYCE_DEFINITIONS["gcpool"] = {
"name" : "Name of the variable whose value is to be returned.",
"start": "Which component to start retrieving for name; default is 0.",
"cvals": "Values associated with name.",
"found": "True if variable is in pool.",
}
CSPYCE_URL["gcpool"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gcpool_c.html"

CSPYCE_SIGNATURES ["gcpool_error"] = ["string", "int"]
CSPYCE_ARGNAMES   ["gcpool_error"] = ["name", "start"]
CSPYCE_RETURNS    ["gcpool_error"] = ["string[*]"]
CSPYCE_RETNAMES   ["gcpool_error"] = ["cvals"]
CSPYCE_ABSTRACT   ["gcpool_error"] = """
Return the character value of a kernel variable from the kernel pool.
"""
CSPYCE_DEFINITIONS["gcpool_error"] = {
"name" : "Name of the variable whose value is to be returned.",
"start": "Which component to start retrieving for name; default is 0.",
"cvals": "Values associated with name.",
}
CSPYCE_PS ["gcpool_error"] = "Raise a SPICE error condition if the variable is not in the pool, if it has the wrong type, or if the start index is out of range."
CSPYCE_URL["gcpool_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gcpool_c.html"

#########################################
CSPYCE_SIGNATURES ["gdpool"] = ["string", "int"]
CSPYCE_ARGNAMES   ["gdpool"] = ["name", "start"]
CSPYCE_DEFAULTS   ["gdpool"] = [0]
CSPYCE_RETURNS    ["gdpool"] = ["float[*]", "bool"]
CSPYCE_RETNAMES   ["gdpool"] = ["values", "found"]
CSPYCE_ABSTRACT   ["gdpool"] = """
Return the float value of a kernel variable from the kernel pool.
"""
CSPYCE_DEFINITIONS["gdpool"] = {
"name" : "Name of the variable whose value is to be returned.",
"start": "Which component to start retrieving for name; default is 0.",
"values": "Values associated with name.",
"found": "True if variable is in pool.",
}
CSPYCE_URL["gdpool"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gdpool_c.html"

CSPYCE_SIGNATURES ["gdpool_error"] = ["string", "int"]
CSPYCE_ARGNAMES   ["gdpool_error"] = ["name", "start"]
CSPYCE_DEFAULTS   ["gdpool_error"] = [0]
CSPYCE_RETURNS    ["gdpool_error"] = ["float[*]"]
CSPYCE_RETNAMES   ["gdpool_error"] = ["values"]
CSPYCE_ABSTRACT   ["gdpool_error"] = """
Return the float value of a kernel variable from the kernel pool.
"""
CSPYCE_DEFINITIONS["gdpool_error"] = {
"name"  : "Name of the variable whose value is to be returned.",
"start" : "Which component to start retrieving for name; default is 0.",
"values": "Values associated with name.",
}
CSPYCE_PS ["gdpool_error"] = "Raise a SPICE error condition if the variable is not in the pool, if it has the wrong type, or if the start index is out of range."
CSPYCE_URL["gdpool_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gdpool_c.html"

#########################################
CSPYCE_SIGNATURES ["georec"] = 5*["float"]
CSPYCE_ARGNAMES   ["georec"] = ["lon", "lat", "alt", "re", "f"]
CSPYCE_RETURNS    ["georec"] = ["float[3]"]
CSPYCE_RETNAMES   ["georec"] = ["rectan"]
CSPYCE_ABSTRACT   ["georec"] = """
Convert geodetic coordinates to rectangular coordinates.
"""
CSPYCE_DEFINITIONS["georec"] = {
"lon": "Geodetic longitude of point (radians).",
"lat": "Geodetic latitude  of point (radians).",
"alt": "Altitude of point above the reference spheroid.",
"re" : "Equatorial radius of the reference spheroid.",
"f"  : "Flattening coefficient.",
"rectan": "Rectangular coordinates of point.",
}
CSPYCE_URL["georec"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/georec_c.html"

#########################################
CSPYCE_SIGNATURES ["getfov"] = ["int"]
CSPYCE_ARGNAMES   ["getfov"] = ["instid"]
CSPYCE_RETURNS    ["getfov"] = ["string", "string", "float[3]", "float[*,3]"]
CSPYCE_RETNAMES   ["getfov"] = ["shape", "frame", "bsight", "bounds"]
CSPYCE_ABSTRACT   ["getfov"] = """
This subroutine returns the field-of-view (FOV) configuration for a
specified instrument.
"""
CSPYCE_DEFINITIONS["getfov"] = {
"instid": "NAIF ID of an instrument.",
"shape" : "Instrument FOV shape.",
"frame" : "Name of the frame in which FOV vectors are defined.",
"bsight": "Boresight vector.",
"bounds": "FOV boundary vectors.",
}
CSPYCE_URL["getfov"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/getfov_c.html"

#########################################
CSPYCE_SIGNATURES ["getmsg"] = ["string"]
CSPYCE_ARGNAMES   ["getmsg"] = ["option"]
CSPYCE_RETURNS    ["getmsg"] = ["string"]
CSPYCE_RETNAMES   ["getmsg"] = ["msg"]
CSPYCE_ABSTRACT   ["getmsg"] = """
Retrieve the current short error message, the explanation of the short
error message, or the long error message.
"""
CSPYCE_DEFINITIONS["getmsg"] = {
"option": "Indicates type of error message, \"SHORT\", \"LONG\", or \"EXPLAIN\".",
"msg"   : "The error message to be retrieved.",
}
CSPYCE_URL["getmsg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/getmsg_c.html"

#########################################
CSPYCE_SIGNATURES ["gipool"] = ["string", "int"]
CSPYCE_ARGNAMES   ["gipool"] = ["name", "start"]
CSPYCE_DEFAULTS   ["gipool"] = [0]
CSPYCE_RETURNS    ["gipool"] = ["int[*]", "bool"]
CSPYCE_RETNAMES   ["gipool"] = ["ivals", "found"]
CSPYCE_ABSTRACT   ["gipool"] = """
Return the integer value of a kernel variable from the kernel pool.
"""
CSPYCE_DEFINITIONS["gipool"] = {
"name": "Name of the variable whose value is to be returned.",
"start": "Which component to start retrieving for name; default is 0.",
"ivals": "Values associated with name.",
"found": "True if variable is in pool.",
}
CSPYCE_URL["gipool"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gipool_c.html"

CSPYCE_SIGNATURES ["gipool_error"] = ["string", "int"]
CSPYCE_ARGNAMES   ["gipool_error"] = ["name", "start"]
CSPYCE_DEFAULTS   ["gipool_error"] = [0]
CSPYCE_RETURNS    ["gipool_error"] = ["int[*]"]
CSPYCE_RETNAMES   ["gipool_error"] = ["ivals"]
CSPYCE_ABSTRACT   ["gipool_error"] = """
Return the integer value of a kernel variable from the kernel pool.
"""
CSPYCE_DEFINITIONS["gipool_error"] = {
"name": "Name of the variable whose value is to be returned.",
"start": "Which component to start retrieving for name; default is 0.",
"ivals": "Values associated with name.",
}
CSPYCE_PS ["gipool_error"] = "Raise a SPICE error condition if the variable is not in the pool, if it has the wrong type, or if the start index is out of range."
CSPYCE_URL["gipool_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gipool_c.html"

#########################################
CSPYCE_SIGNATURES ["gnpool"] = ["string", "int"]
CSPYCE_ARGNAMES   ["gnpool"] = ["name", "start"]
CSPYCE_DEFAULTS   ["gnpool"] = [0]
CSPYCE_RETURNS    ["gnpool"] = ["string[*]", "bool"]
CSPYCE_RETNAMES   ["gnpool"] = ["kvars", "found"]
CSPYCE_ABSTRACT   ["gnpool"] = """
Return names of kernel variables matching a specified template.
"""
CSPYCE_DEFINITIONS["gnpool"] = {
"name": "Template that names should match.",
"start": "Index of first matching name to retrieve; default is 0.",
"kvars": "Kernel pool variables whose names match name.",
"found": "True if variable is in pool.",
}
CSPYCE_PS ["gnpool"] = "Raise a SPICE error condition if the variable is not in the pool, if it has the wrong type, or if the start index is out of range."
CSPYCE_URL["gnpool"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gnpool_c.html"

CSPYCE_SIGNATURES ["gnpool_error"] = ["string", "int"]
CSPYCE_ARGNAMES   ["gnpool_error"] = ["name", "start"]
CSPYCE_DEFAULTS   ["gnpool_error"] = [0]
CSPYCE_RETURNS    ["gnpool_error"] = ["string[*]"]
CSPYCE_RETNAMES   ["gnpool_error"] = ["kvars"]
CSPYCE_ABSTRACT   ["gnpool_error"] = """
Return names of kernel variables matching a specified template.
"""
CSPYCE_DEFINITIONS["gnpool_error"] = {
"name": "Template that names should match.",
"start": "Index of first matching name to retrieve; default is 0.",
"kvars": "Kernel pool variables whose names match name.",
}
CSPYCE_PS ["gnpool_error"] = "Raise a SPICE error condition if no variables matching the template are found in the pool, or if the start index is out of range."
CSPYCE_URL["gnpool_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gnpool_c.html"

#########################################
CSPYCE_SIGNATURES ["halfpi"] = []
CSPYCE_ARGNAMES   ["halfpi"] = []
CSPYCE_RETURNS    ["halfpi"] = ["float"]
CSPYCE_RETNAMES   ["halfpi"] = ["value"]
CSPYCE_ABSTRACT   ["halfpi"] = """
Return half the value of pi
"""
CSPYCE_DEFINITIONS["halfpi"] = {
"value": "half the value of pi"
}
CSPYCE_URL["halfpi"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/halfpi_c.html"

#########################################
CSPYCE_SIGNATURES ["ident"] = []
CSPYCE_ARGNAMES   ["ident"] = []
CSPYCE_RETURNS    ["ident"] = ["rotmat[3,3]"]
CSPYCE_RETNAMES   ["ident"] = ["matrix"]
CSPYCE_ABSTRACT   ["ident"] = """
Return the 3x3 identity matrix.
"""
CSPYCE_DEFINITIONS["ident"] = {
"matrix": "is the 3x3 identity matrix.",
}
CSPYCE_URL["ident"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ident_c.html"

#########################################
CSPYCE_SIGNATURES ["illum"] = ["body_name", "time", "string", "body_name", "float[3]"]
CSPYCE_ARGNAMES   ["illum"] = ["target", "et", "abcorr", "obsrvr", "spoint"]
CSPYCE_RETURNS    ["illum"] = 3*["float"]
CSPYCE_RETNAMES   ["illum"] = ["phase", "solar", "emissn"]
CSPYCE_ABSTRACT   ["illum"] = """
Find the illumination angles at a specified surface point of a target
body.
"""
CSPYCE_DEFINITIONS["illum"] = {
"target": "Name of target body.",
"et": "Epoch in ephemeris seconds past J2000.",
"abcorr": "Aberration correction, \"NONE\", \"LT\", \"LT+S\", \"CN\", or \"CN+S\".",
"obsrvr": "Name of observing body.",
"spoint": "Body-fixed coordinates of a target surface point.",
"phase": "Phase angle at the surface point.",
"solar": "Solar incidence angle at the surface point.",
"emissn": "Emission angle at the surface point.",
}
CSPYCE_URL["illum"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/illum_c.html"

#########################################
CSPYCE_SIGNATURES ["illumf"] = ["string", "body_name", "body_name", "time", "frame_name", "string", "body_name", "float[3]"]
CSPYCE_ARGNAMES   ["illumf"] = ["method", "target", "ilusrc", "et", "fixref", "abcorr", "obsrvr", "spoint"]
CSPYCE_RETURNS    ["illumf"] = ["float", "float[3]", "float", "float", "float", "bool", "bool"]
CSPYCE_RETNAMES   ["illumf"] = ["trgepc", "srfvec", "phase", "incdnc", "emissn", "visibl", "lit"]
CSPYCE_ABSTRACT   ["illumf"] = """
Compute the illumination angles---phase, incidence, and emission---at a
specified point on a target body. Return logical flags indicating
whether the surface point is visible from the observer's position and
whether the surface point is illuminated.

The target body's surface is represented using topographic data
provided by DSK files or by a reference ellipsoid.

The illumination source is a specified ephemeris object.
"""
CSPYCE_DEFINITIONS["illumf"] = {
"method": "Computation method.",
"target": "Name of target body.",
"ilusrc": "Name of illumination source.",
"et": "Epoch in TDB seconds past J2000 TDB.",
"fixref": "Body-fixed, body-centered target body frame.",
"abcorr": "Aberration correction, \"NONE\", \"LT\", \"LT+S\", \"CN\", or \"CN+S\".",
"obsrvr": "Name of observing body.",
"spoint": "Body-fixed coordinates of a target surface point.",
"trgepc": "Target surface point epoch.",
"srfvec": "Vector from observer to target surface point.",
"phase": "Phase angle at the surface point.",
"incdnc": "Source incidence angle at the surface point.",
"emissn": "Emission angle at the surface point.",
"visibl": "Visibility flag: True for visible)",
"lit": "Illumination flag: True for illuminated.",
}
CSPYCE_URL["illumf"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/illumf_c.html"

#########################################
CSPYCE_SIGNATURES ["illumg"] = ["string", "body_name", "body_name", "time", "frame_name", "string", "body_name", "float[3]"]
CSPYCE_ARGNAMES   ["illumg"] = ["method", "target", "ilusrc", "et", "fixref", "abcorr", "obsrvr", "spoint"]
CSPYCE_RETURNS    ["illumg"] = ["float", "float[3]", "float", "float", "float"]
CSPYCE_RETNAMES   ["illumg"] = ["trgepc", "srfvec", "phase", "incdnc", "emissn"]
CSPYCE_ABSTRACT   ["illumg"] = """
Find the illumination angles (phase, incidence, and emission) at a
specified surface point of a target body.

The surface of the target body may be represented by a triaxial
ellipsoid or by topographic data provided by DSK files.

The illumination source is a specified ephemeris object.
"""
CSPYCE_DEFINITIONS["illumg"] = {
"method": "Computation method.",
"target": "Name of target body.",
"ilusrc": "Name of illumination source.",
"et": "Epoch in TDB seconds past J2000 TDB.",
"fixref": "Body-fixed, body-centered target body frame.",
"abcorr": "Aberration correction, \"NONE\", \"LT\", \"LT+S\", \"CN\", or \"CN+S\".",
"obsrvr": "Name of observing body.",
"spoint": "Body-fixed coordinates of a target surface point.",
"trgepc": "Target surface point epoch.",
"srfvec": "Vector from observer to target surface point.",
"phase": "Phase angle at the surface point.",
"incdnc": "Source incidence angle at the surface point.",
"emissn": "Emission angle at the surface point.",
}
CSPYCE_URL["illumg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/illumg_c.html"

#########################################
CSPYCE_SIGNATURES ["ilumin"] = ["string", "body_name", "time", "frame_name", "string", "body_name", "float[3]"]
CSPYCE_ARGNAMES   ["ilumin"] = ["method", "target", "et", "fixref", "abcorr", "obsrvr", "spoint"]
CSPYCE_RETURNS    ["ilumin"] = ["float", "float[3]", "float", "float", "float"]
CSPYCE_RETNAMES   ["ilumin"] = ["trgepc", "srfvec", "phase", "incdnc", "emissn"]
CSPYCE_ABSTRACT   ["ilumin"] = """
Find the illumination angles (phase, solar incidence, and emission) at a
specified surface point of a target body.

This routine supersedes illum.
"""
CSPYCE_DEFINITIONS["ilumin"] = {
"method": "Computation method.",
"target": "Name of target body.",
"et"    : "Epoch in TDB seconds past J2000 TDB.",
"fixref": "Body-fixed, body-centered target body frame.",
"abcorr": "Aberration correction, \"NONE\", \"LT\", \"LT+S\", \"CN\", or \"CN+S\".",
"obsrvr": "Name of observing body.",
"spoint": "Body-fixed coordinates of a target surface point.",
"trgepc": "Target surface point epoch.",
"srfvec": "Vector from observer to target surface point.",
"phase" : "Phase angle at the surface point.",
"incdnc": "Solar incidence angle at the surface point.",
"emissn": "Emission angle at the surface point.",
}
CSPYCE_URL["ilumin"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ilumin_c.html"

#########################################
CSPYCE_SIGNATURES ["inedpl"] = 3*["float"] + ["float[4]"]
CSPYCE_ARGNAMES   ["inedpl"] = ["a", "b", "c", "plane"]
CSPYCE_RETURNS    ["inedpl"] = ["float[9]", "bool"]
CSPYCE_RETNAMES   ["inedpl"] = ["ellipse", "found"]
CSPYCE_ABSTRACT   ["inedpl"] = """
Find the intersection of a triaxial ellipsoid and a plane.
"""
CSPYCE_DEFINITIONS["inedpl"] = {
"a": "Length of ellipsoid semi-axis lying on the x-axis.",
"b": "Length of ellipsoid semi-axis lying on the y-axis.",
"c": "Length of ellipsoid semi-axis lying on the z-axis.",
"plane": "Plane that intersects ellipsoid.",
"ellipse": "Intersection ellipse, when found is True.",
"found": "Flag indicating whether ellipse was found.",
}
CSPYCE_URL["inedpl"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/inedpl_c.html"

#########################################
CSPYCE_SIGNATURES ["inelpl"] = ["float[9]", "float[4]"]
CSPYCE_ARGNAMES   ["inelpl"] = ["ellips", "plane"]
CSPYCE_RETURNS    ["inelpl"] = ["int", "float[3]", "float[3]"]
CSPYCE_RETNAMES   ["inelpl"] = ["nxpts", "xpt1", "xpt2"]
CSPYCE_ABSTRACT   ["inelpl"] = """
Find the intersection of an ellipse and a plane.
"""
CSPYCE_DEFINITIONS["inelpl"] = {
"ellips": "A CSPICE ellipse.",
"plane": "A CSPICE plane.",
"nxpts": "Number of intersection points of plane and ellipse.",
"xpt1": "First intersection point.",
"xpt2": "Second intersection point.",
}
CSPYCE_URL["inelpl"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/inelpl_c.html"

#########################################
CSPYCE_SIGNATURES ["inrypl"] = ["float[3]", "float[3]", "float[4]"]
CSPYCE_ARGNAMES   ["inrypl"] = ["vertex", "dir", "plane"]
CSPYCE_RETURNS    ["inrypl"] = ["int", "float[3]"]
CSPYCE_RETNAMES   ["inrypl"] = ["nxpts", "xpt"]
CSPYCE_ABSTRACT   ["inrypl"] = """
Find the intersection of a ray and a plane.
"""
CSPYCE_DEFINITIONS["inrypl"] = {
"vertex": "Vertex of ray.",
"dir": "Direction vector of ray.",
"plane": "A CSPICE plane.",
"nxpts": "Number of intersection points of ray and plane.",
"xpt": "Intersection point, if nxpts = 1.",
}
CSPYCE_URL["inrypl"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/inrypl_c.html"

#########################################
CSPYCE_SIGNATURES ["intmax"] = []
CSPYCE_ARGNAMES   ["intmax"] = []
CSPYCE_RETURNS    ["intmax"] = ["int"]
CSPYCE_RETNAMES   ["intmax"] = ["value"]
CSPYCE_ABSTRACT   ["intmax"] = """
Return the value of the largest (positive) number representable in a
variable.
"""
CSPYCE_DEFINITIONS["intmax"] = {
"value": "the largest (positive) number that can be represented in a variable.",
}
CSPYCE_URL["intmax"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/intmax_c.html"

#########################################
CSPYCE_SIGNATURES ["intmin"] = []
CSPYCE_ARGNAMES   ["intmin"] = []
CSPYCE_RETURNS    ["intmin"] = ["int"]
CSPYCE_RETNAMES   ["intmin"] = ["value"]
CSPYCE_ABSTRACT   ["intmin"] = """
Return the value of the smallest (negative) number representable in a
SpiceInt variable.
"""
CSPYCE_DEFINITIONS["intmin"] = {
"value": "the smallest (negative) number that can be represented in a variable.",
}
CSPYCE_URL["intmin"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/intmin_c.html"

#########################################
CSPYCE_SIGNATURES ["invert"] = ["float[3,3]"]
CSPYCE_ARGNAMES   ["invert"] = ["m1"]
CSPYCE_RETURNS    ["invert"] = ["float[3,3]"]
CSPYCE_RETNAMES   ["invert"] = ["mout"]
CSPYCE_ABSTRACT   ["invert"] = """
Generate the inverse of a 3x3 matrix.
"""
CSPYCE_DEFINITIONS["invert"] = {
"m1": "Matrix to be inverted.",
"mout": "Inverted matrix (m1**-1).",
}
CSPYCE_PS ["invert"] = "If m1 is singular, then a matrix filled with zeros is returned."
CSPYCE_URL["invert"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/invert_c.html"

CSPYCE_SIGNATURES ["invert_error"] = ["float[3,3]"]
CSPYCE_ARGNAMES   ["invert_error"] = ["m1"]
CSPYCE_RETURNS    ["invert_error"] = ["float[3,3]"]
CSPYCE_RETNAMES   ["invert_error"] = ["mout"]
CSPYCE_ABSTRACT   ["invert_error"] = """
Generate the inverse of a 3x3 matrix.
"""
CSPYCE_DEFINITIONS["invert_error"] = {
"m1": "Matrix to be inverted.",
"mout": "Inverted matrix (m1**-1).",
}
CSPYCE_PS ["invert_error"] = "If m1 is singular, then a SPICE(SINGULARMATRIX) condition is raised."
CSPYCE_URL["invert_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/invert_c.html"

#########################################
CSPYCE_SIGNATURES ["invort"] = ["float[3,3]"]
CSPYCE_ARGNAMES   ["invort"] = ["m"]
CSPYCE_RETURNS    ["invort"] = ["float[3,3]"]
CSPYCE_RETNAMES   ["invort"] = ["mit"]
CSPYCE_ABSTRACT   ["invort"] = """
Given a matrix, construct the matrix whose rows are the columns of the
first divided by the length squared of the the corresponding columns of
the input matrix.
"""
CSPYCE_DEFINITIONS["invort"] = {
"m": "A 3x3 matrix.",
"mit": "m after transposition and scaling of rows.",
}
CSPYCE_URL["invort"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/invort_c.html"

#########################################
CSPYCE_SIGNATURES ["isrot"] = ["float[3,3]", "float", "float"]
CSPYCE_ARGNAMES   ["isrot"] = ["m", "ntol", "dtol"]
CSPYCE_RETURNS    ["isrot"] = ["bool"]
CSPYCE_RETNAMES   ["isrot"] = ["status"]
CSPYCE_ABSTRACT   ["isrot"] = """
Indicate whether a 3x3 matrix is a rotation matrix.
"""
CSPYCE_DEFINITIONS["isrot"] = {
"m": "A matrix to be tested.",
"ntol": "Tolerance for the norms of the columns of m.",
"dtol": "Tolerance for the determinant of a matrix whose columns are the unitized columns of m.",
"status": "True if and only if m is a rotation matrix.",
}
CSPYCE_URL["isrot"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/isrot_c.html"

#########################################
CSPYCE_SIGNATURES ["j1900"] = []
CSPYCE_ARGNAMES   ["j1900"] = []
CSPYCE_RETURNS    ["j1900"] = ["float"]
CSPYCE_RETNAMES   ["j1900"] = ["jd"]
CSPYCE_ABSTRACT   ["j1900"] = """
Return the Julian Date of 1899 DEC 31 12:00:00 (1900 JAN 0.5).
"""
CSPYCE_DEFINITIONS["j1900"] = {
"jd": "Julian Date of 1900 JAN 0.5",
}
CSPYCE_URL["j1900"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/j1900_c.html"

#########################################
CSPYCE_SIGNATURES ["j1950"] = []
CSPYCE_ARGNAMES   ["j1950"] = []
CSPYCE_RETURNS    ["j1950"] = ["float"]
CSPYCE_RETNAMES   ["j1950"] = ["jd"]
CSPYCE_ABSTRACT   ["j1950"] = """
Return the Julian Date of 1950 JAN 01 00:00:00 (1950 JAN 1.0).
"""
CSPYCE_DEFINITIONS["j1950"] = {
"jd": "Julian Date of 1950 JAN 1.0",
}
CSPYCE_URL["j1950"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/j1950_c.html"

#########################################
CSPYCE_SIGNATURES ["j2000"] = []
CSPYCE_ARGNAMES   ["j2000"] = []
CSPYCE_RETURNS    ["j2000"] = ["float"]
CSPYCE_RETNAMES   ["j2000"] = ["jd"]
CSPYCE_ABSTRACT   ["j2000"] = """
Return the Julian Date of 2000 JAN 01 12:00:00 (2000 JAN 1.5).
"""
CSPYCE_DEFINITIONS["j2000"] = {
"jd": "Julian Date of 2000 JAN 1.5",
}
CSPYCE_URL["j2000"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/j2000_c.html"

#########################################
CSPYCE_SIGNATURES ["j2100"] = []
CSPYCE_ARGNAMES   ["j2100"] = []
CSPYCE_RETURNS    ["j2100"] = ["float"]
CSPYCE_RETNAMES   ["j2100"] = ["jd"]
CSPYCE_ABSTRACT   ["j2100"] = """
Return the Julian Date of 2100 JAN 01 12:00:00 (2100 JAN 1.5).
"""
CSPYCE_DEFINITIONS["j2100"] = {
"jd": "Julian Date of 2100 JAN 1.5",
}
CSPYCE_URL["j2100"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/j2100_c.html"

#########################################
CSPYCE_SIGNATURES ["jyear"] = []
CSPYCE_ARGNAMES   ["jyear"] = []
CSPYCE_RETURNS    ["jyear"] = ["float"]
CSPYCE_RETNAMES   ["jyear"] = ["value"]
CSPYCE_ABSTRACT   ["jyear"] = """
Return the number of seconds in a julian year.
"""
CSPYCE_DEFINITIONS["jyear"] = {
"value": "number of seconds in a julian year",
}
CSPYCE_URL["jyear"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/jyear_c.html"

#########################################
CSPYCE_SIGNATURES ["kplfrm"] = ["int"]
CSPYCE_ARGNAMES   ["kplfrm"] = ["frmcls"]
CSPYCE_RETURNS    ["kplfrm"] = ["int[*]"]
CSPYCE_RETNAMES   ["kplfrm"] = ["idset"]
CSPYCE_ABSTRACT   ["kplfrm"] = """
Return an array containing the frame IDs of all reference frames of a
given class having specifications in the kernel pool.
"""
CSPYCE_DEFINITIONS["kplfrm"] = {
"frmcls": "Frame class (-1 = all; 1 = built-in inertial; 2 = PCK-based; 3 = CK-based; 4 = fixed rotational; 5 = dynamic).",
"idset": "Set of ID codes of frames of the specified class.",
}
CSPYCE_URL["kplfrm"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/kplfrm_c.html"

#########################################
CSPYCE_SIGNATURES ["latcyl"] = 3*["float"]
CSPYCE_ARGNAMES   ["latcyl"] = ["radius", "lon", "lat"]
CSPYCE_RETURNS    ["latcyl"] = 3*["float"]
CSPYCE_RETNAMES   ["latcyl"] = ["r", "lonc", "z"]
CSPYCE_ABSTRACT   ["latcyl"] = """
Convert from latitudinal coordinates to cylindrical coordinates.
"""
CSPYCE_DEFINITIONS["latcyl"] = {
"radius": "Distance of a point from the origin.",
"lon": "Angle of the point from the XZ plane in radians.",
"lat": "Angle of the point from the XY plane in radians.",
"r": "Distance of the point from the z axis.",
"lonc": "Angle of the point from the XZ plane in radians.",
"z": "Height of the point above the XY plane.",
}
CSPYCE_URL["latcyl"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/latcyl_c.html"

#########################################
CSPYCE_SIGNATURES ["latrec"] = 3*["float"]
CSPYCE_ARGNAMES   ["latrec"] = ["radius", "lon", "lat"]
CSPYCE_RETURNS    ["latrec"] = ["float[3]"]
CSPYCE_RETNAMES   ["latrec"] = ["rectan"]
CSPYCE_ABSTRACT   ["latrec"] = """
Convert from latitudinal coordinates to rectangular coordinates.
"""
CSPYCE_DEFINITIONS["latrec"] = {
"radius": "Distance of a point from the origin.",
"lon": "Longitude of point in radians.",
"lat": "Latitude of point in radians.",
"rectan": "Rectangular coordinates of the point.",
}
CSPYCE_URL["latrec"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/latrec_c.html"

#########################################
CSPYCE_SIGNATURES ["latsrf"] = ["string", "body_name", "time", "frame_name", "float[*,2]"]
CSPYCE_ARGNAMES   ["latsrf"] = ["method", "target", "et", "fixref", "lonlat"]
CSPYCE_RETURNS    ["latsrf"] = ["float[*,3]"]
CSPYCE_RETNAMES   ["latsrf"] = ["srfpts"]
CSPYCE_ABSTRACT   ["latsrf"] = """
Map array of planetocentric longitude/latitude coordinate pairs to
surface points on a specified target body.

The surface of the target body may be represented by a triaxial
ellipsoid or by topographic data provided by DSK files.
"""
CSPYCE_DEFINITIONS["latsrf"] = {
"method": "Computation method: ELLIPSOID or DSK/UNPRIORITIZED[/SURFACES = <surface list>].",
"target": "Name of target body.",
"et": "Epoch in TDB seconds past J2000 TDB.",
"fixref": "Body-fixed, body-centered target body frame.",
"lonlat": "Array of longitude/latitude coordinate pairs.",
"srfpts": "Array of surface points.",
}
CSPYCE_URL["latsrf"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/latsrf_c.html"

#########################################
CSPYCE_SIGNATURES ["latsph"] = 3*["float"]
CSPYCE_ARGNAMES   ["latsph"] = ["radius", "lon", "lat"]
CSPYCE_RETURNS    ["latsph"] = 3*["float"]
CSPYCE_RETNAMES   ["latsph"] = ["rho", "colat", "lon2"]
CSPYCE_ABSTRACT   ["latsph"] = """
Convert from latitudinal coordinates to spherical coordinates.
"""
CSPYCE_DEFINITIONS["latsph"] = {
"radius": "Distance of a point from the origin.",
"lon": "Angle of the point from the XZ plane in radians.",
"lat": "Angle of the point from the XY plane in radians.",
"rho": "Distance of the point from the origin.",
"colat": "Angle of the point from positive z axis (radians).",
"lon2": "Angle of the point from the XZ plane (radians).",
}
CSPYCE_URL["latsph"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/latsph_c.html"

#########################################
CSPYCE_SIGNATURES ["ldpool"] = ["string"]
CSPYCE_ARGNAMES   ["ldpool"] = ["filename"]
CSPYCE_RETURNS    ["ldpool"] = []
CSPYCE_RETNAMES   ["ldpool"] = []
CSPYCE_ABSTRACT   ["ldpool"] = """
Load the variables contained in a NAIF ASCII kernel file into the kernel
pool.
"""
CSPYCE_DEFINITIONS["ldpool"] = {
"filename": "Name of the kernel file.",
}
CSPYCE_URL["ldpool"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ldpool_c.html"

#########################################
CSPYCE_SIGNATURES ["limbpt"] = ["string", "body_name", "time", "frame_name", "string", "string", "body_name", "float[3]", "float", "int", "float", "float", "int"]
CSPYCE_ARGNAMES   ["limbpt"] = ["method", "target", "et", "fixref", "abcorr", "corloc", "obsrvr", "refvec", "rolstp", "ncuts", "schstp", "soltol", "maxn"]
CSPYCE_RETURNS    ["limbpt"] = ["int[*]", "float[*,3]", "float[*]", "float[*,3]"]
CSPYCE_RETNAMES   ["limbpt"] = ["npts", "points", "epochs", "tangts"]
CSPYCE_ABSTRACT   ["limbpt"] = """
Find limb points on a target body. The limb is the set of points of
tangency on the target of rays emanating from the observer. The caller
specifies half-planes bounded by the observer-target center vector in
which to search for limb points.

The surface of the target body may be represented either by a triaxial
ellipsoid or by topographic data.
"""
CSPYCE_DEFINITIONS["limbpt"] = {
"method": "Computation method.",
"target": "Name of target body.",
"et": "Epoch in ephemeris seconds past J2000 TDB.",
"fixref": "Body-fixed, body-centered target body frame.",
"abcorr": "Aberration correction, \"NONE\", \"LT\", \"LT+S\", \"CN\", or \"CN+S\".",
"corloc": "Aberration correction locus.",
"obsrvr": "Name of observing body.",
"refvec": "Reference vector for cutting half-planes.",
"rolstp": "Roll angular step for cutting half-planes.",
"ncuts": "Number of cutting half-planes.",
"schstp": "Angular step size for searching.",
"soltol": "Solution convergence tolerance.",
"maxn": "Maximum number of entries in output arrays.",
"npts": "Counts of limb points corresponding to cuts.",
"points": "Limb points.",
"epochs": "Times associated with limb points.",
"tangts": "Tangent vectors emanating from the observer.",
}
CSPYCE_URL["limbpt"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/limbpt_c.html"

#########################################
CSPYCE_SIGNATURES ["lspcn"] = ["body_name", "time", "string"]
CSPYCE_ARGNAMES   ["lspcn"] = ["body", "et", "abcorr"]
CSPYCE_RETURNS    ["lspcn"] = ["float"]
CSPYCE_RETNAMES   ["lspcn"] = ["value"]
CSPYCE_ABSTRACT   ["lspcn"] = """
Compute L_s, the planetocentric longitude of the sun, as seen from a
specified body.
"""
CSPYCE_DEFINITIONS["lspcn"] = {
"body": "Name of central body.",
"et": "Epoch in seconds past J2000 TDB.",
"abcorr": "Aberration correction, \"NONE\", \"LT\", \"LT+S\", \"CN\", or \"CN+S\".",
"value": "L_s for the specified body at the specified time.",
}
CSPYCE_URL["lspcn"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/lspcn_c.html"

#########################################
CSPYCE_SIGNATURES ["ltime"] = ["time", "body_code", "string", "body_code"]
CSPYCE_ARGNAMES   ["ltime"] = ["etobs", "obs", "dir", "targ"]
CSPYCE_RETURNS    ["ltime"] = ["float", "float"]
CSPYCE_RETNAMES   ["ltime"] = ["ettarg", "elapsd"]
CSPYCE_ABSTRACT   ["ltime"] = """
Light Time
"""
CSPYCE_DEFINITIONS["ltime"] = {
"etobs": "Epoch of a signal at some observer",
"obs": "NAIF ID of some observer",
"dir": "Direction the signal travels (\"->\" or \"<-\")",
"targ": "NAIF ID of the target object",
"ettarg": "Epoch of the signal at the target",
"elapsd": "Time between transmit and receipt of the signal",
}
CSPYCE_URL["ltime"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ltime_c.html"

#########################################
CSPYCE_SIGNATURES ["m2eul"] = ["rotmat[3,3]"] + 3*["int"]
CSPYCE_ARGNAMES   ["m2eul"] = ["r", "axis3", "axis2", "axis1"]
CSPYCE_RETURNS    ["m2eul"] = 3*["float"]
CSPYCE_RETNAMES   ["m2eul"] = ["angle3", "angle2", "angle1"]
CSPYCE_ABSTRACT   ["m2eul"] = """
Factor a rotation matrix as a product of three rotations about specified
coordinate axes.
"""
CSPYCE_DEFINITIONS["m2eul"] = {
"r": "A rotation matrix to be factored.",
"axis3": "Number of the third rotation axis.",
"axis2": "Number of the second rotation axis.",
"axis1": "Number of the first rotation axis.",
"angle3": "Third Euler angle, in radians.",
"angle2": "Second Euler angle, in radians.",
"angle1": "First Euler angle, in radians.",
}
CSPYCE_URL["m2eul"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/m2eul_c.html"

#########################################
CSPYCE_SIGNATURES ["m2q"] = ["rotmat[3,3]"]
CSPYCE_ARGNAMES   ["m2q"] = ["r"]
CSPYCE_RETURNS    ["m2q"] = ["float[4]"]
CSPYCE_RETNAMES   ["m2q"] = ["q"]
CSPYCE_ABSTRACT   ["m2q"] = """
Find a unit quaternion corresponding to a specified rotation matrix.
"""
CSPYCE_DEFINITIONS["m2q"] = {
"r": "A rotation matrix.",
"q": "A unit quaternion representing r.",
}
CSPYCE_URL["m2q"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/m2q_c.html"

#########################################
CSPYCE_SIGNATURES ["mequ"] = ["float[3,3]"]
CSPYCE_ARGNAMES   ["mequ"] = ["m1"]
CSPYCE_RETURNS    ["mequ"] = ["float[3,3]"]
CSPYCE_RETNAMES   ["mequ"] = ["mout"]
CSPYCE_ABSTRACT   ["mequ"] = """
Set one double precision 3x3 matrix equal to another.
"""
CSPYCE_DEFINITIONS["mequ"] = {
"m1": "Input matrix.",
"mout": "Output matrix equal to m1.",
}
CSPYCE_URL["mequ"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mequ_c.html"

#########################################
CSPYCE_SIGNATURES ["mequg"] = ["float[*,*]"]
CSPYCE_ARGNAMES   ["mequg"] = ["m1"]
CSPYCE_RETURNS    ["mequg"] = ["float[*,*]"]
CSPYCE_RETNAMES   ["mequg"] = ["mout"]
CSPYCE_ABSTRACT   ["mequg"] = """
Set one double precision matrix of arbitrary size equal to another.
"""
CSPYCE_DEFINITIONS["mequg"] = {
"m1": "Input matrix.",
"mout": "Output matrix equal to m1.",
}
CSPYCE_URL["mequg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mequg_c.html"

#########################################
CSPYCE_SIGNATURES ["mtxm"] = 2*["float[3,3]"]
CSPYCE_ARGNAMES   ["mtxm"] = ["m1", "m2"]
CSPYCE_RETURNS    ["mtxm"] = ["float[3,3]"]
CSPYCE_RETNAMES   ["mtxm"] = ["mout"]
CSPYCE_ABSTRACT   ["mtxm"] = """
Multiply the transpose of a 3x3 matrix and a 3x3 matrix.
"""
CSPYCE_DEFINITIONS["mtxm"] = {
"m1": "3x3 double precision matrix.",
"m2": "3x3 double precision matrix.",
"mout": "The produce m1 transpose times m2.",
}
CSPYCE_URL["mtxm"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mtxm_c.html"

#########################################
CSPYCE_SIGNATURES ["mtxmg"] = 2*["float[*,*]"]
CSPYCE_ARGNAMES   ["mtxmg"] = ["m1", "m2"]
CSPYCE_RETURNS    ["mtxmg"] = ["float[*,*]"]
CSPYCE_RETNAMES   ["mtxmg"] = ["mout"]
CSPYCE_ABSTRACT   ["mtxmg"] = """
Multiply the transpose of a matrix with another matrix, both of
arbitrary size. (The dimensions of the matrices must be compatible with
this multiplication.)
"""
CSPYCE_DEFINITIONS["mtxmg"] = {
"m1": "nr1r2 X ncol1 double precision matrix.",
"m2": "nr1r2 X ncol2 double precision matrix.",
"mout": "Transpose of m1 times m2.",
}
CSPYCE_URL["mtxmg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mtxmg_c.html"

#########################################
CSPYCE_SIGNATURES ["mtxv"] = ["float[3,3]", "float[3]"]
CSPYCE_ARGNAMES   ["mtxv"] = ["m1", "vin"]
CSPYCE_RETURNS    ["mtxv"] = ["float[3]"]
CSPYCE_RETNAMES   ["mtxv"] = ["vout"]
CSPYCE_ABSTRACT   ["mtxv"] = """
Multiply the transpose of a 3x3 matrix on the left with a vector on the
right.
"""
CSPYCE_DEFINITIONS["mtxv"] = {
"m1": "3x3 double precision matrix.",
"vin": "3-dimensional double precision vector.",
"vout": "the product m1**t * vin.",
}
CSPYCE_URL["mtxv"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mtxv_c.html"

#########################################
CSPYCE_SIGNATURES ["mtxvg"] = ["float[*,*]", "float[*]"]
CSPYCE_ARGNAMES   ["mtxvg"] = ["m1", "v2"]
CSPYCE_RETURNS    ["mtxvg"] = ["float[*]"]
CSPYCE_RETNAMES   ["mtxvg"] = ["vout"]
CSPYCE_ABSTRACT   ["mtxvg"] = """
Multiply the transpose of a matrix and a vector of arbitrary size.
"""
CSPYCE_DEFINITIONS["mtxvg"] = {
"m1": "Left-hand matrix to be multiplied.",
"v2": "Right-hand vector to be multiplied.",
"vout": "Product vector m1 transpose * v2.",
}
CSPYCE_URL["mtxvg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mtxvg_c.html"

#########################################
CSPYCE_SIGNATURES ["mxm"] = ["float[3,3]", "float[3,3]"]
CSPYCE_ARGNAMES   ["mxm"] = ["m1", "m2"]
CSPYCE_RETURNS    ["mxm"] = ["float[3,3]"]
CSPYCE_RETNAMES   ["mxm"] = ["mout"]
CSPYCE_ABSTRACT   ["mxm"] = """
Multiply two 3x3 matrices.
"""
CSPYCE_DEFINITIONS["mxm"] = {
"m1": "3x3 double precision matrix.",
"m2": "3x3 double precision matrix.",
"mout": "the product m1*m2.",
}
CSPYCE_URL["mxm"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mxm_c.html"

#########################################
CSPYCE_SIGNATURES ["mxmg"] = ["float[*,*]", "float[*,*]"]
CSPYCE_ARGNAMES   ["mxmg"] = ["m1", "m2"]
CSPYCE_RETURNS    ["mxmg"] = ["float[*,*]"]
CSPYCE_RETNAMES   ["mxmg"] = ["mout"]
CSPYCE_ABSTRACT   ["mxmg"] = """
Multiply two double precision matrices of arbitrary size.
"""
CSPYCE_DEFINITIONS["mxmg"] = {
"m1": "nrow1 X ncol1 double precision matrix.",
"m2": "ncol1 X ncol2 double precision matrix.",
"mout": "nrow1 X ncol2 double precision matrix.",
}
CSPYCE_URL["mxmg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mxmg_c.html"

#########################################
CSPYCE_SIGNATURES ["mxmt"] = ["float[3,3]", "float[3,3]"]
CSPYCE_ARGNAMES   ["mxmt"] = ["m1", "m2"]
CSPYCE_RETURNS    ["mxmt"] = ["float[3,3]"]
CSPYCE_RETNAMES   ["mxmt"] = ["mout"]
CSPYCE_ABSTRACT   ["mxmt"] = """
Multiply a 3x3 matrix and the transpose of another 3x3 matrix.
"""
CSPYCE_DEFINITIONS["mxmt"] = {
"m1": "3x3 double precision matrix.",
"m2": "3x3 double precision matrix.",
"mout": "The product m1 times m2 transpose .",
}
CSPYCE_URL["mxmt"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mxmt_c.html"

#########################################
CSPYCE_SIGNATURES ["mxmtg"] = ["float[*,*]", "float[*]"]
CSPYCE_ARGNAMES   ["mxmtg"] = ["m1", "m2"]
CSPYCE_RETURNS    ["mxmtg"] = ["float[*]"]
CSPYCE_RETNAMES   ["mxmtg"] = ["mout"]
CSPYCE_ABSTRACT   ["mxmtg"] = """
Multiply a matrix and the transpose of a matrix, both of arbitrary size.
"""
CSPYCE_DEFINITIONS["mxmtg"] = {
"m1": "Left-hand matrix to be multiplied.",
"m2": "Right-hand matrix whose transpose is to be multiplied",
"mout": "Product matrix.",
}
CSPYCE_URL["mxmtg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mxmtg_c.html"

#########################################
CSPYCE_SIGNATURES ["mxv"] = ["float[3,3]", "float[3]"]
CSPYCE_ARGNAMES   ["mxv"] = ["m1", "vin"]
CSPYCE_RETURNS    ["mxv"] = ["float[3]"]
CSPYCE_RETNAMES   ["mxv"] = ["vout"]
CSPYCE_ABSTRACT   ["mxv"] = """
Multiply a 3x3 double precision matrix with a 3-dimensional double
precision vector.
"""
CSPYCE_DEFINITIONS["mxv"] = {
"m1": "3x3 double precision matrix.",
"vin": "3-dimensional double precision vector.",
"vout": "3-dimensinoal double precision vector. vout is the product m1*vin.",
}
CSPYCE_URL["mxv"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mxv_c.html"

#########################################
CSPYCE_SIGNATURES ["mxvg"] = ["float[*,*]", "float[*]"]
CSPYCE_ARGNAMES   ["mxvg"] = ["m1", "v2"]
CSPYCE_RETURNS    ["mxvg"] = ["float[*]"]
CSPYCE_RETNAMES   ["mxvg"] = ["vout"]
CSPYCE_ABSTRACT   ["mxvg"] = """
Multiply a matrix and a vector of arbitrary size.
"""
CSPYCE_DEFINITIONS["mxvg"] = {
"m1": "Left-hand matrix to be multiplied.",
"v2": "Right-hand vector to be multiplied.",
"vout": "Product vector m1*v2.",
}
CSPYCE_URL["mxvg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mxvg_c.html"

#########################################
CSPYCE_SIGNATURES ["namfrm"] = ["frame_name"]
CSPYCE_ARGNAMES   ["namfrm"] = ["frname"]
CSPYCE_RETURNS    ["namfrm"] = ["int"]
CSPYCE_RETNAMES   ["namfrm"] = ["frcode"]
CSPYCE_ABSTRACT   ["namfrm"] = """
Look up the frame ID code associated with a string.
"""
CSPYCE_DEFINITIONS["namfrm"] = {
"frname": "The name of some reference frame.",
"frcode": "The SPICE ID code of the frame; 0 on error.",
}
CSPYCE_URL["namfrm"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/namfrm_c.html"

CSPYCE_SIGNATURES ["namfrm_error"] = ["frame_name"]
CSPYCE_ARGNAMES   ["namfrm_error"] = ["frname"]
CSPYCE_RETURNS    ["namfrm_error"] = ["frame_code"]
CSPYCE_RETNAMES   ["namfrm_error"] = ["frcode"]
CSPYCE_ABSTRACT   ["namfrm_error"] = """
Look up the frame ID code associated with a string.
"""
CSPYCE_DEFINITIONS["namfrm_error"] = {
"frname": "The name of some reference frame.",
"frcode": "The SPICE ID code of the frame.",
}
CSPYCE_PS ["namfrm_error"] = "Raise SPICE(FRAMEIDNOTFOUND) error condition if not found."
CSPYCE_URL["namfrm_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/namfrm_c.html"

#########################################
CSPYCE_SIGNATURES ["nearpt"] = ["float[3]"] + 3*["float"]
CSPYCE_ARGNAMES   ["nearpt"] = ["positn", "a", "b", "c"]
CSPYCE_RETURNS    ["nearpt"] = ["float[3]", "float"]
CSPYCE_RETNAMES   ["nearpt"] = ["npoint", "alt"]
CSPYCE_ABSTRACT   ["nearpt"] = """
This routine locates the point on the surface of an ellipsoid that is
nearest to a specified position. It also returns the altitude of the
position above the ellipsoid.
"""
CSPYCE_DEFINITIONS["nearpt"] = {
"positn": "Position of a point in bodyfixed frame.",
"a": "Length of semi-axis parallel to x-axis.",
"b": "Length of semi-axis parallel to y-axis.",
"c": "Length on semi-axis parallel to z-axis.",
"npoint": "Point on the ellipsoid closest to positn.",
"alt": "Altitude of positn above the ellipsoid.",
}
CSPYCE_URL["nearpt"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/nearpt_c.html"

#########################################
CSPYCE_SIGNATURES ["npedln"] = 3*["float"] + 2*["float[3]"]
CSPYCE_ARGNAMES   ["npedln"] = ["a", "b", "c", "linept", "linedr"]
CSPYCE_RETURNS    ["npedln"] = ["float[3]", "float"]
CSPYCE_RETNAMES   ["npedln"] = ["pnear", "dist"]
CSPYCE_ABSTRACT   ["npedln"] = """
Find nearest point on a triaxial ellipsoid to a specified line, and the
distance from the ellipsoid to the line.
"""
CSPYCE_DEFINITIONS["npedln"] = {
"a": "Length of ellipsoid's semi-axis in the x direction",
"b": "Length of ellipsoid's semi-axis in the y direction",
"c": "Length of ellipsoid's semi-axis in the z direction",
"linept": "Point on line",
"linedr": "Direction vector of line",
"pnear": "Nearest point on ellipsoid to line",
"dist": "Distance of ellipsoid from line",
}
CSPYCE_URL["npedln"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/npedln_c.html"

#########################################
CSPYCE_SIGNATURES ["npelpt"] = ["float[3]", "float[9]"]
CSPYCE_ARGNAMES   ["npelpt"] = ["point", "ellips"]
CSPYCE_RETURNS    ["npelpt"] = ["float[3]", "float"]
CSPYCE_RETNAMES   ["npelpt"] = ["pnear", "dist"]
CSPYCE_ABSTRACT   ["npelpt"] = """
Find the nearest point on an ellipse to a specified point, both in
three-dimensional space, and find the distance between the ellipse and
the point.
"""
CSPYCE_DEFINITIONS["npelpt"] = {
"point": "Point whose distance to an ellipse is to be found.",
"ellips": "A CSPICE ellipse.",
"pnear": "Nearest point on ellipse to input point.",
"dist": "Distance of input point to ellipse.",
}
CSPYCE_URL["npelpt"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/npelpt_c.html"

#########################################
CSPYCE_SIGNATURES ["nplnpt"] = 3*["float[3]"]
CSPYCE_ARGNAMES   ["nplnpt"] = ["linpt", "lindir", "point"]
CSPYCE_RETURNS    ["nplnpt"] = ["float[3]", "float"]
CSPYCE_RETNAMES   ["nplnpt"] = ["pnear", "dist"]
CSPYCE_ABSTRACT   ["nplnpt"] = """
Find the nearest point on a line to a specified point, and find the
distance between the two points.
"""
CSPYCE_DEFINITIONS["nplnpt"] = {
"linpt": "Point on a line.",
"lindir": "The line's direction vector.",
"point": "A second point.",
"pnear": "Nearest point on the line to point.",
"dist": "Distance between point and pnear.",
}
CSPYCE_URL["nplnpt"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/nplnpt_c.html"

#########################################
CSPYCE_SIGNATURES ["nvc2pl"] = ["float[3]", "float"]
CSPYCE_ARGNAMES   ["nvc2pl"] = ["normal", "constant"]
CSPYCE_RETURNS    ["nvc2pl"] = ["float[4]"]
CSPYCE_RETNAMES   ["nvc2pl"] = ["plane"]
CSPYCE_ABSTRACT   ["nvc2pl"] = """
Make a CSPICE plane from a normal vector and a constant.
"""
CSPYCE_DEFINITIONS["nvc2pl"] = {
"normal": "A normal vector",
"constant": "A constant defining a plane.",
"plane": "A CSPICE plane structure representing the plane.",
}
CSPYCE_URL["nvc2pl"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/nvc2pl_c.html"

#########################################
CSPYCE_SIGNATURES ["nvp2pl"] = 2*["float[3]"]
CSPYCE_ARGNAMES   ["nvp2pl"] = ["normal", "point"]
CSPYCE_RETURNS    ["nvp2pl"] = ["float[4]"]
CSPYCE_RETNAMES   ["nvp2pl"] = ["plane"]
CSPYCE_ABSTRACT   ["nvp2pl"] = """
Make a CSPICE plane from a normal vector and a point.
"""
CSPYCE_DEFINITIONS["nvp2pl"] = {
"normal": "A normal vector",
"point": "A point defining a plane.",
"plane": "A CSPICE plane structure representing the plane.",
}
CSPYCE_URL["nvp2pl"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/nvp2pl_c.html"

#########################################
CSPYCE_SIGNATURES ["occult"] = 2*["body_name", "string", "frame_name"] + ["string", "body_name", "time"]
CSPYCE_ARGNAMES   ["occult"] = ["targ1", "shape1", "frame1","targ2", "shape2", "frame2","abcorr", "obsrvr", "et"]
CSPYCE_RETURNS    ["occult"] = ["int"]
CSPYCE_RETNAMES   ["occult"] = ["ocltid"]
CSPYCE_ABSTRACT   ["occult"] = """
Determines the occultation condition (not occulted, partially, etc.) of
one target relative to another target as seen by an observer at a given
time.

The surfaces of the target bodies may be represented by triaxial
ellipsoids or by topographic data provided by DSK files.
"""
CSPYCE_DEFINITIONS["occult"] = {
"targ1": "Name or ID of first target.",
"shape1": "Type of shape model used for first target.",
"frame1": "Body-fixed, body-centered frame for first body.",
"targ2": "Name or ID of second target.",
"shape2": "Type of shape model used for second target.",
"frame2": "Body-fixed, body-centered frame for second body.",
"abcorr": "Aberration correction, \"NONE\", \"LT\", \"LT+S\", \"CN\", or \"CN+S\".",
"obsrvr": "Name or ID of the observer.",
"et": "Time of the observation (seconds past J2000).",
"ocltid": "Occultation identification code.",
}
CSPYCE_URL["occult"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/occult_c.html"

#########################################
CSPYCE_SIGNATURES ["oscelt"] = ["float[6]", "time", "float"]
CSPYCE_ARGNAMES   ["oscelt"] = ["state", "et", "gm"]
CSPYCE_RETURNS    ["oscelt"] = ["float[8]"]
CSPYCE_RETNAMES   ["oscelt"] = ["elts"]
CSPYCE_ABSTRACT   ["oscelt"] = """
Determine the set of osculating conic orbital elements that corresponds
to the state (position, velocity) of a body at some epoch.
"""
CSPYCE_DEFINITIONS["oscelt"] = {
"state": "State of body at epoch of elements.",
"et": "Epoch of elements.",
"gm": "Gravitational parameter (GM) of primary body.",
"elts": "Equivalent conic elements",
}
CSPYCE_URL["oscelt"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/oscelt_c.html"

#########################################
CSPYCE_SIGNATURES ["oscltx"] = ["float[6]", "time", "float"]
CSPYCE_ARGNAMES   ["oscltx"] = ["state", "et", "gm"]
CSPYCE_RETURNS    ["oscltx"] = ["float[*]"]
CSPYCE_RETNAMES   ["oscltx"] = ["elts"]
CSPYCE_ABSTRACT   ["oscltx"] = """
Determine the set of osculating conic orbital elements that corresponds
to the state (position, velocity) of a body at some epoch. In
additional to the classical elements, return the true anomaly,
semi-major axis, and period, if applicable.
"""
CSPYCE_DEFINITIONS["oscltx"] = {
"state": "State of body at epoch of elements.",
"et": "Epoch of elements.",
"gm": "Gravitational parameter (GM) of primary body.",
"elts": "Extended set of classical conic elements.",
}
CSPYCE_URL["oscltx"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/oscltx_c.html"

#########################################
CSPYCE_SIGNATURES ["pckcov"] = ["string", "frame_code"]
CSPYCE_ARGNAMES   ["pckcov"] = ["pck", "idcode"]
CSPYCE_RETURNS    ["pckcov"] = ["float[*,2]"]
CSPYCE_RETNAMES   ["pckcov"] = ["cover"]
CSPYCE_ABSTRACT   ["pckcov"] = """
Find the coverage window for a specified reference frame in a specified
binary PCK file.
"""
CSPYCE_DEFINITIONS["pckcov"] = {
"pck": "Name of PCK file.",
"idcode": "Class ID code of PCK reference frame.",
"cover": "An array of shape (n,2), where cover[:,0] are start times and cover[:,1] are stop times.",
}
CSPYCE_URL["pckcov"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pckcov_c.html"

CSPYCE_SIGNATURES ["pckcov_error"] = ["string", "frame_code"]
CSPYCE_ARGNAMES   ["pckcov_error"] = ["pck", "idcode"]
CSPYCE_RETURNS    ["pckcov_error"] = ["float[*,2]"]
CSPYCE_RETNAMES   ["pckcov_error"] = ["cover"]
CSPYCE_ABSTRACT   ["pckcov_error"] = """
Find the coverage window for a specified reference frame in a specified
binary PCK file.
"""
CSPYCE_DEFINITIONS["pckcov_error"] = {
"pck": "Name of PCK file.",
"idcode": "Class ID code of PCK reference frame.",
"cover": "An array of shape (n,2), where cover[:,0] are start times and cover[:,1] are stop times.",
}
CSPYCE_PS ["pckcov_error"] = "Raise KeyError if the idcode is not found."
CSPYCE_URL["pckcov_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pckcov_c.html"

#########################################
CSPYCE_SIGNATURES ["pckfrm"] = ["string"]
CSPYCE_ARGNAMES   ["pckfrm"] = ["pck"]
CSPYCE_RETURNS    ["pckfrm"] = ["int[*]"]
CSPYCE_RETNAMES   ["pckfrm"] = ["ids"]
CSPYCE_ABSTRACT   ["pckfrm"] = """
Find the set of reference frame class ID codes of all frames in a
specified binary PCK file.
"""
CSPYCE_DEFINITIONS["pckfrm"] = {
"pck": "Name of PCK file.",
"ids": "Set of frame ID codes of frames in PCK file.",
}
CSPYCE_URL["pckfrm"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pckfrm_c.html"

#########################################
CSPYCE_SIGNATURES ["pcpool"] = ["string", "string[*]"]
CSPYCE_ARGNAMES   ["pcpool"] = ["name", "cvals"]
CSPYCE_RETURNS    ["pcpool"] = []
CSPYCE_RETNAMES   ["pcpool"] = []
CSPYCE_ABSTRACT   ["pcpool"] = """
This entry point provides toolkit programmers a method for
programmatically inserting character data into the kernel pool.
"""
CSPYCE_DEFINITIONS["pcpool"] = {
"name": "The kernel pool name to associate with cvals.",
"cvals": "An array of strings to insert into the kernel pool.",
}
CSPYCE_URL["pcpool"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pcpool_c.html"

#########################################
CSPYCE_SIGNATURES ["pdpool"] = ["string", "float[*]"]
CSPYCE_ARGNAMES   ["pdpool"] = ["name", "dvals"]
CSPYCE_RETURNS    ["pdpool"] = []
CSPYCE_RETNAMES   ["pdpool"] = []
CSPYCE_ABSTRACT   ["pdpool"] = """
This entry point provides toolkit programmers a method for
programmatically inserting double precision data into the kernel pool.
"""
CSPYCE_DEFINITIONS["pdpool"] = {
"name": "The kernel pool name to associate with dvals.",
"dvals": "An array of values to insert into the kernel pool.",
}
CSPYCE_URL["pdpool"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pdpool_c.html"

#########################################
CSPYCE_SIGNATURES ["pgrrec"] = ["body_name"] + 5*["float"]
CSPYCE_ARGNAMES   ["pgrrec"] = ["body", "lon", "lat", "alt", "re", "f"]
CSPYCE_RETURNS    ["pgrrec"] = ["float[3]"]
CSPYCE_RETNAMES   ["pgrrec"] = ["rectan"]
CSPYCE_ABSTRACT   ["pgrrec"] = """
Convert planetographic coordinates to rectangular coordinates.
"""
CSPYCE_DEFINITIONS["pgrrec"] = {
"body": "Body with which coordinate system is associated.",
"lon": "Planetographic longitude of a point (radians).",
"lat": "Planetographic latitude of a point (radians).",
"alt": "Altitude of a point above reference spheroid.",
"re": "Equatorial radius of the reference spheroid.",
"f": "Flattening coefficient.",
"rectan": "Rectangular coordinates of the point.",
}
CSPYCE_URL["pgrrec"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pgrrec_c.html"

#########################################
CSPYCE_SIGNATURES ["phaseq"] = ["time", "body_name", "body_name", "body_name", "string"]
CSPYCE_ARGNAMES   ["phaseq"] = ["et", "target", "illmn", "obsrvr", "abcorr"]
CSPYCE_RETURNS    ["phaseq"] = ["float"]
CSPYCE_RETNAMES   ["phaseq"] = ["value"]
CSPYCE_ABSTRACT   ["phaseq"] = """
Compute the apparent phase angle for a target, observer, illuminator set
of ephemeris objects.
"""
CSPYCE_DEFINITIONS["phaseq"] = {
"et": "Ephemeris seconds past J2000 TDB.",
"target": "Target body name.",
"illmn": "Illuminating body name.",
"obsrvr": "Observer body.",
"abcorr": "Aberration correction, \"NONE\", \"LT\", \"LT+S\", \"CN\", or \"CN+S\".",
"value": "Value of phase angle.",
}
CSPYCE_URL["phaseq"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/phaseq_c.html"

#########################################
CSPYCE_SIGNATURES ["pi"] = []
CSPYCE_ARGNAMES   ["pi"] = []
CSPYCE_RETURNS    ["pi"] = ["float"]
CSPYCE_RETNAMES   ["pi"] = ["value"]
CSPYCE_ABSTRACT   ["pi"] = """
Return the value of pi.
"""
CSPYCE_DEFINITIONS["pi"] = {
"value": "value of pi",
}
CSPYCE_URL["pi"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pi_c.html"

#########################################
CSPYCE_SIGNATURES ["pipool"] = ["string", "int[*]"]
CSPYCE_ARGNAMES   ["pipool"] = ["name", "ivals"]
CSPYCE_RETURNS    ["pipool"] = []
CSPYCE_RETNAMES   ["pipool"] = []
CSPYCE_ABSTRACT   ["pipool"] = """
This entry point provides toolkit programmers a method for
programmatically inserting integer data into the kernel pool.
"""
CSPYCE_DEFINITIONS["pipool"] = {
"name": "The kernel pool name to associate with values.",
"ivals": "An array of integers to insert into the pool.",
}
CSPYCE_URL["pipool"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pipool_c.html"

#########################################
CSPYCE_SIGNATURES ["pjelpl"] = ["float[9]", "float[4]"]
CSPYCE_ARGNAMES   ["pjelpl"] = ["elin", "plane"]
CSPYCE_RETURNS    ["pjelpl"] = ["float[9]"]
CSPYCE_RETNAMES   ["pjelpl"] = ["elout"]
CSPYCE_ABSTRACT   ["pjelpl"] = """
Project an ellipse onto a plane, orthogonally.
"""
CSPYCE_DEFINITIONS["pjelpl"] = {
"elin": "A CSPICE ellipse to be projected.",
"plane": "A plane onto which elin is to be projected.",
"elout": "A CSPICE ellipse resulting from the projection.",
}
CSPYCE_URL["pjelpl"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pjelpl_c.html"

#########################################
CSPYCE_SIGNATURES ["pltar"] = ["float[*,3]", "int[*,3]"]
CSPYCE_ARGNAMES   ["pltar"] = ["vrtces", "plates"]
CSPYCE_RETURNS    ["pltar"] = ["float"]
CSPYCE_RETNAMES   ["pltar"] = ["area"]
CSPYCE_ABSTRACT   ["pltar"] = """
Compute the total area of a collection of triangular plates.
"""
CSPYCE_DEFINITIONS["pltar"] = {
"vrtces": "Array of vertices.",
"plates": "Array of plates defined by the indices of three vertices. Indices start at 1.",
"area": "total area of plates.",
}
CSPYCE_URL["pltar"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pltar_c.html"

#########################################
CSPYCE_SIGNATURES ["pltexp"] = ["float[3,3]", "float"]
CSPYCE_ARGNAMES   ["pltexp"] = ["iverts", "delta"]
CSPYCE_RETURNS    ["pltexp"] = ["float[3,3]"]
CSPYCE_RETNAMES   ["pltexp"] = ["overts"]
CSPYCE_ABSTRACT   ["pltexp"] = """
Expand a triangular plate by a specified amount. The expanded plate is
co-planar with, and has the same orientation as, the original. The
centroids of the two plates coincide.
"""
CSPYCE_DEFINITIONS["pltexp"] = {
"iverts": "Vertices of the plate to be expanded.",
"delta": "Fraction by which the plate is to be expanded.",
"overts": "Vertices of the expanded plate.",
}
CSPYCE_URL["pltexp"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pltexp_c.html"

#########################################
CSPYCE_SIGNATURES ["pltnp"] = 4*["float[3]"]
CSPYCE_ARGNAMES   ["pltnp"] = ["point", "v1", "v2", "v3"]
CSPYCE_RETURNS    ["pltnp"] = ["float[3]", "float"]
CSPYCE_RETNAMES   ["pltnp"] = ["pnear", "dist"]
CSPYCE_ABSTRACT   ["pltnp"] = """
Find the nearest point on a triangular plate to a given point.
"""
CSPYCE_DEFINITIONS["pltnp"] = {
"point": "A point in 3-dimensional space.",
"v1": "Vertex of a triangular plate.",
"v2": "Vertex of a triangular plate.",
"v3": "Vertex of a triangular plate.",
"pnear": "Nearest point on the plate to `point'.",
"dist": "Distance between `pnear' and `point'.",
}
CSPYCE_URL["pltnp"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pltnp_c.html"

#########################################
CSPYCE_SIGNATURES ["pltvol"] = ["float[*,3]", "int[*,3]"]
CSPYCE_ARGNAMES   ["pltvol"] = ["vrtces", "plates"]
CSPYCE_RETURNS    ["pltvol"] = ["float"]
CSPYCE_RETNAMES   ["pltvol"] = ["volume"]
CSPYCE_ABSTRACT   ["pltvol"] = """
Compute the volume of a three-dimensional region bounded by a collection
of triangular plates.
"""
CSPYCE_DEFINITIONS["pltvol"] = {
"vrtces": "Array of vertices.",
"plates": "Array of plates defined by the indices of three vertices. Indices start at 1.",
"volume": "the volume of the spatial region bounded by the plates.",
}
CSPYCE_URL["pltvol"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pltvol_c.html"

#########################################
CSPYCE_SIGNATURES ["pl2nvc"] = ["float[4]"]
CSPYCE_ARGNAMES   ["pl2nvc"] = ["plane"]
CSPYCE_RETURNS    ["pl2nvc"] = ["float[3]", "float"]
CSPYCE_RETNAMES   ["pl2nvc"] = ["normal", "constant"]
CSPYCE_ABSTRACT   ["pl2nvc"] = """
Return a unit normal vector and constant that define a specified plane.
"""
CSPYCE_DEFINITIONS["pl2nvc"] = {
"plane": "A CSPICE plane.",
"normal": "A normal vector defining the geometric plane.",
"constant": "A constant defining the geometric plane.",
}
CSPYCE_URL["pl2nvc"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pl2nvc_c.html"

#########################################
CSPYCE_SIGNATURES ["pl2nvp"] = ["float[4]"]
CSPYCE_ARGNAMES   ["pl2nvp"] = ["plane"]
CSPYCE_RETURNS    ["pl2nvp"] = 2*["float[3]"]
CSPYCE_RETNAMES   ["pl2nvp"] = ["normal", "point"]
CSPYCE_ABSTRACT   ["pl2nvp"] = """
Return a unit normal vector and point that define a specified plane.
"""
CSPYCE_DEFINITIONS["pl2nvp"] = {
"plane": "A CSPICE plane.",
"normal": "A unit normal vector defining the plane.",
"point": "A point that defines plane.",
}
CSPYCE_URL["pl2nvp"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pl2nvp_c.html"

#########################################
CSPYCE_SIGNATURES ["pl2psv"] = ["float[4]"]
CSPYCE_ARGNAMES   ["pl2psv"] = ["plane"]
CSPYCE_RETURNS    ["pl2psv"] = 3*["float[3]"]
CSPYCE_RETNAMES   ["pl2psv"] = ["point", "span1", "span2"]
CSPYCE_ABSTRACT   ["pl2psv"] = """
Return a point and two orthogonal spanning vectors that generate a
specified plane.
"""
CSPYCE_DEFINITIONS["pl2psv"] = {
"plane": "A CSPICE plane.",
"point": "A point in the input plane.",
"span1": "The first of two vectors spanning the input plane.",
"span2": "The second of two vectors spanning the input plane.",
}
CSPYCE_URL["pl2psv"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pl2psv_c.html"

#########################################
CSPYCE_SIGNATURES ["prop2b"] = ["float", "float[6]", "float"]
CSPYCE_ARGNAMES   ["prop2b"] = ["gm", "pvinit", "dt"]
CSPYCE_RETURNS    ["prop2b"] = ["float[6]"]
CSPYCE_RETNAMES   ["prop2b"] = ["pvprop"]
CSPYCE_ABSTRACT   ["prop2b"] = """
Given a central mass and the state of massless body at time t_0, this
routine determines the state as predicted by a two-body force model at
time t_0 + dt.
"""
CSPYCE_DEFINITIONS["prop2b"] = {
"gm": "Gravity of the central mass.",
"pvinit": "Initial state from which to propagate a state.",
"dt": "Time offset from initial state to propagate to.",
"pvprop": "The propagated state.",
}
CSPYCE_URL["prop2b"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/prop2b_c.html"

#########################################
CSPYCE_SIGNATURES ["psv2pl"] = 3*["float[3]"]
CSPYCE_ARGNAMES   ["psv2pl"] = ["point", "span1", "span2"]
CSPYCE_RETURNS    ["psv2pl"] = ["float[4]"]
CSPYCE_RETNAMES   ["psv2pl"] = ["plane"]
CSPYCE_ABSTRACT   ["psv2pl"] = """
Make a CSPICE plane from a point and two spanning vectors.
"""
CSPYCE_DEFINITIONS["psv2pl"] = {
"point": "A point in the plane.",
"span1": "The first of two vectors spanning the plane.",
"span2": "The second of two vectors spanning the plane.",
"plane": "A CSPICE plane representing the plane.",
}
CSPYCE_URL["psv2pl"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/psv2pl_c.html"

#########################################
CSPYCE_SIGNATURES ["pxform"] = ["frame_name", "frame_name", "time"]
CSPYCE_ARGNAMES   ["pxform"] = ["fromfr", "tofr", "et"]
CSPYCE_RETURNS    ["pxform"] = ["rotmat[3,3]"]
CSPYCE_RETNAMES   ["pxform"] = ["rotate"]
CSPYCE_ABSTRACT   ["pxform"] = """
Return the matrix that transforms position vectors from one specified
frame to another at a specified epoch.
"""
CSPYCE_DEFINITIONS["pxform"] = {
"fromfr": "Name of the frame to transform from.",
"tofr": "Name of the frame to transform to.",
"et": "Epoch of the rotation matrix.",
"rotate": "A rotation matrix.",
}
CSPYCE_URL["pxform"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pxform_c.html"

#########################################
CSPYCE_SIGNATURES ["pxfrm2"] = ["frame_name", "frame_name", "time", "time"]
CSPYCE_ARGNAMES   ["pxfrm2"] = ["fromfr", "tofr", "etfrom", "etto"]
CSPYCE_RETURNS    ["pxfrm2"] = ["rotmat[3,3]"]
CSPYCE_RETNAMES   ["pxfrm2"] = ["rotate"]
CSPYCE_ABSTRACT   ["pxfrm2"] = """
Return the 3x3 matrix that transforms position vectors from one
specified frame at a specified epoch to another specified frame at
another specified epoch.
"""
CSPYCE_DEFINITIONS["pxfrm2"] = {
"fromfr": "Name of the frame to transform from.",
"tofr": "Name of the frame to transform to.",
"etfrom": "Evaluation time of `from' frame.",
"etto": "Evaluation time of `to' frame.",
"rotate": "A position transformation matrix from frame `from' to frame `to'.",
}
CSPYCE_URL["pxfrm2"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pxfrm2_c.html"

#########################################
CSPYCE_SIGNATURES ["q2m"] = ["float[4]"]
CSPYCE_ARGNAMES   ["q2m"] = ["q"]
CSPYCE_RETURNS    ["q2m"] = ["rotmat[3,3]"]
CSPYCE_RETNAMES   ["q2m"] = ["r"]
CSPYCE_ABSTRACT   ["q2m"] = """
Find the rotation matrix corresponding to a specified unit quaternion.
"""
CSPYCE_DEFINITIONS["q2m"] = {
"q": "A unit quaternion.",
"r": "A rotation matrix corresponding to q.",
}
CSPYCE_URL["q2m"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/q2m_c.html"

#########################################
CSPYCE_SIGNATURES ["qcktrc"] = []
CSPYCE_ARGNAMES   ["qcktrc"] = []
CSPYCE_RETURNS    ["qcktrc"] = ["string"]
CSPYCE_RETNAMES   ["qcktrc"] = ["trace"]
CSPYCE_ABSTRACT   ["qcktrc"] = """
Return a string containing a traceback.
"""
CSPYCE_DEFINITIONS["qcktrc"] = {
"trace": "A traceback string.",
}
CSPYCE_URL["qcktrc"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/qcktrc_c.html"

#########################################
CSPYCE_SIGNATURES ["qdq2av"] = ["float[4]", "float[4]"]
CSPYCE_ARGNAMES   ["qdq2av"] = ["q", "dq"]
CSPYCE_RETURNS    ["qdq2av"] = ["float[3]"]
CSPYCE_RETNAMES   ["qdq2av"] = ["av"]
CSPYCE_ABSTRACT   ["qdq2av"] = """
Derive angular velocity from a unit quaternion and its derivative with
respect to time.
"""
CSPYCE_DEFINITIONS["qdq2av"] = {
"q" : "Unit SPICE quaternion.",
"dq": "Derivative of `q' with respect to time.",
"av": "Angular velocity defined by q and dq.",
}
CSPYCE_URL["qdq2av"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/qdq2av_c.html"

#########################################
CSPYCE_SIGNATURES ["qxq"] = ["float[4]", "float[4]"]
CSPYCE_ARGNAMES   ["qxq"] = ["q1", "q2"]
CSPYCE_RETURNS    ["qxq"] = ["float[4]"]
CSPYCE_RETNAMES   ["qxq"] = ["qout"]
CSPYCE_ABSTRACT   ["qxq"] = """
Multiply two quaternions.
"""
CSPYCE_DEFINITIONS["qxq"] = {
"q1": "First SPICE quaternion factor.",
"q2": "Second SPICE quaternion factor.",
"qout": "Product of `q1' and `q2'.",
}
CSPYCE_URL["qxq"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/qxq_c.html"

#########################################
CSPYCE_SIGNATURES ["radrec"] = 3*["float"]
CSPYCE_ARGNAMES   ["radrec"] = ["range", "ra", "dec"]
CSPYCE_RETURNS    ["radrec"] = ["float[3]"]
CSPYCE_RETNAMES   ["radrec"] = ["rectan"]
CSPYCE_ABSTRACT   ["radrec"] = """
Convert from range, right ascension, and declination to rectangular
coordinates.
"""
CSPYCE_DEFINITIONS["radrec"] = {
"range": "Distance of a point from the origin.",
"ra": "Right ascension of point in radians.",
"dec": "Declination of point in radians.",
"rectan": "Rectangular coordinates of the point.",
}
CSPYCE_URL["radrec"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/radrec_c.html"

#########################################
CSPYCE_SIGNATURES ["rav2xf"] = ["rotmat[3,3]", "float[3]"]
CSPYCE_ARGNAMES   ["rav2xf"] = ["rot", "av"]
CSPYCE_RETURNS    ["rav2xf"] = ["rotmat[6,6]"]
CSPYCE_RETNAMES   ["rav2xf"] = ["xform"]
CSPYCE_ABSTRACT   ["rav2xf"] = """
This routine determines from a state transformation matrix the
associated rotation matrix and angular velocity of the rotation.
"""
CSPYCE_DEFINITIONS["rav2xf"] = {
"rot": "Rotation matrix.",
"av": "Angular velocity vector.",
"xform": "State transformation associated with rot and av.",
}
CSPYCE_URL["rav2xf"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/rav2xf_c.html"

#########################################
CSPYCE_SIGNATURES ["raxisa"] = ["rotmat[3,3]"]
CSPYCE_ARGNAMES   ["raxisa"] = ["matrix"]
CSPYCE_RETURNS    ["raxisa"] = ["float[3]", "float"]
CSPYCE_RETNAMES   ["raxisa"] = ["axis", "angle"]
CSPYCE_ABSTRACT   ["raxisa"] = """
Compute the axis of the rotation given by an input matrix and the angle
of the rotation about that axis.
"""
CSPYCE_DEFINITIONS["raxisa"] = {
"matrix": "3x3 rotation matrix in double precision.",
"axis": "Axis of the rotation.",
"angle": "Angle through which the rotation is performed.",
}
CSPYCE_URL["raxisa"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/raxisa_c.html"

#########################################
CSPYCE_SIGNATURES ["reccyl"] = ["float[3]"]
CSPYCE_ARGNAMES   ["reccyl"] = ["rectan"]
CSPYCE_RETURNS    ["reccyl"] = 3*["float"]
CSPYCE_RETNAMES   ["reccyl"] = ["r", "lon", "z"]
CSPYCE_ABSTRACT   ["reccyl"] = """
Convert from rectangular to cylindrical coordinates.
"""
CSPYCE_DEFINITIONS["reccyl"] = {
"rectan": "Rectangular coordinates of a point.",
"r": "Distance of the point from z axis.",
"lon": "Angle (radians) of the point from xZ plane",
"z": "Height of the point above xY plane.",
}
CSPYCE_URL["reccyl"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/reccyl_c.html"

#########################################
CSPYCE_SIGNATURES ["recgeo"] = ["float[3]", "float", "float"]
CSPYCE_ARGNAMES   ["recgeo"] = ["rectan", "re", "f"]
CSPYCE_RETURNS    ["recgeo"] = 3*["float"]
CSPYCE_RETNAMES   ["recgeo"] = ["lon", "lat", "alt"]
CSPYCE_ABSTRACT   ["recgeo"] = """
Convert from rectangular coordinates to geodetic coordinates.
"""
CSPYCE_DEFINITIONS["recgeo"] = {
"rectan": "Rectangular coordinates of a point.",
"re": "Equatorial radius of the reference spheroid.",
"f": "Flattening coefficient.",
"lon": "Geodetic longitude of the point (radians).",
"lat": "Geodetic latitude  of the point (radians).",
"alt": "Altitude of the point above reference spheroid.",
}
CSPYCE_URL["recgeo"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/recgeo_c.html"

#########################################
CSPYCE_SIGNATURES ["reclat"] = ["float[3]"]
CSPYCE_ARGNAMES   ["reclat"] = ["rectan"]
CSPYCE_RETURNS    ["reclat"] = 3*["float"]
CSPYCE_RETNAMES   ["reclat"] = ["radius", "lon", "lat"]
CSPYCE_ABSTRACT   ["reclat"] = """
Convert from rectangular coordinates to latitudinal coordinates.
"""
CSPYCE_DEFINITIONS["reclat"] = {
"rectan": "Rectangular coordinates of a point.",
"radius": "Distance of the point from the origin.",
"lon": "Longitude of the point in radians.",
"lat": "Latitude of the point in radians.",
}
CSPYCE_URL["reclat"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/reclat_c.html"

#########################################
CSPYCE_SIGNATURES ["recpgr"] = ["body_name", "float[3]", "float", "float"]
CSPYCE_ARGNAMES   ["recpgr"] = ["body", "rectan", "re", "f"]
CSPYCE_RETURNS    ["recpgr"] = 3*["float"]
CSPYCE_RETNAMES   ["recpgr"] = ["lon", "lat", "alt"]
CSPYCE_ABSTRACT   ["recpgr"] = """
Convert rectangular coordinates to planetographic coordinates.
"""
CSPYCE_DEFINITIONS["recpgr"] = {
"body": "Body with which coordinate system is associated.",
"rectan": "Rectangular coordinates of a point.",
"re": "Equatorial radius of the reference spheroid.",
"f": "Flattening coefficient.",
"lon": "Planetographic longitude of the point (radians).",
"lat": "Planetographic latitude of the point (radians).",
"alt": "Altitude of the point above reference spheroid.",
}
CSPYCE_URL["recpgr"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/recpgr_c.html"

#########################################
CSPYCE_SIGNATURES ["recrad"] = ["float[3]"]
CSPYCE_ARGNAMES   ["recrad"] = ["rectan"]
CSPYCE_RETURNS    ["recrad"] = 3*["float"]
CSPYCE_RETNAMES   ["recrad"] = ["range", "ra", "dec"]
CSPYCE_ABSTRACT   ["recrad"] = """
Convert rectangular coordinates to range, right ascension, and
declination.
"""
CSPYCE_DEFINITIONS["recrad"] = {
"rectan": "Rectangular coordinates of a point.",
"range": "Distance of the point from the origin.",
"ra": "Right ascension in radians.",
"dec": "Declination in radians.",
}
CSPYCE_URL["recrad"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/recrad_c.html"

#########################################
CSPYCE_SIGNATURES ["recsph"] = ["float[3]"]
CSPYCE_ARGNAMES   ["recsph"] = ["rectan"]
CSPYCE_RETURNS    ["recsph"] = 3*["float"]
CSPYCE_RETNAMES   ["recsph"] = ["r", "colat", "lon"]
CSPYCE_ABSTRACT   ["recsph"] = """
Convert from rectangular coordinates to spherical coordinates.
"""
CSPYCE_DEFINITIONS["recsph"] = {
"rectan": "Rectangular coordinates of a point.",
"r": "Distance of the point from the origin.",
"colat": "Angle of the point from the positive Z-axis.",
"lon": "Longitude of the point in radians.",
}
CSPYCE_URL["recsph"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/recsph_c.html"

#########################################
CSPYCE_SIGNATURES ["refchg"] = ["frame_code", "frame_code", "time"]
CSPYCE_ARGNAMES   ["refchg"] = ["frame1", "frame2", "et"]
CSPYCE_RETURNS    ["refchg"] = ["rotmat[3,3]"]
CSPYCE_RETNAMES   ["refchg"] = ["rotate"]
CSPYCE_ABSTRACT   ["refchg"] = """
Return the transformation matrix from one frame to another.
"""
CSPYCE_DEFINITIONS["refchg"] = {
"frame1": "the frame id-code for some reference frame",
"frame2": "the frame id-code for some reference frame",
"et"    : "an epoch in TDB seconds past J2000.",
"rotate": "a rotation matrix.",
}
CSPYCE_URL["refchg"] = ""

#########################################
CSPYCE_SIGNATURES ["repmc"] = ["string", "string", "string"]
CSPYCE_ARGNAMES   ["repmc"] = ["instr", "marker", "value"]
CSPYCE_RETURNS    ["repmc"] = ["string"]
CSPYCE_RETNAMES   ["repmc"] = ["out"]
CSPYCE_ABSTRACT   ["repmc"] = """
Replace a marker with a character string.
"""
CSPYCE_DEFINITIONS["repmc"] = {
"instr" : "Input string.",
"marker": "Marker to be replaced.",
"value" : "Replacement value.",
"out"   : "Output string.",
}
CSPYCE_URL["repmc"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/repmc_c.html"

#########################################
CSPYCE_SIGNATURES ["repmct"] = ["string", "string", "int", "string"]
CSPYCE_ARGNAMES   ["repmct"] = ["instr", "marker", "value", "repcase"]
CSPYCE_RETURNS    ["repmct"] = ["string"]
CSPYCE_RETNAMES   ["repmct"] = ["out"]
CSPYCE_ABSTRACT   ["repmct"] = """
Replace a marker with the text representation of a cardinal number.
"""
CSPYCE_DEFINITIONS["repmct"] = {
"instr"  : "Input string.",
"marker" : "Marker to be replaced.",
"value"  : "Replacement value.",
"repcase": "Case of replacement text: \"U\" = UPPPERCASE; \"L\" = lowercase; \"C\" = Capitalized.",
"out"    : "Output string.",
}
CSPYCE_URL["repmct"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/repmct_c.html"

#########################################
CSPYCE_SIGNATURES ["repmd"] = ["string", "string", "float", "int"]
CSPYCE_ARGNAMES   ["repmd"] = ["instr", "marker", "value", "sigdig"]
CSPYCE_RETURNS    ["repmd"] = ["string"]
CSPYCE_RETNAMES   ["repmd"] = ["out"]
CSPYCE_ABSTRACT   ["repmd"] = """
Replace a marker with a double precision number.
"""
CSPYCE_DEFINITIONS["repmd"] = {
"instr": "Input string.",
"marker": "Marker to be replaced.",
"value": "Replacement value.",
"sigdig": "Significant digits in replacement text.",
"out": "Output string.",
}
CSPYCE_URL["repmd"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/repmd_c.html"

#########################################
CSPYCE_SIGNATURES ["repmf"] = ["string", "string", "float", "int", "string"]
CSPYCE_ARGNAMES   ["repmf"] = ["instr", "marker", "value", "sigdig", "format"]
CSPYCE_RETURNS    ["repmf"] = ["string"]
CSPYCE_RETNAMES   ["repmf"] = ["out"]
CSPYCE_ABSTRACT   ["repmf"] = """
Replace a marker in a string with a formatted double precision value.
"""
CSPYCE_DEFINITIONS["repmf"] = {
"instr": "Input string.",
"marker": "Marker to be replaced.",
"value": "Replacement value.",
"sigdig": "Significant digits in replacement text.",
"format": "Format: \"E\" or \"F\".",
"out": "Output string.",
}
CSPYCE_URL["repmf"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/repmf_c.html"

#########################################
CSPYCE_SIGNATURES ["repmi"] = ["string", "string", "int"]
CSPYCE_ARGNAMES   ["repmi"] = ["instr", "marker", "value"]
CSPYCE_RETURNS    ["repmi"] = ["string"]
CSPYCE_RETNAMES   ["repmi"] = ["out"]
CSPYCE_ABSTRACT   ["repmi"] = """
Replace a marker with an integer.
"""
CSPYCE_DEFINITIONS["repmi"] = {
"instr": "Input string.",
"marker": "Marker to be replaced.",
"value": "Replacement value.",
"out": "Output string.",
}
CSPYCE_URL["repmi"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/repmi_c.html"

#########################################
CSPYCE_SIGNATURES ["repmot"] = ["string", "string", "int", "string"]
CSPYCE_ARGNAMES   ["repmot"] = ["instr", "marker", "value", "repcase"]
CSPYCE_RETURNS    ["repmot"] = ["string"]
CSPYCE_RETNAMES   ["repmot"] = ["out"]
CSPYCE_ABSTRACT   ["repmot"] = """
Replace a marker with the text representation of an ordinal number.
"""
CSPYCE_DEFINITIONS["repmot"] = {
"instr": "Input string.",
"marker": "Marker to be replaced.",
"value": "Replacement value.",
"repcase": "Case of replacement text (\"U\" for UPPERCASE, \"L\" for lowercase, \"C\" for Capitalized).",
"out": "Output string.",
}
CSPYCE_URL["repmot"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/repmot_c.html"

#########################################
CSPYCE_SIGNATURES ["reset"] = []
CSPYCE_ARGNAMES   ["reset"] = []
CSPYCE_RETURNS    ["reset"] = []
CSPYCE_RETNAMES   ["reset"] = []
CSPYCE_ABSTRACT   ["reset"] = """
Reset the CSPICE error status to a value of "no error." as a result, the
status routine, failed, will return a value of False.
"""
CSPYCE_DEFINITIONS["reset"] = {}
CSPYCE_URL["reset"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/reset_c.html"

#########################################
CSPYCE_SIGNATURES ["rotate"] = ["float", "int"]
CSPYCE_ARGNAMES   ["rotate"] = ["angle", "iaxis"]
CSPYCE_RETURNS    ["rotate"] = ["rotmat[3,3]"]
CSPYCE_RETNAMES   ["rotate"] = ["mout"]
CSPYCE_ABSTRACT   ["rotate"] = """
Calculate the 3x3 rotation matrix generated by a rotation of a specified
angle about a specified axis. This rotation is thought of as rotating
the coordinate system.
"""
CSPYCE_DEFINITIONS["rotate"] = {
"angle": "Angle of rotation (radians).",
"iaxis": "Axis of rotation (X=1, Y=2, Z=3).",
"mout": "Resulting rotation matrix.",
}
CSPYCE_URL["rotate"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/rotate_c.html"

#########################################
CSPYCE_SIGNATURES ["rotmat"] = ["rotmat[3,3]", "float", "int"]
CSPYCE_ARGNAMES   ["rotmat"] = ["m1", "angle", "iaxis"]
CSPYCE_RETURNS    ["rotmat"] = ["rotmat[3,3]"]
CSPYCE_RETNAMES   ["rotmat"] = ["mout"]
CSPYCE_ABSTRACT   ["rotmat"] = """
Apply a rotation of angle radians about axis iaxis to a matrix. This
rotation is thought of as rotating the coordinate system.
"""
CSPYCE_DEFINITIONS["rotmat"] = {
"m1": "Matrix to be rotated.",
"angle": "Angle of rotation (radians).",
"iaxis": "Axis of rotation (X=1, Y=2, Z=3).",
"mout": "Resulting rotated matrix.",
}
CSPYCE_URL["rotmat"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/rotmat_c.html"

#########################################
CSPYCE_SIGNATURES ["rotvec"] = ["float[3]", "float", "int"]
CSPYCE_ARGNAMES   ["rotvec"] = ["v1", "angle", "iaxis"]
CSPYCE_RETURNS    ["rotvec"] = ["float[3]"]
CSPYCE_RETNAMES   ["rotvec"] = ["vout"]
CSPYCE_ABSTRACT   ["rotvec"] = """
Transform a vector to a new coordinate system rotated by angle radians
about axis iaxis.  This transformation rotates v1 by -angle radians
about the specified axis.
"""
CSPYCE_DEFINITIONS["rotvec"] = {
"v1": " Vector whose coordinate system is to be rotated.",
"angle": " Angle of rotation in radians.",
"iaxis": " Axis of rotation (X=1, Y=2, Z=3).",
"vout": "Resulting vector[angle]",
}
CSPYCE_URL["rotvec"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/rotvec_c.html"

#########################################
CSPYCE_SIGNATURES ["rpd"] = []
CSPYCE_ARGNAMES   ["rpd"] = []
CSPYCE_RETURNS    ["rpd"] = ["float"]
CSPYCE_RETNAMES   ["rpd"] = ["value"]
CSPYCE_ABSTRACT   ["rpd"] = """
Return the number of radians per degree.
"""
CSPYCE_DEFINITIONS["rpd"] = {
"value": "radians per degree"
}
CSPYCE_URL["rpd"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/rpd_c.html"

#########################################
CSPYCE_SIGNATURES ["rquad"] = 3*["float"]
CSPYCE_ARGNAMES   ["rquad"] = ["a", "b", "c"]
CSPYCE_RETURNS    ["rquad"] = 2*["float[2]"]
CSPYCE_RETNAMES   ["rquad"] = ["root1", "root2"]
CSPYCE_ABSTRACT   ["rquad"] = """
Find the roots of a quadratic equation.
"""
CSPYCE_DEFINITIONS["rquad"] = {
"a": "Coefficient of quadratic term.",
"b": "Coefficient of linear term.",
"c": "Constant.",
"root1": "Root built from positive discriminant term.",
"root2": "Root built from negative discriminant term.",
}
CSPYCE_URL["rquad"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/rquad_c.html"

#########################################
CSPYCE_SIGNATURES ["saelgv"] = 2*["float[3]"]
CSPYCE_ARGNAMES   ["saelgv"] = ["vec1", "vec2"]
CSPYCE_RETURNS    ["saelgv"] = 2*["float[3]"]
CSPYCE_RETNAMES   ["saelgv"] = ["smajor", "sminor"]
CSPYCE_ABSTRACT   ["saelgv"] = """
Find semi-axis vectors of an ellipse generated by two arbitrary
three-dimensional vectors.
"""
CSPYCE_DEFINITIONS["saelgv"] = {
"vec1": "The first of two vectors used to generate an ellipse.",
"vec2": "The second of two vectors used to generate an ellipse.",
"smajor": "Semi-major axis of ellipse.",
"sminor": "Semi-minor axis of ellipse.",
}
CSPYCE_URL["saelgv"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/saelgv_c.html"

#########################################
CSPYCE_SIGNATURES ["scdecd"] = ["body_code", "float"]
CSPYCE_ARGNAMES   ["scdecd"] = ["sc", "sclkdp"]
CSPYCE_RETURNS    ["scdecd"] = ["string"]
CSPYCE_RETNAMES   ["scdecd"] = ["sclkch"]
CSPYCE_ABSTRACT   ["scdecd"] = """
Convert double precision encoding of spacecraft clock time into a
character representation.
"""
CSPYCE_DEFINITIONS["scdecd"] = {
"sc": "NAIF spacecraft identification code.",
"sclkdp": "Encoded representation of a spacecraft clock count.",
"sclkch": "Character representation of a clock count.",
}
CSPYCE_URL["scdecd"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/scdecd_c.html"

#########################################
CSPYCE_SIGNATURES ["sce2c"] = ["body_code", "time"]
CSPYCE_ARGNAMES   ["sce2c"] = ["sc", "et"]
CSPYCE_RETURNS    ["sce2c"] = ["float"]
CSPYCE_RETNAMES   ["sce2c"] = ["sclkdp"]
CSPYCE_ABSTRACT   ["sce2c"] = """
Convert ephemeris seconds past j2000 (ET) to continuous encoded
spacecraft clock (`ticks').  Non-integral tick values may be returned.
"""
CSPYCE_DEFINITIONS["sce2c"] = {
"sc": "NAIF spacecraft ID code.",
"et": "Ephemeris time, seconds past j2000.",
"sclkdp": "SCLK, encoded as ticks since spacecraft clock start. sclkdp need not be integral.",
}
CSPYCE_URL["sce2c"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sce2c_c.html"

#########################################
CSPYCE_SIGNATURES ["sce2s"] = ["body_code", "time"]
CSPYCE_ARGNAMES   ["sce2s"] = ["sc", "et"]
CSPYCE_RETURNS    ["sce2s"] = ["string"]
CSPYCE_RETNAMES   ["sce2s"] = ["sclkch"]
CSPYCE_ABSTRACT   ["sce2s"] = """
Convert an epoch specified as ephemeris seconds past J2000 (ET) to a
character string representation of a spacecraft clock value (SCLK).
"""
CSPYCE_DEFINITIONS["sce2s"] = {
"sc": "NAIF spacecraft clock ID code.",
"et": "Ephemeris time, specified as seconds past J2000.",
"sclkch": "An SCLK string.",
}
CSPYCE_URL["sce2s"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sce2s_c.html"

#########################################
CSPYCE_SIGNATURES ["sce2t"] = ["body_code", "time"]
CSPYCE_ARGNAMES   ["sce2t"] = ["sc", "et"]
CSPYCE_RETURNS    ["sce2t"] = ["float"]
CSPYCE_RETNAMES   ["sce2t"] = ["sclkdp"]
CSPYCE_ABSTRACT   ["sce2t"] = """
Convert ephemeris seconds past J2000 (ET) to integral encoded spacecraft
clock (`ticks'). For conversion to fractional ticks, (required for
C-kernel production), see the routine sce2c.
"""
CSPYCE_DEFINITIONS["sce2t"] = {
"sc": "NAIF spacecraft ID code.",
"et": "Ephemeris time, seconds past J2000.",
"sclkdp": "SCLK, encoded as ticks since spacecraft clock start.",
}
CSPYCE_URL["sce2t"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sce2t_c.html"

#########################################
CSPYCE_SIGNATURES ["scencd"] = ["body_code", "string"]
CSPYCE_ARGNAMES   ["scencd"] = ["sc", "sclkch"]
CSPYCE_RETURNS    ["scencd"] = ["float"]
CSPYCE_RETNAMES   ["scencd"] = ["sclkdp"]
CSPYCE_ABSTRACT   ["scencd"] = """
Encode character representation of spacecraft clock time into a double
precision number.
"""
CSPYCE_DEFINITIONS["scencd"] = {
"sc": "NAIF spacecraft identification code.",
"sclkch": "Character representation of a spacecraft clock.",
"sclkdp": "Encoded representation of the clock count.",
}
CSPYCE_URL["scencd"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/scencd_c.html"

#########################################
CSPYCE_SIGNATURES ["scfmt"] = ["body_code", "float"]
CSPYCE_ARGNAMES   ["scfmt"] = ["sc", "ticks"]
CSPYCE_RETURNS    ["scfmt"] = ["string"]
CSPYCE_RETNAMES   ["scfmt"] = ["clkstr"]
CSPYCE_ABSTRACT   ["scfmt"] = """
Convert encoded spacecraft clock ticks to character clock format.
"""
CSPYCE_DEFINITIONS["scfmt"] = {
"sc": "NAIF spacecraft identification code.",
"ticks": "Encoded representation of a spacecraft clock count.",
"clkstr": "Character representation of a clock count.",
}
CSPYCE_URL["scfmt"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/scfmt_c.html"

#########################################
CSPYCE_SIGNATURES ["scpart"] = ["body_code"]
CSPYCE_ARGNAMES   ["scpart"] = ["sc"]
CSPYCE_RETURNS    ["scpart"] = 2*["float"]
CSPYCE_RETNAMES   ["scpart"] = ["pstart", "pstop"]
CSPYCE_ABSTRACT   ["scpart"] = """
Get spacecraft clock partition information from a spacecraft clock
kernel file.
"""
CSPYCE_DEFINITIONS["scpart"] = {
"sc": "NAIF spacecraft identification code.",
"pstart": "Array of partition start times.",
"pstop": "Array of partition stop times.",
}
CSPYCE_URL["scpart"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/scpart_c.html"

#########################################
CSPYCE_SIGNATURES ["scs2e"] = ["body_code", "string"]
CSPYCE_ARGNAMES   ["scs2e"] = ["sc", "sclkch"]
CSPYCE_RETURNS    ["scs2e"] = ["float"]
CSPYCE_RETNAMES   ["scs2e"] = ["et"]
CSPYCE_ABSTRACT   ["scs2e"] = """
Convert a spacecraft clock string to ephemeris seconds past J2000 (ET).
"""
CSPYCE_DEFINITIONS["scs2e"] = {
"sc": "NAIF integer code for a spacecraft.",
"sclkch": "An SCLK string.",
"et": "Ephemeris time, seconds past J2000.",
}
CSPYCE_URL["scs2e"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/scs2e_c.html"

#########################################
CSPYCE_SIGNATURES ["sct2e"] = ["body_code", "float"]
CSPYCE_ARGNAMES   ["sct2e"] = ["sc", "sclkdp"]
CSPYCE_RETURNS    ["sct2e"] = ["float"]
CSPYCE_RETNAMES   ["sct2e"] = ["et"]
CSPYCE_ABSTRACT   ["sct2e"] = """
Convert encoded spacecraft clock (`ticks') to ephemeris seconds past
J2000 (ET).
"""
CSPYCE_DEFINITIONS["sct2e"] = {
"sc": "NAIF spacecraft ID code.",
"sclkdp": "SCLK, encoded as ticks since spacecraft clock start.",
"et": "Ephemeris time, seconds past J2000.",
}
CSPYCE_URL["sct2e"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sct2e_c.html"

#########################################
CSPYCE_SIGNATURES ["sctiks"] = ["body_code", "string"]
CSPYCE_ARGNAMES   ["sctiks"] = ["sc", "clkstr"]
CSPYCE_RETURNS    ["sctiks"] = ["float"]
CSPYCE_RETNAMES   ["sctiks"] = ["ticks"]
CSPYCE_ABSTRACT   ["sctiks"] = """
Convert a spacecraft clock format string to number of "ticks".
"""
CSPYCE_DEFINITIONS["sctiks"] = {
"sc": "NAIF spacecraft identification code.",
"clkstr": "Character representation of a spacecraft clock.",
"ticks": "Number of ticks represented by the clock string.",
}
CSPYCE_URL["sctiks"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sctiks_c.html"

#########################################
CSPYCE_SIGNATURES ["setmsg"] = ["string"]
CSPYCE_ARGNAMES   ["setmsg"] = ["message"]
CSPYCE_RETURNS    ["setmsg"] = []
CSPYCE_RETNAMES   ["setmsg"] = []
CSPYCE_ABSTRACT   ["setmsg"] = """
Set the value of the current long error message.
"""
CSPYCE_DEFINITIONS["setmsg"] = {
"message": "A long error message.",
}
CSPYCE_URL["setmsg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/setmsg_c.html"

#########################################
CSPYCE_SIGNATURES ["sigerr"] = ["string"]
CSPYCE_ARGNAMES   ["sigerr"] = ["message"]
CSPYCE_RETURNS    ["sigerr"] = []
CSPYCE_RETNAMES   ["sigerr"] = []
CSPYCE_ABSTRACT   ["sigerr"] = """
Inform the CSPICE error processing mechanism that an error has occurred,
and specify the type of error.
"""
CSPYCE_DEFINITIONS["sigerr"] = {
"message": "A short error message.",
}
CSPYCE_URL["sigerr"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sigerr_c.html"

#########################################
CSPYCE_SIGNATURES ["sincpt"] = ["string", "body_name", "time", "frame_name", "string", "body_name", "frame_name", "float[3]"]
CSPYCE_ARGNAMES   ["sincpt"] = ["method", "target", "et", "fixref", "abcorr", "obsrvr", "dref", "dvec"]
CSPYCE_RETURNS    ["sincpt"] = ["float[3]", "time", "float[3]", "bool"]
CSPYCE_RETNAMES   ["sincpt"] = ["spoint", "trgepc", "srfvec", "found"]
CSPYCE_ABSTRACT   ["sincpt"] = """
Given an observer and a direction vector defining a ray, compute the
surface intercept of the ray on a target body at a specified epoch,
optionally corrected for light time and stellar aberration.

The surface of the target body may be represented by a triaxial
ellipsoid or by topographic data provided by DSK files.

This routine supersedes srfxpt.
"""
CSPYCE_DEFINITIONS["sincpt"] = {
"method": "Computation method.",
"target": "Name of target body.",
"et": "Epoch in TDB seconds past J2000 TDB.",
"fixref": "Body-fixed, body-centered target body frame.",
"abcorr": "Aberration correction, \"NONE\", \"LT\", \"LT+S\", \"CN\", or \"CN+S\".",
"obsrvr": "Name of observing body.",
"dref": "Reference frame of ray's direction vector.",
"dvec": "Ray's direction vector.",
"spoint": "Surface intercept point on the target body.",
"trgepc": "Intercept epoch.",
"srfvec": "Vector from observer to intercept point.",
"found": "Flag indicating whether intercept was found.",
}
CSPYCE_URL["sincpt"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sincpt_c.html"

#########################################
CSPYCE_SIGNATURES ["spd"] = []
CSPYCE_ARGNAMES   ["spd"] = []
CSPYCE_RETURNS    ["spd"] = ["float"]
CSPYCE_RETNAMES   ["spd"] = ["value"]
CSPYCE_ABSTRACT   ["spd"] = """
Return the number of seconds in a day.
"""
CSPYCE_DEFINITIONS["spd"] = {
"value": "number of seconds per day",
}
CSPYCE_URL["spd"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spd_c.html"

#########################################
CSPYCE_SIGNATURES ["sphcyl"] = 3*["float"]
CSPYCE_ARGNAMES   ["sphcyl"] = ["radius", "colat", "lon"]
CSPYCE_RETURNS    ["sphcyl"] = 3*["float"]
CSPYCE_RETNAMES   ["sphcyl"] = ["r", "lon2", "z"]
CSPYCE_ABSTRACT   ["sphcyl"] = """
This routine converts from spherical coordinates to cylindrical
coordinates.
"""
CSPYCE_DEFINITIONS["sphcyl"] = {
"radius": "Distance of point from origin.",
"colat" : "Polar angle (co-latitude in radians) of point.",
"lon"   : "Azimuthal angle (longitude) of point (radians).",
"r"     : "Distance of point from z axis.",
"lon2"  : "angle (radians) of point from XZ plane.",
"z"     : "Height of point above XY plane.",
}
CSPYCE_URL["sphcyl"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sphcyl_c.html"

#########################################
CSPYCE_SIGNATURES ["sphlat"] = 3*["float"]
CSPYCE_ARGNAMES   ["sphlat"] = ["radius", "colat", "lon"]
CSPYCE_RETURNS    ["sphlat"] = 3*["float"]
CSPYCE_RETNAMES   ["sphlat"] = ["r", "lon2", "lat"]
CSPYCE_ABSTRACT   ["sphlat"] = """
Convert from spherical coordinates to latitudinal coordinates.
"""
CSPYCE_DEFINITIONS["sphlat"] = {
"r": "Distance of the point from the origin.",
"colat": "Angle of the point from positive z axis (radians).",
"lon": "Angle of the point from the XZ plane (radians).",
"radius": "Distance of a point from the origin",
"lon2": "Angle of the point from the XZ plane in radians",
"lat": "Angle of the point from the XY plane in radians",
}
CSPYCE_URL["sphlat"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sphlat_c.html"

#########################################
CSPYCE_SIGNATURES ["sphrec"] = 3*["float"]
CSPYCE_ARGNAMES   ["sphrec"] = ["radius", "colat", "lon"]
CSPYCE_RETURNS    ["sphrec"] = ["float[3]"]
CSPYCE_RETNAMES   ["sphrec"] = ["rectan"]
CSPYCE_ABSTRACT   ["sphrec"] = """
Convert from spherical coordinates to rectangular coordinates.
"""
CSPYCE_DEFINITIONS["sphrec"] = {
"radius": "Distance of a point from the origin.",
"colat" : "Angle of the point from the positive Z-axis.",
"lon"   : "Angle of the point from the XZ plane in radians.",
"rectan": "Rectangular coordinates of the point.",
}
CSPYCE_URL["sphrec"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sphrec_c.html"

#########################################
CSPYCE_SIGNATURES ["spkacs"] = ["body_code", "time", "frame_name", "string", "body_code"]
CSPYCE_ARGNAMES   ["spkacs"] = ["targ", "et", "ref", "abcorr", "obs"]
CSPYCE_RETURNS    ["spkacs"] = ["float[6]", "float", "float"]
CSPYCE_RETNAMES   ["spkacs"] = ["starg", "lt", "dlt"]
CSPYCE_ABSTRACT   ["spkacs"] = """
Return the state (position and velocity) of a target body relative to an
observer, optionally corrected for light time and stellar aberration,
expressed relative to an inertial reference frame.
"""
CSPYCE_DEFINITIONS["spkacs"] = {
"targ": "Target body.",
"et": "Observer epoch.",
"ref": "Inertial reference frame of output state.",
"abcorr": "Aberration correction flag (\"NONE\", \"LT\", \"LT+S\", \"CN\", \"CN+S\", \"XLT\", \"XLT+S\", \"XCN\", or \"XCN+S\").",
"obs": "Observer.",
"starg": "State of target.",
"lt": "One way light time between observer and target.",
"dlt": "Derivative of light time with respect to time.",
}
CSPYCE_URL["spkacs"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkacs_c.html"

#########################################
CSPYCE_SIGNATURES ["spkapo"] = ["body_code", "time", "frame_name", "float[6]", "string"]
CSPYCE_ARGNAMES   ["spkapo"] = ["targ", "et", "ref", "sobs", "abcorr"]
CSPYCE_RETURNS    ["spkapo"] = ["float[6]", "float"]
CSPYCE_RETNAMES   ["spkapo"] = ["ptarg", "lt"]
CSPYCE_ABSTRACT   ["spkapo"] = """
Return the position of a target body relative to an observer, optionally
corrected for light time and stellar aberration.
"""
CSPYCE_DEFINITIONS["spkapo"] = {
"targ": "Target body.",
"et": "Observer epoch.",
"ref": "Inertial reference frame of observer's state.",
"sobs": "State of observer wrt. solar system barycenter.",
"abcorr": "Aberration correction flag (\"NONE\", \"LT\", \"LT+S\", \"CN\", \"CN+S\", \"XLT\", \"XLT+S\", \"XCN\", or \"XCN+S\").",
"ptarg": "Position of target.",
"lt": "One way light time between observer and target.",
}
CSPYCE_URL["spkapo"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkapo_c.html"

#########################################
CSPYCE_SIGNATURES ["spkapp"] = ["body_code", "time", "frame_name", "float[6]", "string"]
CSPYCE_ARGNAMES   ["spkapp"] = ["targ", "et", "ref", "sobs", "abcorr"]
CSPYCE_RETURNS    ["spkapp"] = ["float[6]", "float"]
CSPYCE_RETNAMES   ["spkapp"] = ["starg", "lt"]
CSPYCE_ABSTRACT   ["spkapp"] = """
Return the state (position and velocity) of a target body relative to an
observer, optionally corrected for light time and stellar aberration.

WARNING: For aberration-corrected states, the velocity is not precisely
equal to the time derivative of the position. Use spkaps instead.
"""
CSPYCE_DEFINITIONS["spkapp"] = {
"targ": "Target body.",
"et": "Observer epoch.",
"ref": "Inertial reference frame of observer's state.",
"sobs": "State of observer wrt. solar system barycenter.",
"abcorr": "Aberration correction flag (\"NONE\", \"LT\", \"LT+S\", \"CN\", \"CN+S\", \"XLT\", \"XLT+S\", \"XCN\", or \"XCN+S\").",
"starg": "State of target.",
"lt": "One way light time between observer and target.",
}
CSPYCE_URL["spkapp"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkapp_c.html"

#########################################
CSPYCE_SIGNATURES ["spkaps"] = ["body_code", "float", "frame_name", "string", "float[6]", "float[3]"]
CSPYCE_ARGNAMES   ["spkaps"] = ["targ", "et", "ref", "abcorr", "stobs", "accobs"]
CSPYCE_RETURNS    ["spkaps"] = ["float[6]", "float", "float"]
CSPYCE_RETNAMES   ["spkaps"] = ["starg", "lt", "dlt"]
CSPYCE_ABSTRACT   ["spkaps"] = """
Given the state and acceleration of an observer relative to the solar
system barycenter, return the state (position and velocity) of a target
body relative to the observer, optionally corrected for light time and
stellar aberration. All input and output vectors are expressed relative
to an inertial reference frame.

This routine supersedes spkapp.

SPICE users normally should call the high-level API routines spkezr or
spkez rather than this routine.
"""
CSPYCE_DEFINITIONS["spkaps"] = {
"targ": "Target body.",
"et": "Observer epoch.",
"ref": "Inertial reference frame of output state.",
"abcorr": "Aberration correction flag (\"NONE\", \"LT\", \"LT+S\", \"CN\", \"CN+S\", \"XLT\", \"XLT+S\", \"XCN\", or \"XCN+S\").",
"stobs": "State of the observer relative to the SSB.",
"accobs": "Acceleration of the observer relative to the SSB.",
"starg": "State of target.",
"lt": "One way light time between observer and target.",
"dlt": "Derivative of light time with respect to time.",
}
CSPYCE_URL["spkaps"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkaps_c.html"

#########################################
CSPYCE_SIGNATURES ["spkcov"] = ["string", "body_code"]
CSPYCE_ARGNAMES   ["spkcov"] = ["spk", "idcode"]
CSPYCE_RETURNS    ["spkcov"] = ["float[*,2]"]
CSPYCE_RETNAMES   ["spkcov"] = ["cover"]
CSPYCE_ABSTRACT   ["spkcov"] = """
Find the coverage window for a specified ephemeris object in a specified
SPK file.
"""
CSPYCE_DEFINITIONS["spkcov"] = {
"spk": "Name of SPK file.",
"idcode": "ID code of ephemeris object.",
"cover": "An array of shape (n,2), where cover[:,0] are start times and cover[:,1] are stop times.",
}
CSPYCE_URL["spkcov"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkcov_c.html"

CSPYCE_SIGNATURES ["spkcov_error"] = ["string", "body_code"]
CSPYCE_ARGNAMES   ["spkcov_error"] = ["spk", "idcode"]
CSPYCE_RETURNS    ["spkcov_error"] = ["float[*,2]"]
CSPYCE_RETNAMES   ["spkcov_error"] = ["cover"]
CSPYCE_ABSTRACT   ["spkcov_error"] = """
Find the coverage window for a specified ephemeris object in a specified
SPK file.
"""
CSPYCE_DEFINITIONS["spkcov_error"] = {
"spk": "Name of SPK file.",
"idcode": "ID code of ephemeris object.",
"cover": "An array of shape (n,2), where cover[:,0] are start times and cover[:,1] are stop times.",
}
CSPYCE_PS ["spkcov_error"] = "Raise KeyError if the idcode is not found."
CSPYCE_URL["spkcov_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkcov_c.html"

#########################################
CSPYCE_SIGNATURES ["spkez"] = ["body_code", "time", "frame_name", "string", "body_code"]
CSPYCE_ARGNAMES   ["spkez"] = ["targ", "et", "ref", "abcorr", "obs"]
CSPYCE_RETURNS    ["spkez"] = ["float[6]", "float"]
CSPYCE_RETNAMES   ["spkez"] = ["starg", "lt"]
CSPYCE_ABSTRACT   ["spkez"] = """
Return the state (position and velocity) of a target body relative to an
observing body, optionally corrected for light time (planetary
aberration) and stellar aberration.
"""
CSPYCE_DEFINITIONS["spkez"] = {
"targ": "Target body.",
"et": "Observer epoch.",
"ref": "Reference frame of output state vector.",
"abcorr": "Aberration correction flag (\"NONE\", \"LT\", \"LT+S\", \"CN\", \"CN+S\", \"XLT\", \"XLT+S\", \"XCN\", or \"XCN+S\").",
"obs": "Observing body.",
"starg": "State of target.",
"lt": "One way light time between observer and target.",
}
CSPYCE_URL["spkez"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkez_c.html"

#########################################
CSPYCE_SIGNATURES ["spkezp"] = ["body_code", "time", "frame_name", "string", "body_code"]
CSPYCE_ARGNAMES   ["spkezp"] = ["targ", "et", "ref", "abcorr", "obs"]
CSPYCE_RETURNS    ["spkezp"] = ["float[3]", "float"]
CSPYCE_RETNAMES   ["spkezp"] = ["ptarg", "lt"]
CSPYCE_ABSTRACT   ["spkezp"] = """
Return the position of a target body relative to an observing body,
optionally corrected for light time (planetary aberration) and stellar
aberration.
"""
CSPYCE_DEFINITIONS["spkezp"] = {
"targ": "Target body NAIF ID code.",
"et": "Observer epoch.",
"ref": "Reference frame of output position vector.",
"abcorr": "Aberration correction flag (\"NONE\", \"LT\", \"LT+S\", \"CN\", \"CN+S\", \"XLT\", \"XLT+S\", \"XCN\", or \"XCN+S\").",
"obs": "Observing body NAIF ID code.",
"ptarg": "Position of target.",
"lt": "One way light time between observer and target.",
}
CSPYCE_URL["spkezp"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkezp_c.html"

#########################################
CSPYCE_SIGNATURES ["spkezr"] = ["body_name", "time", "frame_name", "string", "body_name"]
CSPYCE_ARGNAMES   ["spkezr"] = ["target", "et", "ref", "abcorr", "obsrvr"]
CSPYCE_RETURNS    ["spkezr"] = ["float[6]", "float"]
CSPYCE_RETNAMES   ["spkezr"] = ["starg", "lt"]
CSPYCE_ABSTRACT   ["spkezr"] = """
Return the state (position and velocity) of a target body relative to an
observing body, optionally corrected for light time (planetary
aberration) and stellar aberration.
"""
CSPYCE_DEFINITIONS["spkezr"] = {
"target": "Target body name.",
"et": "Observer epoch.",
"ref": "Reference frame of output state vector.",
"abcorr": "Aberration correction flag (\"NONE\", \"LT\", \"LT+S\", \"CN\", \"CN+S\", \"XLT\", \"XLT+S\", \"XCN\", or \"XCN+S\").",
"obsrvr": "Observing body name.",
"starg": "State of target.",
"lt": "One way light time between observer and target.",
}
CSPYCE_URL["spkezr"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkezr_c.html"

#########################################
CSPYCE_SIGNATURES ["spkgeo"] = ["body_code", "time", "frame_name", "body_code"]
CSPYCE_ARGNAMES   ["spkgeo"] = ["targ", "et", "ref", "obs"]
CSPYCE_RETURNS    ["spkgeo"] = ["float[6]", "float"]
CSPYCE_RETNAMES   ["spkgeo"] = ["state", "lt"]
CSPYCE_ABSTRACT   ["spkgeo"] = """
Compute the geometric state (position and velocity) of a target body
relative to an observing body.
"""
CSPYCE_DEFINITIONS["spkgeo"] = {
"targ": "Target body code.",
"et": "Target epoch.",
"ref": "Target reference frame name.",
"obs": "Observing body code.",
"state": "State of target.",
"lt": "Light time.",
}
CSPYCE_URL["spkgeo"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkgeo_c.html"

#########################################
CSPYCE_SIGNATURES ["spkgps"] = ["body_code", "time", "frame_name", "body_code"]
CSPYCE_ARGNAMES   ["spkgps"] = ["targ", "et", "ref", "obs"]
CSPYCE_RETURNS    ["spkgps"] = ["float[3]", "float"]
CSPYCE_RETNAMES   ["spkgps"] = ["pos", "lt"]
CSPYCE_ABSTRACT   ["spkgps"] = """
Compute the geometric position of a target body relative to an observing
body.
"""
CSPYCE_DEFINITIONS["spkgps"] = {
"targ": "Target body code.",
"et": "Target epoch.",
"ref": "Target reference frame name.",
"obs": "Observing body code.",
"pos": "Position of target.",
"lt": "Light time.",
}
CSPYCE_URL["spkgps"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkgps_c.html"

#########################################
CSPYCE_SIGNATURES ["spkltc"] = ["body_code", "time", "frame_name", "string", "float[6]"]
CSPYCE_ARGNAMES   ["spkltc"] = ["targ", "et", "ref", "abcorr", "stobs"]
CSPYCE_RETURNS    ["spkltc"] = ["float[6]", "float", "float"]
CSPYCE_RETNAMES   ["spkltc"] = ["starg", "lt", "dlt"]
CSPYCE_ABSTRACT   ["spkltc"] = """
Return the state (position and velocity) of a target body relative to an
observer, optionally corrected for light time, expressed relative to an
inertial reference frame.
"""
CSPYCE_DEFINITIONS["spkltc"] = {
"targ": "Target body code.",
"et": "Observer epoch.",
"ref": "Inertial reference frame name of output state.",
"abcorr": "Aberration correction flag, \"NONE\", \"LT\", \"LT+S\", \"CN\", or \"CN+S\".",
"stobs": "State of the observer relative to the SSB.",
"starg": "State of target.",
"lt": "One way light time between observer and target.",
"dlt": "Derivative of light time with respect to time.",
}
CSPYCE_URL["spkltc"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkltc_c.html"

#########################################
CSPYCE_SIGNATURES ["spkobj"] = ["string"]
CSPYCE_ARGNAMES   ["spkobj"] = ["spk"]
CSPYCE_RETURNS    ["spkobj"] = ["int[*]"]
CSPYCE_RETNAMES   ["spkobj"] = ["ids"]
CSPYCE_ABSTRACT   ["spkobj"] = """
Find the set of ID codes of all objects in a specified SPK file.
"""
CSPYCE_DEFINITIONS["spkobj"] = {
"spk": "Name of SPK file.",
"ids": "Array of ID codes of objects in SPK file.",
}
CSPYCE_URL["spkobj"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkobj_c.html"

#########################################
CSPYCE_SIGNATURES ["spkpos"] = ["body_name", "time", "frame_name", "string", "body_name"]
CSPYCE_ARGNAMES   ["spkpos"] = ["target", "et", "ref", "abcorr", "obsrvr"]
CSPYCE_RETURNS    ["spkpos"] = ["float[3]", "float"]
CSPYCE_RETNAMES   ["spkpos"] = ["ptarg", "lt"]
CSPYCE_ABSTRACT   ["spkpos"] = """
Return the position of a target body relative to an observing body,
optionally corrected for light time (planetary aberration) and stellar
aberration.
"""
CSPYCE_DEFINITIONS["spkpos"] = {
"target": "Target body name.",
"et": "Observer epoch.",
"ref": "Reference frame of output position vector.",
"abcorr": "Aberration correction flag (\"NONE\", \"LT\", \"LT+S\", \"CN\", \"CN+S\", \"XLT\", \"XLT+S\", \"XCN\", or \"XCN+S\").",
"obsrvr": "Observing body name.",
"ptarg": "Position of target.",
"lt": "One way light time between observer and target.",
}
CSPYCE_URL["spkpos"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkpos_c.html"

#########################################
CSPYCE_SIGNATURES ["spkssb"] = ["body_code", "time", "frame_name"]
CSPYCE_ARGNAMES   ["spkssb"] = ["targ", "et", "ref"]
CSPYCE_RETURNS    ["spkssb"] = ["float[6]"]
CSPYCE_RETNAMES   ["spkssb"] = ["starg"]
CSPYCE_ABSTRACT   ["spkssb"] = """
Return the state (position and velocity) of a target body relative to
the solar system barycenter.
"""
CSPYCE_DEFINITIONS["spkssb"] = {
"targ": "Target body code.",
"et": "Target epoch.",
"ref": "Target reference frame name.",
"starg": "State of target.",
}
CSPYCE_URL["spkssb"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkssb_c.html"

#########################################
CSPYCE_SIGNATURES ["srfc2s"] = ["int", "body_code"]
CSPYCE_ARGNAMES   ["srfc2s"] = ["code", "bodyid"]
CSPYCE_RETURNS    ["srfc2s"] = ["string", "bool"]
CSPYCE_RETNAMES   ["srfc2s"] = ["srfstr", "isname"]
CSPYCE_ABSTRACT   ["srfc2s"] = """
Translate a surface ID code, together with a body ID code, to the
corresponding surface name. If no such name exists, return a string
representation of the surface ID code.
"""
CSPYCE_DEFINITIONS["srfc2s"] = {
"code"  : "Integer surface ID code to translate to a string.",
"bodyid": "ID code of body associated with surface.",
"srfstr": "String corresponding to surface ID code.",
"isname": "True to indicate output is a surface name.",
}
CSPYCE_URL["srfc2s"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/srfc2s_c.html"

CSPYCE_SIGNATURES ["srfc2s_error"] = ["int", "body_code"]
CSPYCE_ARGNAMES   ["srfc2s_error"] = ["code", "bodyid"]
CSPYCE_RETURNS    ["srfc2s_error"] = ["string"]
CSPYCE_RETNAMES   ["srfc2s_error"] = ["srfstr"]
CSPYCE_ABSTRACT   ["srfc2s_error"] = """
Translate a surface ID code, together with a body ID code, to the
corresponding surface name. If no such name exists, raise KeyError.
"""
CSPYCE_DEFINITIONS["srfc2s_error"] = {
"code"  : "Integer surface ID code to translate to a string.",
"bodyid": "ID code of body associated with surface.",
"srfstr": "String corresponding to surface ID code.",
}
CSPYCE_PS ["srfc2s_error"] = "Raise KeyError if not found."
CSPYCE_URL["srfc2s_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/srfc2s_c.html"

#########################################
CSPYCE_SIGNATURES ["srfcss"] = ["int", "body_name"]
CSPYCE_ARGNAMES   ["srfcss"] = ["code", "bodstr"]
CSPYCE_RETURNS    ["srfcss"] = ["string", "bool"]
CSPYCE_RETNAMES   ["srfcss"] = ["srfstr", "isname"]
CSPYCE_ABSTRACT   ["srfcss"] = """
Translate a surface ID code, together with a body string, to the
corresponding surface name. If no such surface name exists, return a
string representation of the surface ID code.
"""
CSPYCE_DEFINITIONS["srfcss"] = {
"code": "Integer surface ID code to translate to a string.",
"bodstr": "Name or ID of body associated with surface.",
"srfstr": "String corresponding to surface ID code.",
"isname": "Flag indicating whether output is a surface name.",
}
CSPYCE_URL["srfcss"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/srfcss_c.html"

CSPYCE_SIGNATURES ["srfcss_error"] = ["int", "body_name"]
CSPYCE_ARGNAMES   ["srfcss_error"] = ["code", "bodstr"]
CSPYCE_RETURNS    ["srfcss_error"] = ["string"]
CSPYCE_RETNAMES   ["srfcss_error"] = ["srfstr"]
CSPYCE_ABSTRACT   ["srfcss_error"] = """
Translate a surface ID code, together with a body string, to the
corresponding surface name. If no such surface name exists, an
exception.
"""
CSPYCE_DEFINITIONS["srfcss_error"] = {
"code": "Integer surface ID code to translate to a string.",
"bodstr": "Name or ID of body associated with surface.",
"srfstr": "String corresponding to surface ID code.",
}
CSPYCE_PS ["srfcss_error"] = "Raise a SPICE(NOTRANSLATION) condition if not found."
CSPYCE_URL["srfcss_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/srfcss_c.html"

#########################################
CSPYCE_SIGNATURES ["srfnrm"] = ["string", "body_name", "time", "frame_name"]
CSPYCE_ARGNAMES   ["srfnrm"] = ["method", "target", "et", "fixref"]
CSPYCE_RETURNS    ["srfnrm"] = ["float[*,3]", "float[*,3]"]
CSPYCE_RETNAMES   ["srfnrm"] = ["srfpts", "normls"]
CSPYCE_ABSTRACT   ["srfnrm"] = """
Map array of surface points on a specified target body to the
corresponding unit length outward surface normal vectors.

The surface of the target body may be represented by a triaxial
ellipsoid or by topographic data provided by DSK files.
"""
CSPYCE_DEFINITIONS["srfnrm"] = {
"method": "Computation method.",
"target": "Name of target body.",
"et": "Epoch in TDB seconds past J2000 TDB.",
"fixref": "Body-fixed, body-centered target body frame.",
"srfpts": "Array of surface points.",
"normls": "Array of outward, unit length normal vectors.",
}
CSPYCE_URL["srfnrm"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/srfnrm_c.html"

#########################################
CSPYCE_SIGNATURES ["srfrec"] = ["body_code", "float", "float"]
CSPYCE_ARGNAMES   ["srfrec"] = ["body", "lon", "lat"]
CSPYCE_RETURNS    ["srfrec"] = ["float[3]"]
CSPYCE_RETNAMES   ["srfrec"] = ["rectan"]
CSPYCE_ABSTRACT   ["srfrec"] = """
Convert planetocentric latitude and longitude of a surface point on a
specified body to rectangular coordinates.
"""
CSPYCE_DEFINITIONS["srfrec"] = {
"body": "NAIF integer code of an extended body.",
"lon": "Longitude of point in radians.",
"lat": "Latitude of point in radians.",
"rectan": "Rectangular coordinates of the point.",
}
CSPYCE_URL["srfrec"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/srfrec_c.html"

#########################################
CSPYCE_SIGNATURES ["srfs2c"] = ["string", "body_name"]
CSPYCE_ARGNAMES   ["srfs2c"] = ["srfstr", "bodstr"]
CSPYCE_RETURNS    ["srfs2c"] = ["int", "bool"]
CSPYCE_RETNAMES   ["srfs2c"] = ["code", "found"]
CSPYCE_ABSTRACT   ["srfs2c"] = """
Translate a surface string, together with a body string, to the
corresponding surface ID code. The input strings may contain names or
integer ID codes.
"""
CSPYCE_DEFINITIONS["srfs2c"] = {
"srfstr": "Surface name or ID string.",
"bodstr": "Body name or ID string.",
"code": "Integer surface ID code.",
"found": "True indicating that surface ID was found, False otherwise.",
}
CSPYCE_URL["srfs2c"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/srfs2c_c.html"

CSPYCE_SIGNATURES ["srfs2c_error"] = ["string", "body_name"]
CSPYCE_ARGNAMES   ["srfs2c_error"] = ["srfstr", "bodstr"]
CSPYCE_RETURNS    ["srfs2c_error"] = ["int"]
CSPYCE_RETNAMES   ["srfs2c_error"] = ["code"]
CSPYCE_ABSTRACT   ["srfs2c_error"] = """
Translate a surface string, together with a body string, to the
corresponding surface ID code. The input strings may contain names or
integer ID codes.
"""
CSPYCE_DEFINITIONS["srfs2c_error"] = {
"srfstr": "Surface name or ID string.",
"bodstr": "Body name or ID string.",
"code": "Integer surface ID code.",
}
CSPYCE_PS ["srfs2c_error"] = "Raise KeyError if not found."
CSPYCE_URL["srfs2c_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/srfs2c_c.html"

#########################################
CSPYCE_SIGNATURES ["srfscc"] = ["string", "body_code"]
CSPYCE_ARGNAMES   ["srfscc"] = ["srfstr", "bodyid"]
CSPYCE_RETURNS    ["srfscc"] = ["int", "bool"]
CSPYCE_RETNAMES   ["srfscc"] = ["code", "found"]
CSPYCE_ABSTRACT   ["srfscc"] = """
Translate a surface string, together with a body ID code, to the
corresponding surface ID code. The input surface string may contain a
name or an integer ID code.
"""
CSPYCE_DEFINITIONS["srfscc"] = {
"srfstr": "Surface name or ID string.",
"bodyid": "Body ID code.",
"code": "Integer surface ID code.",
"found": "True indicating that surface ID was found, False otherwise.",
}
CSPYCE_URL["srfscc"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/srfscc_c.html"

CSPYCE_SIGNATURES ["srfscc_error"] = ["string", "body_code"]
CSPYCE_ARGNAMES   ["srfscc_error"] = ["srfstr", "bodyid"]
CSPYCE_RETURNS    ["srfscc_error"] = ["int"]
CSPYCE_RETNAMES   ["srfscc_error"] = ["code"]
CSPYCE_ABSTRACT   ["srfscc_error"] = """
Translate a surface string, together with a body ID code, to the
corresponding surface ID code. The input surface string may contain a
name or an integer ID code.
"""
CSPYCE_DEFINITIONS["srfscc_error"] = {
"srfstr": "Surface name or ID string.",
"bodyid": "Body ID code.",
"code": "Integer surface ID code.",
}
CSPYCE_PS ["srfscc_error"] = "Raise KeyError if not found."
CSPYCE_URL["srfscc_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/srfscc_c.html"

#########################################
CSPYCE_SIGNATURES ["srfxpt"] = ["string", "body_name", "time", "string", "body_name", "frame_name", "float[3]"]
CSPYCE_ARGNAMES   ["srfxpt"] = ["method", "target", "et", "abcorr", "obsrvr", "dref", "dvec"]
CSPYCE_RETURNS    ["srfxpt"] = ["float[3]", "float", "float", "float[3]", "bool"]
CSPYCE_RETNAMES   ["srfxpt"] = ["spoint", "dist", "trgepc", "obspos", "found"]
CSPYCE_ABSTRACT   ["srfxpt"] = """
Given an observer and a direction vector defining a ray, compute the
surface intercept point of the ray on a target body at a specified
epoch, optionally corrected for light time and stellar aberration.
"""
CSPYCE_DEFINITIONS["srfxpt"] = {
"method": "Computation method.",
"target": "Name of target body.",
"et": "Epoch in ephemeris seconds past J2000 TDB.",
"abcorr": "Aberration correction, \"NONE\", \"LT\", \"LT+S\", \"CN\", or \"CN+S\".",
"obsrvr": "Name of observing body.",
"dref": "Reference frame of input direction vector.",
"dvec": "Ray's direction vector.",
"spoint": "Surface intercept point on the target body.",
"dist": "Distance from the observer to the intercept point.",
"trgepc": "Intercept epoch.",
"obspos": "Observer position relative to target center.",
"found": "Flag indicating whether intercept was found.",
}
CSPYCE_URL["srfxpt"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/srfxpt_c.html"

#########################################
CSPYCE_SIGNATURES ["stcf01"] = ["string"] + 4*["float"]
CSPYCE_ARGNAMES   ["stcf01"] = ["catnam", "westra", "eastra", "sthdec", "nthdec"]
CSPYCE_RETURNS    ["stcf01"] = ["int"]
CSPYCE_RETNAMES   ["stcf01"] = ["nstars"]
CSPYCE_ABSTRACT   ["stcf01"] = """
Search through a type 1 star catalog and return the number of stars
within a specified RA - DEC rectangle.
"""
CSPYCE_DEFINITIONS["stcf01"] = {
"catnam": "Catalog table name.",
"westra": "Western most right ascension in radians.",
"eastra": "Eastern most right ascension in radians.",
"sthdec": "Southern most declination in radians.",
"nthdec": "Northern most declination in radians.",
"nstars": "Number of stars found.",
}
CSPYCE_URL["stcf01"] = ""

#########################################
CSPYCE_SIGNATURES ["stcg01"] = ["int"]
CSPYCE_ARGNAMES   ["stcg01"] = ["index"]
CSPYCE_RETURNS    ["stcg01"] = 4*["float"] + ["int", "string", "float"]
CSPYCE_RETNAMES   ["stcg01"] = ["ra", "dec", "rasig", "decsig", "catnum", "sptype", "vmag"]
CSPYCE_ABSTRACT   ["stcg01"] = """
Get data for a single star from a SPICE type 1 star catalog.
"""
CSPYCE_DEFINITIONS["stcg01"] = {
"index": "Star index.",
"ra": "Right ascension in radians.",
"dec": "Declination in radians.",
"rasig": "Right ascension uncertainty in radians.",
"decsig": "Declination uncertainty in radians.",
"catnum": "Catalog number.",
"sptype": "Spectral type.",
"vmag": "Visual magnitude.",
}
CSPYCE_URL["stcg01"] = ""

#########################################
CSPYCE_SIGNATURES ["stcl01"] = ["string"]
CSPYCE_ARGNAMES   ["stcl01"] = ["catfnm"]
CSPYCE_RETURNS    ["stcl01"] = ["string", "int"]
CSPYCE_RETNAMES   ["stcl01"] = ["tabnam", "handle"]
CSPYCE_ABSTRACT   ["stcl01"] = """
Load SPICE type 1 star catalog and return the catalog's table name.
"""
CSPYCE_DEFINITIONS["stcl01"] = {
"catfnm": "Catalog file name.",
"tabnam": "Catalog table name.",
"handle": "Catalog file handle.",
}
CSPYCE_URL["stcl01"] = ""

#########################################
CSPYCE_SIGNATURES ["stelab"] = 2*["float[3]"]
CSPYCE_ARGNAMES   ["stelab"] = ["pobj", "vobs"]
CSPYCE_RETURNS    ["stelab"] = ["float[3]"]
CSPYCE_RETNAMES   ["stelab"] = ["appobj"]
CSPYCE_ABSTRACT   ["stelab"] = """
Correct the apparent position of an object for stellar aberration.
"""
CSPYCE_DEFINITIONS["stelab"] = {
"pobj": "Position of an object with respect to the observer.",
"vobs": "Velocity of the observer with respect to the Solar System barycenter.",
"appobj": "Apparent position of the object with respect to the observer, corrected for stellar aberration.",
}
CSPYCE_URL["stelab"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/stelab_c.html"

#########################################
CSPYCE_SIGNATURES ["stlabx"] = 2*["float[3]"]
CSPYCE_ARGNAMES   ["stlabx"] = ["pobj", "vobs"]
CSPYCE_RETURNS    ["stlabx"] = ["float[3]"]
CSPYCE_RETNAMES   ["stlabx"] = ["corpos"]
CSPYCE_ABSTRACT   ["stlabx"] = """
Correct the position of a target for the stellar aberration effect on
radiation transmitted from a specified observer to the target.
"""
CSPYCE_DEFINITIONS["stlabx"] = {
"pobj": "Position of an object with respect to the observer.",
"vobs": "Velocity of the observer with respect to the Solar System barycenter.",
"corpos": "Corrected position of the object.",
}
CSPYCE_URL["stlabx"] = ""

#########################################
CSPYCE_SIGNATURES ["stpool"] = ["string", "int", "string"]
CSPYCE_ARGNAMES   ["stpool"] = ["item", "nth", "contin"]
CSPYCE_RETURNS    ["stpool"] = ["string", "bool"]
CSPYCE_RETNAMES   ["stpool"] = ["string", "found"]
CSPYCE_ABSTRACT   ["stpool"] = """
Retrieve the nth string from the kernel pool variable, where the string
may be continued across several components of the kernel pool variable.
"""
CSPYCE_DEFINITIONS["stpool"] = {
"item": "Name of the kernel pool variable.",
"nth": "Index of the full string to retrieve.",
"contin": "Character sequence used to indicate continuation.",
"string": "A full string concatenated across continuations.",
"found": "True indicating success of request; False on failure.",
}
CSPYCE_URL["stpool"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/stpool_c.html"

CSPYCE_SIGNATURES ["stpool_error"] = ["string", "int", "string"]
CSPYCE_ARGNAMES   ["stpool_error"] = ["item", "nth", "contin"]
CSPYCE_RETURNS    ["stpool_error"] = ["string"]
CSPYCE_RETNAMES   ["stpool_error"] = ["string"]
CSPYCE_ABSTRACT   ["stpool_error"] = """
Retrieve the nth string from the kernel pool variable, where the string
may be continued across several components of the kernel pool variable.
"""
CSPYCE_DEFINITIONS["stpool_error"] = {
"item": "Name of the kernel pool variable.",
"nth": "Index of the full string to retrieve.",
"contin": "Character sequence used to indicate continuation.",
"string": "A full string concatenated across continuations.",
}
CSPYCE_PS ["stpool_error"] = "Raise KeyError if request failed."
CSPYCE_URL["stpool_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/stpool_c.html"

#########################################
CSPYCE_SIGNATURES ["str2et"] = ["string"]
CSPYCE_ARGNAMES   ["str2et"] = ["str"]
CSPYCE_RETURNS    ["str2et"] = ["float"]
CSPYCE_RETNAMES   ["str2et"] = ["et"]
CSPYCE_ABSTRACT   ["str2et"] = """
Convert a string representing an epoch to a double precision value
representing the number of TDB seconds past the J2000 epoch
corresponding to the input epoch.
"""
CSPYCE_DEFINITIONS["str2et"] = {
"str": "A string representing an epoch.",
"et": "The equivalent value in seconds past J2000, TDB.",
}
CSPYCE_URL["str2et"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/str2et_c.html"

#########################################
CSPYCE_SIGNATURES ["subpnt"] = ["string", "body_name", "time", "frame_name", "string", "body_name"]
CSPYCE_ARGNAMES   ["subpnt"] = ["method", "target", "et", "fixref", "abcorr", "obsrvr"]
CSPYCE_RETURNS    ["subpnt"] = ["float[3]", "time", "float[3]"]
CSPYCE_RETNAMES   ["subpnt"] = ["spoint", "trgepc", "srfvec"]
CSPYCE_ABSTRACT   ["subpnt"] = """
Compute the rectangular coordinates of the sub-observer point on a
target body at a specified epoch, optionally corrected for light time
and stellar aberration.

The surface of the target body may be represented by a triaxial
ellipsoid or by topographic data provided by DSK files.

This routine supersedes subpt.
"""
CSPYCE_DEFINITIONS["subpnt"] = {
"method": "Computation method.",
"target": "Name of target body.",
"et": "Epoch in TDB seconds past J2000 TDB.",
"fixref": "Body-fixed, body-centered target body frame.",
"abcorr": "Aberration correction, \"NONE\", \"LT\", \"LT+S\", \"CN\", or \"CN+S\".",
"obsrvr": "Name of observing body.",
"spoint": "Sub-observer point on the target body.",
"trgepc": "Sub-observer point epoch.",
"srfvec": "Vector from observer to sub-observer point.",
}
CSPYCE_URL["subpnt"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/subpnt_c.html"

#########################################
CSPYCE_SIGNATURES ["subpt"] = ["string", "body_name", "time", "string", "body_name"]
CSPYCE_ARGNAMES   ["subpt"] = ["method", "target", "et", "abcorr", "obsrvr"]
CSPYCE_RETURNS    ["subpt"] = ["float[3]", "float"]
CSPYCE_RETNAMES   ["subpt"] = ["spoint", "alt"]
CSPYCE_ABSTRACT   ["subpt"] = """
Compute the rectangular coordinates of the sub-observer point on a
target body at a particular epoch, optionally corrected for planetary
(light time) and stellar aberration.  Return these coordinates expressed
in the body-fixed frame associated with the target body.  Also, return
the observer's altitude above the target body.
"""
CSPYCE_DEFINITIONS["subpt"] = {
"method": "Computation method.",
"target": "Name of target body.",
"et": "Epoch in ephemeris seconds past J2000 TDB.",
"abcorr": "Aberration correction, \"NONE\", \"LT\", \"LT+S\", \"CN\", or \"CN+S\".",
"obsrvr": "Name of observing body.",
"spoint": "Sub-observer point on the target body.",
"alt": "Altitude of the observer above the target body.",
}
CSPYCE_URL["subpt"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/subpt_c.html"

#########################################
CSPYCE_SIGNATURES ["subslr"] = ["string", "body_name", "time", "frame_name", "string", "body_name"]
CSPYCE_ARGNAMES   ["subslr"] = ["method", "target", "et", "fixref", "abcorr", "obsrvr"]
CSPYCE_RETURNS    ["subslr"] = ["float[3]", "time", "float[3]"]
CSPYCE_RETNAMES   ["subslr"] = ["spoint", "trgepc", "srfvec"]
CSPYCE_ABSTRACT   ["subslr"] = """
Compute the rectangular coordinates of the sub-solar point on a target
body at a specified epoch, optionally corrected for light time and
stellar aberration.

The surface of the target body may be represented by a triaxial
ellipsoid or by topographic data provided by DSK files.

This routine supersedes subsol.
"""
CSPYCE_DEFINITIONS["subslr"] = {
"method": "Computation method.",
"target": "Name of target body.",
"et": "Epoch in ephemeris seconds past J2000 TDB.",
"fixref": "Body-fixed, body-centered target body frame.",
"abcorr": "Aberration correction, \"NONE\", \"LT\", \"LT+S\", \"CN\", or \"CN+S\".",
"obsrvr": "Name of observing body.",
"spoint": "Sub-solar point on the target body.",
"trgepc": "Sub-solar point epoch.",
"srfvec": "Vector from observer to sub-solar point.",
}
CSPYCE_URL["subslr"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/subslr_c.html"

#########################################
CSPYCE_SIGNATURES ["subsol"] = ["string", "body_name", "time", "string", "body_name"]
CSPYCE_ARGNAMES   ["subsol"] = ["method", "target", "et", "abcorr", "obsrvr"]
CSPYCE_RETURNS    ["subsol"] = ["float[3]"]
CSPYCE_RETNAMES   ["subsol"] = ["spoint"]
CSPYCE_ABSTRACT   ["subsol"] = """
Determine the coordinates of the sub-solar point on a target body as
seen by a specified observer at a specified epoch, optionally corrected
for planetary (light time) and stellar aberration.
"""
CSPYCE_DEFINITIONS["subsol"] = {
"method": "Computation method.",
"target": "Name of target body.",
"et": "Epoch in ephemeris seconds past J2000 TDB.",
"abcorr": "Aberration correction, \"NONE\", \"LT\", \"LT+S\", \"CN\", or \"CN+S\".",
"obsrvr": "Name of observing body.",
"spoint": "Sub-solar point on the target body.",
}
CSPYCE_URL["subsol"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/subsol_c.html"

#########################################
CSPYCE_SIGNATURES ["surfnm"] = 3*["float"] + ["float[3]"]
CSPYCE_ARGNAMES   ["surfnm"] = ["a", "b", "c", "point"]
CSPYCE_RETURNS    ["surfnm"] = ["float[3]"]
CSPYCE_RETNAMES   ["surfnm"] = ["normal"]
CSPYCE_ABSTRACT   ["surfnm"] = """
This routine computes the outward-pointing, unit normal vector from a
point on the surface of an ellipsoid.
"""
CSPYCE_DEFINITIONS["surfnm"] = {
"a": "Length of the ellisoid semi-axis along the x-axis.",
"b": "Length of the ellisoid semi-axis along the y-axis.",
"c": "Length of the ellisoid semi-axis along the z-axis.",
"point": "Body-fixed coordinates of a point on the ellipsoid",
"normal": "Outward pointing unit normal to ellipsoid at point",
}
CSPYCE_URL["surfnm"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/surfnm_c.html"

#########################################
CSPYCE_SIGNATURES ["surfpt"] = 2*["float[3]"] + 3*["float"]
CSPYCE_ARGNAMES   ["surfpt"] = ["positn", "u", "a", "b", "c"]
CSPYCE_RETURNS    ["surfpt"] = ["float[3]", "bool"]
CSPYCE_RETNAMES   ["surfpt"] = ["point", "found"]
CSPYCE_ABSTRACT   ["surfpt"] = """
Determine the intersection of a line-of-sight vector with the surface of
an ellipsoid.
"""
CSPYCE_DEFINITIONS["surfpt"] = {
"positn": "Position of the observer in body-fixed frame.",
"u": "Vector from the observer in some direction.",
"a": "Length of the ellipsoid semi-axis along the x-axis.",
"b": "Length of the ellipsoid semi-axis along the y-axis.",
"c": "Length of the ellipsoid semi-axis along the z-axis.",
"point": "Point on the ellipsoid pointed to by u.",
"found": "Flag indicating if u points at the ellipsoid.",
}
CSPYCE_URL["surfpt"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/surfpt_c.html"

#########################################
CSPYCE_SIGNATURES ["surfpv"] = 2*["float[6]"] + 3*["float"]
CSPYCE_ARGNAMES   ["surfpv"] = ["stvrtx", "stdir", "a", "b", "c"]
CSPYCE_RETURNS    ["surfpv"] = ["float[6]", "bool"]
CSPYCE_RETNAMES   ["surfpv"] = ["stx", "found"]
CSPYCE_ABSTRACT   ["surfpv"] = """
Find the state (position and velocity) of the surface intercept defined
by a specified ray, ray velocity, and ellipsoid.
"""
CSPYCE_DEFINITIONS["surfpv"] = {
"stvrtx": "State of ray's vertex.",
"stdir": "State of ray's direction vector.",
"a": "Length of ellipsoid semi-axis along the x-axis.",
"b": "Length of ellipsoid semi-axis along the y-axis.",
"c": "Length of ellipsoid semi-axis along the z-axis.",
"stx": "State of surface intercept.",
"found": "Flag indicating whether intercept state was found.",
}
CSPYCE_URL["surfpv"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/surfpv_c.html"

#########################################
CSPYCE_SIGNATURES ["sxform"] = ["frame_name", "frame_name", "time"]
CSPYCE_ARGNAMES   ["sxform"] = ["fromfr", "tofr", "et"]
CSPYCE_RETURNS    ["sxform"] = ["rotmat[6,6]"]
CSPYCE_RETNAMES   ["sxform"] = ["xform"]
CSPYCE_ABSTRACT   ["sxform"] = """
Return the state transformation matrix from one frame to another at a
specified epoch.
"""
CSPYCE_DEFINITIONS["sxform"] = {
"fromfr": "Name of the frame to transform from.",
"tofr": "Name of the frame to transform to.",
"et": "Epoch of the state transformation matrix.",
"xform": "A state transformation matrix.",
}
CSPYCE_URL["sxform"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sxform_c.html"

#########################################
CSPYCE_SIGNATURES ["termpt"] = ["string", "body_name", "body_name", "time", "frame_name", "string", "string", "body_name", "float[3]", "float", "int", "float", "float", "int"]
CSPYCE_ARGNAMES   ["termpt"] = ["method", "ilusrc", "target", "et", "fixref", "abcorr", "corloc", "obsrvr", "refvec", "rolstp", "ncuts", "schstp", "soltol", "maxn"]
CSPYCE_RETURNS    ["termpt"] = ["int[*]", "float[*,3]", "float[*]", "float[*,3]"]
CSPYCE_RETNAMES   ["termpt"] = ["npts", "points", "epochs", "trmvcs"]
CSPYCE_ABSTRACT   ["termpt"] = """
Find terminator points on a target body. The caller specifies
half-planes, bounded by the illumination source center-target center
vector, in which to search for terminator points.

The terminator can be either umbral or penumbral. The umbral terminator
is the boundary of the region on the target surface where no light from
the source is visible. The penumbral terminator is the boundary of the
region on the target surface where none of the light from the source is
blocked by the target itself.

The surface of the target body may be represented either by a triaxial
ellipsoid or by topographic data.
"""
CSPYCE_DEFINITIONS["termpt"] = {
"method": "Computation method.",
"ilusrc": "Illumination source.",
"target": "Name of target body.",
"et": "Epoch in ephemeris seconds past J2000 TDB.",
"fixref": "Body-fixed, body-centered target body frame.",
"abcorr": "Aberration correction.",
"corloc": "Aberration correction locus.",
"obsrvr": "Name of observing body.",
"refvec": "Reference vector for cutting half-planes.",
"rolstp": "Roll angular step for cutting half-planes.",
"ncuts": "Number of cutting planes.",
"schstp": "Angular step size for searching.",
"soltol": "Solution convergence tolerance.",
"maxn": "Maximum number of entries in output arrays.",
"npts": "Counts of terminator points corresponding to cuts.",
"points": "Terminator points.",
"epochs": "Times associated with terminator points.",
"trmvcs": "Terminator vectors emanating from the observer.",
}
CSPYCE_URL["termpt"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/termpt_c.html"

#########################################
CSPYCE_SIGNATURES ["timdef"] = ["string", "string", "string"]
CSPYCE_ARGNAMES   ["timdef"] = ["action", "item", "value"]
CSPYCE_RETURNS    ["timdef"] = ["string"]
CSPYCE_RETNAMES   ["timdef"] = ["output"]
CSPYCE_DEFAULTS   ["timdef"] = ["", ""]
CSPYCE_ABSTRACT   ["timdef"] = """
Set and retrieve the defaults associated with calendar input strings.
"""
CSPYCE_DEFINITIONS["timdef"] = {
"action": "the kind of action to take \"SET\" or \"GET\" (default \"GET\").",
"item"  : "the default item of interest (\"CALENDAR\", \"SYSTEM\", or \"ZONE\").",
"value" : "the value associated with the item on \"SET\"; ignored on \"GET\". Default is "".",
"output": "on \"GET\", the value of the requested parameter.",
}
CSPYCE_PS ["timdef"] = "As a special case, a single argument is \"CALENDAR\", \"SYSTEM\", or \"ZONE\", a \"GET\" operation is performed; if two arguments are provided and the first is \"CALENDAR\", \"SYSTEM\", or \"ZONE\", a \"SET\" operation is performed."
CSPYCE_URL["timdef"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/timdef_c.html"

#########################################
CSPYCE_SIGNATURES ["timout"] = ["time", "string"]
CSPYCE_ARGNAMES   ["timout"] = ["et", "pictur"]
CSPYCE_RETURNS    ["timout"] = ["string"]
CSPYCE_RETNAMES   ["timout"] = ["output"]
CSPYCE_ABSTRACT   ["timout"] = """
This routine converts an input epoch represented in TDB seconds past the
TDB epoch of J2000 to a character string formatted to the specifications
of a user's format picture.
"""
CSPYCE_DEFINITIONS["timout"] = {
"et": "An epoch in seconds past the ephemeris epoch J2000.",
"pictur": "A format specification for the output string.",
"output": "A string representation of the input epoch.",
}
CSPYCE_URL["timout"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/timout_c.html"

#########################################
CSPYCE_SIGNATURES ["tipbod"] = ["frame_code", "body_code", "time"]
CSPYCE_ARGNAMES   ["tipbod"] = ["ref", "body", "et"]
CSPYCE_RETURNS    ["tipbod"] = ["rotmat[3,3]"]
CSPYCE_RETNAMES   ["tipbod"] = ["tipm"]
CSPYCE_ABSTRACT   ["tipbod"] = """
Return a 3x3 matrix that transforms positions in inertial coordinates to
positions in body-equator-and-prime-meridian coordinates.
"""
CSPYCE_DEFINITIONS["tipbod"] = {
"ref": "ID of inertial reference frame to transform from.",
"body": "ID code of body.",
"et": "Epoch of transformation.",
"tipm": "Transformation (position), inertial to prime meridian.",
}
CSPYCE_URL["tipbod"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/tipbod_c.html"

#########################################
CSPYCE_SIGNATURES ["tisbod"] = ["frame_code", "body_code", "time"]
CSPYCE_ARGNAMES   ["tisbod"] = ["ref", "body", "et"]
CSPYCE_RETURNS    ["tisbod"] = ["rotmat[6,6]"]
CSPYCE_RETNAMES   ["tisbod"] = ["tsipm"]
CSPYCE_ABSTRACT   ["tisbod"] = """
Return a 6x6 matrix that transforms states in inertial coordinates to
states in body-equator-and-prime-meridian coordinates.
"""
CSPYCE_DEFINITIONS["tisbod"] = {
"ref": "ID of inertial reference frame to transform from",
"body": "ID code of body",
"et": "Epoch of transformation",
"tsipm": "Transformation (state), inertial to prime meridian",
}
CSPYCE_URL["tisbod"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/tisbod_c.html"

#########################################
CSPYCE_SIGNATURES ["tkvrsn"] = ["string"]
CSPYCE_ARGNAMES   ["tkvrsn"] = ["item"]
CSPYCE_DEFAULTS  ["tkvrsn"] = ["TOOLKIT"]
CSPYCE_RETURNS    ["tkvrsn"] = ["string"]
CSPYCE_RETNAMES   ["tkvrsn"] = ["value"]
CSPYCE_ABSTRACT   ["tkvrsn"] = """
Given an item such as the Toolkit or an entry point name, return the
latest version string.
"""
CSPYCE_DEFINITIONS["tkvrsn"] = {
"item": "Item for which a version string is desired; the default and only valid value is \"TOOLKIT\".",
"value": "A version string.",
}
CSPYCE_URL["tkvrsn"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/tkvrsn_c.html"

#########################################
CSPYCE_SIGNATURES ["tparse"] = ["string"]
CSPYCE_ARGNAMES   ["tparse"] = ["string"]
CSPYCE_RETURNS    ["tparse"] = ["float", "string"]
CSPYCE_RETNAMES   ["tparse"] = ["sp2000", "errmsg"]
CSPYCE_ABSTRACT   ["tparse"] = """
Parse a time string and return seconds past the J2000 epoch on a formal
calendar.
"""
CSPYCE_DEFINITIONS["tparse"] = {
"string": "Input time string, UTC.",
"sp2000": "Equivalent UTC seconds past J2000.",
"errmsg": "Descriptive error message.",
}
CSPYCE_URL["tparse"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/tparse_c.html"

CSPYCE_SIGNATURES ["tparse_error"] = ["string"]
CSPYCE_ARGNAMES   ["tparse_error"] = ["string"]
CSPYCE_RETURNS    ["tparse_error"] = ["float"]
CSPYCE_RETNAMES   ["tparse_error"] = ["sp2000"]
CSPYCE_ABSTRACT   ["tparse_error"] = """
Parse a time string and return seconds past the J2000 epoch on a formal
calendar.
"""
CSPYCE_DEFINITIONS["tparse_error"] = {
"string": "Input time string, UTC.",
"sp2000": "Equivalent UTC seconds past J2000.",
}
CSPYCE_PS ["tparse_error"] = "Raise ValueError on invalid input string."
CSPYCE_URL["tparse_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/tparse_c.html"

#########################################
CSPYCE_SIGNATURES ["tpictr"] = ["string"]
CSPYCE_ARGNAMES   ["tpictr"] = ["sample"]
CSPYCE_RETURNS    ["tpictr"] = ["string", "bool", "string"]
CSPYCE_RETNAMES   ["tpictr"] = ["pictr", "ok", "errmsg"]
CSPYCE_ABSTRACT   ["tpictr"] = """
Given a sample time string, create a time format picture suitable for
use by the routine timout.
"""
CSPYCE_DEFINITIONS["tpictr"] = {
"sample": "A sample time string.",
"pictr" : "A format picture that describes sample.",
"ok"    : "Flag indicating whether sample parsed successfully.",
"errmsg": "Diagnostic returned if sample cannot be parsed.",
}
CSPYCE_URL["tpictr"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/tpictr_c.html"

CSPYCE_SIGNATURES ["tpictr_error"] = ["string"]
CSPYCE_ARGNAMES   ["tpictr_error"] = ["sample"]
CSPYCE_RETURNS    ["tpictr_error"] = ["string"]
CSPYCE_RETNAMES   ["tpictr_error"] = ["pictr"]
CSPYCE_ABSTRACT   ["tpictr_error"] = """
Given a sample time string, create a time format picture suitable for
use by the routine timout.
"""
CSPYCE_DEFINITIONS["tpictr_error"] = {
"sample": "A sample time string.",
"pictr" : "A format picture that describes sample.",
}
CSPYCE_PS ["tpictr_error"] = "Raise ValueError on invalid sample string."
CSPYCE_URL["tpictr_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/tpictr_c.html"

#########################################
CSPYCE_SIGNATURES ["trace"] = ["float[3,3]"]
CSPYCE_ARGNAMES   ["trace"] = ["matrix"]
CSPYCE_RETURNS    ["trace"] = ["float"]
CSPYCE_RETNAMES   ["trace"] = ["trace"]
CSPYCE_ABSTRACT   ["trace"] = """
Return the trace of a 3x3 matrix.
"""
CSPYCE_DEFINITIONS["trace"] = {
"matrix": "3x3 matrix of double precision numbers.",
"trace": "The trace of the matrix.",
}
CSPYCE_URL["trace"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/trace_c.html"

#########################################
CSPYCE_SIGNATURES ["trcoff"] = []
CSPYCE_ARGNAMES   ["trcoff"] = []
CSPYCE_RETURNS    ["trcoff"] = []
CSPYCE_RETNAMES   ["trcoff"] = []
CSPYCE_ABSTRACT   ["trcoff"] = """
Disable tracing.
"""
CSPYCE_DEFINITIONS["trcoff"] = {}
CSPYCE_URL["trcoff"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/trcoff_c.html"

#########################################
CSPYCE_SIGNATURES ["trcdep"] = []
CSPYCE_ARGNAMES   ["trcdep"] = []
CSPYCE_RETURNS    ["trcdep"] = ["int"]
CSPYCE_RETNAMES   ["trcdep"] = ["depth"]
CSPYCE_ABSTRACT   ["trcdep"] = """
Return the number of modules in the traceback representation.
"""
CSPYCE_DEFINITIONS["trcdep"] = {
"depth": "The number of modules in the traceback.",
}
CSPYCE_URL["trcdep"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/trcdep_c.html"

#########################################
CSPYCE_SIGNATURES ["trcnam"] = ["int"]
CSPYCE_ARGNAMES   ["trcnam"] = ["index"]
CSPYCE_RETURNS    ["trcnam"] = ["string"]
CSPYCE_RETNAMES   ["trcnam"] = ["name"]
CSPYCE_ABSTRACT   ["trcnam"] = """
Return the name of the module having the specified position in the trace
representation. The first module to check in is at index 0.
"""
CSPYCE_DEFINITIONS["trcnam"] = {
"index": "The position of the requested module name.",
"name": "The name at position `index' in the traceback.",
}
CSPYCE_URL["trcnam"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/trcnam_c.html"

#########################################
CSPYCE_SIGNATURES ["tsetyr"] = ["int"]
CSPYCE_ARGNAMES   ["tsetyr"] = ["year"]
CSPYCE_RETURNS    ["tsetyr"] = []
CSPYCE_RETNAMES   ["tsetyr"] = []
CSPYCE_ABSTRACT   ["tsetyr"] = """
Set the lower bound on the 100 year range.
"""
CSPYCE_DEFINITIONS["tsetyr"] = {
"year": "Lower bound on the 100 year interval of expansion",
}
CSPYCE_URL["tsetyr"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/tsetyr_c.html"

#########################################
CSPYCE_SIGNATURES ["twopi"] = []
CSPYCE_ARGNAMES   ["twopi"] = []
CSPYCE_RETURNS    ["twopi"] = ["float"]
CSPYCE_RETNAMES   ["twopi"] = ["value"]
CSPYCE_ABSTRACT   ["twopi"] = """
Return twice the value of pi.
"""
CSPYCE_DEFINITIONS["twopi"] = {
"value": "twice the value of pi",
}
CSPYCE_URL["twopi"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/twopi_c.html"

#########################################
CSPYCE_SIGNATURES ["twovec"] = 2*["float[3]", "int"]
CSPYCE_ARGNAMES   ["twovec"] = ["axdef", "indexa", "plndef", "indexp"]
CSPYCE_RETURNS    ["twovec"] = ["rotmat[3,3]"]
CSPYCE_RETNAMES   ["twovec"] = ["mout"]
CSPYCE_ABSTRACT   ["twovec"] = """
Find the transformation to the right-handed frame having a given vector
as a specified axis and having a second given vector lying in a
specified coordinate plane.
"""
CSPYCE_DEFINITIONS["twovec"] = {
"axdef": "Vector defining a principal axis.",
"indexa": "Principal axis number of axdef (X=1, Y=2, Z=3).",
"plndef": "Vector defining (with axdef) a principal plane.",
"indexp": "Second axis number (with indexa) of principal plane.",
"mout": "Output rotation matrix.",
}
CSPYCE_URL["twovec"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/twovec_c.html"

#########################################
CSPYCE_SIGNATURES ["tyear"] = []
CSPYCE_ARGNAMES   ["tyear"] = []
CSPYCE_RETURNS    ["tyear"] = ["float"]
CSPYCE_RETNAMES   ["tyear"] = ["value"]
CSPYCE_ABSTRACT   ["tyear"] = """
Return the number of seconds in a tropical year.
"""
CSPYCE_DEFINITIONS["tyear"] = {
"value": "number of seconds in a tropical year",
}
CSPYCE_URL["tyear"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/tyear_c.html"

#########################################
CSPYCE_SIGNATURES ["ucrss"] = 2*["float[3]"]
CSPYCE_ARGNAMES   ["ucrss"] = ["v1", "v2"]
CSPYCE_RETURNS    ["ucrss"] = ["float[3]"]
CSPYCE_RETNAMES   ["ucrss"] = ["vout"]
CSPYCE_ABSTRACT   ["ucrss"] = """
Compute the normalized cross product of two 3-vectors.
"""
CSPYCE_DEFINITIONS["ucrss"] = {
"v1": "Left vector for cross product.",
"v2": "Right vector for cross product.",
"vout": "Normalized cross product (v1xv2) / |v1xv2|.",
}
CSPYCE_URL["ucrss"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ucrss_c.html"

#########################################
CSPYCE_SIGNATURES ["unitim"] = ["time", "string", "string"]
CSPYCE_ARGNAMES   ["unitim"] = ["epoch", "insys", "outsys"]
CSPYCE_RETURNS    ["unitim"] = ["float"]
CSPYCE_RETNAMES   ["unitim"] = ["value"]
CSPYCE_ABSTRACT   ["unitim"] = """
Transform time from one uniform scale to another.  The uniform time
scales are TAI, TDT, TDB, <float> et, JED, JDTDB, JDTDT.
"""
CSPYCE_DEFINITIONS["unitim"] = {
"epoch": "An epoch to be converted.",
"insys": "The time scale associated with the input epoch.",
"outsys": "The time scale associated with the function value.",
"value": "the value in outsys that is equivalent to the epoch on the insys time scale.",
}
CSPYCE_URL["unitim"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/unitim_c.html"

#########################################
CSPYCE_SIGNATURES ["unload"] = ["string"]
CSPYCE_ARGNAMES   ["unload"] = ["file"]
CSPYCE_RETURNS    ["unload"] = []
CSPYCE_RETNAMES   ["unload"] = []
CSPYCE_ABSTRACT   ["unload"] = """
Unload a SPICE kernel.
"""
CSPYCE_DEFINITIONS["unload"] = {
"file": "The name of a kernel to unload.",
}
CSPYCE_URL["unload"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/unload_c.html"

#########################################
CSPYCE_SIGNATURES ["unorm"] = ["float[3]"]
CSPYCE_ARGNAMES   ["unorm"] = ["v1"]
CSPYCE_RETURNS    ["unorm"] = ["float[3]", "float"]
CSPYCE_RETNAMES   ["unorm"] = ["vout", "vmag"]
CSPYCE_ABSTRACT   ["unorm"] = """
Normalize a double precision 3-vector and return its magnitude.
"""
CSPYCE_DEFINITIONS["unorm"] = {
"v1": "Vector to be normalized.",
"vout": "Unit vector v1 / |v1|.",
"vmag": "Magnitude of v1, i.e. |v1|.",
}
CSPYCE_PS ["unorm"] = "If v1 is the zero vector, then vout will also be zero."
CSPYCE_URL["unorm"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/unorm_c.html"

#########################################
CSPYCE_SIGNATURES ["unormg"] = ["float[*]"]
CSPYCE_ARGNAMES   ["unormg"] = ["v1"]
CSPYCE_RETURNS    ["unormg"] = ["float[*]", "float"]
CSPYCE_RETNAMES   ["unormg"] = ["vout", "vmag"]
CSPYCE_ABSTRACT   ["unormg"] = """
Normalize a double precision vector of arbitrary dimension and return
its magnitude.
"""
CSPYCE_DEFINITIONS["unormg"] = {
"v1": "Vector to be normalized.",
"vout": "Unit vector v1 / |v1|.",
"vmag": "Magnitude of v1, that is, |v1|.",
}
CSPYCE_PS ["unormg"] = "If v1 is the zero vector, then vout will also be zero."
CSPYCE_URL["unormg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/unormg_c.html"

#########################################
CSPYCE_SIGNATURES ["utc2et"] = ["string"]
CSPYCE_ARGNAMES   ["utc2et"] = ["utcstr"]
CSPYCE_RETURNS    ["utc2et"] = ["float"]
CSPYCE_RETNAMES   ["utc2et"] = ["et"]
CSPYCE_ABSTRACT   ["utc2et"] = """
Convert an input time from Calendar or Julian Date format, UTC, to
ephemeris seconds past J2000.
"""
CSPYCE_DEFINITIONS["utc2et"] = {
"utcstr": "Input time string, UTC.",
"et": "Output epoch, ephemeris seconds past J2000.",
}
CSPYCE_URL["utc2et"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/utc2et_c.html"

#########################################
CSPYCE_SIGNATURES ["vadd"] = 2*["float[3]"]
CSPYCE_ARGNAMES   ["vadd"] = ["v1", "v2"]
CSPYCE_RETURNS    ["vadd"] = ["float[3]"]
CSPYCE_RETNAMES   ["vadd"] = ["vout"]
CSPYCE_ABSTRACT   ["vadd"] = """
add two 3 dimensional vectors.
"""
CSPYCE_DEFINITIONS["vadd"] = {
"v1": "First vector to be added.",
"v2": "Second vector to be added.",
"vout": "Sum vector, v1 + v2.",
}
CSPYCE_URL["vadd"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vadd_c.html"

#########################################
CSPYCE_SIGNATURES ["vaddg"] = 2*["float[*]"]
CSPYCE_ARGNAMES   ["vaddg"] = ["v1", "v2"]
CSPYCE_RETURNS    ["vaddg"] = ["float[*]"]
CSPYCE_RETNAMES   ["vaddg"] = ["vout"]
CSPYCE_ABSTRACT   ["vaddg"] = """
add two vectors of arbitrary dimension.
"""
CSPYCE_DEFINITIONS["vaddg"] = {
"v1": "First vector to be added.",
"v2": "Second vector to be added.",
"vout": "Sum vector, v1 + v2.",
}
CSPYCE_URL["vaddg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vaddg_c.html"

#########################################
CSPYCE_SIGNATURES ["vcrss"] = 2*["float[3]"]
CSPYCE_ARGNAMES   ["vcrss"] = ["v1", "v2"]
CSPYCE_RETURNS    ["vcrss"] = ["float[3]"]
CSPYCE_RETNAMES   ["vcrss"] = ["vout"]
CSPYCE_ABSTRACT   ["vcrss"] = """
Compute the cross product of two 3-dimensional vectors.
"""
CSPYCE_DEFINITIONS["vcrss"] = {
"v1": "Left hand vector for cross product.",
"v2": "Right hand vector for cross product.",
"vout": "Cross product v1xv2.",
}
CSPYCE_URL["vcrss"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vcrss_c.html"

#########################################
CSPYCE_SIGNATURES ["vdist"] = 2*["float[3]"]
CSPYCE_ARGNAMES   ["vdist"] = ["v1", "v2"]
CSPYCE_RETURNS    ["vdist"] = ["float"]
CSPYCE_RETNAMES   ["vdist"] = ["dist"]
CSPYCE_ABSTRACT   ["vdist"] = """
Return the distance between two three-dimensional vectors.
"""
CSPYCE_DEFINITIONS["vdist"] = {
"v1": "The first of two 3-vectors.",
"v2": "The second of two 3-vectors.",
"dist": "The distance between v1 and v2.",
}
CSPYCE_URL["vdist"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vdist_c.html"

#########################################
CSPYCE_SIGNATURES ["vdistg"] = 2*["float[*]"]
CSPYCE_ARGNAMES   ["vdistg"] = ["v1", "v2"]
CSPYCE_RETURNS    ["vdistg"] = ["float"]
CSPYCE_RETNAMES   ["vdistg"] = ["dist"]
CSPYCE_ABSTRACT   ["vdistg"] = """
Return the distance between two vectors of arbitrary dimension.
"""
CSPYCE_DEFINITIONS["vdistg"] = {
"v1": "The first of two 3-vectors.",
"v2": "The second of two 3-vectors.",
"dist": "The distance between v1 and v2.",
}
CSPYCE_URL["vdistg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vdistg_c.html"

#########################################
CSPYCE_SIGNATURES ["vdot"] = 2*["float[3]"]
CSPYCE_ARGNAMES   ["vdot"] = ["v1", "v2"]
CSPYCE_RETURNS    ["vdot"] = ["float"]
CSPYCE_RETNAMES   ["vdot"] = ["value"]
CSPYCE_ABSTRACT   ["vdot"] = """
Compute the dot product of two double precision, 3-dimensional vectors.
"""
CSPYCE_DEFINITIONS["vdot"] = {
"v1": "First vector in the dot product.",
"v2": "Second vector in the dot product.",
"value": "The value of the dot product of v1 and v2.",
}
CSPYCE_URL["vdot"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vdot_c.html"

#########################################
CSPYCE_SIGNATURES ["vdotg"] = 2*["float[*]"]
CSPYCE_ARGNAMES   ["vdotg"] = ["v1", "v2"]
CSPYCE_RETURNS    ["vdotg"] = ["float"]
CSPYCE_RETNAMES   ["vdotg"] = ["value"]
CSPYCE_ABSTRACT   ["vdotg"] = """
Compute the dot product of two vectors of arbitrary dimension.
"""
CSPYCE_DEFINITIONS["vdotg"] = {
"v1": "First vector in the dot product.",
"v2": "Second vector in the dot product.",
"value": "The value of the dot product of v1 and v2.",
}
CSPYCE_URL["vdotg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vdotg_c.html"

#########################################
CSPYCE_SIGNATURES ["vequ"] = ["float[3]"]
CSPYCE_ARGNAMES   ["vequ"] = ["vin"]
CSPYCE_RETURNS    ["vequ"] = ["float[3]"]
CSPYCE_RETNAMES   ["vequ"] = ["vout"]
CSPYCE_ABSTRACT   ["vequ"] = """
Make one double precision 3-dimensional vector equal to another.
"""
CSPYCE_DEFINITIONS["vequ"] = {
"vin": "3-dimensional double precision vector.",
"vout": "3-dimensional double precision vector set equal to vin.",
}
CSPYCE_URL["vequ"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vequ_c.html"

#########################################
CSPYCE_SIGNATURES ["vequg"] = ["float[*]"]
CSPYCE_ARGNAMES   ["vequg"] = ["vin"]
CSPYCE_RETURNS    ["vequg"] = ["float[*]"]
CSPYCE_RETNAMES   ["vequg"] = ["vout"]
CSPYCE_ABSTRACT   ["vequg"] = """
Make one double precision vector of arbitrary dimension equal to
another.
"""
CSPYCE_DEFINITIONS["vequg"] = {
"vin": "double precision vector.",
"vout": "double precision vector set equal to vin.",
}
CSPYCE_URL["vequg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vequg_c.html"

#########################################
CSPYCE_SIGNATURES ["vhat"] = ["float[3]"]
CSPYCE_ARGNAMES   ["vhat"] = ["v1"]
CSPYCE_RETURNS    ["vhat"] = ["float[3]"]
CSPYCE_RETNAMES   ["vhat"] = ["vout"]
CSPYCE_ABSTRACT   ["vhat"] = """
Find the unit vector along a double precision 3-dimensional vector.
"""
CSPYCE_DEFINITIONS["vhat"] = {
"v1": "Vector to be unitized.",
"vout": "Unit vector v1 / |v1|.",
}
CSPYCE_URL["vhat"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vhat_c.html"

#########################################
CSPYCE_SIGNATURES ["vhatg"] = ["float[*]"]
CSPYCE_ARGNAMES   ["vhatg"] = ["v1"]
CSPYCE_RETURNS    ["vhatg"] = ["float[*]"]
CSPYCE_RETNAMES   ["vhatg"] = ["vout"]
CSPYCE_ABSTRACT   ["vhatg"] = """
Find the unit vector along a double precision vector of arbitrary
dimension.
"""
CSPYCE_DEFINITIONS["vhatg"] = {
"v1": "Vector to be normalized.",
"vout": "Unit vector v1 / |v1|.",
}
CSPYCE_PS ["vhatg"] = "If v1 is the zero vector, then vout will also be zero."
CSPYCE_URL["vhatg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vhatg_c.html"

#########################################
CSPYCE_SIGNATURES ["vlcom3"] = 3*["float", "float[3]"]
CSPYCE_ARGNAMES   ["vlcom3"] = ["a", "v1", "b", "v2", "c", "v3"]
CSPYCE_RETURNS    ["vlcom3"] = ["float[3]"]
CSPYCE_RETNAMES   ["vlcom3"] = ["sum"]
CSPYCE_ABSTRACT   ["vlcom3"] = """
This subroutine computes the vector linear combination
a*v1 + b*v2 + c*v3 of double precision, 3-dimensional vectors.
"""
CSPYCE_DEFINITIONS["vlcom3"] = {
"a": "Coefficient of v1",
"v1": "Vector in 3-space",
"b": "Coefficient of v2",
"v2": "Vector in 3-space",
"c": "Coefficient of v3",
"v3": "Vector in 3-space",
"sum": "Linear Vector Combination a*v1 + b*v2 + c*v3",
}
CSPYCE_URL["vlcom3"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vlcom3_c.html"

#########################################
CSPYCE_SIGNATURES ["vlcom"] = 2*["float", "float[3]"]
CSPYCE_ARGNAMES   ["vlcom"] = ["a", "v1", "b", "v2"]
CSPYCE_RETURNS    ["vlcom"] = ["float[3]"]
CSPYCE_RETNAMES   ["vlcom"] = ["sum"]
CSPYCE_ABSTRACT   ["vlcom"] = """
Compute a vector linear combination of two double precision,
3-dimensional vectors.
"""
CSPYCE_DEFINITIONS["vlcom"] = {
"a": "Coefficient of v1",
"v1": "Vector in 3-space",
"b": "Coefficient of v2",
"v2": "Vector in 3-space",
"sum": "Linear Vector Combination a*v1 + b*v2",
}
CSPYCE_URL["vlcom"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vlcom_c.html"

#########################################
CSPYCE_SIGNATURES ["vlcomg"] = 2*["float", "float[*]"]
CSPYCE_ARGNAMES   ["vlcomg"] = ["a", "v1", "b", "v2"]
CSPYCE_RETURNS    ["vlcomg"] = ["float[*]"]
CSPYCE_RETNAMES   ["vlcomg"] = ["sum"]
CSPYCE_ABSTRACT   ["vlcomg"] = """
Compute a vector linear combination of two double precision vectors of
arbitrary dimension.
"""
CSPYCE_DEFINITIONS["vlcomg"] = {
"a": "Coefficient of v1",
"v1": "Vector in n-space",
"b": "Coefficient of v2",
"v2": "Vector in n-space",
"sum": "Linear Vector Combination a*v1 + b*v2",
}
CSPYCE_URL["vlcomg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vlcomg_c.html"

#########################################
CSPYCE_SIGNATURES ["vminug"] = ["float[*]"]
CSPYCE_ARGNAMES   ["vminug"] = ["vin"]
CSPYCE_RETURNS    ["vminug"] = ["float[*]"]
CSPYCE_RETNAMES   ["vminug"] = ["vout"]
CSPYCE_ABSTRACT   ["vminug"] = """
Negate a double precision vector of arbitrary dimension.
"""
CSPYCE_DEFINITIONS["vminug"] = {
"vin": "ndim-dimensional double precision vector to be negated.",
"vout": "ndouble precision vector equal to -vin.",
}
CSPYCE_URL["vminug"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vminug_c.html"

#########################################
CSPYCE_SIGNATURES ["vminus"] = ["float[3]"]
CSPYCE_ARGNAMES   ["vminus"] = ["v1"]
CSPYCE_RETURNS    ["vminus"] = ["float[3]"]
CSPYCE_RETNAMES   ["vminus"] = ["vout"]
CSPYCE_ABSTRACT   ["vminus"] = """
Negate a double precision 3-dimensional vector.
"""
CSPYCE_DEFINITIONS["vminus"] = {
"v1": " Vector to be negated.",
"vout": "Negated vector -v1.",
}
CSPYCE_URL["vminus"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vminus_c.html"

#########################################
CSPYCE_SIGNATURES ["vnorm"] = ["float[3]"]
CSPYCE_ARGNAMES   ["vnorm"] = ["v1"]
CSPYCE_RETURNS    ["vnorm"] = ["float"]
CSPYCE_RETNAMES   ["vnorm"] = ["value"]
CSPYCE_ABSTRACT   ["vnorm"] = """
Compute the magnitude of a double precision, 3-dimensional vector.
"""
CSPYCE_DEFINITIONS["vnorm"] = {
"v1": "Vector whose magnitude is to be found.",
"value": "The norm of v1.",
}
CSPYCE_URL["vnorm"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vnorm_c.html"

#########################################
CSPYCE_SIGNATURES ["vnormg"] = ["float[*]"]
CSPYCE_ARGNAMES   ["vnormg"] = ["v1"]
CSPYCE_RETURNS    ["vnormg"] = ["float"]
CSPYCE_RETNAMES   ["vnormg"] = ["value"]
CSPYCE_ABSTRACT   ["vnormg"] = """
Compute the magnitude of a double precision vector of arbitrary
dimension.
"""
CSPYCE_DEFINITIONS["vnormg"] = {
"v1": "Vector whose magnitude is to be found.",
"value": "The norm of v1.",
}
CSPYCE_URL["vnormg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vnormg_c.html"

#########################################
CSPYCE_SIGNATURES ["vpack"] = 3*["float"]
CSPYCE_ARGNAMES   ["vpack"] = ["x", "y", "z"]
CSPYCE_RETURNS    ["vpack"] = ["float[3]"]
CSPYCE_RETNAMES   ["vpack"] = ["vout"]
CSPYCE_ABSTRACT   ["vpack"] = """
Pack three scalar components into a vector.
"""
CSPYCE_DEFINITIONS["vpack"] = {
"x": "First scalar component of a 3-vector.",
"y": "Second scalar component of a 3-vector.",
"z": "Third scalar component of a 3-vector.",
"vout": "Equivalent 3-vector.",
}
CSPYCE_URL["vpack"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vpack_c.html"

#########################################
CSPYCE_SIGNATURES ["vperp"] = 2*["float[3]"]
CSPYCE_ARGNAMES   ["vperp"] = ["v1", "v2"]
CSPYCE_RETURNS    ["vperp"] = ["float[3]"]
CSPYCE_RETNAMES   ["vperp"] = ["perp"]
CSPYCE_ABSTRACT   ["vperp"] = """
Find the component of a vector that is perpendicular to a second vector.
All vectors are 3-dimensional.
"""
CSPYCE_DEFINITIONS["vperp"] = {
"v1": "The vector whose orthogonal component is sought.",
"v2": "The vector used as the orthogonal reference.",
"perp": "The component of a orthogonal to b.",
}
CSPYCE_URL["vperp"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vperp_c.html"

#########################################
CSPYCE_SIGNATURES ["vprjp"] = ["float[3]", "float[4]"]
CSPYCE_ARGNAMES   ["vprjp"] = ["vin", "plane"]
CSPYCE_RETURNS    ["vprjp"] = ["float[3]"]
CSPYCE_RETNAMES   ["vprjp"] = ["vout"]
CSPYCE_ABSTRACT   ["vprjp"] = """
Project a vector onto a specified plane, orthogonally.
"""
CSPYCE_DEFINITIONS["vprjp"] = {
"vin": "Vector to be projected.",
"plane": "A CSPICE plane onto which vin is projected.",
"vout": "Vector resulting from projection.",
}
CSPYCE_URL["vprjp"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vprjp_c.html"

#########################################
CSPYCE_SIGNATURES ["vprjpi"] = ["float[3]", "float[4]", "float[4]"]
CSPYCE_ARGNAMES   ["vprjpi"] = ["vin", "projpl", "invpl"]
CSPYCE_RETURNS    ["vprjpi"] = ["float[3]", "bool"]
CSPYCE_RETNAMES   ["vprjpi"] = ["vout", "found"]
CSPYCE_ABSTRACT   ["vprjpi"] = """
Find the vector in a specified plane that maps to a specified vector in
another plane under orthogonal projection.
"""
CSPYCE_DEFINITIONS["vprjpi"] = {
"vin": "The projected vector.",
"projpl": "Plane containing vin.",
"invpl": "Plane containing inverse image of vin.",
"vout": "Inverse projection of vin.",
"found": "Flag indicating whether vout could be calculated.",
}
CSPYCE_URL["vprjpi"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vprjpi_c.html"

#########################################
CSPYCE_SIGNATURES ["vproj"] = ["float[3]", "float[3]"]
CSPYCE_ARGNAMES   ["vproj"] = ["v1", "v2"]
CSPYCE_RETURNS    ["vproj"] = ["float[3]"]
CSPYCE_RETNAMES   ["vproj"] = ["proj"]
CSPYCE_ABSTRACT   ["vproj"] = """
Find the projection of one vector onto another vector. All vectors are
3-dimensional.
"""
CSPYCE_DEFINITIONS["vproj"] = {
"v1": "The vector to be projected.",
"v2": "The vector onto which a is to be projected.",
"proj": "The projection of a onto b.",
}
CSPYCE_URL["vproj"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vproj_c.html"

#########################################
CSPYCE_SIGNATURES ["vrel"] = ["float[3]", "float[3]"]
CSPYCE_ARGNAMES   ["vrel"] = ["v1", "v2"]
CSPYCE_RETURNS    ["vrel"] = ["float"]
CSPYCE_RETNAMES   ["vrel"] = ["value"]
CSPYCE_ABSTRACT   ["vrel"] = """
Return the relative difference between two 3-dimensional vectors.
"""
CSPYCE_DEFINITIONS["vrel"] = {
"v1": "The first of two 3-vectors.",
"v2": "The second of two 3-vectors.",
"value": "The relative difference.",
}
CSPYCE_URL["vrel"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vrel_c.html"

#########################################
CSPYCE_SIGNATURES ["vrelg"] = ["float[*]", "float[*]"]
CSPYCE_ARGNAMES   ["vrelg"] = ["v1", "v2"]
CSPYCE_RETURNS    ["vrelg"] = ["float"]
CSPYCE_RETNAMES   ["vrelg"] = ["value"]
CSPYCE_ABSTRACT   ["vrelg"] = """
Return the relative difference between two vectors of general dimension.
"""
CSPYCE_DEFINITIONS["vrelg"] = {
"v1": "The first of two 3-vectors.",
"v2": "The second of two 3-vectors.",
"value": "The relative difference.",
}
CSPYCE_URL["vrelg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vrelg_c.html"

#########################################
CSPYCE_SIGNATURES ["vrotv"] = ["float[3]", "float[3]", "float"]
CSPYCE_ARGNAMES   ["vrotv"] = ["v", "axis", "theta"]
CSPYCE_RETURNS    ["vrotv"] = ["float[3]"]
CSPYCE_RETNAMES   ["vrotv"] = ["r"]
CSPYCE_ABSTRACT   ["vrotv"] = """
Rotate a vector about a specified axis vector by a specified angle and
return the rotated vector.
"""
CSPYCE_DEFINITIONS["vrotv"] = {
"v": "Vector to be rotated.",
"axis": "Axis of the rotation.",
"theta": "Angle of rotation (radians).",
"r": "Result of rotating v about axis by theta.",
}
CSPYCE_URL["vrotv"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vrotv_c.html"

#########################################
CSPYCE_SIGNATURES ["vscl"] = ["float", "float[3]"]
CSPYCE_ARGNAMES   ["vscl"] = ["s", "v1"]
CSPYCE_RETURNS    ["vscl"] = ["float[3]"]
CSPYCE_RETNAMES   ["vscl"] = ["vout"]
CSPYCE_ABSTRACT   ["vscl"] = """
Multiply a scalar and a 3-dimensional double precision vector.
"""
CSPYCE_DEFINITIONS["vscl"] = {
"s": "Scalar to multiply a vector.",
"v1": "Vector to be multiplied.",
"vout": "Product vector, s*v1.",
}
CSPYCE_URL["vscl"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vscl_c.html"

#########################################
CSPYCE_SIGNATURES ["vsclg"] = ["float", "float[*]"]
CSPYCE_ARGNAMES   ["vsclg"] = ["s", "v1"]
CSPYCE_RETURNS    ["vsclg"] = ["float[*]"]
CSPYCE_RETNAMES   ["vsclg"] = ["vout"]
CSPYCE_ABSTRACT   ["vsclg"] = """
Multiply a scalar and a double precision vector of arbitrary dimension.
"""
CSPYCE_DEFINITIONS["vsclg"] = {
"s": "Scalar to multiply a vector.",
"v1": "Vector to be multiplied.",
"vout": "Product vector, s*v1.",
}
CSPYCE_URL["vsclg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vsclg_c.html"

#########################################
CSPYCE_SIGNATURES ["vsep"] = ["float[3]", "float[3]"]
CSPYCE_ARGNAMES   ["vsep"] = ["v1", "v2"]
CSPYCE_RETURNS    ["vsep"] = ["float"]
CSPYCE_RETNAMES   ["vsep"] = ["value"]
CSPYCE_ABSTRACT   ["vsep"] = """
Find the separation angle in radians between two double precision,
3-dimensional vectors.  This angle is defined as zero if either vector
is zero.
"""
CSPYCE_DEFINITIONS["vsep"] = {
"v1": "First vector.",
"v2": "Second vector.",
"value": "The separation angle in radians.",
}
CSPYCE_URL["vsep"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vsep_c.html"

#########################################
CSPYCE_SIGNATURES ["vsepg"] = ["float[*]", "float[*]"]
CSPYCE_ARGNAMES   ["vsepg"] = ["v1", "v2"]
CSPYCE_RETURNS    ["vsepg"] = ["float"]
CSPYCE_RETNAMES   ["vsepg"] = ["value"]
CSPYCE_ABSTRACT   ["vsepg"] = """
Find the separation angle in radians between two double precision
vectors of arbitrary dimension. This angle is defined as zero if either
vector is zero.
"""
CSPYCE_DEFINITIONS["vsepg"] = {
"v1": "First vector.",
"v2": "Second vector.",
"value": "The separation angle in radians.",
}
CSPYCE_URL["vsepg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vsepg_c.html"

#########################################
CSPYCE_SIGNATURES ["vsub"] = ["float[3]", "float[3]"]
CSPYCE_ARGNAMES   ["vsub"] = ["v1", "v2"]
CSPYCE_RETURNS    ["vsub"] = ["float[3]"]
CSPYCE_RETNAMES   ["vsub"] = ["vout"]
CSPYCE_ABSTRACT   ["vsub"] = """
Compute the difference between two 3-dimensional, double precision
vectors.
"""
CSPYCE_DEFINITIONS["vsub"] = {
"v1": "First vector (minuend).",
"v2": "Second vector (subtrahend).",
"vout": "Difference vector, v1 - v2.",
}
CSPYCE_URL["vsub"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vsub_c.html"

#########################################
CSPYCE_SIGNATURES ["vsubg"] = ["float[*]", "float[*]"]
CSPYCE_ARGNAMES   ["vsubg"] = ["v1", "v2"]
CSPYCE_RETURNS    ["vsubg"] = ["float[*]"]
CSPYCE_RETNAMES   ["vsubg"] = ["vout"]
CSPYCE_ABSTRACT   ["vsubg"] = """
Compute the difference between two double precision vectors of arbitrary
dimension.
"""
CSPYCE_DEFINITIONS["vsubg"] = {
"v1": "First vector (minuend).",
"v2": "Second vector (subtrahend).",
"vout": "Difference vector, v1 - v2.",
}
CSPYCE_URL["vsubg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vsubg_c.html"

#########################################
CSPYCE_SIGNATURES ["vtmv"] = ["float[3]", "float[3,3]", "float[3]"]
CSPYCE_ARGNAMES   ["vtmv"] = ["v1", "matrix", "v2"]
CSPYCE_RETURNS    ["vtmv"] = ["float"]
CSPYCE_RETNAMES   ["vtmv"] = ["value"]
CSPYCE_ABSTRACT   ["vtmv"] = """
Multiply the transpose of a 3-dimensional column vector, a 3x3 matrix,
and a 3-dimensional column vector.
"""
CSPYCE_DEFINITIONS["vtmv"] = {
"v1": "3 dimensional double precision column vector.",
"matrix": "3x3 double precision matrix.",
"v2": "3 dimensional double precision column vector.",
"value": "The result of (v1**t * matrix * v2).",
}
CSPYCE_URL["vtmv"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vtmv_c.html"

#########################################
CSPYCE_SIGNATURES ["vtmvg"] = ["float[*]", "float[*,*]", "float[*]"]
CSPYCE_ARGNAMES   ["vtmvg"] = ["v1", "matrix", "v2"]
CSPYCE_RETURNS    ["vtmvg"] = ["float"]
CSPYCE_RETNAMES   ["vtmvg"] = ["value"]
CSPYCE_ABSTRACT   ["vtmvg"] = """
Multiply the transpose of a n-dimensional column vector, a nxm matrix,
and a m-dimensional column vector.
"""
CSPYCE_DEFINITIONS["vtmvg"] = {
"v1": "n-dimensional double precision column vector.",
"matrix": "nxm double precision matrix.",
"v2": "m-dimensional double porecision column vector.",
"value": "The result of (v1**t * matrix * v2).",
}
CSPYCE_URL["vtmvg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vtmvg_c.html"

#########################################
CSPYCE_SIGNATURES ["vupack"] = ["float[3]"]
CSPYCE_ARGNAMES   ["vupack"] = ["v"]
CSPYCE_RETURNS    ["vupack"] = 3*["float"]
CSPYCE_RETNAMES   ["vupack"] = ["x", "y", "z"]
CSPYCE_ABSTRACT   ["vupack"] = """
Unpack three scalar components from a vector.
"""
CSPYCE_DEFINITIONS["vupack"] = {
"v": "3-vector.",
"x": "First scalar component of 3-vector.",
"y": "Second scalar component of 3-vector.",
"z": "Third scalar component of 3-vector.",
}
CSPYCE_URL["vupack"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vupack_c.html"

#########################################
CSPYCE_SIGNATURES ["vzero"] = ["float[3]"]
CSPYCE_ARGNAMES   ["vzero"] = ["v"]
CSPYCE_RETURNS    ["vzero"] = ["bool"]
CSPYCE_RETNAMES   ["vzero"] = ["value"]
CSPYCE_ABSTRACT   ["vzero"] = """
Indicate whether a 3-vector is the zero vector.
"""
CSPYCE_DEFINITIONS["vzero"] = {
"v": "Vector to be tested.",
"value": "True if and only if v is the zero vector.",
}
CSPYCE_URL["vzero"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vzero_c.html"

#########################################
CSPYCE_SIGNATURES ["vzerog"] = ["float[*]"]
CSPYCE_ARGNAMES   ["vzerog"] = ["v"]
CSPYCE_RETURNS    ["vzerog"] = ["bool"]
CSPYCE_RETNAMES   ["vzerog"] = ["value"]
CSPYCE_ABSTRACT   ["vzerog"] = """
Indicate whether a general-dimensional vector is the zero vector.
"""
CSPYCE_DEFINITIONS["vzerog"] = {
"v": "Vector to be tested.",
"value": "True if and only if v is the zero vector.",
}
CSPYCE_URL["vzerog"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vzerog_c.html"

#########################################
CSPYCE_SIGNATURES ["xf2eul"] = ["rotmat[6,6]"] + 3*["int"]
CSPYCE_ARGNAMES   ["xf2eul"] = ["xform", "axisa", "axisb", "axisc"]
CSPYCE_RETURNS    ["xf2eul"] = ["float[3]", "bool"]
CSPYCE_RETNAMES   ["xf2eul"] = ["eulang", "unique"]
CSPYCE_ABSTRACT   ["xf2eul"] = """
Convert a state transformation matrix to Euler angles and their
derivatives with respect to a specified set of axes. The companion
routine eul2xf converts Euler angles and their derivatives with respect
to a specified set of axes to a state transformation matrix.
"""
CSPYCE_DEFINITIONS["xf2eul"] = {
"xform": "A state transformation matrix.",
"axisa": "Axis A of the Euler angle factorization.",
"axisb": "Axis B of the Euler angle factorization.",
"axisc": "Axis C of the Euler angle factorization.",
"eulang": "An array of Euler angles and their derivatives.",
"unique": "Indicates if eulang is a unique representation.",
}
CSPYCE_URL["xf2eul"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/xf2eul_c.html"

#########################################
CSPYCE_SIGNATURES ["xf2rav"] = ["rotmat[6,6]"]
CSPYCE_ARGNAMES   ["xf2rav"] = ["xform"]
CSPYCE_RETURNS    ["xf2rav"] = ["rotmat[3,3]", "float[3]"]
CSPYCE_RETNAMES   ["xf2rav"] = ["rot", "av"]
CSPYCE_ABSTRACT   ["xf2rav"] = """
This routine determines from a state transformation matrix the
associated rotation matrix and angular velocity of the rotation.
"""
CSPYCE_DEFINITIONS["xf2rav"] = {
"xform": "a state transformation matrix.",
"rot": "the rotation associated with xform.",
"av": "the angular velocity associated with xform.",
}
CSPYCE_URL["xf2rav"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/xf2rav_c.html"

#########################################
CSPYCE_SIGNATURES ["xfmsta"] = ["float[6]", "string", "string", "string"]
CSPYCE_ARGNAMES   ["xfmsta"] = ["instate", "insys", "outsys", "body"]
CSPYCE_RETURNS    ["xfmsta"] = ["float[6]"]
CSPYCE_RETNAMES   ["xfmsta"] = ["outstate"]
CSPYCE_ABSTRACT   ["xfmsta"] = """
Transform a state between coordinate systems.
"""
CSPYCE_DEFINITIONS["xfmsta"] = {
"instate": "Input state.",
"insys": "Current (input) coordinate system.",
"outsys": "Desired (output) coordinate system.",
"body": "Name or NAIF ID of body with which coordinates are associated (if applicable).",
"outstate": "Converted output state.",
}
CSPYCE_URL["xfmsta"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/xfmsta_c.html"

#########################################
CSPYCE_SIGNATURES ["xpose6"] = ["float[6,6]"]
CSPYCE_ARGNAMES   ["xpose6"] = ["m1"]
CSPYCE_RETURNS    ["xpose6"] = ["float[6,6]"]
CSPYCE_RETNAMES   ["xpose6"] = ["mout"]
CSPYCE_ABSTRACT   ["xpose6"] = """
Transpose a 6x6 matrix.
"""
CSPYCE_DEFINITIONS["xpose6"] = {
"m1": "6x6 matrix to be transposed.",
"mout": "Transpose of m1.",
}
CSPYCE_URL["xpose6"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/xpose6_c.html"

#########################################
CSPYCE_SIGNATURES ["xpose"] = ["float[3,3]"]
CSPYCE_ARGNAMES   ["xpose"] = ["m1"]
CSPYCE_RETURNS    ["xpose"] = ["float[3,3]"]
CSPYCE_RETNAMES   ["xpose"] = ["mout"]
CSPYCE_ABSTRACT   ["xpose"] = """
Transpose a 3x3 matrix.
"""
CSPYCE_DEFINITIONS["xpose"] = {
"m1": "3x3 matrix to be transposed.",
"mout": "Transpose of m1.",
}
CSPYCE_URL["xpose"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/xpose_c.html"

#########################################
CSPYCE_SIGNATURES ["xposeg"] = ["float[*,*]"]
CSPYCE_ARGNAMES   ["xposeg"] = ["matrix"]
CSPYCE_RETURNS    ["xposeg"] = ["float[*,*]"]
CSPYCE_RETNAMES   ["xposeg"] = ["xposem"]
CSPYCE_ABSTRACT   ["xposeg"] = """
Transpose a matrix of arbitrary size (in place, the matrix need not be
square).
"""
CSPYCE_DEFINITIONS["xposeg"] = {
"matrix": "Matrix to be transposed.",
"xposem": "Transposed matrix.",
}
CSPYCE_URL["xposeg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/xposeg_c.html"

#########################################
