################################################################################
# A dictionary of docstrings and call signatures, keyed by the name of the
# CSPICE function name
################################################################################

SPYCE_SIGNATURES  = {}
SPYCE_ARGNAMES    = {}
SPYCE_DEFAULTS    = {}
SPYCE_RETURNS     = {}
SPYCE_RETNAMES    = {}
SPYCE_ABSTRACT    = {}
SPYCE_DEFINITIONS = {}
SPYCE_PS          = {}
SPYCE_URL         = {}

SPYCE_SIGNATURES ["axisar"] = ["int", "float"]
SPYCE_ARGNAMES   ["axisar"] = ["axis", "angle"]
SPYCE_RETURNS    ["axisar"] = ["rotmat[3,3]"]
SPYCE_RETNAMES   ["axisar"] = ["rotmat"]
SPYCE_ABSTRACT   ["axisar"] = """
Construct a rotation matrix that rotates vectors by a specified angle
about a specified axis.
"""
SPYCE_DEFINITIONS["axisar"] = {
"axis": "Rotation axis.",
"angle": "Rotation angle, in radians.",
"rotmat": "Rotation matrix corresponding to axis and angle.",
}
SPYCE_URL["axisar"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/axisar_c.html"

#########################################
SPYCE_SIGNATURES ["b1900"] = []
SPYCE_ARGNAMES   ["b1900"] = []
SPYCE_RETURNS    ["b1900"] = ["float"]
SPYCE_RETNAMES   ["b1900"] = ["jd"]
SPYCE_ABSTRACT   ["b1900"] = """
Return the Julian Date corresponding to Besselian Date 1900.0.
"""
SPYCE_DEFINITIONS["b1900"] = {
"jd": "JD of Besselian Date 1900.0",
}
SPYCE_URL["b1900"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/b1900_c.html"

#########################################
SPYCE_SIGNATURES ["b1950"] = []
SPYCE_ARGNAMES   ["b1950"] = []
SPYCE_RETURNS    ["b1950"] = ["float"]
SPYCE_RETNAMES   ["b1950"] = ["jd"]
SPYCE_ABSTRACT   ["b1950"] = """
Return the Julian Date corresponding to Besselian Date 1950.0.
"""
SPYCE_DEFINITIONS["b1950"] = {
"jd": "JD of Besselian Date 1950.0",
}
SPYCE_URL["b1950"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/b1950_c.html"

#########################################
SPYCE_SIGNATURES ["bltfrm"] = ["int"]
SPYCE_ARGNAMES   ["bltfrm"] = ["frmcls"]
SPYCE_RETURNS    ["bltfrm"] = ["int[*]"]
SPYCE_RETNAMES   ["bltfrm"] = ["idset"]
SPYCE_ABSTRACT   ["bltfrm"] = """
Return a list containing all the frame IDs of all built-in frames of a
specified class.
"""
SPYCE_DEFINITIONS["bltfrm"] = {
"frmcls": "Frame class (-1 = all; 1 = built-in inertial; 2 = PCK-based; 3 = CK-based; 4 = fixed rotational; 5 = dynamic).",
"idset": "List of ID codes of frames of the specified class.",
}
SPYCE_URL["bltfrm"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bltfrm_c.html"

#########################################
SPYCE_SIGNATURES ["bodc2n"] = ["body_code"]
SPYCE_ARGNAMES   ["bodc2n"] = ["code"]
SPYCE_RETURNS    ["bodc2n"] = ["body_name", "bool"]
SPYCE_RETNAMES   ["bodc2n"] = ["name", "found"]
SPYCE_ABSTRACT   ["bodc2n"] = """
Translate the SPICE integer code of a body into a common name for that
body.
"""
SPYCE_DEFINITIONS["bodc2n"] = {
"code": "Integer ID code to be translated into a name.",
"name": "A common name for the body identified by code.",
"found": "True if translated, otherwise False.",
}
SPYCE_URL["bodc2n"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bodc2n_c.html"

SPYCE_SIGNATURES ["bodc2n_error"] = ["body_code"]
SPYCE_ARGNAMES   ["bodc2n_error"] = ["code"]
SPYCE_RETURNS    ["bodc2n_error"] = ["body_name"]
SPYCE_RETNAMES   ["bodc2n_error"] = ["name"]
SPYCE_ABSTRACT   ["bodc2n_error"] = """
Translate the SPICE integer code of a body into a common name for that
body.
"""
SPYCE_DEFINITIONS["bodc2n_error"] = {
"code": "Integer ID code to be translated into a name.",
"name": "A common name for the body identified by code.",
}
SPYCE_PS ["bodc2n_error"] = "Raise SPICE(BODYIDNOTFOUND) condition if code cound not be translated."
SPYCE_URL["bodc2n_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bodc2n_c.html"

#########################################
SPYCE_SIGNATURES ["bodc2s"] = ["body_code"]
SPYCE_ARGNAMES   ["bodc2s"] = ["code"]
SPYCE_RETURNS    ["bodc2s"] = ["body_name"]
SPYCE_RETNAMES   ["bodc2s"] = ["name"]
SPYCE_ABSTRACT   ["bodc2s"] = """
Translate a body ID code to either the corresponding name or if no name
to ID code mapping exists, the string representation of the body ID
value.
"""
SPYCE_DEFINITIONS["bodc2s"] = {
"code": "Integer ID code to translate to a string.",
"name": "String corresponding to 'code'.",
}
SPYCE_URL["bodc2s"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bodc2s_c.html"

#########################################
SPYCE_SIGNATURES ["boddef"] = ["string", "int"]
SPYCE_ARGNAMES   ["boddef"] = ["name", "code"]
SPYCE_RETURNS    ["boddef"] = []
SPYCE_RETNAMES   ["boddef"] = []
SPYCE_ABSTRACT   ["boddef"] = """
Define a body name/ID code pair for later translation via bodn2c or
bodc2n.
"""
SPYCE_DEFINITIONS["boddef"] = {
"name": "Common name of some body.",
"code": "Integer code for that body.",
}
SPYCE_URL["boddef"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/boddef_c.html"

#########################################
SPYCE_SIGNATURES ["bodfnd"] = ["body_code", "string"]
SPYCE_ARGNAMES   ["bodfnd"] = ["body", "item"]
SPYCE_RETURNS    ["bodfnd"] = ["bool"]
SPYCE_RETNAMES   ["bodfnd"] = ["found"]
SPYCE_ABSTRACT   ["bodfnd"] = """
Determine whether values exist for some item for any body in the kernel
pool.
"""
SPYCE_DEFINITIONS["bodfnd"] = {
"body": "ID code of body.",
"item": "Item to find (\"RADII\", \"NUT_AMP_RA\", etc.).",
"found": "True if the item is in the kernel pool; False if it is not.",
}
SPYCE_URL["bodfnd"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bodfnd_c.html"

#########################################
SPYCE_SIGNATURES ["bodn2c"] = ["body_name"]
SPYCE_ARGNAMES   ["bodn2c"] = ["name"]
SPYCE_RETURNS    ["bodn2c"] = ["body_code", "bool"]
SPYCE_RETNAMES   ["bodn2c"] = ["code", "found"]
SPYCE_ABSTRACT   ["bodn2c"] = """
Translate the name of a body or object to the corresponding SPICE
integer ID code.
"""
SPYCE_DEFINITIONS["bodn2c"] = {
"name": "Body name to be translated into a SPICE ID code.",
"code": "SPICE integer ID code for the named body.",
"found": "True if translated, otherwise False.",
}
SPYCE_URL["bodn2c"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bodn2c_c.html"

SPYCE_SIGNATURES ["bodn2c_error"] = ["body_name"]
SPYCE_ARGNAMES   ["bodn2c_error"] = ["name"]
SPYCE_RETURNS    ["bodn2c_error"] = ["body_code"]
SPYCE_RETNAMES   ["bodn2c_error"] = ["code"]
SPYCE_ABSTRACT   ["bodn2c_error"] = """
Translate the name of a body or object to the corresponding SPICE
integer ID code.
"""
SPYCE_DEFINITIONS["bodn2c_error"] = {
"name": "Body name to be translated into a SPICE ID code.",
"code": "SPICE integer ID code for the named body.",
}
SPYCE_PS ["bodn2c_error"] = "Raise SPICE(BODYNAMENOTFOUND) condition if name cound not be translated."
SPYCE_URL["bodn2c_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bodn2c_c.html"

#########################################
SPYCE_SIGNATURES ["bods2c"] = ["body_name"]
SPYCE_ARGNAMES   ["bods2c"] = ["name"]
SPYCE_RETURNS    ["bods2c"] = ["body_code", "bool"]
SPYCE_RETNAMES   ["bods2c"] = ["code", "found"]
SPYCE_ABSTRACT   ["bods2c"] = """
Translate a string containing a body name or ID code to an integer code.
"""
SPYCE_DEFINITIONS["bods2c"] = {
"name": "String to be translated to an ID code.",
"code": "Integer ID code corresponding to `name'.",
"found": "True if translated, otherwise False.",
}
SPYCE_URL["bods2c"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bods2c_c.html"

SPYCE_SIGNATURES ["bods2c_error"] = ["body_name"]
SPYCE_ARGNAMES   ["bods2c_error"] = ["name"]
SPYCE_RETURNS    ["bods2c_error"] = ["body_code"]
SPYCE_RETNAMES   ["bods2c_error"] = ["code"]
SPYCE_ABSTRACT   ["bods2c_error"] = """
Translate a string containing a body name or ID code to an integer code.
"""
SPYCE_DEFINITIONS["bods2c_error"] = {
"name": "String to be translated to an ID code.",
"code": "Integer ID code corresponding to `name'.",
}
SPYCE_PS ["bods2c_error"] = "Raise SPICE(BODYNAMENOTFOUND) condition if name cound not be translated."
SPYCE_URL["bods2c_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bods2c_c.html"

#########################################
SPYCE_SIGNATURES ["bodvar"] = ["body_code", "string"]
SPYCE_ARGNAMES   ["bodvar"] = ["bodyid", "item"]
SPYCE_RETURNS    ["bodvar"] = ["float[*]"]
SPYCE_RETNAMES   ["bodvar"] = ["values"]
SPYCE_ABSTRACT   ["bodvar"] = """
Deprecated: This routine has been superseded by bodvcd and bodvrd. This
routine is supported for purposes of backward compatibility only.

Return the values of some item for any body in the kernel pool.
"""
SPYCE_DEFINITIONS["bodvar"] = {
"bodyid": "ID code of body.",
"item"  : "Item for which values are desired. (\"RADII\", \"NUT_PREC_ANGLES\", etc.)",
"values": "Values.",
}
SPYCE_URL["bodvar"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bodvar_c.html"

#########################################
SPYCE_SIGNATURES ["bodvcd"] = ["body_code", "string"]
SPYCE_ARGNAMES   ["bodvcd"] = ["bodyid", "item"]
SPYCE_RETURNS    ["bodvcd"] = ["float[*]"]
SPYCE_RETNAMES   ["bodvcd"] = ["values"]
SPYCE_ABSTRACT   ["bodvcd"] = """
Fetch from the kernel pool the float values of an item associated with a
body, where the body is specified by an integer ID code.
"""
SPYCE_DEFINITIONS["bodvcd"] = {
"bodyid": "Body ID code.",
"item"  : "Item for which values are desired. (\"RADII\", \"NUT_PREC_ANGLES\", etc.).",
"values": "Values as an array.",
}
SPYCE_URL["bodvcd"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bodvcd_c.html"

#########################################
SPYCE_SIGNATURES ["bodvrd"] = ["body_name", "string"]
SPYCE_ARGNAMES   ["bodvrd"] = ["bodynm", "item"]
SPYCE_RETURNS    ["bodvrd"] = ["float[*]"]
SPYCE_RETNAMES   ["bodvrd"] = ["values"]
SPYCE_ABSTRACT   ["bodvrd"] = """
Fetch from the kernel pool the double precision values of an item
associated with a body.
"""
SPYCE_DEFINITIONS["bodvrd"] = {
"bodynm": "Body name.",
"item"  : "Item for which values are desired. (\"RADII\", \"NUT_PREC_ANGLES\", etc.).",
"values": "Values as an array.",
}
SPYCE_URL["bodvrd"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bodvrd_c.html"

#########################################
SPYCE_SIGNATURES ["ccifrm"] = ["int", "int"]
SPYCE_ARGNAMES   ["ccifrm"] = ["frclss", "clssid"]
SPYCE_RETURNS    ["ccifrm"] = ["int", "string", "int", "bool"]
SPYCE_RETNAMES   ["ccifrm"] = ["frcode", "frname", "center", "found"]
SPYCE_ABSTRACT   ["ccifrm"] = """
Return the frame name, frame ID, and center associated with a given
frame class and class ID.
"""
SPYCE_DEFINITIONS["ccifrm"] = {
"frclss": "Class of frame.",
"clssid": "Class ID of frame.",
"frcode": "ID code of the frame.",
"frname": "Name of the frame.",
"center": "ID code of the center of the frame.",
"found": "True if the requested information is available.",
}
SPYCE_URL["ccifrm"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ccifrm_c.html"

SPYCE_SIGNATURES ["ccifrm_error"] = ["int", "int"]
SPYCE_ARGNAMES   ["ccifrm_error"] = ["frclss", "clssid"]
SPYCE_RETURNS    ["ccifrm_error"] = ["int", "string", "int"]
SPYCE_RETNAMES   ["ccifrm_error"] = ["frcode", "frname", "center"]
SPYCE_ABSTRACT   ["ccifrm_error"] = """
Return the frame name, frame ID, and center associated with a given
frame class and class ID.
"""
SPYCE_DEFINITIONS["ccifrm_error"] = {
"frclss": "Class of frame.",
"clssid": "Class ID of frame.",
"frcode": "ID code of the frame.",
"frname": "Name of the frame.",
"center": "ID code of the center of the frame.",
}
SPYCE_PS ["ccifrm_error"] = "Raise SPICE(INVALIDFRAMEDEF) condition if frame is not found."
SPYCE_URL["ccifrm_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ccifrm_c.html"

#########################################
SPYCE_SIGNATURES ["cgv2el"] = 3*["float[3]"]
SPYCE_ARGNAMES   ["cgv2el"] = ["center", "vec1", "vec2"]
SPYCE_RETURNS    ["cgv2el"] = ["float[9]"]
SPYCE_RETNAMES   ["cgv2el"] = ["ellipse"]
SPYCE_ABSTRACT   ["cgv2el"] = """
Form a CSPICE ellipse from a center vector and two generating vectors.
"""
SPYCE_DEFINITIONS["cgv2el"] = {
"center" : "center vector",
"vec1"   : "two generating vectors for an ellipse.",
"vec2"   : "two generating vectors for an ellipse.",
"ellipse": "the CSPICE ellipse defined by the input vectors.",
}
SPYCE_URL["cgv2el"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cgv2el_c.html"

#########################################
SPYCE_SIGNATURES ["chkin"] = ["string"]
SPYCE_ARGNAMES   ["chkin"] = ["module"]
SPYCE_RETURNS    ["chkin"] = []
SPYCE_RETNAMES   ["chkin"] = []
SPYCE_ABSTRACT   ["chkin"] = """
Inform the CSPICE error handling mechanism of entry into a routine.
"""
SPYCE_DEFINITIONS["chkin"] = {
"module": "The name of the calling routine.",
}
SPYCE_URL["chkin"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/chkin_c.html"

#########################################
SPYCE_SIGNATURES ["chkout"] = ["string"]
SPYCE_ARGNAMES   ["chkout"] = ["module"]
SPYCE_RETURNS    ["chkout"] = []
SPYCE_RETNAMES   ["chkout"] = []
SPYCE_ABSTRACT   ["chkout"] = """
Inform the CSPICE error handling mechanism of exit from a routine.
"""
SPYCE_DEFINITIONS["chkout"] = {
"module": "The name of the calling routine.",
}
SPYCE_URL["chkout"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/chkout_c.html"

#########################################
SPYCE_SIGNATURES ["cidfrm"] = ["body_code"]
SPYCE_ARGNAMES   ["cidfrm"] = ["cent"]
SPYCE_RETURNS    ["cidfrm"] = ["frame_code", "frame_name", "bool"]
SPYCE_RETNAMES   ["cidfrm"] = ["frcode", "frname", "found"]
SPYCE_ABSTRACT   ["cidfrm"] = """
Retrieve frame ID code and name to associate with a frame center.
"""
SPYCE_DEFINITIONS["cidfrm"] = {
"cent": "An object ID to associate a frame with.",
"frcode": "The ID code of the frame associated with cent.",
"frname": "The name of the frame with ID frcode.",
"found": "True if the requested information is available.",
}
SPYCE_PS ["cidfrm"] = "Raise SPICE(CKINSUFFDATA) condition if the requested information is unavailable."
SPYCE_URL["cidfrm"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cidfrm_c.html"

SPYCE_SIGNATURES ["cidfrm_error"] = ["body_code"]
SPYCE_ARGNAMES   ["cidfrm_error"] = ["cent"]
SPYCE_RETURNS    ["cidfrm_error"] = ["frame_code", "frame_name"]
SPYCE_RETNAMES   ["cidfrm_error"] = ["frcode", "frname"]
SPYCE_ABSTRACT   ["cidfrm_error"] = """
Retrieve frame ID code and name to associate with a frame center.
"""
SPYCE_DEFINITIONS["cidfrm_error"] = {
"cent": "An object ID to associate a frame with.",
"frcode": "The ID code of the frame associated with cent.",
"frname": "The name of the frame with ID frcode.",
}
SPYCE_PS ["cidfrm_error"] = "Raise SPICE(BODYIDNOTFOUND) condition if the requested information is unavailable."
SPYCE_URL["cidfrm_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cidfrm_c.html"

#########################################
SPYCE_SIGNATURES ["ckcov"] = ["string", "body_code", "bool", "string", "float", "string"]
SPYCE_ARGNAMES   ["ckcov"] = ["ck", "idcode", "needav", "level", "tol", "timsys"]
SPYCE_RETURNS    ["ckcov"] = ["float[*,2]"]
SPYCE_RETNAMES   ["ckcov"] = ["cover"]
SPYCE_ABSTRACT   ["ckcov"] = """
Find the coverage window for a specified object in a specified CK file.
"""
SPYCE_DEFINITIONS["ckcov"] = {
"ck": "Name of CK file.",
"idcode": "ID code of object.",
"needav": "Flag indicating whether angular velocity is needed.",
"level": "Coverage level: \"SEGMENT\" OR \"INTERVAL\".",
"tol": "Tolerance in ticks.",
"timsys": "Time system used to represent coverage.",
"cover":  "array of shape (intervals,2) where cover[:,0] are start times and cover[:,1] are stop times.",
}
SPYCE_URL["ckcov"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckcov_c.html"

SPYCE_SIGNATURES ["ckcov_error"] = ["string", "body_code", "bool", "string", "float", "string"]
SPYCE_ARGNAMES   ["ckcov_error"] = ["ck", "idcode", "needav", "level", "tol", "timsys"]
SPYCE_RETURNS    ["ckcov_error"] = ["float[*,2]"]
SPYCE_RETNAMES   ["ckcov_error"] = ["cover"]
SPYCE_ABSTRACT   ["ckcov_error"] = """
Find the coverage window for a specified object in a specified CK file.
"""
SPYCE_DEFINITIONS["ckcov_error"] = {
"ck": "Name of CK file.",
"idcode": "ID code of object.",
"needav": "Flag indicating whether angular velocity is needed.",
"level": "Coverage level: \"SEGMENT\" or \"INTERVAL\".",
"tol": "Tolerance in ticks.",
"timsys": "Time system used to represent coverage.",
"cover": "array of shape (intervals,2) where cover[:,0] are start times and cover[:,1] are stop times.",
}
SPYCE_PS ["ckcov_error"] = "Raise SPICE(BODYIDNOTFOUND) if the body code is not found in the C kernel."
SPYCE_URL["ckcov_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckcov_c.html"

#########################################
SPYCE_SIGNATURES ["ckgp"] = ["body_code", "float", "float", "frame_name"]
SPYCE_ARGNAMES   ["ckgp"] = ["inst", "sclkdp", "tol", "ref"]
SPYCE_RETURNS    ["ckgp"] = ["rotmat[3,3]", "float", "bool"]
SPYCE_RETNAMES   ["ckgp"] = ["cmat", "clkout", "found"]
SPYCE_ABSTRACT   ["ckgp"] = """
Get pointing(attitude) for a specified spacecraft clock time.
"""
SPYCE_DEFINITIONS["ckgp"] = {
"inst": "NAIF ID of instrument, spacecraft, or structure.",
"sclkdp": "Encoded spacecraft clock time.",
"tol": "Time tolerance.",
"ref": "Reference frame.",
"cmat": "C-matrix pointing data.",
"clkout": "Output encoded spacecraft clock time.",
"found": "True when requested pointing is available.",
}
SPYCE_URL["ckgp"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckgp_c.html"

SPYCE_SIGNATURES ["ckgp_error"] = ["body_code", "float", "float", "frame_name"]
SPYCE_ARGNAMES   ["ckgp_error"] = ["inst", "sclkdp", "tol", "ref"]
SPYCE_RETURNS    ["ckgp_error"] = ["rotmat[3,3]", "float"]
SPYCE_RETNAMES   ["ckgp_error"] = ["cmat", "clkout"]
SPYCE_ABSTRACT   ["ckgp_error"] = """
Get pointing (attitude) for a specified spacecraft clock time.
"""
SPYCE_DEFINITIONS["ckgp_error"] = {
"inst": "NAIF ID of instrument, spacecraft, or structure.",
"sclkdp": "Encoded spacecraft clock time.",
"tol": "Time tolerance.",
"ref": "Reference frame.",
"cmat": "C-matrix pointing data.",
"clkout": "Output encoded spacecraft clock time.",
}
SPYCE_PS ["ckgp_error"] = "Raise SPICE(CKINSUFFDATA) condition if the requested information is unavailable."
SPYCE_URL["ckgp_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckgp_c.html"

#########################################
SPYCE_SIGNATURES ["ckgpav"] = ["body_code", "float", "float", "frame_name"]
SPYCE_ARGNAMES   ["ckgpav"] = ["inst", "sclkdp", "tol", "ref"]
SPYCE_RETURNS    ["ckgpav"] = ["rotmat[3,3]", "float[3]", "float", "bool"]
SPYCE_RETNAMES   ["ckgpav"] = ["cmat", "av", "clkout", "found"]
SPYCE_ABSTRACT   ["ckgpav"] = """
Get pointing(attitude) and angular velocity for a spacecraft clock time.
"""
SPYCE_DEFINITIONS["ckgpav"] = {
"inst": "NAIF ID of instrument, spacecraft, or structure.",
"sclkdp": "Encoded spacecraft clock time.",
"tol": "Time tolerance.",
"ref": "Reference frame.",
"cmat": "C-matrix pointing data.",
"av": "Angular velocity vector.",
"clkout": "Output encoded spacecraft clock time.",
"found": "True when requested pointing is available.",
}
SPYCE_URL["ckgpav"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckgpav_c.html"

SPYCE_SIGNATURES ["ckgpav_error"] = ["body_code", "float", "float", "frame_name"]
SPYCE_ARGNAMES   ["ckgpav_error"] = ["inst", "sclkdp", "tol", "ref"]
SPYCE_RETURNS    ["ckgpav_error"] = ["rotmat[3,3]", "float[3]", "float"]
SPYCE_RETNAMES   ["ckgpav_error"] = ["cmat", "av", "clkout"]
SPYCE_ABSTRACT   ["ckgpav_error"] = """
Get pointing (attitude) and angular velocity for a spacecraft clock
time.
"""
SPYCE_DEFINITIONS["ckgpav_error"] = {
"inst": "NAIF ID of instrument, spacecraft, or structure.",
"sclkdp": "Encoded spacecraft clock time.",
"tol": "Time tolerance.",
"ref": "Reference frame.",
"cmat": "C-matrix pointing data.",
"av": "Angular velocity vector.",
"clkout": "Output encoded spacecraft clock time.",
}
SPYCE_PS ["ckgpav_error"] = "Raise SPICE(CKINSUFFDATA) condition if the requested information is unavailable."
SPYCE_URL["ckgpav_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckgpav_c.html"

#########################################
SPYCE_SIGNATURES ["ckobj"] = ["string"]
SPYCE_ARGNAMES   ["ckobj"] = ["ck"]
SPYCE_RETURNS    ["ckobj"] = ["int[*]"]
SPYCE_RETNAMES   ["ckobj"] = ["ids"]
SPYCE_ABSTRACT   ["ckobj"] = """
Find the set of ID codes of all objects in a specified CK file.
"""
SPYCE_DEFINITIONS["ckobj"] = {
"ck": "Name of CK file.",
"ids": "Array of ID codes of objects in CK file.",
}
SPYCE_URL["ckobj"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckobj_c.html"

#########################################
SPYCE_SIGNATURES ["clight"] = []
SPYCE_ARGNAMES   ["clight"] = []
SPYCE_RETURNS    ["clight"] = ["float"]
SPYCE_RETNAMES   ["clight"] = ["c"]
SPYCE_ABSTRACT   ["clight"] = """
Return the speed of light in a vacuum (IAU official value, in km/sec).
"""
SPYCE_DEFINITIONS["clight"] = {
"c": "speed of light",
}
SPYCE_URL["clight"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/clight_c.html"

#########################################
SPYCE_SIGNATURES ["clpool"] = []
SPYCE_ARGNAMES   ["clpool"] = []
SPYCE_RETURNS    ["clpool"] = []
SPYCE_RETNAMES   ["clpool"] = []
SPYCE_ABSTRACT   ["clpool"] = """
Remove all variables from the kernel pool.
"""
SPYCE_DEFINITIONS["clpool"] = {}
SPYCE_URL["clpool"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/clpool_c.html"

#########################################
SPYCE_SIGNATURES ["cnmfrm"] = ["body_name"]
SPYCE_ARGNAMES   ["cnmfrm"] = ["cname"]
SPYCE_RETURNS    ["cnmfrm"] = ["frame_code", "frame_name", "bool"]
SPYCE_RETNAMES   ["cnmfrm"] = ["frcode", "frname", "found"]
SPYCE_ABSTRACT   ["cnmfrm"] = """
Retrieve frame ID code and name to associate with an object.
"""
SPYCE_DEFINITIONS["cnmfrm"] = {
"cname": "Name of the object to find a frame for.",
"frcode": "The ID code of the frame associated with cname.",
"frname": "The name of the frame with ID frcode.",
"found": "True if the requested information is available.",
}
SPYCE_URL["cnmfrm"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cnmfrm_c.html"

SPYCE_SIGNATURES ["cnmfrm_error"] = ["body_name"]
SPYCE_ARGNAMES   ["cnmfrm_error"] = ["cname"]
SPYCE_RETURNS    ["cnmfrm_error"] = ["frame_code", "frame_name"]
SPYCE_RETNAMES   ["cnmfrm_error"] = ["frcode", "frname"]
SPYCE_ABSTRACT   ["cnmfrm_error"] = """
Retrieve frame ID code and name to associate with an object.
"""
SPYCE_DEFINITIONS["cnmfrm_error"] = {
"cname": "Name of the object to find a frame for.",
"frcode": "The ID code of the frame associated with cname.",
"frname": "The name of the frame with ID frcode.",
}
SPYCE_PS ["cnmfrm_error"] = "Raise SPICE(BODYNAMENOTFOUND) condition if the requested information is unavailable."
SPYCE_URL["cnmfrm_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cnmfrm_c.html"

#########################################
SPYCE_SIGNATURES ["conics"] = ["float[8]", "time"]
SPYCE_ARGNAMES   ["conics"] = ["elts", "et"]
SPYCE_RETURNS    ["conics"] = ["float[6]"]
SPYCE_RETNAMES   ["conics"] = ["state"]
SPYCE_ABSTRACT   ["conics"] = """
Determine the state (position, velocity) of an orbiting body from a set
of elliptic, hyperbolic, or parabolic orbital elements.
"""
SPYCE_DEFINITIONS["conics"] = {
"elts": "Conic elements.",
"et": "Input time.",
"state": "State of orbiting body at et.",
}
SPYCE_URL["conics"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/conics_c.html"

#########################################
SPYCE_SIGNATURES ["convrt"] = ["float", "string", "string"]
SPYCE_ARGNAMES   ["convrt"] = ["x", "in1", "out"]
SPYCE_RETURNS    ["convrt"] = ["float"]
SPYCE_RETNAMES   ["convrt"] = ["y"]
SPYCE_ABSTRACT   ["convrt"] = """
Take a measurement X, the units associated with X, and units to which X
should be converted; return Y, the value of the measurement in the output
units.
"""
SPYCE_DEFINITIONS["convrt"] = {
"x": "Number representing a measurement in some units.",
"in1": "The units in which x is measured.",
"out": "Desired units for the measurement.",
"y": "The measurment in the desired units.",
}
SPYCE_URL["convrt"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/convrt_c.html"

#########################################
SPYCE_SIGNATURES ["cyllat"] = 3*["float"]
SPYCE_ARGNAMES   ["cyllat"] = ["r", "lonc", "z"]
SPYCE_RETURNS    ["cyllat"] = 3*["float"]
SPYCE_RETNAMES   ["cyllat"] = ["radius", "lon", "lat"]
SPYCE_ABSTRACT   ["cyllat"] = """
Convert from cylindrical to latitudinal coordinates.
"""
SPYCE_DEFINITIONS["cyllat"] = {
"r": "Distance of point from z axis.",
"lonc": "Cylindrical angle of point from XZ plane (radians).",
"z": "Height of point above XY plane.",
"radius": "Distance of point from origin.",
"lon": "Longitude of point (radians).",
"lat": "Latitude of point  (radians).",
}
SPYCE_URL["cyllat"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cyllat_c.html"

#########################################
SPYCE_SIGNATURES ["cylrec"] = 3*["float"]
SPYCE_ARGNAMES   ["cylrec"] = ["r", "lon", "z"]
SPYCE_RETURNS    ["cylrec"] = ["float[3]"]
SPYCE_RETNAMES   ["cylrec"] = ["rectan"]
SPYCE_ABSTRACT   ["cylrec"] = """
Convert from cylindrical to rectangular coordinates.
"""
SPYCE_DEFINITIONS["cylrec"] = {
"r": "Distance of a point from z axis.",
"lon": "Angle (radians) of a point from xZ plane",
"z": "Height of a point above xY plane.",
"rectan": "Rectangular coordinates of the point.",
}
SPYCE_URL["cylrec"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cylrec_c.html"

#########################################
SPYCE_SIGNATURES ["cylsph"] = 3*["float"]
SPYCE_ARGNAMES   ["cylsph"] = ["r", "lonc", "z"]
SPYCE_RETURNS    ["cylsph"] = 3*["float"]
SPYCE_RETNAMES   ["cylsph"] = ["radius", "colat", "lon"]
SPYCE_ABSTRACT   ["cylsph"] = """
Convert from cylindrical to spherical coordinates.
"""
SPYCE_DEFINITIONS["cylsph"] = {
"r": "Distance of point from z axis.",
"lonc": "Angle (radians) of point from XZ plane.",
"z": "Height of point above XY plane.",
"radius": "Distance of point from origin.",
"colat": "Polar angle (co-latitude in radians) of point.",
"lon": "Azimuthal angle (longitude) of point (radians).",
}
SPYCE_URL["cylsph"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cylsph_c.html"

#########################################
SPYCE_SIGNATURES ["dafbfs"] = ["int"]
SPYCE_ARGNAMES   ["dafbfs"] = ["handle"]
SPYCE_RETURNS    ["dafbfs"] = []
SPYCE_RETNAMES   ["dafbfs"] = []
SPYCE_ABSTRACT   ["dafbfs"] = """
Begin a forward search for arrays in a DAF.
"""
SPYCE_DEFINITIONS["dafbfs"] = {
"handle": "Handle of file to be searched.",
}
SPYCE_URL["dafbfs"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafbfs_c.html"

#########################################
SPYCE_SIGNATURES ["dafcls"] = ["int"]
SPYCE_ARGNAMES   ["dafcls"] = ["handle"]
SPYCE_RETURNS    ["dafcls"] = []
SPYCE_RETNAMES   ["dafcls"] = []
SPYCE_ABSTRACT   ["dafcls"] = """
Close the DAF associated with a given handle.
"""
SPYCE_DEFINITIONS["dafcls"] = {
"handle": "Handle of DAF to be closed.",
}
SPYCE_URL["dafcls"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafcls_c.html"

#########################################
SPYCE_SIGNATURES ["dafgda"] = 3*["int"]
SPYCE_ARGNAMES   ["dafgda"] = ["handle", "begin", "end"]
SPYCE_RETURNS    ["dafgda"] = ["float[*]"]
SPYCE_RETNAMES   ["dafgda"] = ["data"]
SPYCE_ABSTRACT   ["dafgda"] = """
Read the double precision data bounded by two addresses within a DAF.
"""
SPYCE_DEFINITIONS["dafgda"] = {
"handle": "Handle of a DAF.",
"begin": "Initial address within file.",
"end": "Final address within file.",
"data": "Data contained between `begin' and `end'.",
}
SPYCE_URL["dafgda"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafgda_c.html"

#########################################
SPYCE_SIGNATURES ["dafgn"] = ["int"]
SPYCE_ARGNAMES   ["dafgn"] = ["lenout"]
SPYCE_RETURNS    ["dafgn"] = ["string"]
SPYCE_RETNAMES   ["dafgn"] = ["name"]
SPYCE_ABSTRACT   ["dafgn"] = """
Return (get) the name for the current array in the current DAF.
"""
SPYCE_DEFINITIONS["dafgn"] = {
"lenout": "Length of array name string.",
"name": "Name of current array.",
}
SPYCE_URL["dafgn"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafgn_c.html"

#########################################
SPYCE_SIGNATURES ["dafgs"] = []
SPYCE_ARGNAMES   ["dafgs"] = []
SPYCE_RETURNS    ["dafgs"] = ["float[128]"]
SPYCE_RETNAMES   ["dafgs"] = ["sum"]
SPYCE_ABSTRACT   ["dafgs"] = """
Return (get) the summary for the current array in the current DAF.
"""
SPYCE_DEFINITIONS["dafgs"] = {
"sum": "Summary for current array.",
}
SPYCE_URL["dafgs"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafgs_c.html"

#########################################
SPYCE_SIGNATURES ["daffna"] = []
SPYCE_ARGNAMES   ["daffna"] = []
SPYCE_RETURNS    ["daffna"] = ["bool"]
SPYCE_RETNAMES   ["daffna"] = ["found"]
SPYCE_ABSTRACT   ["daffna"] = """
Find the next (forward) array in the current DAF.
"""
SPYCE_DEFINITIONS["daffna"] = {
"found": "True if an array was found.",
}
SPYCE_URL["daffna"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/daffna_c.html"

#########################################
SPYCE_SIGNATURES ["dafopr"] = ["string"]
SPYCE_ARGNAMES   ["dafopr"] = ["fname"]
SPYCE_RETURNS    ["dafopr"] = ["int"]
SPYCE_RETNAMES   ["dafopr"] = ["handle"]
SPYCE_ABSTRACT   ["dafopr"] = """
Open a DAF for subsequent read requests.
"""
SPYCE_DEFINITIONS["dafopr"] = {
"fname": "Name of DAF to be opened.",
"handle": "Handle assigned to DAF.",
}
SPYCE_URL["dafopr"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafopr_c.html"

#########################################
SPYCE_SIGNATURES ["dafus"] = ["float[*]", "int", "int"]
SPYCE_ARGNAMES   ["dafus"] = ["sum", "nd", "ni"]
SPYCE_RETURNS    ["dafus"] = ["float[*]", "int[*]"]
SPYCE_RETNAMES   ["dafus"] = ["dc", "ic"]
SPYCE_ABSTRACT   ["dafus"] = """
Unpack an array summary into its double precision and integer
components.
"""
SPYCE_DEFINITIONS["dafus"] = {
"sum": "Array summary.",
"nd": "Number of double precision components.",
"ni": "Number of integer components.",
"dc": "Double precision components.",
"ic": "Integer components.",
}
SPYCE_URL["dafus"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafus_c.html"

#########################################
SPYCE_SIGNATURES ["dcyldr"] = 3*["float"]
SPYCE_ARGNAMES   ["dcyldr"] = ["x", "y", "z"]
SPYCE_RETURNS    ["dcyldr"] = ["float[3,3]"]
SPYCE_RETNAMES   ["dcyldr"] = ["jacobi"]
SPYCE_ABSTRACT   ["dcyldr"] = """
This routine computes the Jacobian of the transformation from
rectangular to cylindrical coordinates.
"""
SPYCE_DEFINITIONS["dcyldr"] = {
"x": "X-coordinate of point.",
"y": "Y-coordinate of point.",
"z": "Z-coordinate of point.",
"jacobi": "Matrix of partial derivatives.",
}
SPYCE_URL["dcyldr"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dcyldr_c.html"

#########################################
SPYCE_SIGNATURES ["deltet"] = ["time", "string"]
SPYCE_ARGNAMES   ["deltet"] = ["epoch", "eptype"]
SPYCE_RETURNS    ["deltet"] = ["float"]
SPYCE_RETNAMES   ["deltet"] = ["delta"]
SPYCE_ABSTRACT   ["deltet"] = """
Return the value of Delta ET (ET-UTC) for an input epoch.
"""
SPYCE_DEFINITIONS["deltet"] = {
"epoch": "Input epoch (seconds past J2000).",
"eptype": "Type of input epoch (\"UTC\" or \"ET\").",
"delta": "Delta ET (ET-UTC) at input epoch.",
}
SPYCE_URL["deltet"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/deltet_c.html"

#########################################
SPYCE_SIGNATURES ["det"] = ["float[3,3]"]
SPYCE_ARGNAMES   ["det"] = ["m1"]
SPYCE_RETURNS    ["det"] = ["float"]
SPYCE_RETNAMES   ["det"] = ["value"]
SPYCE_ABSTRACT   ["det"] = """
Compute the determinant of a double precision 3x3 matrix.
"""
SPYCE_DEFINITIONS["det"] = {
"m1": "Matrix whose determinant is to be found.",
"value": "value of determinant.",
}
SPYCE_URL["det"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/det_c.html"

#########################################
SPYCE_SIGNATURES ["dgeodr"] = 5*["float"]
SPYCE_ARGNAMES   ["dgeodr"] = ["x", "y", "z", "re", "f"]
SPYCE_RETURNS    ["dgeodr"] = ["float[3,3]"]
SPYCE_RETNAMES   ["dgeodr"] = ["jacobi"]
SPYCE_ABSTRACT   ["dgeodr"] = """
This routine computes the Jacobian of the transformation from
rectangular to geodetic coordinates.
"""
SPYCE_DEFINITIONS["dgeodr"] = {
"x": "X-coordinate of point.",
"y": "Y-coordinate of point.",
"z": "Z-coordinate of point.",
"re": "Equatorial radius of the reference spheroid.",
"f": "Flattening coefficient.",
"jacobi": "Matrix of partial derivatives.",
}
SPYCE_URL["dgeodr"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dgeodr_c.html"

#########################################
SPYCE_SIGNATURES ["diags2"] = ["float[2,2]"]
SPYCE_ARGNAMES   ["diags2"] = ["symmat"]
SPYCE_RETURNS    ["diags2"] = 2*["float[2,2]"]
SPYCE_RETNAMES   ["diags2"] = ["diag", "rotate"]
SPYCE_ABSTRACT   ["diags2"] = """
Diagonalize a symmetric 2x2 matrix.
"""
SPYCE_DEFINITIONS["diags2"] = {
"symmat": "A symmetric 2x2 matrix.",
"diag": "A diagonal matrix similar to symmat.",
"rotate": "A rotation used as the similarity transformation.",
}
SPYCE_URL["diags2"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/diags2_c.html"

#########################################
SPYCE_SIGNATURES ["dlatdr"] = 3*["float"]
SPYCE_ARGNAMES   ["dlatdr"] = ["x", "y", "z"]
SPYCE_RETURNS    ["dlatdr"] = ["float[3,3]"]
SPYCE_RETNAMES   ["dlatdr"] = ["jacobi"]
SPYCE_ABSTRACT   ["dlatdr"] = """
This routine computes the Jacobian of the transformation from
rectangular to latitudinal coordinates.
"""
SPYCE_DEFINITIONS["dlatdr"] = {
"x": "X-coordinate of point.",
"y": "Y-coordinate of point.",
"z": "Z-coordinate of point.",
"jacobi": "Matrix of partial derivatives.",
}
SPYCE_URL["dlatdr"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dlatdr_c.html"

#########################################
SPYCE_SIGNATURES ["dpgrdr"] = ["body_name"] + 5*["float"]
SPYCE_ARGNAMES   ["dpgrdr"] = ["body", "x", "y", "z", "re", "f"]
SPYCE_RETURNS    ["dpgrdr"] = ["float[3,3]"]
SPYCE_RETNAMES   ["dpgrdr"] = ["jacobi"]
SPYCE_ABSTRACT   ["dpgrdr"] = """
This routine computes the Jacobian matrix of the transformation from
rectangular to planetographic coordinates.
"""
SPYCE_DEFINITIONS["dpgrdr"] = {
"body": "Body with which coordinate system is associated.",
"x": "X-coordinate of point.",
"y": "Y-coordinate of point.",
"z": "Z-coordinate of point.",
"re": "Equatorial radius of the reference spheroid.",
"f": "Flattening coefficient.",
"jacobi": "Matrix of partial derivatives.",
}
SPYCE_URL["dpgrdr"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dpgrdr_c.html"

#########################################
SPYCE_SIGNATURES ["dpmax"] = []
SPYCE_ARGNAMES   ["dpmax"] = []
SPYCE_RETURNS    ["dpmax"] = ["float"]
SPYCE_RETNAMES   ["dpmax"] = ["value"]
SPYCE_ABSTRACT   ["dpmax"] = """
Return the value of the largest (positive) number representable in a
double precision variable.
"""
SPYCE_DEFINITIONS["dpmax"] = {
"value": "maximum respresentable double-precision number",
}
SPYCE_URL["dpmax"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dpmax_c.html"

#########################################
SPYCE_SIGNATURES ["dpmin"] = []
SPYCE_ARGNAMES   ["dpmin"] = []
SPYCE_RETURNS    ["dpmin"] = ["float"]
SPYCE_RETNAMES   ["dpmin"] = ["value"]
SPYCE_ABSTRACT   ["dpmin"] = """
Return the value of the smallest (negative) number representable in a
double precision variable.
"""
SPYCE_DEFINITIONS["dpmin"] = {
"value": "minimum respresentable double-precision number (negative)",
}
SPYCE_URL["dpmin"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dpmin_c.html"

#########################################
SPYCE_SIGNATURES ["dpr"] = []
SPYCE_ARGNAMES   ["dpr"] = []
SPYCE_RETURNS    ["dpr"] = ["float"]
SPYCE_RETNAMES   ["dpr"] = ["value"]
SPYCE_ABSTRACT   ["dpr"] = """
Return the number of degrees per radian.
"""
SPYCE_DEFINITIONS["dpr"] = {
"value": "degrees per radian"
}
SPYCE_URL["dpr"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dpr_c.html"

#########################################
SPYCE_SIGNATURES ["drdcyl"] = 3*["float"]
SPYCE_ARGNAMES   ["drdcyl"] = ["r", "lon", "z"]
SPYCE_RETURNS    ["drdcyl"] = ["float[3,3]"]
SPYCE_RETNAMES   ["drdcyl"] = ["jacobi"]
SPYCE_ABSTRACT   ["drdcyl"] = """
This routine computes the Jacobian of the transformation from
cylindrical to rectangular coordinates.
"""
SPYCE_DEFINITIONS["drdcyl"] = {
"r": "Distance of a point from the origin.",
"lon": "Angle of the point from the xz plane in radians.",
"z": "Height of the point above the xy plane.",
"jacobi": "Matrix of partial derivatives.",
}
SPYCE_URL["drdcyl"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/drdcyl_c.html"

#########################################
SPYCE_SIGNATURES ["drdgeo"] = 5*["float"]
SPYCE_ARGNAMES   ["drdgeo"] = ["lon", "lat", "alt", "re", "f"]
SPYCE_RETURNS    ["drdgeo"] = ["float[3,3]"]
SPYCE_RETNAMES   ["drdgeo"] = ["jacobi"]
SPYCE_ABSTRACT   ["drdgeo"] = """
This routine computes the Jacobian of the transformation from geodetic
to rectangular coordinates.
"""
SPYCE_DEFINITIONS["drdgeo"] = {
"lon": "Geodetic longitude of point (radians).",
"lat": "Geodetic latitude of point (radians).",
"alt": "Altitude of point above the reference spheroid.",
"re": "Equatorial radius of the reference spheroid.",
"f": "Flattening coefficient.",
"jacobi": "Matrix of partial derivatives.",
}
SPYCE_URL["drdgeo"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/drdgeo_c.html"

#########################################
SPYCE_SIGNATURES ["drdlat"] = 3*["float"]
SPYCE_ARGNAMES   ["drdlat"] = ["radius", "lon", "lat"]
SPYCE_RETURNS    ["drdlat"] = ["float[3,3]"]
SPYCE_RETNAMES   ["drdlat"] = ["jacobi"]
SPYCE_ABSTRACT   ["drdlat"] = """
Compute the Jacobian of the transformation from latitudinal to
rectangular coordinates.
"""
SPYCE_DEFINITIONS["drdlat"] = {
"radius": "Distance of a point from the origin.",
"lon": "Angle of the point from the XZ plane in radians.",
"lat": "Angle of the point from the XY plane in radians.",
"jacobi": "Matrix of partial derivatives.",
}
SPYCE_URL["drdlat"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/drdlat_c.html"

#########################################
SPYCE_SIGNATURES ["drdpgr"] = ["body_name"] + 5*["float"]
SPYCE_ARGNAMES   ["drdpgr"] = ["body", "lon", "lat", "alt", "re", "f"]
SPYCE_RETURNS    ["drdpgr"] = ["float[3,3]"]
SPYCE_RETNAMES   ["drdpgr"] = ["jacobi"]
SPYCE_ABSTRACT   ["drdpgr"] = """
This routine computes the Jacobian matrix of the transformation from
planetographic to rectangular coordinates.
"""
SPYCE_DEFINITIONS["drdpgr"] = {
"body": "Name of body with which coordinates are associated.",
"lon": "Planetographic longitude of a point (radians).",
"lat": "Planetographic latitude of a point (radians).",
"alt": "Altitude of a point above reference spheroid.",
"re": "Equatorial radius of the reference spheroid.",
"f": "Flattening coefficient.",
"jacobi": "Matrix of partial derivatives.",
}
SPYCE_URL["drdpgr"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/drdpgr_c.html"

#########################################
SPYCE_SIGNATURES ["drdsph"] = 3*["float"]
SPYCE_ARGNAMES   ["drdsph"] = ["r", "colat", "lon"]
SPYCE_RETURNS    ["drdsph"] = ["float[3,3]"]
SPYCE_RETNAMES   ["drdsph"] = ["jacobi"]
SPYCE_ABSTRACT   ["drdsph"] = """
This routine computes the Jacobian of the transformation from spherical
to rectangular coordinates.
"""
SPYCE_DEFINITIONS["drdsph"] = {
"r": "Distance of a point from the origin.",
"colat": "Angle of the point from the positive z-axis.",
"lon": "Angle of the point from the xy plane.",
"jacobi": "Matrix of partial derivatives.",
}
SPYCE_URL["drdsph"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/drdsph_c.html"

#########################################
SPYCE_SIGNATURES ["dsphdr"] = 3*["float"]
SPYCE_ARGNAMES   ["dsphdr"] = ["x", "y", "z"]
SPYCE_RETURNS    ["dsphdr"] = ["float[3,3]"]
SPYCE_RETNAMES   ["dsphdr"] = ["jacobi"]
SPYCE_ABSTRACT   ["dsphdr"] = """
This routine computes the Jacobian of the transformation from
rectangular to spherical coordinates.
"""
SPYCE_DEFINITIONS["dsphdr"] = {
"x": "x-coordinate of point.",
"y": "y-coordinate of point.",
"z": "z-coordinate of point.",
"jacobi": "Matrix of partial derivatives.",
}
SPYCE_URL["dsphdr"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dsphdr_c.html"

#########################################
SPYCE_SIGNATURES ["dtpool"] = ["string"]
SPYCE_ARGNAMES   ["dtpool"] = ["name"]
SPYCE_RETURNS    ["dtpool"] = ["bool", "int", "string"]
SPYCE_RETNAMES   ["dtpool"] = ["found", "n", "vtype"]
SPYCE_ABSTRACT   ["dtpool"] = """
Return the data about a kernel pool variable.
"""
SPYCE_DEFINITIONS["dtpool"] = {
"name": "Name of the variable whose value is to be returned.",
"found": "True if variable is in pool.",
"n": "Number of values returned for name.",
"vtype": "Type of the variable: \"C\", \"N\", or \"X\"",
}
SPYCE_URL["dtpool"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dtpool_c.html"

SPYCE_SIGNATURES ["dtpool_error"] = ["string"]
SPYCE_ARGNAMES   ["dtpool_error"] = ["name"]
SPYCE_RETURNS    ["dtpool_error"] = ["int", "string"]
SPYCE_RETNAMES   ["dtpool_error"] = ["n", "vtype"]
SPYCE_ABSTRACT   ["dtpool_error"] = """
Return the data about a kernel pool variable.
"""
SPYCE_DEFINITIONS["dtpool_error"] = {
"name": "Name of the variable whose value is to be returned.",
"n": "Number of values returned for name.",
"vtype": "Type of the variable: \"C\", \"N\", or \"X\"",
}
SPYCE_PS ["dtpool_error"] = "Raise SPICE(VARIABLENOTFOUND) if the requested variable is not in the kernel pool."
SPYCE_URL["dtpool_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dtpool_c.html"

#########################################
SPYCE_SIGNATURES ["ducrss"] = 2*["float[6]"]
SPYCE_ARGNAMES   ["ducrss"] = ["s1", "s2"]
SPYCE_RETURNS    ["ducrss"] = ["float[6]"]
SPYCE_RETNAMES   ["ducrss"] = ["sout"]
SPYCE_ABSTRACT   ["ducrss"] = """
Compute the unit vector parallel to the cross product of two
3-dimensional vectors and the derivative of this unit vector.
"""
SPYCE_DEFINITIONS["ducrss"] = {
"s1": "Left hand state for cross product and derivative.",
"s2": "Right hand state for cross product and derivative.",
"sout": "Unit vector and derivative of the cross product.",
}
SPYCE_URL["ducrss"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ducrss_c.html"

#########################################
SPYCE_SIGNATURES ["dvcrss"] = 2*["float[6]"]
SPYCE_ARGNAMES   ["dvcrss"] = ["s1", "s2"]
SPYCE_RETURNS    ["dvcrss"] = ["float[6]"]
SPYCE_RETNAMES   ["dvcrss"] = ["sout"]
SPYCE_ABSTRACT   ["dvcrss"] = """
Compute the cross product of two 3-dimensional vectors and the
derivative of this cross product.
"""
SPYCE_DEFINITIONS["dvcrss"] = {
"s1": "Left hand state for cross product and derivative.",
"s2": "Right hand state for cross product and derivative.",
"sout": "State associated with cross product of positions.",
}
SPYCE_URL["dvcrss"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dvcrss_c.html"

#########################################
SPYCE_SIGNATURES ["dvdot"] = 2*["float[6]"]
SPYCE_ARGNAMES   ["dvdot"] = ["s1", "s2"]
SPYCE_RETURNS    ["dvdot"] = ["float[6]"]
SPYCE_RETNAMES   ["dvdot"] = ["value"]
SPYCE_ABSTRACT   ["dvdot"] = """
Compute the derivative of the dot product of two double precision
position vectors.
"""
SPYCE_DEFINITIONS["dvdot"] = {
"s1": "First state vector in the dot product.",
"s2": "Second state vector in the dot product.",
"value": "The derivative of the dot product <s1,s2>",
}
SPYCE_URL["dvdot"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dvdot_c.html"

#########################################
SPYCE_SIGNATURES ["dvhat"] = ["float[6]"]
SPYCE_ARGNAMES   ["dvhat"] = ["s1"]
SPYCE_RETURNS    ["dvhat"] = ["float"]
SPYCE_RETNAMES   ["dvhat"] = ["sout"]
SPYCE_ABSTRACT   ["dvhat"] = """
Find the unit vector corresponding to a state vector and the derivative
of the unit vector.
"""
SPYCE_DEFINITIONS["dvhat"] = {
"s1": "State to be normalized.",
"sout": "Unit vector s1 / |s1|, and its time derivative.",
}
SPYCE_URL["dvhat"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dvhat_c.html"

#########################################
SPYCE_SIGNATURES ["dvnorm"] = ["float[6]"]
SPYCE_ARGNAMES   ["dvnorm"] = ["state"]
SPYCE_RETURNS    ["dvnorm"] = ["float[6]"]
SPYCE_RETNAMES   ["dvnorm"] = ["value"]
SPYCE_ABSTRACT   ["dvnorm"] = """
Function to calculate the derivative of the norm of a 3-vector.
"""
SPYCE_DEFINITIONS["dvnorm"] = {
"state": "A 6-vector composed of three coordinates and their derivatives.",
"value": "derivative of the norm",
}
SPYCE_URL["dvnorm"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dvnorm_c.html"

#########################################
SPYCE_SIGNATURES ["dvpool"] = ["string"]
SPYCE_ARGNAMES   ["dvpool"] = ["name"]
SPYCE_RETURNS    ["dvpool"] = []
SPYCE_RETNAMES   ["dvpool"] = []
SPYCE_ABSTRACT   ["dvpool"] = """
Delete a variable from the kernel pool.
"""
SPYCE_DEFINITIONS["dvpool"] = {
"name": "Name of the kernel variable to be deleted.",
}
SPYCE_URL["dvpool"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dvpool_c.html"

#########################################
SPYCE_SIGNATURES ["dvsep"] = 2*["float[6]"]
SPYCE_ARGNAMES   ["dvsep"] = ["s1", "s2"]
SPYCE_RETURNS    ["dvsep"] = ["float"]
SPYCE_RETNAMES   ["dvsep"] = ["value"]
SPYCE_ABSTRACT   ["dvsep"] = """
Calculate the time derivative of the separation angle between two input
states, S1 and S2.
"""
SPYCE_DEFINITIONS["dvsep"] = {
"s1": "State vector of the first body",
"s2": "State vector of the second  body",
"value": "derivate of the separation angle between state vectors.",
}
SPYCE_URL["dvsep"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dvsep_c.html"

#########################################
SPYCE_SIGNATURES ["edlimb"] = 3*["float"] + ["float[3]"]
SPYCE_ARGNAMES   ["edlimb"] = ["a", "b", "c", "viewpt"]
SPYCE_RETURNS    ["edlimb"] = ["float[9]"]
SPYCE_RETNAMES   ["edlimb"] = ["limb"]
SPYCE_ABSTRACT   ["edlimb"] = """
Find the limb of a triaxial ellipsoid, viewed from a specified point.
"""
SPYCE_DEFINITIONS["edlimb"] = {
"a": "Length of ellipsoid semi-axis lying on the x-axis.",
"b": "Length of ellipsoid semi-axis lying on the y-axis.",
"c": "Length of ellipsoid semi-axis lying on the z-axis.",
"viewpt": "Location of viewing point.",
"limb": "Limb of ellipsoid as seen from viewing point.",
}
SPYCE_URL["edlimb"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/edlimb_c.html"

#########################################
SPYCE_SIGNATURES ["edterm"] = ["string", "body_name", "body_name", "time", "frame_name", "string", "body_name", "int"]
SPYCE_ARGNAMES   ["edterm"] = ["trmtyp", "source", "target", "et", "fixref", "abcorr", "obsrvr", "npts"]
SPYCE_RETURNS    ["edterm"] = ["time", "float[3]", "float[*,3]"]
SPYCE_RETNAMES   ["edterm"] = ["trgepc", "obspos", "trmpts"]
SPYCE_ABSTRACT   ["edterm"] = """
Compute a set of points on the umbral or penumbral terminator of a
specified target body, where the target shape is modeled as an
ellipsoid.
"""
SPYCE_DEFINITIONS["edterm"] = {
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
SPYCE_URL["edterm"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/edterm_c.html"

#########################################
SPYCE_SIGNATURES ["el2cgv"] = ["float[9]"]
SPYCE_ARGNAMES   ["el2cgv"] = ["ellipse"]
SPYCE_RETURNS    ["el2cgv"] = 3*["float[3]"]
SPYCE_RETNAMES   ["el2cgv"] = ["center", "smajor", "sminor"]
SPYCE_ABSTRACT   ["el2cgv"] = """
Convert a CSPICE ellipse to a center vector and two generating vectors.
The selected generating vectors are semi-axes of the ellipse.
"""
SPYCE_DEFINITIONS["el2cgv"] = {
"ellipse": "A CSPICE ellipse.",
"center": "Center of ellipse.",
"smajor": "Semi-major axis of ellipse.",
"sminor": "Semi-minor axes of ellipse.",
}
SPYCE_URL["el2cgv"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/el2cgv_c.html"

#########################################
SPYCE_SIGNATURES ["eqncpv"] = ["time", "time", "float[9]", "float", "float"]
SPYCE_ARGNAMES   ["eqncpv"] = ["et", "epoch", "eqel", "rapol", "decpol"]
SPYCE_RETURNS    ["eqncpv"] = ["float[6]"]
SPYCE_RETNAMES   ["eqncpv"] = ["state"]
SPYCE_ABSTRACT   ["eqncpv"] = """
Compute the state (position and velocity of an object whose trajectory
is described via equinoctial elements relative to some fixed plane
(usually the equatorial plane of some planet).
"""
SPYCE_DEFINITIONS["eqncpv"] = {
"et": "Epoch in seconds past J2000 to find state",
"epoch": "Epoch of elements in seconds past J2000",
"eqel": "Array of equinoctial elements",
"rapol": "Right Ascension of the pole of the reference plane",
"decpol": "Declination of the pole of the reference plane",
"state": "State of the object described by eqel.",
}
SPYCE_URL["eqncpv"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/eqncpv_c.html"

#########################################
SPYCE_SIGNATURES ["erract"] = ["string", "string"]
SPYCE_ARGNAMES   ["erract"] = ["op", "action"]
SPYCE_DEFAULTS  ["erract"] = ["GET", ""]
SPYCE_RETURNS    ["erract"] = ["string"]
SPYCE_RETNAMES   ["erract"] = ["action2"]
SPYCE_ABSTRACT   ["erract"] = """
Retrieve or set the default error action.
"""
SPYCE_DEFINITIONS["erract"] = {
"op": "Operation: \"GET\" or \"SET\"; default is \"GET\".",
"action": "Error response action for \"SET\"; ignored on \"GET\". Options are \"ABORT\", \"REPORT\", \"RETURN\", \"IGNORE\", \"DEFAULT\", \"EXCEPTION\", or \"RUNTIME\" to use the Python exception system.",
"action2": "Current or new error response action.",
}
SPYCE_PS ["erract"] = "As a special case, if a single argument is provided and it is one of the allowed actions, then \"SET\" is assumed and the argument is interpreted as the action."
SPYCE_URL["erract"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/erract_c.html"

#########################################
SPYCE_SIGNATURES ["errch"] = 2*["string"]
SPYCE_ARGNAMES   ["errch"] = ["marker", "string"]
SPYCE_RETURNS    ["errch"] = []
SPYCE_RETNAMES   ["errch"] = []
SPYCE_ABSTRACT   ["errch"] = """
Substitute a character string for the first occurrence of a marker in
the current long error message.
"""
SPYCE_DEFINITIONS["errch"] = {
"marker": "A substring of the error message to be replaced.",
"string": "The character string to substitute for marker.",
}
SPYCE_URL["errch"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/errch_c.html"

#########################################
SPYCE_SIGNATURES ["errdev"] = ["string", "string"]
SPYCE_ARGNAMES   ["errdev"] = ["op", "device"]
SPYCE_DEFAULTS  ["errdev"] = ["GET", ""]
SPYCE_RETURNS    ["errdev"] = ["string"]
SPYCE_RETNAMES   ["errdev"] = ["device2"]
SPYCE_ABSTRACT   ["errdev"] = """
Retrieve or set the name of the current output device for error
messages.
"""
SPYCE_DEFINITIONS["errdev"] = {
"op": "The operation: \"GET\" or \"SET\"; default is \"GET\".",
"device": "The device name; ignored on \"GET\". Options are a file name, \"SCREEN\" and \"NULL\".",
"device2": "Current or new output device.",
}
SPYCE_PS ["erract"] = "As a special case, if a single argument is provided, \"SET\" is assumed and the argument is interpreted as the device."
SPYCE_URL["errdev"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/errdev_c.html"

#########################################
SPYCE_SIGNATURES ["errdp"] = ["string", "float"]
SPYCE_ARGNAMES   ["errdp"] = ["marker", "number"]
SPYCE_RETURNS    ["errdp"] = []
SPYCE_RETNAMES   ["errdp"] = []
SPYCE_ABSTRACT   ["errdp"] = """
Substitute a double precision number for the first occurrence of a
marker found in the current long error message.
"""
SPYCE_DEFINITIONS["errdp"] = {
"marker": "A substring of the error message to be replaced.",
"number": "The d.p. number to substitute for marker.",
}
SPYCE_URL["errdp"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/errdp_c.html"

#########################################
SPYCE_SIGNATURES ["errint"] = ["string", "int"]
SPYCE_ARGNAMES   ["errint"] = ["marker", "number"]
SPYCE_RETURNS    ["errint"] = []
SPYCE_RETNAMES   ["errint"] = []
SPYCE_ABSTRACT   ["errint"] = """
Substitute an integer for the first occurrence of a marker found in the
current long error message.
"""
SPYCE_DEFINITIONS["errint"] = {
"marker": "A substring of the error message to be replaced.",
"number": "The integer to substitute for marker.",
}
SPYCE_URL["errint"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/errint_c.html"

#########################################
SPYCE_SIGNATURES ["errprt"] = ["string", "string"]
SPYCE_ARGNAMES   ["errprt"] = ["op", "list"]
SPYCE_DEFAULTS  ["errprt"] = ["GET", ""]
SPYCE_RETURNS    ["errprt"] = ["string"]
SPYCE_RETNAMES   ["errprt"] = ["list2"]
SPYCE_ABSTRACT   ["errprt"] = """
Retrieve or set the list of error message items to be output when an
error is detected.
"""
SPYCE_DEFINITIONS["errprt"] = {
"op": "The operation: \"GET\" or \"SET\"; default is \"GET\"",
"list": "Specification of error messages to be output on \"SET\"; ignored on \"GET\". Options are \"SHORT\", \"LONG\", \"EXPLAIN\", \"TRACEBACK\", \"ALL\", \"NONE\" and \"DEFAULT\". Specified options add to current set; use \"NONE\" to clear and start over.",
"list2": "The current or new list.",
}

SPYCE_PS ["errprt"] = "As a special case, if a single argument is provided and is not \"GET\", then \"SET\" is assumed and this argument is interpreted as the list."
SPYCE_URL["errprt"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/errprt_c.html"

#########################################
SPYCE_SIGNATURES ["et2lst"] = ["time", "body_code", "float", "string"]
SPYCE_ARGNAMES   ["et2lst"] = ["et", "body", "lon", "type"]
SPYCE_RETURNS    ["et2lst"] = 3*["float"] + 2*["string"]
SPYCE_RETNAMES   ["et2lst"] = ["hr", "mn", "sc", "time", "ampm"]
SPYCE_ABSTRACT   ["et2lst"] = """
Given an ephemeris epoch, compute the local solar time for an object on
the surface of a body at a specified longitude.
"""
SPYCE_DEFINITIONS["et2lst"] = {
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
SPYCE_URL["et2lst"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/et2lst_c.html"

#########################################
SPYCE_SIGNATURES ["et2utc"] = ["time", "string", "int"]
SPYCE_ARGNAMES   ["et2utc"] = ["et", "format", "prec"]
SPYCE_RETURNS    ["et2utc"] = ["string"]
SPYCE_RETNAMES   ["et2utc"] = ["utcstr"]
SPYCE_ABSTRACT   ["et2utc"] = """
Convert an input time from ephemeris seconds past J2000 to Calendar,
Day-of-Year, or Julian Date format, UTC.
"""
SPYCE_DEFINITIONS["et2utc"] = {
"et": "Input epoch, given in ephemeris seconds past J2000.",
"format": "Format of output epoch: \"C\" for calendar format; \"D\" for day-of-year format; \"J\" for Julian date; \"ISOC\" for ISO calendar format; \"ISOD\" for ISO day-of-year format.",
"prec": "Digits of precision in fractional seconds or days.",
"utcstr": "Output time string, UTC.",
}
SPYCE_URL["et2utc"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/et2utc_c.html"

#########################################
SPYCE_SIGNATURES ["etcal"] = ["time"]
SPYCE_ARGNAMES   ["etcal"] = ["et"]
SPYCE_RETURNS    ["etcal"] = ["string"]
SPYCE_RETNAMES   ["etcal"] = ["string"]
SPYCE_ABSTRACT   ["etcal"] = """
Convert from an ephemeris epoch measured in seconds past the epoch of
J2000 to a calendar string format using a formal calendar free of
leapseconds.
"""
SPYCE_DEFINITIONS["etcal"] = {
"et": "Ephemeris time measured in seconds past J2000.",
"string": "A standard calendar representation of et.",
}
SPYCE_URL["etcal"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/etcal_c.html"

#########################################
SPYCE_SIGNATURES ["eul2m"] = 3*["float"] + 3*["int"]
SPYCE_ARGNAMES   ["eul2m"] = ["angle3", "angle2", "angle1", "axis3", "axis2", "axis1"]
SPYCE_RETURNS    ["eul2m"] = ["rotmat[3,3]"]
SPYCE_RETNAMES   ["eul2m"] = ["rotmat"]
SPYCE_ABSTRACT   ["eul2m"] = """
Construct a rotation matrix from a set of Euler angles.
"""
SPYCE_DEFINITIONS["eul2m"] = {
"angle3": "Rotation angle about the third axis (radians).",
"angle2": "Rotation angle about the second axis (radians).",
"angle1": "Rotation angles about the first axis (radians).",
"axis3" : "Axis number (1,2, or 3) of the third rotation axis.",
"axis2" : "Axis number (1,2, or 3) of the second rotation axis.",
"axis1" : "Axis number (1,2, or 3) of the first rotation axis.",
"rotmat": "Product of the 3 rotations.",
}
SPYCE_URL["eul2m"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/eul2m_c.html"

#########################################
SPYCE_SIGNATURES ["eul2xf"] = ["float[6]"] + 3*["int"]
SPYCE_ARGNAMES   ["eul2xf"] = ["eulang", "axisa", "axisb", "axisc"]
SPYCE_RETURNS    ["eul2xf"] = ["rotmat[6,6]"]
SPYCE_RETNAMES   ["eul2xf"] = ["xform"]
SPYCE_ABSTRACT   ["eul2xf"] = """
This routine computes a state transformation from an Euler angle
factorization of a rotation and the derivatives of those Euler angles.
"""
SPYCE_DEFINITIONS["eul2xf"] = {
"eulang": "An array of Euler angles and their derivatives.",
"axisa": "Axis A of the Euler angle factorization.",
"axisb": "Axis B of the Euler angle factorization.",
"axisc": "Axis C of the Euler angle factorization.",
"xform": "A state transformation matrix.",
}
SPYCE_URL["eul2xf"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/eul2xf_c.html"

#########################################
SPYCE_SIGNATURES ["expool"] = ["string"]
SPYCE_ARGNAMES   ["expool"] = ["name"]
SPYCE_RETURNS    ["expool"] = ["bool"]
SPYCE_RETNAMES   ["expool"] = ["found"]
SPYCE_ABSTRACT   ["expool"] = """
Confirm the existence of a kernel variable in the kernel pool.
"""
SPYCE_DEFINITIONS["expool"] = {
"name": "Name of the variable whose value is to be returned.",
"found": "True if the variable is in the pool; False othewise.",
}
SPYCE_URL["expool"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/expool_c.html"

#########################################
SPYCE_SIGNATURES ["failed"] = []
SPYCE_ARGNAMES   ["failed"] = []
SPYCE_RETURNS    ["failed"] = ["bool"]
SPYCE_RETNAMES   ["failed"] = ["value"]
SPYCE_ABSTRACT   ["failed"] = """
True if an error condition has been signalled via sigerr. failed is the
CSPICE status indicator.
"""
SPYCE_DEFINITIONS["failed"] = {
"value": "True if an error condition was detected; it is False otherwise.",
}
SPYCE_URL["failed"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/failed_c.html"

#########################################
SPYCE_SIGNATURES ["fovray"] = ["string", "float[3]", "frame_name", "string", "body_name", "time"]
SPYCE_ARGNAMES   ["fovray"] = ["inst", "raydir", "rframe", "abcorr", "observer", "et"]
SPYCE_RETURNS    ["fovray"] = ["bool"]
SPYCE_RETNAMES   ["fovray"] = ["visible"]
SPYCE_ABSTRACT   ["fovray"] = """
Determine if a specified ray is within the field-of-view (FOV) of a
specified instrument at a given time.
"""
SPYCE_DEFINITIONS["fovray"] = {
"inst": "Name or ID code string of the instrument.",
"raydir": "Ray's direction vector.",
"rframe": "Body-fixed, body-centered frame for target body.",
"abcorr": "Aberration correction, \"NONE\", \"LT\", \"LT+S\", \"CN\", or \"CN+S\".",
"observer": "Name or ID code string of the observer.",
"et": "Time of the observation (seconds past J2000).",
"visible": "Visibility flag (True/False).",
}
SPYCE_URL["fovray"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/fovray_c.html"

#########################################
SPYCE_SIGNATURES ["fovtrg"] = ["string", "body_name", "string", "frame_name", "string", "body_name", "time"]
SPYCE_ARGNAMES   ["fovtrg"] = ["inst", "target", "tshape", "tframe", "abcorr", "obsrvr", "et"]
SPYCE_RETURNS    ["fovtrg"] = ["bool"]
SPYCE_RETNAMES   ["fovtrg"] = ["visible"]
SPYCE_ABSTRACT   ["fovtrg"] = """
Determine if a specified ephemeris object is within the field-of-view
(FOV) of a specified instrument at a given time.
"""
SPYCE_DEFINITIONS["fovtrg"] = {
"inst": "Name or ID code string of the instrument.",
"target": "Name or ID code string of the target.",
"tshape": "Type of shape model used for the target.",
"tframe": "Body-fixed, body-centered frame for target body.",
"abcorr": "Aberration correction, \"NONE\", \"LT\", \"LT+S\", \"CN\", or \"CN+S\".",
"obsrvr": "Name or ID code string of the observer.",
"et": "Time of the observation (seconds past J2000).",
"visible": "Visibility flag (True/False).",
}
SPYCE_URL["fovtrg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/fovtrg_c.html"

#########################################
SPYCE_SIGNATURES ["frame"] = ["float[3]"]
SPYCE_ARGNAMES   ["frame"] = ["xin"]
SPYCE_RETURNS    ["frame"] = 3*["float[3]"]
SPYCE_RETNAMES   ["frame"] = ["x", "y", "z"]
SPYCE_ABSTRACT   ["frame"] = """
Given a vector x, this routine builds a right handed orthonormal frame
x,y,z where the output x is parallel to the input x.
"""
SPYCE_DEFINITIONS["frame"] = {
"xin": "Input vector.",
"x": "A unit vector parallel to xin.",
"y": "Unit vector in the plane orthogonal to x.",
"z": "Unit vector given by x X y.",
}
SPYCE_URL["frame"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/frame_c.html"

#########################################
SPYCE_SIGNATURES ["frinfo"] = ["frame_code"]
SPYCE_ARGNAMES   ["frinfo"] = ["frcode"]
SPYCE_RETURNS    ["frinfo"] = 3*["int"] + ["bool"]
SPYCE_RETNAMES   ["frinfo"] = ["cent", "frclss", "clssid", "found"]
SPYCE_ABSTRACT   ["frinfo"] = """
Retrieve the minimal attributes associated with a frame needed for
converting transformations to and from it.
"""
SPYCE_DEFINITIONS["frinfo"] = {
"frcode": "the idcode for some frame",
"cent": "the center of the frame",
"frclss": "the class (type) of the frame",
"clssid": "the idcode for the frame within its class.",
"found": "True if the requested information is available.",
}
SPYCE_URL["frinfo"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/frinfo_c.html"

SPYCE_SIGNATURES ["frinfo_error"] = ["frame_code"]
SPYCE_ARGNAMES   ["frinfo_error"] = ["frcode"]
SPYCE_RETURNS    ["frinfo_error"] = 3*["int"]
SPYCE_RETNAMES   ["frinfo_error"] = ["cent", "frclss", "clssid"]
SPYCE_ABSTRACT   ["frinfo_error"] = """
Retrieve the minimal attributes associated with a frame needed for
converting transformations to and from it.
"""
SPYCE_DEFINITIONS["frinfo_error"] = {
"frcode": "the idcode for some frame",
"cent"  : "the center of the frame",
"frclss": "the class (type) of the frame",
"clssid": "the idcode for the frame within its class.",
}
SPYCE_PS ["frinfo_error"] = "Raise SPICE(FRAMEIDNOTFOUND) condition if the requested information is unavailable."
SPYCE_URL["frinfo_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/frinfo_c.html"

#########################################
SPYCE_SIGNATURES ["frmchg"] = ["frame_code", "frame_code", "time"]
SPYCE_ARGNAMES   ["frmchg"] = ["frame1", "frame2", "et"]
SPYCE_RETURNS    ["frmchg"] = ["rotmat[6,6]"]
SPYCE_RETNAMES   ["frmchg"] = ["xform"]
SPYCE_ABSTRACT   ["frmchg"] = """
Return the state transformation matrix from one frame to another.
"""
SPYCE_DEFINITIONS["frmchg"] = {
"frame1": "the frame id-code for some reference frame",
"frame2": "the frame id-code for some reference frame",
"et"    : "an epoch in TDB seconds past J2000.",
"xform" : "a state transformation matrix",
}
SPYCE_URL["frmchg"] = ""

#########################################
SPYCE_SIGNATURES ["frmnam"] = ["frame_code"]
SPYCE_ARGNAMES   ["frmnam"] = ["frcode"]
SPYCE_RETURNS    ["frmnam"] = ["frame_name"]
SPYCE_RETNAMES   ["frmnam"] = ["frname"]
SPYCE_ABSTRACT   ["frmnam"] = """
Retrieve the name of a reference frame associated with a SPICE ID code.
"""
SPYCE_DEFINITIONS["frmnam"] = {
"frcode": "an integer code for a reference frame",
"frname": "the name associated with the reference frame; blank on error.",
}
SPYCE_URL["frmnam"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/frmnam_c.html"

SPYCE_SIGNATURES ["frmnam_error"] = ["frame_code"]
SPYCE_ARGNAMES   ["frmnam_error"] = ["frcode"]
SPYCE_RETURNS    ["frmnam_error"] = ["frame_name"]
SPYCE_RETNAMES   ["frmnam_error"] = ["frname"]
SPYCE_ABSTRACT   ["frmnam_error"] = """
Retrieve the name of a reference frame associated with a SPICE ID code.
"""
SPYCE_DEFINITIONS["frmnam_error"] = {
"frcode": "an integer code for a reference frame",
"frname": "the name associated with the reference frame.",
}
SPYCE_PS ["frmnam_error"] = "Raise SPICE(FRAMEIDNOTFOUND) if not found."
SPYCE_URL["frmnam_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/frmnam_c.html"

#########################################
SPYCE_SIGNATURES ["furnsh"] = ["string"]
SPYCE_ARGNAMES   ["furnsh"] = ["file"]
SPYCE_RETURNS    ["furnsh"] = []
SPYCE_RETNAMES   ["furnsh"] = []
SPYCE_ABSTRACT   ["furnsh"] = """
Load one or more SPICE kernels into a program.
"""
SPYCE_DEFINITIONS["furnsh"] = {
"file": "Name of SPICE kernel file.",
}
SPYCE_URL["furnsh"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/furnsh_c.html"

#########################################
SPYCE_SIGNATURES ["gcpool"] = ["string", "int"]
SPYCE_ARGNAMES   ["gcpool"] = ["name", "start"]
SPYCE_DEFAULTS   ["gcpool"] = [0]
SPYCE_RETURNS    ["gcpool"] = ["string[*]", "bool"]
SPYCE_RETNAMES   ["gcpool"] = ["cvals", "found"]
SPYCE_ABSTRACT   ["gcpool"] = """
Return the character value of a kernel variable from the kernel pool.
"""
SPYCE_DEFINITIONS["gcpool"] = {
"name" : "Name of the variable whose value is to be returned.",
"start": "Which component to start retrieving for name; default is 0.",
"cvals": "Values associated with name.",
"found": "True if variable is in pool.",
}
SPYCE_URL["gcpool"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gcpool_c.html"

SPYCE_SIGNATURES ["gcpool_error"] = ["string", "int"]
SPYCE_ARGNAMES   ["gcpool_error"] = ["name", "start"]
SPYCE_RETURNS    ["gcpool_error"] = ["string[*]"]
SPYCE_RETNAMES   ["gcpool_error"] = ["cvals"]
SPYCE_ABSTRACT   ["gcpool_error"] = """
Return the character value of a kernel variable from the kernel pool.
"""
SPYCE_DEFINITIONS["gcpool_error"] = {
"name" : "Name of the variable whose value is to be returned.",
"start": "Which component to start retrieving for name; default is 0.",
"cvals": "Values associated with name.",
}
SPYCE_PS ["gcpool_error"] = "Raise a SPICE error condition if the variable is not in the pool, if it has the wrong type, or if the start index is out of range."
SPYCE_URL["gcpool_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gcpool_c.html"

#########################################
SPYCE_SIGNATURES ["gdpool"] = ["string", "int"]
SPYCE_ARGNAMES   ["gdpool"] = ["name", "start"]
SPYCE_DEFAULTS   ["gdpool"] = [0]
SPYCE_RETURNS    ["gdpool"] = ["float[*]", "bool"]
SPYCE_RETNAMES   ["gdpool"] = ["values", "found"]
SPYCE_ABSTRACT   ["gdpool"] = """
Return the float value of a kernel variable from the kernel pool.
"""
SPYCE_DEFINITIONS["gdpool"] = {
"name" : "Name of the variable whose value is to be returned.",
"start": "Which component to start retrieving for name; default is 0.",
"values": "Values associated with name.",
"found": "True if variable is in pool.",
}
SPYCE_URL["gdpool"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gdpool_c.html"

SPYCE_SIGNATURES ["gdpool_error"] = ["string", "int"]
SPYCE_ARGNAMES   ["gdpool_error"] = ["name", "start"]
SPYCE_DEFAULTS   ["gdpool_error"] = [0]
SPYCE_RETURNS    ["gdpool_error"] = ["float[*]"]
SPYCE_RETNAMES   ["gdpool_error"] = ["values"]
SPYCE_ABSTRACT   ["gdpool_error"] = """
Return the float value of a kernel variable from the kernel pool.
"""
SPYCE_DEFINITIONS["gdpool_error"] = {
"name"  : "Name of the variable whose value is to be returned.",
"start" : "Which component to start retrieving for name; default is 0.",
"values": "Values associated with name.",
}
SPYCE_PS ["gdpool_error"] = "Raise a SPICE error condition if the variable is not in the pool, if it has the wrong type, or if the start index is out of range."
SPYCE_URL["gdpool_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gdpool_c.html"

#########################################
SPYCE_SIGNATURES ["georec"] = 5*["float"]
SPYCE_ARGNAMES   ["georec"] = ["lon", "lat", "alt", "re", "f"]
SPYCE_RETURNS    ["georec"] = ["float[3]"]
SPYCE_RETNAMES   ["georec"] = ["rectan"]
SPYCE_ABSTRACT   ["georec"] = """
Convert geodetic coordinates to rectangular coordinates.
"""
SPYCE_DEFINITIONS["georec"] = {
"lon": "Geodetic longitude of point (radians).",
"lat": "Geodetic latitude  of point (radians).",
"alt": "Altitude of point above the reference spheroid.",
"re" : "Equatorial radius of the reference spheroid.",
"f"  : "Flattening coefficient.",
"rectan": "Rectangular coordinates of point.",
}
SPYCE_URL["georec"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/georec_c.html"

#########################################
SPYCE_SIGNATURES ["getfov"] = ["int"]
SPYCE_ARGNAMES   ["getfov"] = ["instid"]
SPYCE_RETURNS    ["getfov"] = ["string", "string", "float[3]", "float[*,3]"]
SPYCE_RETNAMES   ["getfov"] = ["shape", "frame", "bsight", "bounds"]
SPYCE_ABSTRACT   ["getfov"] = """
This subroutine returns the field-of-view (FOV) configuration for a
specified instrument.
"""
SPYCE_DEFINITIONS["getfov"] = {
"instid": "NAIF ID of an instrument.",
"shape" : "Instrument FOV shape.",
"frame" : "Name of the frame in which FOV vectors are defined.",
"bsight": "Boresight vector.",
"bounds": "FOV boundary vectors.",
}
SPYCE_URL["getfov"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/getfov_c.html"

#########################################
SPYCE_SIGNATURES ["getmsg"] = ["string"]
SPYCE_ARGNAMES   ["getmsg"] = ["option"]
SPYCE_RETURNS    ["getmsg"] = ["string"]
SPYCE_RETNAMES   ["getmsg"] = ["msg"]
SPYCE_ABSTRACT   ["getmsg"] = """
Retrieve the current short error message, the explanation of the short
error message, or the long error message.
"""
SPYCE_DEFINITIONS["getmsg"] = {
"option": "Indicates type of error message, \"SHORT\", \"LONG\", or \"EXPLAIN\".",
"msg"   : "The error message to be retrieved.",
}
SPYCE_URL["getmsg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/getmsg_c.html"

#########################################
SPYCE_SIGNATURES ["gipool"] = ["string", "int"]
SPYCE_ARGNAMES   ["gipool"] = ["name", "start"]
SPYCE_DEFAULTS   ["gipool"] = [0]
SPYCE_RETURNS    ["gipool"] = ["int[*]", "bool"]
SPYCE_RETNAMES   ["gipool"] = ["ivals", "found"]
SPYCE_ABSTRACT   ["gipool"] = """
Return the integer value of a kernel variable from the kernel pool.
"""
SPYCE_DEFINITIONS["gipool"] = {
"name": "Name of the variable whose value is to be returned.",
"start": "Which component to start retrieving for name; default is 0.",
"ivals": "Values associated with name.",
"found": "True if variable is in pool.",
}
SPYCE_URL["gipool"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gipool_c.html"

SPYCE_SIGNATURES ["gipool_error"] = ["string", "int"]
SPYCE_ARGNAMES   ["gipool_error"] = ["name", "start"]
SPYCE_DEFAULTS   ["gipool_error"] = [0]
SPYCE_RETURNS    ["gipool_error"] = ["int[*]"]
SPYCE_RETNAMES   ["gipool_error"] = ["ivals"]
SPYCE_ABSTRACT   ["gipool_error"] = """
Return the integer value of a kernel variable from the kernel pool.
"""
SPYCE_DEFINITIONS["gipool_error"] = {
"name": "Name of the variable whose value is to be returned.",
"start": "Which component to start retrieving for name; default is 0.",
"ivals": "Values associated with name.",
}
SPYCE_PS ["gipool_error"] = "Raise a SPICE error condition if the variable is not in the pool, if it has the wrong type, or if the start index is out of range."
SPYCE_URL["gipool_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gipool_c.html"

#########################################
SPYCE_SIGNATURES ["gnpool"] = ["string", "int"]
SPYCE_ARGNAMES   ["gnpool"] = ["name", "start"]
SPYCE_DEFAULTS   ["gnpool"] = [0]
SPYCE_RETURNS    ["gnpool"] = ["string[*]", "bool"]
SPYCE_RETNAMES   ["gnpool"] = ["kvars", "found"]
SPYCE_ABSTRACT   ["gnpool"] = """
Return names of kernel variables matching a specified template.
"""
SPYCE_DEFINITIONS["gnpool"] = {
"name": "Template that names should match.",
"start": "Index of first matching name to retrieve; default is 0.",
"kvars": "Kernel pool variables whose names match name.",
"found": "True if variable is in pool.",
}
SPYCE_PS ["gnpool"] = "Raise a SPICE error condition if the variable is not in the pool, if it has the wrong type, or if the start index is out of range."
SPYCE_URL["gnpool"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gnpool_c.html"

SPYCE_SIGNATURES ["gnpool_error"] = ["string", "int"]
SPYCE_ARGNAMES   ["gnpool_error"] = ["name", "start"]
SPYCE_DEFAULTS   ["gnpool_error"] = [0]
SPYCE_RETURNS    ["gnpool_error"] = ["string[*]"]
SPYCE_RETNAMES   ["gnpool_error"] = ["kvars"]
SPYCE_ABSTRACT   ["gnpool_error"] = """
Return names of kernel variables matching a specified template.
"""
SPYCE_DEFINITIONS["gnpool_error"] = {
"name": "Template that names should match.",
"start": "Index of first matching name to retrieve; default is 0.",
"kvars": "Kernel pool variables whose names match name.",
}
SPYCE_PS ["gnpool_error"] = "Raise a SPICE error condition if no variables matching the template are found in the pool, or if the start index is out of range."
SPYCE_URL["gnpool_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gnpool_c.html"

#########################################
SPYCE_SIGNATURES ["halfpi"] = []
SPYCE_ARGNAMES   ["halfpi"] = []
SPYCE_RETURNS    ["halfpi"] = ["float"]
SPYCE_RETNAMES   ["halfpi"] = ["value"]
SPYCE_ABSTRACT   ["halfpi"] = """
Return half the value of pi
"""
SPYCE_DEFINITIONS["halfpi"] = {
"value": "half the value of pi"
}
SPYCE_URL["halfpi"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/halfpi_c.html"

#########################################
SPYCE_SIGNATURES ["ident"] = []
SPYCE_ARGNAMES   ["ident"] = []
SPYCE_RETURNS    ["ident"] = ["rotmat[3,3]"]
SPYCE_RETNAMES   ["ident"] = ["matrix"]
SPYCE_ABSTRACT   ["ident"] = """
Return the 3x3 identity matrix.
"""
SPYCE_DEFINITIONS["ident"] = {
"matrix": "is the 3x3 identity matrix.",
}
SPYCE_URL["ident"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ident_c.html"

#########################################
SPYCE_SIGNATURES ["illum"] = ["body_name", "time", "string", "body_name", "float[3]"]
SPYCE_ARGNAMES   ["illum"] = ["target", "et", "abcorr", "obsrvr", "spoint"]
SPYCE_RETURNS    ["illum"] = 3*["float"]
SPYCE_RETNAMES   ["illum"] = ["phase", "solar", "emissn"]
SPYCE_ABSTRACT   ["illum"] = """
Find the illumination angles at a specified surface point of a target
body.
"""
SPYCE_DEFINITIONS["illum"] = {
"target": "Name of target body.",
"et": "Epoch in ephemeris seconds past J2000.",
"abcorr": "Aberration correction, \"NONE\", \"LT\", \"LT+S\", \"CN\", or \"CN+S\".",
"obsrvr": "Name of observing body.",
"spoint": "Body-fixed coordinates of a target surface point.",
"phase": "Phase angle at the surface point.",
"solar": "Solar incidence angle at the surface point.",
"emissn": "Emission angle at the surface point.",
}
SPYCE_URL["illum"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/illum_c.html"

#########################################
SPYCE_SIGNATURES ["illumf"] = ["string", "body_name", "body_name", "time", "frame_name", "string", "body_name", "float[3]"]
SPYCE_ARGNAMES   ["illumf"] = ["method", "target", "ilusrc", "et", "fixref", "abcorr", "obsrvr", "spoint"]
SPYCE_RETURNS    ["illumf"] = ["float", "float[3]", "float", "float", "float", "bool", "bool"]
SPYCE_RETNAMES   ["illumf"] = ["trgepc", "srfvec", "phase", "incdnc", "emissn", "visibl", "lit"]
SPYCE_ABSTRACT   ["illumf"] = """
Compute the illumination angles---phase, incidence, and emission---at a
specified point on a target body. Return logical flags indicating
whether the surface point is visible from the observer's position and
whether the surface point is illuminated.

The target body's surface is represented using topographic data
provided by DSK files or by a reference ellipsoid.

The illumination source is a specified ephemeris object.
"""
SPYCE_DEFINITIONS["illumf"] = {
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
SPYCE_URL["illumf"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/illumf_c.html"

#########################################
SPYCE_SIGNATURES ["illumg"] = ["string", "body_name", "body_name", "time", "frame_name", "string", "body_name", "float[3]"]
SPYCE_ARGNAMES   ["illumg"] = ["method", "target", "ilusrc", "et", "fixref", "abcorr", "obsrvr", "spoint"]
SPYCE_RETURNS    ["illumg"] = ["float", "float[3]", "float", "float", "float"]
SPYCE_RETNAMES   ["illumg"] = ["trgepc", "srfvec", "phase", "incdnc", "emissn"]
SPYCE_ABSTRACT   ["illumg"] = """
Find the illumination angles (phase, incidence, and emission) at a
specified surface point of a target body.

The surface of the target body may be represented by a triaxial
ellipsoid or by topographic data provided by DSK files.

The illumination source is a specified ephemeris object.
"""
SPYCE_DEFINITIONS["illumg"] = {
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
SPYCE_URL["illumg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/illumg_c.html"

#########################################
SPYCE_SIGNATURES ["ilumin"] = ["string", "body_name", "time", "frame_name", "string", "body_name", "float[3]"]
SPYCE_ARGNAMES   ["ilumin"] = ["method", "target", "et", "fixref", "abcorr", "obsrvr", "spoint"]
SPYCE_RETURNS    ["ilumin"] = ["float", "float[3]", "float", "float", "float"]
SPYCE_RETNAMES   ["ilumin"] = ["trgepc", "srfvec", "phase", "incdnc", "emissn"]
SPYCE_ABSTRACT   ["ilumin"] = """
Find the illumination angles (phase, solar incidence, and emission) at a
specified surface point of a target body.

This routine supersedes illum.
"""
SPYCE_DEFINITIONS["ilumin"] = {
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
SPYCE_URL["ilumin"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ilumin_c.html"

#########################################
SPYCE_SIGNATURES ["inedpl"] = 3*["float"] + ["float[4]"]
SPYCE_ARGNAMES   ["inedpl"] = ["a", "b", "c", "plane"]
SPYCE_RETURNS    ["inedpl"] = ["float[9]", "bool"]
SPYCE_RETNAMES   ["inedpl"] = ["ellipse", "found"]
SPYCE_ABSTRACT   ["inedpl"] = """
Find the intersection of a triaxial ellipsoid and a plane.
"""
SPYCE_DEFINITIONS["inedpl"] = {
"a": "Length of ellipsoid semi-axis lying on the x-axis.",
"b": "Length of ellipsoid semi-axis lying on the y-axis.",
"c": "Length of ellipsoid semi-axis lying on the z-axis.",
"plane": "Plane that intersects ellipsoid.",
"ellipse": "Intersection ellipse, when found is True.",
"found": "Flag indicating whether ellipse was found.",
}
SPYCE_URL["inedpl"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/inedpl_c.html"

#########################################
SPYCE_SIGNATURES ["inelpl"] = ["float[9]", "float[4]"]
SPYCE_ARGNAMES   ["inelpl"] = ["ellips", "plane"]
SPYCE_RETURNS    ["inelpl"] = ["int", "float[3]", "float[3]"]
SPYCE_RETNAMES   ["inelpl"] = ["nxpts", "xpt1", "xpt2"]
SPYCE_ABSTRACT   ["inelpl"] = """
Find the intersection of an ellipse and a plane.
"""
SPYCE_DEFINITIONS["inelpl"] = {
"ellips": "A CSPICE ellipse.",
"plane": "A CSPICE plane.",
"nxpts": "Number of intersection points of plane and ellipse.",
"xpt1": "First intersection point.",
"xpt2": "Second intersection point.",
}
SPYCE_URL["inelpl"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/inelpl_c.html"

#########################################
SPYCE_SIGNATURES ["inrypl"] = ["float[3]", "float[3]", "float[4]"]
SPYCE_ARGNAMES   ["inrypl"] = ["vertex", "dir", "plane"]
SPYCE_RETURNS    ["inrypl"] = ["int", "float[3]"]
SPYCE_RETNAMES   ["inrypl"] = ["nxpts", "xpt"]
SPYCE_ABSTRACT   ["inrypl"] = """
Find the intersection of a ray and a plane.
"""
SPYCE_DEFINITIONS["inrypl"] = {
"vertex": "Vertex of ray.",
"dir": "Direction vector of ray.",
"plane": "A CSPICE plane.",
"nxpts": "Number of intersection points of ray and plane.",
"xpt": "Intersection point, if nxpts = 1.",
}
SPYCE_URL["inrypl"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/inrypl_c.html"

#########################################
SPYCE_SIGNATURES ["intmax"] = []
SPYCE_ARGNAMES   ["intmax"] = []
SPYCE_RETURNS    ["intmax"] = ["int"]
SPYCE_RETNAMES   ["intmax"] = ["value"]
SPYCE_ABSTRACT   ["intmax"] = """
Return the value of the largest (positive) number representable in a
variable.
"""
SPYCE_DEFINITIONS["intmax"] = {
"value": "the largest (positive) number that can be represented in a variable.",
}
SPYCE_URL["intmax"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/intmax_c.html"

#########################################
SPYCE_SIGNATURES ["intmin"] = []
SPYCE_ARGNAMES   ["intmin"] = []
SPYCE_RETURNS    ["intmin"] = ["int"]
SPYCE_RETNAMES   ["intmin"] = ["value"]
SPYCE_ABSTRACT   ["intmin"] = """
Return the value of the smallest (negative) number representable in a
SpiceInt variable.
"""
SPYCE_DEFINITIONS["intmin"] = {
"value": "the smallest (negative) number that can be represented in a variable.",
}
SPYCE_URL["intmin"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/intmin_c.html"

#########################################
SPYCE_SIGNATURES ["invert"] = ["float[3,3]"]
SPYCE_ARGNAMES   ["invert"] = ["m1"]
SPYCE_RETURNS    ["invert"] = ["float[3,3]"]
SPYCE_RETNAMES   ["invert"] = ["mout"]
SPYCE_ABSTRACT   ["invert"] = """
Generate the inverse of a 3x3 matrix.
"""
SPYCE_DEFINITIONS["invert"] = {
"m1": "Matrix to be inverted.",
"mout": "Inverted matrix (m1**-1).",
}
SPYCE_PS ["invert"] = "If m1 is singular, then a matrix filled with zeros is returned."
SPYCE_URL["invert"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/invert_c.html"

SPYCE_SIGNATURES ["invert_error"] = ["float[3,3]"]
SPYCE_ARGNAMES   ["invert_error"] = ["m1"]
SPYCE_RETURNS    ["invert_error"] = ["float[3,3]"]
SPYCE_RETNAMES   ["invert_error"] = ["mout"]
SPYCE_ABSTRACT   ["invert_error"] = """
Generate the inverse of a 3x3 matrix.
"""
SPYCE_DEFINITIONS["invert_error"] = {
"m1": "Matrix to be inverted.",
"mout": "Inverted matrix (m1**-1).",
}
SPYCE_PS ["invert_error"] = "If m1 is singular, then a SPICE(SINGULARMATRIX) condition is raised."
SPYCE_URL["invert_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/invert_c.html"

#########################################
SPYCE_SIGNATURES ["invort"] = ["float[3,3]"]
SPYCE_ARGNAMES   ["invort"] = ["m"]
SPYCE_RETURNS    ["invort"] = ["float[3,3]"]
SPYCE_RETNAMES   ["invort"] = ["mit"]
SPYCE_ABSTRACT   ["invort"] = """
Given a matrix, construct the matrix whose rows are the columns of the
first divided by the length squared of the the corresponding columns of
the input matrix.
"""
SPYCE_DEFINITIONS["invort"] = {
"m": "A 3x3 matrix.",
"mit": "m after transposition and scaling of rows.",
}
SPYCE_URL["invort"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/invort_c.html"

#########################################
SPYCE_SIGNATURES ["isrot"] = ["float[3,3]", "float", "float"]
SPYCE_ARGNAMES   ["isrot"] = ["m", "ntol", "dtol"]
SPYCE_RETURNS    ["isrot"] = ["bool"]
SPYCE_RETNAMES   ["isrot"] = ["status"]
SPYCE_ABSTRACT   ["isrot"] = """
Indicate whether a 3x3 matrix is a rotation matrix.
"""
SPYCE_DEFINITIONS["isrot"] = {
"m": "A matrix to be tested.",
"ntol": "Tolerance for the norms of the columns of m.",
"dtol": "Tolerance for the determinant of a matrix whose columns are the unitized columns of m.",
"status": "True if and only if m is a rotation matrix.",
}
SPYCE_URL["isrot"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/isrot_c.html"

#########################################
SPYCE_SIGNATURES ["j1900"] = []
SPYCE_ARGNAMES   ["j1900"] = []
SPYCE_RETURNS    ["j1900"] = ["float"]
SPYCE_RETNAMES   ["j1900"] = ["jd"]
SPYCE_ABSTRACT   ["j1900"] = """
Return the Julian Date of 1899 DEC 31 12:00:00 (1900 JAN 0.5).
"""
SPYCE_DEFINITIONS["j1900"] = {
"jd": "Julian Date of 1900 JAN 0.5",
}
SPYCE_URL["j1900"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/j1900_c.html"

#########################################
SPYCE_SIGNATURES ["j1950"] = []
SPYCE_ARGNAMES   ["j1950"] = []
SPYCE_RETURNS    ["j1950"] = ["float"]
SPYCE_RETNAMES   ["j1950"] = ["jd"]
SPYCE_ABSTRACT   ["j1950"] = """
Return the Julian Date of 1950 JAN 01 00:00:00 (1950 JAN 1.0).
"""
SPYCE_DEFINITIONS["j1950"] = {
"jd": "Julian Date of 1950 JAN 1.0",
}
SPYCE_URL["j1950"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/j1950_c.html"

#########################################
SPYCE_SIGNATURES ["j2000"] = []
SPYCE_ARGNAMES   ["j2000"] = []
SPYCE_RETURNS    ["j2000"] = ["float"]
SPYCE_RETNAMES   ["j2000"] = ["jd"]
SPYCE_ABSTRACT   ["j2000"] = """
Return the Julian Date of 2000 JAN 01 12:00:00 (2000 JAN 1.5).
"""
SPYCE_DEFINITIONS["j2000"] = {
"jd": "Julian Date of 2000 JAN 1.5",
}
SPYCE_URL["j2000"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/j2000_c.html"

#########################################
SPYCE_SIGNATURES ["j2100"] = []
SPYCE_ARGNAMES   ["j2100"] = []
SPYCE_RETURNS    ["j2100"] = ["float"]
SPYCE_RETNAMES   ["j2100"] = ["jd"]
SPYCE_ABSTRACT   ["j2100"] = """
Return the Julian Date of 2100 JAN 01 12:00:00 (2100 JAN 1.5).
"""
SPYCE_DEFINITIONS["j2100"] = {
"jd": "Julian Date of 2100 JAN 1.5",
}
SPYCE_URL["j2100"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/j2100_c.html"

#########################################
SPYCE_SIGNATURES ["jyear"] = []
SPYCE_ARGNAMES   ["jyear"] = []
SPYCE_RETURNS    ["jyear"] = ["float"]
SPYCE_RETNAMES   ["jyear"] = ["value"]
SPYCE_ABSTRACT   ["jyear"] = """
Return the number of seconds in a julian year.
"""
SPYCE_DEFINITIONS["jyear"] = {
"value": "number of seconds in a julian year",
}
SPYCE_URL["jyear"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/jyear_c.html"

#########################################
SPYCE_SIGNATURES ["kplfrm"] = ["int"]
SPYCE_ARGNAMES   ["kplfrm"] = ["frmcls"]
SPYCE_RETURNS    ["kplfrm"] = ["int[*]"]
SPYCE_RETNAMES   ["kplfrm"] = ["idset"]
SPYCE_ABSTRACT   ["kplfrm"] = """
Return an array containing the frame IDs of all reference frames of a
given class having specifications in the kernel pool.
"""
SPYCE_DEFINITIONS["kplfrm"] = {
"frmcls": "Frame class (-1 = all; 1 = built-in inertial; 2 = PCK-based; 3 = CK-based; 4 = fixed rotational; 5 = dynamic).",
"idset": "Set of ID codes of frames of the specified class.",
}
SPYCE_URL["kplfrm"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/kplfrm_c.html"

#########################################
SPYCE_SIGNATURES ["latcyl"] = 3*["float"]
SPYCE_ARGNAMES   ["latcyl"] = ["radius", "lon", "lat"]
SPYCE_RETURNS    ["latcyl"] = 3*["float"]
SPYCE_RETNAMES   ["latcyl"] = ["r", "lonc", "z"]
SPYCE_ABSTRACT   ["latcyl"] = """
Convert from latitudinal coordinates to cylindrical coordinates.
"""
SPYCE_DEFINITIONS["latcyl"] = {
"radius": "Distance of a point from the origin.",
"lon": "Angle of the point from the XZ plane in radians.",
"lat": "Angle of the point from the XY plane in radians.",
"r": "Distance of the point from the z axis.",
"lonc": "Angle of the point from the XZ plane in radians.",
"z": "Height of the point above the XY plane.",
}
SPYCE_URL["latcyl"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/latcyl_c.html"

#########################################
SPYCE_SIGNATURES ["latrec"] = 3*["float"]
SPYCE_ARGNAMES   ["latrec"] = ["radius", "lon", "lat"]
SPYCE_RETURNS    ["latrec"] = ["float[3]"]
SPYCE_RETNAMES   ["latrec"] = ["rectan"]
SPYCE_ABSTRACT   ["latrec"] = """
Convert from latitudinal coordinates to rectangular coordinates.
"""
SPYCE_DEFINITIONS["latrec"] = {
"radius": "Distance of a point from the origin.",
"lon": "Longitude of point in radians.",
"lat": "Latitude of point in radians.",
"rectan": "Rectangular coordinates of the point.",
}
SPYCE_URL["latrec"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/latrec_c.html"

#########################################
SPYCE_SIGNATURES ["latsrf"] = ["string", "body_name", "time", "frame_name", "float[*,2]"]
SPYCE_ARGNAMES   ["latsrf"] = ["method", "target", "et", "fixref", "lonlat"]
SPYCE_RETURNS    ["latsrf"] = ["float[*,3]"]
SPYCE_RETNAMES   ["latsrf"] = ["srfpts"]
SPYCE_ABSTRACT   ["latsrf"] = """
Map array of planetocentric longitude/latitude coordinate pairs to
surface points on a specified target body.

The surface of the target body may be represented by a triaxial
ellipsoid or by topographic data provided by DSK files.
"""
SPYCE_DEFINITIONS["latsrf"] = {
"method": "Computation method: ELLIPSOID or DSK/UNPRIORITIZED[/SURFACES = <surface list>].",
"target": "Name of target body.",
"et": "Epoch in TDB seconds past J2000 TDB.",
"fixref": "Body-fixed, body-centered target body frame.",
"lonlat": "Array of longitude/latitude coordinate pairs.",
"srfpts": "Array of surface points.",
}
SPYCE_URL["latsrf"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/latsrf_c.html"

#########################################
SPYCE_SIGNATURES ["latsph"] = 3*["float"]
SPYCE_ARGNAMES   ["latsph"] = ["radius", "lon", "lat"]
SPYCE_RETURNS    ["latsph"] = 3*["float"]
SPYCE_RETNAMES   ["latsph"] = ["rho", "colat", "lon2"]
SPYCE_ABSTRACT   ["latsph"] = """
Convert from latitudinal coordinates to spherical coordinates.
"""
SPYCE_DEFINITIONS["latsph"] = {
"radius": "Distance of a point from the origin.",
"lon": "Angle of the point from the XZ plane in radians.",
"lat": "Angle of the point from the XY plane in radians.",
"rho": "Distance of the point from the origin.",
"colat": "Angle of the point from positive z axis (radians).",
"lon2": "Angle of the point from the XZ plane (radians).",
}
SPYCE_URL["latsph"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/latsph_c.html"

#########################################
SPYCE_SIGNATURES ["ldpool"] = ["string"]
SPYCE_ARGNAMES   ["ldpool"] = ["filename"]
SPYCE_RETURNS    ["ldpool"] = []
SPYCE_RETNAMES   ["ldpool"] = []
SPYCE_ABSTRACT   ["ldpool"] = """
Load the variables contained in a NAIF ASCII kernel file into the kernel
pool.
"""
SPYCE_DEFINITIONS["ldpool"] = {
"filename": "Name of the kernel file.",
}
SPYCE_URL["ldpool"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ldpool_c.html"

#########################################
SPYCE_SIGNATURES ["limbpt"] = ["string", "body_name", "time", "frame_name", "string", "string", "body_name", "float[3]", "float", "int", "float", "float", "int"]
SPYCE_ARGNAMES   ["limbpt"] = ["method", "target", "et", "fixref", "abcorr", "corloc", "obsrvr", "refvec", "rolstp", "ncuts", "schstp", "soltol", "maxn"]
SPYCE_RETURNS    ["limbpt"] = ["int[*]", "float[*,3]", "float[*]", "float[*,3]"]
SPYCE_RETNAMES   ["limbpt"] = ["npts", "points", "epochs", "tangts"]
SPYCE_ABSTRACT   ["limbpt"] = """
Find limb points on a target body. The limb is the set of points of
tangency on the target of rays emanating from the observer. The caller
specifies half-planes bounded by the observer-target center vector in
which to search for limb points.

The surface of the target body may be represented either by a triaxial
ellipsoid or by topographic data.
"""
SPYCE_DEFINITIONS["limbpt"] = {
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
SPYCE_URL["limbpt"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/limbpt_c.html"

#########################################
SPYCE_SIGNATURES ["lspcn"] = ["body_name", "time", "string"]
SPYCE_ARGNAMES   ["lspcn"] = ["body", "et", "abcorr"]
SPYCE_RETURNS    ["lspcn"] = ["float"]
SPYCE_RETNAMES   ["lspcn"] = ["value"]
SPYCE_ABSTRACT   ["lspcn"] = """
Compute L_s, the planetocentric longitude of the sun, as seen from a
specified body.
"""
SPYCE_DEFINITIONS["lspcn"] = {
"body": "Name of central body.",
"et": "Epoch in seconds past J2000 TDB.",
"abcorr": "Aberration correction, \"NONE\", \"LT\", \"LT+S\", \"CN\", or \"CN+S\".",
"value": "L_s for the specified body at the specified time.",
}
SPYCE_URL["lspcn"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/lspcn_c.html"

#########################################
SPYCE_SIGNATURES ["ltime"] = ["time", "body_code", "string", "body_code"]
SPYCE_ARGNAMES   ["ltime"] = ["etobs", "obs", "dir", "targ"]
SPYCE_RETURNS    ["ltime"] = ["float", "float"]
SPYCE_RETNAMES   ["ltime"] = ["ettarg", "elapsd"]
SPYCE_ABSTRACT   ["ltime"] = """
Light Time
"""
SPYCE_DEFINITIONS["ltime"] = {
"etobs": "Epoch of a signal at some observer",
"obs": "NAIF ID of some observer",
"dir": "Direction the signal travels (\"->\" or \"<-\")",
"targ": "NAIF ID of the target object",
"ettarg": "Epoch of the signal at the target",
"elapsd": "Time between transmit and receipt of the signal",
}
SPYCE_URL["ltime"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ltime_c.html"

#########################################
SPYCE_SIGNATURES ["m2eul"] = ["rotmat[3,3]"] + 3*["int"]
SPYCE_ARGNAMES   ["m2eul"] = ["r", "axis3", "axis2", "axis1"]
SPYCE_RETURNS    ["m2eul"] = 3*["float"]
SPYCE_RETNAMES   ["m2eul"] = ["angle3", "angle2", "angle1"]
SPYCE_ABSTRACT   ["m2eul"] = """
Factor a rotation matrix as a product of three rotations about specified
coordinate axes.
"""
SPYCE_DEFINITIONS["m2eul"] = {
"r": "A rotation matrix to be factored.",
"axis3": "Number of the third rotation axis.",
"axis2": "Number of the second rotation axis.",
"axis1": "Number of the first rotation axis.",
"angle3": "Third Euler angle, in radians.",
"angle2": "Second Euler angle, in radians.",
"angle1": "First Euler angle, in radians.",
}
SPYCE_URL["m2eul"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/m2eul_c.html"

#########################################
SPYCE_SIGNATURES ["m2q"] = ["rotmat[3,3]"]
SPYCE_ARGNAMES   ["m2q"] = ["r"]
SPYCE_RETURNS    ["m2q"] = ["float[4]"]
SPYCE_RETNAMES   ["m2q"] = ["q"]
SPYCE_ABSTRACT   ["m2q"] = """
Find a unit quaternion corresponding to a specified rotation matrix.
"""
SPYCE_DEFINITIONS["m2q"] = {
"r": "A rotation matrix.",
"q": "A unit quaternion representing r.",
}
SPYCE_URL["m2q"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/m2q_c.html"

#########################################
SPYCE_SIGNATURES ["mequ"] = ["float[3,3]"]
SPYCE_ARGNAMES   ["mequ"] = ["m1"]
SPYCE_RETURNS    ["mequ"] = ["float[3,3]"]
SPYCE_RETNAMES   ["mequ"] = ["mout"]
SPYCE_ABSTRACT   ["mequ"] = """
Set one double precision 3x3 matrix equal to another.
"""
SPYCE_DEFINITIONS["mequ"] = {
"m1": "Input matrix.",
"mout": "Output matrix equal to m1.",
}
SPYCE_URL["mequ"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mequ_c.html"

#########################################
SPYCE_SIGNATURES ["mequg"] = ["float[*,*]"]
SPYCE_ARGNAMES   ["mequg"] = ["m1"]
SPYCE_RETURNS    ["mequg"] = ["float[*,*]"]
SPYCE_RETNAMES   ["mequg"] = ["mout"]
SPYCE_ABSTRACT   ["mequg"] = """
Set one double precision matrix of arbitrary size equal to another.
"""
SPYCE_DEFINITIONS["mequg"] = {
"m1": "Input matrix.",
"mout": "Output matrix equal to m1.",
}
SPYCE_URL["mequg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mequg_c.html"

#########################################
SPYCE_SIGNATURES ["mtxm"] = 2*["float[3,3]"]
SPYCE_ARGNAMES   ["mtxm"] = ["m1", "m2"]
SPYCE_RETURNS    ["mtxm"] = ["float[3,3]"]
SPYCE_RETNAMES   ["mtxm"] = ["mout"]
SPYCE_ABSTRACT   ["mtxm"] = """
Multiply the transpose of a 3x3 matrix and a 3x3 matrix.
"""
SPYCE_DEFINITIONS["mtxm"] = {
"m1": "3x3 double precision matrix.",
"m2": "3x3 double precision matrix.",
"mout": "The produce m1 transpose times m2.",
}
SPYCE_URL["mtxm"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mtxm_c.html"

#########################################
SPYCE_SIGNATURES ["mtxmg"] = 2*["float[*,*]"]
SPYCE_ARGNAMES   ["mtxmg"] = ["m1", "m2"]
SPYCE_RETURNS    ["mtxmg"] = ["float[*,*]"]
SPYCE_RETNAMES   ["mtxmg"] = ["mout"]
SPYCE_ABSTRACT   ["mtxmg"] = """
Multiply the transpose of a matrix with another matrix, both of
arbitrary size. (The dimensions of the matrices must be compatible with
this multiplication.)
"""
SPYCE_DEFINITIONS["mtxmg"] = {
"m1": "nr1r2 X ncol1 double precision matrix.",
"m2": "nr1r2 X ncol2 double precision matrix.",
"mout": "Transpose of m1 times m2.",
}
SPYCE_URL["mtxmg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mtxmg_c.html"

#########################################
SPYCE_SIGNATURES ["mtxv"] = ["float[3,3]", "float[3]"]
SPYCE_ARGNAMES   ["mtxv"] = ["m1", "vin"]
SPYCE_RETURNS    ["mtxv"] = ["float[3]"]
SPYCE_RETNAMES   ["mtxv"] = ["vout"]
SPYCE_ABSTRACT   ["mtxv"] = """
Multiply the transpose of a 3x3 matrix on the left with a vector on the
right.
"""
SPYCE_DEFINITIONS["mtxv"] = {
"m1": "3x3 double precision matrix.",
"vin": "3-dimensional double precision vector.",
"vout": "the product m1**t * vin.",
}
SPYCE_URL["mtxv"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mtxv_c.html"

#########################################
SPYCE_SIGNATURES ["mtxvg"] = ["float[*,*]", "float[*]"]
SPYCE_ARGNAMES   ["mtxvg"] = ["m1", "v2"]
SPYCE_RETURNS    ["mtxvg"] = ["float[*]"]
SPYCE_RETNAMES   ["mtxvg"] = ["vout"]
SPYCE_ABSTRACT   ["mtxvg"] = """
Multiply the transpose of a matrix and a vector of arbitrary size.
"""
SPYCE_DEFINITIONS["mtxvg"] = {
"m1": "Left-hand matrix to be multiplied.",
"v2": "Right-hand vector to be multiplied.",
"vout": "Product vector m1 transpose * v2.",
}
SPYCE_URL["mtxvg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mtxvg_c.html"

#########################################
SPYCE_SIGNATURES ["mxm"] = ["float[3,3]", "float[3,3]"]
SPYCE_ARGNAMES   ["mxm"] = ["m1", "m2"]
SPYCE_RETURNS    ["mxm"] = ["float[3,3]"]
SPYCE_RETNAMES   ["mxm"] = ["mout"]
SPYCE_ABSTRACT   ["mxm"] = """
Multiply two 3x3 matrices.
"""
SPYCE_DEFINITIONS["mxm"] = {
"m1": "3x3 double precision matrix.",
"m2": "3x3 double precision matrix.",
"mout": "the product m1*m2.",
}
SPYCE_URL["mxm"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mxm_c.html"

#########################################
SPYCE_SIGNATURES ["mxmg"] = ["float[*,*]", "float[*,*]"]
SPYCE_ARGNAMES   ["mxmg"] = ["m1", "m2"]
SPYCE_RETURNS    ["mxmg"] = ["float[*,*]"]
SPYCE_RETNAMES   ["mxmg"] = ["mout"]
SPYCE_ABSTRACT   ["mxmg"] = """
Multiply two double precision matrices of arbitrary size.
"""
SPYCE_DEFINITIONS["mxmg"] = {
"m1": "nrow1 X ncol1 double precision matrix.",
"m2": "ncol1 X ncol2 double precision matrix.",
"mout": "nrow1 X ncol2 double precision matrix.",
}
SPYCE_URL["mxmg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mxmg_c.html"

#########################################
SPYCE_SIGNATURES ["mxmt"] = ["float[3,3]", "float[3,3]"]
SPYCE_ARGNAMES   ["mxmt"] = ["m1", "m2"]
SPYCE_RETURNS    ["mxmt"] = ["float[3,3]"]
SPYCE_RETNAMES   ["mxmt"] = ["mout"]
SPYCE_ABSTRACT   ["mxmt"] = """
Multiply a 3x3 matrix and the transpose of another 3x3 matrix.
"""
SPYCE_DEFINITIONS["mxmt"] = {
"m1": "3x3 double precision matrix.",
"m2": "3x3 double precision matrix.",
"mout": "The product m1 times m2 transpose .",
}
SPYCE_URL["mxmt"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mxmt_c.html"

#########################################
SPYCE_SIGNATURES ["mxmtg"] = ["float[*,*]", "float[*]"]
SPYCE_ARGNAMES   ["mxmtg"] = ["m1", "m2"]
SPYCE_RETURNS    ["mxmtg"] = ["float[*]"]
SPYCE_RETNAMES   ["mxmtg"] = ["mout"]
SPYCE_ABSTRACT   ["mxmtg"] = """
Multiply a matrix and the transpose of a matrix, both of arbitrary size.
"""
SPYCE_DEFINITIONS["mxmtg"] = {
"m1": "Left-hand matrix to be multiplied.",
"m2": "Right-hand matrix whose transpose is to be multiplied",
"mout": "Product matrix.",
}
SPYCE_URL["mxmtg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mxmtg_c.html"

#########################################
SPYCE_SIGNATURES ["mxv"] = ["float[3,3]", "float[3]"]
SPYCE_ARGNAMES   ["mxv"] = ["m1", "vin"]
SPYCE_RETURNS    ["mxv"] = ["float[3]"]
SPYCE_RETNAMES   ["mxv"] = ["vout"]
SPYCE_ABSTRACT   ["mxv"] = """
Multiply a 3x3 double precision matrix with a 3-dimensional double
precision vector.
"""
SPYCE_DEFINITIONS["mxv"] = {
"m1": "3x3 double precision matrix.",
"vin": "3-dimensional double precision vector.",
"vout": "3-dimensinoal double precision vector. vout is the product m1*vin.",
}
SPYCE_URL["mxv"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mxv_c.html"

#########################################
SPYCE_SIGNATURES ["mxvg"] = ["float[*,*]", "float[*]"]
SPYCE_ARGNAMES   ["mxvg"] = ["m1", "v2"]
SPYCE_RETURNS    ["mxvg"] = ["float[*]"]
SPYCE_RETNAMES   ["mxvg"] = ["vout"]
SPYCE_ABSTRACT   ["mxvg"] = """
Multiply a matrix and a vector of arbitrary size.
"""
SPYCE_DEFINITIONS["mxvg"] = {
"m1": "Left-hand matrix to be multiplied.",
"v2": "Right-hand vector to be multiplied.",
"vout": "Product vector m1*v2.",
}
SPYCE_URL["mxvg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mxvg_c.html"

#########################################
SPYCE_SIGNATURES ["namfrm"] = ["frame_name"]
SPYCE_ARGNAMES   ["namfrm"] = ["frname"]
SPYCE_RETURNS    ["namfrm"] = ["int"]
SPYCE_RETNAMES   ["namfrm"] = ["frcode"]
SPYCE_ABSTRACT   ["namfrm"] = """
Look up the frame ID code associated with a string.
"""
SPYCE_DEFINITIONS["namfrm"] = {
"frname": "The name of some reference frame.",
"frcode": "The SPICE ID code of the frame; 0 on error.",
}
SPYCE_URL["namfrm"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/namfrm_c.html"

SPYCE_SIGNATURES ["namfrm_error"] = ["frame_name"]
SPYCE_ARGNAMES   ["namfrm_error"] = ["frname"]
SPYCE_RETURNS    ["namfrm_error"] = ["frame_code"]
SPYCE_RETNAMES   ["namfrm_error"] = ["frcode"]
SPYCE_ABSTRACT   ["namfrm_error"] = """
Look up the frame ID code associated with a string.
"""
SPYCE_DEFINITIONS["namfrm_error"] = {
"frname": "The name of some reference frame.",
"frcode": "The SPICE ID code of the frame.",
}
SPYCE_PS ["namfrm_error"] = "Raise SPICE(FRAMEIDNOTFOUND) error condition if not found."
SPYCE_URL["namfrm_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/namfrm_c.html"

#########################################
SPYCE_SIGNATURES ["nearpt"] = ["float[3]"] + 3*["float"]
SPYCE_ARGNAMES   ["nearpt"] = ["positn", "a", "b", "c"]
SPYCE_RETURNS    ["nearpt"] = ["float[3]", "float"]
SPYCE_RETNAMES   ["nearpt"] = ["npoint", "alt"]
SPYCE_ABSTRACT   ["nearpt"] = """
This routine locates the point on the surface of an ellipsoid that is
nearest to a specified position. It also returns the altitude of the
position above the ellipsoid.
"""
SPYCE_DEFINITIONS["nearpt"] = {
"positn": "Position of a point in bodyfixed frame.",
"a": "Length of semi-axis parallel to x-axis.",
"b": "Length of semi-axis parallel to y-axis.",
"c": "Length on semi-axis parallel to z-axis.",
"npoint": "Point on the ellipsoid closest to positn.",
"alt": "Altitude of positn above the ellipsoid.",
}
SPYCE_URL["nearpt"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/nearpt_c.html"

#########################################
SPYCE_SIGNATURES ["npedln"] = 3*["float"] + 2*["float[3]"]
SPYCE_ARGNAMES   ["npedln"] = ["a", "b", "c", "linept", "linedr"]
SPYCE_RETURNS    ["npedln"] = ["float[3]", "float"]
SPYCE_RETNAMES   ["npedln"] = ["pnear", "dist"]
SPYCE_ABSTRACT   ["npedln"] = """
Find nearest point on a triaxial ellipsoid to a specified line, and the
distance from the ellipsoid to the line.
"""
SPYCE_DEFINITIONS["npedln"] = {
"a": "Length of ellipsoid's semi-axis in the x direction",
"b": "Length of ellipsoid's semi-axis in the y direction",
"c": "Length of ellipsoid's semi-axis in the z direction",
"linept": "Point on line",
"linedr": "Direction vector of line",
"pnear": "Nearest point on ellipsoid to line",
"dist": "Distance of ellipsoid from line",
}
SPYCE_URL["npedln"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/npedln_c.html"

#########################################
SPYCE_SIGNATURES ["npelpt"] = ["float[3]", "float[9]"]
SPYCE_ARGNAMES   ["npelpt"] = ["point", "ellips"]
SPYCE_RETURNS    ["npelpt"] = ["float[3]", "float"]
SPYCE_RETNAMES   ["npelpt"] = ["pnear", "dist"]
SPYCE_ABSTRACT   ["npelpt"] = """
Find the nearest point on an ellipse to a specified point, both in
three-dimensional space, and find the distance between the ellipse and
the point.
"""
SPYCE_DEFINITIONS["npelpt"] = {
"point": "Point whose distance to an ellipse is to be found.",
"ellips": "A CSPICE ellipse.",
"pnear": "Nearest point on ellipse to input point.",
"dist": "Distance of input point to ellipse.",
}
SPYCE_URL["npelpt"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/npelpt_c.html"

#########################################
SPYCE_SIGNATURES ["nplnpt"] = 3*["float[3]"]
SPYCE_ARGNAMES   ["nplnpt"] = ["linpt", "lindir", "point"]
SPYCE_RETURNS    ["nplnpt"] = ["float[3]", "float"]
SPYCE_RETNAMES   ["nplnpt"] = ["pnear", "dist"]
SPYCE_ABSTRACT   ["nplnpt"] = """
Find the nearest point on a line to a specified point, and find the
distance between the two points.
"""
SPYCE_DEFINITIONS["nplnpt"] = {
"linpt": "Point on a line.",
"lindir": "The line's direction vector.",
"point": "A second point.",
"pnear": "Nearest point on the line to point.",
"dist": "Distance between point and pnear.",
}
SPYCE_URL["nplnpt"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/nplnpt_c.html"

#########################################
SPYCE_SIGNATURES ["nvc2pl"] = ["float[3]", "float"]
SPYCE_ARGNAMES   ["nvc2pl"] = ["normal", "constant"]
SPYCE_RETURNS    ["nvc2pl"] = ["float[4]"]
SPYCE_RETNAMES   ["nvc2pl"] = ["plane"]
SPYCE_ABSTRACT   ["nvc2pl"] = """
Make a CSPICE plane from a normal vector and a constant.
"""
SPYCE_DEFINITIONS["nvc2pl"] = {
"normal": "A normal vector",
"constant": "A constant defining a plane.",
"plane": "A CSPICE plane structure representing the plane.",
}
SPYCE_URL["nvc2pl"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/nvc2pl_c.html"

#########################################
SPYCE_SIGNATURES ["nvp2pl"] = 2*["float[3]"]
SPYCE_ARGNAMES   ["nvp2pl"] = ["normal", "point"]
SPYCE_RETURNS    ["nvp2pl"] = ["float[4]"]
SPYCE_RETNAMES   ["nvp2pl"] = ["plane"]
SPYCE_ABSTRACT   ["nvp2pl"] = """
Make a CSPICE plane from a normal vector and a point.
"""
SPYCE_DEFINITIONS["nvp2pl"] = {
"normal": "A normal vector",
"point": "A point defining a plane.",
"plane": "A CSPICE plane structure representing the plane.",
}
SPYCE_URL["nvp2pl"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/nvp2pl_c.html"

#########################################
SPYCE_SIGNATURES ["occult"] = 2*["body_name", "string", "frame_name"] + ["string", "body_name", "time"]
SPYCE_ARGNAMES   ["occult"] = ["targ1", "shape1", "frame1","targ2", "shape2", "frame2","abcorr", "obsrvr", "et"]
SPYCE_RETURNS    ["occult"] = ["int"]
SPYCE_RETNAMES   ["occult"] = ["ocltid"]
SPYCE_ABSTRACT   ["occult"] = """
Determines the occultation condition (not occulted, partially, etc.) of
one target relative to another target as seen by an observer at a given
time.

The surfaces of the target bodies may be represented by triaxial
ellipsoids or by topographic data provided by DSK files.
"""
SPYCE_DEFINITIONS["occult"] = {
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
SPYCE_URL["occult"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/occult_c.html"

#########################################
SPYCE_SIGNATURES ["oscelt"] = ["float[6]", "time", "float"]
SPYCE_ARGNAMES   ["oscelt"] = ["state", "et", "gm"]
SPYCE_RETURNS    ["oscelt"] = ["float[8]"]
SPYCE_RETNAMES   ["oscelt"] = ["elts"]
SPYCE_ABSTRACT   ["oscelt"] = """
Determine the set of osculating conic orbital elements that corresponds
to the state (position, velocity) of a body at some epoch.
"""
SPYCE_DEFINITIONS["oscelt"] = {
"state": "State of body at epoch of elements.",
"et": "Epoch of elements.",
"gm": "Gravitational parameter (GM) of primary body.",
"elts": "Equivalent conic elements",
}
SPYCE_URL["oscelt"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/oscelt_c.html"

#########################################
SPYCE_SIGNATURES ["oscltx"] = ["float[6]", "time", "float"]
SPYCE_ARGNAMES   ["oscltx"] = ["state", "et", "gm"]
SPYCE_RETURNS    ["oscltx"] = ["float[*]"]
SPYCE_RETNAMES   ["oscltx"] = ["elts"]
SPYCE_ABSTRACT   ["oscltx"] = """
Determine the set of osculating conic orbital elements that corresponds
to the state (position, velocity) of a body at some epoch. In
additional to the classical elements, return the true anomaly,
semi-major axis, and period, if applicable.
"""
SPYCE_DEFINITIONS["oscltx"] = {
"state": "State of body at epoch of elements.",
"et": "Epoch of elements.",
"gm": "Gravitational parameter (GM) of primary body.",
"elts": "Extended set of classical conic elements.",
}
SPYCE_URL["oscltx"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/oscltx_c.html"

#########################################
SPYCE_SIGNATURES ["pckcov"] = ["string", "frame_code"]
SPYCE_ARGNAMES   ["pckcov"] = ["pck", "idcode"]
SPYCE_RETURNS    ["pckcov"] = ["float[*,2]"]
SPYCE_RETNAMES   ["pckcov"] = ["cover"]
SPYCE_ABSTRACT   ["pckcov"] = """
Find the coverage window for a specified reference frame in a specified
binary PCK file.
"""
SPYCE_DEFINITIONS["pckcov"] = {
"pck": "Name of PCK file.",
"idcode": "Class ID code of PCK reference frame.",
"cover": "An array of shape (n,2), where cover[:,0] are start times and cover[:,1] are stop times.",
}
SPYCE_URL["pckcov"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pckcov_c.html"

SPYCE_SIGNATURES ["pckcov_error"] = ["string", "frame_code"]
SPYCE_ARGNAMES   ["pckcov_error"] = ["pck", "idcode"]
SPYCE_RETURNS    ["pckcov_error"] = ["float[*,2]"]
SPYCE_RETNAMES   ["pckcov_error"] = ["cover"]
SPYCE_ABSTRACT   ["pckcov_error"] = """
Find the coverage window for a specified reference frame in a specified
binary PCK file.
"""
SPYCE_DEFINITIONS["pckcov_error"] = {
"pck": "Name of PCK file.",
"idcode": "Class ID code of PCK reference frame.",
"cover": "An array of shape (n,2), where cover[:,0] are start times and cover[:,1] are stop times.",
}
SPYCE_PS ["pckcov_error"] = "Raise KeyError if the idcode is not found."
SPYCE_URL["pckcov_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pckcov_c.html"

#########################################
SPYCE_SIGNATURES ["pckfrm"] = ["string"]
SPYCE_ARGNAMES   ["pckfrm"] = ["pck"]
SPYCE_RETURNS    ["pckfrm"] = ["int[*]"]
SPYCE_RETNAMES   ["pckfrm"] = ["ids"]
SPYCE_ABSTRACT   ["pckfrm"] = """
Find the set of reference frame class ID codes of all frames in a
specified binary PCK file.
"""
SPYCE_DEFINITIONS["pckfrm"] = {
"pck": "Name of PCK file.",
"ids": "Set of frame ID codes of frames in PCK file.",
}
SPYCE_URL["pckfrm"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pckfrm_c.html"

#########################################
SPYCE_SIGNATURES ["pcpool"] = ["string", "string[*]"]
SPYCE_ARGNAMES   ["pcpool"] = ["name", "cvals"]
SPYCE_RETURNS    ["pcpool"] = []
SPYCE_RETNAMES   ["pcpool"] = []
SPYCE_ABSTRACT   ["pcpool"] = """
This entry point provides toolkit programmers a method for
programmatically inserting character data into the kernel pool.
"""
SPYCE_DEFINITIONS["pcpool"] = {
"name": "The kernel pool name to associate with cvals.",
"cvals": "An array of strings to insert into the kernel pool.",
}
SPYCE_URL["pcpool"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pcpool_c.html"

#########################################
SPYCE_SIGNATURES ["pdpool"] = ["string", "float[*]"]
SPYCE_ARGNAMES   ["pdpool"] = ["name", "dvals"]
SPYCE_RETURNS    ["pdpool"] = []
SPYCE_RETNAMES   ["pdpool"] = []
SPYCE_ABSTRACT   ["pdpool"] = """
This entry point provides toolkit programmers a method for
programmatically inserting double precision data into the kernel pool.
"""
SPYCE_DEFINITIONS["pdpool"] = {
"name": "The kernel pool name to associate with dvals.",
"dvals": "An array of values to insert into the kernel pool.",
}
SPYCE_URL["pdpool"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pdpool_c.html"

#########################################
SPYCE_SIGNATURES ["pgrrec"] = ["body_name"] + 5*["float"]
SPYCE_ARGNAMES   ["pgrrec"] = ["body", "lon", "lat", "alt", "re", "f"]
SPYCE_RETURNS    ["pgrrec"] = ["float[3]"]
SPYCE_RETNAMES   ["pgrrec"] = ["rectan"]
SPYCE_ABSTRACT   ["pgrrec"] = """
Convert planetographic coordinates to rectangular coordinates.
"""
SPYCE_DEFINITIONS["pgrrec"] = {
"body": "Body with which coordinate system is associated.",
"lon": "Planetographic longitude of a point (radians).",
"lat": "Planetographic latitude of a point (radians).",
"alt": "Altitude of a point above reference spheroid.",
"re": "Equatorial radius of the reference spheroid.",
"f": "Flattening coefficient.",
"rectan": "Rectangular coordinates of the point.",
}
SPYCE_URL["pgrrec"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pgrrec_c.html"

#########################################
SPYCE_SIGNATURES ["phaseq"] = ["time", "body_name", "body_name", "body_name", "string"]
SPYCE_ARGNAMES   ["phaseq"] = ["et", "target", "illmn", "obsrvr", "abcorr"]
SPYCE_RETURNS    ["phaseq"] = ["float"]
SPYCE_RETNAMES   ["phaseq"] = ["value"]
SPYCE_ABSTRACT   ["phaseq"] = """
Compute the apparent phase angle for a target, observer, illuminator set
of ephemeris objects.
"""
SPYCE_DEFINITIONS["phaseq"] = {
"et": "Ephemeris seconds past J2000 TDB.",
"target": "Target body name.",
"illmn": "Illuminating body name.",
"obsrvr": "Observer body.",
"abcorr": "Aberration correction, \"NONE\", \"LT\", \"LT+S\", \"CN\", or \"CN+S\".",
"value": "Value of phase angle.",
}
SPYCE_URL["phaseq"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/phaseq_c.html"

#########################################
SPYCE_SIGNATURES ["pi"] = []
SPYCE_ARGNAMES   ["pi"] = []
SPYCE_RETURNS    ["pi"] = ["float"]
SPYCE_RETNAMES   ["pi"] = ["value"]
SPYCE_ABSTRACT   ["pi"] = """
Return the value of pi.
"""
SPYCE_DEFINITIONS["pi"] = {
"value": "value of pi",
}
SPYCE_URL["pi"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pi_c.html"

#########################################
SPYCE_SIGNATURES ["pipool"] = ["string", "int[*]"]
SPYCE_ARGNAMES   ["pipool"] = ["name", "ivals"]
SPYCE_RETURNS    ["pipool"] = []
SPYCE_RETNAMES   ["pipool"] = []
SPYCE_ABSTRACT   ["pipool"] = """
This entry point provides toolkit programmers a method for
programmatically inserting integer data into the kernel pool.
"""
SPYCE_DEFINITIONS["pipool"] = {
"name": "The kernel pool name to associate with values.",
"ivals": "An array of integers to insert into the pool.",
}
SPYCE_URL["pipool"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pipool_c.html"

#########################################
SPYCE_SIGNATURES ["pjelpl"] = ["float[9]", "float[4]"]
SPYCE_ARGNAMES   ["pjelpl"] = ["elin", "plane"]
SPYCE_RETURNS    ["pjelpl"] = ["float[9]"]
SPYCE_RETNAMES   ["pjelpl"] = ["elout"]
SPYCE_ABSTRACT   ["pjelpl"] = """
Project an ellipse onto a plane, orthogonally.
"""
SPYCE_DEFINITIONS["pjelpl"] = {
"elin": "A CSPICE ellipse to be projected.",
"plane": "A plane onto which elin is to be projected.",
"elout": "A CSPICE ellipse resulting from the projection.",
}
SPYCE_URL["pjelpl"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pjelpl_c.html"

#########################################
SPYCE_SIGNATURES ["pltar"] = ["float[*,3]", "int[*,3]"]
SPYCE_ARGNAMES   ["pltar"] = ["vrtces", "plates"]
SPYCE_RETURNS    ["pltar"] = ["float"]
SPYCE_RETNAMES   ["pltar"] = ["area"]
SPYCE_ABSTRACT   ["pltar"] = """
Compute the total area of a collection of triangular plates.
"""
SPYCE_DEFINITIONS["pltar"] = {
"vrtces": "Array of vertices.",
"plates": "Array of plates defined by the indices of three vertices. Indices start at 1.",
"area": "total area of plates.",
}
SPYCE_URL["pltar"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pltar_c.html"

#########################################
SPYCE_SIGNATURES ["pltexp"] = ["float[3,3]", "float"]
SPYCE_ARGNAMES   ["pltexp"] = ["iverts", "delta"]
SPYCE_RETURNS    ["pltexp"] = ["float[3,3]"]
SPYCE_RETNAMES   ["pltexp"] = ["overts"]
SPYCE_ABSTRACT   ["pltexp"] = """
Expand a triangular plate by a specified amount. The expanded plate is
co-planar with, and has the same orientation as, the original. The
centroids of the two plates coincide.
"""
SPYCE_DEFINITIONS["pltexp"] = {
"iverts": "Vertices of the plate to be expanded.",
"delta": "Fraction by which the plate is to be expanded.",
"overts": "Vertices of the expanded plate.",
}
SPYCE_URL["pltexp"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pltexp_c.html"

#########################################
SPYCE_SIGNATURES ["pltnp"] = 4*["float[3]"]
SPYCE_ARGNAMES   ["pltnp"] = ["point", "v1", "v2", "v3"]
SPYCE_RETURNS    ["pltnp"] = ["float[3]", "float"]
SPYCE_RETNAMES   ["pltnp"] = ["pnear", "dist"]
SPYCE_ABSTRACT   ["pltnp"] = """
Find the nearest point on a triangular plate to a given point.
"""
SPYCE_DEFINITIONS["pltnp"] = {
"point": "A point in 3-dimensional space.",
"v1": "Vertex of a triangular plate.",
"v2": "Vertex of a triangular plate.",
"v3": "Vertex of a triangular plate.",
"pnear": "Nearest point on the plate to `point'.",
"dist": "Distance between `pnear' and `point'.",
}
SPYCE_URL["pltnp"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pltnp_c.html"

#########################################
SPYCE_SIGNATURES ["pltvol"] = ["float[*,3]", "int[*,3]"]
SPYCE_ARGNAMES   ["pltvol"] = ["vrtces", "plates"]
SPYCE_RETURNS    ["pltvol"] = ["float"]
SPYCE_RETNAMES   ["pltvol"] = ["volume"]
SPYCE_ABSTRACT   ["pltvol"] = """
Compute the volume of a three-dimensional region bounded by a collection
of triangular plates.
"""
SPYCE_DEFINITIONS["pltvol"] = {
"vrtces": "Array of vertices.",
"plates": "Array of plates defined by the indices of three vertices. Indices start at 1.",
"volume": "the volume of the spatial region bounded by the plates.",
}
SPYCE_URL["pltvol"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pltvol_c.html"

#########################################
SPYCE_SIGNATURES ["pl2nvc"] = ["float[4]"]
SPYCE_ARGNAMES   ["pl2nvc"] = ["plane"]
SPYCE_RETURNS    ["pl2nvc"] = ["float[3]", "float"]
SPYCE_RETNAMES   ["pl2nvc"] = ["normal", "constant"]
SPYCE_ABSTRACT   ["pl2nvc"] = """
Return a unit normal vector and constant that define a specified plane.
"""
SPYCE_DEFINITIONS["pl2nvc"] = {
"plane": "A CSPICE plane.",
"normal": "A normal vector defining the geometric plane.",
"constant": "A constant defining the geometric plane.",
}
SPYCE_URL["pl2nvc"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pl2nvc_c.html"

#########################################
SPYCE_SIGNATURES ["pl2nvp"] = ["float[4]"]
SPYCE_ARGNAMES   ["pl2nvp"] = ["plane"]
SPYCE_RETURNS    ["pl2nvp"] = 2*["float[3]"]
SPYCE_RETNAMES   ["pl2nvp"] = ["normal", "point"]
SPYCE_ABSTRACT   ["pl2nvp"] = """
Return a unit normal vector and point that define a specified plane.
"""
SPYCE_DEFINITIONS["pl2nvp"] = {
"plane": "A CSPICE plane.",
"normal": "A unit normal vector defining the plane.",
"point": "A point that defines plane.",
}
SPYCE_URL["pl2nvp"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pl2nvp_c.html"

#########################################
SPYCE_SIGNATURES ["pl2psv"] = ["float[4]"]
SPYCE_ARGNAMES   ["pl2psv"] = ["plane"]
SPYCE_RETURNS    ["pl2psv"] = 3*["float[3]"]
SPYCE_RETNAMES   ["pl2psv"] = ["point", "span1", "span2"]
SPYCE_ABSTRACT   ["pl2psv"] = """
Return a point and two orthogonal spanning vectors that generate a
specified plane.
"""
SPYCE_DEFINITIONS["pl2psv"] = {
"plane": "A CSPICE plane.",
"point": "A point in the input plane.",
"span1": "The first of two vectors spanning the input plane.",
"span2": "The second of two vectors spanning the input plane.",
}
SPYCE_URL["pl2psv"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pl2psv_c.html"

#########################################
SPYCE_SIGNATURES ["prop2b"] = ["float", "float[6]", "float"]
SPYCE_ARGNAMES   ["prop2b"] = ["gm", "pvinit", "dt"]
SPYCE_RETURNS    ["prop2b"] = ["float[6]"]
SPYCE_RETNAMES   ["prop2b"] = ["pvprop"]
SPYCE_ABSTRACT   ["prop2b"] = """
Given a central mass and the state of massless body at time t_0, this
routine determines the state as predicted by a two-body force model at
time t_0 + dt.
"""
SPYCE_DEFINITIONS["prop2b"] = {
"gm": "Gravity of the central mass.",
"pvinit": "Initial state from which to propagate a state.",
"dt": "Time offset from initial state to propagate to.",
"pvprop": "The propagated state.",
}
SPYCE_URL["prop2b"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/prop2b_c.html"

#########################################
SPYCE_SIGNATURES ["psv2pl"] = 3*["float[3]"]
SPYCE_ARGNAMES   ["psv2pl"] = ["point", "span1", "span2"]
SPYCE_RETURNS    ["psv2pl"] = ["float[4]"]
SPYCE_RETNAMES   ["psv2pl"] = ["plane"]
SPYCE_ABSTRACT   ["psv2pl"] = """
Make a CSPICE plane from a point and two spanning vectors.
"""
SPYCE_DEFINITIONS["psv2pl"] = {
"point": "A point in the plane.",
"span1": "The first of two vectors spanning the plane.",
"span2": "The second of two vectors spanning the plane.",
"plane": "A CSPICE plane representing the plane.",
}
SPYCE_URL["psv2pl"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/psv2pl_c.html"

#########################################
SPYCE_SIGNATURES ["pxform"] = ["frame_name", "frame_name", "time"]
SPYCE_ARGNAMES   ["pxform"] = ["fromfr", "tofr", "et"]
SPYCE_RETURNS    ["pxform"] = ["rotmat[3,3]"]
SPYCE_RETNAMES   ["pxform"] = ["rotate"]
SPYCE_ABSTRACT   ["pxform"] = """
Return the matrix that transforms position vectors from one specified
frame to another at a specified epoch.
"""
SPYCE_DEFINITIONS["pxform"] = {
"fromfr": "Name of the frame to transform from.",
"tofr": "Name of the frame to transform to.",
"et": "Epoch of the rotation matrix.",
"rotate": "A rotation matrix.",
}
SPYCE_URL["pxform"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pxform_c.html"

#########################################
SPYCE_SIGNATURES ["pxfrm2"] = ["frame_name", "frame_name", "time", "time"]
SPYCE_ARGNAMES   ["pxfrm2"] = ["fromfr", "tofr", "etfrom", "etto"]
SPYCE_RETURNS    ["pxfrm2"] = ["rotmat[3,3]"]
SPYCE_RETNAMES   ["pxfrm2"] = ["rotate"]
SPYCE_ABSTRACT   ["pxfrm2"] = """
Return the 3x3 matrix that transforms position vectors from one
specified frame at a specified epoch to another specified frame at
another specified epoch.
"""
SPYCE_DEFINITIONS["pxfrm2"] = {
"fromfr": "Name of the frame to transform from.",
"tofr": "Name of the frame to transform to.",
"etfrom": "Evaluation time of `from' frame.",
"etto": "Evaluation time of `to' frame.",
"rotate": "A position transformation matrix from frame `from' to frame `to'.",
}
SPYCE_URL["pxfrm2"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pxfrm2_c.html"

#########################################
SPYCE_SIGNATURES ["q2m"] = ["float[4]"]
SPYCE_ARGNAMES   ["q2m"] = ["q"]
SPYCE_RETURNS    ["q2m"] = ["rotmat[3,3]"]
SPYCE_RETNAMES   ["q2m"] = ["r"]
SPYCE_ABSTRACT   ["q2m"] = """
Find the rotation matrix corresponding to a specified unit quaternion.
"""
SPYCE_DEFINITIONS["q2m"] = {
"q": "A unit quaternion.",
"r": "A rotation matrix corresponding to q.",
}
SPYCE_URL["q2m"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/q2m_c.html"

#########################################
SPYCE_SIGNATURES ["qcktrc"] = []
SPYCE_ARGNAMES   ["qcktrc"] = []
SPYCE_RETURNS    ["qcktrc"] = ["string"]
SPYCE_RETNAMES   ["qcktrc"] = ["trace"]
SPYCE_ABSTRACT   ["qcktrc"] = """
Return a string containing a traceback.
"""
SPYCE_DEFINITIONS["qcktrc"] = {
"trace": "A traceback string.",
}
SPYCE_URL["qcktrc"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/qcktrc_c.html"

#########################################
SPYCE_SIGNATURES ["qdq2av"] = ["float[4]", "float[4]"]
SPYCE_ARGNAMES   ["qdq2av"] = ["q", "dq"]
SPYCE_RETURNS    ["qdq2av"] = ["float[3]"]
SPYCE_RETNAMES   ["qdq2av"] = ["av"]
SPYCE_ABSTRACT   ["qdq2av"] = """
Derive angular velocity from a unit quaternion and its derivative with
respect to time.
"""
SPYCE_DEFINITIONS["qdq2av"] = {
"q" : "Unit SPICE quaternion.",
"dq": "Derivative of `q' with respect to time.",
"av": "Angular velocity defined by q and dq.",
}
SPYCE_URL["qdq2av"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/qdq2av_c.html"

#########################################
SPYCE_SIGNATURES ["qxq"] = ["float[4]", "float[4]"]
SPYCE_ARGNAMES   ["qxq"] = ["q1", "q2"]
SPYCE_RETURNS    ["qxq"] = ["float[4]"]
SPYCE_RETNAMES   ["qxq"] = ["qout"]
SPYCE_ABSTRACT   ["qxq"] = """
Multiply two quaternions.
"""
SPYCE_DEFINITIONS["qxq"] = {
"q1": "First SPICE quaternion factor.",
"q2": "Second SPICE quaternion factor.",
"qout": "Product of `q1' and `q2'.",
}
SPYCE_URL["qxq"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/qxq_c.html"

#########################################
SPYCE_SIGNATURES ["radrec"] = 3*["float"]
SPYCE_ARGNAMES   ["radrec"] = ["range", "ra", "dec"]
SPYCE_RETURNS    ["radrec"] = ["float[3]"]
SPYCE_RETNAMES   ["radrec"] = ["rectan"]
SPYCE_ABSTRACT   ["radrec"] = """
Convert from range, right ascension, and declination to rectangular
coordinates.
"""
SPYCE_DEFINITIONS["radrec"] = {
"range": "Distance of a point from the origin.",
"ra": "Right ascension of point in radians.",
"dec": "Declination of point in radians.",
"rectan": "Rectangular coordinates of the point.",
}
SPYCE_URL["radrec"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/radrec_c.html"

#########################################
SPYCE_SIGNATURES ["rav2xf"] = ["rotmat[3,3]", "float[3]"]
SPYCE_ARGNAMES   ["rav2xf"] = ["rot", "av"]
SPYCE_RETURNS    ["rav2xf"] = ["rotmat[6,6]"]
SPYCE_RETNAMES   ["rav2xf"] = ["xform"]
SPYCE_ABSTRACT   ["rav2xf"] = """
This routine determines from a state transformation matrix the
associated rotation matrix and angular velocity of the rotation.
"""
SPYCE_DEFINITIONS["rav2xf"] = {
"rot": "Rotation matrix.",
"av": "Angular velocity vector.",
"xform": "State transformation associated with rot and av.",
}
SPYCE_URL["rav2xf"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/rav2xf_c.html"

#########################################
SPYCE_SIGNATURES ["raxisa"] = ["rotmat[3,3]"]
SPYCE_ARGNAMES   ["raxisa"] = ["matrix"]
SPYCE_RETURNS    ["raxisa"] = ["float[3]", "float"]
SPYCE_RETNAMES   ["raxisa"] = ["axis", "angle"]
SPYCE_ABSTRACT   ["raxisa"] = """
Compute the axis of the rotation given by an input matrix and the angle
of the rotation about that axis.
"""
SPYCE_DEFINITIONS["raxisa"] = {
"matrix": "3x3 rotation matrix in double precision.",
"axis": "Axis of the rotation.",
"angle": "Angle through which the rotation is performed.",
}
SPYCE_URL["raxisa"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/raxisa_c.html"

#########################################
SPYCE_SIGNATURES ["reccyl"] = ["float[3]"]
SPYCE_ARGNAMES   ["reccyl"] = ["rectan"]
SPYCE_RETURNS    ["reccyl"] = 3*["float"]
SPYCE_RETNAMES   ["reccyl"] = ["r", "lon", "z"]
SPYCE_ABSTRACT   ["reccyl"] = """
Convert from rectangular to cylindrical coordinates.
"""
SPYCE_DEFINITIONS["reccyl"] = {
"rectan": "Rectangular coordinates of a point.",
"r": "Distance of the point from z axis.",
"lon": "Angle (radians) of the point from xZ plane",
"z": "Height of the point above xY plane.",
}
SPYCE_URL["reccyl"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/reccyl_c.html"

#########################################
SPYCE_SIGNATURES ["recgeo"] = ["float[3]", "float", "float"]
SPYCE_ARGNAMES   ["recgeo"] = ["rectan", "re", "f"]
SPYCE_RETURNS    ["recgeo"] = 3*["float"]
SPYCE_RETNAMES   ["recgeo"] = ["lon", "lat", "alt"]
SPYCE_ABSTRACT   ["recgeo"] = """
Convert from rectangular coordinates to geodetic coordinates.
"""
SPYCE_DEFINITIONS["recgeo"] = {
"rectan": "Rectangular coordinates of a point.",
"re": "Equatorial radius of the reference spheroid.",
"f": "Flattening coefficient.",
"lon": "Geodetic longitude of the point (radians).",
"lat": "Geodetic latitude  of the point (radians).",
"alt": "Altitude of the point above reference spheroid.",
}
SPYCE_URL["recgeo"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/recgeo_c.html"

#########################################
SPYCE_SIGNATURES ["reclat"] = ["float[3]"]
SPYCE_ARGNAMES   ["reclat"] = ["rectan"]
SPYCE_RETURNS    ["reclat"] = 3*["float"]
SPYCE_RETNAMES   ["reclat"] = ["radius", "lon", "lat"]
SPYCE_ABSTRACT   ["reclat"] = """
Convert from rectangular coordinates to latitudinal coordinates.
"""
SPYCE_DEFINITIONS["reclat"] = {
"rectan": "Rectangular coordinates of a point.",
"radius": "Distance of the point from the origin.",
"lon": "Longitude of the point in radians.",
"lat": "Latitude of the point in radians.",
}
SPYCE_URL["reclat"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/reclat_c.html"

#########################################
SPYCE_SIGNATURES ["recpgr"] = ["body_name", "float[3]", "float", "float"]
SPYCE_ARGNAMES   ["recpgr"] = ["body", "rectan", "re", "f"]
SPYCE_RETURNS    ["recpgr"] = 3*["float"]
SPYCE_RETNAMES   ["recpgr"] = ["lon", "lat", "alt"]
SPYCE_ABSTRACT   ["recpgr"] = """
Convert rectangular coordinates to planetographic coordinates.
"""
SPYCE_DEFINITIONS["recpgr"] = {
"body": "Body with which coordinate system is associated.",
"rectan": "Rectangular coordinates of a point.",
"re": "Equatorial radius of the reference spheroid.",
"f": "Flattening coefficient.",
"lon": "Planetographic longitude of the point (radians).",
"lat": "Planetographic latitude of the point (radians).",
"alt": "Altitude of the point above reference spheroid.",
}
SPYCE_URL["recpgr"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/recpgr_c.html"

#########################################
SPYCE_SIGNATURES ["recrad"] = ["float[3]"]
SPYCE_ARGNAMES   ["recrad"] = ["rectan"]
SPYCE_RETURNS    ["recrad"] = 3*["float"]
SPYCE_RETNAMES   ["recrad"] = ["range", "ra", "dec"]
SPYCE_ABSTRACT   ["recrad"] = """
Convert rectangular coordinates to range, right ascension, and
declination.
"""
SPYCE_DEFINITIONS["recrad"] = {
"rectan": "Rectangular coordinates of a point.",
"range": "Distance of the point from the origin.",
"ra": "Right ascension in radians.",
"dec": "Declination in radians.",
}
SPYCE_URL["recrad"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/recrad_c.html"

#########################################
SPYCE_SIGNATURES ["recsph"] = ["float[3]"]
SPYCE_ARGNAMES   ["recsph"] = ["rectan"]
SPYCE_RETURNS    ["recsph"] = 3*["float"]
SPYCE_RETNAMES   ["recsph"] = ["r", "colat", "lon"]
SPYCE_ABSTRACT   ["recsph"] = """
Convert from rectangular coordinates to spherical coordinates.
"""
SPYCE_DEFINITIONS["recsph"] = {
"rectan": "Rectangular coordinates of a point.",
"r": "Distance of the point from the origin.",
"colat": "Angle of the point from the positive Z-axis.",
"lon": "Longitude of the point in radians.",
}
SPYCE_URL["recsph"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/recsph_c.html"

#########################################
SPYCE_SIGNATURES ["refchg"] = ["frame_code", "frame_code", "time"]
SPYCE_ARGNAMES   ["refchg"] = ["frame1", "frame2", "et"]
SPYCE_RETURNS    ["refchg"] = ["rotmat[3,3]"]
SPYCE_RETNAMES   ["refchg"] = ["rotate"]
SPYCE_ABSTRACT   ["refchg"] = """
Return the transformation matrix from one frame to another.
"""
SPYCE_DEFINITIONS["refchg"] = {
"frame1": "the frame id-code for some reference frame",
"frame2": "the frame id-code for some reference frame",
"et"    : "an epoch in TDB seconds past J2000.",
"rotate": "a rotation matrix.",
}
SPYCE_URL["refchg"] = ""

#########################################
SPYCE_SIGNATURES ["repmc"] = ["string", "string", "string"]
SPYCE_ARGNAMES   ["repmc"] = ["instr", "marker", "value"]
SPYCE_RETURNS    ["repmc"] = ["string"]
SPYCE_RETNAMES   ["repmc"] = ["out"]
SPYCE_ABSTRACT   ["repmc"] = """
Replace a marker with a character string.
"""
SPYCE_DEFINITIONS["repmc"] = {
"instr" : "Input string.",
"marker": "Marker to be replaced.",
"value" : "Replacement value.",
"out"   : "Output string.",
}
SPYCE_URL["repmc"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/repmc_c.html"

#########################################
SPYCE_SIGNATURES ["repmct"] = ["string", "string", "int", "string"]
SPYCE_ARGNAMES   ["repmct"] = ["instr", "marker", "value", "repcase"]
SPYCE_RETURNS    ["repmct"] = ["string"]
SPYCE_RETNAMES   ["repmct"] = ["out"]
SPYCE_ABSTRACT   ["repmct"] = """
Replace a marker with the text representation of a cardinal number.
"""
SPYCE_DEFINITIONS["repmct"] = {
"instr"  : "Input string.",
"marker" : "Marker to be replaced.",
"value"  : "Replacement value.",
"repcase": "Case of replacement text: \"U\" = UPPPERCASE; \"L\" = lowercase; \"C\" = Capitalized.",
"out"    : "Output string.",
}
SPYCE_URL["repmct"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/repmct_c.html"

#########################################
SPYCE_SIGNATURES ["repmd"] = ["string", "string", "float", "int"]
SPYCE_ARGNAMES   ["repmd"] = ["instr", "marker", "value", "sigdig"]
SPYCE_RETURNS    ["repmd"] = ["string"]
SPYCE_RETNAMES   ["repmd"] = ["out"]
SPYCE_ABSTRACT   ["repmd"] = """
Replace a marker with a double precision number.
"""
SPYCE_DEFINITIONS["repmd"] = {
"instr": "Input string.",
"marker": "Marker to be replaced.",
"value": "Replacement value.",
"sigdig": "Significant digits in replacement text.",
"out": "Output string.",
}
SPYCE_URL["repmd"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/repmd_c.html"

#########################################
SPYCE_SIGNATURES ["repmf"] = ["string", "string", "float", "int", "string"]
SPYCE_ARGNAMES   ["repmf"] = ["instr", "marker", "value", "sigdig", "format"]
SPYCE_RETURNS    ["repmf"] = ["string"]
SPYCE_RETNAMES   ["repmf"] = ["out"]
SPYCE_ABSTRACT   ["repmf"] = """
Replace a marker in a string with a formatted double precision value.
"""
SPYCE_DEFINITIONS["repmf"] = {
"instr": "Input string.",
"marker": "Marker to be replaced.",
"value": "Replacement value.",
"sigdig": "Significant digits in replacement text.",
"format": "Format: \"E\" or \"F\".",
"out": "Output string.",
}
SPYCE_URL["repmf"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/repmf_c.html"

#########################################
SPYCE_SIGNATURES ["repmi"] = ["string", "string", "int"]
SPYCE_ARGNAMES   ["repmi"] = ["instr", "marker", "value"]
SPYCE_RETURNS    ["repmi"] = ["string"]
SPYCE_RETNAMES   ["repmi"] = ["out"]
SPYCE_ABSTRACT   ["repmi"] = """
Replace a marker with an integer.
"""
SPYCE_DEFINITIONS["repmi"] = {
"instr": "Input string.",
"marker": "Marker to be replaced.",
"value": "Replacement value.",
"out": "Output string.",
}
SPYCE_URL["repmi"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/repmi_c.html"

#########################################
SPYCE_SIGNATURES ["repmot"] = ["string", "string", "int", "string"]
SPYCE_ARGNAMES   ["repmot"] = ["instr", "marker", "value", "repcase"]
SPYCE_RETURNS    ["repmot"] = ["string"]
SPYCE_RETNAMES   ["repmot"] = ["out"]
SPYCE_ABSTRACT   ["repmot"] = """
Replace a marker with the text representation of an ordinal number.
"""
SPYCE_DEFINITIONS["repmot"] = {
"instr": "Input string.",
"marker": "Marker to be replaced.",
"value": "Replacement value.",
"repcase": "Case of replacement text (\"U\" for UPPERCASE, \"L\" for lowercase, \"C\" for Capitalized).",
"out": "Output string.",
}
SPYCE_URL["repmot"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/repmot_c.html"

#########################################
SPYCE_SIGNATURES ["reset"] = []
SPYCE_ARGNAMES   ["reset"] = []
SPYCE_RETURNS    ["reset"] = []
SPYCE_RETNAMES   ["reset"] = []
SPYCE_ABSTRACT   ["reset"] = """
Reset the CSPICE error status to a value of "no error." as a result, the
status routine, failed, will return a value of False.
"""
SPYCE_DEFINITIONS["reset"] = {}
SPYCE_URL["reset"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/reset_c.html"

#########################################
SPYCE_SIGNATURES ["rotate"] = ["float", "int"]
SPYCE_ARGNAMES   ["rotate"] = ["angle", "iaxis"]
SPYCE_RETURNS    ["rotate"] = ["rotmat[3,3]"]
SPYCE_RETNAMES   ["rotate"] = ["mout"]
SPYCE_ABSTRACT   ["rotate"] = """
Calculate the 3x3 rotation matrix generated by a rotation of a specified
angle about a specified axis. This rotation is thought of as rotating
the coordinate system.
"""
SPYCE_DEFINITIONS["rotate"] = {
"angle": "Angle of rotation (radians).",
"iaxis": "Axis of rotation (X=1, Y=2, Z=3).",
"mout": "Resulting rotation matrix.",
}
SPYCE_URL["rotate"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/rotate_c.html"

#########################################
SPYCE_SIGNATURES ["rotmat"] = ["rotmat[3,3]", "float", "int"]
SPYCE_ARGNAMES   ["rotmat"] = ["m1", "angle", "iaxis"]
SPYCE_RETURNS    ["rotmat"] = ["rotmat[3,3]"]
SPYCE_RETNAMES   ["rotmat"] = ["mout"]
SPYCE_ABSTRACT   ["rotmat"] = """
Apply a rotation of angle radians about axis iaxis to a matrix. This
rotation is thought of as rotating the coordinate system.
"""
SPYCE_DEFINITIONS["rotmat"] = {
"m1": "Matrix to be rotated.",
"angle": "Angle of rotation (radians).",
"iaxis": "Axis of rotation (X=1, Y=2, Z=3).",
"mout": "Resulting rotated matrix.",
}
SPYCE_URL["rotmat"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/rotmat_c.html"

#########################################
SPYCE_SIGNATURES ["rotvec"] = ["float[3]", "float", "int"]
SPYCE_ARGNAMES   ["rotvec"] = ["v1", "angle", "iaxis"]
SPYCE_RETURNS    ["rotvec"] = ["float[3]"]
SPYCE_RETNAMES   ["rotvec"] = ["vout"]
SPYCE_ABSTRACT   ["rotvec"] = """
Transform a vector to a new coordinate system rotated by angle radians
about axis iaxis.  This transformation rotates v1 by -angle radians
about the specified axis.
"""
SPYCE_DEFINITIONS["rotvec"] = {
"v1": " Vector whose coordinate system is to be rotated.",
"angle": " Angle of rotation in radians.",
"iaxis": " Axis of rotation (X=1, Y=2, Z=3).",
"vout": "Resulting vector[angle]",
}
SPYCE_URL["rotvec"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/rotvec_c.html"

#########################################
SPYCE_SIGNATURES ["rpd"] = []
SPYCE_ARGNAMES   ["rpd"] = []
SPYCE_RETURNS    ["rpd"] = ["float"]
SPYCE_RETNAMES   ["rpd"] = ["value"]
SPYCE_ABSTRACT   ["rpd"] = """
Return the number of radians per degree.
"""
SPYCE_DEFINITIONS["rpd"] = {
"value": "radians per degree"
}
SPYCE_URL["rpd"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/rpd_c.html"

#########################################
SPYCE_SIGNATURES ["rquad"] = 3*["float"]
SPYCE_ARGNAMES   ["rquad"] = ["a", "b", "c"]
SPYCE_RETURNS    ["rquad"] = 2*["float[2]"]
SPYCE_RETNAMES   ["rquad"] = ["root1", "root2"]
SPYCE_ABSTRACT   ["rquad"] = """
Find the roots of a quadratic equation.
"""
SPYCE_DEFINITIONS["rquad"] = {
"a": "Coefficient of quadratic term.",
"b": "Coefficient of linear term.",
"c": "Constant.",
"root1": "Root built from positive discriminant term.",
"root2": "Root built from negative discriminant term.",
}
SPYCE_URL["rquad"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/rquad_c.html"

#########################################
SPYCE_SIGNATURES ["saelgv"] = 2*["float[3]"]
SPYCE_ARGNAMES   ["saelgv"] = ["vec1", "vec2"]
SPYCE_RETURNS    ["saelgv"] = 2*["float[3]"]
SPYCE_RETNAMES   ["saelgv"] = ["smajor", "sminor"]
SPYCE_ABSTRACT   ["saelgv"] = """
Find semi-axis vectors of an ellipse generated by two arbitrary
three-dimensional vectors.
"""
SPYCE_DEFINITIONS["saelgv"] = {
"vec1": "The first of two vectors used to generate an ellipse.",
"vec2": "The second of two vectors used to generate an ellipse.",
"smajor": "Semi-major axis of ellipse.",
"sminor": "Semi-minor axis of ellipse.",
}
SPYCE_URL["saelgv"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/saelgv_c.html"

#########################################
SPYCE_SIGNATURES ["scdecd"] = ["body_code", "float"]
SPYCE_ARGNAMES   ["scdecd"] = ["sc", "sclkdp"]
SPYCE_RETURNS    ["scdecd"] = ["string"]
SPYCE_RETNAMES   ["scdecd"] = ["sclkch"]
SPYCE_ABSTRACT   ["scdecd"] = """
Convert double precision encoding of spacecraft clock time into a
character representation.
"""
SPYCE_DEFINITIONS["scdecd"] = {
"sc": "NAIF spacecraft identification code.",
"sclkdp": "Encoded representation of a spacecraft clock count.",
"sclkch": "Character representation of a clock count.",
}
SPYCE_URL["scdecd"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/scdecd_c.html"

#########################################
SPYCE_SIGNATURES ["sce2c"] = ["body_code", "time"]
SPYCE_ARGNAMES   ["sce2c"] = ["sc", "et"]
SPYCE_RETURNS    ["sce2c"] = ["float"]
SPYCE_RETNAMES   ["sce2c"] = ["sclkdp"]
SPYCE_ABSTRACT   ["sce2c"] = """
Convert ephemeris seconds past j2000 (ET) to continuous encoded
spacecraft clock (`ticks').  Non-integral tick values may be returned.
"""
SPYCE_DEFINITIONS["sce2c"] = {
"sc": "NAIF spacecraft ID code.",
"et": "Ephemeris time, seconds past j2000.",
"sclkdp": "SCLK, encoded as ticks since spacecraft clock start. sclkdp need not be integral.",
}
SPYCE_URL["sce2c"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sce2c_c.html"

#########################################
SPYCE_SIGNATURES ["sce2s"] = ["body_code", "time"]
SPYCE_ARGNAMES   ["sce2s"] = ["sc", "et"]
SPYCE_RETURNS    ["sce2s"] = ["string"]
SPYCE_RETNAMES   ["sce2s"] = ["sclkch"]
SPYCE_ABSTRACT   ["sce2s"] = """
Convert an epoch specified as ephemeris seconds past J2000 (ET) to a
character string representation of a spacecraft clock value (SCLK).
"""
SPYCE_DEFINITIONS["sce2s"] = {
"sc": "NAIF spacecraft clock ID code.",
"et": "Ephemeris time, specified as seconds past J2000.",
"sclkch": "An SCLK string.",
}
SPYCE_URL["sce2s"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sce2s_c.html"

#########################################
SPYCE_SIGNATURES ["sce2t"] = ["body_code", "time"]
SPYCE_ARGNAMES   ["sce2t"] = ["sc", "et"]
SPYCE_RETURNS    ["sce2t"] = ["float"]
SPYCE_RETNAMES   ["sce2t"] = ["sclkdp"]
SPYCE_ABSTRACT   ["sce2t"] = """
Convert ephemeris seconds past J2000 (ET) to integral encoded spacecraft
clock (`ticks'). For conversion to fractional ticks, (required for
C-kernel production), see the routine sce2c.
"""
SPYCE_DEFINITIONS["sce2t"] = {
"sc": "NAIF spacecraft ID code.",
"et": "Ephemeris time, seconds past J2000.",
"sclkdp": "SCLK, encoded as ticks since spacecraft clock start.",
}
SPYCE_URL["sce2t"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sce2t_c.html"

#########################################
SPYCE_SIGNATURES ["scencd"] = ["body_code", "string"]
SPYCE_ARGNAMES   ["scencd"] = ["sc", "sclkch"]
SPYCE_RETURNS    ["scencd"] = ["float"]
SPYCE_RETNAMES   ["scencd"] = ["sclkdp"]
SPYCE_ABSTRACT   ["scencd"] = """
Encode character representation of spacecraft clock time into a double
precision number.
"""
SPYCE_DEFINITIONS["scencd"] = {
"sc": "NAIF spacecraft identification code.",
"sclkch": "Character representation of a spacecraft clock.",
"sclkdp": "Encoded representation of the clock count.",
}
SPYCE_URL["scencd"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/scencd_c.html"

#########################################
SPYCE_SIGNATURES ["scfmt"] = ["body_code", "float"]
SPYCE_ARGNAMES   ["scfmt"] = ["sc", "ticks"]
SPYCE_RETURNS    ["scfmt"] = ["string"]
SPYCE_RETNAMES   ["scfmt"] = ["clkstr"]
SPYCE_ABSTRACT   ["scfmt"] = """
Convert encoded spacecraft clock ticks to character clock format.
"""
SPYCE_DEFINITIONS["scfmt"] = {
"sc": "NAIF spacecraft identification code.",
"ticks": "Encoded representation of a spacecraft clock count.",
"clkstr": "Character representation of a clock count.",
}
SPYCE_URL["scfmt"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/scfmt_c.html"

#########################################
SPYCE_SIGNATURES ["scpart"] = ["body_code"]
SPYCE_ARGNAMES   ["scpart"] = ["sc"]
SPYCE_RETURNS    ["scpart"] = 2*["float"]
SPYCE_RETNAMES   ["scpart"] = ["pstart", "pstop"]
SPYCE_ABSTRACT   ["scpart"] = """
Get spacecraft clock partition information from a spacecraft clock
kernel file.
"""
SPYCE_DEFINITIONS["scpart"] = {
"sc": "NAIF spacecraft identification code.",
"pstart": "Array of partition start times.",
"pstop": "Array of partition stop times.",
}
SPYCE_URL["scpart"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/scpart_c.html"

#########################################
SPYCE_SIGNATURES ["scs2e"] = ["body_code", "string"]
SPYCE_ARGNAMES   ["scs2e"] = ["sc", "sclkch"]
SPYCE_RETURNS    ["scs2e"] = ["float"]
SPYCE_RETNAMES   ["scs2e"] = ["et"]
SPYCE_ABSTRACT   ["scs2e"] = """
Convert a spacecraft clock string to ephemeris seconds past J2000 (ET).
"""
SPYCE_DEFINITIONS["scs2e"] = {
"sc": "NAIF integer code for a spacecraft.",
"sclkch": "An SCLK string.",
"et": "Ephemeris time, seconds past J2000.",
}
SPYCE_URL["scs2e"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/scs2e_c.html"

#########################################
SPYCE_SIGNATURES ["sct2e"] = ["body_code", "float"]
SPYCE_ARGNAMES   ["sct2e"] = ["sc", "sclkdp"]
SPYCE_RETURNS    ["sct2e"] = ["float"]
SPYCE_RETNAMES   ["sct2e"] = ["et"]
SPYCE_ABSTRACT   ["sct2e"] = """
Convert encoded spacecraft clock (`ticks') to ephemeris seconds past
J2000 (ET).
"""
SPYCE_DEFINITIONS["sct2e"] = {
"sc": "NAIF spacecraft ID code.",
"sclkdp": "SCLK, encoded as ticks since spacecraft clock start.",
"et": "Ephemeris time, seconds past J2000.",
}
SPYCE_URL["sct2e"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sct2e_c.html"

#########################################
SPYCE_SIGNATURES ["sctiks"] = ["body_code", "string"]
SPYCE_ARGNAMES   ["sctiks"] = ["sc", "clkstr"]
SPYCE_RETURNS    ["sctiks"] = ["float"]
SPYCE_RETNAMES   ["sctiks"] = ["ticks"]
SPYCE_ABSTRACT   ["sctiks"] = """
Convert a spacecraft clock format string to number of "ticks".
"""
SPYCE_DEFINITIONS["sctiks"] = {
"sc": "NAIF spacecraft identification code.",
"clkstr": "Character representation of a spacecraft clock.",
"ticks": "Number of ticks represented by the clock string.",
}
SPYCE_URL["sctiks"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sctiks_c.html"

#########################################
SPYCE_SIGNATURES ["setmsg"] = ["string"]
SPYCE_ARGNAMES   ["setmsg"] = ["message"]
SPYCE_RETURNS    ["setmsg"] = []
SPYCE_RETNAMES   ["setmsg"] = []
SPYCE_ABSTRACT   ["setmsg"] = """
Set the value of the current long error message.
"""
SPYCE_DEFINITIONS["setmsg"] = {
"message": "A long error message.",
}
SPYCE_URL["setmsg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/setmsg_c.html"

#########################################
SPYCE_SIGNATURES ["sigerr"] = ["string"]
SPYCE_ARGNAMES   ["sigerr"] = ["message"]
SPYCE_RETURNS    ["sigerr"] = []
SPYCE_RETNAMES   ["sigerr"] = []
SPYCE_ABSTRACT   ["sigerr"] = """
Inform the CSPICE error processing mechanism that an error has occurred,
and specify the type of error.
"""
SPYCE_DEFINITIONS["sigerr"] = {
"message": "A short error message.",
}
SPYCE_URL["sigerr"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sigerr_c.html"

#########################################
SPYCE_SIGNATURES ["sincpt"] = ["string", "body_name", "time", "frame_name", "string", "body_name", "frame_name", "float[3]"]
SPYCE_ARGNAMES   ["sincpt"] = ["method", "target", "et", "fixref", "abcorr", "obsrvr", "dref", "dvec"]
SPYCE_RETURNS    ["sincpt"] = ["float[3]", "time", "float[3]", "bool"]
SPYCE_RETNAMES   ["sincpt"] = ["spoint", "trgepc", "srfvec", "found"]
SPYCE_ABSTRACT   ["sincpt"] = """
Given an observer and a direction vector defining a ray, compute the
surface intercept of the ray on a target body at a specified epoch,
optionally corrected for light time and stellar aberration.

The surface of the target body may be represented by a triaxial
ellipsoid or by topographic data provided by DSK files.

This routine supersedes srfxpt.
"""
SPYCE_DEFINITIONS["sincpt"] = {
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
SPYCE_URL["sincpt"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sincpt_c.html"

#########################################
SPYCE_SIGNATURES ["spd"] = []
SPYCE_ARGNAMES   ["spd"] = []
SPYCE_RETURNS    ["spd"] = ["float"]
SPYCE_RETNAMES   ["spd"] = ["value"]
SPYCE_ABSTRACT   ["spd"] = """
Return the number of seconds in a day.
"""
SPYCE_DEFINITIONS["spd"] = {
"value": "number of seconds per day",
}
SPYCE_URL["spd"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spd_c.html"

#########################################
SPYCE_SIGNATURES ["sphcyl"] = 3*["float"]
SPYCE_ARGNAMES   ["sphcyl"] = ["radius", "colat", "lon"]
SPYCE_RETURNS    ["sphcyl"] = 3*["float"]
SPYCE_RETNAMES   ["sphcyl"] = ["r", "lon2", "z"]
SPYCE_ABSTRACT   ["sphcyl"] = """
This routine converts from spherical coordinates to cylindrical
coordinates.
"""
SPYCE_DEFINITIONS["sphcyl"] = {
"radius": "Distance of point from origin.",
"colat" : "Polar angle (co-latitude in radians) of point.",
"lon"   : "Azimuthal angle (longitude) of point (radians).",
"r"     : "Distance of point from z axis.",
"lon2"  : "angle (radians) of point from XZ plane.",
"z"     : "Height of point above XY plane.",
}
SPYCE_URL["sphcyl"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sphcyl_c.html"

#########################################
SPYCE_SIGNATURES ["sphlat"] = 3*["float"]
SPYCE_ARGNAMES   ["sphlat"] = ["radius", "colat", "lon"]
SPYCE_RETURNS    ["sphlat"] = 3*["float"]
SPYCE_RETNAMES   ["sphlat"] = ["r", "lon2", "lat"]
SPYCE_ABSTRACT   ["sphlat"] = """
Convert from spherical coordinates to latitudinal coordinates.
"""
SPYCE_DEFINITIONS["sphlat"] = {
"r": "Distance of the point from the origin.",
"colat": "Angle of the point from positive z axis (radians).",
"lon": "Angle of the point from the XZ plane (radians).",
"radius": "Distance of a point from the origin",
"lon2": "Angle of the point from the XZ plane in radians",
"lat": "Angle of the point from the XY plane in radians",
}
SPYCE_URL["sphlat"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sphlat_c.html"

#########################################
SPYCE_SIGNATURES ["sphrec"] = 3*["float"]
SPYCE_ARGNAMES   ["sphrec"] = ["radius", "colat", "lon"]
SPYCE_RETURNS    ["sphrec"] = ["float[3]"]
SPYCE_RETNAMES   ["sphrec"] = ["rectan"]
SPYCE_ABSTRACT   ["sphrec"] = """
Convert from spherical coordinates to rectangular coordinates.
"""
SPYCE_DEFINITIONS["sphrec"] = {
"radius": "Distance of a point from the origin.",
"colat" : "Angle of the point from the positive Z-axis.",
"lon"   : "Angle of the point from the XZ plane in radians.",
"rectan": "Rectangular coordinates of the point.",
}
SPYCE_URL["sphrec"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sphrec_c.html"

#########################################
SPYCE_SIGNATURES ["spkacs"] = ["body_code", "time", "frame_name", "string", "body_code"]
SPYCE_ARGNAMES   ["spkacs"] = ["targ", "et", "ref", "abcorr", "obs"]
SPYCE_RETURNS    ["spkacs"] = ["float[6]", "float", "float"]
SPYCE_RETNAMES   ["spkacs"] = ["starg", "lt", "dlt"]
SPYCE_ABSTRACT   ["spkacs"] = """
Return the state (position and velocity) of a target body relative to an
observer, optionally corrected for light time and stellar aberration,
expressed relative to an inertial reference frame.
"""
SPYCE_DEFINITIONS["spkacs"] = {
"targ": "Target body.",
"et": "Observer epoch.",
"ref": "Inertial reference frame of output state.",
"abcorr": "Aberration correction flag (\"NONE\", \"LT\", \"LT+S\", \"CN\", \"CN+S\", \"XLT\", \"XLT+S\", \"XCN\", or \"XCN+S\").",
"obs": "Observer.",
"starg": "State of target.",
"lt": "One way light time between observer and target.",
"dlt": "Derivative of light time with respect to time.",
}
SPYCE_URL["spkacs"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkacs_c.html"

#########################################
SPYCE_SIGNATURES ["spkapo"] = ["body_code", "time", "frame_name", "float[6]", "string"]
SPYCE_ARGNAMES   ["spkapo"] = ["targ", "et", "ref", "sobs", "abcorr"]
SPYCE_RETURNS    ["spkapo"] = ["float[6]", "float"]
SPYCE_RETNAMES   ["spkapo"] = ["ptarg", "lt"]
SPYCE_ABSTRACT   ["spkapo"] = """
Return the position of a target body relative to an observer, optionally
corrected for light time and stellar aberration.
"""
SPYCE_DEFINITIONS["spkapo"] = {
"targ": "Target body.",
"et": "Observer epoch.",
"ref": "Inertial reference frame of observer's state.",
"sobs": "State of observer wrt. solar system barycenter.",
"abcorr": "Aberration correction flag (\"NONE\", \"LT\", \"LT+S\", \"CN\", \"CN+S\", \"XLT\", \"XLT+S\", \"XCN\", or \"XCN+S\").",
"ptarg": "Position of target.",
"lt": "One way light time between observer and target.",
}
SPYCE_URL["spkapo"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkapo_c.html"

#########################################
SPYCE_SIGNATURES ["spkapp"] = ["body_code", "time", "frame_name", "float[6]", "string"]
SPYCE_ARGNAMES   ["spkapp"] = ["targ", "et", "ref", "sobs", "abcorr"]
SPYCE_RETURNS    ["spkapp"] = ["float[6]", "float"]
SPYCE_RETNAMES   ["spkapp"] = ["starg", "lt"]
SPYCE_ABSTRACT   ["spkapp"] = """
Return the state (position and velocity) of a target body relative to an
observer, optionally corrected for light time and stellar aberration.

WARNING: For aberration-corrected states, the velocity is not precisely
equal to the time derivative of the position. Use spkaps instead.
"""
SPYCE_DEFINITIONS["spkapp"] = {
"targ": "Target body.",
"et": "Observer epoch.",
"ref": "Inertial reference frame of observer's state.",
"sobs": "State of observer wrt. solar system barycenter.",
"abcorr": "Aberration correction flag (\"NONE\", \"LT\", \"LT+S\", \"CN\", \"CN+S\", \"XLT\", \"XLT+S\", \"XCN\", or \"XCN+S\").",
"starg": "State of target.",
"lt": "One way light time between observer and target.",
}
SPYCE_URL["spkapp"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkapp_c.html"

#########################################
SPYCE_SIGNATURES ["spkaps"] = ["body_code", "float", "frame_name", "string", "float[6]", "float[3]"]
SPYCE_ARGNAMES   ["spkaps"] = ["targ", "et", "ref", "abcorr", "stobs", "accobs"]
SPYCE_RETURNS    ["spkaps"] = ["float[6]", "float", "float"]
SPYCE_RETNAMES   ["spkaps"] = ["starg", "lt", "dlt"]
SPYCE_ABSTRACT   ["spkaps"] = """
Given the state and acceleration of an observer relative to the solar
system barycenter, return the state (position and velocity) of a target
body relative to the observer, optionally corrected for light time and
stellar aberration. All input and output vectors are expressed relative
to an inertial reference frame.

This routine supersedes spkapp.

SPICE users normally should call the high-level API routines spkezr or
spkez rather than this routine.
"""
SPYCE_DEFINITIONS["spkaps"] = {
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
SPYCE_URL["spkaps"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkaps_c.html"

#########################################
SPYCE_SIGNATURES ["spkcov"] = ["string", "body_code"]
SPYCE_ARGNAMES   ["spkcov"] = ["spk", "idcode"]
SPYCE_RETURNS    ["spkcov"] = ["float[*,2]"]
SPYCE_RETNAMES   ["spkcov"] = ["cover"]
SPYCE_ABSTRACT   ["spkcov"] = """
Find the coverage window for a specified ephemeris object in a specified
SPK file.
"""
SPYCE_DEFINITIONS["spkcov"] = {
"spk": "Name of SPK file.",
"idcode": "ID code of ephemeris object.",
"cover": "An array of shape (n,2), where cover[:,0] are start times and cover[:,1] are stop times.",
}
SPYCE_URL["spkcov"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkcov_c.html"

SPYCE_SIGNATURES ["spkcov_error"] = ["string", "body_code"]
SPYCE_ARGNAMES   ["spkcov_error"] = ["spk", "idcode"]
SPYCE_RETURNS    ["spkcov_error"] = ["float[*,2]"]
SPYCE_RETNAMES   ["spkcov_error"] = ["cover"]
SPYCE_ABSTRACT   ["spkcov_error"] = """
Find the coverage window for a specified ephemeris object in a specified
SPK file.
"""
SPYCE_DEFINITIONS["spkcov_error"] = {
"spk": "Name of SPK file.",
"idcode": "ID code of ephemeris object.",
"cover": "An array of shape (n,2), where cover[:,0] are start times and cover[:,1] are stop times.",
}
SPYCE_PS ["spkcov_error"] = "Raise KeyError if the idcode is not found."
SPYCE_URL["spkcov_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkcov_c.html"

#########################################
SPYCE_SIGNATURES ["spkez"] = ["body_code", "time", "frame_name", "string", "body_code"]
SPYCE_ARGNAMES   ["spkez"] = ["targ", "et", "ref", "abcorr", "obs"]
SPYCE_RETURNS    ["spkez"] = ["float[6]", "float"]
SPYCE_RETNAMES   ["spkez"] = ["starg", "lt"]
SPYCE_ABSTRACT   ["spkez"] = """
Return the state (position and velocity) of a target body relative to an
observing body, optionally corrected for light time (planetary
aberration) and stellar aberration.
"""
SPYCE_DEFINITIONS["spkez"] = {
"targ": "Target body.",
"et": "Observer epoch.",
"ref": "Reference frame of output state vector.",
"abcorr": "Aberration correction flag (\"NONE\", \"LT\", \"LT+S\", \"CN\", \"CN+S\", \"XLT\", \"XLT+S\", \"XCN\", or \"XCN+S\").",
"obs": "Observing body.",
"starg": "State of target.",
"lt": "One way light time between observer and target.",
}
SPYCE_URL["spkez"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkez_c.html"

#########################################
SPYCE_SIGNATURES ["spkezp"] = ["body_code", "time", "frame_name", "string", "body_code"]
SPYCE_ARGNAMES   ["spkezp"] = ["targ", "et", "ref", "abcorr", "obs"]
SPYCE_RETURNS    ["spkezp"] = ["float[3]", "float"]
SPYCE_RETNAMES   ["spkezp"] = ["ptarg", "lt"]
SPYCE_ABSTRACT   ["spkezp"] = """
Return the position of a target body relative to an observing body,
optionally corrected for light time (planetary aberration) and stellar
aberration.
"""
SPYCE_DEFINITIONS["spkezp"] = {
"targ": "Target body NAIF ID code.",
"et": "Observer epoch.",
"ref": "Reference frame of output position vector.",
"abcorr": "Aberration correction flag (\"NONE\", \"LT\", \"LT+S\", \"CN\", \"CN+S\", \"XLT\", \"XLT+S\", \"XCN\", or \"XCN+S\").",
"obs": "Observing body NAIF ID code.",
"ptarg": "Position of target.",
"lt": "One way light time between observer and target.",
}
SPYCE_URL["spkezp"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkezp_c.html"

#########################################
SPYCE_SIGNATURES ["spkezr"] = ["body_name", "time", "frame_name", "string", "body_name"]
SPYCE_ARGNAMES   ["spkezr"] = ["target", "et", "ref", "abcorr", "obsrvr"]
SPYCE_RETURNS    ["spkezr"] = ["float[6]", "float"]
SPYCE_RETNAMES   ["spkezr"] = ["starg", "lt"]
SPYCE_ABSTRACT   ["spkezr"] = """
Return the state (position and velocity) of a target body relative to an
observing body, optionally corrected for light time (planetary
aberration) and stellar aberration.
"""
SPYCE_DEFINITIONS["spkezr"] = {
"target": "Target body name.",
"et": "Observer epoch.",
"ref": "Reference frame of output state vector.",
"abcorr": "Aberration correction flag (\"NONE\", \"LT\", \"LT+S\", \"CN\", \"CN+S\", \"XLT\", \"XLT+S\", \"XCN\", or \"XCN+S\").",
"obsrvr": "Observing body name.",
"starg": "State of target.",
"lt": "One way light time between observer and target.",
}
SPYCE_URL["spkezr"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkezr_c.html"

#########################################
SPYCE_SIGNATURES ["spkgeo"] = ["body_code", "time", "frame_name", "body_code"]
SPYCE_ARGNAMES   ["spkgeo"] = ["targ", "et", "ref", "obs"]
SPYCE_RETURNS    ["spkgeo"] = ["float[6]", "float"]
SPYCE_RETNAMES   ["spkgeo"] = ["state", "lt"]
SPYCE_ABSTRACT   ["spkgeo"] = """
Compute the geometric state (position and velocity) of a target body
relative to an observing body.
"""
SPYCE_DEFINITIONS["spkgeo"] = {
"targ": "Target body code.",
"et": "Target epoch.",
"ref": "Target reference frame name.",
"obs": "Observing body code.",
"state": "State of target.",
"lt": "Light time.",
}
SPYCE_URL["spkgeo"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkgeo_c.html"

#########################################
SPYCE_SIGNATURES ["spkgps"] = ["body_code", "time", "frame_name", "body_code"]
SPYCE_ARGNAMES   ["spkgps"] = ["targ", "et", "ref", "obs"]
SPYCE_RETURNS    ["spkgps"] = ["float[3]", "float"]
SPYCE_RETNAMES   ["spkgps"] = ["pos", "lt"]
SPYCE_ABSTRACT   ["spkgps"] = """
Compute the geometric position of a target body relative to an observing
body.
"""
SPYCE_DEFINITIONS["spkgps"] = {
"targ": "Target body code.",
"et": "Target epoch.",
"ref": "Target reference frame name.",
"obs": "Observing body code.",
"pos": "Position of target.",
"lt": "Light time.",
}
SPYCE_URL["spkgps"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkgps_c.html"

#########################################
SPYCE_SIGNATURES ["spkltc"] = ["body_code", "time", "frame_name", "string", "float[6]"]
SPYCE_ARGNAMES   ["spkltc"] = ["targ", "et", "ref", "abcorr", "stobs"]
SPYCE_RETURNS    ["spkltc"] = ["float[6]", "float", "float"]
SPYCE_RETNAMES   ["spkltc"] = ["starg", "lt", "dlt"]
SPYCE_ABSTRACT   ["spkltc"] = """
Return the state (position and velocity) of a target body relative to an
observer, optionally corrected for light time, expressed relative to an
inertial reference frame.
"""
SPYCE_DEFINITIONS["spkltc"] = {
"targ": "Target body code.",
"et": "Observer epoch.",
"ref": "Inertial reference frame name of output state.",
"abcorr": "Aberration correction flag, \"NONE\", \"LT\", \"LT+S\", \"CN\", or \"CN+S\".",
"stobs": "State of the observer relative to the SSB.",
"starg": "State of target.",
"lt": "One way light time between observer and target.",
"dlt": "Derivative of light time with respect to time.",
}
SPYCE_URL["spkltc"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkltc_c.html"

#########################################
SPYCE_SIGNATURES ["spkobj"] = ["string"]
SPYCE_ARGNAMES   ["spkobj"] = ["spk"]
SPYCE_RETURNS    ["spkobj"] = ["int[*]"]
SPYCE_RETNAMES   ["spkobj"] = ["ids"]
SPYCE_ABSTRACT   ["spkobj"] = """
Find the set of ID codes of all objects in a specified SPK file.
"""
SPYCE_DEFINITIONS["spkobj"] = {
"spk": "Name of SPK file.",
"ids": "Array of ID codes of objects in SPK file.",
}
SPYCE_URL["spkobj"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkobj_c.html"

#########################################
SPYCE_SIGNATURES ["spkpos"] = ["body_name", "time", "frame_name", "string", "body_name"]
SPYCE_ARGNAMES   ["spkpos"] = ["target", "et", "ref", "abcorr", "obsrvr"]
SPYCE_RETURNS    ["spkpos"] = ["float[3]", "float"]
SPYCE_RETNAMES   ["spkpos"] = ["ptarg", "lt"]
SPYCE_ABSTRACT   ["spkpos"] = """
Return the position of a target body relative to an observing body,
optionally corrected for light time (planetary aberration) and stellar
aberration.
"""
SPYCE_DEFINITIONS["spkpos"] = {
"target": "Target body name.",
"et": "Observer epoch.",
"ref": "Reference frame of output position vector.",
"abcorr": "Aberration correction flag (\"NONE\", \"LT\", \"LT+S\", \"CN\", \"CN+S\", \"XLT\", \"XLT+S\", \"XCN\", or \"XCN+S\").",
"obsrvr": "Observing body name.",
"ptarg": "Position of target.",
"lt": "One way light time between observer and target.",
}
SPYCE_URL["spkpos"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkpos_c.html"

#########################################
SPYCE_SIGNATURES ["spkssb"] = ["body_code", "time", "frame_name"]
SPYCE_ARGNAMES   ["spkssb"] = ["targ", "et", "ref"]
SPYCE_RETURNS    ["spkssb"] = ["float[6]"]
SPYCE_RETNAMES   ["spkssb"] = ["starg"]
SPYCE_ABSTRACT   ["spkssb"] = """
Return the state (position and velocity) of a target body relative to
the solar system barycenter.
"""
SPYCE_DEFINITIONS["spkssb"] = {
"targ": "Target body code.",
"et": "Target epoch.",
"ref": "Target reference frame name.",
"starg": "State of target.",
}
SPYCE_URL["spkssb"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkssb_c.html"

#########################################
SPYCE_SIGNATURES ["srfc2s"] = ["int", "body_code"]
SPYCE_ARGNAMES   ["srfc2s"] = ["code", "bodyid"]
SPYCE_RETURNS    ["srfc2s"] = ["string", "bool"]
SPYCE_RETNAMES   ["srfc2s"] = ["srfstr", "isname"]
SPYCE_ABSTRACT   ["srfc2s"] = """
Translate a surface ID code, together with a body ID code, to the
corresponding surface name. If no such name exists, return a string
representation of the surface ID code.
"""
SPYCE_DEFINITIONS["srfc2s"] = {
"code"  : "Integer surface ID code to translate to a string.",
"bodyid": "ID code of body associated with surface.",
"srfstr": "String corresponding to surface ID code.",
"isname": "True to indicate output is a surface name.",
}
SPYCE_URL["srfc2s"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/srfc2s_c.html"

SPYCE_SIGNATURES ["srfc2s_error"] = ["int", "body_code"]
SPYCE_ARGNAMES   ["srfc2s_error"] = ["code", "bodyid"]
SPYCE_RETURNS    ["srfc2s_error"] = ["string"]
SPYCE_RETNAMES   ["srfc2s_error"] = ["srfstr"]
SPYCE_ABSTRACT   ["srfc2s_error"] = """
Translate a surface ID code, together with a body ID code, to the
corresponding surface name. If no such name exists, raise KeyError.
"""
SPYCE_DEFINITIONS["srfc2s_error"] = {
"code"  : "Integer surface ID code to translate to a string.",
"bodyid": "ID code of body associated with surface.",
"srfstr": "String corresponding to surface ID code.",
}
SPYCE_PS ["srfc2s_error"] = "Raise KeyError if not found."
SPYCE_URL["srfc2s_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/srfc2s_c.html"

#########################################
SPYCE_SIGNATURES ["srfcss"] = ["int", "body_name"]
SPYCE_ARGNAMES   ["srfcss"] = ["code", "bodstr"]
SPYCE_RETURNS    ["srfcss"] = ["string", "bool"]
SPYCE_RETNAMES   ["srfcss"] = ["srfstr", "isname"]
SPYCE_ABSTRACT   ["srfcss"] = """
Translate a surface ID code, together with a body string, to the
corresponding surface name. If no such surface name exists, return a
string representation of the surface ID code.
"""
SPYCE_DEFINITIONS["srfcss"] = {
"code": "Integer surface ID code to translate to a string.",
"bodstr": "Name or ID of body associated with surface.",
"srfstr": "String corresponding to surface ID code.",
"isname": "Flag indicating whether output is a surface name.",
}
SPYCE_URL["srfcss"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/srfcss_c.html"

SPYCE_SIGNATURES ["srfcss_error"] = ["int", "body_name"]
SPYCE_ARGNAMES   ["srfcss_error"] = ["code", "bodstr"]
SPYCE_RETURNS    ["srfcss_error"] = ["string"]
SPYCE_RETNAMES   ["srfcss_error"] = ["srfstr"]
SPYCE_ABSTRACT   ["srfcss_error"] = """
Translate a surface ID code, together with a body string, to the
corresponding surface name. If no such surface name exists, an
exception.
"""
SPYCE_DEFINITIONS["srfcss_error"] = {
"code": "Integer surface ID code to translate to a string.",
"bodstr": "Name or ID of body associated with surface.",
"srfstr": "String corresponding to surface ID code.",
}
SPYCE_PS ["srfcss_error"] = "Raise a SPICE(NOTRANSLATION) condition if not found."
SPYCE_URL["srfcss_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/srfcss_c.html"

#########################################
SPYCE_SIGNATURES ["srfnrm"] = ["string", "body_name", "time", "frame_name"]
SPYCE_ARGNAMES   ["srfnrm"] = ["method", "target", "et", "fixref"]
SPYCE_RETURNS    ["srfnrm"] = ["float[*,3]", "float[*,3]"]
SPYCE_RETNAMES   ["srfnrm"] = ["srfpts", "normls"]
SPYCE_ABSTRACT   ["srfnrm"] = """
Map array of surface points on a specified target body to the
corresponding unit length outward surface normal vectors.

The surface of the target body may be represented by a triaxial
ellipsoid or by topographic data provided by DSK files.
"""
SPYCE_DEFINITIONS["srfnrm"] = {
"method": "Computation method.",
"target": "Name of target body.",
"et": "Epoch in TDB seconds past J2000 TDB.",
"fixref": "Body-fixed, body-centered target body frame.",
"srfpts": "Array of surface points.",
"normls": "Array of outward, unit length normal vectors.",
}
SPYCE_URL["srfnrm"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/srfnrm_c.html"

#########################################
SPYCE_SIGNATURES ["srfrec"] = ["body_code", "float", "float"]
SPYCE_ARGNAMES   ["srfrec"] = ["body", "lon", "lat"]
SPYCE_RETURNS    ["srfrec"] = ["float[3]"]
SPYCE_RETNAMES   ["srfrec"] = ["rectan"]
SPYCE_ABSTRACT   ["srfrec"] = """
Convert planetocentric latitude and longitude of a surface point on a
specified body to rectangular coordinates.
"""
SPYCE_DEFINITIONS["srfrec"] = {
"body": "NAIF integer code of an extended body.",
"lon": "Longitude of point in radians.",
"lat": "Latitude of point in radians.",
"rectan": "Rectangular coordinates of the point.",
}
SPYCE_URL["srfrec"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/srfrec_c.html"

#########################################
SPYCE_SIGNATURES ["srfs2c"] = ["string", "body_name"]
SPYCE_ARGNAMES   ["srfs2c"] = ["srfstr", "bodstr"]
SPYCE_RETURNS    ["srfs2c"] = ["int", "bool"]
SPYCE_RETNAMES   ["srfs2c"] = ["code", "found"]
SPYCE_ABSTRACT   ["srfs2c"] = """
Translate a surface string, together with a body string, to the
corresponding surface ID code. The input strings may contain names or
integer ID codes.
"""
SPYCE_DEFINITIONS["srfs2c"] = {
"srfstr": "Surface name or ID string.",
"bodstr": "Body name or ID string.",
"code": "Integer surface ID code.",
"found": "True indicating that surface ID was found, False otherwise.",
}
SPYCE_URL["srfs2c"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/srfs2c_c.html"

SPYCE_SIGNATURES ["srfs2c_error"] = ["string", "body_name"]
SPYCE_ARGNAMES   ["srfs2c_error"] = ["srfstr", "bodstr"]
SPYCE_RETURNS    ["srfs2c_error"] = ["int"]
SPYCE_RETNAMES   ["srfs2c_error"] = ["code"]
SPYCE_ABSTRACT   ["srfs2c_error"] = """
Translate a surface string, together with a body string, to the
corresponding surface ID code. The input strings may contain names or
integer ID codes.
"""
SPYCE_DEFINITIONS["srfs2c_error"] = {
"srfstr": "Surface name or ID string.",
"bodstr": "Body name or ID string.",
"code": "Integer surface ID code.",
}
SPYCE_PS ["srfs2c_error"] = "Raise KeyError if not found."
SPYCE_URL["srfs2c_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/srfs2c_c.html"

#########################################
SPYCE_SIGNATURES ["srfscc"] = ["string", "body_code"]
SPYCE_ARGNAMES   ["srfscc"] = ["srfstr", "bodyid"]
SPYCE_RETURNS    ["srfscc"] = ["int", "bool"]
SPYCE_RETNAMES   ["srfscc"] = ["code", "found"]
SPYCE_ABSTRACT   ["srfscc"] = """
Translate a surface string, together with a body ID code, to the
corresponding surface ID code. The input surface string may contain a
name or an integer ID code.
"""
SPYCE_DEFINITIONS["srfscc"] = {
"srfstr": "Surface name or ID string.",
"bodyid": "Body ID code.",
"code": "Integer surface ID code.",
"found": "True indicating that surface ID was found, False otherwise.",
}
SPYCE_URL["srfscc"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/srfscc_c.html"

SPYCE_SIGNATURES ["srfscc_error"] = ["string", "body_code"]
SPYCE_ARGNAMES   ["srfscc_error"] = ["srfstr", "bodyid"]
SPYCE_RETURNS    ["srfscc_error"] = ["int"]
SPYCE_RETNAMES   ["srfscc_error"] = ["code"]
SPYCE_ABSTRACT   ["srfscc_error"] = """
Translate a surface string, together with a body ID code, to the
corresponding surface ID code. The input surface string may contain a
name or an integer ID code.
"""
SPYCE_DEFINITIONS["srfscc_error"] = {
"srfstr": "Surface name or ID string.",
"bodyid": "Body ID code.",
"code": "Integer surface ID code.",
}
SPYCE_PS ["srfscc_error"] = "Raise KeyError if not found."
SPYCE_URL["srfscc_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/srfscc_c.html"

#########################################
SPYCE_SIGNATURES ["srfxpt"] = ["string", "body_name", "time", "string", "body_name", "frame_name", "float[3]"]
SPYCE_ARGNAMES   ["srfxpt"] = ["method", "target", "et", "abcorr", "obsrvr", "dref", "dvec"]
SPYCE_RETURNS    ["srfxpt"] = ["float[3]", "float", "float", "float[3]", "bool"]
SPYCE_RETNAMES   ["srfxpt"] = ["spoint", "dist", "trgepc", "obspos", "found"]
SPYCE_ABSTRACT   ["srfxpt"] = """
Given an observer and a direction vector defining a ray, compute the
surface intercept point of the ray on a target body at a specified
epoch, optionally corrected for light time and stellar aberration.
"""
SPYCE_DEFINITIONS["srfxpt"] = {
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
SPYCE_URL["srfxpt"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/srfxpt_c.html"

#########################################
SPYCE_SIGNATURES ["stcf01"] = ["string"] + 4*["float"]
SPYCE_ARGNAMES   ["stcf01"] = ["catnam", "westra", "eastra", "sthdec", "nthdec"]
SPYCE_RETURNS    ["stcf01"] = ["int"]
SPYCE_RETNAMES   ["stcf01"] = ["nstars"]
SPYCE_ABSTRACT   ["stcf01"] = """
Search through a type 1 star catalog and return the number of stars
within a specified RA - DEC rectangle.
"""
SPYCE_DEFINITIONS["stcf01"] = {
"catnam": "Catalog table name.",
"westra": "Western most right ascension in radians.",
"eastra": "Eastern most right ascension in radians.",
"sthdec": "Southern most declination in radians.",
"nthdec": "Northern most declination in radians.",
"nstars": "Number of stars found.",
}
SPYCE_URL["stcf01"] = ""

#########################################
SPYCE_SIGNATURES ["stcg01"] = ["int"]
SPYCE_ARGNAMES   ["stcg01"] = ["index"]
SPYCE_RETURNS    ["stcg01"] = 4*["float"] + ["int", "string", "float"]
SPYCE_RETNAMES   ["stcg01"] = ["ra", "dec", "rasig", "decsig", "catnum", "sptype", "vmag"]
SPYCE_ABSTRACT   ["stcg01"] = """
Get data for a single star from a SPICE type 1 star catalog.
"""
SPYCE_DEFINITIONS["stcg01"] = {
"index": "Star index.",
"ra": "Right ascension in radians.",
"dec": "Declination in radians.",
"rasig": "Right ascension uncertainty in radians.",
"decsig": "Declination uncertainty in radians.",
"catnum": "Catalog number.",
"sptype": "Spectral type.",
"vmag": "Visual magnitude.",
}
SPYCE_URL["stcg01"] = ""

#########################################
SPYCE_SIGNATURES ["stcl01"] = ["string"]
SPYCE_ARGNAMES   ["stcl01"] = ["catfnm"]
SPYCE_RETURNS    ["stcl01"] = ["string", "int"]
SPYCE_RETNAMES   ["stcl01"] = ["tabnam", "handle"]
SPYCE_ABSTRACT   ["stcl01"] = """
Load SPICE type 1 star catalog and return the catalog's table name.
"""
SPYCE_DEFINITIONS["stcl01"] = {
"catfnm": "Catalog file name.",
"tabnam": "Catalog table name.",
"handle": "Catalog file handle.",
}
SPYCE_URL["stcl01"] = ""

#########################################
SPYCE_SIGNATURES ["stelab"] = 2*["float[3]"]
SPYCE_ARGNAMES   ["stelab"] = ["pobj", "vobs"]
SPYCE_RETURNS    ["stelab"] = ["float[3]"]
SPYCE_RETNAMES   ["stelab"] = ["appobj"]
SPYCE_ABSTRACT   ["stelab"] = """
Correct the apparent position of an object for stellar aberration.
"""
SPYCE_DEFINITIONS["stelab"] = {
"pobj": "Position of an object with respect to the observer.",
"vobs": "Velocity of the observer with respect to the Solar System barycenter.",
"appobj": "Apparent position of the object with respect to the observer, corrected for stellar aberration.",
}
SPYCE_URL["stelab"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/stelab_c.html"

#########################################
SPYCE_SIGNATURES ["stlabx"] = 2*["float[3]"]
SPYCE_ARGNAMES   ["stlabx"] = ["pobj", "vobs"]
SPYCE_RETURNS    ["stlabx"] = ["float[3]"]
SPYCE_RETNAMES   ["stlabx"] = ["corpos"]
SPYCE_ABSTRACT   ["stlabx"] = """
Correct the position of a target for the stellar aberration effect on
radiation transmitted from a specified observer to the target.
"""
SPYCE_DEFINITIONS["stlabx"] = {
"pobj": "Position of an object with respect to the observer.",
"vobs": "Velocity of the observer with respect to the Solar System barycenter.",
"corpos": "Corrected position of the object.",
}
SPYCE_URL["stlabx"] = ""

#########################################
SPYCE_SIGNATURES ["stpool"] = ["string", "int", "string"]
SPYCE_ARGNAMES   ["stpool"] = ["item", "nth", "contin"]
SPYCE_RETURNS    ["stpool"] = ["string", "bool"]
SPYCE_RETNAMES   ["stpool"] = ["string", "found"]
SPYCE_ABSTRACT   ["stpool"] = """
Retrieve the nth string from the kernel pool variable, where the string
may be continued across several components of the kernel pool variable.
"""
SPYCE_DEFINITIONS["stpool"] = {
"item": "Name of the kernel pool variable.",
"nth": "Index of the full string to retrieve.",
"contin": "Character sequence used to indicate continuation.",
"string": "A full string concatenated across continuations.",
"found": "True indicating success of request; False on failure.",
}
SPYCE_URL["stpool"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/stpool_c.html"

SPYCE_SIGNATURES ["stpool_error"] = ["string", "int", "string"]
SPYCE_ARGNAMES   ["stpool_error"] = ["item", "nth", "contin"]
SPYCE_RETURNS    ["stpool_error"] = ["string"]
SPYCE_RETNAMES   ["stpool_error"] = ["string"]
SPYCE_ABSTRACT   ["stpool_error"] = """
Retrieve the nth string from the kernel pool variable, where the string
may be continued across several components of the kernel pool variable.
"""
SPYCE_DEFINITIONS["stpool_error"] = {
"item": "Name of the kernel pool variable.",
"nth": "Index of the full string to retrieve.",
"contin": "Character sequence used to indicate continuation.",
"string": "A full string concatenated across continuations.",
}
SPYCE_PS ["stpool_error"] = "Raise KeyError if request failed."
SPYCE_URL["stpool_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/stpool_c.html"

#########################################
SPYCE_SIGNATURES ["str2et"] = ["string"]
SPYCE_ARGNAMES   ["str2et"] = ["str"]
SPYCE_RETURNS    ["str2et"] = ["float"]
SPYCE_RETNAMES   ["str2et"] = ["et"]
SPYCE_ABSTRACT   ["str2et"] = """
Convert a string representing an epoch to a double precision value
representing the number of TDB seconds past the J2000 epoch
corresponding to the input epoch.
"""
SPYCE_DEFINITIONS["str2et"] = {
"str": "A string representing an epoch.",
"et": "The equivalent value in seconds past J2000, TDB.",
}
SPYCE_URL["str2et"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/str2et_c.html"

#########################################
SPYCE_SIGNATURES ["subpnt"] = ["string", "body_name", "time", "frame_name", "string", "body_name"]
SPYCE_ARGNAMES   ["subpnt"] = ["method", "target", "et", "fixref", "abcorr", "obsrvr"]
SPYCE_RETURNS    ["subpnt"] = ["float[3]", "time", "float[3]"]
SPYCE_RETNAMES   ["subpnt"] = ["spoint", "trgepc", "srfvec"]
SPYCE_ABSTRACT   ["subpnt"] = """
Compute the rectangular coordinates of the sub-observer point on a
target body at a specified epoch, optionally corrected for light time
and stellar aberration.

The surface of the target body may be represented by a triaxial
ellipsoid or by topographic data provided by DSK files.

This routine supersedes subpt.
"""
SPYCE_DEFINITIONS["subpnt"] = {
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
SPYCE_URL["subpnt"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/subpnt_c.html"

#########################################
SPYCE_SIGNATURES ["subpt"] = ["string", "body_name", "time", "string", "body_name"]
SPYCE_ARGNAMES   ["subpt"] = ["method", "target", "et", "abcorr", "obsrvr"]
SPYCE_RETURNS    ["subpt"] = ["float[3]", "float"]
SPYCE_RETNAMES   ["subpt"] = ["spoint", "alt"]
SPYCE_ABSTRACT   ["subpt"] = """
Compute the rectangular coordinates of the sub-observer point on a
target body at a particular epoch, optionally corrected for planetary
(light time) and stellar aberration.  Return these coordinates expressed
in the body-fixed frame associated with the target body.  Also, return
the observer's altitude above the target body.
"""
SPYCE_DEFINITIONS["subpt"] = {
"method": "Computation method.",
"target": "Name of target body.",
"et": "Epoch in ephemeris seconds past J2000 TDB.",
"abcorr": "Aberration correction, \"NONE\", \"LT\", \"LT+S\", \"CN\", or \"CN+S\".",
"obsrvr": "Name of observing body.",
"spoint": "Sub-observer point on the target body.",
"alt": "Altitude of the observer above the target body.",
}
SPYCE_URL["subpt"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/subpt_c.html"

#########################################
SPYCE_SIGNATURES ["subslr"] = ["string", "body_name", "time", "frame_name", "string", "body_name"]
SPYCE_ARGNAMES   ["subslr"] = ["method", "target", "et", "fixref", "abcorr", "obsrvr"]
SPYCE_RETURNS    ["subslr"] = ["float[3]", "time", "float[3]"]
SPYCE_RETNAMES   ["subslr"] = ["spoint", "trgepc", "srfvec"]
SPYCE_ABSTRACT   ["subslr"] = """
Compute the rectangular coordinates of the sub-solar point on a target
body at a specified epoch, optionally corrected for light time and
stellar aberration.

The surface of the target body may be represented by a triaxial
ellipsoid or by topographic data provided by DSK files.

This routine supersedes subsol.
"""
SPYCE_DEFINITIONS["subslr"] = {
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
SPYCE_URL["subslr"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/subslr_c.html"

#########################################
SPYCE_SIGNATURES ["subsol"] = ["string", "body_name", "time", "string", "body_name"]
SPYCE_ARGNAMES   ["subsol"] = ["method", "target", "et", "abcorr", "obsrvr"]
SPYCE_RETURNS    ["subsol"] = ["float[3]"]
SPYCE_RETNAMES   ["subsol"] = ["spoint"]
SPYCE_ABSTRACT   ["subsol"] = """
Determine the coordinates of the sub-solar point on a target body as
seen by a specified observer at a specified epoch, optionally corrected
for planetary (light time) and stellar aberration.
"""
SPYCE_DEFINITIONS["subsol"] = {
"method": "Computation method.",
"target": "Name of target body.",
"et": "Epoch in ephemeris seconds past J2000 TDB.",
"abcorr": "Aberration correction, \"NONE\", \"LT\", \"LT+S\", \"CN\", or \"CN+S\".",
"obsrvr": "Name of observing body.",
"spoint": "Sub-solar point on the target body.",
}
SPYCE_URL["subsol"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/subsol_c.html"

#########################################
SPYCE_SIGNATURES ["surfnm"] = 3*["float"] + ["float[3]"]
SPYCE_ARGNAMES   ["surfnm"] = ["a", "b", "c", "point"]
SPYCE_RETURNS    ["surfnm"] = ["float[3]"]
SPYCE_RETNAMES   ["surfnm"] = ["normal"]
SPYCE_ABSTRACT   ["surfnm"] = """
This routine computes the outward-pointing, unit normal vector from a
point on the surface of an ellipsoid.
"""
SPYCE_DEFINITIONS["surfnm"] = {
"a": "Length of the ellisoid semi-axis along the x-axis.",
"b": "Length of the ellisoid semi-axis along the y-axis.",
"c": "Length of the ellisoid semi-axis along the z-axis.",
"point": "Body-fixed coordinates of a point on the ellipsoid",
"normal": "Outward pointing unit normal to ellipsoid at point",
}
SPYCE_URL["surfnm"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/surfnm_c.html"

#########################################
SPYCE_SIGNATURES ["surfpt"] = 2*["float[3]"] + 3*["float"]
SPYCE_ARGNAMES   ["surfpt"] = ["positn", "u", "a", "b", "c"]
SPYCE_RETURNS    ["surfpt"] = ["float[3]", "bool"]
SPYCE_RETNAMES   ["surfpt"] = ["point", "found"]
SPYCE_ABSTRACT   ["surfpt"] = """
Determine the intersection of a line-of-sight vector with the surface of
an ellipsoid.
"""
SPYCE_DEFINITIONS["surfpt"] = {
"positn": "Position of the observer in body-fixed frame.",
"u": "Vector from the observer in some direction.",
"a": "Length of the ellipsoid semi-axis along the x-axis.",
"b": "Length of the ellipsoid semi-axis along the y-axis.",
"c": "Length of the ellipsoid semi-axis along the z-axis.",
"point": "Point on the ellipsoid pointed to by u.",
"found": "Flag indicating if u points at the ellipsoid.",
}
SPYCE_URL["surfpt"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/surfpt_c.html"

#########################################
SPYCE_SIGNATURES ["surfpv"] = 2*["float[6]"] + 3*["float"]
SPYCE_ARGNAMES   ["surfpv"] = ["stvrtx", "stdir", "a", "b", "c"]
SPYCE_RETURNS    ["surfpv"] = ["float[6]", "bool"]
SPYCE_RETNAMES   ["surfpv"] = ["stx", "found"]
SPYCE_ABSTRACT   ["surfpv"] = """
Find the state (position and velocity) of the surface intercept defined
by a specified ray, ray velocity, and ellipsoid.
"""
SPYCE_DEFINITIONS["surfpv"] = {
"stvrtx": "State of ray's vertex.",
"stdir": "State of ray's direction vector.",
"a": "Length of ellipsoid semi-axis along the x-axis.",
"b": "Length of ellipsoid semi-axis along the y-axis.",
"c": "Length of ellipsoid semi-axis along the z-axis.",
"stx": "State of surface intercept.",
"found": "Flag indicating whether intercept state was found.",
}
SPYCE_URL["surfpv"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/surfpv_c.html"

#########################################
SPYCE_SIGNATURES ["sxform"] = ["frame_name", "frame_name", "time"]
SPYCE_ARGNAMES   ["sxform"] = ["fromfr", "tofr", "et"]
SPYCE_RETURNS    ["sxform"] = ["rotmat[6,6]"]
SPYCE_RETNAMES   ["sxform"] = ["xform"]
SPYCE_ABSTRACT   ["sxform"] = """
Return the state transformation matrix from one frame to another at a
specified epoch.
"""
SPYCE_DEFINITIONS["sxform"] = {
"fromfr": "Name of the frame to transform from.",
"tofr": "Name of the frame to transform to.",
"et": "Epoch of the state transformation matrix.",
"xform": "A state transformation matrix.",
}
SPYCE_URL["sxform"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sxform_c.html"

#########################################
SPYCE_SIGNATURES ["termpt"] = ["string", "body_name", "body_name", "time", "frame_name", "string", "string", "body_name", "float[3]", "float", "int", "float", "float", "int"]
SPYCE_ARGNAMES   ["termpt"] = ["method", "ilusrc", "target", "et", "fixref", "abcorr", "corloc", "obsrvr", "refvec", "rolstp", "ncuts", "schstp", "soltol", "maxn"]
SPYCE_RETURNS    ["termpt"] = ["int[*]", "float[*,3]", "float[*]", "float[*,3]"]
SPYCE_RETNAMES   ["termpt"] = ["npts", "points", "epochs", "trmvcs"]
SPYCE_ABSTRACT   ["termpt"] = """
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
SPYCE_DEFINITIONS["termpt"] = {
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
SPYCE_URL["termpt"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/termpt_c.html"

#########################################
SPYCE_SIGNATURES ["timdef"] = ["string", "string", "string"]
SPYCE_ARGNAMES   ["timdef"] = ["action", "item", "value"]
SPYCE_RETURNS    ["timdef"] = ["string"]
SPYCE_RETNAMES   ["timdef"] = ["output"]
SPYCE_DEFAULTS   ["timdef"] = ["", ""]
SPYCE_ABSTRACT   ["timdef"] = """
Set and retrieve the defaults associated with calendar input strings.
"""
SPYCE_DEFINITIONS["timdef"] = {
"action": "the kind of action to take \"SET\" or \"GET\" (default \"GET\").",
"item"  : "the default item of interest (\"CALENDAR\", \"SYSTEM\", or \"ZONE\").",
"value" : "the value associated with the item on \"SET\"; ignored on \"GET\". Default is "".",
"output": "on \"GET\", the value of the requested parameter.",
}
SPYCE_PS ["timdef"] = "As a special case, a single argument is \"CALENDAR\", \"SYSTEM\", or \"ZONE\", a \"GET\" operation is performed; if two arguments are provided and the first is \"CALENDAR\", \"SYSTEM\", or \"ZONE\", a \"SET\" operation is performed."
SPYCE_URL["timdef"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/timdef_c.html"

#########################################
SPYCE_SIGNATURES ["timout"] = ["time", "string"]
SPYCE_ARGNAMES   ["timout"] = ["et", "pictur"]
SPYCE_RETURNS    ["timout"] = ["string"]
SPYCE_RETNAMES   ["timout"] = ["output"]
SPYCE_ABSTRACT   ["timout"] = """
This routine converts an input epoch represented in TDB seconds past the
TDB epoch of J2000 to a character string formatted to the specifications
of a user's format picture.
"""
SPYCE_DEFINITIONS["timout"] = {
"et": "An epoch in seconds past the ephemeris epoch J2000.",
"pictur": "A format specification for the output string.",
"output": "A string representation of the input epoch.",
}
SPYCE_URL["timout"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/timout_c.html"

#########################################
SPYCE_SIGNATURES ["tipbod"] = ["frame_code", "body_code", "time"]
SPYCE_ARGNAMES   ["tipbod"] = ["ref", "body", "et"]
SPYCE_RETURNS    ["tipbod"] = ["rotmat[3,3]"]
SPYCE_RETNAMES   ["tipbod"] = ["tipm"]
SPYCE_ABSTRACT   ["tipbod"] = """
Return a 3x3 matrix that transforms positions in inertial coordinates to
positions in body-equator-and-prime-meridian coordinates.
"""
SPYCE_DEFINITIONS["tipbod"] = {
"ref": "ID of inertial reference frame to transform from.",
"body": "ID code of body.",
"et": "Epoch of transformation.",
"tipm": "Transformation (position), inertial to prime meridian.",
}
SPYCE_URL["tipbod"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/tipbod_c.html"

#########################################
SPYCE_SIGNATURES ["tisbod"] = ["frame_code", "body_code", "time"]
SPYCE_ARGNAMES   ["tisbod"] = ["ref", "body", "et"]
SPYCE_RETURNS    ["tisbod"] = ["rotmat[6,6]"]
SPYCE_RETNAMES   ["tisbod"] = ["tsipm"]
SPYCE_ABSTRACT   ["tisbod"] = """
Return a 6x6 matrix that transforms states in inertial coordinates to
states in body-equator-and-prime-meridian coordinates.
"""
SPYCE_DEFINITIONS["tisbod"] = {
"ref": "ID of inertial reference frame to transform from",
"body": "ID code of body",
"et": "Epoch of transformation",
"tsipm": "Transformation (state), inertial to prime meridian",
}
SPYCE_URL["tisbod"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/tisbod_c.html"

#########################################
SPYCE_SIGNATURES ["tkvrsn"] = ["string"]
SPYCE_ARGNAMES   ["tkvrsn"] = ["item"]
SPYCE_DEFAULTS  ["tkvrsn"] = ["TOOLKIT"]
SPYCE_RETURNS    ["tkvrsn"] = ["string"]
SPYCE_RETNAMES   ["tkvrsn"] = ["value"]
SPYCE_ABSTRACT   ["tkvrsn"] = """
Given an item such as the Toolkit or an entry point name, return the
latest version string.
"""
SPYCE_DEFINITIONS["tkvrsn"] = {
"item": "Item for which a version string is desired; the default and only valid value is \"TOOLKIT\".",
"value": "A version string.",
}
SPYCE_URL["tkvrsn"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/tkvrsn_c.html"

#########################################
SPYCE_SIGNATURES ["tparse"] = ["string"]
SPYCE_ARGNAMES   ["tparse"] = ["string"]
SPYCE_RETURNS    ["tparse"] = ["float", "string"]
SPYCE_RETNAMES   ["tparse"] = ["sp2000", "errmsg"]
SPYCE_ABSTRACT   ["tparse"] = """
Parse a time string and return seconds past the J2000 epoch on a formal
calendar.
"""
SPYCE_DEFINITIONS["tparse"] = {
"string": "Input time string, UTC.",
"sp2000": "Equivalent UTC seconds past J2000.",
"errmsg": "Descriptive error message.",
}
SPYCE_URL["tparse"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/tparse_c.html"

SPYCE_SIGNATURES ["tparse_error"] = ["string"]
SPYCE_ARGNAMES   ["tparse_error"] = ["string"]
SPYCE_RETURNS    ["tparse_error"] = ["float"]
SPYCE_RETNAMES   ["tparse_error"] = ["sp2000"]
SPYCE_ABSTRACT   ["tparse_error"] = """
Parse a time string and return seconds past the J2000 epoch on a formal
calendar.
"""
SPYCE_DEFINITIONS["tparse_error"] = {
"string": "Input time string, UTC.",
"sp2000": "Equivalent UTC seconds past J2000.",
}
SPYCE_PS ["tparse_error"] = "Raise ValueError on invalid input string."
SPYCE_URL["tparse_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/tparse_c.html"

#########################################
SPYCE_SIGNATURES ["tpictr"] = ["string"]
SPYCE_ARGNAMES   ["tpictr"] = ["sample"]
SPYCE_RETURNS    ["tpictr"] = ["string", "bool", "string"]
SPYCE_RETNAMES   ["tpictr"] = ["pictr", "ok", "errmsg"]
SPYCE_ABSTRACT   ["tpictr"] = """
Given a sample time string, create a time format picture suitable for
use by the routine timout.
"""
SPYCE_DEFINITIONS["tpictr"] = {
"sample": "A sample time string.",
"pictr" : "A format picture that describes sample.",
"ok"    : "Flag indicating whether sample parsed successfully.",
"errmsg": "Diagnostic returned if sample cannot be parsed.",
}
SPYCE_URL["tpictr"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/tpictr_c.html"

SPYCE_SIGNATURES ["tpictr_error"] = ["string"]
SPYCE_ARGNAMES   ["tpictr_error"] = ["sample"]
SPYCE_RETURNS    ["tpictr_error"] = ["string"]
SPYCE_RETNAMES   ["tpictr_error"] = ["pictr"]
SPYCE_ABSTRACT   ["tpictr_error"] = """
Given a sample time string, create a time format picture suitable for
use by the routine timout.
"""
SPYCE_DEFINITIONS["tpictr_error"] = {
"sample": "A sample time string.",
"pictr" : "A format picture that describes sample.",
}
SPYCE_PS ["tpictr_error"] = "Raise ValueError on invalid sample string."
SPYCE_URL["tpictr_error"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/tpictr_c.html"

#########################################
SPYCE_SIGNATURES ["trace"] = ["float[3,3]"]
SPYCE_ARGNAMES   ["trace"] = ["matrix"]
SPYCE_RETURNS    ["trace"] = ["float"]
SPYCE_RETNAMES   ["trace"] = ["trace"]
SPYCE_ABSTRACT   ["trace"] = """
Return the trace of a 3x3 matrix.
"""
SPYCE_DEFINITIONS["trace"] = {
"matrix": "3x3 matrix of double precision numbers.",
"trace": "The trace of the matrix.",
}
SPYCE_URL["trace"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/trace_c.html"

#########################################
SPYCE_SIGNATURES ["trcoff"] = []
SPYCE_ARGNAMES   ["trcoff"] = []
SPYCE_RETURNS    ["trcoff"] = []
SPYCE_RETNAMES   ["trcoff"] = []
SPYCE_ABSTRACT   ["trcoff"] = """
Disable tracing.
"""
SPYCE_DEFINITIONS["trcoff"] = {}
SPYCE_URL["trcoff"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/trcoff_c.html"

#########################################
SPYCE_SIGNATURES ["trcdep"] = []
SPYCE_ARGNAMES   ["trcdep"] = []
SPYCE_RETURNS    ["trcdep"] = ["int"]
SPYCE_RETNAMES   ["trcdep"] = ["depth"]
SPYCE_ABSTRACT   ["trcdep"] = """
Return the number of modules in the traceback representation.
"""
SPYCE_DEFINITIONS["trcdep"] = {
"depth": "The number of modules in the traceback.",
}
SPYCE_URL["trcdep"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/trcdep_c.html"

#########################################
SPYCE_SIGNATURES ["trcnam"] = ["int"]
SPYCE_ARGNAMES   ["trcnam"] = ["index"]
SPYCE_RETURNS    ["trcnam"] = ["string"]
SPYCE_RETNAMES   ["trcnam"] = ["name"]
SPYCE_ABSTRACT   ["trcnam"] = """
Return the name of the module having the specified position in the trace
representation. The first module to check in is at index 0.
"""
SPYCE_DEFINITIONS["trcnam"] = {
"index": "The position of the requested module name.",
"name": "The name at position `index' in the traceback.",
}
SPYCE_URL["trcnam"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/trcnam_c.html"

#########################################
SPYCE_SIGNATURES ["tsetyr"] = ["int"]
SPYCE_ARGNAMES   ["tsetyr"] = ["year"]
SPYCE_RETURNS    ["tsetyr"] = []
SPYCE_RETNAMES   ["tsetyr"] = []
SPYCE_ABSTRACT   ["tsetyr"] = """
Set the lower bound on the 100 year range.
"""
SPYCE_DEFINITIONS["tsetyr"] = {
"year": "Lower bound on the 100 year interval of expansion",
}
SPYCE_URL["tsetyr"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/tsetyr_c.html"

#########################################
SPYCE_SIGNATURES ["twopi"] = []
SPYCE_ARGNAMES   ["twopi"] = []
SPYCE_RETURNS    ["twopi"] = ["float"]
SPYCE_RETNAMES   ["twopi"] = ["value"]
SPYCE_ABSTRACT   ["twopi"] = """
Return twice the value of pi.
"""
SPYCE_DEFINITIONS["twopi"] = {
"value": "twice the value of pi",
}
SPYCE_URL["twopi"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/twopi_c.html"

#########################################
SPYCE_SIGNATURES ["twovec"] = 2*["float[3]", "int"]
SPYCE_ARGNAMES   ["twovec"] = ["axdef", "indexa", "plndef", "indexp"]
SPYCE_RETURNS    ["twovec"] = ["rotmat[3,3]"]
SPYCE_RETNAMES   ["twovec"] = ["mout"]
SPYCE_ABSTRACT   ["twovec"] = """
Find the transformation to the right-handed frame having a given vector
as a specified axis and having a second given vector lying in a
specified coordinate plane.
"""
SPYCE_DEFINITIONS["twovec"] = {
"axdef": "Vector defining a principal axis.",
"indexa": "Principal axis number of axdef (X=1, Y=2, Z=3).",
"plndef": "Vector defining (with axdef) a principal plane.",
"indexp": "Second axis number (with indexa) of principal plane.",
"mout": "Output rotation matrix.",
}
SPYCE_URL["twovec"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/twovec_c.html"

#########################################
SPYCE_SIGNATURES ["tyear"] = []
SPYCE_ARGNAMES   ["tyear"] = []
SPYCE_RETURNS    ["tyear"] = ["float"]
SPYCE_RETNAMES   ["tyear"] = ["value"]
SPYCE_ABSTRACT   ["tyear"] = """
Return the number of seconds in a tropical year.
"""
SPYCE_DEFINITIONS["tyear"] = {
"value": "number of seconds in a tropical year",
}
SPYCE_URL["tyear"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/tyear_c.html"

#########################################
SPYCE_SIGNATURES ["ucrss"] = 2*["float[3]"]
SPYCE_ARGNAMES   ["ucrss"] = ["v1", "v2"]
SPYCE_RETURNS    ["ucrss"] = ["float[3]"]
SPYCE_RETNAMES   ["ucrss"] = ["vout"]
SPYCE_ABSTRACT   ["ucrss"] = """
Compute the normalized cross product of two 3-vectors.
"""
SPYCE_DEFINITIONS["ucrss"] = {
"v1": "Left vector for cross product.",
"v2": "Right vector for cross product.",
"vout": "Normalized cross product (v1xv2) / |v1xv2|.",
}
SPYCE_URL["ucrss"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ucrss_c.html"

#########################################
SPYCE_SIGNATURES ["unitim"] = ["time", "string", "string"]
SPYCE_ARGNAMES   ["unitim"] = ["epoch", "insys", "outsys"]
SPYCE_RETURNS    ["unitim"] = ["float"]
SPYCE_RETNAMES   ["unitim"] = ["value"]
SPYCE_ABSTRACT   ["unitim"] = """
Transform time from one uniform scale to another.  The uniform time
scales are TAI, TDT, TDB, <float> et, JED, JDTDB, JDTDT.
"""
SPYCE_DEFINITIONS["unitim"] = {
"epoch": "An epoch to be converted.",
"insys": "The time scale associated with the input epoch.",
"outsys": "The time scale associated with the function value.",
"value": "the value in outsys that is equivalent to the epoch on the insys time scale.",
}
SPYCE_URL["unitim"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/unitim_c.html"

#########################################
SPYCE_SIGNATURES ["unload"] = ["string"]
SPYCE_ARGNAMES   ["unload"] = ["file"]
SPYCE_RETURNS    ["unload"] = []
SPYCE_RETNAMES   ["unload"] = []
SPYCE_ABSTRACT   ["unload"] = """
Unload a SPICE kernel.
"""
SPYCE_DEFINITIONS["unload"] = {
"file": "The name of a kernel to unload.",
}
SPYCE_URL["unload"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/unload_c.html"

#########################################
SPYCE_SIGNATURES ["unorm"] = ["float[3]"]
SPYCE_ARGNAMES   ["unorm"] = ["v1"]
SPYCE_RETURNS    ["unorm"] = ["float[3]", "float"]
SPYCE_RETNAMES   ["unorm"] = ["vout", "vmag"]
SPYCE_ABSTRACT   ["unorm"] = """
Normalize a double precision 3-vector and return its magnitude.
"""
SPYCE_DEFINITIONS["unorm"] = {
"v1": "Vector to be normalized.",
"vout": "Unit vector v1 / |v1|.",
"vmag": "Magnitude of v1, i.e. |v1|.",
}
SPYCE_PS ["unorm"] = "If v1 is the zero vector, then vout will also be zero."
SPYCE_URL["unorm"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/unorm_c.html"

#########################################
SPYCE_SIGNATURES ["unormg"] = ["float[*]"]
SPYCE_ARGNAMES   ["unormg"] = ["v1"]
SPYCE_RETURNS    ["unormg"] = ["float[*]", "float"]
SPYCE_RETNAMES   ["unormg"] = ["vout", "vmag"]
SPYCE_ABSTRACT   ["unormg"] = """
Normalize a double precision vector of arbitrary dimension and return
its magnitude.
"""
SPYCE_DEFINITIONS["unormg"] = {
"v1": "Vector to be normalized.",
"vout": "Unit vector v1 / |v1|.",
"vmag": "Magnitude of v1, that is, |v1|.",
}
SPYCE_PS ["unormg"] = "If v1 is the zero vector, then vout will also be zero."
SPYCE_URL["unormg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/unormg_c.html"

#########################################
SPYCE_SIGNATURES ["utc2et"] = ["string"]
SPYCE_ARGNAMES   ["utc2et"] = ["utcstr"]
SPYCE_RETURNS    ["utc2et"] = ["float"]
SPYCE_RETNAMES   ["utc2et"] = ["et"]
SPYCE_ABSTRACT   ["utc2et"] = """
Convert an input time from Calendar or Julian Date format, UTC, to
ephemeris seconds past J2000.
"""
SPYCE_DEFINITIONS["utc2et"] = {
"utcstr": "Input time string, UTC.",
"et": "Output epoch, ephemeris seconds past J2000.",
}
SPYCE_URL["utc2et"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/utc2et_c.html"

#########################################
SPYCE_SIGNATURES ["vadd"] = 2*["float[3]"]
SPYCE_ARGNAMES   ["vadd"] = ["v1", "v2"]
SPYCE_RETURNS    ["vadd"] = ["float[3]"]
SPYCE_RETNAMES   ["vadd"] = ["vout"]
SPYCE_ABSTRACT   ["vadd"] = """
add two 3 dimensional vectors.
"""
SPYCE_DEFINITIONS["vadd"] = {
"v1": "First vector to be added.",
"v2": "Second vector to be added.",
"vout": "Sum vector, v1 + v2.",
}
SPYCE_URL["vadd"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vadd_c.html"

#########################################
SPYCE_SIGNATURES ["vaddg"] = 2*["float[*]"]
SPYCE_ARGNAMES   ["vaddg"] = ["v1", "v2"]
SPYCE_RETURNS    ["vaddg"] = ["float[*]"]
SPYCE_RETNAMES   ["vaddg"] = ["vout"]
SPYCE_ABSTRACT   ["vaddg"] = """
add two vectors of arbitrary dimension.
"""
SPYCE_DEFINITIONS["vaddg"] = {
"v1": "First vector to be added.",
"v2": "Second vector to be added.",
"vout": "Sum vector, v1 + v2.",
}
SPYCE_URL["vaddg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vaddg_c.html"

#########################################
SPYCE_SIGNATURES ["vcrss"] = 2*["float[3]"]
SPYCE_ARGNAMES   ["vcrss"] = ["v1", "v2"]
SPYCE_RETURNS    ["vcrss"] = ["float[3]"]
SPYCE_RETNAMES   ["vcrss"] = ["vout"]
SPYCE_ABSTRACT   ["vcrss"] = """
Compute the cross product of two 3-dimensional vectors.
"""
SPYCE_DEFINITIONS["vcrss"] = {
"v1": "Left hand vector for cross product.",
"v2": "Right hand vector for cross product.",
"vout": "Cross product v1xv2.",
}
SPYCE_URL["vcrss"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vcrss_c.html"

#########################################
SPYCE_SIGNATURES ["vdist"] = 2*["float[3]"]
SPYCE_ARGNAMES   ["vdist"] = ["v1", "v2"]
SPYCE_RETURNS    ["vdist"] = ["float"]
SPYCE_RETNAMES   ["vdist"] = ["dist"]
SPYCE_ABSTRACT   ["vdist"] = """
Return the distance between two three-dimensional vectors.
"""
SPYCE_DEFINITIONS["vdist"] = {
"v1": "The first of two 3-vectors.",
"v2": "The second of two 3-vectors.",
"dist": "The distance between v1 and v2.",
}
SPYCE_URL["vdist"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vdist_c.html"

#########################################
SPYCE_SIGNATURES ["vdistg"] = 2*["float[*]"]
SPYCE_ARGNAMES   ["vdistg"] = ["v1", "v2"]
SPYCE_RETURNS    ["vdistg"] = ["float"]
SPYCE_RETNAMES   ["vdistg"] = ["dist"]
SPYCE_ABSTRACT   ["vdistg"] = """
Return the distance between two vectors of arbitrary dimension.
"""
SPYCE_DEFINITIONS["vdistg"] = {
"v1": "The first of two 3-vectors.",
"v2": "The second of two 3-vectors.",
"dist": "The distance between v1 and v2.",
}
SPYCE_URL["vdistg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vdistg_c.html"

#########################################
SPYCE_SIGNATURES ["vdot"] = 2*["float[3]"]
SPYCE_ARGNAMES   ["vdot"] = ["v1", "v2"]
SPYCE_RETURNS    ["vdot"] = ["float"]
SPYCE_RETNAMES   ["vdot"] = ["value"]
SPYCE_ABSTRACT   ["vdot"] = """
Compute the dot product of two double precision, 3-dimensional vectors.
"""
SPYCE_DEFINITIONS["vdot"] = {
"v1": "First vector in the dot product.",
"v2": "Second vector in the dot product.",
"value": "The value of the dot product of v1 and v2.",
}
SPYCE_URL["vdot"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vdot_c.html"

#########################################
SPYCE_SIGNATURES ["vdotg"] = 2*["float[*]"]
SPYCE_ARGNAMES   ["vdotg"] = ["v1", "v2"]
SPYCE_RETURNS    ["vdotg"] = ["float"]
SPYCE_RETNAMES   ["vdotg"] = ["value"]
SPYCE_ABSTRACT   ["vdotg"] = """
Compute the dot product of two vectors of arbitrary dimension.
"""
SPYCE_DEFINITIONS["vdotg"] = {
"v1": "First vector in the dot product.",
"v2": "Second vector in the dot product.",
"value": "The value of the dot product of v1 and v2.",
}
SPYCE_URL["vdotg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vdotg_c.html"

#########################################
SPYCE_SIGNATURES ["vequ"] = ["float[3]"]
SPYCE_ARGNAMES   ["vequ"] = ["vin"]
SPYCE_RETURNS    ["vequ"] = ["float[3]"]
SPYCE_RETNAMES   ["vequ"] = ["vout"]
SPYCE_ABSTRACT   ["vequ"] = """
Make one double precision 3-dimensional vector equal to another.
"""
SPYCE_DEFINITIONS["vequ"] = {
"vin": "3-dimensional double precision vector.",
"vout": "3-dimensional double precision vector set equal to vin.",
}
SPYCE_URL["vequ"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vequ_c.html"

#########################################
SPYCE_SIGNATURES ["vequg"] = ["float[*]"]
SPYCE_ARGNAMES   ["vequg"] = ["vin"]
SPYCE_RETURNS    ["vequg"] = ["float[*]"]
SPYCE_RETNAMES   ["vequg"] = ["vout"]
SPYCE_ABSTRACT   ["vequg"] = """
Make one double precision vector of arbitrary dimension equal to
another.
"""
SPYCE_DEFINITIONS["vequg"] = {
"vin": "double precision vector.",
"vout": "double precision vector set equal to vin.",
}
SPYCE_URL["vequg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vequg_c.html"

#########################################
SPYCE_SIGNATURES ["vhat"] = ["float[3]"]
SPYCE_ARGNAMES   ["vhat"] = ["v1"]
SPYCE_RETURNS    ["vhat"] = ["float[3]"]
SPYCE_RETNAMES   ["vhat"] = ["vout"]
SPYCE_ABSTRACT   ["vhat"] = """
Find the unit vector along a double precision 3-dimensional vector.
"""
SPYCE_DEFINITIONS["vhat"] = {
"v1": "Vector to be unitized.",
"vout": "Unit vector v1 / |v1|.",
}
SPYCE_URL["vhat"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vhat_c.html"

#########################################
SPYCE_SIGNATURES ["vhatg"] = ["float[*]"]
SPYCE_ARGNAMES   ["vhatg"] = ["v1"]
SPYCE_RETURNS    ["vhatg"] = ["float[*]"]
SPYCE_RETNAMES   ["vhatg"] = ["vout"]
SPYCE_ABSTRACT   ["vhatg"] = """
Find the unit vector along a double precision vector of arbitrary
dimension.
"""
SPYCE_DEFINITIONS["vhatg"] = {
"v1": "Vector to be normalized.",
"vout": "Unit vector v1 / |v1|.",
}
SPYCE_PS ["vhatg"] = "If v1 is the zero vector, then vout will also be zero."
SPYCE_URL["vhatg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vhatg_c.html"

#########################################
SPYCE_SIGNATURES ["vlcom3"] = 3*["float", "float[3]"]
SPYCE_ARGNAMES   ["vlcom3"] = ["a", "v1", "b", "v2", "c", "v3"]
SPYCE_RETURNS    ["vlcom3"] = ["float[3]"]
SPYCE_RETNAMES   ["vlcom3"] = ["sum"]
SPYCE_ABSTRACT   ["vlcom3"] = """
This subroutine computes the vector linear combination
a*v1 + b*v2 + c*v3 of double precision, 3-dimensional vectors.
"""
SPYCE_DEFINITIONS["vlcom3"] = {
"a": "Coefficient of v1",
"v1": "Vector in 3-space",
"b": "Coefficient of v2",
"v2": "Vector in 3-space",
"c": "Coefficient of v3",
"v3": "Vector in 3-space",
"sum": "Linear Vector Combination a*v1 + b*v2 + c*v3",
}
SPYCE_URL["vlcom3"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vlcom3_c.html"

#########################################
SPYCE_SIGNATURES ["vlcom"] = 2*["float", "float[3]"]
SPYCE_ARGNAMES   ["vlcom"] = ["a", "v1", "b", "v2"]
SPYCE_RETURNS    ["vlcom"] = ["float[3]"]
SPYCE_RETNAMES   ["vlcom"] = ["sum"]
SPYCE_ABSTRACT   ["vlcom"] = """
Compute a vector linear combination of two double precision,
3-dimensional vectors.
"""
SPYCE_DEFINITIONS["vlcom"] = {
"a": "Coefficient of v1",
"v1": "Vector in 3-space",
"b": "Coefficient of v2",
"v2": "Vector in 3-space",
"sum": "Linear Vector Combination a*v1 + b*v2",
}
SPYCE_URL["vlcom"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vlcom_c.html"

#########################################
SPYCE_SIGNATURES ["vlcomg"] = 2*["float", "float[*]"]
SPYCE_ARGNAMES   ["vlcomg"] = ["a", "v1", "b", "v2"]
SPYCE_RETURNS    ["vlcomg"] = ["float[*]"]
SPYCE_RETNAMES   ["vlcomg"] = ["sum"]
SPYCE_ABSTRACT   ["vlcomg"] = """
Compute a vector linear combination of two double precision vectors of
arbitrary dimension.
"""
SPYCE_DEFINITIONS["vlcomg"] = {
"a": "Coefficient of v1",
"v1": "Vector in n-space",
"b": "Coefficient of v2",
"v2": "Vector in n-space",
"sum": "Linear Vector Combination a*v1 + b*v2",
}
SPYCE_URL["vlcomg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vlcomg_c.html"

#########################################
SPYCE_SIGNATURES ["vminug"] = ["float[*]"]
SPYCE_ARGNAMES   ["vminug"] = ["vin"]
SPYCE_RETURNS    ["vminug"] = ["float[*]"]
SPYCE_RETNAMES   ["vminug"] = ["vout"]
SPYCE_ABSTRACT   ["vminug"] = """
Negate a double precision vector of arbitrary dimension.
"""
SPYCE_DEFINITIONS["vminug"] = {
"vin": "ndim-dimensional double precision vector to be negated.",
"vout": "ndouble precision vector equal to -vin.",
}
SPYCE_URL["vminug"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vminug_c.html"

#########################################
SPYCE_SIGNATURES ["vminus"] = ["float[3]"]
SPYCE_ARGNAMES   ["vminus"] = ["v1"]
SPYCE_RETURNS    ["vminus"] = ["float[3]"]
SPYCE_RETNAMES   ["vminus"] = ["vout"]
SPYCE_ABSTRACT   ["vminus"] = """
Negate a double precision 3-dimensional vector.
"""
SPYCE_DEFINITIONS["vminus"] = {
"v1": " Vector to be negated.",
"vout": "Negated vector -v1.",
}
SPYCE_URL["vminus"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vminus_c.html"

#########################################
SPYCE_SIGNATURES ["vnorm"] = ["float[3]"]
SPYCE_ARGNAMES   ["vnorm"] = ["v1"]
SPYCE_RETURNS    ["vnorm"] = ["float"]
SPYCE_RETNAMES   ["vnorm"] = ["value"]
SPYCE_ABSTRACT   ["vnorm"] = """
Compute the magnitude of a double precision, 3-dimensional vector.
"""
SPYCE_DEFINITIONS["vnorm"] = {
"v1": "Vector whose magnitude is to be found.",
"value": "The norm of v1.",
}
SPYCE_URL["vnorm"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vnorm_c.html"

#########################################
SPYCE_SIGNATURES ["vnormg"] = ["float[*]"]
SPYCE_ARGNAMES   ["vnormg"] = ["v1"]
SPYCE_RETURNS    ["vnormg"] = ["float"]
SPYCE_RETNAMES   ["vnormg"] = ["value"]
SPYCE_ABSTRACT   ["vnormg"] = """
Compute the magnitude of a double precision vector of arbitrary
dimension.
"""
SPYCE_DEFINITIONS["vnormg"] = {
"v1": "Vector whose magnitude is to be found.",
"value": "The norm of v1.",
}
SPYCE_URL["vnormg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vnormg_c.html"

#########################################
SPYCE_SIGNATURES ["vpack"] = 3*["float"]
SPYCE_ARGNAMES   ["vpack"] = ["x", "y", "z"]
SPYCE_RETURNS    ["vpack"] = ["float[3]"]
SPYCE_RETNAMES   ["vpack"] = ["vout"]
SPYCE_ABSTRACT   ["vpack"] = """
Pack three scalar components into a vector.
"""
SPYCE_DEFINITIONS["vpack"] = {
"x": "First scalar component of a 3-vector.",
"y": "Second scalar component of a 3-vector.",
"z": "Third scalar component of a 3-vector.",
"vout": "Equivalent 3-vector.",
}
SPYCE_URL["vpack"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vpack_c.html"

#########################################
SPYCE_SIGNATURES ["vperp"] = 2*["float[3]"]
SPYCE_ARGNAMES   ["vperp"] = ["v1", "v2"]
SPYCE_RETURNS    ["vperp"] = ["float[3]"]
SPYCE_RETNAMES   ["vperp"] = ["perp"]
SPYCE_ABSTRACT   ["vperp"] = """
Find the component of a vector that is perpendicular to a second vector.
All vectors are 3-dimensional.
"""
SPYCE_DEFINITIONS["vperp"] = {
"v1": "The vector whose orthogonal component is sought.",
"v2": "The vector used as the orthogonal reference.",
"perp": "The component of a orthogonal to b.",
}
SPYCE_URL["vperp"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vperp_c.html"

#########################################
SPYCE_SIGNATURES ["vprjp"] = ["float[3]", "float[4]"]
SPYCE_ARGNAMES   ["vprjp"] = ["vin", "plane"]
SPYCE_RETURNS    ["vprjp"] = ["float[3]"]
SPYCE_RETNAMES   ["vprjp"] = ["vout"]
SPYCE_ABSTRACT   ["vprjp"] = """
Project a vector onto a specified plane, orthogonally.
"""
SPYCE_DEFINITIONS["vprjp"] = {
"vin": "Vector to be projected.",
"plane": "A CSPICE plane onto which vin is projected.",
"vout": "Vector resulting from projection.",
}
SPYCE_URL["vprjp"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vprjp_c.html"

#########################################
SPYCE_SIGNATURES ["vprjpi"] = ["float[3]", "float[4]", "float[4]"]
SPYCE_ARGNAMES   ["vprjpi"] = ["vin", "projpl", "invpl"]
SPYCE_RETURNS    ["vprjpi"] = ["float[3]", "bool"]
SPYCE_RETNAMES   ["vprjpi"] = ["vout", "found"]
SPYCE_ABSTRACT   ["vprjpi"] = """
Find the vector in a specified plane that maps to a specified vector in
another plane under orthogonal projection.
"""
SPYCE_DEFINITIONS["vprjpi"] = {
"vin": "The projected vector.",
"projpl": "Plane containing vin.",
"invpl": "Plane containing inverse image of vin.",
"vout": "Inverse projection of vin.",
"found": "Flag indicating whether vout could be calculated.",
}
SPYCE_URL["vprjpi"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vprjpi_c.html"

#########################################
SPYCE_SIGNATURES ["vproj"] = ["float[3]", "float[3]"]
SPYCE_ARGNAMES   ["vproj"] = ["v1", "v2"]
SPYCE_RETURNS    ["vproj"] = ["float[3]"]
SPYCE_RETNAMES   ["vproj"] = ["proj"]
SPYCE_ABSTRACT   ["vproj"] = """
Find the projection of one vector onto another vector. All vectors are
3-dimensional.
"""
SPYCE_DEFINITIONS["vproj"] = {
"v1": "The vector to be projected.",
"v2": "The vector onto which a is to be projected.",
"proj": "The projection of a onto b.",
}
SPYCE_URL["vproj"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vproj_c.html"

#########################################
SPYCE_SIGNATURES ["vrel"] = ["float[3]", "float[3]"]
SPYCE_ARGNAMES   ["vrel"] = ["v1", "v2"]
SPYCE_RETURNS    ["vrel"] = ["float"]
SPYCE_RETNAMES   ["vrel"] = ["value"]
SPYCE_ABSTRACT   ["vrel"] = """
Return the relative difference between two 3-dimensional vectors.
"""
SPYCE_DEFINITIONS["vrel"] = {
"v1": "The first of two 3-vectors.",
"v2": "The second of two 3-vectors.",
"value": "The relative difference.",
}
SPYCE_URL["vrel"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vrel_c.html"

#########################################
SPYCE_SIGNATURES ["vrelg"] = ["float[*]", "float[*]"]
SPYCE_ARGNAMES   ["vrelg"] = ["v1", "v2"]
SPYCE_RETURNS    ["vrelg"] = ["float"]
SPYCE_RETNAMES   ["vrelg"] = ["value"]
SPYCE_ABSTRACT   ["vrelg"] = """
Return the relative difference between two vectors of general dimension.
"""
SPYCE_DEFINITIONS["vrelg"] = {
"v1": "The first of two 3-vectors.",
"v2": "The second of two 3-vectors.",
"value": "The relative difference.",
}
SPYCE_URL["vrelg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vrelg_c.html"

#########################################
SPYCE_SIGNATURES ["vrotv"] = ["float[3]", "float[3]", "float"]
SPYCE_ARGNAMES   ["vrotv"] = ["v", "axis", "theta"]
SPYCE_RETURNS    ["vrotv"] = ["float[3]"]
SPYCE_RETNAMES   ["vrotv"] = ["r"]
SPYCE_ABSTRACT   ["vrotv"] = """
Rotate a vector about a specified axis vector by a specified angle and
return the rotated vector.
"""
SPYCE_DEFINITIONS["vrotv"] = {
"v": "Vector to be rotated.",
"axis": "Axis of the rotation.",
"theta": "Angle of rotation (radians).",
"r": "Result of rotating v about axis by theta.",
}
SPYCE_URL["vrotv"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vrotv_c.html"

#########################################
SPYCE_SIGNATURES ["vscl"] = ["float", "float[3]"]
SPYCE_ARGNAMES   ["vscl"] = ["s", "v1"]
SPYCE_RETURNS    ["vscl"] = ["float[3]"]
SPYCE_RETNAMES   ["vscl"] = ["vout"]
SPYCE_ABSTRACT   ["vscl"] = """
Multiply a scalar and a 3-dimensional double precision vector.
"""
SPYCE_DEFINITIONS["vscl"] = {
"s": "Scalar to multiply a vector.",
"v1": "Vector to be multiplied.",
"vout": "Product vector, s*v1.",
}
SPYCE_URL["vscl"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vscl_c.html"

#########################################
SPYCE_SIGNATURES ["vsclg"] = ["float", "float[*]"]
SPYCE_ARGNAMES   ["vsclg"] = ["s", "v1"]
SPYCE_RETURNS    ["vsclg"] = ["float[*]"]
SPYCE_RETNAMES   ["vsclg"] = ["vout"]
SPYCE_ABSTRACT   ["vsclg"] = """
Multiply a scalar and a double precision vector of arbitrary dimension.
"""
SPYCE_DEFINITIONS["vsclg"] = {
"s": "Scalar to multiply a vector.",
"v1": "Vector to be multiplied.",
"vout": "Product vector, s*v1.",
}
SPYCE_URL["vsclg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vsclg_c.html"

#########################################
SPYCE_SIGNATURES ["vsep"] = ["float[3]", "float[3]"]
SPYCE_ARGNAMES   ["vsep"] = ["v1", "v2"]
SPYCE_RETURNS    ["vsep"] = ["float"]
SPYCE_RETNAMES   ["vsep"] = ["value"]
SPYCE_ABSTRACT   ["vsep"] = """
Find the separation angle in radians between two double precision,
3-dimensional vectors.  This angle is defined as zero if either vector
is zero.
"""
SPYCE_DEFINITIONS["vsep"] = {
"v1": "First vector.",
"v2": "Second vector.",
"value": "The separation angle in radians.",
}
SPYCE_URL["vsep"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vsep_c.html"

#########################################
SPYCE_SIGNATURES ["vsepg"] = ["float[*]", "float[*]"]
SPYCE_ARGNAMES   ["vsepg"] = ["v1", "v2"]
SPYCE_RETURNS    ["vsepg"] = ["float"]
SPYCE_RETNAMES   ["vsepg"] = ["value"]
SPYCE_ABSTRACT   ["vsepg"] = """
Find the separation angle in radians between two double precision
vectors of arbitrary dimension. This angle is defined as zero if either
vector is zero.
"""
SPYCE_DEFINITIONS["vsepg"] = {
"v1": "First vector.",
"v2": "Second vector.",
"value": "The separation angle in radians.",
}
SPYCE_URL["vsepg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vsepg_c.html"

#########################################
SPYCE_SIGNATURES ["vsub"] = ["float[3]", "float[3]"]
SPYCE_ARGNAMES   ["vsub"] = ["v1", "v2"]
SPYCE_RETURNS    ["vsub"] = ["float[3]"]
SPYCE_RETNAMES   ["vsub"] = ["vout"]
SPYCE_ABSTRACT   ["vsub"] = """
Compute the difference between two 3-dimensional, double precision
vectors.
"""
SPYCE_DEFINITIONS["vsub"] = {
"v1": "First vector (minuend).",
"v2": "Second vector (subtrahend).",
"vout": "Difference vector, v1 - v2.",
}
SPYCE_URL["vsub"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vsub_c.html"

#########################################
SPYCE_SIGNATURES ["vsubg"] = ["float[*]", "float[*]"]
SPYCE_ARGNAMES   ["vsubg"] = ["v1", "v2"]
SPYCE_RETURNS    ["vsubg"] = ["float[*]"]
SPYCE_RETNAMES   ["vsubg"] = ["vout"]
SPYCE_ABSTRACT   ["vsubg"] = """
Compute the difference between two double precision vectors of arbitrary
dimension.
"""
SPYCE_DEFINITIONS["vsubg"] = {
"v1": "First vector (minuend).",
"v2": "Second vector (subtrahend).",
"vout": "Difference vector, v1 - v2.",
}
SPYCE_URL["vsubg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vsubg_c.html"

#########################################
SPYCE_SIGNATURES ["vtmv"] = ["float[3]", "float[3,3]", "float[3]"]
SPYCE_ARGNAMES   ["vtmv"] = ["v1", "matrix", "v2"]
SPYCE_RETURNS    ["vtmv"] = ["float"]
SPYCE_RETNAMES   ["vtmv"] = ["value"]
SPYCE_ABSTRACT   ["vtmv"] = """
Multiply the transpose of a 3-dimensional column vector, a 3x3 matrix,
and a 3-dimensional column vector.
"""
SPYCE_DEFINITIONS["vtmv"] = {
"v1": "3 dimensional double precision column vector.",
"matrix": "3x3 double precision matrix.",
"v2": "3 dimensional double precision column vector.",
"value": "The result of (v1**t * matrix * v2).",
}
SPYCE_URL["vtmv"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vtmv_c.html"

#########################################
SPYCE_SIGNATURES ["vtmvg"] = ["float[*]", "float[*,*]", "float[*]"]
SPYCE_ARGNAMES   ["vtmvg"] = ["v1", "matrix", "v2"]
SPYCE_RETURNS    ["vtmvg"] = ["float"]
SPYCE_RETNAMES   ["vtmvg"] = ["value"]
SPYCE_ABSTRACT   ["vtmvg"] = """
Multiply the transpose of a n-dimensional column vector, a nxm matrix,
and a m-dimensional column vector.
"""
SPYCE_DEFINITIONS["vtmvg"] = {
"v1": "n-dimensional double precision column vector.",
"matrix": "nxm double precision matrix.",
"v2": "m-dimensional double porecision column vector.",
"value": "The result of (v1**t * matrix * v2).",
}
SPYCE_URL["vtmvg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vtmvg_c.html"

#########################################
SPYCE_SIGNATURES ["vupack"] = ["float[3]"]
SPYCE_ARGNAMES   ["vupack"] = ["v"]
SPYCE_RETURNS    ["vupack"] = 3*["float"]
SPYCE_RETNAMES   ["vupack"] = ["x", "y", "z"]
SPYCE_ABSTRACT   ["vupack"] = """
Unpack three scalar components from a vector.
"""
SPYCE_DEFINITIONS["vupack"] = {
"v": "3-vector.",
"x": "First scalar component of 3-vector.",
"y": "Second scalar component of 3-vector.",
"z": "Third scalar component of 3-vector.",
}
SPYCE_URL["vupack"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vupack_c.html"

#########################################
SPYCE_SIGNATURES ["vzero"] = ["float[3]"]
SPYCE_ARGNAMES   ["vzero"] = ["v"]
SPYCE_RETURNS    ["vzero"] = ["bool"]
SPYCE_RETNAMES   ["vzero"] = ["value"]
SPYCE_ABSTRACT   ["vzero"] = """
Indicate whether a 3-vector is the zero vector.
"""
SPYCE_DEFINITIONS["vzero"] = {
"v": "Vector to be tested.",
"value": "True if and only if v is the zero vector.",
}
SPYCE_URL["vzero"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vzero_c.html"

#########################################
SPYCE_SIGNATURES ["vzerog"] = ["float[*]"]
SPYCE_ARGNAMES   ["vzerog"] = ["v"]
SPYCE_RETURNS    ["vzerog"] = ["bool"]
SPYCE_RETNAMES   ["vzerog"] = ["value"]
SPYCE_ABSTRACT   ["vzerog"] = """
Indicate whether a general-dimensional vector is the zero vector.
"""
SPYCE_DEFINITIONS["vzerog"] = {
"v": "Vector to be tested.",
"value": "True if and only if v is the zero vector.",
}
SPYCE_URL["vzerog"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vzerog_c.html"

#########################################
SPYCE_SIGNATURES ["xf2eul"] = ["rotmat[6,6]"] + 3*["int"]
SPYCE_ARGNAMES   ["xf2eul"] = ["xform", "axisa", "axisb", "axisc"]
SPYCE_RETURNS    ["xf2eul"] = ["float[3]", "bool"]
SPYCE_RETNAMES   ["xf2eul"] = ["eulang", "unique"]
SPYCE_ABSTRACT   ["xf2eul"] = """
Convert a state transformation matrix to Euler angles and their
derivatives with respect to a specified set of axes. The companion
routine eul2xf converts Euler angles and their derivatives with respect
to a specified set of axes to a state transformation matrix.
"""
SPYCE_DEFINITIONS["xf2eul"] = {
"xform": "A state transformation matrix.",
"axisa": "Axis A of the Euler angle factorization.",
"axisb": "Axis B of the Euler angle factorization.",
"axisc": "Axis C of the Euler angle factorization.",
"eulang": "An array of Euler angles and their derivatives.",
"unique": "Indicates if eulang is a unique representation.",
}
SPYCE_URL["xf2eul"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/xf2eul_c.html"

#########################################
SPYCE_SIGNATURES ["xf2rav"] = ["rotmat[6,6]"]
SPYCE_ARGNAMES   ["xf2rav"] = ["xform"]
SPYCE_RETURNS    ["xf2rav"] = ["rotmat[3,3]", "float[3]"]
SPYCE_RETNAMES   ["xf2rav"] = ["rot", "av"]
SPYCE_ABSTRACT   ["xf2rav"] = """
This routine determines from a state transformation matrix the
associated rotation matrix and angular velocity of the rotation.
"""
SPYCE_DEFINITIONS["xf2rav"] = {
"xform": "a state transformation matrix.",
"rot": "the rotation associated with xform.",
"av": "the angular velocity associated with xform.",
}
SPYCE_URL["xf2rav"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/xf2rav_c.html"

#########################################
SPYCE_SIGNATURES ["xfmsta"] = ["float[6]", "string", "string", "string"]
SPYCE_ARGNAMES   ["xfmsta"] = ["instate", "insys", "outsys", "body"]
SPYCE_RETURNS    ["xfmsta"] = ["float[6]"]
SPYCE_RETNAMES   ["xfmsta"] = ["outstate"]
SPYCE_ABSTRACT   ["xfmsta"] = """
Transform a state between coordinate systems.
"""
SPYCE_DEFINITIONS["xfmsta"] = {
"instate": "Input state.",
"insys": "Current (input) coordinate system.",
"outsys": "Desired (output) coordinate system.",
"body": "Name or NAIF ID of body with which coordinates are associated (if applicable).",
"outstate": "Converted output state.",
}
SPYCE_URL["xfmsta"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/xfmsta_c.html"

#########################################
SPYCE_SIGNATURES ["xpose6"] = ["float[6,6]"]
SPYCE_ARGNAMES   ["xpose6"] = ["m1"]
SPYCE_RETURNS    ["xpose6"] = ["float[6,6]"]
SPYCE_RETNAMES   ["xpose6"] = ["mout"]
SPYCE_ABSTRACT   ["xpose6"] = """
Transpose a 6x6 matrix.
"""
SPYCE_DEFINITIONS["xpose6"] = {
"m1": "6x6 matrix to be transposed.",
"mout": "Transpose of m1.",
}
SPYCE_URL["xpose6"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/xpose6_c.html"

#########################################
SPYCE_SIGNATURES ["xpose"] = ["float[3,3]"]
SPYCE_ARGNAMES   ["xpose"] = ["m1"]
SPYCE_RETURNS    ["xpose"] = ["float[3,3]"]
SPYCE_RETNAMES   ["xpose"] = ["mout"]
SPYCE_ABSTRACT   ["xpose"] = """
Transpose a 3x3 matrix.
"""
SPYCE_DEFINITIONS["xpose"] = {
"m1": "3x3 matrix to be transposed.",
"mout": "Transpose of m1.",
}
SPYCE_URL["xpose"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/xpose_c.html"

#########################################
SPYCE_SIGNATURES ["xposeg"] = ["float[*,*]"]
SPYCE_ARGNAMES   ["xposeg"] = ["matrix"]
SPYCE_RETURNS    ["xposeg"] = ["float[*,*]"]
SPYCE_RETNAMES   ["xposeg"] = ["xposem"]
SPYCE_ABSTRACT   ["xposeg"] = """
Transpose a matrix of arbitrary size (in place, the matrix need not be
square).
"""
SPYCE_DEFINITIONS["xposeg"] = {
"matrix": "Matrix to be transposed.",
"xposem": "Transposed matrix.",
}
SPYCE_URL["xposeg"] = "https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/xposeg_c.html"

#########################################
