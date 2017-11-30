################################################################################
# A dictionary of docstrings and call signatures, keyed by the name of the
# CSPICE function name
################################################################################

SPICE_SIGNATURES = {}
SPICE_DEFAULTS   = {}
SPICE_RETURNS    = {}
SPICE_DOCSTRINGS = {}

SPICE_SIGNATURES["axisar"] = ["int", "float"]
SPICE_RETURNS   ["axisar"] = ["float[3,3]"]
SPICE_DOCSTRINGS["axisar"] = """
Construct a rotation matrix that rotates vectors by a specified angle about
a specified axis.

axisar(<int> axis, <float> angle) -> <float[3,3]> rotmat

axis   = Rotation axis.
angle  = Rotation angle, in radians.
rotmat = Rotation matrix corresponding to axis and angle.
"""

#########################################
SPICE_SIGNATURES["b1900"] = []
SPICE_RETURNS   ["b1900"] = ["float"]
SPICE_DOCSTRINGS["b1900"] = """
Return the Julian Date corresponding to Besselian Date 1900.0.

b1900() -> <float> JD of B1900.
"""

#########################################
SPICE_SIGNATURES["b1950"] = []
SPICE_RETURNS   ["b1950"] = ["float"]
SPICE_DOCSTRINGS["b1950"] = """
Return the Julian Date corresponding to Besselian Date 1950.0.

b1950() -> <float> JD of B1950.
"""

#########################################
SPICE_SIGNATURES["bodc2n"] = ["body_code"]
SPICE_RETURNS   ["bodc2n"] = ["body_name", "bool"]
SPICE_DOCSTRINGS["bodc2n"] = """
Translate the SPICE integer code of a body into a common name for that body.

bodc2n(<int> code) -> [<string> name, <bool> found]

code  = Integer ID code to be translated into a name.
name  = A common name for the body identified by code.
found = True if translated, otherwise False.
"""

SPICE_SIGNATURES["bodc2n_error"] = ["body_code"]
SPICE_RETURNS   ["bodc2n_error"] = ["body_name"]
SPICE_DOCSTRINGS["bodc2n_error"] = """
Translate the SPICE integer code of a body into a common name for that body.

bodc2n(<int> code) -> <string> name

code  = Integer ID code to be translated into a name.
name  = A common name for the body identified by code.

Raise KeyError if code cound not be translated.
"""

#########################################
SPICE_SIGNATURES["bodc2s"] = ["body_code"]
SPICE_RETURNS   ["bodc2s"] = ["body_name"]
SPICE_DOCSTRINGS["bodc2s"] = """
Translate a body ID code to either the corresponding name or if no name to
ID code mapping exists, the string representation of the body ID value.

bodc2s(<int> code) -> <string> name

code = Integer ID code to translate to a string.
name = String corresponding to 'code'.
"""

#########################################
SPICE_SIGNATURES["boddef"] = ["string", "int"]
SPICE_RETURNS   ["boddef"] = []
SPICE_DOCSTRINGS["boddef"] = """
Define a body name/ID code pair for later translation via bodn2c or bodc2n.

boddef(<string> name, <int> code)

name = Common name of some body.
code = Integer code for that body.
"""

#########################################
SPICE_SIGNATURES["bodfnd"] = ["body_code", "string"]
SPICE_RETURNS   ["bodfnd"] = ["bool"]
SPICE_DOCSTRINGS["bodfnd"] = """
Determine whether values exist for some item for any body in the kernel
pool.

bodfnd(<int> body, <string> item) -> <bool> found

body  = ID code of body.
item  = Item to find ("RADII", "NUT_AMP_RA", etc.).
found = True if the item is in the kernel pool; False if it is not.
"""

#########################################
SPICE_SIGNATURES["bodn2c"] = ["body_name"]
SPICE_RETURNS   ["bodn2c"] = ["body_code", "bool"]
SPICE_DOCSTRINGS["bodn2c"] = """
Translate the name of a body or object to the corresponding SPICE integer
ID code.

bodn2c(<string> name) -> [<int> code, <bool> found]

name  = Body name to be translated into a SPICE ID code.
code  = SPICE integer ID code for the named body.
found = True if translated, otherwise False.
"""

SPICE_SIGNATURES["bodn2c_error"] = ["body_name"]
SPICE_RETURNS   ["bodn2c_error"] = ["body_code"]
SPICE_DOCSTRINGS["bodn2c_error"] = """
Translate the name of a body or object to the corresponding SPICE integer
ID code.

bodn2c(<string> name) -> <int> code

name  = Body name to be translated into a SPICE ID code.
code  = SPICE integer ID code for the named body.

Raise KeyError if name cound not be translated.
"""

#########################################
SPICE_SIGNATURES["bods2c"] = ["body_name"]
SPICE_RETURNS   ["bods2c"] = ["body_code", "bool"]
SPICE_DOCSTRINGS["bods2c"] = """
Translate a string containing a body name or ID code to an integer code.

bods2c(<string> name) -> [<int> code, <bool> found]

name  = String to be translated to an ID code.
code  = Integer ID code corresponding to `name'.
found = True if translated, otherwise False.
"""

SPICE_SIGNATURES["bods2c_error"] = ["body_name"]
SPICE_RETURNS   ["bods2c_error"] = ["body_code"]
SPICE_DOCSTRINGS["bods2c_error"] = """
Translate a string containing a body name or ID code to an integer code.

bods2c(<string> name) -> <int> code

name  = String to be translated to an ID code.
code  = Integer ID code corresponding to `name'.

Raise KeyError if name cound not be translated.
"""

#########################################
SPICE_SIGNATURES["bodvcd"] = ["body_code", "string"]
SPICE_RETURNS   ["bodvcd"] = ["float[*]"]
SPICE_DOCSTRINGS["bodvcd"] = """
Fetch from the kernel pool the float values of an item associated with a
body, where the body is specified by an integer ID code.

bodvcd(<int> bodyid, <string> item) -> <float[*]> values

bodyid = Body ID code.
item   = Item for which values are desired. ("RADII", "NUT_PREC_ANGLES",
         etc.).
values = Values as an array.
"""

#########################################
SPICE_SIGNATURES["bodvrd"] = ["body_name", "string"]
SPICE_RETURNS   ["bodvrd"] = ["float[*]"]
SPICE_DOCSTRINGS["bodvrd"] = """
Fetch from the kernel pool the double precision values of an item
associated with a body.

bodvrd(<string> bodynm, <string> item) -> <float[*]> values

bodynm = Body name.
item   = Item for which values are desired. ("RADII", "NUT_PREC_ANGLES",
         etc.).
values = Values as an array.
"""

#########################################
SPICE_SIGNATURES["cgv2el"] = 3*["float[3]"]
SPICE_RETURNS   ["cgv2el"] = ["float[9]"]
SPICE_DOCSTRINGS["cgv2el"] = """
Form a CSPICE ellipse from a center vector and two generating vectors.

cgv2el(<float[3]> center, <float[3]> vec1,
                          <float[3]> vec2) -> <float[9]> ellipse

center     = center vector
vec1, vec2 = two generating vectors for an ellipse.
ellipse    = the CSPICE ellipse defined by the input vectors.
"""

#########################################
SPICE_SIGNATURES["cidfrm"] = ["body_code"]
SPICE_RETURNS   ["cidfrm"] = ["frame_code", "frame_name", "bool"]
SPICE_DOCSTRINGS["cidfrm"] = """
Retrieve frame ID code and name to associate with a frame center.

cidfrm(<int> cent) ->[<int> frcode, <string> frname, <bool> found]

cent   = An object ID to associate a frame with.
frcode = The ID code of the frame associated with cent.
frname = The name of the frame with ID frcode.
found  = True if the requested information is available.
"""

SPICE_SIGNATURES["cidfrm_error"] = ["body_code"]
SPICE_RETURNS   ["cidfrm_error"] = ["frame_code", "frame_name"]
SPICE_DOCSTRINGS["cidfrm_error"] = """
Retrieve frame ID code and name to associate with a frame center.

cidfrm(<int> cent) ->[<int> frcode, <string> frname, <bool> found]

cent   = An object ID to associate a frame with.
frcode = The ID code of the frame associated with cent.
frname = The name of the frame with ID frcode.

Raise KeyError if the requested information is unavailable.
"""

#########################################
SPICE_SIGNATURES["ckcov"] = ["string", "body_code", "bool", "string", "float",
                             "string"]
SPICE_RETURNS   ["ckcov"] = ["float[*,2]"]
SPICE_DOCSTRINGS["ckcov"] = """
Find the coverage window for a specified object in a specified CK file.

ckcov(<string> ck, <int> idcode, <bool> needav, <string> level,
      <float> tol, <string> timsys) -> <float[*,2]> cover

ck     = Name of CK file.
idcode = ID code of object.
needav = Flag indicating whether angular velocity is needed.
level  = Coverage level:  "SEGMENT" OR "INTERVAL".
tol    = Tolerance in ticks.
timsys = Time system used to represent coverage.
cover  = array of shape (intervals,2) where cover[:,0] are start times and
         cover[:,1] are stop times.
"""

SPICE_SIGNATURES["ckcov_error"] = ["string", "body_code", "bool", "string",
                                   "float", "string"]
SPICE_RETURNS   ["ckcov_error"] = ["float[*,2]"]
SPICE_DOCSTRINGS["ckcov_error"] = """
Find the coverage window for a specified object in a specified CK file.

ckcov(<string> ck, <int> idcode, <bool> needav, <string> level,
      <float> tol, <string> timsys) -> <float[*,2]> cover

ck     = Name of CK file.
idcode = ID code of object.
needav = Flag indicating whether angular velocity is needed.
level  = Coverage level:  "SEGMENT" OR "INTERVAL".
tol    = Tolerance in ticks.
timsys = Time system used to represent coverage.
cover  = array of shape (intervals,2) where cover[:,0] are start times and
         cover[:,1] are stop times.

Raise KeyError if body code is not found.
"""

#########################################
SPICE_SIGNATURES["ckgp"] = ["body_code", "float", "float", "frame_name"]
SPICE_RETURNS   ["ckgp"] = ["float[3,3]", "float", "bool"]
SPICE_DOCSTRINGS["ckgp"] = """
Get pointing(attitude) for a specified spacecraft clock time.

ckgp(<int> inst, <float> sclkdp, <float> tol, <string> ref) ->
                        [<float[3,3]> cmat, <float> clkout, <bool> found]

inst   = NAIF ID of instrument, spacecraft, or structure.
sclkdp = Encoded spacecraft clock time.
tol    = Time tolerance.
ref    = Reference frame.
cmat   = C-matrix pointing data.
clkout = Output encoded spacecraft clock time.
found  = True when requested pointing is available.
"""

SPICE_SIGNATURES["ckgp_error"] = ["body_code", "float", "float", "frame_name"]
SPICE_RETURNS   ["ckgp_error"] = ["float[3,3]", "float"]
SPICE_DOCSTRINGS["ckgp_error"] = """
Get pointing (attitude) for a specified spacecraft clock time.

ckgp(<int> inst, <float> sclkdp, <float> tol, <string> ref) ->
                                [<float[3,3]> cmat, <float> clkout]

inst   = NAIF ID of instrument, spacecraft, or structure.
sclkdp = Encoded spacecraft clock time.
tol    = Time tolerance.
ref    = Reference frame.
cmat   = C-matrix pointing data.
clkout = Output encoded spacecraft clock time.

Raise ValueError if the requested pointing is unavailable.
"""

#########################################
SPICE_SIGNATURES["ckgpav"] = ["body_code", "float", "float", "frame_name"]
SPICE_RETURNS   ["ckgpav"] = ["float[3,3]", "float[3]", "float", "bool"]
SPICE_DOCSTRINGS["ckgpav"] = """
Get pointing(attitude) and angular velocity for a spacecraft clock time.

ckgpav(<int> inst, <float> sclkdp, <float> tol, <string> ref) ->
            [<float[3,3]> cmat, <float[3]> av, <float> clkout, <bool> found]

inst   = NAIF ID of instrument, spacecraft, or structure.
sclkdp = Encoded spacecraft clock time.
tol    = Time tolerance.
ref    = Reference frame.
cmat   = C-matrix pointing data.
av     = Angular velocity vector.
clkout = Output encoded spacecraft clock time.
found  = True when requested pointing is available.
"""

SPICE_SIGNATURES["ckgpav_error"] = ["body_code", "float", "float", "frame_name"]
SPICE_RETURNS   ["ckgpav_error"] = ["float[3,3]", "float[3]", "float"]
SPICE_DOCSTRINGS["ckgpav_error"] = """
Get pointing (attitude) and angular velocity for a spacecraft clock time.

ckgpav(<int> inst, <float> sclkdp, <float> tol, <string> ref) ->
            [<float[3,3]> cmat, <float[3]> av, <float> clkout]

inst   = NAIF ID of instrument, spacecraft, or structure.
sclkdp = Encoded spacecraft clock time.
tol    = Time tolerance.
ref    = Reference frame.
cmat   = C-matrix pointing data.
av     = Angular velocity vector.
clkout = Output encoded spacecraft clock time.

Raise ValueError if the requested pointing is unavailable.
"""

#########################################
SPICE_SIGNATURES["ckobj"] = ["string"]
SPICE_RETURNS   ["ckobj"] = ["int[*]"]
SPICE_DOCSTRINGS["ckobj"] = """
Find the set of ID codes of all objects in a specified CK file.

ckobj(<string> ck) -> <int[*]> ids

ck  = Name of CK file.
ids = Array of ID codes of objects in CK file.
"""

#########################################
SPICE_SIGNATURES["clight"] = []
SPICE_RETURNS   ["clight"] = ["float"]
SPICE_DOCSTRINGS["clight"] = """
Return the speed of light in a vacuum (IAU official value, in km/sec).

clight() -> <float> value
"""

#########################################
SPICE_SIGNATURES["clpool"] = []
SPICE_RETURNS   ["clpool"] = []
SPICE_DOCSTRINGS["clpool"] = """
Remove all variables from the kernel pool.

clpool()
"""

#########################################
SPICE_SIGNATURES["cnmfrm"] = ["body_name"]
SPICE_RETURNS   ["cnmfrm"] = ["frame_code", "frame_name", "bool"]
SPICE_DOCSTRINGS["cnmfrm"] = """
Retrieve frame ID code and name to associate with an object.

cnmfrm(<string> cname) -> [<int> frcode, <string> frname, <bool> found]

cname  = Name of the object to find a frame for.
frcode = The ID code of the frame associated with cname.
frname = The name of the frame with ID frcode.
found  = True if the requested information is available.
"""

SPICE_SIGNATURES["cnmfrm_error"] = ["body_name"]
SPICE_RETURNS   ["cnmfrm_error"] = ["frame_code", "frame_name"]
SPICE_DOCSTRINGS["cnmfrm_error"] = """
Retrieve frame ID code and name to associate with an object.

cnmfrm(<string> cname) -> [<int> frcode, <string> frname, <bool> found]

cname  = Name of the object to find a frame for.
frcode = The ID code of the frame associated with cname.
frname = The name of the frame with ID frcode.

Raise KeyError if the requested information is unavailable.
"""

#########################################
SPICE_SIGNATURES["conics"] = ["float[8]", "float"]
SPICE_RETURNS   ["conics"] = ["float[6]"]
SPICE_DOCSTRINGS["conics"] = """
Determine the state (position, velocity) of an orbiting body from a set of
elliptic, hyperbolic, or parabolic orbital elements.

conics(<float[8]> elts, <float> et) -> <float[6]> state

elts  = Conic elements.
et    = Input time.
state = State of orbiting body at et.
"""

#########################################
SPICE_SIGNATURES["convrt"] = ["float", "string", "string"]
SPICE_RETURNS   ["convrt"] = ["float"]
SPICE_DOCSTRINGS["convrt"] = """
Take a measurement X, the units associated with X, and units to which X
should be converted; return Y, the value of the measurement in the output
units.

convrt(<float> x, <string> in, <string> out) -> <float> y

x   = Number representing a measurement in some units.
in  = The units in which x is measured.
out = Desired units for the measurement.
y   = The measurment in the desired units.
"""

#########################################
SPICE_SIGNATURES["cyllat"] = 3*["float"]
SPICE_RETURNS   ["cyllat"] = 3*["float"]
SPICE_DOCSTRINGS["cyllat"] = """
Convert from cylindrical to latitudinal coordinates.

cyllat(<float> r, <float> lonc, <float> z) -> [<float> radius, <float> lon,
                                               <float> lat]

r      = Distance of point from z axis.
lonc   = Cylindrical angle of point from XZ plane (radians).
z      = Height of point above XY plane.
radius = Distance of point from origin.
lon    = Longitude of point (radians).
lat    = Latitude of point  (radians).
"""

#########################################
SPICE_SIGNATURES["cylrec"] = 3*["float"]
SPICE_RETURNS   ["cylrec"] = ["float[3]"]
SPICE_DOCSTRINGS["cylrec"] = """
Convert from cylindrical to rectangular coordinates.

cylrec(<float> r, <float> lon, <float> z) -> <float[3]> rectan

r      = Distance of a point from z axis.
lon    = Angle (radians) of a point from xZ plane
z      = Height of a point above xY plane.
rectan = Rectangular coordinates of the point.
"""

#########################################
SPICE_SIGNATURES["cylsph"] = 3*["float"]
SPICE_RETURNS   ["cylsph"] = 3*["float"]
SPICE_DOCSTRINGS["cylsph"] = """
Convert from cylindrical to spherical coordinates.

cylsph(<float> r, <float> lonc, <float> z) ->
                        [<float> radius, <float> colat, <float> lon]

r      = Distance of point from z axis.
lonc   = Angle (radians) of point from XZ plane.
z      = Height of point above XY plane.
radius = Distance of point from origin.
colat  = Polar angle (co-latitude in radians) of point.
lon    = Azimuthal angle (longitude) of point (radians).
"""

#########################################
SPICE_SIGNATURES["dcyldr"] = 3*["float"]
SPICE_RETURNS   ["dcyldr"] = ["float[3,3]"]
SPICE_DOCSTRINGS["dcyldr"] = """
This routine computes the Jacobian of the transformation from rectangular
to cylindrical coordinates.

dcyldr(<float> x, <float> y, <float> z) -> <float[3,3]> jacobi

x      = X-coordinate of point.
y      = Y-coordinate of point.
z      = Z-coordinate of point.
jacobi = Matrix of partial derivatives.
"""

#########################################
SPICE_SIGNATURES["deltet"] = ["float", "string"]
SPICE_RETURNS   ["deltet"] = ["float"]
SPICE_DOCSTRINGS["deltet"] = """
Return the value of Delta ET (ET-UTC) for an input epoch.

deltet(<float> epoch, <string> eptype) -> <float> delta

epoch  = Input epoch (seconds past J2000).
eptype = Type of input epoch ("UTC" or "ET").
delta  = Delta ET (ET-UTC) at input epoch.
"""

#########################################
SPICE_SIGNATURES["det"] = ["float[3,3]"]
SPICE_RETURNS   ["det"] = ["float"]
SPICE_DOCSTRINGS["det"] = """
Compute the determinant of a double precision 3x3 matrix.

det(<float[3,3]> m1) -> <float> value

m1    =  Matrix whose determinant is to be found.
value = value of determinant.
"""

#########################################
SPICE_SIGNATURES["dgeodr"] = 5*["float"]
SPICE_RETURNS   ["dgeodr"] = ["float[3,3]"]
SPICE_DOCSTRINGS["dgeodr"] = """
This routine computes the Jacobian of the transformation from
rectangular to geodetic coordinates.

dgeodr(<float> x, <float> y, <float> z,
                  <float> re, <float> f) -> <float[3,3]> jacobi

x      = X-coordinate of point.
y      = Y-coordinate of point.
z      = Z-coordinate of point.
re     = Equatorial radius of the reference spheroid.
f      = Flattening coefficient.
jacobi = Matrix of partial derivatives.
"""

#########################################
SPICE_SIGNATURES["diags2"] = ["float[2,2]"]
SPICE_RETURNS   ["diags2"] = 2*["float[2,2]"]
SPICE_DOCSTRINGS["diags2"] = """
Diagonalize a symmetric 2x2 matrix.

diags2(<float[2,2]> symmat) -> [<float[2,2]> diag, <float[2,2]> rotate]

symmat = A symmetric 2x2 matrix.
diag   = A diagonal matrix similar to symmat.
rotate = A rotation used as the similarity transformation.
"""

#########################################
SPICE_SIGNATURES["dlatdr"] = 3*["float"]
SPICE_RETURNS   ["dlatdr"] = ["float[3,3]"]
SPICE_DOCSTRINGS["dlatdr"] = """
This routine computes the Jacobian of the transformation from
rectangular to latitudinal coordinates.

dlatdr(<float> x, <float> y, <float> z) -> <float[3,3]> jacobi

x      = X-coordinate of point.
y      = Y-coordinate of point.
z      = Z-coordinate of point.
jacobi = Matrix of partial derivatives.
"""

#########################################
SPICE_SIGNATURES["dpgrdr"] = ["body_name"] + 5*["float"]
SPICE_RETURNS   ["dpgrdr"] = ["float[3,3]"]
SPICE_DOCSTRINGS["dpgrdr"] = """
This routine computes the Jacobian matrix of the transformation from
rectangular to planetographic coordinates.

dpgrdr(<string> body, <float> x, <float> y, <float> z,
                      <float> re, <float> f) -> <float[3,3]> jacobi

body   = Body with which coordinate system is associated.
x      = X-coordinate of point.
y      = Y-coordinate of point.
z      = Z-coordinate of point.
re     = Equatorial radius of the reference spheroid.
f      = Flattening coefficient.
jacobi = Matrix of partial derivatives.
"""

#########################################
SPICE_SIGNATURES["dpmax"] = []
SPICE_RETURNS   ["dpmax"] = ["float"]
SPICE_DOCSTRINGS["dpmax"] = """
Return the value of the largest (positive) number representable
in a double precision variable.

dpmax() -> <float> value
"""

#########################################
SPICE_SIGNATURES["dpmin"] = []
SPICE_RETURNS   ["dpmin"] = ["float"]
SPICE_DOCSTRINGS["dpmin"] = """
Return the value of the smallest (negative) number representable
in a double precision variable.

dpmin() -> <float> value
"""

#########################################
SPICE_SIGNATURES["dpr"] = []
SPICE_RETURNS   ["dpr"] = ["float"]
SPICE_DOCSTRINGS["dpr"] = """
Return the number of degrees per radian.

dpr() -> <float> value
"""

#########################################
SPICE_SIGNATURES["drdcyl"] = 3*["float"]
SPICE_RETURNS   ["drdcyl"] = ["float[3,3]"]
SPICE_DOCSTRINGS["drdcyl"] = """
This routine computes the Jacobian of the transformation from cylindrical
to rectangular coordinates.

drdcyl(<float> r, <float> lon, <float> z) -> <float[3,3]> jacobi

r      = Distance of a point from the origin.
lon    = Angle of the point from the xz plane in radians.
z      = Height of the point above the xy plane.
jacobi = Matrix of partial derivatives.
"""

#########################################
SPICE_SIGNATURES["drdgeo"] = 5*["float"]
SPICE_RETURNS   ["drdgeo"] = ["float[3,3]"]
SPICE_DOCSTRINGS["drdgeo"] = """
This routine computes the Jacobian of the transformation from
geodetic to rectangular coordinates.

drdgeo(<float> lon, <float> lat, <float> alt,
                    <float> re, <float> f) -> <float[3,3]> jacobi

lon    = Geodetic longitude of point (radians).
lat    = Geodetic latitude of point (radians).
alt    = Altitude of point above the reference spheroid.
re     = Equatorial radius of the reference spheroid.
f      = Flattening coefficient.
jacobi = Matrix of partial derivatives.
"""

#########################################
SPICE_SIGNATURES["drdlat"] = 3*["float"]
SPICE_RETURNS   ["drdlat"] = ["float[3,3]"]
SPICE_DOCSTRINGS["drdlat"] = """
Compute the Jacobian of the transformation from latitudinal to rectangular
coordinates.

drdlat(<float> r, <float> lon, <float> lat) -> <float[3,3]> jacobi

radius = Distance of a point from the origin.
lon    = Angle of the point from the XZ plane in radians.
lat    = Angle of the point from the XY plane in radians.
jacobi = Matrix of partial derivatives.
"""

#########################################
SPICE_SIGNATURES["drdpgr"] = ["body_name"] + 5*["float"]
SPICE_RETURNS   ["drdpgr"] = ["float[3,3]"]
SPICE_DOCSTRINGS["drdpgr"] = """
This routine computes the Jacobian matrix of the transformation from
planetographic to rectangular coordinates.

drdpgr(<string> body, <float> lon, <float> lat, <float> alt,
             <float> re, <float> f) -> <float[3,3]> jacobi

body   = Name of body with which coordinates are associated.
lon    = Planetographic longitude of a point (radians).
lat    = Planetographic latitude of a point (radians).
alt    = Altitude of a point above reference spheroid.
re     = Equatorial radius of the reference spheroid.
f      = Flattening coefficient.
jacobi = Matrix of partial derivatives.
"""

#########################################
SPICE_SIGNATURES["drdsph"] = 3*["float"]
SPICE_RETURNS   ["drdsph"] = ["float[3,3]"]
SPICE_DOCSTRINGS["drdsph"] = """
This routine computes the Jacobian of the transformation from spherical to
rectangular coordinates.

drdsph(<float> r, <float> colat, <float> lon) -> <float[3,3]> jacobi

r      = Distance of a point from the origin.
colat  = Angle of the point from the positive z-axis.
lon    = Angle of the point from the xy plane.
jacobi = Matrix of partial derivatives.
"""

#########################################
SPICE_SIGNATURES["dsphdr"] = 3*["float"]
SPICE_RETURNS   ["dsphdr"] = ["float[3,3]"]
SPICE_DOCSTRINGS["dsphdr"] = """
This routine computes the Jacobian of the transformation from rectangular
to spherical coordinates.

dsphdr(<float> x, <float> y, <float> z) -> <float[3,3]> jacobi

x      = x-coordinate of point.
y      = y-coordinate of point.
z      = z-coordinate of point.
jacobi = Matrix of partial derivatives.
"""

#########################################
SPICE_SIGNATURES["dtpool"] = ["string"]
SPICE_RETURNS   ["dtpool"] = ["bool", "int", "string"]
SPICE_DOCSTRINGS["dtpool"] = """
Return the data about a kernel pool variable.

dtpool(<string> name) -> [<bool> found, <int> n, <string> vtype]

name  = Name of the variable whose value is to be returned.
found = True if variable is in pool.
n     = Number of values returned for name.
vtype = Type of the variable:  'C', 'N', or 'X'
"""

SPICE_SIGNATURES["dtpool_error"] = ["string"]
SPICE_RETURNS   ["dtpool_error"] = ["int", "string"]
SPICE_DOCSTRINGS["dtpool_error"] = """
Return the data about a kernel pool variable.

dtpool(<string> name) -> [<int> n, <string> vtype]

name  = Name of the variable whose value is to be returned.
n     = Number of values returned for name.
vtype = Type of the variable:  'C', 'N', or 'X'

Raise KeyError if the variable is not in the pool.
"""

#########################################
SPICE_SIGNATURES["ducrss"] = 2*["float[6]"]
SPICE_RETURNS   ["ducrss"] = ["float[6]"]
SPICE_DOCSTRINGS["ducrss"] = """
Compute the unit vector parallel to the cross product of two 3-dimensional
vectors and the derivative of this unit vector.

ducrss(<float[6]> s1, <float[6]> s2) -> <float[6]> sout

s1   = Left hand state for cross product and derivative.
s2   = Right hand state for cross product and derivative.
sout = Unit vector and derivative of the cross product.
"""

#########################################
SPICE_SIGNATURES["dvcrss"] = 2*["float[6]"]
SPICE_RETURNS   ["dvcrss"] = ["float[6]"]
SPICE_DOCSTRINGS["dvcrss"] = """
Compute the cross product of two 3-dimensional vectors and the derivative
of this cross product.

dvcrss(<float[6]> s1, <float[6]> s2) -> <float[6]> sout

s1   = Left hand state for cross product and derivative.
s2   = Right hand state for cross product and derivative.
sout = State associated with cross product of positions.
"""

#########################################
SPICE_SIGNATURES["dvdot"] = 2*["float[6]"]
SPICE_RETURNS   ["dvdot"] = ["float[6]"]
SPICE_DOCSTRINGS["dvdot"] = """
Compute the derivative of the dot product of two double precision position
vectors.

dvdot(<float[6]> s1, <float[6]> s2) -> <float> value

s1    = First state vector in the dot product.
s2    = Second state vector in the dot product.
value = The derivative of the dot product <s1,s2>
"""

#########################################
SPICE_SIGNATURES["dvhat"] = ["float[6]"]
SPICE_RETURNS   ["dvhat"] = ["float"]
SPICE_DOCSTRINGS["dvhat"] = """
Find the unit vector corresponding to a state vector and the derivative of
the unit vector.

dvhat(<float[6]> s1) -> <float[6]> sout

s1   = State to be normalized.
sout = Unit vector s1 / |s1|, and its time derivative.
"""

#########################################
SPICE_SIGNATURES["dvnorm"] = ["float[6]"]
SPICE_RETURNS   ["dvnorm"] = ["float[6]"]
SPICE_DOCSTRINGS["dvnorm"] = """ TBD
Function to calculate the derivative of the norm of a 3-vector.

dvnorm(<float[6]> state) -> <float> value

state = A 6-vector composed of three coordinates and their derivatives.
value = derivative of the norm
"""

#########################################
SPICE_SIGNATURES["dvpool"] = ["string"]
SPICE_RETURNS   ["dvpool"] = []
SPICE_DOCSTRINGS["dvpool"] = """
Delete a variable from the kernel pool.

dvpool(<string> name)

name = Name of the kernel variable to be deleted.
"""

#########################################
SPICE_SIGNATURES["dvsep"] = 2*["float[6]"]
SPICE_RETURNS   ["dvsep"] = ["float"]
SPICE_DOCSTRINGS["dvsep"] = """
Calculate the time derivative of the separation angle between two input
states, S1 and S2.

dvsep(<float[6]> s1, <float[6]> s2) -> <float> value

s1    = State vector of the first body
s2    = State vector of the second  body
value = derivate of the separation angle between state vectors.
"""

#########################################
SPICE_SIGNATURES["edlimb"] = 3*["float"] + ["float[3]"]
SPICE_RETURNS   ["edlimb"] = ["float[9]"]
SPICE_DOCSTRINGS["edlimb"] = """
Find the limb of a triaxial ellipsoid, viewed from a specified point.

edlimb(<float> a, <float> b, <float> c,
                             <float[3]> viewpt) -> <float[9]> limb

a      = Length of ellipsoid semi-axis lying on the x-axis.
b      = Length of ellipsoid semi-axis lying on the y-axis.
c      = Length of ellipsoid semi-axis lying on the z-axis.
viewpt = Location of viewing point.
limb   = Limb of ellipsoid as seen from viewing point.
"""

#########################################
SPICE_SIGNATURES["edterm"] = ["string", "body_name", "body_name", "float",
                              "frame_name", "string", "body_name", "int"]
SPICE_RETURNS   ["edterm"] = ["float", "float[3]", "float[*,3]"]
SPICE_DOCSTRINGS["edterm"] = """
Compute a set of points on the umbral or penumbral terminator of a
specified target body, where the target shape is modeled as an ellipsoid.

edterm(<string> trmtyp, <string> source, <string> target, <float> et,
       <string> fixref, <string> abcorr, <string> obsrvr, npts) ->
                [<float> trgepc, <float[3]> obspos, <float[*,3]> trmpts]

trmtyp = Terminator type.
source = Light source.
target = Target body.
et     = Observation epoch.
fixref = Body-fixed frame associated with target.
abcorr = Aberration correction.
obsrvr = Observer.
npts   = Number of points in terminator set.
trgepc = Epoch associated with target center.
obspos = Position of observer in body-fixed frame.
trmpts = Terminator point set.
"""

#########################################
SPICE_SIGNATURES["el2cgv"] = ["float[9]"]
SPICE_RETURNS   ["el2cgv"] = 3*["float[3]"]
SPICE_DOCSTRINGS["el2cgv"] = """
Convert a CSPICE ellipse to a center vector and two generating vectors. 
The selected generating vectors are semi-axes of the ellipse.

el2cgv(<float[9]> ellipse) -> [<float[3]> center,
                               <float[3]> smajor, <float[3]> sminor]

ellipse                = A CSPICE ellipse.
center, smajor, sminor = Center and semi-axes of ellipse.
"""

#########################################
SPICE_SIGNATURES["eqncpv"] = ["float", "float", "float[9]", "float", "float"]
SPICE_RETURNS   ["eqncpv"] = ["float[6]"]
SPICE_DOCSTRINGS["eqncpv"] = """
Compute the state (position and velocity of an object whose trajectory is
described via equinoctial elements relative to some fixed plane (usually the
equatorial plane of some planet).

eqncpv(<float> et, <float> epoch, <float[9]> eqel,
                   <float> rapol, <float> decpol) -> <float[6]> state

et     = Epoch in seconds past J2000 to find state
epoch  = Epoch of elements in seconds past J2000
eqel   = Array of equinoctial elements
rapol  = Right Ascension of the pole of the reference plane
decpol = Declination of the pole of the reference plane
state  = State of the object described by eqel.
"""

#########################################
SPICE_SIGNATURES["erract"] = ["string", "string"]
SPICE_DEFAULTS  ["erract"] = ["GET", ""]
SPICE_RETURNS   ["erract"] = ["string"]
SPICE_DOCSTRINGS["erract"] = """
Retrieve or set the default error action.

erract(<string> op='GET', <string> action='') -> <string> action2

op      = Operation: "GET" or "SET"; default is "GET".
action  = Error response action for "SET"; ignored on "GET".
action2 = Current or new error response action.
"""

#########################################
SPICE_SIGNATURES["errch"] = 2*["string"]
SPICE_RETURNS   ["errch"] = []
SPICE_DOCSTRINGS["errch"] = """
Substitute a character string for the first occurrence of a marker in the
current long error message.

errch(<string> marker, <string> string)

marker = A substring of the error message to be replaced.
string = The character string to substitute for marker.
"""

#########################################
SPICE_SIGNATURES["errdev"] = ["string", "string"]
SPICE_DEFAULTS  ["errdev"] = ["GET", ""]
SPICE_RETURNS   ["errdev"] = ["string"]
SPICE_DOCSTRINGS["errdev"] = """
Retrieve or set the name of the current output device for error messages.

errdev(<string> op='GET', <string> device='') -> <string> device2

op      = The operation: "GET" or "SET"; default is "GET".
device  = The device name; ignored on "GET".
device2 = Current or new output device.
"""

#########################################
SPICE_SIGNATURES["errdp"] = ["string", "float"]
SPICE_RETURNS   ["errdp"] = []
SPICE_DOCSTRINGS["errdp"] = """
Substitute a double precision number for the first occurrence of a marker
found in the current long error message.

errdp(<string> marker, <float> number)

marker = A substring of the error message to be replaced.
number = The d.p. number to substitute for marker.
"""

#########################################
SPICE_SIGNATURES["errint"] = ["string", "int"]
SPICE_RETURNS   ["errint"] = []
SPICE_DOCSTRINGS["errint"] = """
Substitute an integer for the first occurrence of a marker found in the
current long error message.

errint(<string> marker, <int> number)

marker = A substring of the error message to be replaced.
number = The integer to substitute for marker.
"""

#########################################
SPICE_SIGNATURES["errprt"] = ["string", "string"]
SPICE_DEFAULTS  ["errprt"] = ["GET", ""]
SPICE_RETURNS   ["errprt"] = ["string"]
SPICE_DOCSTRINGS["errprt"] = """
Retrieve or set the list of error message items to be output when an error
is detected.

errprt(<string> op='GET', <string> list='') -> <string> list2

op    = The operation: "GET" or "SET"; default is "GET"
list  = Specification of error messages to be output on 'SET'; ignored on
        "GET".
list2 = The current or new list.
"""

#########################################
SPICE_SIGNATURES["et2lst"] = ["float", "body_code", "float", "string"]
SPICE_RETURNS   ["et2lst"] = 3*["float"] + 2*["string"]
SPICE_DOCSTRINGS["et2lst"] = """
Given an ephemeris epoch, compute the local solar time for an object on the
surface of a body at a specified longitude.

et2lst(<float> et, <int> body, <float> lon, <string> type) ->
            [<int> hr, <int> mn, <int> sc, <string> time, <string> ampm]

et   = Epoch in seconds past J2000 epoch.
body = ID-code of the body of interest.
lon  = Longitude of surface point (radians).
type = Type of longitude "PLANETOCENTRIC", etc.
hr   = Local hour on a "24 hour" clock.
mn   = Minutes past the hour.
sc   = Seconds past the minute.
time = String giving local time on 24 hour clock.
ampm = String giving time on A.M./ P.M. scale.
"""

#########################################
SPICE_SIGNATURES["et2utc"] = ["float", "string", "int"]
SPICE_RETURNS   ["et2utc"] = ["string"]
SPICE_DOCSTRINGS["et2utc"] = """
Convert an input time from ephemeris seconds past J2000 to Calendar,
Day-of-Year, or Julian Date format, UTC.

et2utc(<float> et, format, <float> prec) -> <string> utcstr

et     = Input epoch, given in ephemeris seconds past J2000.
format = Format of output epoch.
prec   = Digits of precision in fractional seconds or days.
utcstr = Output time string, UTC.
"""

#########################################
SPICE_SIGNATURES["etcal"] = ["float"]
SPICE_RETURNS   ["etcal"] = ["string"]
SPICE_DOCSTRINGS["etcal"] = """
Convert from an ephemeris epoch measured in seconds past the epoch of J2000
to a calendar string format using a formal calendar free of leapseconds.

etcal(<float> et) -> <string> string

et     = Ephemeris time measured in seconds past J2000.
string = A standard calendar representation of et.
"""

#########################################
SPICE_SIGNATURES["eul2m"] = 3*["float"] + 3*["int"]
SPICE_RETURNS   ["eul2m"] = ["float[3,3]"]
SPICE_DOCSTRINGS["eul2m"] = """
Construct a rotation matrix from a set of Euler angles.

eul2m(<float> angle3, <float> angle2, <float> angle1,
      <int> axis3, <int> axis2, <int> axis1) -> <float[3,3]> rotmat

angle3, angle2, angle1 = Rotation angles about third, second, and first
                         rotation axes (radians).
axis3, axis2, axis1    = Axis numbers of third, second, and first rotation
                         axes.
rotmat                 = Product of the 3 rotations.
"""

#########################################
SPICE_SIGNATURES["eul2xf"] = ["float[6]"] + 3*["int"]
SPICE_RETURNS   ["eul2xf"] = ["float[6,6]"]
SPICE_DOCSTRINGS["eul2xf"] = """
This routine computes a state transformation from an Euler angle
factorization of a rotation and the derivatives of those Euler angles.

eul2xf(<float[6]> eulang, <int> axisa,
                          <int> axisb, <int> axisc) ->  <float[6,6]> xform

eulang = An array of Euler angles and their derivatives.
axisa  = Axis A of the Euler angle factorization.
axisb  = Axis B of the Euler angle factorization.
axisc  = Axis C of the Euler angle factorization.
xform  = A state transformation matrix.
"""

#########################################
SPICE_SIGNATURES["expool"] = ["string"]
SPICE_RETURNS   ["expool"] = ["bool"]
SPICE_DOCSTRINGS["expool"] = """
Confirm the existence of a kernel variable in the kernel pool.

expool(<string> name) -> <bool> found

name  = Name of the variable whose value is to be returned.
found = True if the variable is in the pool; False othewise.
"""

#########################################
SPICE_SIGNATURES["failed"] = []
SPICE_RETURNS   ["failed"] = ["bool"]
SPICE_DOCSTRINGS["failed"] = """
True if an error condition has been signalled via sigerr. failed is the
CSPICE status indicator.

failed() -> <bool> value

value = True if an error condition was detected; it is False otherwise.
"""

#########################################
SPICE_SIGNATURES["fovray"] = ["string", "float[3]", "frame_name", "string",
                              "body_name", "float"]
SPICE_RETURNS   ["fovray"] = ["bool"]
SPICE_DOCSTRINGS["fovray"] = """
Determine if a specified ray is within the field-of-view (FOV) of a
specified instrument at a given time.

fovray(<string> inst, <float[3]> raydir, <string> rframe,
       <string> abcorr, <string> observer, <float> et) -> <bool> visible

inst     = Name or ID code string of the instrument.
raydir   = Ray's direction vector.
rframe   = Body-fixed, body-centered frame for target body.
abcorr   = Aberration correction flag.
observer = Name or ID code string of the observer.
et       = Time of the observation (seconds past J2000).
visible  = Visibility flag (True/False).
"""

#########################################
SPICE_SIGNATURES["fovtrg"] = ["string", "body_name", "string", "frame_name",
                              "string", "body_name", "float"]
SPICE_RETURNS   ["fovtrg"] = ["bool"]
SPICE_DOCSTRINGS["fovtrg"] = """
Determine if a specified ephemeris object is within the field-of-view (FOV)
of a specified instrument at a given time.

fovtrg(<string> inst, <string> target, <string> tshape, <string> tframe,
       <string> abcorr, <string> obsrvr, <float> et) -> <bool> visible

inst    = Name or ID code string of the instrument.
target  = Name or ID code string of the target.
tshape  = Type of shape model used for the target.
tframe  = Body-fixed, body-centered frame for target body.
abcorr  = Aberration correction flag.
obsrvr  = Name or ID code string of the observer.
et      = Time of the observation (seconds past J2000).
visible = Visibility flag (True/False).
"""

#########################################
SPICE_SIGNATURES["frame"] = ["float[3]"]
SPICE_RETURNS   ["frame"] = 3*["float[3]"]
SPICE_DOCSTRINGS["frame"] = """
Given a vector x, this routine builds a right handed orthonormal frame
x,y,z where the output x is parallel to the input x.

frame(<float[3]> xin) -> [<float[3]> x, <float[3]> y, <float[3]> z]

xin = Input vector.
x   = A unit vector parallel to xin.
y   = Unit vector in the plane orthogonal to x.
z   = Unit vector given by x X y.
"""

#########################################
SPICE_SIGNATURES["frinfo"] = ["frame_code"]
SPICE_RETURNS   ["frinfo"] = 3*["int"] + ["bool"]
SPICE_DOCSTRINGS["frinfo"] = """
Retrieve the minimal attributes associated with a frame needed for
converting transformations to and from it.

frinfo(<int> frcode) -> [<int> cent, <int> frclss, <int> clssid,
                         <bool> found]

frcode = the idcode for some frame
cent   = the center of the frame
frclss = the class (type) of the frame
clssid = the idcode for the frame within its class.
found  = True if the requested information is available.
"""

SPICE_SIGNATURES["frinfo_error"] = ["frame_code"]
SPICE_RETURNS   ["frinfo_error"] = 3*["int"]
SPICE_DOCSTRINGS["frinfo_error"] = """
Retrieve the minimal attributes associated with a frame needed for
converting transformations to and from it.

frinfo(<int> frcode) -> [<int> cent, <int> frclss, <int> clssid]

frcode = the idcode for some frame
cent   = the center of the frame
frclss = the class (type) of the frame
clssid = the idcode for the frame within its class.

Raise KeyError if the requested information is unavailable.
"""

#########################################
SPICE_SIGNATURES["frmchg"] = ["frame_code", "frame_code", "float"]
SPICE_RETURNS   ["frmchg"] = ["float[6,6]"]
SPICE_DOCSTRINGS["frmchg"] = """
Return the state transformation matrix from one frame to another.

int frmchg(<int> frame1, <int> frame2, <float> et) -> <float[6,6]> xform

frame1 = the frame id-code for some reference frame
frame2 = the frame id-code for some reference frame
et     = an epoch in TDB seconds past J2000.
xform  = a state transformation matrix
"""

#########################################
SPICE_SIGNATURES["frmnam"] = ["frame_code"]
SPICE_RETURNS   ["frmnam"] = ["frame_name"]
SPICE_DOCSTRINGS["frmnam"] = """
Retrieve the name of a reference frame associated with a SPICE ID code.

frmnam(<int> frcode) -> <string> frname

frcode = an integer code for a reference frame
frname = the name associated with the reference frame; blank on error.
"""

SPICE_SIGNATURES["frmnam_error"] = ["frame_code"]
SPICE_RETURNS   ["frmnam_error"] = ["frame_name"]
SPICE_DOCSTRINGS["frmnam_error"] = """
Retrieve the name of a reference frame associated with a SPICE ID code.

frmnam(<int> frcode) -> <string> frname

frcode = an integer code for a reference frame
frname = the name associated with the reference frame.

Raise KeyError if not found
"""

#########################################
SPICE_SIGNATURES["furnsh"] = ["string"]
SPICE_RETURNS   ["furnsh"] = []
SPICE_DOCSTRINGS["furnsh"] = """
Load one or more SPICE kernels into a program.

furnsh(<string> file)

file = Name of SPICE kernel file.
"""

#########################################
SPICE_SIGNATURES["gcpool"] = ["string", "int"]
SPICE_DEFAULTS  ["gcpool"] = [1]
SPICE_RETURNS   ["gcpool"] = ["string[*]", "bool"]
SPICE_DOCSTRINGS["gcpool"] = """
Return the character value of a kernel variable from the kernel pool.

gcpool(<string> name, <int> start=1) -> [<string[*]> cvals, <bool> found]

name  = Name of the variable whose value is to be returned.
start = Which component to start retrieving for name; default 1.
cvals = Values associated with name.
found = True if variable is in pool.
"""

SPICE_SIGNATURES["gcpool_error"] = ["string", "int"]
SPICE_RETURNS   ["gcpool_error"] = ["string[*]"]
SPICE_DOCSTRINGS["gcpool_error"] = """
Return the character value of a kernel variable from the kernel pool.

gcpool(<string> name, <int> start=1) -> <string[*]> cvals

name  = Name of the variable whose value is to be returned.
start = Which component to start retrieving for name; default 1.
cvals = Values associated with name.

Raise KeyError if the variable is not in the pool.
"""

#########################################
SPICE_SIGNATURES["gdpool"] = ["string", "int"]
SPICE_DEFAULTS  ["gdpool"] = [1]
SPICE_RETURNS   ["gdpool"] = ["float[*]", "bool"]
SPICE_DOCSTRINGS["gdpool"] = """
Return the float value of a kernel variable from the kernel pool.

gdpool(<string> name, <int> start=1) -> [<float[*]> values, <bool> found]

name   = Name of the variable whose value is to be returned.
start  = Which component to start retrieving for name; default 1.
values = Values associated with name.
found  = True if variable is in pool.
"""

SPICE_SIGNATURES["gdpool_error"] = ["string", "int"]
SPICE_DEFAULTS  ["gdpool_error"] = [1]
SPICE_RETURNS   ["gdpool_error"] = ["float[*]"]
SPICE_DOCSTRINGS["gdpool_error"] = """
Return the float value of a kernel variable from the kernel pool.

gdpool(<string> name, <int> start=1) -> <float[*]> values

name   = Name of the variable whose value is to be returned.
start  = Which component to start retrieving for name; default 1.
values = Values associated with name.

Raise KeyError if the variable is not in the pool.
"""

#########################################
SPICE_SIGNATURES["georec"] = 5*["float"]
SPICE_RETURNS   ["georec"] = ["float[3]"]
SPICE_DOCSTRINGS["georec"] = """
Convert geodetic coordinates to rectangular coordinates.

georec(<float> lon, <float> lat, <float> alt,
                    <float> re, <float> f) -> <float[3]> rectan

lon    = Geodetic longitude of point (radians).
lat    = Geodetic latitude  of point (radians).
alt    = Altitude of point above the reference spheroid.
re     = Equatorial radius of the reference spheroid.
f      = Flattening coefficient.
rectan = Rectangular coordinates of point.
"""

#########################################
SPICE_SIGNATURES["getfov"] = ["int"]
SPICE_RETURNS   ["getfov"] = ["string", "string", "float[3]", "float[*,3]"]
SPICE_DOCSTRINGS["getfov"] = """
This subroutine returns the field-of-view (FOV) configuration for a
specified instrument.

getfov(<int> instid) -> [<string> shape, <string> frame,
                         <float[3]> bsight, <float[*,3]> bounds]

instid = NAIF ID of an instrument.
shape  = Instrument FOV shape.
frame  = Name of the frame in which FOV vectors are defined.
bsight = Boresight vector.
bounds = FOV boundary vectors.
"""

#########################################
SPICE_SIGNATURES["getmsg"] = ["string"]
SPICE_RETURNS   ["getmsg"] = ["string"]
SPICE_DOCSTRINGS["getmsg"] = """
Retrieve the current short error message, the explanation of the short
error message, or the long error message.

getmsg(<string> option) -> <string> msg

option = Indicates type of error message.
msg    = The error message to be retrieved.
"""

#########################################
SPICE_SIGNATURES["gipool"] = ["string", "int"]
SPICE_DEFAULTS  ["gipool"] = [1]
SPICE_RETURNS   ["gipool"] = ["int[*]", "bool"]
SPICE_DOCSTRINGS["gipool"] = """
Return the integer value of a kernel variable from the kernel pool.

gipool(<string> name, <int> start=1) -> [<int[*]> ivals, <bool> found]

name  = Name of the variable whose value is to be returned.
start = Which component to start retrieving for name; default is 1.
ivals = Values associated with name.
found  = True if variable is in pool.
"""

SPICE_SIGNATURES["gipool_error"] = ["string", "int"]
SPICE_DEFAULTS  ["gipool_error"] = [1]
SPICE_RETURNS   ["gipool_error"] = ["int[*]"]
SPICE_DOCSTRINGS["gipool_error"] = """
Return the integer value of a kernel variable from the kernel pool.

gipool(<string> name, <int> start=1) -> <int[*]> ivals

name  = Name of the variable whose value is to be returned.
start = Which component to start retrieving for name; default is 1.
ivals = Values associated with name.

Raise KeyError if the variable is not in the pool.
"""

#########################################
SPICE_SIGNATURES["gnpool"] = ["string", "int"]
SPICE_DEFAULTS  ["gnpool"] = [1]
SPICE_RETURNS   ["gnpool"] = ["string[*]", "bool"]
SPICE_DOCSTRINGS["gnpool"] = """
Return names of kernel variables matching a specified template.

gnpool(<string> name, <int> start=1) -> [<string[*]> kvars, <bool> found]

name   = Template that names should match.
start  = Index of first matching name to retrieve.
lenout = Length of strings in output array kvars.
kvars  = Kernel pool variables whose names match name.

Raise KeyError if not found.
"""

SPICE_SIGNATURES["gnpool_error"] = ["string", "int"]
SPICE_DEFAULTS  ["gnpool_error"] = [1]
SPICE_RETURNS   ["gnpool_error"] = ["string[*]"]
SPICE_DOCSTRINGS["gnpool_error"] = """
Return names of kernel variables matching a specified template.

gnpool(<string> name, <int> start=1) -> <string[*]> kvars

name   = Template that names should match.
start  = Index of first matching name to retrieve.
lenout = Length of strings in output array kvars.
kvars  = Kernel pool variables whose names match name.

Raise KeyError if the variable is not in the pool.
"""

#########################################
SPICE_SIGNATURES["halfpi"] = []
SPICE_RETURNS   ["halfpi"] = ["float"]
SPICE_DOCSTRINGS["halfpi"] = """
Return half the value of pi

halfpi() -> <float> value
"""

#########################################
SPICE_SIGNATURES["ident"] = []
SPICE_RETURNS   ["ident"] = ["float[3,3]"]
SPICE_DOCSTRINGS["ident"] = """
Return the 3x3 identity matrix.

ident() -> <float[3,3]> matrix

matrix = is the 3x3 identity matrix.
"""

#########################################
SPICE_SIGNATURES["illum"] = ["body_name", "float", "string", "body_name",
                             "float[3]"]
SPICE_RETURNS   ["illum"] = 3*["float"]
SPICE_DOCSTRINGS["illum"] = """
Find the illumination angles at a specified surface point of a target body.

illum(<string> target, <float> et, <string> abcorr, <string> obsrvr,
      <float[3]> spoint) -> [<float> phase, <float> solar, <float> emissn]

target = Name of target body.
et     = Epoch in ephemeris seconds past J2000.
abcorr = Desired aberration correction.
obsrvr = Name of observing body.
spoint = Body-fixed coordinates of a target surface point.
phase  = Phase angle at the surface point.
solar  = Solar incidence angle at the surface point.
emissn = Emission angle at the surface point.
"""

#########################################
SPICE_SIGNATURES["illumf"] = ["string", "body_name", "body_name", "float",
                              "frame_name", "string", "body_name", "float[3]"]
SPICE_RETURNS   ["illumf"] = ["float", "float[3]", "float", "float", "float",
                              "bool", "bool"]
SPICE_DOCSTRINGS["illumf"] = """
Compute the illumination angles---phase, incidence, and emission---at a
specified point on a target body. Return logical flags indicating whether
the surface point is visible from the observer's position and whether the
surface point is illuminated.

The target body's surface is represented using topographic data provided by
DSK files or by a reference ellipsoid.

The illumination source is a specified ephemeris object.

illumf(<string> method, <string> target, <string> ilusrc,
       <float> et, <string> fixref, <string> abcorr, <string> obsrvr,
       <float[3]> spoint) ->
                [<float> trgepc, <float[3]> srfvec, <float> phase,
                 <float> incdnc, <float> emissn, <bool> visibl, <bool> lit]

method = Computation method.
target = Name of target body.
ilusrc = Name of illumination source.
et     = Epoch in TDB seconds past J2000 TDB.
fixref = Body-fixed, body-centered target body frame.
abcorr = Aberration correction flag.
obsrvr = Name of observing body.
spoint = Body-fixed coordinates of a target surface point.
trgepc = Target surface point epoch.
srfvec = Vector from observer to target surface point.
phase  = Phase angle at the surface point.
incdnc = Source incidence angle at the surface point.
emissn = Emission angle at the surface point.
visibl = Visibility flag: True for visible)
lit    = Illumination flag: True for illuminated.
"""

#########################################
SPICE_SIGNATURES["illumg"] = ["string", "body_name", "body_name", "float",
                              "frame_name", "string", "body_name", "float[3]"]
SPICE_RETURNS   ["illumg"] = ["float", "float[3]", "float", "float", "float"]
SPICE_DOCSTRINGS["illumg"] = """
Find the illumination angles (phase, incidence, and emission) at a specified
surface point of a target body.

The surface of the target body may be represented by a triaxial ellipsoid
or by topographic data provided by DSK files.

The illumination source is a specified ephemeris object.

illumg(<string> method, <string> target, <string> ilusrc,
       <float> et, <string> fixref, <string> abcorr, <string> obsrvr,
       <float[3]> spoint) ->
                        [trgepc, <float[3]> srfvec,
                         <float> phase, <float> incdnc, <float> emissn]

method = Computation method.
target = Name of target body.
ilusrc = Name of illumination source.
et     = Epoch in TDB seconds past J2000 TDB.
fixref = Body-fixed, body-centered target body frame.
abcorr = Aberration correction flag.
obsrvr = Name of observing body.
spoint = Body-fixed coordinates of a target surface point.
trgepc = Target surface point epoch.
srfvec = Vector from observer to target surface point.
phase  = Phase angle at the surface point.
incdnc = Source incidence angle at the surface point.
emissn = Emission angle at the surface point.
"""

#########################################
SPICE_SIGNATURES["ilumin"] = ["string", "body_name", "float", "frame_name",
                              "string", "body_name", "float[3]"]
SPICE_RETURNS   ["ilumin"] = ["float", "float[3]", "float", "float", "float"]
SPICE_DOCSTRINGS["ilumin"] = """
Find the illumination angles (phase, solar incidence, and emission) at a
specified surface point of a target body.

This routine supersedes illum.

ilumin(<string> method, <string> target, <float> et,
       <string> fixref, <string> abcorr, <string> obsrvr,
       <float[3]> spoint] ->
                        [trgepc, <float[3]> srfvec, <float> phase,
                         <float> incdnc, <float> emissn]

method = Computation method.
target = Name of target body.
et     = Epoch in TDB seconds past J2000 TDB.
fixref = Body-fixed, body-centered target body frame.
abcorr = Aberration correction flag.
obsrvr = Name of observing body.
spoint = Body-fixed coordinates of a target surface point.
trgepc = Target surface point epoch.
srfvec = Vector from observer to target surface point.
phase  = Phase angle at the surface point.
incdnc = Solar incidence angle at the surface point.
emissn = Emission angle at the surface point.
"""

#########################################
SPICE_SIGNATURES["inedpl"] = 3*["float"] + ["float[4]"]
SPICE_RETURNS   ["inedpl"] = ["float[9]", "bool"]
SPICE_DOCSTRINGS["inedpl"] = """
Find the intersection of a triaxial ellipsoid and a plane.

inedpl(<float> a, <float> b, <float> c, <float[4]> plane) ->
                                    [<float[9]> ellipse, <bool> found]

a       = Length of ellipsoid semi-axis lying on the x-axis.
b       = Length of ellipsoid semi-axis lying on the y-axis.
c       = Length of ellipsoid semi-axis lying on the z-axis.
plane   = Plane that intersects ellipsoid.
ellipse = Intersection ellipse, when found is True.
found   = Flag indicating whether ellipse was found.
"""

#########################################
SPICE_SIGNATURES["inelpl"] = 3*["float"] + ["float[4]"]
SPICE_RETURNS   ["inelpl"] = ["int", "float[3]", "float[3]"]
SPICE_DOCSTRINGS["inelpl"] = """
Find the intersection of an ellipse and a plane.

inelpl(<float[9]> ellips, <float[4]> plane) ->
                        [<int> nxpts, <float[3]> xpt1, <float[3]> xpt2]

ellips     = A CSPICE ellipse.
plane      = A CSPICE plane.
nxpts      = Number of intersection points of plane and ellipse.
xpt1, xpt2 = Intersection points.
"""

#########################################
SPICE_SIGNATURES["inrypl"] = ["float[3]", "float[3]", "float[4]"]
SPICE_RETURNS   ["inrypl"] = ["int", "float[3]"]
SPICE_DOCSTRINGS["inrypl"] = """
Find the intersection of a ray and a plane.

inrypl(<float[3]> vertex, <float[3]> dir, <float[4]> plane) ->
                        [<int> nxpts, <float[3]> xpt]

vertex, dir = Vertex and direction vector of ray.
plane       = A CSPICE plane.
nxpts       = Number of intersection points of ray and plane.
xpt         = Intersection point, if nxpts = 1.
"""

#########################################
SPICE_SIGNATURES["intmax"] = []
SPICE_RETURNS   ["intmax"] = ["int"]
SPICE_DOCSTRINGS["intmax"] = """
Return the value of the largest (positive) number representable in a
variable.

intmax() -> <int> value

value = the largest (positive) number that can be represented in a variable.
"""

#########################################
SPICE_SIGNATURES["intmin"] = []
SPICE_RETURNS   ["intmin"] = ["int"]
SPICE_DOCSTRINGS["intmin"] = """
Return the value of the smallest (negative) number representable in a
SpiceInt variable.

intmin() -> <int> value

value = the smallest (negative) number that can be represented in a
        variable.
"""

#########################################
SPICE_SIGNATURES["invert"] = ["float[3,3]"]
SPICE_RETURNS   ["invert"] = ["float[3,3]"]
SPICE_DOCSTRINGS["invert"] = """
Generate the inverse of a 3x3 matrix.

invert(<float[3,3]> m1) -> <float[3,3]> mout

m1   = Matrix to be inverted.
mout = Inverted matrix (m1**-1).

If m1 is singular, then a RuntimeError is raised.
"""

#########################################
SPICE_SIGNATURES["invort"] = ["float[3,3]"]
SPICE_RETURNS   ["invort"] = ["float[3,3]"]
SPICE_DOCSTRINGS["invort"] = """
Given a matrix, construct the matrix whose rows are the columns of the
first divided by the length squared of the the corresponding columns of the
input matrix.

invort(<float[3,3]> m) -> <float[3,3]> mit

m   = A 3x3 matrix.
mit = m after transposition and scaling of rows.
"""

#########################################
SPICE_SIGNATURES["isrot"] = ["float[3,3]", "float", "float"]
SPICE_RETURNS   ["isrot"] = ["bool"]
SPICE_DOCSTRINGS["isrot"] = """
Indicate whether a 3x3 matrix is a rotation matrix.

isrot(<float[3,3]> m, <float> ntol, <float> dtol) -> status

m      = A matrix to be tested.
ntol   = Tolerance for the norms of the columns of m.
dtol   = Tolerance for the determinant of a matrix whose columns are the
         unitized columns of m.
status = True if and only if m is a rotation matrix.
"""

#########################################
SPICE_SIGNATURES["j1900"] = []
SPICE_RETURNS   ["j1900"] = ["float"]
SPICE_DOCSTRINGS["j1900"] = """
Return the Julian Date of 1899 DEC 31 12:00:00 (1900 JAN 0.5).

j1900() -> <float> value
"""

#########################################
SPICE_SIGNATURES["j1950"] = []
SPICE_RETURNS   ["j1950"] = ["float"]
SPICE_DOCSTRINGS["j1950"] = """
Return the Julian Date of 1950 JAN 01 00:00:00 (1950 JAN 1.0).

j1950() -> <float> value
"""

#########################################
SPICE_SIGNATURES["j2000"] = []
SPICE_RETURNS   ["j2000"] = ["float"]
SPICE_DOCSTRINGS["j2000"] = """
Return the Julian Date of 2000 JAN 01 12:00:00 (2000 JAN 1.5).

j2000() -> <float> value
"""

#########################################
SPICE_SIGNATURES["j2100"] = []
SPICE_RETURNS   ["j2100"] = ["float"]
SPICE_DOCSTRINGS["j2100"] = """
Return the Julian Date of 2100 JAN 01 12:00:00 (2100 JAN 1.5).

j2100() -> <float> value
"""

#########################################
SPICE_SIGNATURES["jyear"] = []
SPICE_RETURNS   ["jyear"] = ["float"]
SPICE_DOCSTRINGS["jyear"] = """
Return the number of seconds in a julian year.

jyear() -> <float> value
"""

#########################################
SPICE_SIGNATURES["latcyl"] = 3*["float"]
SPICE_RETURNS   ["latcyl"] = 3*["float"]
SPICE_DOCSTRINGS["latcyl"] = """
Convert from latitudinal coordinates to cylindrical coordinates.

latcyl(<float> radius, <float> lon, <float> lat) ->
                            [<float> r, <float> lonc, <float> z]

radius = Distance of a point from the origin.
lon    = Angle of the point from the XZ plane in radians.
lat    = Angle of the point from the XY plane in radians.
r      = Distance of the point from the z axis.
lonc   = Angle of the point from the XZ plane in radians.
z      = Height of the point above the XY plane.
"""

#########################################
SPICE_SIGNATURES["latrec"] = 3*["float"]
SPICE_RETURNS   ["latrec"] = 3*["float[3]"]
SPICE_DOCSTRINGS["latrec"] = """
Convert from latitudinal coordinates to rectangular coordinates.

latrec(<float> radius, <float> longitude,
                       <float> latitude) -> <float[3]> rectan

radius    = Distance of a point from the origin.
longitude = Longitude of point in radians.
latitude  = Latitude of point in radians.
rectan    = Rectangular coordinates of the point.
"""

#########################################
SPICE_SIGNATURES["latsrf"] = ["string", "body_name", "float", "frame_name",
                              "float[*,2]"]
SPICE_RETURNS   ["latsrf"] = ["float[*,3]"]
SPICE_DOCSTRINGS["latsrf"] = """
Map array of planetocentric longitude/latitude coordinate pairs to surface
points on a specified target body.

The surface of the target body may be represented by a triaxial ellipsoid
or by topographic data provided by DSK files.

latsrf(<string> method, <string> target, <float> et, <string> fixref,
       <float[n,2]> lonlat) -> <float[n,3]> srfpts

method = Computation method.
target = Name of target body.
et     = Epoch in TDB seconds past J2000 TDB.
fixref = Body-fixed, body-centered target body frame.
lonlat = Array of longitude/latitude coordinate pairs.
srfpts = Array of surface points.
"""

#########################################
SPICE_SIGNATURES["latsph"] = 3*["float"]
SPICE_RETURNS   ["latsph"] = 3*["float"]
SPICE_DOCSTRINGS["latsph"] = """
Convert from latitudinal coordinates to spherical coordinates.

latsph(<float> radius, <float> lon, <float> lat) ->
                            [<float> rho, <float> colat, <float> lons]

radius = Distance of a point from the origin.
lon    = Angle of the point from the XZ plane in radians.
lat    = Angle of the point from the XY plane in radians.
rho    = Distance of the point from the origin.
colat  = Angle of the point from positive z axis (radians).
lons   = Angle of the point from the XZ plane (radians).
"""

#########################################
SPICE_SIGNATURES["ldpool"] = ["string"]
SPICE_RETURNS   ["ldpool"] = []
SPICE_DOCSTRINGS["ldpool"] = """
Load the variables contained in a NAIF ASCII kernel file into the kernel
pool.

ldpool(<string> filename)

filename = Name of the kernel file.
"""

#########################################
SPICE_SIGNATURES["limbpt"] = ["string", "body_name", "float", "frame_name",
                              "string", "string", "body_name", "float[3]",
                              "float", "int", "float", "float", "int"]
SPICE_RETURNS   ["limbpt"] = ["int[*]", "float[*,3]", "float[*]", "float[*,3]"]
SPICE_DOCSTRINGS["limbpt"] = """
Find limb points on a target body. The limb is the set of points of
tangency on the target of rays emanating from the observer. The caller
specifies half-planes bounded by the observer-target center vector in which
to search for limb points.

The surface of the target body may be represented either by a triaxial
ellipsoid or by topographic data.

limbpt(<string> method, <string> target, <float> et,
       <string> fixref, <string> abcorr, corloc, <string> obsrvr,
       <float[3]> refvec, <float> rolstp, ncuts, schstp, <float> soltol,
       <int> maxn) ->
                    [<int[*]> npts, <float[*,3]> points, <float[*]> epochs,
                     <float[*,3]> tangts]

method = Computation method.
target = Name of target body.
et     = Epoch in ephemeris seconds past J2000 TDB.
fixref = Body-fixed, body-centered target body frame.
abcorr = Aberration correction.
corloc = Aberration correction locus.
obsrvr = Name of observing body.
refvec = Reference vector for cutting half-planes.
rolstp = Roll angular step for cutting half-planes.
ncuts  = Number of cutting half-planes.
schstp = Angular step size for searching.
soltol = Solution convergence tolerance.
maxn   = Maximum number of entries in output arrays.
npts   = Counts of limb points corresponding to cuts.
points = Limb points.
epochs = Times associated with limb points.
tangts = Tangent vectors emanating from the observer.
"""

#########################################
SPICE_SIGNATURES["lspcn"] = ["body_name", "float", "string"]
SPICE_RETURNS   ["lspcn"] = ["float"]
SPICE_DOCSTRINGS["lspcn"] = """
Compute L_s, the planetocentric longitude of the sun, as seen from a
specified body.

lspcn(<string> body, <float> et, <string> abcorr) -> <float> value

body   = Name of central body.
et     = Epoch in seconds past J2000 TDB.
abcorr = Aberration correction.
value  = L_s for the specified body at the specified time.
"""

#########################################
SPICE_SIGNATURES["ltime"] = ["float", "body_code", "string", "body_code"]
SPICE_RETURNS   ["ltime"] = ["float", "float"]
SPICE_DOCSTRINGS["ltime"] = """
Light Time

ltime(<float> etobs, <int> obs, <string> dir, <int> targ) ->
                                    [<float> ettarg, <float> elapsd]

etobs  = Epoch of a signal at some observer
obs    = NAIF ID of some observer
dir    = Direction the signal travels ("->" or "<-")
targ   = NAIF ID of the target object
ettarg = Epoch of the signal at the target
elapsd = Time between transmit and receipt of the signal
"""

#########################################
SPICE_SIGNATURES["m2eul"] = ["float[3,3]"] + 3*["int"]
SPICE_RETURNS   ["m2eul"] = 3*["float"]
SPICE_DOCSTRINGS["m2eul"] = """
Factor a rotation matrix as a product of three rotations about
specified coordinate axes.

m2eul(<float[3,3]> r, <int> axis3, <int> axis2, <int> axis1) ->
                        [<float> angle3, <float> angle2, <float> angle1]

r                      = A rotation matrix to be factored.
axis3, axis2, axis1    = Numbers of third, second, and first rotation axes.
angle3, angle2, angle1 = Third, second, and first Euler angles, in radians.
"""

#########################################
SPICE_SIGNATURES["m2q"] = ["float[3,3]"]
SPICE_RETURNS   ["m2q"] = ["float[4]"]
SPICE_DOCSTRINGS["m2q"] = """
Find a unit quaternion corresponding to a specified rotation matrix.

m2q(<float[3,3]> r) -> <float[4]> q

r = A rotation matrix.
q = A unit quaternion representing r.
"""

#########################################
SPICE_SIGNATURES["mequ"] = ["float[3,3]"]
SPICE_RETURNS   ["mequ"] = ["float[3,3]"]
SPICE_DOCSTRINGS["mequ"] = """
Set one double precision 3x3 matrix equal to another.

mequ(<float[3,3]> m1) -> <float[3,3]> mout

m1   = Input matrix.
mout = Output matrix equal to m1.
"""

#########################################
SPICE_SIGNATURES["mequg"] = ["float[*,*]"]
SPICE_RETURNS   ["mequg"] = ["float[*,*]"]
SPICE_DOCSTRINGS["mequg"] = """
Set one double precision matrix of arbitrary size equal to another.

mequg(<float[*,*]> m1) -> <float[*,*]> mout

m1   = Input matrix.
mout = Output matrix equal to m1.
"""

#########################################
SPICE_SIGNATURES["mtxm"] = 2*["float[3,3]"]
SPICE_RETURNS   ["mtxm"] = ["float[3,3]"]
SPICE_DOCSTRINGS["mtxm"] = """
Multiply the transpose of a 3x3 matrix and a 3x3 matrix.

mtxm(<float[3,3]> m1, <float[3,3]> m2) -> <float[3,3]> mout

m1   = 3x3 double precision matrix.
m2   = 3x3 double precision matrix.
mout = The produce m1 transpose times m2.
"""

#########################################
SPICE_SIGNATURES["mtxmg"] = 2*["float[*,*]"]
SPICE_RETURNS   ["mtxmg"] = ["float[*,*]"]
SPICE_DOCSTRINGS["mtxmg"] = """
Multiply the transpose of a matrix with another matrix, both of arbitrary
size. (The dimensions of the matrices must be compatible with this
multiplication.)

mtxmg(<float[*,*]> m1, <float[*,*]>m2) -> <float[*,*]>mout

m1   = nr1r2 X ncol1 double precision matrix.
m2   = nr1r2 X ncol2 double precision matrix.
mout = Transpose of m1 times m2.
"""

#########################################
SPICE_SIGNATURES["mtxv"] = ["float[3,3]", "float[3]"]
SPICE_RETURNS   ["mtxv"] = ["float[3]"]
SPICE_DOCSTRINGS["mtxv"] = """
Multiply the transpose of a 3x3 matrix on the left with a vector on the
right.

mtxv(<float[3,3]> m1, <float[3]> vin) -> <float[3]> vout

m1   = 3x3 double precision matrix.
vin  = 3-dimensional double precision vector.
vout = the product m1**t * vin.
"""

#########################################
SPICE_SIGNATURES["mtxvg"] = ["float[*,*]", "float[*]"]
SPICE_RETURNS   ["mtxvg"] = ["float[*]"]
SPICE_DOCSTRINGS["mtxvg"] = """
Multiply the transpose of a matrix and a vector of arbitrary size.

mtxvg(<float[*,*]> m1, <float[*]>v2) -> <float[*]> vout

m1   = Left-hand matrix to be multiplied.
v2   = Right-hand vector to be multiplied.
vout = Product vector m1 transpose * v2.
"""

#########################################
SPICE_SIGNATURES["mxm"] = ["float[3,3]", "float[3,3]"]
SPICE_RETURNS   ["mxm"] = ["float[3,3]"]
SPICE_DOCSTRINGS["mxm"] = """
Multiply two 3x3 matrices.

mxm(<float[3,3]> m1, <float[3,3]> m2) -> <float[3,3]> mout

m1   = 3x3 double precision matrix.
m2   = 3x3 double precision matrix.
mout = the product m1*m2.
"""

#########################################
SPICE_SIGNATURES["mxmg"] = ["float[*,*]", "float[*,*]"]
SPICE_RETURNS   ["mxmg"] = ["float[*,*]"]
SPICE_DOCSTRINGS["mxmg"] = """
Multiply two double precision matrices of arbitrary size.

mxmg(<float[*,*]> m1, <float[*,*]> m2) -> <float[*,*]> mout

m1    = nrow1 X ncol1 double precision matrix.
m2    = ncol1 X ncol2 double precision matrix.
mout  = nrow1 X ncol2 double precision matrix.
"""

#########################################
SPICE_SIGNATURES["mxmt"] = ["float[3,3]", "float[3,3]"]
SPICE_RETURNS   ["mxmt"] = ["float[3,3]"]
SPICE_DOCSTRINGS["mxmt"] = """
Multiply a 3x3 matrix and the transpose of another 3x3 matrix.

mxmt(<float[3,3]> m1, <float[3,3]> m2) -> <float[3,3]> mout

m1   = 3x3 double precision matrix.
m2   = 3x3 double precision matrix.
mout = The product m1 times m2 transpose .
"""

#########################################
SPICE_SIGNATURES["mxmtg"] = ["float[*,*]", "float[*]"]
SPICE_RETURNS   ["mxmtg"] = ["float[*]"]
SPICE_DOCSTRINGS["mxmtg"] = """
Multiply a matrix and the transpose of a matrix, both of arbitrary size.

mxmtg(<float[*,*]> m1, <float[*,*]> m2) -> <float[*,*]> mout

m1   = Left-hand matrix to be multiplied.
m2   = Right-hand matrix whose transpose is to be multiplied
mout = Product matrix.
"""

#########################################
SPICE_SIGNATURES["mxv"] = ["float[3,3]", "float[3]"]
SPICE_RETURNS   ["mxv"] = ["float[3]"]
SPICE_DOCSTRINGS["mxv"] = """
Multiply a 3x3 double precision matrix with a 3-dimensional double
precision vector.

mxv(<float[3,3]> m1, <float[3]> vin) -> <float[3]> vout

m1   = 3x3 double precision matrix.
vin  = 3-dimensional double precision vector.
vout = 3-dimensinoal double precision vector. vout is the product m1*vin.
"""

#########################################
SPICE_SIGNATURES["mxvg"] = ["float[*,*]", "float[*]"]
SPICE_RETURNS   ["mxvg"] = ["float[*]"]
SPICE_DOCSTRINGS["mxvg"] = """
Multiply a matrix and a vector of arbitrary size.

mxvg(<float[*,*]> m1, <float[*]> v2) -> <float[*]> vout

m1   = Left-hand matrix to be multiplied.
v2   = Right-hand vector to be multiplied.
vout = Product vector m1*v2.
"""

#########################################
SPICE_SIGNATURES["namfrm"] = ["frame_name"]
SPICE_RETURNS   ["namfrm"] = ["frame_code"]
SPICE_DOCSTRINGS["namfrm"] = """
Look up the frame ID code associated with a string.

namfrm(<string> frname) -> <int> frcode

frname = The name of some reference frame.
frcode = The SPICE ID code of the frame; 0 on error.
"""

SPICE_SIGNATURES["namfrm_error"] = ["frame_name"]
SPICE_RETURNS   ["namfrm_error"] = ["frame_code"]
SPICE_DOCSTRINGS["namfrm_error"] = """
Look up the frame ID code associated with a string.

namfrm(<string> frname) -> <int> frcode

frname = The name of some reference frame.
frcode = The SPICE ID code of the frame.

Raise KeyError if not found.
"""

#########################################
SPICE_SIGNATURES["nearpt"] = ["float[3]"] + 3*["float"]
SPICE_RETURNS   ["nearpt"] = ["float[3]", "float"]
SPICE_DOCSTRINGS["nearpt"] = """
This routine locates the point on the surface of an ellipsoid that is
nearest to a specified position. It also returns the altitude of the
position above the ellipsoid.

nearpt(<float[3]> positn, <float> a, <float> b, <float> c) ->
                                    [<float[3]> npoint, <float> alt]

positn = Position of a point in bodyfixed frame.
a      = Length of semi-axis parallel to x-axis.
b      = Length of semi-axis parallel to y-axis.
c      = Length on semi-axis parallel to z-axis.
npoint = Point on the ellipsoid closest to positn.
alt    = Altitude of positn above the ellipsoid.
"""

#########################################
SPICE_SIGNATURES["npedln"] = 3*["float"] + 2*["float[3]"]
SPICE_RETURNS   ["npedln"] = ["float[3]", "float"]
SPICE_DOCSTRINGS["npedln"] = """
Find nearest point on a triaxial ellipsoid to a specified line, and the
distance from the ellipsoid to the line.

npedln(<float> a, <float> b, <float> c,
       <float[3]> linept, <float[3]> linedr) -> [<float[3]> pnear,
                                                 <float> dist]

a      = Length of ellipsoid's semi-axis in the x direction
b      = Length of ellipsoid's semi-axis in the y direction
c      = Length of ellipsoid's semi-axis in the z direction
linept = Point on line
linedr = Direction vector of line
pnear  = Nearest point on ellipsoid to line
dist   = Distance of ellipsoid from line
"""

#########################################
SPICE_SIGNATURES["npelpt"] = ["float[3]", "float[9]"]
SPICE_RETURNS   ["npelpt"] = ["float[3]", "float"]
SPICE_DOCSTRINGS["npelpt"] = """
Find the nearest point on an ellipse to a specified point, both in
three-dimensional space, and find the distance between the ellipse and the
point.

npelpt(<float[3]> point, <float[9]> ellips) -> [<float[3]> pnear,
                                                <float> dist]

point  = Point whose distance to an ellipse is to be found.
ellips = A CSPICE ellipse.
pnear  = Nearest point on ellipse to input point.
dist   = Distance of input point to ellipse.
"""

#########################################
SPICE_SIGNATURES["nplnpt"] = 3*["float[3]"]
SPICE_RETURNS   ["nplnpt"] = ["float[3]", "float"]
SPICE_DOCSTRINGS["nplnpt"] = """
Find the nearest point on a line to a specified point, and find the
distance between the two points.

nplnpt(<float[3]> linpt, <float[3]> lindir, <float[3]> point) ->
                                        [<float[3]> pnear, <float> dist]

linpt  = Point on a line.
lindir = The line's direction vector.
point  = A second point.
pnear  = Nearest point on the line to point.
dist  = Distance between point and pnear.
"""

#########################################
SPICE_SIGNATURES["nvc2pl"] = ["float[3]", "float"]
SPICE_RETURNS   ["nvc2pl"] = ["float[4]"]
SPICE_DOCSTRINGS["nvc2pl"] = """
Make a CSPICE plane from a normal vector and a constant.

nvc2pl(<float[3]> normal, <float> constant) -> <float[4]> plane

normal   = A normal vector
constant = A constant defining a plane.
plane    = A CSPICE plane structure representing the plane.
"""

#########################################
SPICE_SIGNATURES["nvp2pl"] = 2*["float[3]"]
SPICE_RETURNS   ["nvp2pl"] = ["float[4]"]
SPICE_DOCSTRINGS["nvp2pl"] = """
Make a CSPICE plane from a normal vector and a point.

nvp2pl(<float[3]> normal, <float[3]> point) -> <float[4]> plane

normal = A normal vector
point  = A point defining a plane.
plane  = A CSPICE plane structure representing the plane.
"""

#########################################
SPICE_SIGNATURES["occult"] = 2*["body_name", "string", "frame_name"] + \
                             ["string", "body_name", "float"]
SPICE_RETURNS   ["occult"] = ["int"]
SPICE_DOCSTRINGS["occult"] = """
Determines the occultation condition (not occulted, partially, etc.) of one
target relative to another target as seen by an observer at a given time.

The surfaces of the target bodies may be represented by triaxial ellipsoids
or by topographic data provided by DSK files.

occult(<string> targ1, <string> shape1,  <string> frame1,
        <string> targ2,  <string> shape2,  <string> frame2,
        <string> abcorr, <string> obsrvr, <float> et) -> <int> ocltid

targ1  = Name or ID of first target.
shape1 = Type of shape model used for first target.
frame1 = Body-fixed, body-centered frame for first body.
targ2  = Name or ID of second target.
shape2 = Type of shape model used for second target.
frame2 = Body-fixed, body-centered frame for second body.
abcorr = Aberration correction flag.
obsrvr = Name or ID of the observer.
et     = Time of the observation (seconds past J2000).
ocltid = Occultation identification code.
"""

#########################################
SPICE_SIGNATURES["oscelt"] = ["float[6]", "float", "float"]
SPICE_RETURNS   ["oscelt"] = ["float[8]"]
SPICE_DOCSTRINGS["oscelt"] = """
Determine the set of osculating conic orbital elements that corresponds to
the state (position, velocity) of a body at some epoch.

oscelt(<float[6]> state, <float> et, <float> mu) -> <float[8]> elts

state = State of body at epoch of elements.
et    = Epoch of elements.
mu    = Gravitational parameter (GM) of primary body.
elts  = Equivalent conic elements
"""

#########################################
SPICE_SIGNATURES["oscltx"] = ["float[6]", "float", "float"]
SPICE_RETURNS   ["oscltx"] = ["float[*]"]
SPICE_DOCSTRINGS["oscltx"] = """
Determine the set of osculating conic orbital elements that corresponds to
the state (position, velocity) of a body at some epoch. In additional to the
classical elements, return the true anomaly, semi-major axis, and period,
if applicable.

oscltx(<float[6]> state, <float> et, <float> mu) -> <float[*]> elts

state = State of body at epoch of elements.
et    = Epoch of elements.
mu    = Gravitational parameter (GM) of primary body.
elts  = Extended set of classical conic elements.
"""

#########################################
SPICE_SIGNATURES["pckcov"] = ["string", "frame_code"]
SPICE_RETURNS   ["pckcov"] = ["float[*,2]"]
SPICE_DOCSTRINGS["pckcov"] = """
Find the coverage window for a specified reference frame in a specified
binary PCK file.

pckcov(<string> pck, <int> idcode) -> <float[:,2]> cover

pck    = Name of PCK file.
idcode = Class ID code of PCK reference frame.
cover  = An array of shape (n,2), where cover[:,0] are start times and
         cover[:,1] are stop times.
"""

SPICE_SIGNATURES["pckcov_error"] = ["string", "frame_code"]
SPICE_RETURNS   ["pckcov_error"] = ["float[*,2]"]
SPICE_DOCSTRINGS["pckcov_error"] = """
Find the coverage window for a specified reference frame in a specified
binary PCK file.

pckcov(<string> pck, <int> idcode) -> <float[:,2]> cover

pck    = Name of PCK file.
idcode = Class ID code of PCK reference frame.
cover  = An array of shape (n,2), where cover[:,0] are start times and
         cover[:,1] are stop times.

Raise KeyError if the idcode is not found.
"""

#########################################
SPICE_SIGNATURES["pcpool"] = ["string", "string[*]"]
SPICE_RETURNS   ["pcpool"] = []
SPICE_DOCSTRINGS["pcpool"] = """
This entry point provides toolkit programmers a method for programmatically
inserting character data into the kernel pool.

pcpool(<string> name, <string[*]> cvals)

name    = The kernel pool name to associate with cvals.
cvals   = An array of strings to insert into the kernel pool.
"""

#########################################
SPICE_SIGNATURES["pdpool"] = ["string", "float[*]"]
SPICE_RETURNS   ["pdpool"] = []
SPICE_DOCSTRINGS["pdpool"] = """
This entry point provides toolkit programmers a method for programmatically
inserting double precision data into the kernel pool.

pdpool(<string> name, <float[*]> dvals)

name  = The kernel pool name to associate with dvals.
dvals = An array of values to insert into the kernel pool.
"""

#########################################
SPICE_SIGNATURES["pgrrec"] = ["body_name"] + 5*["float"]
SPICE_RETURNS   ["pgrrec"] = ["float[3]"]
SPICE_DOCSTRINGS["pgrrec"] = """
Convert planetographic coordinates to rectangular coordinates.

pgrrec(<string> body, <float> lon, <float> lat, <float> alt,
                      <float> re, <float> f) -> <float[3]> rectan

body   = Body with which coordinate system is associated.
lon    = Planetographic longitude of a point (radians).
lat    = Planetographic latitude of a point (radians).
alt    = Altitude of a point above reference spheroid.
re     = Equatorial radius of the reference spheroid.
f      = Flattening coefficient.
rectan = Rectangular coordinates of the point.
"""

#########################################
SPICE_SIGNATURES["phaseq"] = ["float", "body_name", "body_name", "body_name",
                              "string"]
SPICE_RETURNS   ["phaseq"] = ["float"]
SPICE_DOCSTRINGS["phaseq"] = """
Compute the apparent phase angle for a target, observer, illuminator set of
ephemeris objects.

phaseq(<float> et, <string> target, <string> illmn,
       <string> obsrvr, <string> abcorr) -> <float> value

et     = Ephemeris seconds past J2000 TDB.
target = Target body name.
illmn  = Illuminating body name.
obsrvr = Observer body.
abcorr = Aberration correction flag.
value  = Value of phase angle.
"""

#########################################
SPICE_SIGNATURES["pi"] = []
SPICE_RETURNS   ["pi"] = ["float"]
SPICE_DOCSTRINGS["pi"] = """
Return the value of pi.

pi() -> <float> value
"""

#########################################
SPICE_SIGNATURES["pipool"] = ["string", "int[*]"]
SPICE_RETURNS   ["pipool"] = []
SPICE_DOCSTRINGS["pipool"] = """
This entry point provides toolkit programmers a method for programmatically
inserting integer data into the kernel pool.

pipool(<string> name, <int[*]> ivals)

name  = The kernel pool name to associate with values.
ivals = An array of integers to insert into the pool.
"""

#########################################
SPICE_SIGNATURES["pjelpl"] = ["float[9]", "float[4]"]
SPICE_RETURNS   ["pjelpl"] = ["float[9]"]
SPICE_DOCSTRINGS["pjelpl"] = """
Project an ellipse onto a plane, orthogonally.

pjelpl(<float[9]> elin, <float[4]> plane) -> <float[9]> elout

elin  = A CSPICE ellipse to be projected.
plane = A plane onto which elin is to be projected.
elout = A CSPICE ellipse resulting from the projection.
"""

#########################################
SPICE_SIGNATURES["pltar"] = ["float[*,3]", "float[*,3]"]
SPICE_RETURNS   ["pltar"] = ["float"]
SPICE_DOCSTRINGS["pltar"] = """
Compute the total area of a collection of triangular plates.

pltar(<float[:,3]> vrtces, <float[:,3]> plates) -> <float> area

vrtces = Array of vertices.
plates = Array of plates.
area   = total area of plates.
"""

#########################################
SPICE_SIGNATURES["pltexp"] = ["float[3,3]", "float"]
SPICE_RETURNS   ["pltexp"] = ["float[3,3]"]
SPICE_DOCSTRINGS["pltexp"] = """
Expand a triangular plate by a specified amount. The expanded plate is
co-planar with, and has the same orientation as, the original. The
centroids of the two plates coincide.

pltexp(<float[3,3]> iverts, <float> delta) -> <float[3,3]> overts

iverts = Vertices of the plate to be expanded.
delta  = Fraction by which the plate is to be expanded.
overts = Vertices of the expanded plate.
"""

#########################################
SPICE_SIGNATURES["pltnp"] = 4*["float[3]"]
SPICE_RETURNS   ["pltnp"] = ["float[3]", "float"]
SPICE_DOCSTRINGS["pltnp"] = """
Find the nearest point on a triangular plate to a given point.

pltnp(<float[3]> point, <float[3]> v1, <float[3]> v2, <float[3]> v3) ->
                                        [<float[3]> pnear, <float> dist]

point      = A point in 3-dimensional space.
v1, v2, v3 = Vertices of a triangular plate.
pnear      = Nearest point on the plate to `point'.
dist       = Distance between `pnear' and `point'.
"""

#########################################
SPICE_SIGNATURES["pltvol"] = ["float[*,3]", "float[*,3]"]
SPICE_RETURNS   ["pltvol"] = ["float"]
SPICE_DOCSTRINGS["pltvol"] = """
Compute the volume of a three-dimensional region bounded by a collection
of triangular plates.

pltvol(<float[:,3]> vrtces, <float[:,3]> plates) = <float> volume

vrtces = Array of vertices.
plates = Array of plates.
volume = the volume of the spatial region bounded by the plates.
"""

#########################################
SPICE_SIGNATURES["pl2nvc"] = ["float[4]"]
SPICE_RETURNS   ["pl2nvc"] = ["float[3]", "float"]
SPICE_DOCSTRINGS["pl2nvc"] = """
Return a unit normal vector and constant that define a specified plane.

pl2nvc(<float[4]> plane) -> [<float[3]> normal, <float> constant]

plane            = A CSPICE plane.
normal, constant = A normal vector and constant defining the geometric
                   plane.
"""

#########################################
SPICE_SIGNATURES["pl2nvp"] = ["float[4]"]
SPICE_RETURNS   ["pl2nvp"] = 2*["float[3]"]
SPICE_DOCSTRINGS["pl2nvp"] = """
Return a unit normal vector and point that define a specified plane.

pl2nvp(<float[4]> plane) -> [<float[3]> normal, <float[3]> point]

plane         = A CSPICE plane.
normal, point = A unit normal vector and point that define plane.
"""

#########################################
SPICE_SIGNATURES["pl2psv"] = ["float[4]"]
SPICE_RETURNS   ["pl2psv"] = 3*["float[3]"]
SPICE_DOCSTRINGS["pl2psv"] = """
Return a point and two orthogonal spanning vectors that generate a
specified plane.

pl2psv(<float[4]> plane) -> [<float[3]> point, <float[3]> span1,
                                               <float[3]> span2]

plane               = A CSPICE plane.
point, span1, span2 = A point in the input plane and two vectors spanning
                      the input plane.
"""

#########################################
SPICE_SIGNATURES["prop2b"] = ["float", "float[6]", "float"]
SPICE_RETURNS   ["prop2b"] = ["float[6]"]
SPICE_DOCSTRINGS["prop2b"] = """
Given a central mass and the state of massless body at time t_0, this
routine determines the state as predicted by a two-body force model at time
t_0 + dt.

prop2b(<float> gm, <float[6]> pvinit, <float> dt) -> <float[6]> pvprop

gm     = Gravity of the central mass.
pvinit = Initial state from which to propagate a state.
dt     = Time offset from initial state to propagate to.
pvprop = The propagated state.
"""

#########################################
SPICE_SIGNATURES["psv2pl"] = 3*["float[3]"]
SPICE_RETURNS   ["psv2pl"] = ["float[4]"]
SPICE_DOCSTRINGS["psv2pl"] = """
Make a CSPICE plane from a point and two spanning vectors.

psv2pl(<float[3]> point, <float[3]> span1,
                         <float[3]> span2) -> <float[4]> plane

point, span1, span2 = A point and two spanning vectors defining a plane.
plane               = A CSPICE plane representing the plane.
"""

#########################################
SPICE_SIGNATURES["pxform"] = ["frame_name", "frame_name", "float"]
SPICE_RETURNS   ["pxform"] = ["float[3,3]"]
SPICE_DOCSTRINGS["pxform"] = """
Return the matrix that transforms position vectors from one specified frame
to another at a specified epoch.

pxform(<string> from, <string> to, <float> et) -> <float[3,3]> rotate

from   = Name of the frame to transform from.
to     = Name of the frame to transform to.
et     = Epoch of the rotation matrix.
rotate = A rotation matrix.
"""

#########################################
SPICE_SIGNATURES["pxfrm2"] = ["frame_name", "frame_name", "float", "float"]
SPICE_RETURNS   ["pxfrm2"] = ["float[3,3]"]
SPICE_DOCSTRINGS["pxfrm2"] = """
Return the 3x3 matrix that transforms position vectors from one specified
frame at a specified epoch to another specified frame at another specified
epoch.

pxfrm2(<string> from, <string> to, <float> etfrom,
                                   <float> etto) -> <float[3,3]> rotate

from   = Name of the frame to transform from.
to     = Name of the frame to transform to.
etfrom = Evaluation time of `from' frame.
etto   = Evaluation time of `to' frame.
rotate = A position transformation matrix from frame `from' to frame `to'.
"""

#########################################
SPICE_SIGNATURES["q2m"] = ["float[4]"]
SPICE_RETURNS   ["q2m"] = ["float[3,3]"]
SPICE_DOCSTRINGS["q2m"] = """
Find the rotation matrix corresponding to a specified unit quaternion.

q2m(<float[4]> q) -> <float[3,3]> r

q = A unit quaternion.
r = A rotation matrix corresponding to q.
"""

#########################################
SPICE_SIGNATURES["qdq2av"] = ["float[4]", "float[4]"]
SPICE_RETURNS   ["qdq2av"] = ["float[3]"]
SPICE_DOCSTRINGS["qdq2av"] = """
Derive angular velocity from a unit quaternion and its derivative with
respect to time.

qdq2av(<float[4]> q, <float[4]> dq) -> <float[3]> av

q  = Unit SPICE quaternion.
dq = Derivative of `q' with respect to time.
av = Angular velocity defined by `q' and `dq'.
"""

#########################################
SPICE_SIGNATURES["qxq"] = ["float[4]", "float[4]"]
SPICE_RETURNS   ["qxq"] = ["float[4]"]
SPICE_DOCSTRINGS["qxq"] = """
Multiply two quaternions.

qxq(<float[4]> q1, <float[4]> q2) -> <float[4]> qout

q1   = First SPICE quaternion factor.
q2   = Second SPICE quaternion factor.
qout = Product of `q1' and `q2'.
"""

#########################################
SPICE_SIGNATURES["radrec"] = 3*["float"]
SPICE_RETURNS   ["radrec"] = ["float[3]"]
SPICE_DOCSTRINGS["radrec"] = """
Convert from range, right ascension, and declination to rectangular
coordinates.

radrec(<float> range, <float> ra, <float> dec) -> <float[3]> rectan


range  = Distance of a point from the origin.
ra     = Right ascension of point in radians.
dec    = Declination of point in radians.
rectan = Rectangular coordinates of the point.
"""

#########################################
SPICE_SIGNATURES["rav2xf"] = ["float[3,3]", "float[3]"]
SPICE_RETURNS   ["rav2xf"] = ["float[6,6]"]
SPICE_DOCSTRINGS["rav2xf"] = """
This routine determines from a state transformation matrix the associated
rotation matrix and angular velocity of the rotation.

rav2xf(<float[3,3]> rot, <float[3]> av) -> <float[6,6]> xform

rot   = Rotation matrix.
av    = Angular velocity vector.
xform = State transformation associated with rot and av.
"""

#########################################
SPICE_SIGNATURES["raxisa"] = ["float[3,3]"]
SPICE_RETURNS   ["raxisa"] = ["float[3]", "float"]
SPICE_DOCSTRINGS["raxisa"] = """
Compute the axis of the rotation given by an input matrix and the angle of
the rotation about that axis.

raxisa(<float[3,3]> matrix) -> [<float[3]> axis, <float> angle]

matrix = 3x3 rotation matrix in double precision.
axis   = Axis of the rotation.
angle  = Angle through which the rotation is performed.
"""

#########################################
SPICE_SIGNATURES["reccyl"] = ["float[3]"]
SPICE_RETURNS   ["reccyl"] = 3*["float"]
SPICE_DOCSTRINGS["reccyl"] = """
Convert from rectangular to cylindrical coordinates.

reccyl(<float[3]> rectan) -> [<float> r, <float> lon, <float> z]

rectan = Rectangular coordinates of a point.
r      = Distance of the point from z axis.
lon    = Angle (radians) of the point from xZ plane
z      = Height of the point above xY plane.
"""

#########################################
SPICE_SIGNATURES["recgeo"] = ["float[3]", "float", "float"]
SPICE_RETURNS   ["recgeo"] = 3*["float"]
SPICE_DOCSTRINGS["recgeo"] = """
Convert from rectangular coordinates to geodetic coordinates.

recgeo(<float[3]> rectan, <float> re, <float> f) ->
                                [<float> lon, <float> lat, <float> alt]

rectan = Rectangular coordinates of a point.
re     = Equatorial radius of the reference spheroid.
f      = Flattening coefficient.
lon    = Geodetic longitude of the point (radians).
lat    = Geodetic latitude  of the point (radians).
alt    = Altitude of the point above reference spheroid.
"""

#########################################
SPICE_SIGNATURES["reclat"] = ["float[3]"]
SPICE_RETURNS   ["reclat"] = 3*["float"]
SPICE_DOCSTRINGS["reclat"] = """
Convert from rectangular coordinates to latitudinal coordinates.

reclat(<float[3]> rectan) -> [<float> radius, <float> longitude,
                                              <float> latitude]

rectan    = Rectangular coordinates of a point.
radius    = Distance of the point from the origin.
longitude = Longitude of the point in radians.
latitude  = Latitude of the point in radians.
"""

#########################################
SPICE_SIGNATURES["recpgr"] = ["body_name", "float[3]", "float", "float"]
SPICE_RETURNS   ["recpgr"] = 3*["float"]
SPICE_DOCSTRINGS["recpgr"] = """
Convert rectangular coordinates to planetographic coordinates.

recpgr(<string> body, <float[3]> rectan, <float> re, <float> f) ->
                                [<float> lon, <float> lat, <float> alt]

body   = Body with which coordinate system is associated.
rectan = Rectangular coordinates of a point.
re     = Equatorial radius of the reference spheroid.
f      = Flattening coefficient.
lon    = Planetographic longitude of the point (radians).
lat    = Planetographic latitude of the point (radians).
alt    = Altitude of the point above reference spheroid.
"""

#########################################
SPICE_SIGNATURES["recrad"] = ["float[3]"]
SPICE_RETURNS   ["recrad"] = 3*["float"]
SPICE_DOCSTRINGS["recrad"] = """
Convert rectangular coordinates to range, right ascension, and declination.

recrad(<float[3]> rectan) -> [<float> range, <float> ra, <float> dec]

rectan = Rectangular coordinates of a point.
range  = Distance of the point from the origin.
ra     = Right ascension in radians.
dec    = Declination in radians.
"""

#########################################
SPICE_SIGNATURES["recsph"] = ["float[3]"]
SPICE_RETURNS   ["recsph"] = 3*["float"]
SPICE_DOCSTRINGS["recsph"] = """
Convert from rectangular coordinates to spherical coordinates.

recsph(<float[3]> rectan) -> [<float> r, <float> colat, <float> lon]

rectan = Rectangular coordinates of a point.
r      = Distance of the point from the origin.
colat  = Angle of the point from the positive Z-axis.
lon    = Longitude of the point in radians.
"""

#########################################
SPICE_SIGNATURES["refchg"] = ["frame_code", "frame_code", "float"]
SPICE_RETURNS   ["refchg"] = ["float[3,3]"]
SPICE_DOCSTRINGS["refchg"] = """
Return the transformation matrix from one frame to another.

refchg(<int> frame1, <int> frame2, <float> et) -> <float[3,3]> rotate

frame1 = the frame id-code for some reference frame
frame2 = the frame id-code for some reference frame
et     = an epoch in TDB seconds past J2000.
rotate = a rotation matrix.
"""

#########################################
SPICE_SIGNATURES["repmc"] = ["string", "string", "string"]
SPICE_RETURNS   ["repmc"] = ["string"]
SPICE_DOCSTRINGS["repmc"] = """
Replace a marker with a character string.

repmc(<string> in, <string> marker, <string> value) -> <string> out

in     = Input string.
marker = Marker to be replaced.
value  = Replacement value.
out    = Output string.
"""

#########################################
SPICE_SIGNATURES["repmct"] = ["string", "string", "int", "string"]
SPICE_RETURNS   ["repmct"] = ["string"]
SPICE_DOCSTRINGS["repmct"] = """
Replace a marker with the text representation of a cardinal number.

repmct(<string> in, <string> marker, <int> value,
                                     <string> repcase) -> <string> out

in      = Input string.
marker  = Marker to be replaced.
value   = Replacement value.
repcase = Case of replacement text.
out     = Output string.
"""

#########################################
SPICE_SIGNATURES["repmd"] = ["string", "string", "float", "int"]
SPICE_RETURNS   ["repmd"] = ["string"]
SPICE_DOCSTRINGS["repmd"] = """
Replace a marker with a double precision number.

repmd(<string> in, <string> marker, <float> value,
                                    <int>sigdig) -> <string> out

in     = Input string.
marker = Marker to be replaced.
value  = Replacement value.
sigdig = Significant digits in replacement text.
out    = Output string.
"""

#########################################
SPICE_SIGNATURES["repmf"] = ["string", "string", "float", "int", "string"]
SPICE_RETURNS   ["repmf"] = ["string"]
SPICE_DOCSTRINGS["repmf"] = """
Replace a marker in a string with a formatted double precision value.

repmf(<string> in, <string> marker, <float> value,
                   <int> sigdig, <string> format) -> <string> out

in     = Input string.
marker = Marker to be replaced.
value  = Replacement value.
sigdig = Significant digits in replacement text.
format = Format: 'E' or 'F'.
out    = Output string.
"""

#########################################
SPICE_SIGNATURES["repmi"] = ["string", "string", "int"]
SPICE_RETURNS   ["repmi"] = ["string"]
SPICE_DOCSTRINGS["repmi"] = """
Replace a marker with an integer.

repmi(<string> in, <string> marker, <string> value) -> <string> out

in     = Input string.
marker = Marker to be replaced.
value  = Replacement value.
out    = Output string.
"""

#########################################
SPICE_SIGNATURES["repmot"] = ["string", "string", "int", "string"]
SPICE_RETURNS   ["repmot"] = ["string"]
SPICE_DOCSTRINGS["repmot"] = """
Replace a marker with the text representation of an ordinal number.

repmot(<string> in, <string> marker, <int> value,
                                     <string> repcase) -> <string> out

in      = Input string.
marker  = Marker to be replaced.
value   = Replacement value.
repcase = Case of replacement text.
out     = Output string.
"""

#########################################
SPICE_SIGNATURES["reset"] = []
SPICE_RETURNS   ["reset"] = []
SPICE_DOCSTRINGS["reset"] = """
Reset the CSPICE error status to a value of "no error." as a result, the
status routine, failed, will return a value of False.

reset()
"""

#########################################
SPICE_SIGNATURES["rotate"] = ["float", "int"]
SPICE_RETURNS   ["rotate"] = ["float[3,3]"]
SPICE_DOCSTRINGS["rotate"] = """
Calculate the 3x3 rotation matrix generated by a rotation of a specified
angle about a specified axis. This rotation is thought of as rotating the
coordinate system.

rotate(<float> angle, <int> iaxis) -> <float[3,3]> mout

angle = Angle of rotation (radians).
iaxis = Axis of rotation (X=1, Y=2, Z=3).
mout  = Resulting rotation matrix.
"""

#########################################
SPICE_SIGNATURES["rotmat"] = ["float[3,3]", "float", "int"]
SPICE_RETURNS   ["rotmat"] = ["float[3,3]"]
SPICE_DOCSTRINGS["rotmat"] = """
Apply a rotation of angle radians about axis iaxis to a matrix. This
rotation is thought of as rotating the coordinate system.

rotmat(<float[3,3]> m1, <float> angle, iaxis) -> <float[3,3]> mout

m1    = Matrix to be rotated.
angle = Angle of rotation (radians).
iaxis = Axis of rotation (X=1, Y=2, Z=3).
mout  = Resulting rotated matrix.
"""

#########################################
SPICE_SIGNATURES["rotvec"] = ["float[3]", "float", "int"]
SPICE_RETURNS   ["rotvec"] = ["float[3]"]
SPICE_DOCSTRINGS["rotvec"] = """
Transform a vector to a new coordinate system rotated by angle radians
about axis iaxis.  This transformation rotates v1 by -angle radians about
the specified axis.

rotvec(<float[3]> v1, <float> angle, iaxis) -> <float[3]> vout

v1    =  Vector whose coordinate system is to be rotated.
angle =  Angle of rotation in radians.
iaxis =  Axis of rotation (X=1, Y=2, Z=3).
vout  = Resulting vector[angle]
"""

#########################################
SPICE_SIGNATURES["rpd"] = []
SPICE_RETURNS   ["rpd"] = ["float"]
SPICE_DOCSTRINGS["rpd"] = """
Return the number of radians per degree.

rpd() -> <float> value
"""

#########################################
SPICE_SIGNATURES["rquad"] = 3*["float"]
SPICE_RETURNS   ["rquad"] = 2*["float[2]"]
SPICE_DOCSTRINGS["rquad"] = """
Find the roots of a quadratic equation.

rquad(<float> a, <float> b, <float> c) -> [<float[2]> root1,
                                           <float[2]> root2]

a     = Coefficient of quadratic term.
b     = Coefficient of linear term.
c     = Constant.
root1 = Root built from positive discriminant term.
root2 = Root built from negative discriminant term.
"""

#########################################
SPICE_SIGNATURES["saelgv"] = 2*["float[3]"]
SPICE_RETURNS   ["saelgv"] = 2*["float[3]"]
SPICE_DOCSTRINGS["saelgv"] = """
Find semi-axis vectors of an ellipse generated by two arbitrary
three-dimensional vectors.

saelgv(<float[3]> vec1, <float[3]> vec2) -> [<float[3]> smajor,
                                             <float[3]> sminor]

vec1, vec2 = Two vectors used to generate an ellipse.
smajor     = Semi-major axis of ellipse.
sminor     = Semi-minor axis of ellipse.
"""

#########################################
SPICE_SIGNATURES["scdecd"] = ["body_code", "float"]
SPICE_RETURNS   ["scdecd"] = ["string"]
SPICE_DOCSTRINGS["scdecd"] = """
Convert double precision encoding of spacecraft clock time into a character
representation.

scdecd(<int> sc, <float> sclkdp) -> <string> sclkch

sc     = NAIF spacecraft identification code.
sclkdp = Encoded representation of a spacecraft clock count.
sclkch = Character representation of a clock count.
"""

#########################################
SPICE_SIGNATURES["sce2c"] = ["body_code", "float"]
SPICE_RETURNS   ["sce2c"] = ["float"]
SPICE_DOCSTRINGS["sce2c"] = """
Convert ephemeris seconds past j2000 (ET) to continuous encoded spacecraft
clock (`ticks').  Non-integral tick values may be returned.

sce2c(<int> sc, <float> et) -> <float> sclkdp

sc     = NAIF spacecraft ID code.
et     = Ephemeris time, seconds past j2000.
sclkdp = SCLK, encoded as ticks since spacecraft clock start. sclkdp need
         not be integral.
"""

#########################################
SPICE_SIGNATURES["sce2s"] = ["body_code", "float"]
SPICE_RETURNS   ["sce2s"] = ["string"]
SPICE_DOCSTRINGS["sce2s"] = """
Convert an epoch specified as ephemeris seconds past J2000 (ET) to a
character string representation of a spacecraft clock value (SCLK).

sce2s(<int> sc, <float> et) -> <string> sclkch

sc     = NAIF spacecraft clock ID code.
et     = Ephemeris time, specified as seconds past J2000.
sclkch = An SCLK string.
"""

#########################################
SPICE_SIGNATURES["sce2t"] = ["body_code", "float"]
SPICE_RETURNS   ["sce2t"] = ["float"]
SPICE_DOCSTRINGS["sce2t"] = """
Convert ephemeris seconds past J2000 (ET) to integral encoded spacecraft
clock (`ticks'). For conversion to fractional ticks, (required for C-kernel
production), see the routine sce2c.

sce2t(<int> sc, <float> et) -> <float> sclkdp

sc     = NAIF spacecraft ID code.
et     = Ephemeris time, seconds past J2000.
sclkdp = SCLK, encoded as ticks since spacecraft clock start.
"""

#########################################
SPICE_SIGNATURES["scencd"] = ["body_code", "string"]
SPICE_RETURNS   ["scencd"] = ["float"]
SPICE_DOCSTRINGS["scencd"] = """
Encode character representation of spacecraft clock time into a double
precision number.

scencd(<int> sc, <string> sclkch) -> <float> sclkdp

sc     = NAIF spacecraft identification code.
sclkch = Character representation of a spacecraft clock.
sclkdp = Encoded representation of the clock count.
"""

#########################################
SPICE_SIGNATURES["scfmt"] = ["body_code", "float"]
SPICE_RETURNS   ["scfmt"] = ["string"]
SPICE_DOCSTRINGS["scfmt"] = """
Convert encoded spacecraft clock ticks to character clock format.

scfmt(<int> sc, <float> ticks) -> <string> clkstr

sc     = NAIF spacecraft identification code.
ticks  = Encoded representation of a spacecraft clock count.
clkstr = Character representation of a clock count.
"""

#########################################
SPICE_SIGNATURES["scpart"] = ["body_code"]
SPICE_RETURNS   ["scpart"] = 2*["float"]
SPICE_DOCSTRINGS["scpart"] = """
Get spacecraft clock partition information from a spacecraft clock kernel
file.

scpart(<int> sc) -> [<float> pstart, <float> pstop]

sc     = NAIF spacecraft identification code.
pstart = Array of partition start times.
pstop  = Array of partition stop times.
"""

#########################################
SPICE_SIGNATURES["scs2e"] = ["body_code", "string"]
SPICE_RETURNS   ["scs2e"] = ["float"]
SPICE_DOCSTRINGS["scs2e"] = """
Convert a spacecraft clock string to ephemeris seconds past J2000 (ET).

scs2e(<int> sc, <string> sclkch) -> <float> et

sc     = NAIF integer code for a spacecraft.
sclkch = An SCLK string.
et     = Ephemeris time, seconds past J2000.
"""

#########################################
SPICE_SIGNATURES["sct2e"] = ["body_code", "float"]
SPICE_RETURNS   ["sct2e"] = ["float"]
SPICE_DOCSTRINGS["sct2e"] = """
Convert encoded spacecraft clock (`ticks') to ephemeris seconds past
J2000 (ET).

sct2e(<int> sc, <float> sclkdp) -> <float> et

sc     = NAIF spacecraft ID code.
sclkdp = SCLK, encoded as ticks since spacecraft clock start.
et     = Ephemeris time, seconds past J2000.
"""

#########################################
SPICE_SIGNATURES["sctiks"] = ["body_code", "string"]
SPICE_RETURNS   ["sctiks"] = ["float"]
SPICE_DOCSTRINGS["sctiks"] = """
Convert a spacecraft clock format string to number of "ticks".

sctiks(<int> sc, <string> clkstr) -> <float> ticks

sc     = NAIF spacecraft identification code.
clkstr = Character representation of a spacecraft clock.
ticks  = Number of ticks represented by the clock string.
"""

#########################################
SPICE_SIGNATURES["setmsg"] = ["string"]
SPICE_RETURNS   ["setmsg"] = []
SPICE_DOCSTRINGS["setmsg"] = """
Set the value of the current long error message.

setmsg(<string> message)

message = A long error message.
"""

#########################################
SPICE_SIGNATURES["sigerr"] = ["string"]
SPICE_RETURNS   ["sigerr"] = []
SPICE_DOCSTRINGS["sigerr"] = """
Inform the CSPICE error processing mechanism that an error has occurred,
and specify the type of error.

sigerr(<string> message)

message = A short error message.
"""

#########################################
SPICE_SIGNATURES["sincpt"] = ["string", "body_name", "float", "frame_name",
                              "string", "body_name", "frame_name", "float[3]"]
SPICE_RETURNS   ["sincpt"] = ["float[3]", "float", "float[3]", "bool"]
SPICE_DOCSTRINGS["sincpt"] = """
Given an observer and a direction vector defining a ray, compute the
surface intercept of the ray on a target body at a specified epoch,
optionally corrected for light time and stellar aberration.

The surface of the target body may be represented by a triaxial ellipsoid
or by topographic data provided by DSK files.

This routine supersedes srfxpt.

sincpt(<string> method, <string> target, <float> et, <string> fixref,
       <string> abcorr, <string> obsrvr, dref, <float[3]> dvec) ->
                        [<float[3]> spoint, <float> trgepc,
                         <float[3]> srfvec, <bool> found]

method = Computation method.
target = Name of target body.
et     = Epoch in TDB seconds past J2000 TDB.
fixref = Body-fixed, body-centered target body frame.
abcorr = Aberration correction flag.
obsrvr = Name of observing body.
dref   = Reference frame of ray's direction vector.
dvec   = Ray's direction vector.
spoint = Surface intercept point on the target body.
trgepc = Intercept epoch.
srfvec = Vector from observer to intercept point.
found  = Flag indicating whether intercept was found.
"""

#########################################
SPICE_SIGNATURES["spd"] = []
SPICE_RETURNS   ["spd"] = ["float"]
SPICE_DOCSTRINGS["spd"] = """
Return the number of seconds in a day.

spd() -> <float> value
"""

#########################################
SPICE_SIGNATURES["sphcyl"] = 3*["float"]
SPICE_RETURNS   ["sphcyl"] = 3*["float"]
SPICE_DOCSTRINGS["sphcyl"] = """
This routine converts from spherical coordinates to cylindrical coordinates.

sphcyl(<float> radius, <float> colat, <float> slon) ->
                                    [<float> r, <float> lon, <float> z]

radius = Distance of point from origin.
colat  = Polar angle (co-latitude in radians) of point.
slon   = Azimuthal angle (longitude) of point (radians).
r      = Distance of point from z axis.
lon    = angle (radians) of point from XZ plane.
z      = Height of point above XY plane.
"""

#########################################
SPICE_SIGNATURES["sphlat"] = 3*["float"]
SPICE_RETURNS   ["sphlat"] = 3*["float"]
SPICE_DOCSTRINGS["sphlat"] = """
Convert from spherical coordinates to latitudinal coordinates.

sphlat(<float> r, <float> colat, <float> lons) ->
                                [<float> radius, <float> lon, <float> lat]

r      = Distance of the point from the origin.
colat  = Angle of the point from positive z axis (radians).
lons   = Angle of the point from the XZ plane (radians).
radius = Distance of a point from the origin
lon    = Angle of the point from the XZ plane in radians
lat    = Angle of the point from the XY plane in radians
"""

#########################################
SPICE_SIGNATURES["sphrec"] = 3*["float"]
SPICE_RETURNS   ["sphrec"] = ["float[3]"]
SPICE_DOCSTRINGS["sphrec"] = """
Convert from spherical coordinates to rectangular coordinates.

sphrec(<float> r, <float> colat, <float> lon) -> <float[3]> rectan

r      = Distance of a point from the origin.
colat  = Angle of the point from the positive Z-axis.
lon    = Angle of the point from the XZ plane in radians.
rectan = Rectangular coordinates of the point.
"""

#########################################
SPICE_SIGNATURES["spkacs"] = ["body_code", "float", "frame_name", "string",
                              "body_code"]
SPICE_RETURNS   ["spkacs"] = ["float[6]", "float", "float"]
SPICE_DOCSTRINGS["spkacs"] = """
Return the state (position and velocity) of a target body relative to an
observer, optionally corrected for light time and stellar aberration,
expressed relative to an inertial reference frame.

spkacs(<int> targ, <float> et, <string> ref, <string> abcorr,
       <int> obs) -> [<float[6]> starg, lt, dlt]

targ   = Target body.
et     = Observer epoch.
ref    = Inertial reference frame of output state.
abcorr = Aberration correction flag.
obs    = Observer.
starg  = State of target.
lt     = One way light time between observer and target.
dlt    = Derivative of light time with respect to time.
"""

#########################################
SPICE_SIGNATURES["spkapo"] = ["body_code", "float", "frame_name", "float[6]",
                              "string"]
SPICE_RETURNS   ["spkapo"] = ["float[6]", "float"]
SPICE_DOCSTRINGS["spkapo"] = """
Return the position of a target body relative to an observer, optionally
corrected for light time and stellar aberration.

spkapo(<int> targ, <float> et, <string> ref,
       <float[6]> sobs, <string> abcorr) -> [<float[3]> ptarg, <float> lt]

targ   = Target body.
et     = Observer epoch.
ref    = Inertial reference frame of observer's state.
sobs   = State of observer wrt. solar system barycenter.
abcorr = Aberration correction flag.
ptarg  = Position of target.
lt     = One way light time between observer and target.
"""

#########################################
SPICE_SIGNATURES["spkapp"] = ["body_code", "float", "frame_name", "float[6]",
                              "string"]
SPICE_RETURNS   ["spkapp"] = ["float[6]", "float"]
SPICE_DOCSTRINGS["spkapp"] = """
Return the state (position and velocity) of a target body relative to an
observer, optionally corrected for light time and stellar aberration.

spkapp(<int> targ, <float> et, <string> ref, <float[6]> sobs,
       <string> abcorr) -> [<float[6]> starg, <float> lt]

targ   = Target body.
et     = Observer epoch.
ref    = Inertial reference frame of observer's state.
sobs   = State of observer wrt. solar system barycenter.
abcorr = Aberration correction flag.
starg  = State of target.
lt     = One way light time between observer and target.
"""

#########################################
SPICE_SIGNATURES["spkaps"] = ["body_code", "float", "frame_name", "string",
                              "float[6]", "float[6]"]
SPICE_RETURNS   ["spkaps"] = ["float[6]", "float", "float"]
SPICE_DOCSTRINGS["spkaps"] = """
Given the state and acceleration of an observer relative to the solar
system barycenter, return the state (position and velocity) of a target body
relative to the observer, optionally corrected for light time and stellar
aberration. All input and output vectors are expressed relative to an
inertial reference frame.

This routine supersedes spkapp.

SPICE users normally should call the high-level API routines spkezr or
spkez rather than this routine.

spkaps(<int> targ, <float> et, <string> ref, <string> abcorr,
       <float[6]> stobs, <float[6]> accobs) -> [<float[6]> starg,
                                                <float> lt, <float> dlt]

targ   = Target body.
et     = Observer epoch.
ref    = Inertial reference frame of output state.
abcorr = Aberration correction flag.
stobs  = State of the observer relative to the SSB.
accobs = Acceleration of the observer relative to the SSB.
starg  = State of target.
lt     = One way light time between observer and target.
dlt    = Derivative of light time with respect to time.
"""

#########################################
SPICE_SIGNATURES["spkcov"] = ["string", "body_code"]
SPICE_RETURNS   ["spkcov"] = ["float[*,2]"]
SPICE_DOCSTRINGS["spkcov"] = """
Find the coverage window for a specified ephemeris object in a specified
SPK file.

spkcov(<string> spk, <int> idcode) -> <float[*,2]> cover

spk    = Name of SPK file.
idcode = ID code of ephemeris object.
cover  = An array of shape (n,2), where cover[:,0] are start times and
         cover[:,1] are stop times.
"""

SPICE_SIGNATURES["spkcov_error"] = ["string", "body_code"]
SPICE_RETURNS   ["spkcov_error"] = ["float[*,2]", "body_code"]
SPICE_DOCSTRINGS["spkcov_error"] = """
Find the coverage window for a specified ephemeris object in a specified
SPK file.

spkcov(<string> spk, <int> idcode) -> <float[*,2]> cover

spk    = Name of SPK file.
idcode = ID code of ephemeris object.
cover  = An array of shape (n,2), where cover[:,0] are start times and
         cover[:,1] are stop times.

Raise KeyError if the idcode is not found.
"""

#########################################
SPICE_SIGNATURES["spkez"] = ["body_code", "float", "frame_name", "string",
                             "body_code"]
SPICE_RETURNS   ["spkez"] = ["float[6]", "float"]
SPICE_DOCSTRINGS["spkez"] = """
Return the state (position and velocity) of a target body relative to an
observing body, optionally corrected for light time (planetary aberration)
and stellar aberration.

spkez(<int> targ, <float> et, <string> ref, <string> abcorr,
      <int> obs) -> [<float[6]> starg, <float> lt]

targ   = Target body.
et     = Observer epoch.
ref    = Reference frame of output state vector.
abcorr = Aberration correction flag.
obs    = Observing body.
starg  = State of target.
lt     = One way light time between observer and target.
"""

SPICE_SIGNATURES["spkez_vector"] = ["body_code", "float[*]", "frame_name",
                                    "string", "body_code"]
SPICE_RETURNS   ["spkez_vector"] = ["float[*,6]", "float[*]"]
SPICE_DOCSTRINGS["spkez_vector"] = """
Return the state (position and velocity) of a target body relative to an
observing body, optionally corrected for light time (planetary aberration)
and stellar aberration.

This vectorized version handles an array of values for et.

spkez(<int> targ, <float[*]> et, <string> ref, <string> abcorr,
      <int> obs) -> [<float[*,6]> starg, <float[*]> lt]

targ   = Target body.
et     = Observer epoch.
ref    = Reference frame of output state vector.
abcorr = Aberration correction flag.
obs    = Observing body.
starg  = State of target.
lt     = One way light time between observer and target.
"""

#########################################
SPICE_SIGNATURES["spkezp"] = ["body_code", "float", "frame_name", "string",
                              "body_code"]
SPICE_RETURNS   ["spkezp"] = ["float[6]", "float"]
SPICE_DOCSTRINGS["spkezp"] = """
Return the position of a target body relative to an observing body,
optionally corrected for light time (planetary aberration) and stellar
aberration.

spkezp(<int> targ, <float> et, <string> ref, <string> abcorr,
       <int> obs) -> [<float[3]> ptarg, <float> lt]

targ   = Target body NAIF ID code.
et     = Observer epoch.
ref    = Reference frame of output position vector.
abcorr = Aberration correction flag.
obs    = Observing body NAIF ID code.
ptarg  = Position of target.
lt     = One way light time between observer and target.
"""

#########################################
SPICE_SIGNATURES["spkezr"] = ["body_name", "float", "frame_name", "string",
                              "body_name"]
SPICE_RETURNS   ["spkezr"] = ["float[6]", "float"]
SPICE_DOCSTRINGS["spkezr"] = """
Return the state (position and velocity) of a target body relative to an
observing body, optionally corrected for light time (planetary aberration)
and stellar aberration.

spkezr(<string> targ, <float> et, ref, <string> abcorr, <int> obs) ->
                                        [<float[6]> starg, <float> lt]

targ   = Target body name.
et     = Observer epoch.
ref    = Reference frame of output state vector.
abcorr = Aberration correction flag.
obs    = Observing body name.
starg  = State of target.
lt     = One way light time between observer and target.
"""

#########################################
SPICE_SIGNATURES["spkgeo"] = ["body_code", "float", "frame_name",
                              "body_code"]
SPICE_RETURNS   ["spkgeo"] = ["float[6]", "float"]
SPICE_DOCSTRINGS["spkgeo"] = """
Compute the geometric state (position and velocity) of a target body
relative to an observing body.

spkgeo(<int> targ, <float> et, ref, obs) -> [<float[6]> state, <float> lt]

targ  = Target body code.
et    = Target epoch.
ref   = Target reference frame name.
obs   = Observing body code.
state = State of target.
lt    = Light time.
"""

#########################################
SPICE_SIGNATURES["spkgps"] = ["body_code", "float", "frame_name",
                              "body_code"]
SPICE_RETURNS   ["spkgps"] = ["float[3]", "float"]
SPICE_DOCSTRINGS["spkgps"] = """
Compute the geometric position of a target body relative to an observing
body.

spkgps(<int> targ, <float> et, <string> ref, <int> obs) ->
                                        [<float[3]> pos, <float> lt]

targ = Target body code.
et   = Target epoch.
ref  = Target reference frame name.
obs  = Observing body code.
pos  = Position of target.
lt   = Light time.
"""

#########################################
SPICE_SIGNATURES["spkltc"] = ["body_code", "float", "frame_name", "string",
                              "float[6]", "float[6]"]
SPICE_RETURNS   ["spkltc"] = ["float[6]", "float", "float"]
SPICE_DOCSTRINGS["spkltc"] = """
Return the state (position and velocity) of a target body relative to an
observer, optionally corrected for light time, expressed relative to an
inertial reference frame.

spkltc(<int> targ, <float> et, <string> ref, <string> abcorr,
       <float[6]> stobs) -> [<float[6]> starg, <float> lt, <float> dlt]

targ   = Target body code.
et     = Observer epoch.
ref    = Inertial reference frame name of output state.
abcorr = Aberration correction flag.
stobs  = State of the observer relative to the SSB.
starg  = State of target.
lt     = One way light time between observer and target.
dlt    = Derivative of light time with respect to time.
"""

#########################################
SPICE_SIGNATURES["spkobj"] = ["string"]
SPICE_RETURNS   ["spkobj"] = ["int[*]"]
SPICE_DOCSTRINGS["spkobj"] = """
Find the set of ID codes of all objects in a specified SPK file.

spkobj(<string> spk) -> <int[*]> ids

spk = Name of SPK file.
ids = Array of ID codes of objects in SPK file.
"""

#########################################
SPICE_SIGNATURES["spkpos"] = ["body_name", "float", "frame_name", "string",
                              "body_name"]
SPICE_RETURNS   ["spkpos"] = ["float[3]", "float"]
SPICE_DOCSTRINGS["spkpos"] = """
Return the position of a target body relative to an observing body,
optionally corrected for light time (planetary aberration) and stellar
aberration.

spkpos(<string> targ, <float> et, <string> ref, <string> abcorr,
       <string> obs) -> [<float[3]> ptarg, <float> lt]

targ   = Target body name.
et     = Observer epoch.
ref    = Reference frame of output position vector.
abcorr = Aberration correction flag.
obs    = Observing body name.
ptarg  = Position of target.
lt     = One way light time between observer and target.
"""

#########################################
SPICE_SIGNATURES["spkssb"] = ["body_code", "float", "frame_name"]
SPICE_RETURNS   ["spkssb"] = ["float[6]"]
SPICE_DOCSTRINGS["spkssb"] = """
Return the state (position and velocity) of a target body relative to the
solar system barycenter.

spkssb(<int> targ, <float> et, <string> ref) -> <float[6]> starg

targ  = Target body code.
et    = Target epoch.
ref   = Target reference frame name.
starg = State of target.
"""

#########################################
SPICE_SIGNATURES["srfc2s"] = ["int", "body_code"]
SPICE_RETURNS   ["srfc2s"] = ["string", "bool"]
SPICE_DOCSTRINGS["srfc2s"] = """
Translate a surface ID code, together with a body ID code, to the
corresponding surface name. If no such name exists, return a string
representation of the surface ID code.

srfc2s(<int> code, <int> bodyid) -> [<string> srfstr, <bool> isname]

code   = Integer surface ID code to translate to a string.
bodyid = ID code of body associated with surface.
srflen = Length of output string `srfstr'.
srfstr = String corresponding to surface ID code.
isname = True to indicate output is a surface name.
"""

SPICE_SIGNATURES["srfc2s_error"] = ["int", "body_code"]
SPICE_RETURNS   ["srfc2s_error"] = ["string"]
SPICE_DOCSTRINGS["srfc2s_error"] = """
Translate a surface ID code, together with a body ID code, to the
corresponding surface name. If no such name exists, raise KeyError.

srfc2s(<int> code, <int> bodyid) -> <string> srfstr

code   = Integer surface ID code to translate to a string.
bodyid = ID code of body associated with surface.
srflen = Length of output string `srfstr'.
srfstr = String corresponding to surface ID code.

Raise KeyError if not found.
"""

#########################################
SPICE_SIGNATURES["srfcss"] = ["int", "body_name"]
SPICE_RETURNS   ["srfcss"] = ["string", "bool"]
SPICE_DOCSTRINGS["srfcss"] = """
Translate a surface ID code, together with a body string, to the
corresponding surface name. If no such surface name exists, return a
string representation of the surface ID code.

srfcss(<int> code, <string> bodstr) -> [<string> srfstr, <bool> isname]

code   = Integer surface ID code to translate to a string.
bodstr = Name or ID of body associated with surface.
srflen = Length of output string `srfstr'.
srfstr = String corresponding to surface ID code.
isname = Flag indicating whether output is a surface name.
"""

SPICE_SIGNATURES["srfcss_error"] = ["int", "body_name"]
SPICE_RETURNS   ["srfcss_error"] = ["string"]
SPICE_DOCSTRINGS["srfcss_error"] = """
Translate a surface ID code, together with a body string, to the
corresponding surface name. If no such surface name exists, raise a
KeyError.

srfcss(<int> code, <string> bodstr) -> <string> srfstr

code   = Integer surface ID code to translate to a string.
bodstr = Name or ID of body associated with surface.
srflen = Length of output string `srfstr'.
srfstr = String corresponding to surface ID code.

Raise KeyError if not found.
"""

#########################################
SPICE_SIGNATURES["srfnrm"] = ["string", "body_name", "float", "frame_name"]
SPICE_RETURNS   ["srfnrm"] = ["float[*,3]", "float[*,3]"]
SPICE_DOCSTRINGS["srfnrm"] = """
Map array of surface points on a specified target body to the corresponding
unit length outward surface normal vectors.

The surface of the target body may be represented by a triaxial ellipsoid
or by topographic data provided by DSK files.

srfnrm(<string> method, <string> target, <float> et, <string> fixref) ->
                            [<float[:,3]> srfpts, <float[:,3]> normls]

method = Computation method.
target = Name of target body.
et     = Epoch in TDB seconds past J2000 TDB.
fixref = Body-fixed, body-centered target body frame.
srfpts = Array of surface points.
normls = Array of outward, unit length normal vectors.
"""

#########################################
SPICE_SIGNATURES["srfrec"] = ["body_code", "float", "float"]
SPICE_RETURNS   ["srfrec"] = ["float[3]"]
SPICE_DOCSTRINGS["srfrec"] = """
Convert planetocentric latitude and longitude of a surface point on a
specified body to rectangular coordinates.

srfrec(<int> body, <float> longitude,
                   <float> latitude) -> <float[3]> rectan

body      = NAIF integer code of an extended body.
longitude = Longitude of point in radians.
latitude  = Latitude of point in radians.
rectan    = Rectangular coordinates of the point.
"""

#########################################
SPICE_SIGNATURES["srfs2c"] = ["string", "body_name"]
SPICE_RETURNS   ["srfs2c"] = ["int", "bool"]
SPICE_DOCSTRINGS["srfs2c"] = """
Translate a surface string, together with a body string, to the
corresponding surface ID code. The input strings may contain names or
integer ID codes.

srfs2c(<string> srfstr, <string> bodstr) -> [<int> code, <bool> found]

srfstr = Surface name or ID string.
bodstr = Body name or ID string.
code   = Integer surface ID code.
found  = True indicating that surface ID was found, False otherwise.
"""

SPICE_SIGNATURES["srfs2c_error"] = ["string", "body_name"]
SPICE_RETURNS   ["srfs2c_error"] = ["int"]
SPICE_DOCSTRINGS["srfs2c_error"] = """
Translate a surface string, together with a body string, to the
corresponding surface ID code. The input strings may contain names or
integer ID codes.

srfs2c(<string> srfstr, <string> bodstr) -> <int> code

srfstr = Surface name or ID string.
bodstr = Body name or ID string.
code   = Integer surface ID code.

Raise KeyError if not found.
"""

#########################################
SPICE_SIGNATURES["srfscc"] = ["string", "body_code"]
SPICE_RETURNS   ["srfscc"] = ["int", "bool"]
SPICE_DOCSTRINGS["srfscc"] = """
Translate a surface string, together with a body ID code, to the
corresponding surface ID code. The input surface string may contain a name
or an integer ID code.

srfscc(<string> srfstr, <int> bodyid) -> [<int> code, <bool> found]

srfstr = Surface name or ID string.
bodyid = Body ID code.
code   = Integer surface ID code.
found  = True indicating that surface ID was found, False otherwise.
"""

SPICE_SIGNATURES["srfscc_error"] = ["string", "body_code"]
SPICE_RETURNS   ["srfscc_error"] = ["int"]
SPICE_DOCSTRINGS["srfscc_error"] = """
Translate a surface string, together with a body ID code, to the
corresponding surface ID code. The input surface string may contain a name
or an integer ID code.

srfscc(<string> srfstr, <int> bodyid) -> <int> code

srfstr = Surface name or ID string.
bodyid = Body ID code.
code   = Integer surface ID code.

Raise KeyError if not found.
"""

#########################################
SPICE_SIGNATURES["srfxpt"] = ["string", "body_name", "float", "string",
                              "body_name", "frame_name", "float[3]"]
SPICE_RETURNS   ["srfxpt"] = ["float[3]", "float", "float", "float[3]", "bool"]
SPICE_DOCSTRINGS["srfxpt"] = """
Given an observer and a direction vector defining a ray, compute the
surface intercept point of the ray on a target body at a specified epoch,
optionally corrected for light time and stellar aberration.

srfxpt(<string> method, <string> target, <float> et, <string> abcorr,
       <string> obsrvr, <string> dref, <float[3]> dvec) -> 
                            [<float[3]> spoint, <float> dist,
                             <float> trgepc, <float[3]> obspos, <bool> found]

method = Computation method.
target = Name of target body.
et     = Epoch in ephemeris seconds past J2000 TDB.
abcorr = Aberration correction.
obsrvr = Name of observing body.
dref   = Reference frame of input direction vector.
dvec   = Ray's direction vector.
spoint = Surface intercept point on the target body.
dist   = Distance from the observer to the intercept point.
trgepc = Intercept epoch.
obspos = Observer position relative to target center.
found  = Flag indicating whether intercept was found.
"""

#########################################
SPICE_SIGNATURES["stcf01"] = ["string"] + 4*["float"]
SPICE_RETURNS   ["stcf01"] = ["int"]
SPICE_DOCSTRINGS["stcf01"] = """
Search through a type 1 star catalog and return the number of stars within
a specified RA - DEC rectangle.

stcf01(<string> catnam, <float> westra, <float> eastra,
                        <float> sthdec, <float> nthdec) -> <int> nstars

catnam = Catalog table name.
westra = Western most right ascension in radians.
eastra = Eastern most right ascension in radians.
sthdec = Southern most declination in radians.
nthdec = Northern most declination in radians.
nstars = Number of stars found.
"""

#########################################
SPICE_SIGNATURES["stcg01"] = ["int"]
SPICE_RETURNS   ["stcg01"] = 4*["float"] + ["int", "string", "float"]
SPICE_DOCSTRINGS["stcg01"] = """
Get data for a single star from a SPICE type 1 star catalog.

stcg01(<int> index) -> [<float> ra, <float> dec,
                        <float> rasig, <float> decsig,
                        <int> catnum, <string> sptype, <float> vmag]

index  = Star index.
ra     = Right ascension in radians.
dec    = Declination in radians.
ras    = Right ascension uncertainty in radians.
decs   = Declination uncertainty in radians.
catnum = Catalog number.
sptype = Spectral type.
vmag   = Visual magnitude.
"""

#########################################
SPICE_SIGNATURES["stcl01"] = ["string"]
SPICE_RETURNS   ["stcl01"] = ["string", "int"]
SPICE_DOCSTRINGS["stcl01"] = """
Load SPICE type 1 star catalog and return the catalog's table name.

stcl01(<string> catfnm) -> [<string> tabnam, <int> handle]

catfnm = Catalog file name.
tabnam = Catalog table name.
handle = Catalog file handle.
"""

#########################################
SPICE_SIGNATURES["stelab"] = 2*["float[3]"]
SPICE_RETURNS   ["stelab"] = ["float[3]"]
SPICE_DOCSTRINGS["stelab"] = """
Correct the apparent position of an object for stellar aberration.

stelab(<float[3]> pobj, <float[3]> vobs) -> <float[3]> appobj

pobj   = Position of an object with respect to the observer.
vobs   = Velocity of the observer with respect to the Solar System
         barycenter.
appobj = Apparent position of the object with respect to the observer,
         corrected for stellar aberration.
"""

#########################################
SPICE_SIGNATURES["stlabx"] = 2*["float[3]"]
SPICE_RETURNS   ["stlabx"] = ["float[3]"]
SPICE_DOCSTRINGS["stlabx"] = """
Correct the position of a target for the stellar aberration effect on
radiation transmitted from a specified observer to the target.

stlabx_(<float[3]> pobj, <float[3]> vobs) -> <float[3]> corpos

pobj   = Position of an object with respect to the observer.
vobs   = Velocity of the observer with respect to the Solar System
         barycenter.
corpos = Corrected position of the object.
"""

#########################################
SPICE_SIGNATURES["stpool"] = ["string", "int", "string"]
SPICE_RETURNS   ["stpool"] = ["string", "bool"]
SPICE_DOCSTRINGS["stpool"] = """
Retrieve the nth string from the kernel pool variable, where the string may
be continued across several components of the kernel pool variable.

stpool(<string> item, <int> nth, <string> contin) -> [<string> string,
                                                      <bool> found]

item   = Name of the kernel pool variable.
nth    = Index of the full string to retrieve.
contin = Character sequence used to indicate continuation.
lenout = Available space in output string.
string = A full string concatenated across continuations.
size   = The number of characters in the full string value.
found  = True indicating success of request; False on failure.
"""

SPICE_SIGNATURES["stpool_error"] = ["string", "int", "string"]
SPICE_RETURNS   ["stpool_error"] = ["string"]
SPICE_DOCSTRINGS["stpool_error"] = """
Retrieve the nth string from the kernel pool variable, where the string may
be continued across several components of the kernel pool variable.

stpool(<string> item, <int> nth, <string> contin) -> <string> string

item   = Name of the kernel pool variable.
nth    = Index of the full string to retrieve.
contin = Character sequence used to indicate continuation.
lenout = Available space in output string.
string = A full string concatenated across continuations.
size   = The number of characters in the full string value.

Raise KeyError if request failed.
"""

#########################################
SPICE_SIGNATURES["str2et"] = ["string"]
SPICE_RETURNS   ["str2et"] = ["float"]
SPICE_DOCSTRINGS["str2et"] = """
Convert a string representing an epoch to a double precision value
representing the number of TDB seconds past the J2000 epoch corresponding
to the input epoch.

str2et(<string> str) -> <float> et

str = A string representing an epoch.
et  = The equivalent value in seconds past J2000, TDB.
"""

#########################################
SPICE_SIGNATURES["subpnt"] = ["string", "body_name", "float", "frame_name",
                              "string", "body_name"]
SPICE_RETURNS   ["subpnt"] = ["float[3]", "float", "float[3]"]
SPICE_DOCSTRINGS["subpnt"] = """
Compute the rectangular coordinates of the sub-observer point on a target
body at a specified epoch, optionally corrected for light time and stellar
aberration.

The surface of the target body may be represented by a triaxial ellipsoid
or by topographic data provided by DSK files.

This routine supersedes subpt.

subpnt(<string> method, <string> target, <float> et, <string> fixref,
       <string> abcorr, <string> obsrvr) ->
                    [<float[3]> spoint, <float> trgepc, <float[3]> srfvec]

method = Computation method.
target = Name of target body.
et     = Epoch in TDB seconds past J2000 TDB.
fixref = Body-fixed, body-centered target body frame.
abcorr = Aberration correction flag.
obsrvr = Name of observing body.
spoint = Sub-observer point on the target body.
trgepc = Sub-observer point epoch.
srfvec = Vector from observer to sub-observer point.
"""

#########################################
SPICE_SIGNATURES["subpt"] = ["string", "body_name", "float", "string",
                             "body_name"]
SPICE_RETURNS   ["subpt"] = ["float[3]", "float"]
SPICE_DOCSTRINGS["subpt"] = """
Compute the rectangular coordinates of the sub-observer point on a target
body at a particular epoch, optionally corrected for planetary (light time)
and stellar aberration.  Return these coordinates expressed in the
body-fixed frame associated with the target body.  Also, return the
observer's altitude above the target body.

subpt(<string> method, <string> target, <float> et,
      <string> abcorr, <string> obsrvr) -> [<float[3]> spoint, <float> alt]

method = Computation method.
target = Name of target body.
et     = Epoch in ephemeris seconds past J2000 TDB.
abcorr = Aberration correction.
obsrvr = Name of observing body.
spoint = Sub-observer point on the target body.
alt    = Altitude of the observer above the target body.
"""

#########################################
SPICE_SIGNATURES["subslr"] = ["string", "body_name", "float", "string",
                              "body_name"]
SPICE_RETURNS   ["subslr"] = ["float[3]", "float", "float[3]"]
SPICE_DOCSTRINGS["subslr"] = """
Compute the rectangular coordinates of the sub-solar point on a target body
at a specified epoch, optionally corrected for light time and stellar
aberration.

The surface of the target body may be represented by a triaxial ellipsoid
or by topographic data provided by DSK files.

This routine supersedes subsol.

subslr(<string> method, <string> target, <float> et, <string> fixref,
       <string> abcorr, <string> obsrvr) ->
                    [<float[3]> spoint, <float> trgepc, <float[3]> srfvec]

method = Computation method.
target = Name of target body.
et     = Epoch in ephemeris seconds past J2000 TDB.
fixref = Body-fixed, body-centered target body frame.
abcorr = Aberration correction.
obsrvr = Name of observing body.
spoint = Sub-solar point on the target body.
trgepc = Sub-solar point epoch.
srfvec = Vector from observer to sub-solar point.
"""

#########################################
SPICE_SIGNATURES["subsol"] = ["string", "body_name", "float", "string",
                              "body_name"]
SPICE_RETURNS   ["subsol"] = ["float[3]"]
SPICE_DOCSTRINGS["subsol"] = """
Determine the coordinates of the sub-solar point on a target body as seen
by a specified observer at a specified epoch, optionally corrected for
planetary (light time) and stellar aberration.

subsol(<string> method, <string> target, <float> et,
       <string> abcorr, <string> obsrvr) -> <float[3]> spoint

method = Computation method.
target = Name of target body.
et     = Epoch in ephemeris seconds past J2000 TDB.
abcorr = Aberration correction.
obsrvr = Name of observing body.
spoint = Sub-solar point on the target body.
"""

#########################################
SPICE_SIGNATURES["surfnm"] = 3*["float"] + ["float[3]"]
SPICE_RETURNS   ["surfnm"] = ["float[3]"]
SPICE_DOCSTRINGS["surfnm"] = """
This routine computes the outward-pointing, unit normal vector from a point
on the surface of an ellipsoid.

surfnm(<float> a, <float> b, <float> c,
                             <float[3]> point) -> <float[3]> normal

a      = Length of the ellisoid semi-axis along the x-axis.
b      = Length of the ellisoid semi-axis along the y-axis.
c      = Length of the ellisoid semi-axis along the z-axis.
point  = Body-fixed coordinates of a point on the ellipsoid
normal = Outward pointing unit normal to ellipsoid at point
"""

#########################################
SPICE_SIGNATURES["surfpt"] = 2*["float[3]"] + 3*["float"]
SPICE_RETURNS   ["surfpt"] = ["float[3]", "bool"]
SPICE_DOCSTRINGS["surfpt"] = """
Determine the intersection of a line-of-sight vector with the surface of an
ellipsoid.

surfpt(<float[3]> positn, <float[3]> u,
       <float> a, <float> b, <float> c) -> [<float[3]> point, <bool> found]

positn = Position of the observer in body-fixed frame.
u      = Vector from the observer in some direction.
a      = Length of the ellipsoid semi-axis along the x-axis.
b      = Length of the ellipsoid semi-axis along the y-axis.
c      = Length of the ellipsoid semi-axis along the z-axis.
point  = Point on the ellipsoid pointed to by u.
found  = Flag indicating if u points at the ellipsoid.
"""

#########################################
SPICE_SIGNATURES["surfpv"] = 2*["float[6]"] + 3*["float"]
SPICE_RETURNS   ["surfpv"] = ["float[6]", "bool"]
SPICE_DOCSTRINGS["surfpv"] = """
Find the state (position and velocity) of the surface intercept defined by a
specified ray, ray velocity, and ellipsoid.

surfpv(<float[6]> stvrtx, <float[6]> stdir,
       <float> a, <float> b, <float> c) -> [<float[6]> stx, <bool> found]

stvrtx = State of ray's vertex.
stdir  = State of ray's direction vector.
a      = Length of ellipsoid semi-axis along the x-axis.
b      = Length of ellipsoid semi-axis along the y-axis.
c      = Length of ellipsoid semi-axis along the z-axis.
stx    = State of surface intercept.
found  = Flag indicating whether intercept state was found.
"""

#########################################
SPICE_SIGNATURES["sxform"] = ["frame_name", "frame_name", "float"]
SPICE_RETURNS   ["sxform"] = ["float[6,6]"]
SPICE_DOCSTRINGS["sxform"] = """
Return the state transformation matrix from one frame to another at a
specified epoch.

sxform(<string> from, <string> to, <float> et) -> <float[6,6]> xform

from  = Name of the frame to transform from.
to    = Name of the frame to transform to.
et    = Epoch of the state transformation matrix.
xform = A state transformation matrix.
"""

SPICE_SIGNATURES["sxform_vector"] = ["frame_name", "frame_name", "float"]
SPICE_RETURNS   ["sxform_vector"] = ["float[*,6,6]"]
SPICE_DOCSTRINGS["sxform_vector"] = """
Return the state transformation matrix from one frame to another at a
specified epoch.

This vector version handles an array of et values.

sxform(<string> from, <string> to, <float[*]> et) -> <float[*,6,6]> xform

from  = Name of the frame to transform from.
to    = Name of the frame to transform to.
et    = Epoch of the state transformation matrix.
xform = A state transformation matrix.
"""

#########################################
SPICE_SIGNATURES["timdef"] = ["string", "string"]
SPICE_RETURNS   ["timdef"] = ["string"]
SPICE_DOCSTRINGS["timdef"] = """
Set and retrieve the defaults associated with calendar input strings.

timdef(<string> action, <string> item) -> <string> value

action = is the kind of action to take "SET" or "GET".
item   = is the default item of interest.
value  = is the value associated with the default item.
"""

#########################################
SPICE_SIGNATURES["timout"] = ["float", "string"]
SPICE_RETURNS   ["timout"] = ["string"]
SPICE_DOCSTRINGS["timout"] = """
This routine converts an input epoch represented in TDB seconds past the
TDB epoch of J2000 to a character string formatted to the specifications of
a user's format picture.

timout(<float> et, <string> pictur) -> <string> output

et     = An epoch in seconds past the ephemeris epoch J2000.
pictur = A format specification for the output string.
output = A string representation of the input epoch.
"""

#########################################
SPICE_SIGNATURES["tipbod"] = ["frame_code", "body_code", "float"]
SPICE_RETURNS   ["tipbod"] = ["float[3,3]"]
SPICE_DOCSTRINGS["tipbod"] = """
Return a 3x3 matrix that transforms positions in inertial coordinates to
positions in body-equator-and-prime-meridian coordinates.

tipbod(<int> ref, <int> body, <float> et) -> <float[3,3]> tipm

ref  = ID of inertial reference frame to transform from.
body = ID code of body.
et   = Epoch of transformation.
tipm = Transformation (position), inertial to prime meridian.
"""

#########################################
SPICE_SIGNATURES["tisbod"] = ["frame_code", "body_code", "float"]
SPICE_RETURNS   ["tisbod"] = ["float[6,6]"]
SPICE_DOCSTRINGS["tisbod"] = """
Return a 6x6 matrix that transforms states in inertial coordinates to
states in body-equator-and-prime-meridian coordinates.

tisbod(<int> ref, <int> body, <float> et) -> <float[6,6]> tsipm

ref   = ID of inertial reference frame to transform from
body  = ID code of body
et    = Epoch of transformation
tsipm = Transformation (state), inertial to prime meridian
"""

#########################################
SPICE_SIGNATURES["tkvrsn"] = ["string"]
SPICE_RETURNS   ["tkvrsn"] = ["string"]
SPICE_DOCSTRINGS["tkvrsn"] = """
Given an item such as the Toolkit or an entry point name, return the latest
version string.

tkvrsn(<string> item) -> <string> value

item  = Item for which a version string is desired.
value = A version string.
"""

#########################################
SPICE_SIGNATURES["tparse"] = ["string"]
SPICE_RETURNS   ["tparse"] = ["float"]
SPICE_DOCSTRINGS["tparse"] = """
Parse a time string and return seconds past the J2000 epoch on a formal
calendar.

tparse(<string> string) -> <float> sp2000
"""

#########################################
SPICE_SIGNATURES["tpictr"] = ["string"]
SPICE_RETURNS   ["tpictr"] = ["string"]
SPICE_DOCSTRINGS["tpictr"] = """
Given a sample time string, create a time format picture suitable for use
by the routine timout.

tpictr(<string> sample) -> <string> pictur

sample = A sample time string.
pictur = A format picture that describes sample.

Raise SyntaxError on error.
"""

#########################################
SPICE_SIGNATURES["trace"] = ["float[3,3]"]
SPICE_RETURNS   ["trace"] = ["float"]
SPICE_DOCSTRINGS["trace"] = """
Return the trace of a 3x3 matrix.

trace(<float[3,3]> matrix) -> <float> trace

matrix = 3x3 matrix of double precision numbers.
trace  = The trace of the matrix.
"""

#########################################
SPICE_SIGNATURES["trcoff"] = []
SPICE_RETURNS   ["trcoff"] = []
SPICE_DOCSTRINGS["trcoff"] = """
Disable tracing.

trcoff()
"""

#########################################
SPICE_SIGNATURES["trcdep"] = []
SPICE_RETURNS   ["trcdep"] = ["int"]
SPICE_DOCSTRINGS["trcdep"] = """
Return the number of modules in the traceback representation.

trcdep() -> <int> depth

depth = The number of modules in the traceback.
"""

#########################################
SPICE_SIGNATURES["tsetyr"] = ["int"]
SPICE_RETURNS   ["tsetyr"] = []
SPICE_DOCSTRINGS["tsetyr"] = """
Set the lower bound on the 100 year range.

tsetyr(<int> year)

year = Lower bound on the 100 year interval of expansion
"""

#########################################
SPICE_SIGNATURES["twopi"] = []
SPICE_RETURNS   ["twopi"] = ["float"]
SPICE_DOCSTRINGS["twopi"] = """
Return twice the value of pi.

twopi() -> <float> value
"""

#########################################
SPICE_SIGNATURES["twovec"] = 2*["float[3]", "int"]
SPICE_RETURNS   ["twovec"] = ["float[3,3]"]
SPICE_DOCSTRINGS["twovec"] = """
Find the transformation to the right-handed frame having a given vector as
a specified axis and having a second given vector lying in a specified
coordinate plane.

twovec(<float[3]> axdef, <int> indexa,
       <float[3]> plndef, <int> indexp) -> <float[3,3]> mout

axdef  = Vector defining a principal axis.
indexa = Principal axis number of axdef (X=1, Y=2, Z=3).
plndef = Vector defining (with axdef) a principal plane.
indexp = Second axis number (with indexa) of principal plane.
mout   = Output rotation matrix.
"""

#########################################
SPICE_SIGNATURES["tyear"] = []
SPICE_RETURNS   ["tyear"] = ["float"]
SPICE_DOCSTRINGS["tyear"] = """
Return the number of seconds in a tropical year.

tyear() -> <float> value
"""

#########################################
SPICE_SIGNATURES["ucrss"] = 2*["float[3]"]
SPICE_RETURNS   ["ucrss"] = ["float[3]"]
SPICE_DOCSTRINGS["ucrss"] = """
Compute the normalized cross product of two 3-vectors.

ucrss(<float[3]> v1, <float[3]> v2) -> <float[3]> vout

v1   = Left vector for cross product.
v2   = Right vector for cross product.
vout = Normalized cross product (v1xv2) / |v1xv2|.
"""

#########################################
SPICE_SIGNATURES["unitim"] = ["float", "string", "string"]
SPICE_RETURNS   ["unitim"] = ["float"]
SPICE_DOCSTRINGS["unitim"] = """
Transform time from one uniform scale to another.  The uniform time scales
are TAI, TDT, TDB, <float> et, JED, JDTDB, JDTDT.

unitim(<float> epoch, <string> insys, <string> outsys) -> <float> value

epoch  = An epoch to be converted.
insys  = The time scale associated with the input epoch.
outsys = The time scale associated with the function value.
value  = the value in outsys that is equivalent to the epoch on the insys
         time scale.
"""

#########################################
SPICE_SIGNATURES["unload"] = ["string"]
SPICE_RETURNS   ["unload"] = []
SPICE_DOCSTRINGS["unload"] = """
Unload a SPICE kernel.

unload(<string> file)

file = The name of a kernel to unload.
"""

#########################################
SPICE_SIGNATURES["unorm"] = ["float[3]"]
SPICE_RETURNS   ["unorm"] = ["float[3]", "float"]
SPICE_DOCSTRINGS["unorm"] = """
Normalize a double precision 3-vector and return its magnitude.

unorm(<float[3]> v1) -> [<float[3]> vout, <float> vmag]

v1   = Vector to be normalized.
vout = Unit vector v1 / |v1|.
vmag = Magnitude of v1, i.e. |v1|.

If v1 is the zero vector, then vout will also be zero.
"""

#########################################
SPICE_SIGNATURES["unormg"] = ["float[*]"]
SPICE_RETURNS   ["unormg"] = ["float[*]", "float"]
SPICE_DOCSTRINGS["unormg"] = """
Normalize a double precision vector of arbitrary dimension and return its
magnitude.

unormg(<float[*]> v1) -> [<float[*]> vout, <float[*]> vmag]

v1   = Vector to be normalized.
vout = Unit vector v1 / |v1|.
vmag = Magnitude of v1, that is, |v1|.

If v1 = 0, vout will also be zero.
"""

#########################################
SPICE_SIGNATURES["utc2et"] = ["string"]
SPICE_RETURNS   ["utc2et"] = ["float"]
SPICE_DOCSTRINGS["utc2et"] = """
Convert an input time from Calendar or Julian Date format, UTC, to
ephemeris seconds past J2000.

utc2et(<string> utcstr) -> <float> et

utcstr = Input time string, UTC.
et     = Output epoch, ephemeris seconds past J2000.
"""

#########################################
SPICE_SIGNATURES["vadd"] = 2*["float[3]"]
SPICE_RETURNS   ["vadd"] = ["float[3]"]
SPICE_DOCSTRINGS["vadd"] = """
add two 3 dimensional vectors.

vadd(<float[3]> v1, <float[3]> v2) -> <float[3]> vout

v1   = First vector to be added.
v2   = Second vector to be added.
vout = Sum vector, v1 + v2.
"""

#########################################
SPICE_SIGNATURES["vaddg"] = 2*["float[*]"]
SPICE_RETURNS   ["vaddg"] = ["float[*]"]
SPICE_DOCSTRINGS["vaddg"] = """
add two vectors of arbitrary dimension.

vaddg(<float[*]> v1, <float[*]> v2) -> <float[*]> vout

v1   = First vector to be added.
v2   = Second vector to be added.
vout = Sum vector, v1 + v2.
"""

#########################################
SPICE_SIGNATURES["vcrss"] = 2*["float[3]"]
SPICE_RETURNS   ["vcrss"] = ["float[3]"]
SPICE_DOCSTRINGS["vcrss"] = """
Compute the cross product of two 3-dimensional vectors.

vcrss(<float[3]> v1, <float[3]> v2) -> <float[3]> vout

v1   = Left hand vector for cross product.
v2   = Right hand vector for cross product.
vout = Cross product v1xv2.
"""

#########################################
SPICE_SIGNATURES["vdist"] = 2*["float[3]"]
SPICE_RETURNS   ["vdist"] = ["float"]
SPICE_DOCSTRINGS["vdist"] = """
Return the distance between two three-dimensional vectors.

vdist(<float[3]> v1, <float[3]> v2) -> <float> dist

v1, v2 = Two 3-vectors.
dist   = The distance between v1 and v2.
"""

#########################################
SPICE_SIGNATURES["vdistg"] = 2*["float[*]"]
SPICE_RETURNS   ["vdistg"] = ["float"]
SPICE_DOCSTRINGS["vdistg"] = """
Return the distance between two vectors of arbitrary dimension.

vdistg(<float[*]> v1, <float[*]> v2) -> <float> dist

v1, v2 = Two vectors of arbitrary dimension.
dist   = The distance between v1 and v2.
"""

#########################################
SPICE_SIGNATURES["vdot"] = 2*["float[3]"]
SPICE_RETURNS   ["vdot"] = ["float"]
SPICE_DOCSTRINGS["vdot"] = """
Compute the dot product of two double precision, 3-dimensional vectors.

vdot(<float[3]> v1, <float[3]> v2) -> <float> value

v1     = First vector in the dot product.
v2    = Second vector in the dot product.
value = The value of the dot product of v1 and v2.
"""

#########################################
SPICE_SIGNATURES["vdotg"] = 2*["float[*]"]
SPICE_RETURNS   ["vdotg"] = ["float"]
SPICE_DOCSTRINGS["vdotg"] = """
Compute the dot product of two vectors of arbitrary dimension.

vdotg(<float[*]> v1, <float[*]> v2) -> <float[*]> value

v1    = First vector in the dot product.
v2    = Second vector in the dot product.
value = The value of the dot product of v1 and v2.
"""

#########################################
SPICE_SIGNATURES["vequ"] = ["float[3]"]
SPICE_RETURNS   ["vequ"] = ["float[3]"]
SPICE_DOCSTRINGS["vequ"] = """
Make one double precision 3-dimensional vector equal to another.

vequ(<float[3]> vin) -> <float[3]> vout

vin  = 3-dimensional double precision vector.
vout = 3-dimensional double precision vector set equal to vin.
"""

#########################################
SPICE_SIGNATURES["vequg"] = ["float[*]"]
SPICE_RETURNS   ["vequg"] = ["float[*]"]
SPICE_DOCSTRINGS["vequg"] = """
Make one double precision vector of arbitrary dimension equal to another.

vequg(<float[*]> vin) -> <float[*]> vout

vin  = double precision vector.
vout = double precision vector set equal to vin.
"""

#########################################
SPICE_SIGNATURES["vhat"] = ["float[3]"]
SPICE_RETURNS   ["vhat"] = ["float[3]"]
SPICE_DOCSTRINGS["vhat"] = """
Find the unit vector along a double precision 3-dimensional vector.

vhat(<float[3]> v1) -> <float[3]> vout

v1   = Vector to be unitized.
vout = Unit vector v1 / |v1|.
"""

#########################################
SPICE_SIGNATURES["vhatg"] = ["float[*]"]
SPICE_RETURNS   ["vhatg"] = ["float[*]"]
SPICE_DOCSTRINGS["vhatg"] = """
Find the unit vector along a double precision vector of arbitrary dimension.

vhatg(<float[*]> v1) -> <float[*]> vout

v1   = Vector to be normalized.
vout = Unit vector v1 / |v1|.

If v1 = 0, vout will also be zero.
"""

#########################################
SPICE_SIGNATURES["vlcom3"] = 3*["float", "float[3]"]
SPICE_RETURNS   ["vlcom3"] = ["float[3]"]
SPICE_DOCSTRINGS["vlcom3"] = """
This subroutine computes the vector linear combination
a*v1 + b*v2 + c*v3 of double precision, 3-dimensional vectors.

vlcom3(<float> a, <float[3]> v1,
       <float> b, <float[3]> v2,
       <float> c, <float[3]> v3) -> <float[3]> sum

a    = Coefficient of v1
v1   = Vector in 3-space
b    = Coefficient of v2
v2   = Vector in 3-space
c    = Coefficient of v3
v3   = Vector in 3-space
sum = Linear Vector Combination a*v1 + b*v2 + c*v3
"""

#########################################
SPICE_SIGNATURES["vlcom"] = 2*["float", "float[3]"]
SPICE_RETURNS   ["vlcom"] = ["float[3]"]
SPICE_DOCSTRINGS["vlcom"] = """
Compute a vector linear combination of two double precision, 3-dimensional
vectors.

vlcom(<float> a, <float[3]> v1, <float> b, <float[3]> v2) -> <float[3]> sum

a   = Coefficient of v1
v1  = Vector in 3-space
b   = Coefficient of v2
v2  = Vector in 3-space
sum = Linear Vector Combination a*v1 + b*v2
"""

#########################################
SPICE_SIGNATURES["vlcomg"] = 2*["float", "float[*]"]
SPICE_RETURNS   ["vlcomg"] = ["float[*]"]
SPICE_DOCSTRINGS["vlcomg"] = """
Compute a vector linear combination of two double precision vectors of
arbitrary dimension.

vlcomg(<float> a, <float[*]> v1,
       <float> b, <float[*]> v2) -> <float[*]> sum

a   = Coefficient of v1
v1  = Vector in n-space
b   = Coefficient of v2
v2  = Vector in n-space
sum = Linear Vector Combination a*v1 + b*v2
"""

#########################################
SPICE_SIGNATURES["vminug"] = ["float[*]"]
SPICE_RETURNS   ["vminug"] = ["float[*]"]
SPICE_DOCSTRINGS["vminug"] = """
Negate a double precision vector of arbitrary dimension.

vminug(<float[*]> vin) -> <float[*]> vout

vin  = ndim-dimensional double precision vector to be negated.
vout = ndouble precision vector equal to -vin.
"""

#########################################
SPICE_SIGNATURES["vminus"] = ["float[3]"]
SPICE_RETURNS   ["vminus"] = ["float[3]"]
SPICE_DOCSTRINGS["vminus"] = """
Negate a double precision 3-dimensional vector.

vminus(<float[3]> v1) -> <float[3]> vout

v1   =  Vector to be negated.
vout = Negated vector -v1.
"""

#########################################
SPICE_SIGNATURES["vnorm"] = ["float[3]"]
SPICE_RETURNS   ["vnorm"] = ["float"]
SPICE_DOCSTRINGS["vnorm"] = """
Compute the magnitude of a double precision, 3-dimensional vector.

vnorm(<float[3]> v1) -> <float> value

v1    = Vector whose magnitude is to be found.
value = The norm of v1.
"""

#########################################
SPICE_SIGNATURES["vnormg"] = ["float[*]"]
SPICE_RETURNS   ["vnormg"] = ["float"]
SPICE_DOCSTRINGS["vnormg"] = """
Compute the magnitude of a double precision vector of arbitrary dimension.

vnormg(<float[*]> v1) -> <float> value

v1    = Vector whose magnitude is to be found.
value = The norm of v1.
"""

#########################################
SPICE_SIGNATURES["vpack"] = 3*["float"]
SPICE_RETURNS   ["vpack"] = ["float[3]"]
SPICE_DOCSTRINGS["vpack"] = """
Pack three scalar components into a vector.

vpack(<float> x, <float> y, <float> z) -> <float[3]> v

x, y, z = Scalar components of a 3-vector.
v       = Equivalent 3-vector.
"""

#########################################
SPICE_SIGNATURES["vperp"] = 2*["float[3]"]
SPICE_RETURNS   ["vperp"] = ["float[3]"]
SPICE_DOCSTRINGS["vperp"] = """
Find the component of a vector that is perpendicular to a second vector. 
All vectors are 3-dimensional.

vperp(<float[3]> a, <float[3]> b) -> <float[3]> p

a = The vector whose orthogonal component is sought.
b = The vector used as the orthogonal reference.
p = The component of a orthogonal to b.
"""

#########################################
SPICE_SIGNATURES["vprjp"] = ["float[3]", "float[4]"]
SPICE_RETURNS   ["vprjp"] = ["float[3]"]
SPICE_DOCSTRINGS["vprjp"] = """
Project a vector onto a specified plane, orthogonally.

vprjp(<float[3]> vin, <float[4]> plane) -> <float[3]> vout

vin   = Vector to be projected.
plane = A CSPICE plane onto which vin is projected.
vout  = Vector resulting from projection.
"""

#########################################
SPICE_SIGNATURES["vprjpi"] = ["float[3]", "float[4]", "float[4]"]
SPICE_RETURNS   ["vprjpi"] = ["float[3]", "bool"]
SPICE_DOCSTRINGS["vprjpi"] = """
Find the vector in a specified plane that maps to a specified vector in
another plane under orthogonal projection.

vprjpi(<float[3]> vin, projpl, invpl) -> [<float[3]> vout, <bool> found]

vin    = The projected vector.
projpl = Plane containing vin.
invpl  = Plane containing inverse image of vin.
vout   = Inverse projection of vin.
found  = Flag indicating whether vout could be calculated.
"""

#########################################
SPICE_SIGNATURES["vproj"] = ["float[3]", "float[3]"]
SPICE_RETURNS   ["vproj"] = ["float[3]"]
SPICE_DOCSTRINGS["vproj"] = """
Find the projection of one vector onto another vector. All vectors are
3-dimensional.

vproj(<float[3]> a, <float[3]> b) -> <float[3]> p

a = The vector to be projected.
b = The vector onto which a is to be projected.
p = The projection of a onto b.
"""

#########################################
SPICE_SIGNATURES["vrel"] = ["float[3]", "float[3]"]
SPICE_RETURNS   ["vrel"] = ["float"]
SPICE_DOCSTRINGS["vrel"] = """
Return the relative difference between two 3-dimensional vectors.

vrel(<float[3]> v1, <float[3]> v2) -> <float> value

v1, v2 = Input vectors.
value  = The relative difference.
"""

#########################################
SPICE_SIGNATURES["vrelg"] = ["float[*]", "float[*]"]
SPICE_RETURNS   ["vrelg"] = ["float"]
SPICE_DOCSTRINGS["vrelg"] = """
Return the relative difference between two vectors of general dimension.

vrelg(<float[*]> v1, <float[*]> v2) -> <float> value

v1, v2 = Input vectors.
value  = The relative difference.
"""

#########################################
SPICE_SIGNATURES["vrotv"] = ["float[3]", "float[3]", "float"]
SPICE_RETURNS   ["vrotv"] = ["float[3]"]
SPICE_DOCSTRINGS["vrotv"] = """
Rotate a vector about a specified axis vector by a specified angle and
return the rotated vector.

vrotv(<float[3]> v, <float[3]> axis, <float> theta) -> <float[3]> r

v     = Vector to be rotated.
axis  = Axis of the rotation.
theta = Angle of rotation (radians).
r     = Result of rotating v about axis by theta.
"""

#########################################
SPICE_SIGNATURES["vscl"] = ["float", "float[3]"]
SPICE_RETURNS   ["vscl"] = ["float[3]"]
SPICE_DOCSTRINGS["vscl"] = """
Multiply a scalar and a 3-dimensional double precision vector.

vscl(<float> s, <float[3]> v1) -> <float[3]> vout

s    = Scalar to multiply a vector.
v1   = Vector to be multiplied.
vout = Product vector, s*v1. vout can overwrite v1.
"""

#########################################
SPICE_SIGNATURES["vsclg"] = ["float", "float[*]"]
SPICE_RETURNS   ["vsclg"] = ["float[*]"]
SPICE_DOCSTRINGS["vsclg"] = """
Multiply a scalar and a double precision vector of arbitrary dimension.

vsclg(<float> s, <float[*]> v1) -> <float[*]> vout

s    = Scalar to multiply a vector.
v1   = Vector to be multiplied.
vout = Product vector, s*v1. vout can overwrite v1.
"""

#########################################
SPICE_SIGNATURES["vsep"] = ["float[3]", "float[3]"]
SPICE_RETURNS   ["vsep"] = ["float"]
SPICE_DOCSTRINGS["vsep"] = """
Find the separation angle in radians between two double precision,
3-dimensional vectors.  This angle is defined as zero if either vector is
zero.

vsep(<float[3]> v1, <float[3]> v2) -> <float> value

v1    = First vector.
v2    = Second vector.
value = The separation angle in radians.
"""

#########################################
SPICE_SIGNATURES["vsepg"] = ["float[*]", "float[*]"]
SPICE_RETURNS   ["vsepg"] = ["float"]
SPICE_DOCSTRINGS["vsepg"] = """
Find the separation angle in radians between two double precision vectors
of arbitrary dimension. This angle is defined as zero if either vector is
zero.

vsepg(<float[*]> v1, <float[*]> v2) -> <float[*]> value

v1    = First vector.
v2    = Second vector.
value = The separation angle in radians.
"""

#########################################
SPICE_SIGNATURES["vsub"] = ["float[3]", "float[3]"]
SPICE_RETURNS   ["vsub"] = ["float[3]"]
SPICE_DOCSTRINGS["vsub"] = """
Compute the difference between two 3-dimensional, double precision vectors.

vsub(<float[3]> v1, <float[3]> v2) -> <float[3]> vout

v1   = First vector (minuend).
v2   = Second vector (subtrahend).
vout = Difference vector, v1 - v2.
"""

#########################################
SPICE_SIGNATURES["vsubg"] = ["float[*]", "float[*]"]
SPICE_RETURNS   ["vsubg"] = ["float[*]"]
SPICE_DOCSTRINGS["vsubg"] = """
Compute the difference between two double precision vectors of arbitrary
dimension.

vsubg(<float[*]> v1, <float[*]> v2) -> <float[*]> vout

v1   = First vector (minuend).
v2   = Second vector (subtrahend).
vout = Difference vector, v1 - v2.
"""

#########################################
SPICE_SIGNATURES["vtmv"] = ["float[3]", "float[3,3]", "float[3]"]
SPICE_RETURNS   ["vtmv"] = ["float"]
SPICE_DOCSTRINGS["vtmv"] = """
Multiply the transpose of a 3-dimensional column vector, a 3x3 matrix, and
a 3-dimensional column vector.

vtmv(<float[3]> v1, <float[3,3]> matrix, <float[3]> v2) -> <float> value

v1     = 3 dimensional double precision column vector.
matrix = 3x3 double precision matrix.
v2     = 3 dimensional double precision column vector.
value  = The result of (v1**t * matrix * v2).
"""

#########################################
SPICE_SIGNATURES["vtmvg"] = ["float[*]", "float[*,*]", "float[*]"]
SPICE_RETURNS   ["vtmvg"] = ["float"]
SPICE_DOCSTRINGS["vtmvg"] = """
Multiply the transpose of a n-dimensional column vector, a nxm matrix, and
a m-dimensional column vector.

vtmvg(<float[*]> v1, <float[*,*]> matrix,
                     <float[*]> v2) -> <float[*]> value

v1     = n-dimensional double precision column vector.
matrix = nxm double precision matrix.
v2     = m-dimensional double porecision column vector.
value  = The result of (v1**t * matrix * v2).
"""

#########################################
SPICE_SIGNATURES["vupack"] = ["float[3]"]
SPICE_RETURNS   ["vupack"] = 3*["float"]
SPICE_DOCSTRINGS["vupack"] = """
Unpack three scalar components from a vector.

vupack(<float[3]> v) -> [<float> x, <float> y, <float> z]

v       = 3-vector.
x, y, z = Scalar components of 3-vector.
"""

#########################################
SPICE_SIGNATURES["vzero"] = ["float[3]"]
SPICE_RETURNS   ["vzero"] = ["bool"]
SPICE_DOCSTRINGS["vzero"] = """
Indicate whether a 3-vector is the zero vector.

vzero(<float[3]> v) -> <bool> value

v     = Vector to be tested.
value = True if and only if v is the zero vector.
"""

#########################################
SPICE_SIGNATURES["vzerog"] = ["float[*]"]
SPICE_RETURNS   ["vzerog"] = ["bool"]
SPICE_DOCSTRINGS["vzerog"] = """
Indicate whether a general-dimensional vector is the zero vector.

vzerog(<float[*]> v) -> <bool> value

v     = Vector to be tested.
value = True if and only if v is the zero vector.
"""

#########################################
SPICE_SIGNATURES["xf2eul"] = ["float[6,6]"] + 3*["int"]
SPICE_RETURNS   ["xf2eul"] = ["float[3]", "bool"]
SPICE_DOCSTRINGS["xf2eul"] = """
Convert a state transformation matrix to Euler angles and their derivatives
with respect to a specified set of axes. The companion routine eul2xf
converts Euler angles and their derivatives with respect to a specified set
of axes to a state transformation matrix.

xf2eul(<float[6,6]> xform, <int> axisa, <int> axisb, <int> axisc) ->
                                [<float[6]> eulang, <bool> unique]

xform  = A state transformation matrix.
axisa  = Axis A of the Euler angle factorization.
axisb  = Axis B of the Euler angle factorization.
axisc  = Axis C of the Euler angle factorization.
eulang = An array of Euler angles and their derivatives.
unique = Indicates if eulang is a unique representation.
"""

#########################################
SPICE_SIGNATURES["xf2rav"] = ["float[6,6]"]
SPICE_RETURNS   ["xf2rav"] = ["float[3,3]", "float[3]"]
SPICE_DOCSTRINGS["xf2rav"] = """
This routine determines from a state transformation matrix the associated
rotation matrix and angular velocity of the rotation.

xf2rav(<float[6,6]> xform) -> [<float[3,3]> rot, <float[3]> av]

xform = a state transformation matrix.
rot   = the rotation associated with xform.
av    = the angular velocity associated with xform.
"""

#########################################
SPICE_SIGNATURES["xpose6"] = ["float[6,6]"]
SPICE_RETURNS   ["xpose6"] = ["float[6,6]"]
SPICE_DOCSTRINGS["xpose6"] = """
Transpose a 6x6 matrix.

xpose6(<float[6,6]> m1) -> <float[6,6]> mout

m1   = 6x6 matrix to be transposed.
mout = Transpose of m1.
"""

#########################################
SPICE_SIGNATURES["xpose"] = ["float[3,3]"]
SPICE_RETURNS   ["xpose"] = ["float[3,3]"]
SPICE_DOCSTRINGS["xpose"] = """
Transpose a 3x3 matrix.

xpose(<float[3,3]> m1) -> <float[3,3]> mout

m1   = 3x3 matrix to be transposed.
mout = Transpose of m1.
"""

#########################################
SPICE_SIGNATURES["xposeg"] = ["float[*,*]"]
SPICE_RETURNS   ["xposeg"] = ["float[*,*]"]
SPICE_DOCSTRINGS["xposeg"] = """
Transpose a matrix of arbitrary size (in place, the matrix need not be
square).

xposeg(<float[*,*]> matrix) -> <float[*,*]> xposem

matrix = Matrix to be transposed.
xposem = Transposed matrix (xposem can overwrite matrix).
"""
#########################################
