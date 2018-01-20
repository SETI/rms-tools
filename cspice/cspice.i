%module cspice
%{ 
#define SWIG_FILE_WITH_INIT

#include "SpiceUsr.h"
#include "SpiceCel.h"
#include <math.h>
#include <stdio.h>

#define NPLANE 4
#define NELLIPSE 9

/* Define NAN for Microsoft C compiler if necessary */
#ifdef _MSC_VER
#define INFINITY (DBL_MAX+DBL_MAX)
#define NAN (INFINITY-INFINITY)
#endif

/* Internal routine to malloc a vector of doubles */
double *my_malloc(int count) {
    double *result = (double *) PyMem_Malloc(count * sizeof(double));
    if (!result) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
        return result;
    }

    return result;
}

/* Internal routine to compare integers for equality */
int my_assert_eq(int a, int b, const char *message) {
    if (a != b) {
        PyErr_SetString(PyExc_ValueError, message);
        return 0;
    }
    return 1;
}

%} 

%include "typemaps.i"
%include "cspice_typemaps.i"

%init %{
        import_array(); /* For numpy interface */
        erract_c("SET", 256, "RETURN");
        errdev_c("SET", 256, "NULL");   /* Suppresses default error messages */
%} 

%feature("autodoc", "1");

/***********************************************************************
* -Procedure axisar_c ( Axis and angle to rotation )
*
* -Abstract
*
* Construct a rotation matrix that rotates vectors by a specified 
* angle about a specified axis. 
*
* void axisar_c (
*       ConstSpiceDouble  axis   [3],
*       SpiceDouble       angle,
*       SpiceDouble       r      [3][3]  ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* axis       I   Rotation axis. 
* angle      I   Rotation angle, in radians. 
* r          O   Rotation matrix corresponding to axis and angle. 
***********************************************************************/

%rename (axisar) axisar_c;

%apply (double  IN_ARRAY1[ANY])      {double axis[3]};
%apply (double OUT_ARRAY2[ANY][ANY]) {double rout[3][3]};
%apply (void RETURN_VOID) {void axisar_c};

extern void axisar_c (
        double axis[3],
        double angle,
        double rout[3][3] );

/***********************************************************************
* -Procedure b1900_c ( Besselian Date 1900.0 )
*
* -Abstract
*
* Return the Julian Date corresponding to Besselian Date 1900.0.
*
* SpiceDouble b1900_c (
        void )
*
* -Brief_I/O
*
* The function returns the Julian Date corresponding to Besselian
* date 1900.0.
***********************************************************************/

%rename (b1900) b1900_c;

extern double b1900_c ( void );

/***********************************************************************
* -Procedure  b1950_c ( Besselian Date 1950.0 )
*
* -Abstract
*
* Return the Julian Date corresponding to Besselian Date 1950.0.
*
* SpiceDouble b1950_c (
        void )
*
* -Brief_I/O
*
* The function returns the Julian Date corresponding to Besselian
* date 1950.0.
***********************************************************************/

%rename (b1950) b1950_c;

extern double b1950_c ( void );

/***********************************************************************
* -Procedure bodc2n_c ( Body ID code to name translation )
*
* -Abstract
*
* Translate the SPICE integer code of a body into a common name
* for that body.
*
* void bodc2n_c (
*       SpiceInt        code,
*       SpiceInt        lenout,
*       SpiceChar     * name,
*       SpiceBoolean  * found   )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* code       I   Integer ID code to be translated into a name.
* lenout     I   Maximum length of output name.
* name       O   A common name for the body identified by code.
* found      O   True if translated, otherwise false.
***********************************************************************/

%rename (bodc2n) bodc2n_c;

%apply (int DIM1, char OUT_STRING[ANY]) {(int lenout, char name[256])};
%apply (void RETURN_VOID) {void bodc2n_c};

extern void bodc2n_c (
        int code,
        int lenout, char name[256],
        int *OUT_BOOLEAN_LOOKUPERROR );

/***********************************************************************
* -Procedure boddef_c ( Body name/ID code definition )
*
* -Abstract
*
* Define a body name/ID code pair for later translation via
* bodn2c_c or bodc2n_c.
*
* void boddef_c (
*       ConstSpiceChar   * name,
*       SpiceInt           code )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* name       I   Common name of some body.
* code       I   Integer code for that body.
***********************************************************************/

%rename (boddef) boddef_c;

%apply (void RETURN_VOID) {void boddef_c};

extern void boddef_c (
        char *CONST_STRING,
        int   code    );

/***********************************************************************
* -Procedure bodfnd_c ( Find values from the kernel pool )
*
* -Abstract
*
* Determine whether values exist for some item for any body
* in the kernel pool.
*
* SpiceBoolean bodfnd_c (
*       SpiceInt           body,
*       ConstSpiceChar   * item )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* body       I   ID code of body.
* item       I   Item to find ("RADII", "NUT_AMP_RA", etc.).
* The function returns the value SPICETRUE if the item is in the
* kernel pool, and is SPICEFALSE if it is not.
***********************************************************************/

%rename (bodfnd) bodfnd_c;

%apply (int RETURN_BOOLEAN) {int bodfnd_c};

extern int bodfnd_c (
        int   body,
        char *CONST_STRING );

/***********************************************************************
* -Procedure bodn2c_c ( Body name to ID code translation )
*
* -Abstract
*
* Translate the name of a body or object to the corresponding SPICE
* integer ID code.
*
* void bodn2c_c (
*       ConstSpiceChar  * name,
*       SpiceInt        * code,
*       SpiceBoolean    * found )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* name       I   Body name to be translated into a SPICE ID code.
* code       O   SPICE integer ID code for the named body.
* found      O   SPICETRUE if translated, otherwise SPICEFALSE.
***********************************************************************/

%rename (bodn2c) bodn2c_c;

%apply (void RETURN_VOID) {void bodn2c_c};

extern void bodn2c_c(
        char *CONST_STRING,
        int *OUTPUT,
        int *OUT_BOOLEAN_KEYERROR);

/***********************************************************************
* -Procedure bods2c_c ( Body string to ID code translation )
*
* -Abstract
*
* Translate a string containing a body name or ID code to an integer
* code.
*
* void bods2c_c (
*       ConstSpiceChar  * name,
*       SpiceInt        * code,
*       SpiceBoolean    * found )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* name       I   String to be translated to an ID code.
* code       O   Integer ID code corresponding to `name'.
* found      O   Flag indicating whether translation succeeded.
***********************************************************************/

%rename (bods2c) bods2c_c;

%apply (void RETURN_VOID) {void bods2c_c};

extern void bods2c_c (
        char *CONST_STRING,
        int *OUTPUT,
        int *OUT_BOOLEAN_KEYERROR );

/***********************************************************************
* -Procedure bodvcd_c ( Return d.p. values from the kernel pool )
*
* -Abstract
*
* Fetch from the kernel pool the double precision values of an item
* associated with a body, where the body is specified by an integer ID
* code.
*
* void bodvcd_c (
*       SpiceInt           bodyid,
*       ConstSpiceChar   * item,
*       SpiceInt           maxn,
*       SpiceInt         * dim,
*       SpiceDouble      * values ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* bodyid     I   Body ID code.
* item       I   Item for which values are desired. ("RADII", 
*                "NUT_PREC_ANGLES", etc. ) 
* maxn       I   Maximum number of values that may be returned. 
* dim        O   Number of values returned. 
* values     O   Values. 
***********************************************************************/

%rename (bodvcd) bodvcd_c;

%apply (int DIM1, int *SIZE1, double OUT_ARRAY1[ANY])
                            {(int maxn, int *dim, double values[80])};
%apply (void RETURN_VOID) {void bodvcd_c};

extern void bodvcd_c (
        int bodyid,
        char *CONST_STRING,
        int maxn, int *dim, double values[80]);

/***********************************************************************
* -Procedure bodvrd_c ( Return d.p. values from the kernel pool )
*
* -Abstract
*
* Fetch from the kernel pool the double precision values  
* of an item associated with a body. 
*
* void bodvrd_c (
*       ConstSpiceChar   * bodynm,
*       ConstSpiceChar   * item,
*       SpiceInt           maxn,
*       SpiceInt         * dim,
*       SpiceDouble      * values ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* bodynm     I   Body name. 
* item       I   Item for which values are desired. ("RADII", 
*                "NUT_PREC_ANGLES", etc. ) 
* maxn       I   Maximum number of values that may be returned. 
* dim        O   Number of values returned. 
* values     O   Values. 
***********************************************************************/

%rename (bodvrd) bodvrd_c;

%apply (int DIM1, int *SIZE1, double OUT_ARRAY1[ANY])
                        {(int maxn, int *dim, double values[80])};
%apply (void RETURN_VOID) {void bodvrd_c};

extern void bodvrd_c (
        char *CONST_STRING,
        char *CONST_STRING,
        int maxn, int *dim, double values[80]);

/***********************************************************************
* -Procedure cgv2el_c ( Center and generating vectors to ellipse )
*
* -Abstract
*
* Form a CSPICE ellipse from a center vector and two generating 
* vectors. 
*
* void cgv2el_c (
*       ConstSpiceDouble    center[3],
*       ConstSpiceDouble    vec1  [3],
*       ConstSpiceDouble    vec2  [3],
*       SpiceEllipse      * ellipse   ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* center, 
* vec1, 
* vec2       I   Center and two generating vectors for an ellipse. 
* ellipse    O   The CSPICE ellipse defined by the input vectors. 
***********************************************************************/

%rename (cgv2el) cgv2el_c;

%apply (double  IN_ARRAY1[ANY]) {double center[3]};
%apply (double  IN_ARRAY1[ANY]) {double vec1[3]};
%apply (double  IN_ARRAY1[ANY]) {double vec2[3]};
%apply (double OUT_ARRAY1[ANY]) {double ellipse[NELLIPSE]};
%apply (void RETURN_VOID) {void cgv2el_c};

extern void cgv2el_c (
        double center[3],
        double vec1[3],
        double vec2[3],
        double ellipse[NELLIPSE]);

/***********************************************************************
* -Procedure cidfrm_c ( center SPK ID frame )
*
* -Abstract
*
* Retrieve frame ID code and name to associate with a frame center. 
*
* void cidfrm_c (
*       SpiceInt        cent,
*       SpiceInt        lenout,
*       SpiceInt      * frcode,
*       SpiceChar     * frname,
*       SpiceBoolean  * found  ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* cent       I   An object to associate a frame with. 
* lenout     I   Available space in output string frname.
* frcode     O   The ID code of the frame associated with cent.
* frname     O   The name of the frame with ID frcode.
* found      O   SPICETRUE if the requested information is available. 
***********************************************************************/

%rename (cidfrm) my_cidfrm_c;

%apply (int *OUTPUT) {int *frcode};
%apply (int DIM1, char OUT_STRING[ANY]) {(int lenout,
                                          char frname[256])};
%apply (int *OUT_BOOLEAN_LOOKUPERROR) {int *found};
%apply (void RETURN_VOID) {void my_cidfrm_c};

/* Helper function to reorder arguments */
%inline %{
    void my_cidfrm_c(int cent, int *frcode,
                     int lenout, char frname[256], int *found) {

        cidfrm_c(cent, lenout, frcode, frname, found);
    }
%}

/***********************************************************************
* -Procedure ckcov_c ( CK coverage )
*
* -Abstract
*
* Find the coverage window for a specified object in a specified CK 
* file. 
*
* void ckcov_c (
*       ConstSpiceChar    * ck,
*       SpiceInt            idcode,
*       SpiceBoolean        needav,
*       ConstSpiceChar    * level,
*       SpiceDouble         tol,
*       ConstSpiceChar    * timsys,
*       SpiceCell         * cover   ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* ck         I   Name of CK file. 
* idcode     I   ID code of object. 
* needav     I   Flag indicating whether angular velocity is needed. 
* level      I   Coverage level:  "SEGMENT" OR "INTERVAL". 
* tol        I   Tolerance in ticks. 
* timsys     I   Time system used to represent coverage. 
* cover     I/O  Window giving coverage for `idcode'. 
***********************************************************************/

%rename (ckcov) my_ckcov_c;

%apply (char *CONST_STRING) {char *ck};
%apply (char *CONST_STRING) {char *level};
%apply (char *CONST_STRING) {char *timsys};
%apply (double OUT_ARRAY2[ANY][ANY], int *SIZE1)
                            {(double array[500][2], int *intervals)};
%apply (void RETURN_VOID) {void my_ckcov_c};

%inline %{
    /* Helper function to create a 2-D array of results */
    void my_ckcov_c(char *ck, int idcode, int needav,
                    char *level, double tol, char *timsys,
                    double array[500][2], int *intervals) {

        int     j;
        SPICEDOUBLE_CELL(coverage, 2 * 500);

        scard_c(0, &coverage);
        ckcov_c(ck, idcode, needav, level, tol, timsys, &coverage);

        *intervals = (int) card_c(&coverage) / 2;

        for (j = 0; j < *intervals; j++) {
            wnfetd_c(&coverage, j, &(array[j][0]), &(array[j][1]));
        }
    }
%}

/***********************************************************************
* -Procedure      ckgp_c ( C-kernel, get pointing )
*
* -Abstract
*
* Get pointing (attitude) for a specified spacecraft clock time. 
*
* void ckgp_c (
*       SpiceInt            inst, 
*       SpiceDouble         sclkdp, 
*       SpiceDouble         tol, 
*       ConstSpiceChar    * ref, 
*       SpiceDouble         cmat[3][3], 
*       SpiceDouble       * clkout,  
*       SpiceBoolean      * found      ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* inst       I   NAIF ID of instrument, spacecraft, or structure.
* sclkdp     I   Encoded spacecraft clock time. 
* tol        I   Time tolerance. 
* ref        I   Reference frame. 
* cmat       O   C-matrix pointing data. 
* clkout     O   Output encoded spacecraft clock time. 
* found      O   True when requested pointing is available. 
***********************************************************************/

%rename (ckgp) ckgp_c;

%apply (double OUT_ARRAY2[ANY][ANY]) {double cmat[3][3]};
%apply (void RETURN_VOID) {void ckgp_c};

extern void ckgp_c (
        int inst, 
        double sclkdp, 
        double tol, 
        char *CONST_STRING, 
        double cmat[3][3], 
        double *OUTPUT,  
        int *OUT_BOOLEAN_LOOKUPERROR );

/***********************************************************************
* -Procedure  ckgpav_c ( C-kernel, get pointing and angular velocity )
*
* -Abstract
*
* Get pointing (attitude) and angular velocity for a specified 
* spacecraft clock time.
*
* void ckgpav_c (
*       SpiceInt            inst, 
*       SpiceDouble         sclkdp, 
*       SpiceDouble         tol, 
*       ConstSpiceChar    * ref, 
*       SpiceDouble         cmat[3][3], 
*       SpiceDouble         av[3],
*       SpiceDouble       * clkout,  
*       SpiceBoolean      * found      ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* inst       I   NAIF ID of instrument, spacecraft, or structure.
* sclkdp     I   Encoded spacecraft clock time. 
* tol        I   Time tolerance. 
* ref        I   Reference frame. 
* cmat       O   C-matrix pointing data. 
* av         O   Angular velocity vector.
* clkout     O   Output encoded spacecraft clock time. 
* found      O   True when requested pointing is available. 
***********************************************************************/

%rename (ckgpav) ckgpav_c;

%apply (double OUT_ARRAY2[ANY][ANY]) {double cmat[3][3]};
%apply (double OUT_ARRAY1[ANY])      {double   av[3]   };
%apply (void RETURN_VOID) {void ckgpav_c};

extern void ckgpav_c (
        int inst, 
        double sclkdp, 
        double tol, 
        char *CONST_STRING, 
        double cmat[3][3], 
        double av[3],
        double *OUTPUT,  
        int *OUT_BOOLEAN_LOOKUPERROR );

/***********************************************************************
* -Procedure ckobj_c ( CK objects )
*
* -Abstract
*
* Find the set of ID codes of all objects in a specified CK file. 
*
* void ckobj_c (
*       ConstSpiceChar  * ck,
*       SpiceCell       * ids ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* ck         I   Name of CK file. 
* ids       I/O  Set of ID codes of objects in CK file. 
***********************************************************************/

%rename (ckobj) my_ckobj_c;

%apply (char *CONST_STRING) {char *ck};
%apply (int OUT_ARRAY1[ANY], int *SIZE1) {(int body_ids[200],
                                             int *bodies)};
%apply (void RETURN_VOID) {void my_ckobj_c};

/* Helper function to create a 1-D array of results */
%inline %{
    void my_ckobj_c(char *ck, int body_ids[200], int *bodies) {
        int j;
        SPICEINT_CELL(ids, 200);

        scard_c(0, &ids);
        ckobj_c(ck, &ids);

        *bodies = card_c(&ids);
        for (j = 0; j < *bodies; j++) {
            body_ids[j] = SPICE_CELL_ELEM_I(&ids, j);
        }
    }
%}

/***********************************************************************
* -Procedure  clight_c ( C, Speed of light in a vacuum )
*
* -Abstract
*
* Return the speed of light in a vacuum (IAU official
* value, in km/sec).
*
* SpiceDouble clight_c (
        void )
*
* -Brief_I/O
*
* The function returns the speed of light in vacuo (km/sec).
***********************************************************************/

%rename (clight) clight_c;

extern double clight_c ( void );

/***********************************************************************
* -Procedure clpool_c ( Clear the pool of kernel variables )
*
* -Abstract
*
* Remove all variables from the kernel pool. 
*
* void clpool_c (
*        void ) 
*
* -Brief_I/O
*
* None. 
***********************************************************************/

%rename (clpool) clpool_c;

%apply (void RETURN_VOID) {void clpool_c};

extern void clpool_c ( void );

/***********************************************************************
* -Procedure cnmfrm_c ( Center name to associated frame )
*
* -Abstract
*
* Retrieve frame ID code and name to associate with an object. 
*
* void cnmfrm_c (
*       ConstSpiceChar   * cname,
*       SpiceInt           lenout,
*       SpiceInt         * frcode,
*       SpiceChar        * frname,
*       SpiceBoolean     * found   ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* cname      I   Name of the object to find a frame for.
* lenout     I   Maximum length available for frame name.
* frcode     O   The ID code of the frame associated with cname.
* frname     O   The name of the frame with ID frcode.
* found      O   SPICETRUE if the requested information is available. 
***********************************************************************/

%rename (cnmfrm) my_cnmfrm_c;

%apply (char *CONST_STRING) {char *cname};
%apply (int *OUTPUT) {int *frcode};
%apply (int DIM1, char OUT_STRING[ANY]) {(int lenout,
                                          char frname[256])};
%apply (int *OUT_BOOLEAN_LOOKUPERROR) {int *found};
%apply (void RETURN_VOID) {void my_cnmfrm_c};

%inline %{
    /* Helper function to reorder arguments */
    void my_cnmfrm_c(char *cname, int *frcode,
                     int lenout, char frname[256], int *found) {

        cnmfrm_c(cname, lenout, frcode, frname, found);
    }
%}

/***********************************************************************
* -Procedure conics_c ( Determine state from conic elements )
*
* -Abstract
*
* Determine the state (position, velocity) of an orbiting body
* from a set of elliptic, hyperbolic, or parabolic orbital
* elements.
*
* void conics_c (
*       ConstSpiceDouble  elts[8],
*       SpiceDouble       et,
*       SpiceDouble       state[6] )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* elts       I   Conic elements.
* et         I   Input time.
* state      O   State of orbiting body at et.
***********************************************************************/

%rename (conics) conics_c;

%apply (double  IN_ARRAY1[ANY]) {double elts[8]};
%apply (double OUT_ARRAY1[ANY]) {double state[6]};
%apply (void RETURN_VOID) {void conics_c};

extern void conics_c (
        double elts[8],
        double et,
        double state[6] );

/***********************************************************************
* -Procedure convrt_c ( Convert Units )
*
* -Abstract
*
* Take a measurement X, the units associated with 
* X, and units to which X should be converted; return Y --- 
* the value of the measurement in the output units. 
*
* void convrt_c (
*       SpiceDouble       x,
*       ConstSpiceChar  * in,
*       ConstSpiceChar  * out,
*       SpiceDouble     * y    ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  ------------------------------------------------- 
* x          I   Number representing a measurement in some units. 
* in         I   The units in which x is measured. 
* out        I   Desired units for the measurement. 
* y          O   The measurment in the desired units. 
***********************************************************************/

%rename (convrt) convrt_c;

%apply (void RETURN_VOID) {void convrt_c};

extern void convrt_c (
        double x,
        char *CONST_STRING,
        char *CONST_STRING,
        double *OUTPUT);

/***********************************************************************
* -Procedure cyllat_c ( Cylindrical to latitudinal )
*
* -Abstract
*
* Convert from cylindrical to latitudinal coordinates. 
*
* void cyllat_c (
*       SpiceDouble    r,
*       SpiceDouble    lonc,
*       SpiceDouble    z,
*       SpiceDouble *  radius,
*       SpiceDouble *  lon,
*       SpiceDouble *  lat ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* r          I   Distance of point from z axis. 
* lonc       I   Cylindrical angle of point from XZ plane(radians). 
* z          I   Height of point above XY plane. 
* radius     O   Distance of point from origin. 
* lon        O   Longitude of point (radians). 
* lat        O   Latitude of point (radians). 
***********************************************************************/

%rename (cyllat) cyllat_c;
%apply (void RETURN_VOID) {void cyllat_c};

extern void cyllat_c (
        double r,
        double lonc,
        double z,
        double *OUTPUT,
        double *OUTPUT,
        double *OUTPUT);

/***********************************************************************
* -Procedure cylrec_c ( Cylindrical to rectangular )
*
* -Abstract
*
* Convert from cylindrical to rectangular coordinates.
*
* void cylrec_c (
*       SpiceDouble r,
*       SpiceDouble lon,
*       SpiceDouble z,
*       SpiceDouble rectan[3] )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  -------------------------------------------------
* r          I   Distance of a point from z axis.
* lon        I   Angle (radians) of a point from xZ plane
* z          I   Height of a point above xY plane.
* rectan     O   Rectangular coordinates of the point.
***********************************************************************/

%rename (cylrec) cylrec_c;

%apply (double OUT_ARRAY1[ANY]) {double rectan[3]};
%apply (void RETURN_VOID) {void cylrec_c};

extern void cylrec_c (
        double r,
        double lon,
        double z,
        double rectan[3]);

/***********************************************************************
* -Procedure cylsph_c ( Cylindrical to spherical )
*
* -Abstract
*
* Convert from cylindrical to spherical coordinates.
*
* void cylsph_c (
*       SpiceDouble    r,
*       SpiceDouble    lonc,
*       SpiceDouble    z,
*       SpiceDouble *  radius,
*       SpiceDouble *  colat,
*       SpiceDouble *  lon )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  -------------------------------------------------
* r          I   Distance of point from z axis.
* lonc       I   Angle (radians) of point from XZ plane.
* z          I   Height of point above XY plane.
* radius     O   Distance of point from origin.
* colat      O   Polar angle (co-latitude in radians) of point.
* lon        O   Azimuthal angle (longitude) of point (radians).
***********************************************************************/

%rename (cylsph) cylsph_c;
%apply (void RETURN_VOID) {void cylsph_c};

extern void cylsph_c (
        double r,
        double lonc,
        double z,
        double *OUTPUT,
        double *OUTPUT,
        double *OUTPUT);

/***********************************************************************
* -Procedure dafbfs_c ( DAF, begin forward search )
*
* -Abstract
*
* Begin a forward search for arrays in a DAF.
*  
* void dafbfs_c ( SpiceInt handle )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle of file to be searched.
***********************************************************************/

%rename (dafbfs) dafbfs_c;
%apply (void RETURN_VOID) {void dafbfs_c};

extern void dafbfs_c (
        int handle);

/***********************************************************************
* -Procedure dafgda_c ( DAF, read data from address )
*
* -Abstract
*
* Read the double precision data bounded by two addresses within
* a DAF.
*
* void dafgda_c ( SpiceInt       handle, 
*                 SpiceInt       begin,
*                 SpiceInt       end,
*                 SpiceDouble  * data )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle of a DAF.
* begin,
* end        I   Initial, final address within file.
* data       O   Data contained between `begin' and `end'.                   
***********************************************************************/

%rename (dafgda) dafgda_c;
%apply (double OUT_ARRAY1[ANY]) {double data[256]};
%apply (void RETURN_VOID) {void dafgda_c};

extern void dafgda_c (
        int handle,
        int begin,
        int end,
        double data[256]);
                           
/***********************************************************************
* -Procedure dafgn_c ( DAF, get array name )
*
* -Abstract
*
* Return (get) the name for the current array in the current DAF. 
*
* -Brief_I/O
*
* void dafgn_c ( SpiceInt     lenout,
*                SpiceChar  * name   ) 
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* lenout     I   Length of array name string.
* name       O   Name of current array. 
***********************************************************************/

%rename (dafgn) dafgn_c;

%apply (int DIM1, char OUT_STRING[ANY]) {(int lenout,
                                          char string[256])};
%apply (void RETURN_VOID) {void dafgn_c};

extern void dafgn_c (
        int lenout, char string[256]);

/***********************************************************************
* -Procedure dafgs_c ( DAF, get summary )
*
* -Abstract
*
* Return (get) the summary for the current array in the current
* DAF.
*  
* void dafgs_c ( SpiceDouble sum[] )
*  
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* sum        O   Summary for current array.
***********************************************************************/

%rename (dafgs) dafgs_c;

%apply (double OUT_ARRAY1[ANY]) {double sum[128]};
%apply (void RETURN_VOID) {void dafgs_c};

extern void dafgs_c (
        double sum[128]);

/***********************************************************************
* -Procedure daffna_c ( DAF, find next array )
*
* -Abstract
*
* Find the next (forward) array in the current DAF.
*
* void daffna_c ( SpiceBoolean  * found )
*  
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* found      O   SPICETRUE if an array was found.
***********************************************************************/

%rename (daffna) daffna_c;

%apply (void RETURN_VOID) {void daffna_c};

extern void daffna_c (
        int *OUTPUT);
  
/***********************************************************************
* -Procedure dafopr_c ( DAF, open for read )
*
* -Abstract
*
* Open a DAF for subsequent read requests.
*
* void dafopr_c ( ConstSpiceChar    * fname,
*                 SpiceInt          * handle  )
*                   
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* fname      I   Name of DAF to be opened.
* handle     O   Handle assigned to DAF.
***********************************************************************/

%rename (dafopr) dafopr_c;

%apply (void RETURN_VOID) {void dafopr_c};

extern void dafopr_c (
        char *CONST_STRING,
        int  *OUTPUT);
       
/***********************************************************************
* -Procedure dafus_c ( DAF, unpack summary )
*
* -Abstract
*
* Unpack an array summary into its double precision and integer
* components.
*
* void dafus_c ( ConstSpiceDouble   sum [],
*                SpiceInt           nd,
*                SpiceInt           ni,
*                SpiceDouble        dc  [],
*                SpiceInt           ic  []  )
*                 
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* sum        I   Array summary.
* nd         I   Number of double precision components.
* ni         I   Number of integer components.
* dc         O   Double precision components.
* ic         O   Integer components.
***********************************************************************/

%rename (dafus) dafus_c;

%apply (double IN_ARRAY1[ANY]) {double sum[128]};
%apply (double OUT_ARRAY1[ANY]) {double dc[256]};
%apply (int OUT_ARRAY1[ANY]) {int ic[256]};
%apply (void RETURN_VOID) {void dafus_c};

extern void dafus_c (
        double sum[128],
        int nd,
        int ni,
        double dc[256],
        int ic[256]);
          
/***********************************************************************
* -Procedure dcyldr_c (Derivative of cylindrical w.r.t. rectangular )
*
* -Abstract
*
* This routine computes the Jacobian of the transformation from 
* rectangular to cylindrical coordinates. 
*
* void dcyldr_c (
*       SpiceDouble    x,
*       SpiceDouble    y,
*       SpiceDouble    z,
*       SpiceDouble    jacobi[3][3] )   
*            
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* x          I   X-coordinate of point. 
* y          I   Y-coordinate of point. 
* z          I   Z-coordinate of point. 
* jacobi     O   Matrix of partial derivatives. 
***********************************************************************/

%rename (dcyldr) dcyldr_c;

%apply (double OUT_ARRAY2[ANY][ANY]) {double jacobi[3][3]};
%apply (void RETURN_VOID) {void dcyldr_c};

extern void dcyldr_c (
        double x,
        double y,
        double z,
        double jacobi[3][3]);

/***********************************************************************
* -Procedure deltet_c ( Delta ET, ET - UTC )
*
* -Abstract
*
* Return the value of Delta ET (ET-UTC) for an input epoch. 
*
* void deltet_c (
*       SpiceDouble      epoch,
*       ConstSpiceChar * eptype,
*       SpiceDouble    * delta ) 
*
* -Brief_I/O 
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* epoch      I   Input epoch (seconds past J2000). 
* eptype     I   Type of input epoch ("UTC" or "ET"). 
* delta      O   Delta ET (ET-UTC) at input epoch. 
***********************************************************************/

%rename (deltet) deltet_c;

%apply (void RETURN_VOID) {void deltet_c};

extern void deltet_c (
        double epoch,
        char *CONST_STRING,
        double *OUTPUT);

/***********************************************************************
* -Procedure det_c  ( Determinant of a double precision 3x3 matrix )
*
* -Abstract
*
* Compute the determinant of a double precision 3x3 matrix. 
*
* SpiceDouble det_c (
*       ConstSpiceDouble m1[3][3] ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* m1         I     Matrix whose determinant is to be found. 
***********************************************************************/

%rename (det) det_c;

%apply (double IN_ARRAY2[ANY][ANY]) {double m1[3][3]};
%apply (double RETURN_DOUBLE) {double det_c};

extern double det_c (
        double m1[3][3] );

/***********************************************************************
* -Procedure dgeodr_c ( Derivative of geodetic w.r.t. rectangular )
*
* -Abstract
*
* This routine computes the Jacobian of the transformation from 
* rectangular to geodetic coordinates. 
*
* void dgeodr_c (
*       SpiceDouble   x,
*       SpiceDouble   y,
*       SpiceDouble   z,
*       SpiceDouble   re,
*       SpiceDouble   f,
*       SpiceDouble   jacobi[3][3] ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* X          I   X-coordinate of point. 
* Y          I   Y-coordinate of point. 
* Z          I   Z-coordinate of point. 
* RE         I   Equatorial radius of the reference spheroid. 
* F          I   Flattening coefficient. 
* JACOBI     O   Matrix of partial derivatives. 
***********************************************************************/

%rename (dgeodr) dgeodr_c;

%apply (double OUT_ARRAY2[ANY][ANY]) {double jacobi[3][3]};
%apply (void RETURN_VOID) {void dgeodr_c};

extern void dgeodr_c (
        double x,
        double y,
        double z,
        double re,
        double f,
        double jacobi[3][3] );

/***********************************************************************
* -Procedure diags2_c   ( Diagonalize symmetric 2x2 matrix )
*
* -Abstract
*
* Diagonalize a symmetric 2x2 matrix. 
*
* void diags2_c (
*       ConstSpiceDouble    symmat [2][2],
*       SpiceDouble         diag   [2][2],
*       SpiceDouble         rotate [2][2]  ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* symmat     I   A symmetric 2x2 matrix. 
* diag       O   A diagonal matrix similar to symmat. 
* rotate     O   A rotation used as the similarity transformation. 
***********************************************************************/

%rename (diags2) diags2_c;

%apply (double  IN_ARRAY2[ANY][ANY]) {double symmat[2][2]};
%apply (double OUT_ARRAY2[ANY][ANY]) {double diag  [2][2]};
%apply (double OUT_ARRAY2[ANY][ANY]) {double rotate[2][2]};
%apply (void RETURN_VOID) {void diags2_c};

extern void diags2_c (
        double symmat[2][2],
        double diag  [2][2],
        double rotate[2][2] );

/***********************************************************************
* -Procedure dlatdr_c ( Derivative of latitudinal w.r.t. rectangular )
*
* -Abstract
*
* This routine computes the Jacobian of the transformation from 
* rectangular to latitudinal coordinates. 
*
* void dlatdr_c (
*       SpiceDouble   x,
*       SpiceDouble   y,
*       SpiceDouble   z,
*       SpiceDouble   jacobi[3][3] ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* x          I   X-coordinate of point. 
* y          I   Y-coordinate of point. 
* z          I   Z-coordinate of point. 
* jacobi     O   Matrix of partial derivatives. 
***********************************************************************/

%rename (dlatdr) dlatdr_c;

%apply (double OUT_ARRAY2[ANY][ANY]) {double jacobi[3][3]};
%apply (void RETURN_VOID) {void dlatdr_c};

extern void dlatdr_c (
        double x,
        double y,
        double z,
        double jacobi[3][3] );

/***********************************************************************
* -Procedure dpgrdr_c ( Derivative of planetographic w.r.t. rectangular )
*
* -Abstract
*
* This routine computes the Jacobian matrix of the transformation 
* from rectangular to planetographic coordinates. 
*
* void dpgrdr_c (
*       ConstSpiceChar  * body,
*       SpiceDouble       x,
*       SpiceDouble       y,
*       SpiceDouble       z,
*       SpiceDouble       re,
*       SpiceDouble       f,
*       SpiceDouble       jacobi[3][3]  ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* body       I   Body with which coordinate system is associated. 
* x          I   X-coordinate of point. 
* y          I   Y-coordinate of point. 
* z          I   Z-coordinate of point. 
* re         I   Equatorial radius of the reference spheroid. 
* f          I   Flattening coefficient. 
* jacobi     O   Matrix of partial derivatives. 
***********************************************************************/

%rename (dpgrdr) dpgrdr_c;

%apply (double OUT_ARRAY2[ANY][ANY]) {double jacobi[3][3]};
%apply (void RETURN_VOID) {void dpgrdr_c};

extern void dpgrdr_c (
        char *CONST_STRING,
        double x,
        double y,
        double z,
        double re,
        double f,
        double jacobi[3][3]);

/***********************************************************************
* -Procedure dpmax_c ( Largest DP number )
*
* -Abstract
*
* Return the value of the largest (positive) number representable 
* in a double precision variable. 
*
* SpiceDouble dpmax_c () 
*
* -Brief_I/O
*
* The function returns the value of the largest (positive) number 
* that can be represented in a double precision variable. 
***********************************************************************/

%rename (dpmax) dpmax_c;

extern double dpmax_c ( void );

/***********************************************************************
* -Procedure dpmin_c ( Smallest DP number )
*
* -Abstract
*
* Return the value of the smallest (negative) number representable 
* in a double precision variable. 
*
* SpiceDouble dpmin_c () 
*
* -Brief_I/O
*
* The function returns the value of the smallest (negative) number 
* that can be represented in a double precision variable. 
***********************************************************************/

%rename (dpmin) dpmin_c;

extern double dpmin_c ( void );

/***********************************************************************
* -Procedure  dpr_c ( Degrees per radian )
*
* -Abstract
*
* Return the number of degrees per radian.
*
* SpiceDouble dpr_c (
        void )
*
* -Brief_I/O
*
* The function returns the number of degrees per radian.
***********************************************************************/

%rename (dpr) dpr_c;

extern double dpr_c ( void );

/***********************************************************************
* -Procedure drdcyl_c (Derivative of rectangular w.r.t. cylindrical)
*
* -Abstract
*
* This routine computes the Jacobian of the transformation from 
* cylindrical to rectangular coordinates. 
*
* void drdcyl_c (
*       SpiceDouble    r,
*       SpiceDouble    lon,
*       SpiceDouble    z,
*       SpiceDouble    jacobi[3][3] ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* r          I   Distance of a point from the origin. 
* lon        I   Angle of the point from the xz plane in radians. 
* z          I   Height of the point above the xy plane. 
* jacobi     O   Matrix of partial derivatives. 
***********************************************************************/

%rename (drdcyl) drdcyl_c;

%apply (double OUT_ARRAY2[ANY][ANY]) {double jacobi[3][3]};
%apply (void RETURN_VOID) {void drdcyl_c};

extern void drdcyl_c (
        double r,
        double lon,
        double z,
        double jacobi[3][3]);

/***********************************************************************
* -Procedure drdgeo_c ( Derivative of rectangular w.r.t. geodetic )
*
* -Abstract
*
* This routine computes the Jacobian of the transformation from 
* geodetic to rectangular coordinates. 
*
* void drdgeo_c (
*       SpiceDouble    lon,
*       SpiceDouble    lat,
*       SpiceDouble    alt,
*       SpiceDouble    re,
*       SpiceDouble    f,
*       SpiceDouble    jacobi[3][3] ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* lon        I   Geodetic longitude of point (radians). 
* lat        I   Geodetic latitude of point (radians). 
* alt        I   Altitude of point above the reference spheroid. 
* re         I   Equatorial radius of the reference spheroid. 
* f          I   Flattening coefficient. 
* jacobi     O   Matrix of partial derivatives. 
***********************************************************************/

%rename (drdgeo) drdgeo_c;

%apply (double OUT_ARRAY2[ANY][ANY]) {double jacobi[3][3]};
%apply (void RETURN_VOID) {void drdgeo_c};

extern void drdgeo_c (
        double lon,
        double lat,
        double alt,
        double re,
        double f,
        double jacobi[3][3]);

/***********************************************************************
* -Procedure drdlat_c ( Derivative of rectangular w.r.t. latitudinal )
*
* -Abstract
*
* Compute the Jacobian of the transformation from latitudinal to 
* rectangular coordinates. 
*
* void drdlat_c (
*       SpiceDouble   r,
*       SpiceDouble   lon,
*       SpiceDouble   lat,
*       SpiceDouble   jacobi[3][3] ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* radius     I   Distance of a point from the origin. 
* lon        I   Angle of the point from the XZ plane in radians. 
* lat        I   Angle of the point from the XY plane in radians. 
* jacobi     O   Matrix of partial derivatives. 
***********************************************************************/

%rename (drdlat) drdlat_c;

%apply (double OUT_ARRAY2[ANY][ANY]) {double jacobi[3][3]};
%apply (void RETURN_VOID) {void drdlat_c};

extern void drdlat_c (
        double r,
        double lon,
        double lat,
        double jacobi[3][3]);

/***********************************************************************
* -Procedure drdpgr_c ( Derivative of rectangular w.r.t. planetographic )
*
* -Abstract
*
* This routine computes the Jacobian matrix of the transformation 
* from planetographic to rectangular coordinates. 
*
* void drdpgr_c (
*       ConstSpiceChar  * body,
*       SpiceDouble       lon,
*       SpiceDouble       lat,
*       SpiceDouble       alt,
*       SpiceDouble       re,
*       SpiceDouble       f,
*       SpiceDouble       jacobi[3][3] ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* body       I   Name of body with which coordinates are associated. 
* lon        I   Planetographic longitude of a point (radians). 
* lat        I   Planetographic latitude of a point (radians). 
* alt        I   Altitude of a point above reference spheroid. 
* re         I   Equatorial radius of the reference spheroid. 
* f          I   Flattening coefficient. 
* jacobi     O   Matrix of partial derivatives. 
***********************************************************************/

%rename (drdpgr) drdpgr_c;

%apply (double OUT_ARRAY2[ANY][ANY]) {double jacobi[3][3]};
%apply (void RETURN_VOID) {void drdpgr_c};

extern void drdpgr_c (
        char *CONST_STRING,
        double lon,
        double lat,
        double alt,
        double re,
        double f,
        double jacobi[3][3]);

/***********************************************************************
* -Procedure drdsph_c ( Derivative of rectangular w.r.t. spherical )
*
* -Abstract
*
* This routine computes the Jacobian of the transformation from 
* spherical to rectangular coordinates. 
*
* void drdsph_c (
*       SpiceDouble    r,
*       SpiceDouble    colat,
*       SpiceDouble    lon,
*       SpiceDouble    jacobi[3][3] )  
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* r          I   Distance of a point from the origin. 
* colat      I   Angle of the point from the positive z-axis. 
* lon        I   Angle of the point from the xy plane. 
* jacobi     O   Matrix of partial derivatives. 
***********************************************************************/

%rename (drdsph) drdsph_c;

%apply (double OUT_ARRAY2[ANY][ANY]) {double jacobi[3][3]};
%apply (void RETURN_VOID) {void drdsph_c};

extern void drdsph_c (
        double r,
        double colat,
        double lon,
        double jacobi[3][3]);

/***********************************************************************
* -Procedure dsphdr_c ( Derivative of spherical w.r.t. rectangular )
*
* -Abstract
*
* This routine computes the Jacobian of the transformation from 
* rectangular to spherical coordinates. 
*
* void dsphdr_c (
*       SpiceDouble   x,
*       SpiceDouble   y,
*       SpiceDouble   z,
*       SpiceDouble   jacobi[3][3] ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* x          I   x-coordinate of point. 
* y          I   y-coordinate of point. 
* z          I   z-coordinate of point. 
* jacobi     O   Matrix of partial derivatives. 
***********************************************************************/

%rename (dsphdr) dsphdr_c;

%apply (double OUT_ARRAY2[ANY][ANY]) {double jacobi[3][3]};
%apply (void RETURN_VOID) {void dsphdr_c};

extern void dsphdr_c (
        double x,
        double y,
        double z,
        double jacobi[3][3]);

/***********************************************************************
* -Procedure dtpool_c (Data for a kernel pool variable)
*
* -Abstract
*
* Return the data about a kernel pool variable. 
*
* void dtpool_c (
*       ConstSpiceChar   * name,
*       SpiceBoolean     * found,
*       SpiceInt         * n,
*       SpiceChar          type [1] ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* name       I   Name of the variable whose value is to be returned. 
* found      O   True if variable is in pool. 
* n          O   Number of values returned for name. 
* type       O   Type of the variable:  'C', 'N', or 'X' 
***********************************************************************/

%rename (dtpool) dtpool_c;

%apply (char OUT_STRING[ANY]) {char type[20]};
%apply (void RETURN_VOID) {void dtpool_c};

extern void dtpool_c (
        char *CONST_STRING,
        int *OUT_BOOLEAN_KEYERROR,
        int *OUTPUT,
        char type[20]);

/***********************************************************************
* -Procedure dvdot_c ( Derivative of Vector Dot Product, 3-D )
*
* -Abstract
*
* Compute the derivative of the dot product of two double
* precision position vectors.
*
* SpiceDouble dvdot_c (
*       ConstSpiceDouble s1[6],
*       ConstSpiceDouble s2[6] )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* s1         I   First state vector in the dot product.
* s2         I   Second state vector in the dot product.
* The function returns the derivative of the dot product <s1,s2>
***********************************************************************/

%rename (dvdot) dvdot_c;

%apply (double IN_ARRAY1[ANY]) {double s1[6]};
%apply (double IN_ARRAY1[ANY]) {double s2[6]};
%apply (double RETURN_DOUBLE)  {double dvdot_c};

extern double dvdot_c (
        double s1[6],
        double s2[6]);

/***********************************************************************
* -Procedure dvhat_c ( Derivative and unit vector "V-hat" of a state)
*
* -Abstract
*
* Find the unit vector corresponding to a state vector and the
* derivative of the unit vector.
*
* void dvhat_c (
*       ConstSpiceDouble s1  [6],
*       SpiceDouble      sout[6] )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* s1        I     State to be normalized.
* sout      O     Unit vector s1 / |s1|, and its time derivative.
***********************************************************************/

%rename (dvhat) dvhat_c;

%apply (double  IN_ARRAY1[ANY]) {double s1  [6]};
%apply (double OUT_ARRAY1[ANY]) {double sout[6]};
%apply (void RETURN_VOID) {void dvhat_c};

extern void dvhat_c (
        double s1[6],
        double sout[6]);

/***********************************************************************
* -Procedure edlimb_c   ( Ellipsoid Limb )
*
* -Abstract
*
* Find the limb of a triaxial ellipsoid, viewed from a specified 
* point. 
*
* void edlimb_c (
*       SpiceDouble           a,
*       SpiceDouble           b,
*       SpiceDouble           c,
*       ConstSpiceDouble      viewpt[3],
*       SpiceEllipse        * limb      ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* a          I   Length of ellipsoid semi-axis lying on the x-axis. 
* b          I   Length of ellipsoid semi-axis lying on the y-axis. 
* c          I   Length of ellipsoid semi-axis lying on the z-axis. 
* viewpt     I   Location of viewing point. 
* limb       O   Limb of ellipsoid as seen from viewing point. 
***********************************************************************/

%rename (edlimb) edlimb_c;

%apply (double  IN_ARRAY1[ANY]) {double viewpoint[3]};
%apply (double OUT_ARRAY1[ANY]) {double limb[NELLIPSE]};
%apply (void RETURN_VOID) {void edlimb_c};

extern void edlimb_c (
        double a,
        double b,
        double c,
        double viewpt[3],
        double limb[NELLIPSE]);

/***********************************************************************
* -Procedure el2cgv_c ( Ellipse to center and generating vectors )
*
* -Abstract
*
* Convert a CSPICE ellipse to a center vector and two generating 
* vectors.  The selected generating vectors are semi-axes of the 
* ellipse. 
*
* void el2cgv_c (
*       ConstSpiceEllipse   * ellipse,
*       SpiceDouble           center[3],
*       SpiceDouble           smajor[3],
*       SpiceDouble           sminor[3]  ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* ellipse    I   A CSPICE ellipse. 
* center, 
* smajor, 
* sminor     O   Center and semi-axes of ellipse. 
***********************************************************************/

%rename (el2cgv) el2cgv_c;

%apply (double  IN_ARRAY1[ANY]) {double ellipse[NELLIPSE]};
%apply (double OUT_ARRAY1[ANY]) {double center[3]};
%apply (double OUT_ARRAY1[ANY]) {double smajor[3]};
%apply (double OUT_ARRAY1[ANY]) {double sminor[3]};
%apply (void RETURN_VOID) {void el2cgv_c};

extern void el2cgv_c (
        double ellipse[NELLIPSE],
        double center[3],
        double smajor[3],
        double sminor[3]);

/***********************************************************************
* -Procedure erract_c ( Get/Set Default Error Action )
*
* -Abstract
*
* Retrieve or set the default error action.
*
* void erract_c (
*       ConstSpiceChar * op,
*       SpiceInt         lenout,
*       SpiceChar      * action )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* op         I   Operation -- "GET" or "SET"
* lenout     I   Length of list for output.
* action    I/O  Error response action
***********************************************************************/

%rename (erract) erract_c;

%apply (int DIM1, char INOUT_STRING[ANY]) {(int lenout,
                                           char action[256])};
%apply (void RETURN_VOID) {void erract_c};

extern void erract_c(
        char *CONST_STRING,
        int lenout, char action[256]);

/***********************************************************************
* -Procedure errch_c  ( Insert String into Error Message Text )
*
* -Abstract
*
* Substitute a character string for the first occurrence of
* a marker in the current long error message.
*
* void errch_c (
*       ConstSpiceChar * marker,
*       ConstSpiceChar * string )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  ---------------------------------------------------
* marker     I   A substring of the error message to be replaced.
* string     I   The character string to substitute for marker.
***********************************************************************/

%rename (errch) errch_c;

%apply (void RETURN_VOID) {void errch_c};

extern void errch_c (
        char *CONST_STRING,
        char *CONST_STRING);

/***********************************************************************
* -Procedure errdev_c ( Get/Set Error Output Device Name )
*
* -Abstract
*
* Retrieve or set the name of the current output
* device for error messages.
*
* void errdev_c (
*       ConstSpiceChar * op,
*       SpiceInt         lenout,
*       SpiceChar      * device )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* op         I   The operation:  "GET" or "SET".
* lenout     I   Length of device for output.
* device    I/O  The device name.
***********************************************************************/

%rename (errdev) errdev_c;

%apply (int DIM1, char INOUT_STRING[ANY]) {(int lenout,
                                            char device[256])};
%apply (void RETURN_VOID) {void errdev_c};

extern void errdev_c(
        char *CONST_STRING,
        int lenout, char device[256]);

/***********************************************************************
* -Procedure errdp_c  ( Insert D.P. Number into Error Message Text )
*
* -Abstract
*
* Substitute a double precision number for the first occurrence of
* a marker found in the current long error message.
*
* void errdp_c (
*       ConstSpiceChar  * marker,
*       SpiceDouble       number  )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* marker     I   A substring of the error message to be replaced.
* number     I   The d.p. number to substitute for marker.
***********************************************************************/

%rename (errdp) errdp_c;

%apply (void RETURN_VOID) {void errdp_c};

extern void errdp_c (
        char *CONST_STRING,
        double number);

/***********************************************************************
* -Procedure errint_c ( Insert Integer into Error Message Text )
*
* -Abstract
*
* Substitute an integer for the first occurrence of a marker found
* in the current long error message.
*
* void errint_c (
*       ConstSpiceChar  * marker,
*       SpiceInt          number  )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* marker     I   A substring of the error message to be replaced.
* number     I   The integer to substitute for marker.
***********************************************************************/

%rename (errint) errint_c;

%apply (void RETURN_VOID) {void errint_c};

extern void errint_c (
        char *CONST_STRING,
        int number);

/***********************************************************************
* -Procedure errprt_c ( Get/Set Error Output Items )
*
* -Abstract
*
* Retrieve or set the list of error message items
* to be output when an error is detected.
*
* void errprt_c (
*       ConstSpiceChar * op,
*       SpiceInt         lenout,
*       SpiceChar      * list  )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* op         I   The operation:  "GET" or "SET".
* lenout     I   Length of list for output.
* list      I/O  Specification of error messages to be output.
***********************************************************************/

%rename (errprt) errprt_c;

%apply (int DIM1, char INOUT_STRING[ANY]) {(int lenout,
                                            char list[256])};
%apply (void RETURN_VOID) {void errprt_c};

extern void errprt_c(
        char *CONST_STRING,
        int lenout, char list[256]);

/***********************************************************************
* -Procedure et2lst_c ( ET to Local Solar Time )
*
* -Abstract
*
* Given an ephemeris epoch, compute the local solar time for 
* an object on the surface of a body at a specified longitude. 
*
* void et2lst_c (
*       SpiceDouble        et,
*       SpiceInt           body,
*       SpiceDouble        lon,
*       ConstSpiceChar   * type,
*       SpiceInt           timlen,
*       SpiceInt           ampmlen,
*       SpiceInt         * hr,
*       SpiceInt         * mn,
*       SpiceInt         * sc,
*       SpiceChar        * time,
*       SpiceChar        * ampm ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* et         I   Epoch in seconds past J2000 epoch. 
* body       I   ID-code of the body of interest. 
* lon        I   Longitude of surface point (RADIANS). 
* type       I   Type of longitude "PLANETOCENTRIC", etc. 
* timlen     I   Available room in output time string.
* ampmlen    I   Available room in output `ampm' string.
* hr         O   Local hour on a "24 hour" clock. 
* mn         O   Minutes past the hour. 
* sc         O   Seconds past the minute. 
* time       O   String giving local time on 24 hour clock. 
* ampm       O   String giving time on A.M./ P.M. scale. 
***********************************************************************/

%rename (et2lst) my_et2lst_c;

%apply (char *CONST_STRING) {char *type};
%apply (int DIM1, char OUT_STRING[ANY]) {(int timlen,  char time[256])};
%apply (int DIM1, char OUT_STRING[ANY]) {(int ampmlen, char ampm[10])};
%apply (void RETURN_VOID) {void my_et2lst_c};

%inline %{
    void my_et2lst_c(double et, int body, double lon, char *type,
                     int *hr, int *mn, int *sc,
                     int timlen,  char  time[256],
                     int ampmlen, char  ampm[10]) {

        et2lst_c(et, body, lon, type, timlen, ampmlen,
                 hr, mn, sc, time, ampm);
    }
%}

/***********************************************************************
* -Procedure et2utc_c ( Ephemeris Time to UTC )
*
* -Abstract
*
* Convert an input time from ephemeris seconds past J2000
* to Calendar, Day-of-Year, or Julian Date format, UTC.
*
* void et2utc_c (
*       SpiceDouble       et,
*       ConstSpiceChar  * format,
*       SpiceInt          prec,
*       SpiceInt          lenout,
*       SpiceChar       * utcstr   )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* et         I   Input epoch, given in ephemeris seconds past J2000.
* format     I   Format of output epoch.
* prec       I   Digits of precision in fractional seconds or days.
* lenout     I   The length of the output string plus 1.
* utcstr     O   Output time string, UTC.
***********************************************************************/

%rename (et2utc) et2utc_c;

%apply (int DIM1, char OUT_STRING[ANY]) {(int lenout,
                                          char utcstr[256])};
%apply (void RETURN_VOID) {void et2utc_c};

extern void et2utc_c (
        double et,
        char *CONST_STRING,
        int prec,
        int lenout, char utcstr[256]);

/***********************************************************************
* -Procedure etcal_c ( Convert ET to Calendar format )
*
* -Abstract
*
* Convert from an ephemeris epoch measured in seconds past
* the epoch of J2000 to a calendar string format using a
* formal calendar free of leapseconds.
*
* void etcal_c (
*       SpiceDouble   et,
*       SpiceInt      lenout,
*       SpiceChar   * string )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* et         I   Ephemeris time measured in seconds past J2000.
* lenout     I   Length of output string.
* string     O   A standard calendar representation of et.
***********************************************************************/

%rename (etcal) etcal_c;

%apply (int DIM1, char OUT_STRING[ANY]) {(int lenout,
                                          char string[256])};
%apply (void RETURN_VOID) {void etcal_c};

extern void etcal_c (
        double et,
        int lenout, char string[256]);

/***********************************************************************
* -Procedure eul2m_c ( Euler angles to matrix )
*
* -Abstract
*
* Construct a rotation matrix from a set of Euler angles.
*
* void eul2m_c (
*       SpiceDouble  angle3,
*       SpiceDouble  angle2,
*       SpiceDouble  angle1,
*       SpiceInt     axis3,
*       SpiceInt     axis2,
*       SpiceInt     axis1,
*       SpiceDouble  r [3][3] )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* angle3,
* angle2,
* angle1     I   Rotation angles about third, second, and first
* rotation axes (radians).
* axis3,
* axis2,
* axis1      I   Axis numbers of third, second, and first rotation
* axes.
* r          O   Product of the 3 rotations.
***********************************************************************/

%rename (eul2m) eul2m_c;

%apply (double OUT_ARRAY2[ANY][ANY]) {double rout[3][3]};
%apply (void RETURN_VOID) {void eul2m_c};

extern void eul2m_c (
        double angle3,
        double angle2,
        double angle1,
        int axis3,
        int axis2,
        int axis1,
        double rout[3][3]);

/***********************************************************************
* -Procedure eul2xf_c ( Euler angles and derivative to transformation)
*
* -Abstract
*
* This routine computes a state transformation from an Euler angle 
* factorization of a rotation and the derivatives of those Euler 
* angles. 
*
* void eul2xf_c (
*       ConstSpiceDouble    eulang[6],
*       SpiceInt            axisa,
*       SpiceInt            axisb,
*       SpiceInt            axisc,
*       SpiceDouble         xform [6][6] )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* eulang     I   An array of Euler angles and their derivatives. 
* axisa      I   Axis A of the Euler angle factorization. 
* axisb      I   Axis B of the Euler angle factorization. 
* axisc      I   Axis C of the Euler angle factorization. 
* xform      O   A state transformation matrix. 
***********************************************************************/

%rename (eul2xf) eul2xf_c;

%apply (double  IN_ARRAY1[ANY]     ) {double eulang[6]};
%apply (double OUT_ARRAY2[ANY][ANY]) {double xform[6][6]};
%apply (void RETURN_VOID) {void eul2xf_c};

extern void eul2xf_c (
        double eulang[6],
        int axisa,
        int axisb,
        int axisc,
        double xform[6][6]);

/***********************************************************************
* -Procedure expool_c ( Confirm the existence of a pool kernel variable )
*
* -Abstract
*
* Confirm the existence of a kernel variable in the kernel
* pool.
*
* void expool_c (
*       ConstSpiceChar  * name,
*       SpiceBoolean    * found )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* name       I   Name of the variable whose value is to be returned.
* found      O   True when the variable is in the pool.
***********************************************************************/

%rename (expool) expool_c;

%apply (void RETURN_VOID) {void expool_c};

extern void expool_c (
        char *CONST_STRING,
        int *OUT_BOOLEAN);

/***********************************************************************
* -Procedure failed_c ( Error Status Indicator )
*
* -Abstract
*
* True if an error condition has been signalled via sigerr_c.
* failed_c is the CSPICE status indicator.
*
* SpiceBoolean failed_c ()
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* The function takes the value SPICETRUE if an error condition
* was detected; it is SPICEFALSE otherwise.
***********************************************************************/

%rename (failed) failed_c;

%apply (int RETURN_BOOLEAN) {int failed_c};

extern int failed_c ( void );

/***********************************************************************
* -Procedure frame_c ( Build a right handed coordinate frame )
*
* -Abstract
*
* Given a vector x, this routine builds a right handed 
* orthonormal frame x,y,z where the output x is parallel to 
* the input x. 
*
* void frame_c (
*       SpiceDouble x[3],
*       SpiceDouble y[3],
*       SpiceDouble z[3] ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  ------------------------------------------------ 
* x         I/O  Input vector. A parallel unit vector on output. 
* y          O   Unit vector in the plane orthogonal to x. 
* z          O   Unit vector given by x X y. 
***********************************************************************/

%rename (frame) my_frame_c;

%apply (double  IN_ARRAY1[ANY]) {double xin[3]};
%apply (double OUT_ARRAY1[ANY]) {double x[3]};
%apply (double OUT_ARRAY1[ANY]) {double y[3]};
%apply (double OUT_ARRAY1[ANY]) {double z[3]};
%apply (void RETURN_VOID) {void my_frame_c};

/* Helper function deals with in-out argument */

%inline %{
    void my_frame_c(double xin[3],
                    double x[3], double y[3], double z[3]) {
        x[0] = xin[0];
        x[1] = xin[1];
        x[2] = xin[2];
        frame_c(x, y, z);
    }
%}

/***********************************************************************
* -Procedure frinfo_c ( Frame Information )
*
* -Abstract
*
* Retrieve the minimal attributes associated with a frame 
* needed for converting transformations to and from it. 
*
* void frinfo_c (
*       SpiceInt       frcode,
*       SpiceInt      *cent,
*       SpiceInt      *frclss,
*       SpiceInt      *clssid,
*       SpiceBoolean  *found   )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* frcode     I   the idcode for some frame 
* cent       O   the center of the frame 
* frclss     O   the class (type) of the frame 
* clssid     O   the idcode for the frame within its class. 
* found      O   SPICETRUE if the requested information is available. 
***********************************************************************/

%rename (frinfo) frinfo_c;

%apply (void RETURN_VOID) {void frinfo_c};

extern void frinfo_c (
        int frcode,
        int *OUTPUT,
        int *OUTPUT,
        int *OUTPUT,
        int *OUT_BOOLEAN_LOOKUPERROR);

/***********************************************************************
* -Procedure frmchg_ ( Frame Change )
*
* -Abstract
*
* Return the state transformation matrix from one frame to another.
*
* int frmchg_ (
*       SpiceInt      *frame1,
*       SpiceInt      *frame2,
*       SpiceDouble   *et,
*       SpiceDouble   *xform   )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* frame1     I   the frame id-code for some reference frame
* frame2     I   the frame id-code for some reference frame
* et         I   an epoch in TDB seconds past J2000.
* xform      O   a state transformation matrix
***********************************************************************/

%rename (frmchg) my_frmchg;

%apply (double OUT_ARRAY2[ANY][ANY]) {double xform[6][6]};
%apply (void RETURN_VOID) {void my_frmchg};

/* Helper function to deal with pointers to input arguments */
%inline %{
    void my_frmchg(int frame1, int frame2, double et, double xform[6][6]) {
        frmchg_(&frame1, &frame2, &et, xform);
    }
%}

extern void frmchg_(int *frame1, int *frame2, double *et, double *xform);

/***********************************************************************
* -Procedure frmnam_c (Frame to Name)
*
* -Abstract
*
* Retrieve the name of a reference frame associated with 
* a SPICE ID code. 
*
* void frmnam_c (
*       SpiceInt      frcode,
*       SpiceInt      lenout,
*       SpiceChar *   frname  )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* frcode     I   an integer code for a reference frame 
* lenout     I   Maximum length of output string.
* frname     O   the name associated with the reference frame. 
***********************************************************************/

%rename (frmnam) frmnam_c;

%apply (int DIM1, char OUT_STRING[ANY]) {(int lenout,
                                          char frname[256])};
%apply (void RETURN_VOID) {void frmnam_c};

extern void frmnam_c (
        int frcode,
        int lenout,
        char frname[256]);

/***********************************************************************
* -Procedure furnsh_c ( Furnish a program with SPICE kernels )
*
* -Abstract
*
* Load one or more SPICE kernels into a program.
*
* void furnsh_c (
*       ConstSpiceChar  * file ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* file       I   Name of SPICE kernel file (text or binary). 
***********************************************************************/

%rename (furnsh) furnsh_c;

%apply (void RETURN_VOID) {void furnsh_c};

extern void furnsh_c (
        char *CONST_STRING);

/***********************************************************************
* -Procedure gcpool_c (Get character data from the kernel pool)
*
* -Abstract
*
* Return the character value of a kernel variable from the
* kernel pool.
*
* void gcpool_c (
*       ConstSpiceChar * name,
*       SpiceInt         start,
*       SpiceInt         room,
*       SpiceInt         lenout,
*       SpiceInt       * n,
*       void           * cvals,
*       SpiceBoolean   * found )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* name       I   Name of the variable whose value is to be returned.
* start      I   Which component to start retrieving for name
* room       I   The largest number of values to return.
* lenout     I   The length of the output string.
* n          O   Number of values returned for name.
* cvals      O   Values associated with name.
* found      O   True if variable is in pool.
***********************************************************************/

%rename (gcpool) gcpool_c;

%apply (int DIM1, int DIM2, int *NSTRINGS, char OUT_STRINGS[ANY][ANY])
                {(int room, int lenout, int *n, char cvals[80][256])};
%apply (void RETURN_VOID) {void gcpool_c};

extern void gcpool_c (
        char *CONST_STRING,
        int start,
        int room, int lenout, int *n, char cvals[80][256],
        int *OUT_BOOLEAN_KEYERROR);

/***********************************************************************
* -Procedure gdpool_c (Get d.p. values from the kernel pool)
*
* -Abstract
*
* Return the d.p. value of a kernel variable from the kernel pool.
*
* void gdpool_c (
*       ConstSpiceChar * name,
*       SpiceInt         start,
*       SpiceInt         room,
*       SpiceInt       * n,
*       SpiceDouble    * values,
*       SpiceBoolean   * found )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* name       I   Name of the variable whose value is to be returned.
* start      I   Which component to start retrieving for name
* room       I   The largest number of values to return.
* n          O   Number of values returned for name.
* values     O   Values associated with name.
* found      O   True if variable is in pool.
***********************************************************************/

%rename (gdpool) gdpool_c;

%apply (int DIM1, int *SIZE1, double OUT_ARRAY1[ANY])
                            {(int room, int *n, double values[80])};
%apply (void RETURN_VOID) {void gdpool_c};

extern void gdpool_c (
        char *CONST_STRING,
        int start,
        int room, int *n, double values[80],
        int *OUT_BOOLEAN_KEYERROR);

/***********************************************************************
* -Procedure georec_c ( Geodetic to rectangular coordinates )
*
* -Abstract
*
* Convert geodetic coordinates to rectangular coordinates.
*
* void georec_c (
*       SpiceDouble lon,
*       SpiceDouble lat,
*       SpiceDouble alt,
*       SpiceDouble re,
*       SpiceDouble f,
*       SpiceDouble rectan[3] )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* lon        I   Geodetic longitude of point (radians).
* lat        I   Geodetic latitude  of point (radians).
* alt        I   Altitude of point above the reference spheroid.
* re         I   Equatorial radius of the reference spheroid.
* f          I   Flattening coefficient.
* rectan     O   Rectangular coordinates of point.
***********************************************************************/

%rename (georec) georec_c;

%apply (double OUT_ARRAY1[ANY]) {double rectan[3]};
%apply (void RETURN_VOID) {void georec_c};

extern void georec_c (
        double lon,
        double lat,
        double alt,
        double re,
        double f,
        double rectan[3]);

/***********************************************************************
* -Procedure getfov_c (Get instrument FOV configuration)
*
* -Abstract
*
* This subroutine returns the field-of-view (FOV) configuration for a
* specified instrument.
*
* void getfov_c (
*       SpiceInt        instid,
*       SpiceInt        room,
*       SpiceInt        shapelen,
*       SpiceInt        framelen,
*       SpiceChar     * shape,
*       SpiceChar     * frame,
*       SpiceDouble     bsight [3],
*       SpiceInt      * n,
*       SpiceDouble     bounds [][3] ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* instid     I   NAIF ID of an instrument.
* room       I   Maximum number of vectors that can be returned. 
* shapelen   I   Space available in the string `shape'.
* framelen   I   Space available in the string `frame'.
* shape      O   Instrument FOV shape. 
* frame      O   Name of the frame in which FOV vectors are defined. 
* bsight     O   Boresight vector. 
* n          O   Number of boundary vectors returned. 
* bounds     O   FOV boundary vectors. 
***********************************************************************/

%rename (getfov) my_getfov_c;

%apply (int DIM1, char OUT_STRING[ANY]) {(int shapelen,
                                          char shape[256])};
%apply (int DIM1, char OUT_STRING[ANY]) {(int framelen,
                                          char frame[256])};
%apply (double OUT_ARRAY1[ANY]) {double bsight[3]};
%apply (int SIZE1, char OUT_ARRAY2[ANY][ANY])
                                    {(int *n, double bounds[100][3])};
%apply (void RETURN_VOID) {void my_getfov_c};

/* Helper function to deal with order of arguments */
%inline %{
    void my_getfov_c(int instid, int room,
                     int shapelen, char shape[256],
                     int framelen, char frame[256],
                     double bsight[3],
                     int *n, double bounds[100][3]) {

        getfov_c(instid, room, shapelen, framelen, shape, frame,
                 bsight, n, bounds);
    }
%}

/***********************************************************************
* -Procedure getmsg_c ( Get Error Message )
*
* -Abstract
*
* Retrieve the current short error message, 
* the explanation of the short error message, or the 
* long error message. 
*
* void getmsg_c (
*       ConstSpiceChar  * option,
*       SpiceInt          lenout,
*       SpiceChar       * msg     ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* option     I   Indicates type of error message. 
* lenout     I   Available space in the output string msg.
* msg        O   The error message to be retrieved. 
***********************************************************************/

%rename (getmsg) getmsg_c;

%apply (int DIM1, char OUT_STRING[ANY]) {(int lenout, char msg[1024])};
%apply (void RETURN_VOID) {void getmsg_c};

extern void getmsg_c (
        char *CONST_STRING,
        int lenout, char msg[1024]);

/***********************************************************************
* -Procedure gipool_c (Get integers from the kernel pool)
*
* -Abstract
*
* Return the integer value of a kernel variable from the
* kernel pool.
*
* void gipool_c (
*       ConstSpiceChar * name,
*       SpiceInt         start,
*       SpiceInt         room,
*       SpiceInt       * n,
*       SpiceInt       * ivals,
*       SpiceBoolean   * found )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* name       I   Name of the variable whose value is to be returned.
* start      I   Which component to start retrieving for name
* room       I   The largest number of values to return.
* n          O   Number of values returned for name.
* ivals      O   Values associated with name.
* found      O   True if variable is in pool.
***********************************************************************/

%rename (gipool) gipool_c;

%apply (int DIM1, int *SIZE1, int OUT_ARRAY1[ANY])
                                    {(int room, int *n, int ivals[80])}
%apply (void RETURN_VOID) {void gipool_c};

extern void gipool_c(
        char *CONST_STRING,
        int start,
        int room, int *n, int ivals[80],
        int *OUT_BOOLEAN_KEYERROR);

/***********************************************************************
* -Procedure gnpool_c (Get names of kernel pool variables)
*
* -Abstract
*
* Return names of kernel variables matching a specified template.
*
* void gnpool_c (
*       ConstSpiceChar    * name,
*       SpiceInt            start,
*       SpiceInt            room,
*       SpiceInt            lenout,
*       SpiceInt          * n,
*       void              * kvars,
*       SpiceBoolean      * found  )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* name       I   Template that names should match.
* start      I   Index of first matching name to retrieve.
* room       I   The largest number of values to return.
* lenout     I   Length of strings in output array kvars.
* n          O   Number of values returned for name.
* kvars      O   Kernel pool variables whose names match name.
* found      O   True if there is at least one match.
***********************************************************************/

%rename (gnpool) gnpool_c;

%apply (int DIM1, int DIM2, int *NSTRINGS, char OUT_STRINGS[ANY][ANY])
                {(int room, int lenout, int *n, char kvars[80][256])};
%apply (void RETURN_VOID) {void gnpool_c};

extern void gnpool_c (
        char *CONST_STRING,
        int start,
        int room, int lenout, int *n, char kvars[80][256],
        int *OUT_BOOLEAN_LOOKUPERROR);

/***********************************************************************
* -Procedure halfpi_c ( Half the value of pi )
*
* -Abstract
*
* Return half the value of pi (the ratio of the circumference of 
* a circle to its diameter). 
*
* SpiceDouble halfpi_c (
        void ) 
*
* -Brief_I/O
*
* The function returns half the value of pi. 
***********************************************************************/

%rename (halfpi) halfpi_c;

%apply (double RETURN_DOUBLE) {double halfpi_c};

extern double halfpi_c ( void );

/***********************************************************************
* -Procedure ident_c (Return the 3x3 identity matrix)
*
* -Abstract
*
* This routine returns the 3x3 identity matrix. 
*
* void ident_c (
*       SpiceDouble    matrix[3][3] ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* matrix     O   is the 3x3 identity matrix. 
***********************************************************************/

%rename (ident) ident_c;

%apply (double OUT_ARRAY2[ANY][ANY]) {double matrix[3][3]};
%apply (void RETURN_VOID) {void ident_c};

extern void ident_c (
        double matrix[3][3]);

/***********************************************************************
* -Procedure illum_c ( Illumination angles )
*
* -Abstract
*
* Find the illumination angles at a specified surface point of a 
* target body. 
*
* void illum_c  (
*       ConstSpiceChar          * target,
*       SpiceDouble               et,
*       ConstSpiceChar          * abcorr, 
*       ConstSpiceChar          * obsrvr, 
*       ConstSpiceDouble          spoint [3],
*       SpiceDouble             * phase,
*       SpiceDouble             * solar,
*       SpiceDouble             * emissn     )
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* target     I   Name of target body. 
* et         I   Epoch in ephemeris seconds past J2000. 
* abcorr     I   Desired aberration correction. 
* obsrvr     I   Name of observing body. 
* spoint     I   Body-fixed coordinates of a target surface point. 
* phase      O   Phase angle at the surface point. 
* solar      O   Solar incidence angle at the surface point. 
* emissn     O   Emission angle at the surface point. 
***********************************************************************/

%rename (illum) illum_c;

%apply (double IN_ARRAY1[ANY]) {double spoint[3]};
%apply (void   RETURN_VOID)    {void illum_c};

extern void illum_c (
        char *CONST_STRING,
        double et,
        char *CONST_STRING, 
        char *CONST_STRING, 
        double spoint[3],
        double *OUTPUT,
        double *OUTPUT,
        double *OUTPUT);

/***********************************************************************
* -Procedure inedpl_c ( Intersection of ellipsoid and plane )
*
* -Abstract
*
* Find the intersection of a triaxial ellipsoid and a plane. 
*
* void inedpl_c (
*       SpiceDouble           a,
*       SpiceDouble           b,
*       SpiceDouble           c,
*       ConstSpicePlane     * plane,
*       SpiceEllipse        * ellipse,
*       SpiceBoolean        * found    )
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* a          I   Length of ellipsoid semi-axis lying on the x-axis. 
* b          I   Length of ellipsoid semi-axis lying on the y-axis. 
* c          I   Length of ellipsoid semi-axis lying on the z-axis. 
* plane      I   Plane that intersects ellipsoid. 
* ellipse    O   Intersection ellipse, when found is SPICETRUE.
* found      O   Flag indicating whether ellipse was found. 
***********************************************************************/

%rename (inedpl) inedpl_c;

%apply (double  IN_ARRAY1[ANY]) {double plane[NPLANE]};
%apply (double OUT_ARRAY1[ANY]) {double ellipse[NELLIPSE]};
%apply (void RETURN_VOID) {void inedpl_c};

extern void inedpl_c (
        double a,
        double b,
        double c,
        double plane[NPLANE],
        double ellipse[NELLIPSE],
        int *OUT_BOOLEAN);

/***********************************************************************
* -Procedure inelpl_c ( Intersection of ellipse and plane )
*
* -Abstract
*
* Find the intersection of an ellipse and a plane. 
*
* void inelpl_c (
*       ConstSpiceEllipse  * ellips,
*       ConstSpicePlane    * plane,
*       SpiceInt           * nxpts,
*       SpiceDouble          xpt1[3],
*       SpiceDouble          xpt2[3] ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* ellips     I   A CSPICE ellipse. 
* plane      I   A CSPICE plane. 
* nxpts      O   Number of intersection points of plane and ellipse. 
* xpt1, 
* xpt2       O   Intersection points. 
***********************************************************************/

%rename (inelpl) inelpl_c;

%apply (double IN_ARRAY1[ANY]) {double ellipse[NELLIPSE]};
%apply (double IN_ARRAY1[ANY]) {double plane[NPLANE]};
%apply (double OUT_ARRAY1[ANY]) {double xpt1[3]};
%apply (double OUT_ARRAY1[ANY]) {double xpt2[3]};
%apply (void RETURN_VOID) {void inelpl_c};

extern void inelpl_c (
        double ellipse[NELLIPSE],
        double plane[NPLANE],
        int *OUTPUT,
        double xpt1[3],
        double xpt2[3]);

/***********************************************************************
* -Procedure inrypl_c ( Intersection of ray and plane )
*
* -Abstract
*
* Find the intersection of a ray and a plane. 
*
* void inrypl_c (
*       ConstSpiceDouble     vertex [3],
*       ConstSpiceDouble     dir    [3],
*       ConstSpicePlane    * plane,
*       SpiceInt           * nxpts,
*       SpiceDouble          xpt    [3] ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* vertex, 
* dir        I   Vertex and direction vector of ray. 
* plane      I   A CSPICE plane. 
* nxpts      O   Number of intersection points of ray and plane. 
* xpt        O   Intersection point, if nxpts = 1. 
***********************************************************************/

%rename (inrypl) inrypl_c;

%apply (double IN_ARRAY1[ANY]) {double vertex[3]};
%apply (double IN_ARRAY1[ANY]) {double dir[3]};
%apply (double IN_ARRAY1[ANY]) {double plane[NPLANE]};
%apply (double OUT_ARRAY1[ANY]) {double xpt[3]};
%apply (void RETURN_VOID) {void inrypl_c};

extern void inrypl_c (
        double vertex[3],
        double dir[3],
        double plane[NPLANE],
        int *OUTPUT,
        double xpt[3]);

/***********************************************************************
* -Procedure intmax_c ( Largest integer number )
*
* -Abstract
*
* Return the value of the largest (positive) number representable 
* in a SpiceInt variable. 
*
* SpiceInt intmax_c () 
*
* -Brief_I/O
*
* The function returns the value of the largest (positive) number 
* that can be represented in a SpiceInt variable. 
***********************************************************************/

%rename (intmax) intmax_c;

%apply (int RETURN_INT) {int intmax_c};

extern int intmax_c ( void );

/***********************************************************************
* -Procedure intmin_c ( Smallest integer number )
*
* -Abstract
*
* Return the value of the smallest (negative) number representable 
* in a SpiceInt variable. 
*
* SpiceInt intmin_c () 
*
* -Brief_I/O
*
* The function returns the value of the smallest (negative) number 
* that can be represented in a SpiceInt variable. 
***********************************************************************/

%rename (intmin) intmin_c;

%apply (int RETURN_INT) {int intmin_c};

extern int intmin_c ();

/***********************************************************************
* -Procedure invert_c ( Invert a 3x3 matrix )
*
* -Abstract
*
* Generate the inverse of a 3x3 matrix. 
*
* void invert_c (
*       ConstSpiceDouble  m1  [3][3],
*       SpiceDouble       mout[3][3] ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* m1         I   Matrix to be inverted. 
* mout       O   Inverted matrix (m1)**-1.  If m1 is singular, then 
*                mout will be the zero matrix.   mout can 
*                overwrite m1. 
***********************************************************************/

%rename (invert) invert_c;

%apply (double  IN_ARRAY2[ANY][ANY]) {double m1  [3][3]};
%apply (double OUT_ARRAY2[ANY][ANY]) {double mout[3][3]};
%apply (void RETURN_VOID) {void invert_c};

extern void invert_c (
        double m1  [3][3],
        double mout[3][3] );

/***********************************************************************
* -Procedure invort_c ( Invert nearly orthogonal matrices )
*
* -Abstract
*
* Given a matrix, construct the matrix whose rows are the  
* columns of the first divided by the length squared of the 
* the corresponding columns of the input matrix. 
*
* void invort_c (
*       ConstSpiceDouble   m  [3][3],
*       SpiceDouble        mit[3][3] ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* m          I   A 3x3 matrix. 
* mit        I   m after transposition and scaling of rows. 
***********************************************************************/

%rename (invort) invort_c;

%apply (double  IN_ARRAY2[ANY][ANY]) {double m  [3][3]};
%apply (double OUT_ARRAY2[ANY][ANY]) {double mit[3][3]};
%apply (void RETURN_VOID) {void invort_c};

extern void invort_c (
        double m  [3][3],
        double mit[3][3]);

/***********************************************************************
* -Procedure isrot_c ( Indicate whether a matrix is a rotation matrix )
*
* -Abstract
*
* Indicate whether a 3x3 matrix is a rotation matrix. 
*
* SpiceBoolean isrot_c (
*       ConstSpiceDouble    m   [3][3],
*       SpiceDouble         ntol,
*       SpiceDouble         dtol       )
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* m          I   A matrix to be tested. 
* ntol       I   Tolerance for the norms of the columns of m. 
* dtol       I   Tolerance for the determinant of a matrix whose 
*                columns are the unitized columns of m. 
* The function returns the value SPICETRUE if and only if m is 
* a rotation matrix. 
***********************************************************************/

%rename (isrot) isrot_c;

%apply (double IN_ARRAY2[ANY][ANY]) {double m[3][3]};
%apply (int RETURN_BOOLEAN) {int isrot_c};

extern int isrot_c (
        double m[3][3],
        double ntol,
        double dtol);

/***********************************************************************
* -Procedure j1900_c ( Julian Date of 1900.0 JAN 0.5 )
*
* -Abstract
*
* Return the Julian Date of 1899 DEC 31 12:00:00 (1900 JAN 0.5).
*
* SpiceDouble j1900_c (
        void )
*
* -Brief_I/O
*
* The function returns the Julian Date of 1899 DEC 31 12:00:00
* (1900 JAN 0.5).
***********************************************************************/

%rename (j1900) j1900_c;

%apply (double RETURN_DOUBLE) {double j1900_c};

extern double j1900_c ( void );

/***********************************************************************
* -Procedure j1950_c ( Julian Date of 1950.0 JAN 1.0 )
*
* -Abstract
*
* Return the Julian Date of 1950 JAN 01 00:00:00 (1950 JAN 1.0).
*
* SpiceDouble j1950_c (
        void )
*
* -Brief_I/O
*
* The function returns the Julian Date of 1950 JAN 01 00:00:00
* (1950 JAN 1.0).
***********************************************************************/

%rename (j1950) j1950_c;

%apply (double RETURN_DOUBLE) {double j1950_c};

extern double j1950_c ( void );

/***********************************************************************
* -Procedure  j2000_c ( Julian Date of 2000 JAN 1.5 )
*
* -Abstract
*
* Return the Julian Date of 2000 JAN 01 12:00:00 (2000 JAN 1.5).
*
* SpiceDouble j2000_c (
        void )
*
* -Brief_I/O
*
* The function returns the Julian Date of 2000 JAN 01 12:00:00
* (2000 JAN 1.5).
***********************************************************************/

%rename (j2000) j2000_c;

%apply (double RETURN_DOUBLE) {double j2000_c};

extern double j2000_c ( void );

/***********************************************************************
* -Procedure   j2100_c ( Julian Date of 2100 JAN 1.5 )
*
* -Abstract
*
* Return the Julian Date of 2100 JAN 01 12:00:00 (2100 JAN 1.5).
*
* SpiceDouble j2100_c (
        void )
*
* -Brief_I/O
*
* The function returns the Julian Date of 2100 JAN 01 12:00:00
* (2100 JAN 1.5).
***********************************************************************/

%rename (j2100) j2100_c;

%apply (double RETURN_DOUBLE) {double j2100_c};

extern double j2100_c ( void );

/***********************************************************************
* -Procedure jyear_c ( Seconds per julian year )
*
* -Abstract
*
* Return the number of seconds in a julian year.
*
* SpiceDouble jyear_c (
        void )
*
* -Brief_I/O
*
* VARIABLE  I/O              DESCRIPTION
* --------  ---  --------------------------------------------------
* jyear_c    O   The number of seconds/julian year
***********************************************************************/

%rename (jyear) jyear_c;

%apply (double RETURN_DOUBLE) {double jyear_c};

extern double jyear_c ( void );

/***********************************************************************
* -Procedure latcyl_c ( Latitudinal to cylindrical coordinates )
*
* -Abstract
*
* Convert from latitudinal coordinates to cylindrical coordinates.
*
* void latcyl_c (
*       SpiceDouble    radius,
*       SpiceDouble    lon,
*       SpiceDouble    lat,
*       SpiceDouble *  r,
*       SpiceDouble *  lonc,
*       SpiceDouble *  z )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* radius     I   Distance of a point from the origin.
* lon        I   Angle of the point from the XZ plane in radians.
* lat        I   Angle of the point from the XY plane in radians.
* r          O   Distance of the point from the z axis.
* lonc       O   Angle of the point from the XZ plane in radians.
* z          O   Height of the point above the XY plane.
***********************************************************************/

%rename (latcyl) latcyl_c;
%apply (void RETURN_VOID) {void latcyl_c};

extern void latcyl_c (
        double radius,
        double lon,
        double lat,
        double *OUTPUT,
        double *OUTPUT,
        double *OUTPUT);

/***********************************************************************
* -Procedure   latrec_c ( Latitudinal to rectangular coordinates )
*
* -Abstract
*
* Convert from latitudinal coordinates to rectangular coordinates.
*
* void latrec_c (
*       SpiceDouble    radius,
*       SpiceDouble    longitude,
*       SpiceDouble    latitude,
*       SpiceDouble    rectan[3] )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* radius     I   Distance of a point from the origin.
* longitude  I   Longitude of point in radians.
* latitude   I   Latitude of point in radians.
* rectan     O   Rectangular coordinates of the point.
***********************************************************************/

%rename (latrec) latrec_c;

%apply (double OUT_ARRAY1[ANY]) {double rectan[3]};
%apply (void RETURN_VOID) {void latrec_c};

extern void latrec_c (
        double radius,
        double longitude,
        double latitude,
        double rectan[3]);

/***********************************************************************
* -Procedure latsph_c ( Latitudinal to spherical coordinates )
*
* -Abstract
*
* Convert from latitudinal coordinates to spherical coordinates.
*
* void latsph_c (
*       SpiceDouble    radius,
*       SpiceDouble    lon,
*       SpiceDouble    lat,
*       SpiceDouble *  rho,
*       SpiceDouble *  colat,
*       SpiceDouble *  lons )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* radius     I   Distance of a point from the origin.
* lon        I   Angle of the point from the XZ plane in radians.
* lat        I   Angle of the point from the XY plane in radians.
* rho        O   Distance of the point from the origin.
* colat      O   Angle of the point from positive z axis (radians).
* lons       O   Angle of the point from the XZ plane (radians).
***********************************************************************/

%rename (latsph) latsph_c;

%apply (void RETURN_VOID) {void latsph_c};

extern void latsph_c (
        double radius,
        double lon,
        double lat,
        double *OUTPUT,
        double *OUTPUT,
        double *OUTPUT);

/***********************************************************************
* -Procedure ldpool_c ( Load variables from a kernel file into the pool )
*
* -Abstract
*
* Load the variables contained in a NAIF ASCII kernel file into the 
* kernel pool. 
*
* void ldpool_c (
*       ConstSpiceChar * filename )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* filename   I   Name of the kernel file. 
***********************************************************************/

%rename (ldpool) ldpool_c;

%apply (void RETURN_VOID) {void ldpool_c};

extern void ldpool_c (
        char *CONST_STRING );

/***********************************************************************
* -Procedure lspcn_c  ( Longitude of the sun, planetocentric )
*
* -Abstract
*
* Compute L_s, the planetocentric longitude of the sun, as seen 
* from a specified body. 
*
* SpiceDouble lspcn_c (
*       ConstSpiceChar   * body,
*       SpiceDouble        et,
*       ConstSpiceChar   * abcorr )
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* body       I   Name of central body. 
* et         I   Epoch in seconds past J2000 TDB. 
* abcorr     I   Aberration correction. 
*
* The function returns the value of L_s for the specified body 
* at the specified time. 
***********************************************************************/

%rename (lspcn) lspcn_c;

%apply (double RETURN_DOUBLE) {double lspcn_c};

extern double lspcn_c (
        char *CONST_STRING,
        double et,
        char *CONST_STRING);

/***********************************************************************
* -Procedure ltime_c ( Light Time )
*
* void ltime_c (
*       SpiceDouble        etobs,
*       SpiceInt           obs,
*       ConstSpiceChar   * dir,
*       SpiceInt           targ,
*       SpiceDouble      * ettarg,
*       SpiceDouble      * elapsd  ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* etobs      I   Epoch of a signal at some observer 
* obs        I   NAIF ID of some observer 
* dir        I   Direction the signal travels ( "->" or "<-" ) 
* targ       I   NAIF ID of the target object 
* ettarg     O   Epoch of the signal at the target 
* elapsd     O   Time between transmit and receipt of the signal 
***********************************************************************/

%rename (ltime) ltime_c;

%apply (void RETURN_VOID) {void ltime_c};

extern void ltime_c (
        double etobs,
        int obs,
        char *CONST_STRING,
        int targ,
        double *OUTPUT,
        double *OUTPUT);

/***********************************************************************
* -Procedure m2eul_c ( Matrix to Euler angles )
*
* -Abstract
*
* Factor a rotation matrix as a product of three rotations about
* specified coordinate axes.
*
* void  m2eul_c (
*       ConstSpiceDouble    r[3][3],
*       SpiceInt            axis3,
*       SpiceInt            axis2,
*       SpiceInt            axis1,
*       SpiceDouble       * angle3,
*       SpiceDouble       * angle2,
*       SpiceDouble       * angle1  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* r          I   A rotation matrix to be factored.
* axis3,
* axis2,
* axis1      I   Numbers of third, second, and first rotation axes.
* angle3,
* angle2,
* angle1     O   Third, second, and first Euler angles, in radians.
***********************************************************************/

%rename (m2eul) m2eul_c;

%apply (double IN_ARRAY2[ANY][ANY]) {double rin[3][3]};
%apply (void RETURN_VOID) {void m2eul_c};

extern void m2eul_c (
        double rin[3][3],
        int axis3,
        int axis2,
        int axis1,
        double *OUTPUT,
        double *OUTPUT,
        double *OUTPUT);

/***********************************************************************
* -Procedure m2q_c ( Matrix to quaternion )
*
* -Abstract
*
* Find a unit quaternion corresponding to a specified rotation
* matrix.
*
* void m2q_c (
*       ConstSpiceDouble  r[3][3],
*       SpiceDouble       q[4]     )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* r          I   A rotation matrix.
* q          O   A unit quaternion representing r.
***********************************************************************/

%rename (m2q) m2q_c;

%apply (double  IN_ARRAY2[ANY][ANY]) {double rin[3][3]};
%apply (double OUT_ARRAY1[ANY])      {double qout[4]};
%apply (void RETURN_VOID) {void m2q_c};

extern void m2q_c (
        double rin[3][3],
        double qout[4]);

/***********************************************************************
* -Procedure mequ_c ( Matrix equal to another, 3x3 )
*
* -Abstract
*
* Set one double precision 3x3 matrix equal to another.
*
* void mequ_c (
*       ConstSpiceDouble  m1  [3][3],
*       SpiceDouble       mout[3][3] )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* m1         I     Input matrix.
* mout       O     Output matrix equal to m1.
***********************************************************************/

%rename (mequ) mequ_c;

%apply (double  IN_ARRAY2[ANY][ANY]) {double m1  [3][3]};
%apply (double OUT_ARRAY2[ANY][ANY]) {double mout[3][3]};
%apply (void RETURN_VOID) {void mequ_c};

extern void mequ_c (
        double m1  [3][3],
        double mout[3][3] );

/***********************************************************************
* -Procedure mequg_c ( Matrix equal to another, general dimension )
*
* -Abstract
*
* Set one double precision matrix of arbitrary size equal to
* another.
*
* void mequg_c (
*       SpiceDouble  * m1,
*       SpiceInt       nr,
*       SpiceInt       nc,
*       SpiceDouble  * mout )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* m1        I     Input matrix.
* nr        I     Row dimension of m1 (and also mout).
* nc        I     Column dimension of m1 (and also mout).
* mout      O     Output matrix equal to m1.
***********************************************************************/

%rename (mequg) my_mequg_c;

%apply (double   *IN_ARRAY2, int  DIM1, int DIM2)
                                       {(double *m1, int nr1, int nc1)};
%apply (double **OUT_ARRAY2, int *SIZE1, int *SIZE2)
                          {(double **mout, int *nr_out, int *nc_out)};
%apply (void RETURN_VOID) {void my_mequg_c};

%inline %{
    void my_mequg_c(double  *m1,   int  nr1,     int  nc1,
                    double **mout, int *nr_vout, int *nc_vout) {

        double *result = NULL;

        *mout = NULL;
        *nr_vout = 0;
        *nc_vout = 0;

        result = my_malloc(nr1 * nc1);
        if (!result) return;

        mequg_c(m1, nr1, nc1, result);
        *mout = result;
        *nr_vout = nr1;
        *nc_vout = nc1;
    }
%}

/***********************************************************************
* -Procedure mtxm_c  ( Matrix transpose times matrix, 3x3 )
*
* -Abstract
*
* Multiply the transpose of a 3x3 matrix and a 3x3 matrix.
*
* void mtxm_c (
*       ConstSpiceDouble    m1  [3][3],
*       ConstSpiceDouble    m2  [3][3],
*       SpiceDouble         mout[3][3] )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* m1         I   3x3 double precision matrix.
* m2         I   3x3 double precision matrix.
* mout       O   The produce m1 transpose times m2.
***********************************************************************/

%rename (mtxm) mtxm_c;

%apply (double  IN_ARRAY2[ANY][ANY]) {double m1  [3][3]};
%apply (double  IN_ARRAY2[ANY][ANY]) {double m2  [3][3]};
%apply (double OUT_ARRAY2[ANY][ANY]) {double mout[3][3]};
%apply (void RETURN_VOID) {void mtxm_c};

extern void mtxm_c (
        double m1  [3][3],
        double m2  [3][3],
        double mout[3][3]);

/***********************************************************************
* -Procedure  mtxmg_c ( Matrix transpose times matrix, general dimension )
*
* -Abstract
*
* Multiply the transpose of a matrix with another matrix,
* both of arbitrary size. (The dimensions of the matrices must be
* compatible with this multiplication.)
*
* void mtxmg_c (
*       SpiceDouble  * m1,
*       SpiceDouble  * m2,
*       SpiceInt       ncol1,
*       SpiceInt       nr1r2,
*       SpiceInt       ncol2,
*       SpiceDouble  * mout  )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* m1         I   nr1r2 X ncol1 double precision matrix.
* m2         I   nr1r2 X ncol2 double precision matrix.
* ncol1      I   Column dimension of m1 and row dimension of mout.
* nr1r2      I   Row dimension of m1 and m2.
* ncol2      I   Column dimension of m2 (and also mout).
* mout       O   Transpose of m1 times m2.
***********************************************************************/

%rename (mtxmg) my_mtxmg_c;

%apply (double   *IN_ARRAY2, int  DIM1, int  DIM2)
                        {(double *m1, int nr1, int nc1)};
%apply (double   *IN_ARRAY2, int  DIM1, int  DIM2)
                        {(double *m2, int nr2, int nc2)};
%apply (double **OUT_ARRAY2, int *SIZE1, int *SIZE2)
                        {(double **m3, int *nr3, int *nc3)};
%apply (void RETURN_VOID) {void my_mtxmg_c};

%inline %{
    void my_mtxmg_c(double  *m1, int  nr1, int  nc1,
                    double  *m2, int  nr2, int  nc2,
                    double **m3, int *nr3, int *nc3) {

        double *result = NULL;

        *m3 = NULL;
        *nr3 = 0;
        *nc3 = 0;

        if (!my_assert_eq(nr1, nr2,
            "Array dimension mismatch in MTXMG")) return;

        result = my_malloc(nc1 * nc2);
        if (!result) return;

        mtxmg_c(m1, m2, nc1, nr1, nc2, result);
        *m3 = result;
        *nr3 = nc1;
        *nc3 = nc2;
    }
%}

/***********************************************************************
* -Procedure  mtxv_c ( Matrix transpose times vector, 3x3 )
*
* -Abstract
*
* mtxv_c multiplies the transpose of a 3x3 matrix on the left with
* a vector on the right.
*
* void mtxv_c (
*       ConstSpiceDouble     m1  [3][3],
*       ConstSpiceDouble     vin [3],
*       SpiceDouble          vout[3]   )
*
* -Brief_I/O
*
* VARIABLE  I/O              DESCRIPTION
* --------  ---  --------------------------------------------------
* m1         I   3x3 double precision matrix.
* vin        I   3-dimensional double precision vector.
* vout       O   3-dimensional double precision vector. vout is
* the product m1**t * vin.
***********************************************************************/

%rename (mtxv) mtxv_c;

%apply (double  IN_ARRAY2[ANY][ANY]) {double m1  [3][3]};
%apply (double  IN_ARRAY1[ANY])      {double vin [3]};
%apply (double OUT_ARRAY1[ANY])      {double vout[3]}; 
%apply (void RETURN_VOID) {void mtxv_c};

extern void mtxv_c (
        double m1  [3][3],
        double vin [3],
        double vout[3]);

/***********************************************************************
* -Procedure  mtxvg_c ( Matrix transpose times vector, general dimension )
*
* -Abstract
*
* Multiply the transpose of a matrix and a vector of arbitrary size.
*
* void mtxvg_c (
*       SpiceDouble  * m1,
*       SpiceDouble  * v2,
*       SpiceInt       ncol1,
*       SpiceInt       nr1r2,
*       SpiceDouble  * vout   )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* m1         I   Left-hand matrix to be multiplied.
* v2         I   Right-hand vector to be multiplied.
* ncol1      I   Column dimension of m1 and length of vout.
* nr1r2      I   Row dimension of m1 and length of v2.
* vout       O   Product vector m1 transpose * v2.
***********************************************************************/

%rename (mtxvg) my_mtxvg_c;

%apply (double   *IN_ARRAY2, int  DIM1, int  DIM2)
                        {(double *m1, int nr1, int nc1)};
%apply (double   *IN_ARRAY1, int  DIM1)
                        {(double *v2, int nr2)};
%apply (double **OUT_ARRAY1, int *SIZE1)
                        {(double **v3, int *nr3)};
%apply (void RETURN_VOID) {void my_mtxvg_c};

%inline %{
    void my_mtxvg_c(double  *m1, int  nr1, int  nc1,
                    double  *v2, int  nr2,
                    double **v3, int *nr3) {

        double *result = NULL;

        *v3 = NULL;
        *nr3 = 0;

        if (!my_assert_eq(nr1, nr2,
            "Array dimension mismatch in MTXVG")) return;

        result = my_malloc(nc1);
        if (!result) return;

        mtxvg_c(m1, v2, nc1, nr1, result);
        *v3 = result;
        *nr3 = nc1;
    }
%}

/***********************************************************************
* -Procedure mxm_c ( Matrix times matrix, 3x3 )
*
* -Abstract
*
* Multiply two 3x3 matrices.
*
* void mxm_c (
*       ConstSpiceDouble   m1  [3][3],
*       ConstSpiceDouble   m2  [3][3],
*       SpiceDouble        mout[3][3] )
*
* -Brief_I/O
*
* VARIABLE  I/O              DESCRIPTION
* --------  ---  --------------------------------------------------
* m1        i   3x3 double precision matrix.
* m2        i   3x3 double precision matrix.
* mout      o   3x3 double precision matrix. mout is the product
*               m1*m2.
***********************************************************************/

%rename (mxm) mxm_c;

%apply (double  IN_ARRAY2[ANY][ANY]) {double m1  [3][3]};
%apply (double  IN_ARRAY2[ANY][ANY]) {double m2  [3][3]};
%apply (double OUT_ARRAY2[ANY][ANY]) {double mout[3][3]};
%apply (void RETURN_VOID) {void mxm_c};

extern void mxm_c (
        double m1  [3][3],
        double m2  [3][3],
        double mout[3][3]);

/***********************************************************************
* -Procedure  mxmg_c ( Matrix times matrix, general dimension )
*
* -Abstract
*
* Multiply two double precision matrices of arbitrary size.
*
* void mxmg_c (
*       SpiceDouble   * m1,
*       SpiceDouble   * m2,
*       SpiceInt        nrow1,
*       SpiceInt        ncol1,
*       SpiceInt        ncol2,
*       SpiceDouble   * mout   )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* m1         I   nrow1 X ncol1 double precision matrix.
* m2         I   ncol1 X ncol2 double precision matrix.
* nrow1      I   Row dimension of m1 (and also mout).
* ncol1      I   Column dimension of m1 and row dimension of m2.
* ncol2      I   Column dimension of m2 (and also mout).
* mout       O   nrow1 X ncol2 double precision matrix.
***********************************************************************/

%rename (mxmg) my_mxmg_c;

%apply (double   *IN_ARRAY2, int  DIM1, int  DIM2)
                        {(double *m1, int nr1, int nc1)};
%apply (double   *IN_ARRAY2, int  DIM1, int  DIM2)
                        {(double *m2, int nr2, int nc2)};
%apply (double **OUT_ARRAY2, int *SIZE1, int *SIZE2)
                        {(double **m3, int *nr3, int *nc3)};
%apply (void RETURN_VOID) {void my_mxmg_c};

%inline %{
    void my_mxmg_c(double  *m1, int  nr1, int  nc1,
                   double  *m2, int  nr2, int  nc2,
                   double **m3, int *nr3, int *nc3) {

        double *result = NULL;

        *m3 = NULL;
        *nr3 = 0;
        *nc3 = 0;

        if (!my_assert_eq(nc1, nr2,
            "Array dimension mismatch in MXMG")) return;

        result = my_malloc(nr1 * nc2);
        if (!result) return;

        mxmg_c(m1, m2, nr1, nc1, nc2, result);
        *m3 = result;
        *nr3 = nr1;
        *nc3 = nc2;
    }
%}

/***********************************************************************
* -Procedure mxmt_c ( Matrix times matrix transpose, 3x3 )
*
* -Abstract
*
* Multiply a 3x3 matrix and the transpose of another 3x3 matrix.
*
* void mxmt_c (
*       ConstSpiceDouble    m1  [3][3],
*       ConstSpiceDouble    m2  [3][3],
*       SpiceDouble         mout[3][3] )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* m1         I   3x3 double precision matrix.
* m2         I   3x3 double precision matrix.
* mout       O   The product m1 times m2 transpose .
***********************************************************************/

%rename (mxmt) mxmt_c;

%apply (double  IN_ARRAY2[ANY][ANY]) {double m1  [3][3]};
%apply (double  IN_ARRAY2[ANY][ANY]) {double m2  [3][3]};
%apply (double OUT_ARRAY2[ANY][ANY]) {double mout[3][3]};
%apply (void RETURN_VOID) {void mxmt_c};

extern void mxmt_c (
        double m1  [3][3],
        double m2  [3][3],
        double mout[3][3]);

/***********************************************************************
* -Procedure  mxmtg_c ( Matrix times matrix transpose, general dimension )
*
* -Abstract
*
* Multiply a matrix and the transpose of a matrix, both of
* arbitrary size.
*
* void mxmtg_c (
*       SpiceDouble  * m1,
*       SpiceDouble  * m2,
*       SpiceInt       nrow1,
*       SpiceInt       nc1c2,
*       SpiceInt       nrow2,
*       SpiceDouble  * mout  )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* m1         I   Left-hand matrix to be multiplied.
* m2         I   Right-hand matrix whose transpose is to be multiplied
* nrow1      I   Row dimension of m1 and row dimension of mout.
* nc1c2      I   Column dimension of m1 and column dimension of m2.
* nrow2      I   Row dimension of m2 and column dimension of mout.
* mout       O   Product matrix.
***********************************************************************/

%rename (mxmtg) my_mxmtg_c;

%apply (double   *IN_ARRAY2, int  DIM1, int  DIM2)
                        {(double *m1, int nr1, int nc1)};
%apply (double   *IN_ARRAY2, int  DIM1, int  DIM2)
                        {(double *m2, int nr2, int nc2)};
%apply (double **OUT_ARRAY2, int *SIZE1, int *SIZE2)
                        {(double **m3, int *nr3, int *nc3)};
%apply (void RETURN_VOID) {void my_mxmtg_c};

%inline %{
    void my_mxmtg_c(double  *m1, int  nr1, int  nc1,
                    double  *m2, int  nr2, int  nc2,
                    double **m3, int *nr3, int *nc3) {

        double *result = NULL;

        *m3 = NULL;
        *nr3 = 0;
        *nc3 = 0;

        if (!my_assert_eq(nc1, nc2,
            "Array dimension mismatch in MXMTG")) return;

        result = my_malloc(nr1 * nr2);
        if (!result) return;

        mxmg_c(m1, m2, nr1, nc1, nr2, result);
        *m3 = result;
        *nr3 = nr1;
        *nc3 = nr2;
    }
%}

/***********************************************************************
* -Procedure mxv_c ( Matrix times vector, 3x3 )
*
* -Abstract
*
* Multiply a 3x3 double precision matrix with a 3-dimensional
* double precision vector.
*
* void mxv_c (
*       ConstSpiceDouble    m1  [3][3],
*       ConstSpiceDouble    vin [3],
*       SpiceDouble         vout[3]    )
*
* -Brief_I/O
*
* VARIABLE  I/O              DESCRIPTION
* --------  ---  --------------------------------------------------
* m1        I   3x3 double precision matrix.
* vin       I   3-dimensional double precision vector.
* vout      O   3-dimensinoal double precision vector. vout is
* the product m1*vin.
***********************************************************************/

%rename (mxv) mxv_c;

%apply (double  IN_ARRAY2[ANY][ANY]) {double m1  [3][3]};
%apply (double  IN_ARRAY1[ANY])      {double vin [3]};
%apply (double OUT_ARRAY1[ANY])      {double vout[3]}; 
%apply (void RETURN_VOID) {void mxv_c};

extern void mxv_c (
        double m1  [3][3],
        double vin [3],
        double vout[3] );

/***********************************************************************
* -Procedure mxvg_c ( Matrix times vector, general dimension )
*
* -Abstract
*
* Multiply a matrix and a vector of arbitrary size.
*
* void mxvg_c (
*       SpiceDouble      * m1,
*       SpiceDouble      * v2,
*       SpiceInt           nrow1,
*       SpiceInt           nc1r2,
*       SpiceDouble      * vout  )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* m1         I   Left-hand matrix to be multiplied.
* v2         I   Right-hand vector to be multiplied.
* nrow1      I   Row dimension of m1 and length of vout.
* nc1r2      I   Column dimension of m1 and length of v2.
* vout       O   Product vector m1*v2.
***********************************************************************/

%rename (mxvg) my_mxvg_c;

%apply (double   *IN_ARRAY2, int  DIM1, int  DIM2)
                        {(double *m1, int nr1, int nc1)};
%apply (double   *IN_ARRAY1, int  DIM1)
                        {(double *v2, int nr2)};
%apply (double **OUT_ARRAY1, int *SIZE1)
                        {(double **v3, int *nr3)};
%apply (void RETURN_VOID) {void my_mxvg_c};

%inline %{
    void my_mxvg_c(double  *m1, int   nr1, int  nc1,
                   double  *v2, int   nr2,
                   double **v3, int *nr3) {

        double *result = NULL;

        *v3 = NULL;
        *nr3 = 0;

        if (!my_assert_eq(nc1, nr2,
            "Array dimension mismatch in MXVG")) return;

        result = my_malloc(nr1);
        if (!result) return;

        mxvg_c(m1, v2, nr1, nc1, result);
        *v3 = result;
        *nr3 = nr1;
    }
%}

/***********************************************************************
* -Procedure namfrm_c (Name to frame)
*
* -Abstract
*
* Look up the frame ID code associated with a string. 
*
* void namfrm_c (
*       ConstSpiceChar   * frname,
*       SpiceInt         * frcode  ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* frname     I   The name of some reference frame.
* frcode     O   The SPICE ID code of the frame. 
***********************************************************************/

%rename (namfrm) namfrm_c;

%apply (void RETURN_VOID) {void namfrm_c};

extern void namfrm_c (
        char *CONST_STRING,
        int *OUTPUT);

/***********************************************************************
* -Procedure nearpt_c ( Nearest point on an ellipsoid )
*
* -Abstract
*
* This routine locates the point on the surface of an ellipsoid
* that is nearest to a specified position. It also returns the
* altitude of the position above the ellipsoid.
*
* void nearpt_c (
*       ConstSpiceDouble    positn[3],
*       SpiceDouble         a,
*       SpiceDouble         b,
*       SpiceDouble         c,
*       SpiceDouble         npoint[3],
*       SpiceDouble       * alt        )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* positn     I   Position of a point in bodyfixed frame.
* a          I   Length of semi-axis parallel to x-axis.
* b          I   Length of semi-axis parallel to y-axis.
* c          I   Length on semi-axis parallel to z-axis.
* npoint     O   Point on the ellipsoid closest to positn.
* alt        O   Altitude of positn above the ellipsoid.
***********************************************************************/

%rename (nearpt) nearpt_c;

%apply (double  IN_ARRAY1[ANY]) {double positn[3]};
%apply (double OUT_ARRAY1[ANY]) {double npoint[3]};
%apply (void RETURN_VOID) {void nearpt_c};

extern void nearpt_c (
        double positn[3],
        double a,
        double b,
        double c,
        double npoint[3],
        double *OUTPUT);

/***********************************************************************
* -Procedure npedln_c ( Nearest point on ellipsoid to line )
*
* -Abstract
*
* Find nearest point on a triaxial ellipsoid to a specified line, 
* and the distance from the ellipsoid to the line. 
*
* void npedln_c (
*       SpiceDouble         a,
*       SpiceDouble         b,
*       SpiceDouble         c,
*       ConstSpiceDouble    linept[3],
*       ConstSpiceDouble    linedr[3],
*       SpiceDouble         pnear[3],
*       SpiceDouble       * dist      ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* a          I   Length of ellipsoid's semi-axis in the x direction 
* b          I   Length of ellipsoid's semi-axis in the y direction 
* c          I   Length of ellipsoid's semi-axis in the z direction 
* linept     I   Point on line 
* linedr     I   Direction vector of line 
* pnear      O   Nearest point on ellipsoid to line 
* dist       O   Distance of ellipsoid from line 
***********************************************************************/

%rename (npedln) npedln_c;

%apply (double  IN_ARRAY1[ANY]) {double linept[3]};
%apply (double  IN_ARRAY1[ANY]) {double linedr[3]};
%apply (double OUT_ARRAY1[ANY]) {double pnear[3]};
%apply (void RETURN_VOID) {void npedln_c};

extern void npedln_c (
        double a,
        double b,
        double c,
        double linept[3],
        double linedr[3],
        double pnear[3],
        double *OUTPUT);

/***********************************************************************
* -Procedure npelpt_c  ( Nearest point on ellipse to point )
*
* -Abstract
*
* Find the nearest point on an ellipse to a specified point, both 
* in three-dimensional space, and find the distance between the 
* ellipse and the point. 
*
* void npelpt_c (
*       ConstSpiceDouble      point  [3],
*       ConstSpiceEllipse   * ellips,
*       SpiceDouble           pnear  [3],
*       SpiceDouble         * dist       ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* point      I   Point whose distance to an ellipse is to be found. 
* ellips     I   A CSPICE ellipse. 
* pnear      O   Nearest point on ellipse to input point. 
* dist       O   Distance of input point to ellipse. 
***********************************************************************/

%rename (npelpt) npelpt_c;

%apply (double  IN_ARRAY1[ANY]) {double point[3]};
%apply (double OUT_ARRAY1[ANY]) {double ellipse[NELLIPSE]};
%apply (double OUT_ARRAY1[ANY]) {double pnear[3]};
%apply (void RETURN_VOID) {void npelpt_c};

extern void npelpt_c (
        double point[3],
        double ellipse[NELLIPSE],
        double pnear[3],
        double *OUTPUT);

/***********************************************************************
* -Procedure nplnpt_c ( Nearest point on line to point )
*
* -Abstract
*
* Find the nearest point on a line to a specified point, and find 
* the distance between the two points. 
*
* void nplnpt_c (
*       ConstSpiceDouble    linpt  [3],
*       ConstSpiceDouble    lindir [3],
*       ConstSpiceDouble    point  [3],
*       SpiceDouble         pnear  [3],
*       SpiceDouble       * dist       ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* linpt, 
* lindir     I   Point on a line and the line's direction vector. 
* point      I   A second point. 
* pnear      O   Nearest point on the line to point. 
* dist       O   Distance between point and pnear. 
***********************************************************************/

%rename (nplnpt) nplnpt_c;

%apply (double  IN_ARRAY1[ANY]) {double linpt [3]};
%apply (double  IN_ARRAY1[ANY]) {double lindir[3]};
%apply (double  IN_ARRAY1[ANY]) {double point [3]};
%apply (double OUT_ARRAY1[ANY]) {double pnear [3]};
%apply (void RETURN_VOID) {void nplnpt_c};

extern void nplnpt_c (
        double linpt [3],
        double lindir[3],
        double point [3],
        double pnear [3],
        double *OUTPUT);

/***********************************************************************
* -Procedure nvc2pl_c ( Normal vector and constant to plane )
*
* -Abstract
*
* Make a CSPICE plane from a normal vector and a constant. 
*
* void nvc2pl_c (
*       ConstSpiceDouble     normal[3],
*       SpiceDouble          constant,
*       SpicePlane        *  plane     ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* normal, 
* constant   I   A normal vector and constant defining a plane. 
* plane      O   A CSPICE plane structure representing the plane. 
***********************************************************************/

%rename (nvc2pl) nvc2pl_c;

%apply (double  IN_ARRAY1[ANY]) {double normal[3]};
%apply (double OUT_ARRAY1[ANY]) {double plane[NPLANE]};
%apply (void RETURN_VOID) {void nvc2pl_c};

extern void nvc2pl_c (
        double normal[3],
        double constant,
        double plane[NPLANE]);

/***********************************************************************
* -Procedure nvp2pl_c ( Normal vector and point to plane )
*
* -Abstract
*
* Make a CSPICE plane from a normal vector and a point. 
*
* void nvp2pl_c (
*       ConstSpiceDouble    normal[3],
*       ConstSpiceDouble    point [3],
*       SpicePlane        * plane     ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* normal, 
* point      I   A normal vector and a point defining a plane. 
* plane      O   A CSPICE plane structure representing the plane. 
***********************************************************************/

%rename (nvp2pl) nvp2pl_c;

%apply (double  IN_ARRAY1[ANY]) {double normal[3]};
%apply (double  IN_ARRAY1[ANY]) {double point[3]};
%apply (double OUT_ARRAY1[ANY]) {double plane[NPLANE]};
%apply (void RETURN_VOID) {void nvp2pl_c};

extern void nvp2pl_c (
        double normal[3],
        double point[3],
        double plane[NPLANE]);

/***********************************************************************
* -Procedure oscelt_c ( Determine conic elements from state )
*
* -Abstract
*
* Determine the set of osculating conic orbital elements that
* corresponds to the state (position, velocity) of a body at
* some epoch.
*
* void oscelt_c (
*       ConstSpiceDouble   state[6],
*       SpiceDouble        et,
*       SpiceDouble        mu,
*       SpiceDouble        elts[8]   )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* state      I   State of body at epoch of elements.
* et         I   Epoch of elements.
* mu         I   Gravitational parameter (GM) of primary body.
* elts       O   Equivalent conic elements
***********************************************************************/

%rename (oscelt) oscelt_c;

%apply (double  IN_ARRAY1[ANY]) {double state[6]};
%apply (double OUT_ARRAY1[ANY]) {double elts[8]};
%apply (void RETURN_VOID) {void oscelt_c};

extern void oscelt_c (
        double state[6],
        double et,
        double mu,
        double elts[8]);

/***********************************************************************
* -Procedure pcpool_c ( Put character strings into the kernel pool )
*
* -Abstract
*
* This entry point provides toolkit programmers a method for 
* programmatically inserting character data into the 
* kernel pool. 
*
* void pcpool_c (
*       ConstSpiceChar  * name,
*       SpiceInt          n,
*       SpiceInt          lenvals,
*       const void      * cvals    ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* name       I   The kernel pool name to associate with cvals. 
* n          I   The number of values to insert. 
* lenvals    I   The lengths of the strings in the array cvals.
* cvals      I   An array of strings to insert into the kernel pool. 
***********************************************************************/

%rename (pcpool) pcpool_c;

%apply (int DIM1, int DIM2, char *IN_STRINGS) {(int n, int lenvals,
                                                char *cvals)};
%apply (void RETURN_VOID) {void pcpool_c};

extern void pcpool_c (
        char *CONST_STRING,
        int n, int lenvals, char *cvals);

/***********************************************************************
* -Procedure pdpool_c ( Put d.p.'s into the kernel pool )
*
* -Abstract
*
* This entry point provides toolkit programmers a method for 
* programmatically inserting double precision data into the 
* kernel pool. 
*
* void pdpool_c (
*       ConstSpiceChar      * name,
*       SpiceInt              n,
*       ConstSpiceDouble    * dvals ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* name       I   The kernel pool name to associate with dvals. 
* n          I   The number of values to insert. 
* dvals      I   An array of values to insert into the kernel pool. 
***********************************************************************/

%rename (pdpool) pdpool_c;

%apply (int DIM1, double *IN_ARRAY1) {(int n, double *dvals)};
%apply (void RETURN_VOID) {void pdpool_c};

extern void pdpool_c (
        char *CONST_STRING,
        int n, double *dvals);

/***********************************************************************
* -Procedure pgrrec_c ( Planetographic to rectangular )
*
* -Abstract
*
* Convert planetographic coordinates to rectangular coordinates. 
*
* void pgrrec_c (
*       ConstSpiceChar  * body,
*       SpiceDouble       lon,
*       SpiceDouble       lat,
*       SpiceDouble       alt,
*       SpiceDouble       re,
*       SpiceDouble       f,
*       SpiceDouble       rectan[3] ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* body       I   Body with which coordinate system is associated. 
* lon        I   Planetographic longitude of a point (radians). 
* lat        I   Planetographic latitude of a point (radians). 
* alt        I   Altitude of a point above reference spheroid. 
* re         I   Equatorial radius of the reference spheroid. 
* f          I   Flattening coefficient. 
* rectan     O   Rectangular coordinates of the point. 
***********************************************************************/

%rename (pgrrec) pgrrec_c;

%apply (double OUT_ARRAY1[ANY]) {double rectan[3]};
%apply (void RETURN_VOID) {void pgrrec_c};

extern void pgrrec_c (
        char *CONST_STRING,
        double lon,
        double lat,
        double alt,
        double re,
        double f,
        double rectan[3]);

/***********************************************************************
* -Procedure pi_c ( Value of pi )
*
* -Abstract
*
* Return the value of pi (the ratio of the circumference of
* a circle to its diameter).
*
* SpiceDouble pi_c (
        void )
*
* -Brief_I/O
*
* The function returns the value of pi.
***********************************************************************/

%rename (pi) pi_c;

%apply (double RETURN_DOUBLE) {double pi_c};

extern double pi_c ( void );

/***********************************************************************
* -Procedure pipool_c ( Put integers into the kernel pool )
*
* -Abstract
*
* This entry point provides toolkit programmers a method for 
* programmatically inserting integer data into the kernel pool. 
*
* void pipool_c (
*       ConstSpiceChar  * name,
*       SpiceInt          n,
*       ConstSpiceInt   * ivals ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* name       I   The kernel pool name to associate with values. 
* n          I   The number of values to insert. 
* ivals      I   An array of integers to insert into the pool. 
***********************************************************************/

%rename (pipool) pipool_c;

%apply (int DIM1, int *IN_ARRAY1) {(int n, int *ivals)};
%apply (void RETURN_VOID) {void pipool_c};

extern void pipool_c (
        char *CONST_STRING,
        int n, int *ivals );

/***********************************************************************
* -Procedure pjelpl_c ( Project ellipse onto plane )
*
* -Abstract
*
* Project an ellipse onto a plane, orthogonally. 
*
* void pjelpl_c (
*       ConstSpiceEllipse  * elin,
*       ConstSpicePlane    * plane,
*       SpiceEllipse       * elout  ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* elin       I   A CSPICE ellipse to be projected. 
* plane      I   A plane onto which elin is to be projected. 
* elout      O   A CSPICE ellipse resulting from the projection. 
***********************************************************************/

%rename (pjelpl) pjelpl_c;

%apply (double  IN_ARRAY1[ANY]) {double elin [NELLIPSE]};
%apply (double  IN_ARRAY1[ANY]) {double plane[NPLANE]};
%apply (double OUT_ARRAY1[ANY]) {double elout[NELLIPSE]};
%apply (void RETURN_VOID) {void pjelpl_c};

extern void pjelpl_c (
        double elin [NELLIPSE],
        double plane[NPLANE],
        double elout[NELLIPSE]);

/***********************************************************************
* -Procedure pl2nvc_c ( Plane to normal vector and constant )
*
* -Abstract
*
* Return a unit normal vector and constant that define a specified 
* plane. 
*
* void pl2nvc_c (
*       ConstSpicePlane   * plane,
*       SpiceDouble         normal[3],
*       SpiceDouble       * constant  ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* plane      I   A CSPICE plane. 
* normal, 
* constant   O   A normal vector and constant defining the 
*                geometric plane represented by plane. 
***********************************************************************/

%rename (pl2nvc) pl2nvc_c;

%apply (double IN_ARRAY1[ANY]) {double plane[NPLANE]};
%apply (double IN_ARRAY1[ANY]) {double normal[3]};
%apply (void RETURN_VOID) {void pl2nvc_c};

extern void pl2nvc_c (
        double plane[NPLANE],
        double normal[3],
        double *OUTPUT);

/***********************************************************************
* -Procedure pl2nvp_c ( Plane to normal vector and point )
*
* -Abstract
*
* Return a unit normal vector and point that define a specified 
* plane. 
*
* void pl2nvp_c (
*       ConstSpicePlane   * plane,
*       SpiceDouble         normal[3],
*       SpiceDouble         point [3]  ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* plane      I   A CSPICE plane. 
* normal, 
* point      O   A unit normal vector and point that define plane. 
***********************************************************************/

%rename (pl2nvp) pl2nvp_c;

%apply (double  IN_ARRAY1[ANY]) {double plane[NPLANE]};
%apply (double OUT_ARRAY1[ANY]) {double normal[3]};
%apply (double OUT_ARRAY1[ANY]) {double point [3]}; 
%apply (void RETURN_VOID) {void pl2nvp_c};

extern void pl2nvp_c (
        double plane[NPLANE],
        double normal[3],
        double point [3]);

/***********************************************************************
* -Procedure pl2psv_c ( Plane to point and spanning vectors )
*
* -Abstract
*
* Return a point and two orthogonal spanning vectors that generate 
* a specified plane. 
*
* void pl2psv_c (
*       ConstSpicePlane  * plane,
*       SpiceDouble        point[3],
*       SpiceDouble        span1[3],
*       SpiceDouble        span2[3]  ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* plane      I   A CSPICE plane. 
* point, 
* span1, 
* span2      O   A point in the input plane and two vectors 
* spanning the input plane. 
***********************************************************************/

%rename (pl2psv) pl2psv_c;

%apply (double  IN_ARRAY1[ANY]) {double plane[NPLANE]};
%apply (double OUT_ARRAY1[ANY]) {double point[3]};
%apply (double OUT_ARRAY1[ANY]) {double span1[3]};
%apply (double OUT_ARRAY1[ANY]) {double span2[3]}; 
%apply (void RETURN_VOID) {void pl2psv_c};

extern void pl2psv_c (
        double plane[NPLANE],
        double point[3],
        double span1[3],
        double span2[3]);

/***********************************************************************
* -Procedure prop2b_c ( Propagate a two-body solution )
*
* -Abstract
*
* Given a central mass and the state of massless body at time t_0,
* this routine determines the state as predicted by a two-body
* force model at time t_0 + dt.
*
* void prop2b_c (
*       SpiceDouble         gm,
*       ConstSpiceDouble    pvinit[6],
*       SpiceDouble         dt,
*       SpiceDouble         pvprop[6] )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* gm         I   Gravity of the central mass.
* pvinit     I   Initial state from which to propagate a state.
* dt         I   Time offset from initial state to propagate to.
* pvprop     O   The propagated state.
***********************************************************************/

%rename (prop2b) prop2b_c;

%apply (double  IN_ARRAY1[ANY]) {double pvinit[6]};
%apply (double OUT_ARRAY1[ANY]) {double pvprop[6]};
%apply (void RETURN_VOID) {void prop2b_c};

extern void prop2b_c (
        double gm,
        double pvinit[6],
        double dt,
        double pvprop[6]);

/***********************************************************************
* -Procedure psv2pl_c ( Point and spanning vectors to plane )
*
* -Abstract
*
* Make a CSPICE plane from a point and two spanning vectors. 
*
* void psv2pl_c (
*       ConstSpiceDouble    point[3],
*       ConstSpiceDouble    span1[3],
*       ConstSpiceDouble    span2[3],
*       SpicePlane        * plane    ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* point, 
* span1, 
* span2      I   A point and two spanning vectors defining a plane. 
* plane      O   A CSPICE plane representing the plane. 
***********************************************************************/

%rename (psv2pl) psv2pl_c;

%apply (double  IN_ARRAY1[ANY]) {double point[3]};
%apply (double  IN_ARRAY1[ANY]) {double span1[3]};
%apply (double  IN_ARRAY1[ANY]) {double span2[3]};
%apply (double OUT_ARRAY1[ANY]) {double plane[NPLANE]};
%apply (void RETURN_VOID) {void psv2pl_c};

extern void psv2pl_c (
        double point[3],
        double span1[3],
        double span2[3],
        double plane[NPLANE]);

/***********************************************************************
* -Procedure pxform_c ( Position Transformation Matrix )
*
* -Abstract
*
* Return the matrix that transforms position vectors from one 
* specified frame to another at a specified epoch.
*
* void pxform_c (
*       ConstSpiceChar   * from,
*       ConstSpiceChar   * to,
*       SpiceDouble        et,
*       SpiceDouble        rotate[3][3] )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* from       I   Name of the frame to transform from.
* to         I   Name of the frame to transform to.
* et         I   Epoch of the rotation matrix.
* rotate     O   A rotation matrix.
***********************************************************************/

%rename (pxform) pxform_c;

%apply (double OUT_ARRAY2[ANY][ANY]) {double rotate[3][3]};
%apply (void RETURN_VOID) {void pxform_c};

extern void pxform_c (
        char *CONST_STRING,
        char *CONST_STRING,
        double et,
        double rotate[3][3]);

/***********************************************************************
* -Procedure      q2m_c ( Quaternion to matrix )
*
* -Abstract
*
* Find the rotation matrix corresponding to a specified unit 
* quaternion. 
*
* void q2m_c (
*       ConstSpiceDouble  q[4], 
*       SpiceDouble       r[3][3] ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* q          I   A unit quaternion. 
* r          O   A rotation matrix corresponding to q. 
***********************************************************************/

%rename (q2m) q2m_c;

%apply (double  IN_ARRAY1[ANY]     ) {double qin[4]};
%apply (double OUT_ARRAY2[ANY][ANY]) {double rout[3][3]};
%apply (void RETURN_VOID) {void q2m_c};

extern void q2m_c (
        double qin[4], 
        double rout[3][3]);

/***********************************************************************
* -Procedure qdq2av_c (Quaternion and quaternion derivative to a.v.)
*
* -Abstract
*
* Derive angular velocity from a unit quaternion and its derivative 
* with respect to time. 
*
* void qdq2av_c (
*       ConstSpiceDouble    q  [4],
*       ConstSpiceDouble    dq [4],
*       SpiceDouble         av [3]  ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* q          I   Unit SPICE quaternion. 
* dq         I   Derivative of `q' with respect to time. 
* av         O   Angular velocity defined by `q' and `dq'. 
***********************************************************************/

%rename (qdq2av) qdq2av_c;

%apply (double  IN_ARRAY1[ANY]) {double qin[4]};
%apply (double  IN_ARRAY1[ANY]) {double dq[4]};
%apply (double OUT_ARRAY1[ANY]) {double av[3]}; 
%apply (void RETURN_VOID) {void qdq2av_c};

extern void qdq2av_c (
        double qin[4],
        double dq[4],
        double av[3] );

/***********************************************************************
* -Procedure qxq_c ( Quaternion times quaternion )
*
* -Abstract
*
* Multiply two quaternions. 
*
* void qxq_c (
*       ConstSpiceDouble    q1   [4],
*       ConstSpiceDouble    q2   [4],
*       SpiceDouble         qout [4]  ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* q1         I   First SPICE quaternion factor. 
* q2         I   Second SPICE quaternion factor. 
* qout       O   Product of `q1' and `q2'. 
***********************************************************************/

%rename (qxq) qxq_c;

%apply (double  IN_ARRAY1[ANY]) {double q1  [4]};
%apply (double  IN_ARRAY1[ANY]) {double q2  [4]};
%apply (double OUT_ARRAY1[ANY]) {double qout[4]};
%apply (void RETURN_VOID) {void qxq_c};

extern void qxq_c (
        double q1  [4],
        double q2  [4],
        double qout[4] );

/***********************************************************************
* -Procedure radrec_c ( Range, RA and DEC to rectangular coordinates )
*
* -Abstract
*
* Convert from range, right ascension, and declination to rectangular
* coordinates.
*
* void radrec_c (
*       SpiceDouble range, 
*       SpiceDouble ra, 
*       SpiceDouble dec, 
*       SpiceDouble rectan[3] ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  --------------------------------------------------- 
* range      I   Distance of a point from the origin. 
* ra         I   Right ascension of point in radians. 
* dec        I   Declination of point in radians. 
* rectan     O   Rectangular coordinates of the point.
***********************************************************************/

%rename (radrec) radrec_c;

%apply (double OUT_ARRAY1[ANY]) {double rectan[3]};
%apply (void RETURN_VOID) {void radrec_c};

extern void radrec_c (
        double range, 
        double ra, 
        double dec, 
        double rectan[3] );

/***********************************************************************
* -Procedure rav2xf_c ( Rotation and angular velocity to transform )
*
* -Abstract
*
* This routine determines from a state transformation matrix 
* the associated rotation matrix and angular velocity of the 
* rotation. 
*
* void rav2xf_c (
*       ConstSpiceDouble    rot   [3][3],
*       ConstSpiceDouble    av    [3],
*       SpiceDouble         xform [6][6]  ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* rot        I   Rotation matrix.
* av         I   Angular velocity vector. 
* xform      O   State transformation associated with rot and av.
***********************************************************************/

%rename (rav2xf) rav2xf_c;

%apply (double  IN_ARRAY2[ANY][ANY]) {double rot  [3][3]};
%apply (double  IN_ARRAY1[ANY]     ) {double av   [3]};
%apply (double OUT_ARRAY2[ANY][ANY]) {double xform[6][6]};
%apply (void RETURN_VOID) {void rav2xf_c};

extern void rav2xf_c (
        double rot  [3][3],
        double av   [3],
        double xform[6][6] );

/***********************************************************************
* -Procedure raxisa_c ( Rotation axis of a matrix )
*
* -Abstract
*
* Compute the axis of the rotation given by an input matrix 
* and the angle of the rotation about that axis. 
*
* void raxisa_c (
*       ConstSpiceDouble     matrix[3][3],
*       SpiceDouble          axis  [3],
*       SpiceDouble        * angle       ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* matrix     I   3x3 rotation matrix in double precision. 
* axis       O   Axis of the rotation. 
* angle      O   Angle through which the rotation is performed. 
***********************************************************************/

%rename (raxisa) raxisa_c;

%apply (double  IN_ARRAY2[ANY][ANY]) {double matrix[3][3]};
%apply (double OUT_ARRAY1[ANY]     ) {double axis  [3]};
%apply (void RETURN_VOID) {void raxisa_c};

extern void raxisa_c (
        double matrix[3][3],
        double axis  [3],
        double *OUTPUT      );

/***********************************************************************
* -Procedure reccyl_c ( Rectangular to cylindrical coordinates )
*
* -Abstract
*
* Convert from rectangular to cylindrical coordinates. 
*
* void reccyl_c (
*       ConstSpiceDouble     rectan[3], 
*       SpiceDouble        * r, 
*       SpiceDouble        * lon, 
*       SpiceDouble        * z         ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  ------------------------------------------------- 
* rectan     I   Rectangular coordinates of a point. 
* r          O   Distance of the point from z axis. 
* lon        O   Angle (radians) of the point from xZ plane 
* z          O   Height of the point above xY plane. 
***********************************************************************/

%rename (reccyl) reccyl_c;

%apply (double IN_ARRAY1[ANY]) {double rectan1[3]}; 
%apply (void RETURN_VOID) {void reccyl_c};

extern void reccyl_c (
        double rectan1[3], 
        double *OUTPUT, 
        double *OUTPUT, 
        double *OUTPUT   );

/***********************************************************************
* -Procedure      recgeo_c ( Rectangular to geodetic )
*
* -Abstract
*
* Convert from rectangular coordinates to geodetic coordinates. 
*
* void recgeo_c (
*       ConstSpiceDouble     rectan[3], 
*       SpiceDouble          re, 
*       SpiceDouble          f, 
*       SpiceDouble        * lon,
*       SpiceDouble        * lat,
*       SpiceDouble        * alt        )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* rectan     I   Rectangular coordinates of a point. 
* re         I   Equatorial radius of the reference spheroid. 
* f          I   Flattening coefficient. 
* lon        O   Geodetic longitude of the point (radians). 
* lat        O   Geodetic latitude  of the point (radians). 
* alt        O   Altitude of the point above reference spheroid. 
***********************************************************************/

%rename (recgeo) recgeo_c;

%apply (double IN_ARRAY1[ANY]) {double rectan1[3]}; 
%apply (void RETURN_VOID) {void recgeo_c};

extern void recgeo_c (
        double rectan1[3], 
        double re, 
        double f, 
        double *OUTPUT,
        double *OUTPUT,
        double *OUTPUT   );

/***********************************************************************
* -Procedure   reclat_c ( Rectangular to latitudinal coordinates )
*
* -Abstract
*
* Convert from rectangular coordinates to latitudinal coordinates.
*
* void reclat_c (
*       ConstSpiceDouble    rectan[3],
*       SpiceDouble       * radius,
*       SpiceDouble       * longitude,
*       SpiceDouble       * latitude  )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* rectan     I   Rectangular coordinates of a point.
* radius     O   Distance of the point from the origin.
* longitude  O   Longitude of the point in radians.
* latitude   O   Latitude of the point in radians.
***********************************************************************/

%rename (reclat) reclat_c;

%apply (double IN_ARRAY1[ANY]) {double rectan1[3]};
%apply (void RETURN_VOID) {void reclat_c};

extern void reclat_c (
        double rectan1[3],
        double *OUTPUT,
        double *OUTPUT,
        double *OUTPUT   );

/***********************************************************************
* -Procedure recpgr_c ( Rectangular to planetographic )
*
* -Abstract
*
* Convert rectangular coordinates to planetographic coordinates. 
*
* void recpgr_c (
*       ConstSpiceChar   * body,
*       SpiceDouble        rectan[3],
*       SpiceDouble        re,
*       SpiceDouble        f,
*       SpiceDouble      * lon,
*       SpiceDouble      * lat,
*       SpiceDouble      * alt       ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* body       I   Body with which coordinate system is associated. 
* rectan     I   Rectangular coordinates of a point. 
* re         I   Equatorial radius of the reference spheroid. 
* f          I   Flattening coefficient. 
* lon        O   Planetographic longitude of the point (radians). 
* lat        O   Planetographic latitude of the point (radians). 
* alt        O   Altitude of the point above reference spheroid. 
***********************************************************************/

%rename (recpgr) recpgr_c;

%apply (double IN_ARRAY1[ANY]) {double rectan1[3]};
%apply (void RETURN_VOID) {void recpgr_c};

extern void recpgr_c (
        char *CONST_STRING,
        double rectan1[3],
        double re,
        double f,
        double *OUTPUT,
        double *OUTPUT,
        double *OUTPUT   );

/***********************************************************************
* -Procedure recrad_c ( Rectangular coordinates to RA and DEC )
*
* -Abstract
*
* Convert rectangular coordinates to range, right ascension, and
* declination.
*
* void recrad_c (
*       ConstSpiceDouble    rectan[3],
*       SpiceDouble       * range,
*       SpiceDouble       * ra,
*       SpiceDouble       * dec      ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* rectan     I   Rectangular coordinates of a point. 
* range      O   Distance of the point from the origin. 
* ra         O   Right ascension in radians. 
* dec        O   Declination in radians. 
***********************************************************************/

%rename (recrad) recrad_c;

%apply (double IN_ARRAY1[ANY]) {double rectan[3]};
%apply (void RETURN_VOID) {void recrad_c};

extern void recrad_c (
        double rectan[3],
        double *OUTPUT,
        double *OUTPUT,
        double *OUTPUT   );

/***********************************************************************
* -Procedure      recsph_c ( Rectangular to spherical coordinates )
*
* -Abstract
*
* Convert from rectangular coordinates to spherical coordinates. 
*
* void recsph_c (
*       ConstSpiceDouble     rectan[3], 
*       SpiceDouble        * r, 
*       SpiceDouble        * colat,
*       SpiceDouble        * lon      ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* rectan     I   Rectangular coordinates of a point. 
* r          O   Distance of the point from the origin. 
* colat      O   Angle of the point from the positive Z-axis. 
* lon        O   Longitude of the point in radians. 
***********************************************************************/

%rename (recsph) recsph_c;

%apply (double IN_ARRAY1[ANY]) {double rectan[3]};
%apply (void RETURN_VOID) {void recsph_c};

extern void recsph_c (
        double rectan[3], 
        double *OUTPUT, 
        double *OUTPUT,
        double *OUTPUT   );

/***********************************************************************
* -Procedure refchg_
*
* -Abstract
*
* Return the transformation matrix from one frame to another.
*
* int refchg_ (
*       SpiceInt      *frame1,
*       SpiceInt      *frame2,
*       SpiceDouble   *et,
*       SpiceDouble   *rotate  )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* frame1     I   the frame id-code for some reference frame
* frame2     I   the frame id-code for some reference frame
* et         I   an epoch in TDB seconds past J2000.
* rotate     O   a rotation matrix
***********************************************************************/

%rename (refchg) my_refchg;

%apply (double OUT_ARRAY2[ANY][ANY]) {double rotate[3][3]};
%apply (void RETURN_VOID) {void my_refchg};

/* Helper function to deal with pointers to input arguments */
%inline %{
    void my_refchg(int frame1, int frame2, double et, double rotate[3][3]) {
        refchg_(&frame1, &frame2, &et, rotate);
    }
%}

extern void refchg_(int *frame1, int *frame2, double *et, double *rotate);

/***********************************************************************
* -Procedure repmc_c  ( Replace marker with character string )
*
* -Abstract
*
* Replace a marker with a character string. 
*
* void repmc_c (
*       ConstSpiceChar    * in,
*       ConstSpiceChar    * marker,
*       ConstSpiceChar    * value,
*       SpiceInt            lenout,
*       SpiceChar         * out    ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* in         I   Input string. 
* marker     I   Marker to be replaced. 
* value      I   Replacement value.
* lenout     I   Available space in output string.
* out        O   Output string. 
***********************************************************************/

%rename (repmc) repmc_c;

%apply (int DIM1, char OUT_STRING[ANY]) {(int lenout, char out[1024])};
%apply (void RETURN_VOID) {void repmc_c};

extern void repmc_c (
        char *CONST_STRING,
        char *CONST_STRING,
        char *CONST_STRING,
        int lenout, char out[1024] );

/***********************************************************************
* -Procedure repmct_c  ( Replace marker with cardinal text )
*
* -Abstract
*
* Replace a marker with the text representation of a 
* cardinal number. 
*
* void repmct_c (
*       ConstSpiceChar   * in,
*       ConstSpiceChar   * marker,
*       SpiceInt           value,
*       SpiceChar          repcase,
*       SpiceInt           lenout,
*       SpiceChar        * out      ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* in         I   Input string. 
* marker     I   Marker to be replaced. 
* value      I   Replacement value.
* repcase    I   Case of replacement text. 
* lenout     I   Available space in output string.
* out        O   Output string. 
* MAXLCN     P   is the maximum expected length of any cardinal text.
***********************************************************************/

%rename (repmct) repmct_c;

%apply (int DIM1, char OUT_STRING[ANY]) {(int lenout, char out[1024])};
%apply (void RETURN_VOID) {void repmct_c};

extern void repmct_c(
        char *CONST_STRING,
        char *CONST_STRING,
        int value,
        char IN_STRING,
        int lenout, char out[1024]);

/***********************************************************************
* -Procedure repmd_c  ( Replace marker with double precision number )
*
* -Abstract
*
* Replace a marker with a double precision number. 
*
* void repmd_c (
*       ConstSpiceChar     * in,
*       ConstSpiceChar     * marker,
*       SpiceDouble          value,
*       SpiceInt             sigdig,
*       SpiceInt             lenout,
*       SpiceChar          * out     ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* in         I   Input string. 
* marker     I   Marker to be replaced. 
* value      I   Replacement value.
* sigdig     I   Significant digits in replacement text.
* lenout     I   Available space in output string.
* out        O   Output string. 
* MAXLDP     P   Maximum length of a d.p. number. 
***********************************************************************/

%rename (repmd) repmd_c;

%apply (int DIM1, char OUT_STRING[ANY]) {(int lenout,
                                          char out[1024])};
%apply (void RETURN_VOID) {void repmd_c};

extern void repmd_c (
        char *CONST_STRING,
        char *CONST_STRING,
        double value,
        int sigdig,
        int lenout, char out[1024] );

/***********************************************************************
* -Procedure repmf_c  ( Replace marker with formatted d.p. value )
*
* -Abstract
*
* Replace a marker in a string with a formatted double precision 
* value. 
*
* void repmf_c (
*       ConstSpiceChar     * in,
*       ConstSpiceChar     * marker,
*       SpiceDouble          value,
*       SpiceInt             sigdig,
*       SpiceChar            format,
*       SpiceInt             lenout,
*       SpiceChar          * out ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* in         I   Input string. 
* marker     I   Marker to be replaced. 
* value      I   Replacement value.
* sigdig     I   Significant digits in replacement text.
* format     I   Format: 'E' or 'F'. 
* lenout     I   Available space in output string.
* out        O   Output string. 
* MAXLFD     P   Maximum length of a formatted DP number. 
***********************************************************************/

%rename (repmf) repmf_c;

%apply (char IN_STRING) {char format};
%apply (int DIM1, char OUT_STRING[ANY]) {(int lenout,
                                          char out[1024])};
%apply (void RETURN_VOID) {void repmf_c};

extern void repmf_c (
        char *CONST_STRING,
        char *CONST_STRING,
        double value,
        int sigdig,
        char format,
        int lenout, char out[1024] );

/***********************************************************************
* -Procedure repmi_c  ( Replace marker with integer )
*
* -Abstract
*
* Replace a marker with an integer. 
*
* void repmi_c (
*       ConstSpiceChar     * in,
*       ConstSpiceChar     * marker,
*       SpiceInt             value,
*       SpiceInt             lenout,
*       SpiceChar          * out     ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* in         I   Input string. 
* marker     I   Marker to be replaced. 
* value      I   Replacement value.
* lenout     I   Available space in output string.
* out        O   Output string. 
* MAXLI      P   Maximum length of an integer. 
***********************************************************************/

%rename (repmi) repmi_c;

%apply (int DIM1, char OUT_STRING[ANY]) {(int lenout, char out[1024])};
%apply (void RETURN_VOID) {void repmi_c};

extern void repmi_c (
        char *CONST_STRING,
        char *CONST_STRING,
        int value,
        int lenout, char *out );

/***********************************************************************
* -Procedure repmot_c  ( Replace marker with ordinal text )
*
* -Abstract
*
* Replace a marker with the text representation of an ordinal number.
*
* void repmot_c (
*       ConstSpiceChar   * in,
*       ConstSpiceChar   * marker,
*       SpiceInt           value,
*       SpiceChar          repcase,
*       SpiceInt           lenout,
*       SpiceChar        * out      ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* in         I   Input string. 
* marker     I   Marker to be replaced. 
* value      I   Replacement value.
* repcase    I   Case of replacement text. 
* lenout     I   Available space in output string.
* out        O   Output string. 
* MAXLON     P   Maximum length of an ordinal number. 
***********************************************************************/

%rename (repmot) repmot_c;

%apply (int DIM1, char OUT_STRING[ANY]) {(int lenout,
                                            char out[1024])};
%apply (void RETURN_VOID) {void repmot_c};

extern void repmot_c(
        char *CONST_STRING,
        char *CONST_STRING,
        int value,
        char IN_STRING,
        int lenout, char out[1024]);

/***********************************************************************
* -Procedure reset_c ( Reset Error Status )
*
* -Abstract
*
* Reset the CSPICE error status to a value of "no error."
* as a result, the status routine, failed_c, will return a value
* of SPICEFALSE
*
* void reset_c (
        void )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* None.
***********************************************************************/

%rename (reset) reset_c;

%apply (void RETURN_VOID) {void reset_c};

extern void reset_c ( void );

/***********************************************************************
* -Procedure      rotate_c ( Generate a rotation matrix )
*
* -Abstract
*
* Calculate the 3x3 rotation matrix generated by a rotation 
* of a specified angle about a specified axis. This rotation 
* is thought of as rotating the coordinate system. 
*
* void rotate_c (
*       SpiceDouble     angle, 
*       SpiceInt        iaxis, 
*       SpiceDouble     mout[3][3] ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* angle      I   Angle of rotation (radians). 
* iaxis      I   Axis of rotation (X=1, Y=2, Z=3). 
* mout       O   Resulting rotation matrix [angle] 
* iaxis 
***********************************************************************/

%rename (rotate) rotate_c;

%apply (double OUT_ARRAY2[ANY][ANY]) {double mout[3][3]};
%apply (void RETURN_VOID) {void rotate_c};

extern void rotate_c (
        double angle, 
        int iaxis, 
        double mout[3][3] );

/***********************************************************************
* -Procedure      rotmat_c ( Rotate a matrix )
*
* -Abstract
*
* rotmat_c applies a rotation of angle radians about axis iaxis to a 
* matrix.  This rotation is thought of as rotating the coordinate 
* system. 
*
* void rotmat_c (
*       ConstSpiceDouble   m1[3][3], 
*       SpiceDouble        angle, 
*       SpiceInt           iaxis, 
*       SpiceDouble        mout[3][3] ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* m1        I     Matrix to be rotated. 
* angle     I     Angle of rotation (radians). 
* iaxis     I     Axis of rotation (X=1, Y=2, Z=3). 
* mout      O     Resulting rotated matrix.
***********************************************************************/

%rename (rotmat) rotmat_c;

%apply (double  IN_ARRAY2[ANY][ANY]) {double m1  [3][3]}; 
%apply (double OUT_ARRAY2[ANY][ANY]) {double mout[3][3]};
%apply (void RETURN_VOID) {void rotmat_c};

extern void rotmat_c (
        double m1[3][3], 
        double angle, 
        int iaxis, 
        double mout[3][3] );

/***********************************************************************
* -Procedure  rotvec_c ( Transform a vector via a rotation )
*
* -Abstract
*
* Transform a vector to a new coordinate system rotated by angle 
* radians about axis iaxis.  This transformation rotates v1 by 
* -angle radians about the specified axis.
*
* void rotvec_c (
*       ConstSpiceDouble  v1    [3],
*       SpiceDouble       angle, 
*       SpiceInt          iaxis, 
*       SpiceDouble       vout  [3] ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* v1        I    Vector whose coordinate system is to be rotated. 
* angle     I    Angle of rotation in radians. 
* iaxis     I    Axis of rotation (X=1, Y=2, Z=3). 
* vout      O    Resulting vector [angle]
***********************************************************************/

%rename (rotvec) rotvec_c;

%apply (double  IN_ARRAY1[ANY]) {double v1  [3]};
%apply (double OUT_ARRAY1[ANY]) {double vout[3]};
%apply (void RETURN_VOID) {void rotvec_c};

extern void rotvec_c (
        double v1[3],
        double angle, 
        int iaxis, 
        double vout[3] );

/***********************************************************************
* -Procedure  rpd_c ( Radians per degree ) 
*
* -Abstract
*
* Return the number of radians per degree.
*
* SpiceDouble rpd_c (
        void )
*
* -Brief_I/O
*
* The function returns the number of radians per degree. 
***********************************************************************/

%rename (rpd) rpd_c;

%apply (double RETURN_DOUBLE) {double rpd_c};

extern double rpd_c ( void );

/***********************************************************************
* -Procedure rquad_c ( Roots of a quadratic equation )
*
* -Abstract
*
* Find the roots of a quadratic equation. 
*
* void rquad_c (
*       SpiceDouble  a,
*       SpiceDouble  b,
*       SpiceDouble  c,
*       SpiceDouble  root1[2],
*       SpiceDouble  root2[2] ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* a          I   Coefficient of quadratic term. 
* b          I   Coefficient of linear term. 
* c          I   Constant. 
* root1      O   Root built from positive discriminant term. 
* root2      O   Root built from negative discriminant term. 
***********************************************************************/

%rename (rquad) rquad_c;

%apply (double OUT_ARRAY1[ANY]) {double root1[2]};
%apply (double OUT_ARRAY1[ANY]) {double root2[2]};
%apply (void RETURN_VOID) {void rquad_c};

extern void rquad_c (
        double a,
        double b,
        double c,
        double root1[2],
        double root2[2] );

/***********************************************************************
* -Procedure saelgv_c ( Semi-axes of ellipse from generating vectors )
*
* -Abstract
*
* Find semi-axis vectors of an ellipse generated by two arbitrary 
* three-dimensional vectors. 
*
* void saelgv_c (
*       ConstSpiceDouble   vec1  [3],
*       ConstSpiceDouble   vec2  [3],
*       SpiceDouble        smajor[3],
*       SpiceDouble        sminor[3]  ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* vec1, 
* vec2       I   Two vectors used to generate an ellipse. 
* smajor     O   Semi-major axis of ellipse. 
* sminor     O   Semi-minor axis of ellipse. 
***********************************************************************/

%rename (saelgv) saelgv_c;

%apply (double  IN_ARRAY1[ANY]) {double vec1  [3]};
%apply (double  IN_ARRAY1[ANY]) {double vec2  [3]};
%apply (double OUT_ARRAY1[ANY]) {double smajor[3]};
%apply (double OUT_ARRAY1[ANY]) {double sminor[3]}; 
%apply (void RETURN_VOID) {void saelgv_c};

extern void saelgv_c (
        double vec1  [3],
        double vec2  [3],
        double smajor[3],
        double sminor[3] );

/***********************************************************************
* -Procedure      scdecd_c ( Decode spacecraft clock )
*
* -Abstract
*
* Convert double precision encoding of spacecraft clock time into 
* a character representation. 
*
* void scdecd_c (
*       SpiceInt       sc, 
*       SpiceDouble    sclkdp, 
*       SpiceInt       lenout,
*       SpiceChar    * sclkch  ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* sc         I   NAIF spacecraft identification code. 
* sclkdp     I   Encoded representation of a spacecraft clock count.
* lenout     I   Maximum allowed length of output SCLK string. 
* sclkch     O   Character representation of a clock count. 
* MXPART     P   Maximum number of spacecraft clock partitions. 
***********************************************************************/

%rename (scdecd) scdecd_c;

%apply (int DIM1, char OUT_STRING[ANY]) {(int lenout,
                                            char sclkch[256])};
%apply (void RETURN_VOID) {void scdecd_c};

extern void scdecd_c (
        int sc, 
        double sclkdp, 
        int lenout, char sclkch[256]);

/***********************************************************************
* -Procedure sce2c_c ( ET to continuous SCLK ticks )
*
* -Abstract
*
* Convert ephemeris seconds past j2000_c (ET) to continuous encoded  
* spacecraft clock (`ticks').  Non-integral tick values may be 
* returned. 
*
* void sce2c_c (
*       SpiceInt       sc,
*       SpiceDouble    et,
*       SpiceDouble  * sclkdp ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* sc         I   NAIF spacecraft ID code. 
* et         I   Ephemeris time, seconds past j2000_c. 
* sclkdp     O   SCLK, encoded as ticks since spacecraft clock 
*                start.  sclkdp need not be integral. 
***********************************************************************/

%rename (sce2c) sce2c_c;

%apply (void RETURN_VOID) {void sce2c_c};

extern void sce2c_c (
        int sc,
        double et,
        double *OUTPUT );

/***********************************************************************
* -Procedure      sce2s_c ( ET to SCLK string )
*
* -Abstract
*
* Convert an epoch specified as ephemeris seconds past J2000 (ET) to a
* character string representation of a spacecraft clock value (SCLK).
*
* void sce2s_c (
*       SpiceInt        sc, 
*       SpiceDouble     et, 
*       SpiceInt        lenout,
*       SpiceChar     * sclkch  ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* sc         I   NAIF spacecraft clock ID code. 
* et         I   Ephemeris time, specified as seconds past J2000. 
* lenout     I   Maximum length of output string.
* sclkch     O   An SCLK string. 
***********************************************************************/

%rename (sce2s) sce2s_c;

%apply (int DIM1, char OUT_STRING[ANY]) {(int lenout,
                                          char sclkch[256])};
%apply (void RETURN_VOID) {void sce2s_c};

extern void sce2s_c (
        int sc, 
        double et, 
        int lenout, char sclkch[256]);

/***********************************************************************
* -Procedure      sce2t_c ( ET to SCLK ticks )
*
* -Abstract
*
* Convert ephemeris seconds past J2000 (ET) to integral
* encoded spacecraft clock (`ticks'). For conversion to
* fractional ticks, (required for C-kernel production), see
* the routine sce2c_c..
*
* void sce2t_c (
*       SpiceInt       sc, 
*       SpiceDouble    et, 
*       SpiceDouble  * sclkdp ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* sc         I   NAIF spacecraft ID code. 
* et         I   Ephemeris time, seconds past J2000. 
* sclkdp     O   SCLK, encoded as ticks since spacecraft clock 
* start. 
***********************************************************************/

%rename (sce2t) sce2t_c;

%apply (void RETURN_VOID) {void sce2t_c};

extern void sce2t_c (
        int sc, 
        double et, 
        double *OUTPUT );

/***********************************************************************
* -Procedure      scencd_c ( Encode spacecraft clock )
*
* -Abstract
*
* Encode character representation of spacecraft clock time into a 
* double precision number. 
*
* void scencd_c (
*       SpiceInt           sc, 
*       ConstSpiceChar   * sclkch, 
*       SpiceDouble      * sclkdp ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* sc         I   NAIF spacecraft identification code. 
* sclkch     I   Character representation of a spacecraft clock. 
* sclkdp     O   Encoded representation of the clock count. 
* MXPART     P   Maximum number of spacecraft clock partitions. 
***********************************************************************/

%rename (scencd) scencd_c;

%apply (void RETURN_VOID) {void scencd_c};

extern void scencd_c (
        int sc, 
        char *CONST_STRING, 
        double *OUTPUT );

/***********************************************************************
* -Procedure scfmt_c ( Convert SCLK "ticks" to character clock format)
*
* -Abstract
*
* Convert encoded spacecraft clock ticks to character clock format. 
*
* void scfmt_c (
*       SpiceInt      sc, 
*       SpiceDouble   ticks, 
*       SpiceInt      lenout,
*       SpiceChar   * clkstr  )
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* sc         I   NAIF spacecraft identification code. 
* ticks      I   Encoded representation of a spacecraft clock count. 
* lenout     I   Maximum allowed length of output string. 
* clkstr     O   Character representation of a clock count. 
***********************************************************************/

%rename (scfmt) scfmt_c;

%apply (int DIM1, char OUT_STRING[ANY]) {(int lenout,
                                            char clkstr[256])};
%apply (void RETURN_VOID) {void scfmt_c};

extern void scfmt_c (
        int sc, 
        double ticks, 
        int lenout, char clkstr[256]);

/***********************************************************************
* -Procedure      scpart_c ( Spacecraft Clock Partition Information )
*
* -Abstract
*
* Get spacecraft clock partition information from a spacecraft 
* clock kernel file. 
*
* Global constants
* void scpart_c (
*       SpiceInt        sc, 
*       SpiceInt      * nparts, 
*       SpiceDouble   * pstart, 
*       SpiceDouble   * pstop  ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* sc         I   NAIF spacecraft identification code. 
* nparts     O   The number of spacecraft clock partitions. 
* pstart     O   Array of partition start times. 
* pstop      O   Array of partition stop times. 
* MXPART     P   Maximum number of partitions. 
***********************************************************************/

%rename (scpart) my_scpart_c;

/* Helper function to return results as a 2-D array */
%apply (double OUT_ARRAY2[ANY][ANY], int *SIZE1)
                        {(double pstartstop[100][2], int *nparts)};
%apply (void RETURN_VOID) {void my_scpart_c};

%inline %{
    void my_scpart_c(int sc, double pstartstop[100][2], int *nparts) {
        double  pstart[100], pstop[100];
        int     j;

        scpart_c(sc, nparts, pstart, pstop);

        for (j = 0; j < *nparts; j++) {
            pstartstop[j][0] = pstart[j];
            pstartstop[j][1] = pstop[j];
        }
    }
%}

/***********************************************************************
* -Procedure      scs2e_c ( SCLK string to ET )
*
* -Abstract
*
* Convert a spacecraft clock string to ephemeris seconds past 
* J2000 (ET). 
*
* void scs2e_c (
*       SpiceInt          sc, 
*       ConstSpiceChar  * sclkch, 
*       SpiceDouble     * et      ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* sc         I   NAIF integer code for a spacecraft. 
* sclkch     I   An SCLK string. 
* et         O   Ephemeris time, seconds past J2000. 
***********************************************************************/

%rename (scs2e) scs2e_c;

%apply (void RETURN_VOID) {void scs2e_c};

extern void scs2e_c (
        int sc, 
        char *CONST_STRING, 
        double *OUTPUT );

/***********************************************************************
* -Procedure      sct2e_c ( SCLK ticks to ET )
*
* -Abstract
*
* Convert encoded spacecraft clock (`ticks') to ephemeris 
* seconds past J2000 (ET). 
*
* void sct2e_c (
*       SpiceInt       sc, 
*       SpiceDouble    sclkdp, 
*       SpiceDouble  * et     ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* sc         I   NAIF spacecraft ID code. 
* sclkdp     I   SCLK, encoded as ticks since spacecraft clock 
*                start. 
* et         O   Ephemeris time, seconds past J2000. 
***********************************************************************/

%rename (sct2e) sct2e_c;
%apply (void RETURN_VOID) {void sct2e_c};

extern void sct2e_c (
        int sc, 
        double sclkdp, 
        double *OUTPUT );

/***********************************************************************
* -Procedure      sctiks_c ( Convert spacecraft clock string to ticks. )
*
* -Abstract
*
* Convert a spacecraft clock format string to number of "ticks". 
*
* void sctiks_c (
*       SpiceInt           sc, 
*       ConstSpiceChar   * clkstr, 
*       SpiceDouble      * ticks   ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* sc         I   NAIF spacecraft identification code. 
* clkstr     I   Character representation of a spacecraft clock. 
* ticks      O   Number of ticks represented by the clock string. 
***********************************************************************/

%rename (sctiks) sctiks_c;

%apply (void RETURN_VOID) {void sctiks_c};

extern void sctiks_c (
        int sc, 
        char *CONST_STRING, 
        double *OUTPUT );

/***********************************************************************
* -Procedure setmsg_c  ( Set Long Error Message )
*
* -Abstract
*
* Set the value of the current long error message.
*
* void setmsg_c (
*       ConstSpiceChar * message )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* message    I   A long error message.
***********************************************************************/

%rename (setmsg) setmsg_c;

%apply (void RETURN_VOID) {void setmsg_c};

extern void setmsg_c (
        char *CONST_STRING );

/***********************************************************************
* -Procedure sigerr_c ( Signal Error Condition )
*
* -Abstract
*
* Inform the CSPICE error processing mechanism that an error has 
* occurred, and specify the type of error. 
*
* void sigerr_c (
*       ConstSpiceChar * message )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* msg        I   A short error message. 
***********************************************************************/

%rename (sigerr) sigerr_c;

%apply (void RETURN_VOID) {void sigerr_c};

extern void sigerr_c (
        char *CONST_STRING );

/***********************************************************************
* -Procedure  spd_c ( Seconds per day )
*
* -Abstract
*
* Return the number of seconds in a day.
*
* SpiceDouble spd_c (
        void )
*
* -Brief_I/O
*
* The function returns the number of seconds in a day.
***********************************************************************/

%rename (spd) spd_c;

%apply (double RETURN_DOUBLE) {double spd_c};

extern double spd_c ( void );

/***********************************************************************
* -Procedure sphcyl_c ( Spherical to cylindrical coordinates )
*
* -Abstract
*
* This routine converts from spherical coordinates to cylindrical 
* coordinates. 
*
* void sphcyl_c (
*       SpiceDouble     radius,
*       SpiceDouble     colat,
*       SpiceDouble     slon,
*       SpiceDouble   * r,
*       SpiceDouble   * lon,
*       SpiceDouble   * z ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  ------------------------------------------------- 
* radius     I   Distance of point from origin. 
* colat      I   Polar angle (co-latitude in radians) of point. 
* slon       I   Azimuthal angle (longitude) of point (radians). 
* r          O   Distance of point from z axis. 
* lon        O   angle (radians) of point from XZ plane. 
* z          O   Height of point above XY plane. 
***********************************************************************/

%rename (sphcyl) sphcyl_c;
%apply (void RETURN_VOID) {void sphcyl_c};

extern void sphcyl_c (
        double radius,
        double colat,
        double slon,
        double *OUTPUT,
        double *OUTPUT,
        double *OUTPUT );

/***********************************************************************
* -Procedure sphlat_c ( Spherical to latitudinal coordinates )
*
* -Abstract
*
* Convert from spherical coordinates to latitudinal coordinates. 
*
* void sphlat_c (
*       SpiceDouble     r, 
*       SpiceDouble     colat, 
*       SpiceDouble     lons,
*       SpiceDouble   * radius,
*       SpiceDouble   * lon, 
*       SpiceDouble   * lat ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* r          I   Distance of the point from the origin. 
* colat      I   Angle of the point from positive z axis (radians). 
* lons       I   Angle of the point from the XZ plane (radians). 
* radius     O   Distance of a point from the origin 
* lon        O   Angle of the point from the XZ plane in radians 
* lat        O   Angle of the point from the XY plane in radians 
***********************************************************************/

%rename (sphlat) sphlat_c;
%apply (void RETURN_VOID) {void sphlat_c};

extern void sphlat_c (
        double r, 
        double colat, 
        double lons,
        double *OUTPUT,
        double *OUTPUT, 
        double *OUTPUT );

/***********************************************************************
* -Procedure sphrec_c ( Spherical to rectangular coordinates )
*
* -Abstract
*
* Convert from spherical coordinates to rectangular coordinates. 
*
* void sphrec_c (
*       SpiceDouble    r,
*       SpiceDouble    colat, 
*       SpiceDouble    lon,
*       SpiceDouble    rectan[3] ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* r          I   Distance of a point from the origin. 
* colat      I   Angle of the point from the positive Z-axis. 
* lon        I   Angle of the point from the XZ plane in radians. 
* rectan     O   Rectangular coordinates of the point. 
***********************************************************************/

%rename (sphrec) sphrec_c;

%apply (double OUT_ARRAY1[ANY]) {double rectan[3]};
%apply (void RETURN_VOID) {void sphrec_c};

extern void sphrec_c (
        double r,
        double colat, 
        double lon,
        double rectan[3] );

/***********************************************************************
* -Procedure spkapo_c ( S/P Kernel, apparent position only )
*
* -Abstract
*
* Return the position of a target body relative to an observer, 
* optionally corrected for light time and stellar aberration. 
*
* void spkapo_c (
*       SpiceInt               targ,
*       SpiceDouble            et,
*       ConstSpiceChar       * ref,
*       ConstSpiceDouble       sobs[6],
*       ConstSpiceChar       * abcorr,
*       SpiceDouble            ptarg[3],
*       SpiceDouble          * lt        ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* targ       I   Target body. 
* et         I   Observer epoch. 
* ref        I   Inertial reference frame of observer's state. 
* sobs       I   State of observer wrt. solar system barycenter. 
* abcorr     I   Aberration correction flag. 
* ptarg      O   Position of target. 
* lt         O   One way light time between observer and target. 
***********************************************************************/

%rename (spkapo) spkapo_c;

%apply (double  IN_ARRAY1[ANY]) {double sobs [6]};
%apply (double OUT_ARRAY1[ANY]) {double ptarg[3]};
%apply (void RETURN_VOID) {void spkapo_c};

extern void spkapo_c (
        int targ,
        double et,
        char *CONST_STRING,
        double sobs[6],
        char *CONST_STRING,
        double ptarg[3],
        double *OUTPUT );

/***********************************************************************
* -Procedure spkapp_c ( S/P Kernel, apparent state )
*
* -Abstract
*
* Return the state (position and velocity) of a target body 
* relative to an observer, optionally corrected for light time and 
* stellar aberration. 
*
* void spkapp_c (
*       SpiceInt             targ,
*       SpiceDouble          et,
*       ConstSpiceChar     * ref,
*       ConstSpiceDouble     sobs   [6],
*       ConstSpiceChar     * abcorr,
*       SpiceDouble          starg  [6],
*       SpiceDouble        * lt         ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* targ       I   Target body. 
* et         I   Observer epoch. 
* ref        I   Inertial reference frame of observer's state. 
* sobs       I   State of observer wrt. solar system barycenter. 
* abcorr     I   Aberration correction flag. 
* starg      O   State of target. 
* lt         O   One way light time between observer and target. 
***********************************************************************/

%rename (spkapp) spkapp_c;

%apply (double  IN_ARRAY1[ANY]) {double sobs [6]};
%apply (double OUT_ARRAY1[ANY]) {double starg[6]};
%apply (void RETURN_VOID) {void spkapp_c};

extern void spkapp_c (
        int targ,
        double et,
        char *CONST_STRING,
        double sobs[6],
        char *CONST_STRING,
        double starg[6],
        double *OUTPUT );

/***********************************************************************
* -Procedure spkcov_c ( SPK coverage )
*
* -Abstract
*
* Find the coverage window for a specified ephemeris object in a 
* specified SPK file. 
*
* void spkcov_c (
*       ConstSpiceChar  * spk,
*       SpiceInt          idcode,
*       SpiceCell       * cover   ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* spk        I   Name of SPK file. 
* idcode     I   ID code of ephemeris object. 
* cover      O   Window giving coverage in `spk' for `idcode'. 
***********************************************************************/

%rename (spkcov) my_spkcov_c;

%apply (char *CONST_STRING) {char *spk};
%apply (double OUT_ARRAY2[ANY][ANY], int *SIZE1)
                        {(double array[500][2], int *intervals)};
%apply (void RETURN_VOID) {void my_spkcov_c};

%inline %{
    /* Helper function to create a 2-D array of results */
    void my_spkcov_c(char *spk, int idcode,
                     double array[500][2], int *intervals) {

        int     j;
        SPICEDOUBLE_CELL(coverage, 2 * 500);

        scard_c(0, &coverage);
        spkcov_c(spk, idcode, &coverage);

        *intervals = (int) card_c(&coverage) / 2;
        for (j = 0; j < *intervals; j++) {
            wnfetd_c(&coverage, j, &(array[j][0]), &(array[j][1]));
        }
    }
%}

/***********************************************************************
* -Procedure spkez_c ( S/P Kernel, easy reader )
*
* -Abstract
*
* Return the state (position and velocity) of a target body 
* relative to an observing body, optionally corrected for light 
* time (planetary aberration) and stellar aberration. 
*
* void spkez_c (
*       SpiceInt            targ,
*       SpiceDouble         et,
*       ConstSpiceChar     *ref,
*       ConstSpiceChar     *abcorr,
*       SpiceInt            obs,
*       SpiceDouble         starg[6],
*       SpiceDouble        *lt        )
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* targ       I   Target body. 
* et         I   Observer epoch. 
* ref        I   Reference frame of output state vector. 
* abcorr     I   Aberration correction flag. 
* obs        I   Observing body. 
* starg      O   State of target. 
* lt         O   One way light time between observer and target. 
***********************************************************************/

%rename (spkez) spkez_c;

%apply (double OUT_ARRAY1[ANY]) {double starg[6]};
%apply (void RETURN_VOID) {void spkez_c};

extern void spkez_c (
        int targ,
        double et,
        char *CONST_STRING,
        char *CONST_STRING,
        int obs,
        double starg[6],
        double *OUTPUT );

/*******************************************
* Vector version
*******************************************/

%apply (double *IN_ARRAY1, int DIM1) {(double *et, int et_dim1)};
%apply (char *CONST_STRING) {char *ref};
%apply (char *CONST_STRING) {char *abcorr};
%apply (double **OUT_ARRAY2, int *SIZE1, int *SIZE2)
                {(double **starg, int *starg_dim1, int *starg_dim2)};
%apply (double **OUT_ARRAY1, int *SIZE1)
                {(double **lt, int *lt_dim1)};
%apply (void RETURN_VOID) {void spkez_vector};

%inline %{
    void spkez_vector(int targ,
                      double *et, int et_dim1,
                      char *ref,
                      char *abcorr,
                      int obs,
                      double **starg, int *starg_dim1, int *starg_dim2,
                      double **lt, int *lt_dim1) {

        double *starg_buffer = NULL;
        double *lt_buffer = NULL;
        int     i;

        starg_buffer = my_malloc(et_dim1 * 6);
        if (!starg_buffer) return;

        lt_buffer = my_malloc(et_dim1);
        if (!lt_buffer) return;

        for (i = 0; i < et_dim1; i++) {
            spkez_c(targ, et[i], ref, abcorr, obs,
                    starg_buffer + i*6, lt_buffer + i);
        }

        if (failed_c()) {
            free(starg_buffer);
            *starg = NULL;
            *starg_dim1 = 0;
            *starg_dim2 = 6;

            free(lt_buffer);
            *lt = NULL;
            *lt_dim1 = 0;
        }
        else {
            *starg = starg_buffer;
            *starg_dim1 = et_dim1;
            *starg_dim2 = 6;

            *lt = lt_buffer;
            *lt_dim1 = et_dim1;
        }
    }
%}

/***********************************************************************
* -Procedure spkezp_c ( S/P Kernel, easy position )
*
* -Abstract
*
* Return the position of a target body relative to an observing 
* body, optionally corrected for light time (planetary aberration) 
* and stellar aberration. 
*
* void spkezp_c (
*       SpiceInt            targ,
*       SpiceDouble         et,
*       ConstSpiceChar    * ref,
*       ConstSpiceChar    * abcorr,
*       SpiceInt            obs,
*       SpiceDouble         ptarg[3],
*       SpiceDouble       * lt        ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* targ       I   Target body NAIF ID code. 
* et         I   Observer epoch. 
* ref        I   Reference frame of output position vector. 
* abcorr     I   Aberration correction flag. 
* obs        I   Observing body NAIF ID code. 
* ptarg      O   Position of target. 
* lt         O   One way light time between observer and target. 
***********************************************************************/

%rename (spkezp) spkezp_c;

%apply (double OUT_ARRAY1[ANY]) {double ptarg[3]};
%apply (void RETURN_VOID) {void spkezp_c};

extern void spkezp_c (
        int targ,
        double et,
        char *CONST_STRING,
        char *CONST_STRING,
        int obs,
        double ptarg[3],
        double *OUTPUT );

/***********************************************************************
* -Procedure spkezr_c ( S/P Kernel, easier reader )
*
* -Abstract
*
* Return the state (position and velocity) of a target body 
* relative to an observing body, optionally corrected for light 
* time (planetary aberration) and stellar aberration. 
*
* void spkezr_c (
*       ConstSpiceChar     *targ,
*       SpiceDouble         et,
*       ConstSpiceChar     *ref,
*       ConstSpiceChar     *abcorr,
*       ConstSpiceChar     *obs,
*       SpiceDouble         starg[6],
*       SpiceDouble        *lt        )
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* targ       I   Target body name. 
* et         I   Observer epoch. 
* ref        I   Reference frame of output state vector. 
* abcorr     I   Aberration correction flag. 
* obs        I   Observing body name. 
* starg      O   State of target. 
* lt         O   One way light time between observer and target. 
***********************************************************************/

%rename (spkezr) spkezr_c;

%apply (double OUT_ARRAY1[ANY]) {double starg[6]};
%apply (void RETURN_VOID) {void spkezr_c};

extern void spkezr_c (
        char *CONST_STRING,
        double et,
        char *CONST_STRING,
        char *CONST_STRING,
        char *CONST_STRING,
        double starg[6],
        double *OUTPUT );

/***********************************************************************
* -Procedure spkgeo_c ( S/P Kernel, geometric state )
*
* -Abstract
*
* Compute the geometric state (position and velocity) of a target 
* body relative to an observing body.
*
* void spkgeo_c (
*       SpiceInt          targ, 
*       SpiceDouble       et, 
*       ConstSpiceChar  * ref, 
*       SpiceInt          obs, 
*       SpiceDouble       state[6], 
*       SpiceDouble     * lt       ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* targ       I   Target body. 
* et         I   Target epoch. 
* ref        I   Target reference frame. 
* obs        I   Observing body. 
* state      O   State of target. 
* lt         O   Light time. 
***********************************************************************/

%rename (spkgeo) spkgeo_c;

%apply (double OUT_ARRAY1[ANY]) {double state[6]};
%apply (void RETURN_VOID) {void spkgeo_c};

extern void spkgeo_c (
        int targ, 
        double et, 
        char *CONST_STRING, 
        int obs, 
        double state[6], 
        double *OUTPUT );

/***********************************************************************
* -Procedure spkgps_c ( S/P Kernel, geometric position )
*
* -Abstract
*
* Compute the geometric position of a target body relative to an 
* observing body. 
*
* void spkgps_c (
*       SpiceInt           targ,
*       SpiceDouble        et,
*       ConstSpiceChar   * ref,
*       SpiceInt           obs,
*       SpiceDouble        pos[3],
*       SpiceDouble      * lt     ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* targ       I   Target body. 
* et         I   Target epoch. 
* ref        I   Target reference frame. 
* obs        I   Observing body. 
* pos        O   Position of target. 
* lt         O   Light time. 
***********************************************************************/

%rename (spkgps) spkgps_c;

%apply (double OUT_ARRAY1[ANY]) {double pos[3]};
%apply (void RETURN_VOID) {void spkgps_c};

extern void spkgps_c (
        int targ,
        double et,
        char *CONST_STRING,
        int obs,
        double pos[3],
        double *OUTPUT );

/***********************************************************************
* -Procedure spkobj_c ( SPK objects )
*
* -Abstract
*
* Find the set of ID codes of all objects in a specified SPK file. 
*
* void spkobj_c (
*       ConstSpiceChar  * spk,
*       SpiceCell       * ids ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* spk        I   Name of SPK file. 
* ids       I/O  Set of ID codes of objects in SPK file. 
***********************************************************************/

%rename (spkobj) my_spkobj_c;

%apply (char *CONST_STRING) {char *spk};
%apply (int OUT_ARRAY1[ANY], int *SIZE1) {(int  body_ids[200], int *bodies)};
%apply (void RETURN_VOID) {void my_spkobj_c};

/* Helper function to create a 1-D array of results */
%inline %{
    void my_spkobj_c(char *spk, int body_ids[200], int *bodies) {
        int j;
        SPICEINT_CELL(ids, 200);

        scard_c(0, &ids);
        spkobj_c(spk, &ids);

        *bodies = card_c(&ids);
        for (j = 0; j < *bodies; j++) {
            body_ids[j] = SPICE_CELL_ELEM_I(&ids, j);
        }
    }
%}

/***********************************************************************
* -Procedure spkpos_c ( S/P Kernel, position )
*
* -Abstract
*
* Return the position of a target body relative to an observing 
* body, optionally corrected for light time (planetary aberration) 
* and stellar aberration. 
*
* void spkpos_c (
*       ConstSpiceChar   * targ,
*       SpiceDouble        et,
*       ConstSpiceChar   * ref,
*       ConstSpiceChar   * abcorr,
*       ConstSpiceChar   * obs,
*       SpiceDouble        ptarg[3],
*       SpiceDouble      * lt        ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* targ       I   Target body name. 
* et         I   Observer epoch. 
* ref        I   Reference frame of output position vector. 
* abcorr     I   Aberration correction flag. 
* obs        I   Observing body name. 
* ptarg      O   Position of target. 
* lt         O   One way light time between observer and target. 
***********************************************************************/

%rename (spkpos) spkpos_c;

%apply (double OUT_ARRAY1[ANY]) {double ptarg[3]};
%apply (void RETURN_VOID) {void spkpos_c};

extern void spkpos_c (
        char *CONST_STRING,
        double et,
        char *CONST_STRING,
        char *CONST_STRING,
        char *CONST_STRING,
        double ptarg[3],
        double *OUTPUT );

/***********************************************************************
* -Procedure spkssb_c ( S/P Kernel, solar system barycenter )
*
* -Abstract
*
* Return the state (position and velocity) of a target body 
* relative to the solar system barycenter. 
*
* void spkssb_c (
*       SpiceInt           targ,
*       SpiceDouble        et,
*       ConstSpiceChar   * ref,
*       SpiceDouble        starg[6] ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* targ       I   Target body. 
* et         I   Target epoch. 
* ref        I   Target reference frame. 
* starg      O   State of target. 
***********************************************************************/

%rename (spkssb) spkssb_c;

%apply (double OUT_ARRAY1[ANY]) {double starg[6]};
%apply (void RETURN_VOID) {void spkssb_c};

extern void spkssb_c (
        int targ,
        double et,
        char *CONST_STRING,
        double starg[6] );

/***********************************************************************
* -Procedure srfrec_c ( Surface to rectangular coordinates )
*
* -Abstract
*
* Convert planetocentric latitude and longitude of a surface 
* point on a specified body to rectangular coordinates. 
*
* void srfrec_c (
*       SpiceInt      body,
*       SpiceDouble   longitude,
*       SpiceDouble   latitude,
*       SpiceDouble   rectan[3] ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* body       I   NAIF integer code of an extended body. 
* longitude  I   Longitude of point in radians.
* latitude   I   Latitude of point in radians.
* rectan     O   Rectangular coordinates of the point. 
***********************************************************************/

%rename (srfrec) srfrec_c;

%apply (double OUT_ARRAY1[ANY]) {double rectan[3]};
%apply (void RETURN_VOID) {void srfrec_c};

extern void srfrec_c (
        int body,
        double longitude,
        double latitude,
        double rectan[3] );

/***********************************************************************
* -Procedure srfxpt_c ( Surface intercept point )
*
* -Abstract
*
* Given an observer and a direction vector defining a ray, compute the
* surface intercept point of the ray on a target body at a specified
* epoch, optionally corrected for light time and stellar aberration.
*
* void srfxpt_c (
*       ConstSpiceChar      * method,
*       ConstSpiceChar      * target,
*       SpiceDouble           et,
*       ConstSpiceChar      * abcorr,
*       ConstSpiceChar      * obsrvr,
*       ConstSpiceChar      * dref,
*       ConstSpiceDouble      dvec   [3],
*       SpiceDouble           spoint [3],
*       SpiceDouble         * dist,
*       SpiceDouble         * trgepc,
*       SpiceDouble           obspos [3],
*       SpiceBoolean        * found      )
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* method     I   Computation method. 
* target     I   Name of target body. 
* et         I   Epoch in ephemeris seconds past J2000 TDB. 
* abcorr     I   Aberration correction. 
* obsrvr     I   Name of observing body. 
* dref       I   Reference frame of input direction vector. 
* dvec       I   Ray's direction vector. 
* spoint     O   Surface intercept point on the target body. 
* dist       O   Distance from the observer to the intercept point. 
* trgepc     O   Intercept epoch. 
* obspos     O   Observer position relative to target center. 
* found      O   Flag indicating whether intercept was found. 
***********************************************************************/

%rename (srfxpt) srfxpt_c;

%apply (double  IN_ARRAY1[ANY]) {double dvec  [3]};
%apply (double OUT_ARRAY1[ANY]) {double spoint[3]};
%apply (double OUT_ARRAY1[ANY]) {double obspos[3]};
%apply (void RETURN_VOID) {void srfxpt_c};

extern void srfxpt_c (
        char *CONST_STRING,
        char *CONST_STRING,
        double et,
        char *CONST_STRING,
        char *CONST_STRING,
        char *CONST_STRING,
        double dvec[3],
        double spoint[3],
        double *OUTPUT,
        double *OUTPUT,
        double obspos[3],
        int *OUT_BOOLEAN );

/***********************************************************************
* $Procedure   STCF01 (STAR catalog type 1, find stars in RA-DEC box)
*
* -Abstract
*
* Search through a type 1 star catalog and return the number of
* stars within a specified RA - DEC rectangle.
*
* Original F2C arguments:
*   int stcf01_(char *catnam, doublereal *westra, doublereal *
*				eastra, doublereal *sthdec, doublereal *nthdec, integer *nstars, 
*				ftnlen catnam_len)
*
* New arguments with wrapper:
*   int my_stcf01_c(char *catnam, double westra, double eastra,
*					double sthdec, double nthdec,
*					int *nstars) 
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* CATNAM      I   Catalog table name.
* WESTRA      I   Western most right ascension in radians.
* EASTRA      I   Eastern most right ascension in radians.
* STHDEC      I   Southern most declination in radians.
* NTHDEC      I   Northern most declination in radians.
* NSTARS      O   Number of stars found.
***********************************************************************/

%rename (stcf01) my_stcf01_c;

%apply (char *CONST_STRING) {char *catnam};
%apply (int *OUTPUT) {int *nstars};
%apply (void RETURN_VOID) {void my_stcf01_c};

/* Helper function to reorder arguments */
%inline %{
    void my_stcf01_c(char *catnam, double westra, double eastra,
 					 double sthdec, double nthdec,
 					 int *nstars) {
		stcf01_(catnam, &westra, &eastra, &sthdec, &nthdec, nstars,
				strlen(catnam));
    }
%}

/***********************************************************************
* $Procedure   STCG01 ( STAR catalog type 1, get star data )
*
* -Abstract
*
* Get data for a single star from a SPICE type 1 star catalog.
*
* Original F2C arguments:
*   int stcg01_(integer *index, doublereal *ra, doublereal *dec, 
*				doublereal *rasig, doublereal *decsig, integer *catnum,
*				char *sptype, doublereal *vmag, ftnlen sptype_len)
*
* New arguments with wrapper:
*   int my_stcg01_c(int index, double *ra, double *dec, 
*					double *rasig, double *decsig, int *catnum,
*					char *sptype, doublel *vmag)
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* INDEX       I   Star index.
* RA          O   Right ascension in radians.
* DEC         O   Declination in radians.
* RAS         O   Right ascension uncertainty in radians.
* DECS        O   Declination uncertainty in radians.
* CATNUM      O   Catalog number.
* SPTYPE      O   Spectral type.
* VMAG        O   Visual magnitude.
***********************************************************************/

%rename (stcg01) my_stcg01_c;

%apply (double *OUTPUT) {double *ra};
%apply (double *OUTPUT) {double *dec};
%apply (double *OUTPUT) {double *rasig};
%apply (double *OUTPUT) {double *decsig};
%apply (int *OUTPUT) {int *catnum};
%apply (char OUT_STRING[ANY]) {char sptype[20]};
%apply (double *OUTPUT) {double *vmag};
%apply (void RETURN_VOID) {void my_stcg01_c};

/* Helper function to reorder arguments */
%inline %{
   void my_stcg01_c(int index, double *ra, double *dec, 
					double *rasig, double *decsig, int *catnum,
					char sptype[20], double *vmag) {
		char *s;
		index += 1;
		stcg01_(&index, ra, dec, rasig, decsig, catnum, sptype,
				vmag, 20);
		s = sptype+19;
		while (s >= sptype && *s == ' ') s--; /* Convert FORTRAN->C string */
		s[1] = '\0';
    }
%}

/***********************************************************************
* $Procedure   STCL01 ( STAR catalog type 1, load catalog file )
*
* -Abstract
*
* Load SPICE type 1 star catalog and return the catalog's
* table name.
*
* Original F2C arguments:
*   int stcl01_(char *catfnm, char *tabnam, integer *handle, 
*	  		    ftnlen catfnm_len, ftnlen tabnam_len)
*
* New arguments with wrapper:
*   int my_stcl01_c(char *catfnm, char *tabnam, integer *handle)
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* CATFNM      I   Catalog file name.
* TABNAM      O   Catalog table name.
* HANDLE      O   Catalog file handle.
***********************************************************************/

%rename (stcl01) my_stcl01_c;

%apply (char OUT_STRING[ANY]) {char tabnam[256]};
%apply (int *OUTPUT) {int *handle};
%apply (void RETURN_VOID) {void my_stcl01_c};

/* Helper function to convert strings and reorder arguments */
%inline %{
    void my_stcl01_c(char *catfnm, char tabnam[256], int *handle) {
        char *s;
		stcl01_(catfnm, tabnam, handle, strlen(catfnm), 256);
		s = tabnam+255;
		while (s >= tabnam && *s == ' ') s--; /* Convert FORTRAN->C string */
		s[1] = '\0';
    }
%}

/***********************************************************************
* -Procedure stelab_c     ( Stellar Aberration )
*
* -Abstract
*
* Correct the apparent position of an object for stellar 
* aberration. 
*
* void stelab_c (
*       ConstSpiceDouble   pobj[3],
*       ConstSpiceDouble   vobs[3],
*       SpiceDouble        appobj[3] ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* pobj       I   Position of an object with respect to the 
* observer. 
* vobs       I   Velocity of the observer with respect to the 
* Solar System barycenter. 
* appobj     O   Apparent position of the object with respect to 
* the observer, corrected for stellar aberration. 
***********************************************************************/

%rename (stelab) stelab_c;

%apply (double  IN_ARRAY1[ANY]) {double pobj  [3]};
%apply (double  IN_ARRAY1[ANY]) {double vobs  [3]};
%apply (double OUT_ARRAY1[ANY]) {double appobj[3]};
%apply (void RETURN_VOID) {void stelab_c};

extern void stelab_c (
        double pobj  [3],
        double vobs  [3],
        double appobj[3] );

/***********************************************************************
* -Procedure stlabx_     ( Stellar aberration, transmission case )
*
* -Abstract
*
* Correct the position of a target for the stellar aberration 
* effect on radiation transmitted from a specified observer to 
* the target.  
*
* void stlabx_ (
*       ConstSpiceDouble   pobj[3],
*       ConstSpiceDouble   vobs[3],
*       SpiceDouble        corpos[3] ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* pobj       I   Position of an object with respect to the 
* observer. 
* vobs       I   Velocity of the observer with respect to the 
* Solar System barycenter. 
* corpos     O   Corrected position of the object. 
***********************************************************************/

%rename (stlabx) stlabx_;

%apply (double  IN_ARRAY1[ANY]) {double pobj  [3]};
%apply (double  IN_ARRAY1[ANY]) {double vobs  [3]};
%apply (double OUT_ARRAY1[ANY]) {double corpos[3]};
%apply (void RETURN_VOID) {void stlabx_c};

extern void stlabx_ (
        double pobj  [3],
        double vobs  [3],
        double corpos[3] );

/***********************************************************************
* -Procedure stpool_c ( String from pool )
*
* -Abstract
*
* Retrieve the nth string from the kernel pool variable, where the
* string may be continued across several components of the kernel pool
* variable.
*
* void stpool_c (
*       ConstSpiceChar    * item,
*       SpiceInt            nth,
*       ConstSpiceChar    * contin,
*       SpiceInt            lenout,
*       SpiceChar         * string,
*       SpiceInt          * size,
*       SpiceBoolean      * found  ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* item       I   Name of the kernel pool variable.
* nth        I   Index of the full string to retrieve.
* contin     I   Character sequence used to indicate continuation.
* lenout     I   Available space in output string.
* string     O   A full string concatenated across continuations. 
* size       O   The number of characters in the full string value. 
* found      O   Flag indicating success or failure of request. 
***********************************************************************/

%rename (stpool) stpool_c;

%apply (int DIM1, char OUT_STRING[ANY]) {(int lenout,
                                            char string[1024])};
%apply (void RETURN_VOID) {void stpool_c};

extern void stpool_c (
        char *CONST_STRING,
        int nth,
        char *CONST_STRING,
        int lenout, char string[1024],
        int *OUTPUT,
        int *OUT_BOOLEAN_KEYERROR );

/***********************************************************************
* -Procedure str2et_c ( String to ET )
*
* -Abstract
*
* Convert a string representing an epoch to a double precision
* value representing the number of TDB seconds past the J2000
* epoch corresponding to the input epoch.
*
* void str2et_c (
*       ConstSpiceChar * str,
*       SpiceDouble    * et   )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* str        I   A string representing an epoch.
* et         O   The equivalent value in seconds past J2000, TDB.
***********************************************************************/

%rename (str2et) str2et_c;

%apply (void RETURN_VOID) {void str2et_c};

extern void str2et_c (
        char *CONST_STRING,
        double *OUTPUT );

/***********************************************************************
* -Procedure subpt_c ( Sub-observer point )
*
* -Abstract
*
* Compute the rectangular coordinates of the sub-observer point on
* a target body at a particular epoch, optionally corrected for
* planetary (light time) and stellar aberration.  Return these
* coordinates expressed in the body-fixed frame associated with the
* target body.  Also, return the observer's altitude above the
* target body.
*
* void subpt_c (
*       ConstSpiceChar       * method,
*       ConstSpiceChar       * target,
*       SpiceDouble            et,
*       ConstSpiceChar       * abcorr,
*       ConstSpiceChar       * obsrvr,
*       SpiceDouble            spoint [3],
*       SpiceDouble          * alt         )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* method     I   Computation method.
* target     I   Name of target body.
* et         I   Epoch in ephemeris seconds past J2000 TDB.
* abcorr     I   Aberration correction.
* obsrvr     I   Name of observing body.
* spoint     O   Sub-observer point on the target body.
* alt        O   Altitude of the observer above the target body.
***********************************************************************/

%rename (subpt) subpt_c;

%apply (double OUT_ARRAY1[ANY]) {double spoint[3]};
%apply (void RETURN_VOID) {void subpt_c};

extern void subpt_c (
        char *CONST_STRING,
        char *CONST_STRING,
        double et,
        char *CONST_STRING,
        char *CONST_STRING,
        double spoint[3],
        double *OUTPUT );

/***********************************************************************
* -Procedure subsol_c ( Sub-solar point )
*
* -Abstract
*
* Determine the coordinates of the sub-solar point on a target 
* body as seen by a specified observer at a specified epoch,  
* optionally corrected for planetary (light time) and stellar 
* aberration.   
*
* void subsol_c (
*       ConstSpiceChar   * method,
*       ConstSpiceChar   * target,
*       SpiceDouble        et,
*       ConstSpiceChar   * abcorr,
*       ConstSpiceChar   * obsrvr,
*       SpiceDouble        spoint[3] ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* method     I   Computation method. 
* target     I   Name of target body. 
* et         I   Epoch in ephemeris seconds past J2000 TDB. 
* abcorr     I   Aberration correction. 
* obsrvr     I   Name of observing body. 
* spoint     O   Sub-solar point on the target body. 
***********************************************************************/

%rename (subsol) subsol_c;

%apply (double OUT_ARRAY1[ANY]) {double spoint[3]};
%apply (void RETURN_VOID) {void subsol_c};

extern void subsol_c (
        char *CONST_STRING,
        char *CONST_STRING,
        double et,
        char *CONST_STRING,
        char *CONST_STRING,
        double spoint[3] );

/***********************************************************************
* -Procedure      surfnm_c ( Surface normal vector on an ellipsoid )
*
* -Abstract
*
* This routine computes the outward-pointing, unit normal vector 
* from a point on the surface of an ellipsoid. 
*
* void surfnm_c (
*       SpiceDouble        a, 
*       SpiceDouble        b, 
*       SpiceDouble        c, 
*       ConstSpiceDouble   point[3], 
*       SpiceDouble        normal[3] ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* a          I   Length of the ellisoid semi-axis along the x-axis. 
* b          I   Length of the ellisoid semi-axis along the y-axis. 
* c          I   Length of the ellisoid semi-axis along the z-axis. 
* point      I   Body-fixed coordinates of a point on the ellipsoid 
* normal     O   Outward pointing unit normal to ellipsoid at point 
***********************************************************************/

%rename (surfnm) surfnm_c;

%apply (double  IN_ARRAY1[ANY]) {double point [3]}; 
%apply (double OUT_ARRAY1[ANY]) {double normal[3]};
%apply (void RETURN_VOID) {void surfnm_c};

extern void surfnm_c (
        double a, 
        double b, 
        double c, 
        double point[ 3], 
        double normal[3] );

/***********************************************************************
* -Procedure surfpt_c ( Surface point on an ellipsoid )
*
* -Abstract
*
* Determine the intersection of a line-of-sight vector with the 
* surface of an ellipsoid. 
*
* void surfpt_c (
*       ConstSpiceDouble   positn[3], 
*       ConstSpiceDouble   u[3], 
*       SpiceDouble        a, 
*       SpiceDouble        b,
*       SpiceDouble        c, 
*       SpiceDouble        point[3],  
*       SpiceBoolean     * found     ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* positn     I   Position of the observer in body-fixed frame. 
* u          I   Vector from the observer in some direction.
* a          I   Length of the ellipsoid semi-axis along the x-axis.
* b          I   Length of the ellipsoid semi-axis along the y-axis.
* c          I   Length of the ellipsoid semi-axis along the z-axis.
* point      O   Point on the ellipsoid pointed to by u.
* found      O   Flag indicating if u points at the ellipsoid.
***********************************************************************/

%rename (surfpt) surfpt_c;

%apply (double   IN_ARRAY1[ANY]) {double positn[3]}; 
%apply (double   IN_ARRAY1[ANY]) {double u[     3]}; 
%apply (double  OUT_ARRAY1[ANY]) {double point [3]}; 
%apply (void RETURN_VOID) {void surfpt_c};

extern void surfpt_c (
        double positn[3], 
        double u[3], 
        double a, 
        double b,
        double c, 
        double point[3],  
        int *OUT_BOOLEAN );

/***********************************************************************
* -Procedure      sxform_c ( State Transformation Matrix )
*
* -Abstract
*
* Return the state transformation matrix from one frame to 
* another at a specified epoch. 
*
* void sxform_c (
*       ConstSpiceChar  * from, 
*       ConstSpiceChar  * to, 
*       SpiceDouble       et, 
*       SpiceDouble       xform[6][6] ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* from       I   Name of the frame to transform from.
* to         I   Name of the frame to transform to.
* et         I   Epoch of the state transformation matrix.
* xform      O   A state transformation matrix.
***********************************************************************/

%rename (sxform) sxform_c;

%apply (double OUT_ARRAY2[ANY][ANY]) {double xform[6][6]};
%apply (void RETURN_VOID) {void sxform_c};

extern void sxform_c (
        char *CONST_STRING, 
        char *CONST_STRING, 
        double et, 
        double xform[6][6] );

/*******************************************
* Vector version
*******************************************/

%apply (char *CONST_STRING) {char *_from};
%apply (char *CONST_STRING) {char *to};
%apply (double *IN_ARRAY1, int DIM1) {(double *et, int et_dim1)};
%apply (double **OUT_ARRAY2, int *SIZE1, int *SIZE2)
                {(double **xform, int *xform_dim1, int *xform_dim2)};
%apply (void RETURN_VOID) {void sxform_vector};

%inline %{
    void sxform_vector(char *_from,
                       char *to,
                       double *et, int et_dim1,
                       double **xform, int *xform_dim1, int *xform_dim2) {

        /* Allocate the space for the return arrays */
        double *xform_buffer = NULL;
        int     i;

        xform_buffer = my_malloc(et_dim1 * 36);
        if (!xform_buffer) return;

        for (i = 0; i < et_dim1; i++) {
            sxform_c(_from, to, et[i], xform_buffer + i*36);
        }

        if (failed_c()) {
            free(xform_buffer);
            *xform = NULL;
            *xform_dim1 = 0;
            *xform_dim2 = 36;
        }
        else {
            *xform = xform_buffer;
            *xform_dim1 = et_dim1;
            *xform_dim2 = 36;
        }
    }
%}

/***********************************************************************
* -Procedure timdef_c ( Time Software Defaults )
*
* -Abstract
*
* Set and retrieve the defaults associated with calendar
* input strings.
*
* void timdef_c (
*       ConstSpiceChar * action,
*       ConstSpiceChar * item,
*       SpiceInt         lenout,
*       SpiceChar      * value )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* action     I   is the kind of action to take "SET" or "GET".
* item       I   is the default item of interest.
* lenout     I   Length of list for output.
* value     I/O  is the value associated with the default item.
***********************************************************************/

%rename (timdef) timdef_c;

%apply (int DIM1, char INOUT_STRING[ANY]) {(int lenout,
                                            char action[256])};
%apply (void RETURN_VOID) {void timdef_c};

extern void timdef_c(
        char *CONST_STRING,
        char *CONST_STRING,
        int lenout, char action[256]);

/***********************************************************************
* -Procedure timout_c ( Time Output )
*
* -Abstract
*
* This routine converts an input epoch represented in TDB seconds
* past the TDB epoch of J2000 to a character string formatted to
* the specifications of a user's format picture.
*
* void timout_c (
*       SpiceDouble       et,
*       ConstSpiceChar  * pictur,
*       SpiceInt          lenout,
*       SpiceChar       * output )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* et         I   An epoch in seconds past the ephemeris epoch J2000.
* pictur     I   A format specification for the output string.
* lenout     I   The length of the output string plus 1.
* output     O   A string representation of the input epoch.
***********************************************************************/

%rename (timout) timout_c;

%apply (int DIM1, char OUT_STRING[ANY]) {(int lenout,
                                          char output[256])};
%apply (void RETURN_VOID) {void timout_c};

extern void timout_c (
        double et,
        char *CONST_STRING,
        int lenout, char output[256]);

/***********************************************************************
* -Procedure tipbod_c ( Transformation, inertial position to bodyfixed )
*
* -Abstract
*
* Return a 3x3 matrix that transforms positions in inertial 
* coordinates to positions in body-equator-and-prime-meridian 
* coordinates. 
*
* void tipbod_c (
*       ConstSpiceChar  * ref,
*       SpiceInt          body,
*       SpiceDouble       et,
*       SpiceDouble       tipm[3][3] ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* ref        I   ID of inertial reference frame to transform from. 
* body       I   ID code of body. 
* et         I   Epoch of transformation. 
* tipm       O   Transformation (position), inertial to prime 
* meridian. 
***********************************************************************/

%rename (tipbod) tipbod_c;

%apply (double OUT_ARRAY2[ANY][ANY]) {double tipm[3][3]};
%apply (void RETURN_VOID) {void tipbod_c};

extern void tipbod_c (
        char *CONST_STRING,
        int body,
        double et,
        double tipm[3][3] );

/***********************************************************************
* -Procedure  tisbod_c ( Transformation, inertial state to bodyfixed )
*
* -Abstract
*
* Return a 6x6 matrix that transforms states in inertial coordinates to 
* states in body-equator-and-prime-meridian coordinates.
*
* void tisbod_c (
*       ConstSpiceChar   * ref,    
*       SpiceInt           body,
*       SpiceDouble        et,     
*       SpiceDouble        tsipm[6][6] )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* ref        I   ID of inertial reference frame to transform from
* body       I   ID code of body
* et         I   Epoch of transformation
* tsipm      O   Transformation (state), inertial to prime meridian
***********************************************************************/

%rename (tisbod) tisbod_c;

%apply (double OUT_ARRAY2[ANY][ANY]) {double tsipm[6][6]};
%apply (void RETURN_VOID) {void tisbod_c};

extern void tisbod_c (
        char *CONST_STRING, 
        int body,
        double et, 
        double tsipm[6][6] );

/***********************************************************************
* -Procedure tkvrsn_c ( Toolkit version strings )
*
* -Abstract
*
* Given an item such as the Toolkit or an entry point name, return 
* the latest version string. 
*
* ConstSpiceChar  * tkvrsn_c (
*       ConstSpiceChar * item ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* item       I   Item for which a version string is desired. 
*
* The function returns a pointer to a version string. 
***********************************************************************/

%rename (tkvrsn) tkvrsn_c;

%apply (char *RETURN_STRING) {char *tkvrsn_c};

extern char *tkvrsn_c(char *CONST_STRING);

/***********************************************************************
* -Procedure tparse_c ( Parse a UTC time string )
*
* -Abstract
*
* Parse a time string and return seconds past the J2000 epoch 
* on a formal calendar. 
*
* void tparse_c (
*       ConstSpiceChar  * string,
*       SpiceInt          lenout,
*       SpiceDouble     * sp2000,
*       SpiceChar       * errmsg  ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* string     I   Input time string, UTC. 
* lenout     I   Available space in output error message string.
* sp2000     O   Equivalent UTC seconds past J2000.
* errmsg     O   Descriptive error message. 
***********************************************************************/

%rename (tparse) my_tparse_c;

%apply (char *CONST_STRING) {char *string};
%apply (double *OUTPUT) {double *sp2000};
%apply (int DIM1, char OUT_STRING_SYNTAXERROR[ANY])
        {(int lenout, char errmsg[1024])};
%apply (void RETURN_VOID) {void my_tparse_c};

/* Helper function to deal with order of arguments */
%inline %{
    void my_tparse_c(char *string, double *sp2000,
                     int lenout, char errmsg[1024]) {
        tparse_c(string, lenout, sp2000, errmsg);
    }
%}

/***********************************************************************
* -Procedure tpictr_c ( Create a Time Format Picture )
*
* -Abstract
*
* Given a sample time string, create a time format picture
* suitable for use by the routine timout_c.
*
* void tpictr_c (
*       ConstSpiceChar * sample,
*       SpiceInt         lenout,
*       SpiceInt         lenerr,
*       SpiceChar      * pictur,
*       SpiceBoolean   * ok,
*       SpiceChar      * errmsg )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* sample     I   A sample time string.
* lenout     I   The length for the output picture string.
* lenerr     I   The length for the output error string.
* pictur     O   A format picture that describes sample.
* ok         O   Flag indicating whether sample parsed successfully.
* errmsg     O   Diagnostic returned if sample cannot be parsed.
***********************************************************************/

%rename (tpictr) my_tpictr_c;

%apply (char *CONST_STRING) {char *sample};
%apply (int DIM1, char OUT_STRING[ANY])
                {(int lenout, char pictur[256])};
%apply (int *OK, int DIM1, char OUT_STRING_SYNTAXERROR[ANY])
                {(int *ok, int lenerr, char errmsg[1024])};
%apply (void RETURN_VOID) {void my_tpictr_c};

/* Helper function to deal with order of arguments */
%inline %{
    void my_tpictr_c(char *sample,
                     int lenout, char pictur[256],
                     int *ok, int lenerr, char errmsg[1024]) {

        tpictr_c(sample, lenout, lenerr, pictur, ok, errmsg);
    }
%}

/***********************************************************************
* -Procedure trace_c ( Trace of a 3x3 matrix )
*
* -Abstract
*
* Return the trace of a 3x3 matrix. 
*
* SpiceDouble trace_c (
*       ConstSpiceDouble  matrix[3][3] ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* matrix     I     3x3 matrix of double precision numbers. 
* trace      O     The trace of matrix. 
***********************************************************************/

%rename (trace) trace_c;

%apply (double IN_ARRAY2[ANY][ANY]) {double matrix[3][3]};
%apply (double RETURN_DOUBLE) {double trace_c};

extern double trace_c (
        double matrix[3][3] );

/***********************************************************************
* -Procedure  trcoff_c  ( Turn tracing off )
*
* -Abstract
*
* Disable tracing. 
*
* void trcoff_c (
        void ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* None. 
***********************************************************************/

%rename (trcoff) trcoff_c;

%apply (void RETURN_VOID) {void trcoff_c};

extern void trcoff_c ( void );

/***********************************************************************
* -Procedure tsetyr_c ( Time --- set year expansion boundaries )
*
* -Abstract
*
* Set the lower bound on the 100 year range
*
* void tsetyr_c (
*       SpiceInt year )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* year       I   Lower bound on the 100 year interval of expansion
***********************************************************************/

%rename (tsetyr) tsetyr_c;
%apply (void RETURN_VOID) {void tsetyr_c};

extern void tsetyr_c (
        int year );

/***********************************************************************
* -Procedure twopi_c ( Twice the value of pi )
*
* -Abstract
*
* Return twice the value of pi (the ratio of the circumference of 
* a circle to its diameter). 
*
* SpiceDouble twopi_c (
        void ) 
*
* -Brief_I/O
*
* The function returns twice the value of pi. 
***********************************************************************/

%rename (twopi) twopi_c;

%apply (double RETURN_DOUBLE) {double twopi_c};

extern double twopi_c ( void );

/***********************************************************************
* -Procedure twovec_c ( Two vectors defining an orthonormal frame )
*
* -Abstract
*
* Find the transformation to the right-handed frame having a 
* given vector as a specified axis and having a second given 
* vector lying in a specified coordinate plane. 
*
* void twovec_c (
*       ConstSpiceDouble    axdef  [3],
*       SpiceInt            indexa,
*       ConstSpiceDouble    plndef [3],
*       SpiceInt            indexp,
*       SpiceDouble         mout   [3][3] ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  ------------------------------------------------- 
* axdef      I   Vector defining a principal axis. 
* indexa     I   Principal axis number of axdef (X=1, Y=2, Z=3). 
* plndef     I   Vector defining (with axdef) a principal plane. 
* indexp     I   Second axis number (with indexa) of principal 
* plane. 
* mout       O   Output rotation matrix. 
***********************************************************************/

%rename (twovec) twovec_c;

%apply (double  IN_ARRAY1[ANY]     ) {double axdef  [3]};
%apply (double  IN_ARRAY1[ANY]     ) {double plndef [3]};
%apply (double OUT_ARRAY2[ANY][ANY]) {double mout[3][3]};
%apply (void RETURN_VOID) {void twovec_c};

extern void twovec_c (
        double axdef[3],
        int indexa,
        double plndef[3],
        int indexp,
        double mout[3][3] );

/***********************************************************************
* -Procedure tyear_c ( Seconds per tropical year )
*
* -Abstract
*
* Return the number of seconds in a tropical year. 
*
* SpiceDouble tyear_c (
        void ) 
*
* -Brief_I/O
*
* VARIABLE  I/O              DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* tyear_c       O   The number of seconds/tropical year 
***********************************************************************/

%rename (tyear) tyear_c;

extern double tyear_c ( void );

/***********************************************************************
* -Procedure ucrss_c ( Unitized cross product, 3x3 )
*
* -Abstract
*
* Compute the normalized cross product of two 3-vectors. 
*
* void ucrss_c (
*       ConstSpiceDouble   v1[3],
*       ConstSpiceDouble   v2[3], 
*       SpiceDouble        vout[3] ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* v1         I     Left vector for cross product. 
* v2         I     Right vector for cross product. 
* vout       O     Normalized cross product (v1xv2) / |v1xv2|. 
***********************************************************************/

%rename (ucrss) ucrss_c;

%apply (double  IN_ARRAY1[ANY]) {double v1  [3]};
%apply (double  IN_ARRAY1[ANY]) {double v2  [3]}; 
%apply (double OUT_ARRAY1[ANY]) {double vout[3]};
%apply (void RETURN_VOID) {void ucrss_c};

extern void ucrss_c (
        double v1  [3],
        double v2  [3], 
        double vout[3] );

/***********************************************************************
* -Procedure unitim_c ( Uniform time scale transformation )
*
* -Abstract
*
* Transform time from one uniform scale to another.  The uniform
* time scales are TAI, TDT, TDB, ET, JED, JDTDB, JDTDT.
*
* SpiceDouble unitim_c (
*       SpiceDouble        epoch,
*       ConstSpiceChar   * insys,
*       ConstSpiceChar   * outsys )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* epoch      I   An epoch to be converted.
* insys      I   The time scale associated with the input epoch.
* outsys     I   The time scale associated with the function value.
*
* The function returns the d.p. in outsys that is equivalent to the
* epoch on the insys time scale.
***********************************************************************/

%rename (unitim) unitim_c;

%apply (double RETURN_DOUBLE) {double unitim_c};

extern double unitim_c (
        double epoch,
        char *CONST_STRING,
        char *CONST_STRING );

/***********************************************************************
* -Procedure unload_c ( Unload a kernel )
*
* -Abstract
*
* Unload a SPICE kernel. 
*
* void unload_c (
*       ConstSpiceChar  * file ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* file       I   The name of a kernel to unload. 
***********************************************************************/

%rename (unload) unload_c;

%apply (void RETURN_VOID) {void unload_c};

extern void unload_c (
        char *CONST_STRING );

/***********************************************************************
* -Procedure unorm_c ( Unit vector and norm, 3 dimensional )
*
* -Abstract
*
* Normalize a double precision 3-vector and return its magnitude. 
*
* void unorm_c (
*       ConstSpiceDouble     v1[3],
*       SpiceDouble          vout[3],
*       SpiceDouble        * vmag    ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* v1         I     Vector to be normalized. 
* vout       O     Unit vector v1 / |v1|. 
*                  If v1 is the zero vector, then vout will also 
*                  be zero. vout can overwrite v1. 
* vmag       O     Magnitude of v1, i.e. |v1|. 
***********************************************************************/

%rename (unorm) unorm_c;

%apply (double  IN_ARRAY1[ANY]) {double v1  [3]};
%apply (double OUT_ARRAY1[ANY]) {double vout[3]};
%apply (void RETURN_VOID) {void unorm_c};

extern void unorm_c (
        double v1  [3],
        double vout[3],
        double *OUTPUT );

/***********************************************************************
* -Procedure unormg_c ( Unit vector and norm, general dimension )
*
* -Abstract
*
* Normalize a double precision vector of arbitrary dimension and
* return its magnitude.
*
* void unormg_c (
*       ConstSpiceDouble  * v1,
*       SpiceInt            ndim,
*       SpiceDouble       * vout,
*       SpiceDouble       * vmag )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* v1        I     Vector to be normalized.
* ndim      I     Dimension of v1 (and also vout).
* vout      O     Unit vector v1 / |v1|.
*                 If v1 = 0, vout will also be zero.
*                 vout can overwrite v1.
* vmag      O     Magnitude of v1, that is, |v1|.
***********************************************************************/

%rename (unormg) my_unormg_c;

%apply (double   *IN_ARRAY1, int    DIM1) {(double  *v1, int  nd1)};
%apply (double **OUT_ARRAY1, int *SIZE1) {(double **v2, int *nd2)};
%apply (double   *OUTPUT) {double *vmag};
%apply (void RETURN_VOID) {void my_unormg_c};

%inline %{
    void my_unormg_c(double  *v1, int  nd1,
                     double **v2, int *nd2,
                     double  *vmag) {

        double *result = NULL;

        *v2 = NULL;
        *nd2 = 0;

        result = my_malloc(nd1);
        if (!result) return;

        unormg_c(v1, nd1, result, vmag);
        *v2 = result;
        *nd2 = nd1;
    }
%}

/***********************************************************************
* -Procedure utc2et_c ( UTC to Ephemeris Time )
*
* -Abstract
*
* Convert an input time from Calendar or Julian Date format, UTC,
* to ephemeris seconds past J2000.
*
* void utc2et_c (
*       ConstSpiceChar  * utcstr,
*       SpiceDouble     * et      )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* utcstr     I   Input time string, UTC.
* et         O   Output epoch, ephemeris seconds past J2000.
***********************************************************************/

%rename (utc2et) utc2et_c;

%apply (void RETURN_VOID) {void utc2et_c};

extern void utc2et_c (
        const char *CONST_STRING,
        double *OUTPUT );

/***********************************************************************
* -Procedure vadd_c ( Vector addition, 3 dimensional )
*
* -Abstract
*
* add two 3 dimensional vectors. 
*
* void vadd_c (
*       ConstSpiceDouble   v1[3],
*       ConstSpiceDouble   v2[3],
*       SpiceDouble        vout[3] ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* v1         I     First vector to be added. 
* v2         I     Second vector to be added. 
* vout       O     Sum vector, v1 + v2. 
* vout can overwrite either v1 or v2. 
***********************************************************************/

%rename (vadd) vadd_c;

%apply (double  IN_ARRAY1[ANY]) {double v1  [3]};
%apply (double  IN_ARRAY1[ANY]) {double v2  [3]};
%apply (double OUT_ARRAY1[ANY]) {double vout[3]};
%apply (void RETURN_VOID) {void vadd_c};

extern void vadd_c (
        double v1  [3],
        double v2  [3],
        double vout[3] );

/***********************************************************************
* -Procedure vaddg_c ( Vector addition, general dimension )
*
* -Abstract
*
* add two vectors of arbitrary dimension.
*
* void vaddg_c (
*       ConstSpiceDouble  * v1,
*       ConstSpiceDouble  * v2,
*       SpiceInt            ndim,
*       SpiceDouble       * vout )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* v1        I     First vector to be added.
* v2        I     Second vector to be added.
* ndim      I     Dimension of v1, v2, and vout.
* vout      O     Sum vector, v1 + v2.
* vout can overwrite either v1 or v2.
***********************************************************************/

%rename (vaddg) my_vaddg_c;

%apply (double   *IN_ARRAY1, int    DIM1) {(double  *v1, int   nd1)};
%apply (double   *IN_ARRAY1, int    DIM1) {(double  *v2, int   nd2)};
%apply (double **OUT_ARRAY1, int *SIZE1) {(double **v3, int *nd3)};
%apply (void RETURN_VOID) {void my_vaddg_c};

%inline %{
    void my_vaddg_c(double  *v1, int   nd1,
                    double  *v2, int   nd2,
                    double **v3, int *nd3) {

        double *result = NULL;

        *v3 = NULL;
        *nd3 = 0;

        if (!my_assert_eq(nd1, nd2,
            "Vector size mismatch in VADDG")) return;

        result = my_malloc(nd1);
        if (!result) return;

        vaddg_c(v1, v2, nd1, result);
        *v3 = result;
        *nd3 = nd1;
    }
%}

/***********************************************************************
* -Procedure vcrss_c ( Vector cross product, 3 dimensions )
*
* -Abstract
*
* Compute the cross product of two 3-dimensional vectors.
*
* void vcrss_c (
*       ConstSpiceDouble   v1[3],
*       ConstSpiceDouble   v2[3],
*       SpiceDouble        vout[3] )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* v1         I     Left hand vector for cross product.
* v2         I     Right hand vector for cross product.
* vout       O     Cross product v1xv2.
* vout can overwrite either v1 or v2.
***********************************************************************/

%rename (vcrss) vcrss_c;

%apply (double  IN_ARRAY1[ANY]) {double v1  [3]};
%apply (double  IN_ARRAY1[ANY]) {double v2  [3]};
%apply (double OUT_ARRAY1[ANY]) {double vout[3]};
%apply (void RETURN_VOID) {void vcrss_c};

extern void vcrss_c (
        double v1  [3],
        double v2  [3],
        double vout[3] );

/***********************************************************************
* -Procedure vdist_c ( Vector distance )
*
* -Abstract
*
* Return the distance between two three-dimensional vectors.
*
* SpiceDouble vdist_c (
*       ConstSpiceDouble v1[3],
*       ConstSpiceDouble v2[3] )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* v1,
* v2         I   Two 3-vectors.
*
* The function returns the distance between v1 and v2.
***********************************************************************/

%rename (vdist) vdist_c;

%apply (double IN_ARRAY1[ANY]) {double v1[3]};
%apply (double IN_ARRAY1[ANY]) {double v2[3]};
%apply (double RETURN_DOUBLE) {double vdist_c};

extern double vdist_c (
        double v1[3],
        double v2[3] );

/***********************************************************************
* -Procedure vdistg_c ( Vector distance, general dimension )
*
* -Abstract
*
* Return the distance between two vectors of arbitrary dimension.
*
* SpiceDouble vdistg_c (
*       ConstSpiceDouble   * v1,
*       ConstSpiceDouble   * v2,
*       SpiceInt             ndim )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* v1,
* v2         I   Two vectors of arbitrary dimension.
* ndim       I   The common dimension of v1 and v2
* The function returns the distance between v1 and v2.
***********************************************************************/

%rename (vdistg) my_vdistg_c;

%apply (double *IN_ARRAY1, int  DIM1) {(double *v1, int nd1)}
%apply (double *IN_ARRAY1, int  DIM1) {(double *v2, int nd2)}
%apply (double RETURN_DOUBLE) {double my_vdistg_c};

%inline %{
    double my_vdistg_c(double *v1, int nd1,
                       double *v2, int nd2) {

        if (!my_assert_eq(nd1, nd2,
            "Vector size mismatch in VDISTG")) return NAN;

        return vdistg_c(v1, v2, nd1);
    }
%}

/***********************************************************************
* -Procedure  vdot_c ( Vector dot product, 3 dimensions )
*
* -Abstract
*
* Compute the dot product of two double precision, 3-dimensional
* vectors.
*
* SpiceDouble vdot_c (
*       ConstSpiceDouble   v1[3], 
*       ConstSpiceDouble   v2[3] )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* v1         I   First vector in the dot product.
* v2         I   Second vector in the dot product.
* The function returns the value of the dot product of v1 and v2.
***********************************************************************/

%rename (vdot) vdot_c;

%apply (double IN_ARRAY1[ANY]) {double v1[3]}; 
%apply (double IN_ARRAY1[ANY]) {double v2[3]};
%apply (double RETURN_DOUBLE ) {double vdot_c};

extern double vdot_c (
        double v1[3], 
        double v2[3] );

/***********************************************************************
* -Procedure vdotg_c ( Vector dot product, general dimension )
*
* -Abstract
*
* Compute the dot product of two vectors of arbitrary dimension.
*
* SpiceDouble vdotg_c (
*       ConstSpiceDouble   * v1,
*       ConstSpiceDouble   * v2,
*       SpiceInt             ndim )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* v1        I     First vector in the dot product.
* v2        I     Second vector in the dot product.
* ndim      I     Dimension of v1 and v2.
* The function returns the value of the dot product of v1 and v2.
***********************************************************************/

%rename (vdotg) my_vdotg_c;

%apply (double *IN_ARRAY1, int  DIM1) {(double *v1, int nd1)};
%apply (double *IN_ARRAY1, int  DIM1) {(double *v2, int nd2)};
%apply (double RETURN_DOUBLE) {double my_vdotg_c};

%inline %{
    double my_vdotg_c(double *v1, int nd1,
                      double *v2, int nd2) {

        if (!my_assert_eq(nd1, nd2,
            "Vector size mismatch in VDOTG")) return NAN;

        return vdotg_c(v1, v2, nd1);
    }
%}

/***********************************************************************
* -Procedure vequ_c ( Vector equality, 3 dimensions )
*
* -Abstract
*
* Make one double precision 3-dimensional vector equal to 
* another. 
*
* void vequ_c (
*       ConstSpiceDouble   vin[3],
*       SpiceDouble        vout[3] ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* vin       I   3-dimensional double precision vector. 
* vout      O   3-dimensional double precision vector set equal 
* to vin. 
***********************************************************************/

%rename (vequ) vequ_c;

%apply (double  IN_ARRAY1[ANY]) {double vin [3]};
%apply (double OUT_ARRAY1[ANY]) {double vout[3]};
%apply (void RETURN_VOID) {void vequ_c};

extern void vequ_c (
        double vin [3],
        double vout[3] );

/***********************************************************************
* -Procedure vequg_c ( Vector equality, general dimension )
*
* -Abstract
*
* Make one double precision vector of arbitrary dimension equal
* to another.
*
* void vequg_c (
*       ConstSpiceDouble  * vin,
*       SpiceInt            ndim,
*       SpiceDouble       * vout )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* vin       I   ndim-dimensional double precision vector.
* ndim      I   Dimension of vin (and also vout).
* vout      O   ndim-dimensional double precision vector set
*               equal to vin.
***********************************************************************/

%rename (vequg) my_vequg_c;

%apply (double   *IN_ARRAY1, int    DIM1) {(double  *v1, int   nd1)};
%apply (double **OUT_ARRAY1, int *SIZE1) {(double **v2, int *nd2)};
%apply (void RETURN_VOID) {void my_vequg_c};

%inline %{
    void my_vequg_c(double  *v1, int  nd1,
                    double **v2, int *nd2) {

        double *result = NULL;

        *v2 = NULL;
        *nd2 = 0;

        result = my_malloc(nd1);
        if (!result) return;

        vequg_c(v1, nd1, result);
        *v2 = result;
        *nd2 = nd1;
    }
%}

/***********************************************************************
* -Procedure  vhat_c ( "V-Hat", unit vector along V, 3 dimensions )
*
* -Abstract
*
* Find the unit vector along a double precision 3-dimensional vector.
*
* void vhat_c (
*       ConstSpiceDouble  v1  [3], 
*       SpiceDouble       vout[3] )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* v1         I   Vector to be unitized.
* vout       O   Unit vector v1 / |v1|.
***********************************************************************/

%rename (vhat) vhat_c;

%apply (double  IN_ARRAY1[ANY]) {double v1  [3]}; 
%apply (double OUT_ARRAY1[ANY]) {double vout[3]};
%apply (void RETURN_VOID) {void vhat_c};

extern void vhat_c (
        double v1  [3], 
        double vout[3] );

/***********************************************************************
* -Procedure vhatg_c ( "V-Hat", unit vector along V, general dimension )
*
* -Abstract
*
* Find the unit vector along a double precision vector of 
* arbitrary dimension. 
*
* void vhatg_c (
*       ConstSpiceDouble   * v1,
*       SpiceInt             ndim,
*       SpiceDouble        * vout ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* v1         I   Vector to be normalized. 
* ndim       I   Dimension of v1 (and also vout). 
* vout       O   Unit vector v1 / |v1|. 
*
* If v1 = 0, vout will also be zero. 
* vout can overwrite v1. 
***********************************************************************/

%rename (vhatg) my_vhatg_c;

%apply (double   *IN_ARRAY1, int    DIM1) {(double  *v1, int   nd1)};
%apply (double **OUT_ARRAY1, int *SIZE1) {(double **v2, int *nd2)};
%apply (void RETURN_VOID) {void my_vhatg_c};

%inline %{
    void my_vhatg_c(double  *v1, int   nd1,
                    double **v2, int *nd2) {

        double *result = NULL;

        *v2 = NULL;
        *nd2 = 0;

        result = my_malloc(nd1);
        if (!result) return;

        vhatg_c(v1, nd1, result);
        *v2 = result;
        *nd2 = nd1;
    }
%}

/***********************************************************************
* -Procedure vlcom3_c ( Vector linear combination, 3 dimensions )
*
* -Abstract
*
* This subroutine computes the vector linear combination 
* a*v1 + b*v2 + c*v3 of double precision, 3-dimensional vectors. 
*
* void vlcom3_c (
*       SpiceDouble        a, 
*       ConstSpiceDouble   v1 [3], 
*       SpiceDouble        b, 
*       ConstSpiceDouble   v2 [3], 
*       SpiceDouble        c, 
*       ConstSpiceDouble   v3 [3], 
*       SpiceDouble        sum[3]  ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* a          I   Coefficient of v1 
* v1         I   Vector in 3-space 
* b          I   Coefficient of v2 
* v2         I   Vector in 3-space 
* c          I   Coefficient of v3 
* v3         I   Vector in 3-space 
* sum        O   Linear Vector Combination a*v1 + b*v2 + c*v3 
***********************************************************************/

%rename (vlcom3) vlcom3_c;

%apply (double  IN_ARRAY1[ANY]) {double v1 [3]}; 
%apply (double  IN_ARRAY1[ANY]) {double v2 [3]}; 
%apply (double  IN_ARRAY1[ANY]) {double v3 [3]}; 
%apply (double OUT_ARRAY1[ANY]) {double sum[3]}; 
%apply (void RETURN_VOID) {void vlcom3_c};

extern void vlcom3_c (
        double a, 
        double v1[3], 
        double b, 
        double v2[3], 
        double c, 
        double v3[3], 
        double sum[3] );

/***********************************************************************
* -Procedure      vlcom_c ( Vector linear combination, 3 dimensions )
*
* -Abstract
*
* Compute a vector linear combination of two double precision, 
* 3-dimensional vectors. 
*
* void vlcom_c (
*       SpiceDouble        a, 
*       ConstSpiceDouble   v1[3], 
*       SpiceDouble        b, 
*       ConstSpiceDouble   v2[3], 
*       SpiceDouble        sum[3] ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* a          I   Coefficient of v1 
* v1         I   Vector in 3-space 
* b          I   Coefficient of v2 
* v2         I   Vector in 3-space 
* sum        O   Linear Vector Combination a*v1 + b*v2 
***********************************************************************/

%rename (vlcom) vlcom_c;

%apply (double  IN_ARRAY1[ANY]) {double v1 [3]}; 
%apply (double  IN_ARRAY1[ANY]) {double v2 [3]}; 
%apply (double OUT_ARRAY1[ANY]) {double sum[3]}; 
%apply (void RETURN_VOID) {void vlcom_c};

extern void vlcom_c (
        double a, 
        double v1[3], 
        double b, 
        double v2[3], 
        double sum[3] );

/***********************************************************************
* -Procedure vlcomg_c ( Vector linear combination, general dimension )
*
* -Abstract
*
* Compute a vector linear combination of two double precision
* vectors of arbitrary dimension.
*
* void vlcomg_c (
*       SpiceInt            n,
*       SpiceDouble         a,
*       ConstSpiceDouble *  v1,
*       SpiceDouble         b,
*       ConstSpiceDouble *  v2,
*       SpiceDouble      *  sum )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* n          I   Dimension of vector space
* a          I   Coefficient of v1
* v1         I   Vector in n-space
* b          I   Coefficient of v2
* v2         I   Vector in n-space
* sum        O   Linear Vector Combination a*v1 + b*v2
***********************************************************************/

%rename (vlcomg) my_vlcomg_c;

%apply (double   *IN_ARRAY1, int   DIM1) {(double  *v1, int   nd1)};
%apply (double   *IN_ARRAY1, int   DIM1) {(double  *v2, int   nd2)};
%apply (double **OUT_ARRAY1, int *SIZE1) {(double **v3, int *nd3)};
%apply (void RETURN_VOID) {void my_vlcomg_c};

%inline %{
    void my_vlcomg_c(double a, double  *v1, int  nd1,
                     double b, double  *v2, int  nd2,
                               double **v3, int *nd3) {

        double *result = NULL;

        *v3 = NULL;
        *nd3 = 0;

        if (!my_assert_eq(nd1, nd2,
            "Vector size mismatch in VLCOMG")) return;

        result = my_malloc(nd1);
        if (!result) return;

        vlcomg_c(nd1, a, v1, b, v2, result);
        *v3 = result;
        *nd3 = nd1;
    }
%}

/***********************************************************************
* -Procedure vminug_c ( Minus V, "-V", general dimension )
*
* -Abstract
*
* Negate a double precision vector of arbitrary dimension.
*
* void vminug_c (
*       ConstSpiceDouble  * vin,
*       SpiceInt            ndim,
*       SpiceDouble       * vout )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* vin       I   ndim-dimensional double precision vector to
*               be negated.
* ndim      I   Dimension of vin (and also vout).
* vout      O   ndim-dimensional double precision vector equal to
*               -vin.
***********************************************************************/

%rename (vminug) my_vminug_c;

%apply (double   *IN_ARRAY1, int    DIM1) {(double  *v1,  int  nd1)};
%apply (double **OUT_ARRAY1, int *SIZE1) {(double **v2, int *nd2)};
%apply (void RETURN_VOID) {void my_vminug_c};

%inline %{
    void my_vminug_c(double  *v1,  int  nd1,
                     double **v2, int *nd2) {

        double *result = NULL;

        *v2 = NULL;
        *nd2 = 0;

        result = my_malloc(nd1);
        if (!result) return;

        vminug_c(v1, nd1, result);
        *v2 = result;
        *nd2 = nd1;
    }
%}

/***********************************************************************
* -Procedure vminus_c ( Minus V, "-V", 3 dimensions )
*
* -Abstract
*
* Negate a double precision 3-dimensional vector. 
*
* void vminus_c (
*       ConstSpiceDouble v1[3]
        doublevout[3] ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* v1         I     Vector to be negated. 
* vout       O     Negated vector -v1. vout can overwrite v1. 
***********************************************************************/

%rename (vminus) vminus_c;

%apply (double  IN_ARRAY1[ANY]) {double v1  [3]};
%apply (double OUT_ARRAY1[ANY]) {double vout[3]};
%apply (void RETURN_VOID) {void vminus_c};

extern void vminus_c (
        double v1  [3],
        double vout[3] );

/***********************************************************************
* -Procedure  vnorm_c ( Vector norm, 3 dimensions )
*
* -Abstract
*
* Compute the magnitude of a double precision, 3-dimensional vector.
*
* SpiceDouble vnorm_c (
*       ConstSpiceDouble v1[3] )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* v1         I   Vector whose magnitude is to be found.
* The function returns the norm of v1.
***********************************************************************/

%rename (vnorm) vnorm_c;

%apply (double IN_ARRAY1[ANY]) {double v1[3]};
%apply (double RETURN_DOUBLE ) {double vnorm_c};

extern double vnorm_c (
        double v1[3] );

/***********************************************************************
* -Procedure vnormg_c ( Vector norm, general dimension )
*
* -Abstract
*
* Compute the magnitude of a double precision vector of arbitrary 
* dimension. 
*
* SpiceDouble vnormg_c (
*       ConstSpiceDouble   * v1,
*       SpiceInt             ndim ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* v1        I     Vector whose magnitude is to be found. 
* ndim      I     Dimension of v1. 
***********************************************************************/

%rename (vnormg) vnormg_c;

%apply (double *IN_ARRAY1, int DIM1) {(double *v1, int ndim)};
%apply (double RETURN_DOUBLE) {double vnormg_c};

extern double vnormg_c (
        double *v1, int ndim );

/***********************************************************************
* -Procedure vpack_c ( Pack three scalar components into a vector )
*
* -Abstract
*
* Pack three scalar components into a vector. 
*
* void vpack_c (
*       SpiceDouble   x,
*       SpiceDouble   y,
*       SpiceDouble   z,
*       SpiceDouble   v[3] ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* x, 
* y, 
* z          I   Scalar components of a 3-vector. 
* v          O   Equivalent 3-vector.
***********************************************************************/

%rename (vpack) vpack_c;

%apply (double OUT_ARRAY1[ANY]) {double v[3]};
%apply (void RETURN_VOID) {void vpack_c};

extern void vpack_c (
        double x,
        double y,
        double z,
        double v[3] );

/***********************************************************************
* -Procedure vperp_c ( Perpendicular component of a 3-vector)
*
* -Abstract
*
* Find the component of a vector that is perpendicular to a second
* vector.  All vectors are 3-dimensional.
*
* void vperp_c (
*       ConstSpiceDouble   a[3],
*       ConstSpiceDouble   b[3],
*       SpiceDouble        p[3] )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* a         I    The vector whose orthogonal component is sought.
* b         I    The vector used as the orthogonal reference.
* p         O    The component of a orthogonal to b.
***********************************************************************/

%rename (vperp) vperp_c;

%apply (double  IN_ARRAY1[ANY]) {double a[3]};
%apply (double  IN_ARRAY1[ANY]) {double b[3]};
%apply (double OUT_ARRAY1[ANY]) {double p[3]};
%apply (void RETURN_VOID) {void vperp_c};

extern void vperp_c (
        double a[3],
        double b[3],
        double p[3] );

/***********************************************************************
* -Procedure vprjp_c ( Vector projection onto plane )
*
* -Abstract
*
* Project a vector onto a specified plane, orthogonally. 
*
* void vprjp_c (
*       ConstSpiceDouble    vin   [3],
*       ConstSpicePlane   * plane,
*       SpiceDouble         vout  [3] ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* vin        I   Vector to be projected. 
* plane      I   A CSPICE plane onto which vin is projected. 
* vout       O   Vector resulting from projection. 
***********************************************************************/

%rename (vprjp) vprjp_c;

%apply (double  IN_ARRAY1[ANY]) {double vin[3]};
%apply (double  IN_ARRAY1[ANY]) {double plane[NPLANE]};
%apply (double OUT_ARRAY1[ANY]) {double vout[3]};
%apply (void RETURN_VOID) {void vprjp_c};

extern void vprjp_c (
        double vin[3],
        double plane[NPLANE],
        double vout[3]      );

/***********************************************************************
* -Procedure vprjpi_c ( Vector projection onto plane, inverted )
*
* -Abstract
*
* Find the vector in a specified plane that maps to a specified 
* vector in another plane under orthogonal projection. 
*
* void vprjpi_c (
*       ConstSpiceDouble    vin    [3],
*       ConstSpicePlane   * projpl,
*       ConstSpicePlane   * invpl,
*       SpiceDouble         vout   [3],
*       SpiceBoolean      * found       ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* vin        I   The projected vector. 
* projpl     I   Plane containing vin. 
* invpl      I   Plane containing inverse image of vin. 
* vout       O   Inverse projection of vin. 
* found      O   Flag indicating whether vout could be calculated. 
***********************************************************************/

%rename (vprjpi) vprjpi_c;

%apply (double   IN_ARRAY1[ANY]) {double vin[3]};
%apply (double   IN_ARRAY1[ANY]) {double projpl[NPLANE]};
%apply (double   IN_ARRAY1[ANY]) {double invpl[NPLANE]};
%apply (double  OUT_ARRAY1[ANY]) {double vout[3]};
%apply (void RETURN_VOID) {void vprjpi_c};

extern void vprjpi_c (
        double vin[3],
        double projpl[NPLANE],
        double invpl [NPLANE],
        double vout[3],
        int *OUT_BOOLEAN );

/***********************************************************************
* -Procedure vproj_c ( Vector projection, 3 dimensions )
*
* -Abstract
*
* vproj_c finds the projection of one vector onto another vector.
* all vectors are 3-dimensional.
*
* void vproj_c (
*       ConstSpiceDouble   a[3],
*       ConstSpiceDouble   b[3],
*       SpiceDouble        p[3] )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* a         I    The vector to be projected.
* b         I    The vector onto which a is to be projected.
* p         O    The projection of a onto b.
***********************************************************************/

%rename (vproj) vproj_c;

%apply (double  IN_ARRAY1[ANY]) {double a[3]};
%apply (double  IN_ARRAY1[ANY]) {double b[3]};
%apply (double OUT_ARRAY1[ANY]) {double p[3]};
%apply (void RETURN_VOID) {void vproj_c};

extern void vproj_c (
        double a[3],
        double b[3],
        double p[3] );

/***********************************************************************
* -Procedure vrel_c ( Vector relative difference, 3 dimensions )
*
* -Abstract
*
* Return the relative difference between two 3-dimensional vectors.
*
* SpiceDouble vrel_c (
*       ConstSpiceDouble v1[3],
*       ConstSpiceDouble v2[3]  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* v1,v2     I   Input vectors.
***********************************************************************/

%rename (vrel) vrel_c;

%apply (double IN_ARRAY1[ANY]) {double v1[3]};
%apply (double IN_ARRAY1[ANY]) {double v2[3]}; 
%apply (double RETURN_DOUBLE) {double vrel_c};

extern double vrel_c (
        double v1[3],
        double v2[3] );

/***********************************************************************
* -Procedure vrelg_c ( Vector relative difference, general dimension )
*
* -Abstract
*
* Return the relative difference between two vectors of general
* dimension.
*
* SpiceDouble vrelg_c (
*       ConstSpiceDouble * v1,
*       ConstSpiceDouble * v2,
*       SpiceInt           ndim  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* v1,v2     I   Input vectors.
* ndim      I   Dimension of v1 and v2.
***********************************************************************/

%rename (vrelg) my_vrelg_c;

%apply (double *IN_ARRAY1, int DIM1) {(double *v1, int ndim_v1)};
%apply (double *IN_ARRAY1, int DIM1) {(double *v2, int ndim_v2)};
%apply (void RETURN_VOID) {void my_vrelg_c};

%inline %{
    double my_vrelg_c(double *v1, int  ndim_v1,
                      double *v2, int  ndim_v2) {

        if (!my_assert_eq(ndim_v1, ndim_v2,
            "Vector size mismatch in VRELG")) return NAN;

        return vrelg_c(v1, v2, ndim_v1);
    }
%}

/***********************************************************************
* -Procedure vrotv_c ( Vector rotation about an axis )
*
* -Abstract
*
* Rotate a vector about a specified axis vector by a specified 
* angle and return the rotated vector. 
*
* void vrotv_c (
*       ConstSpiceDouble  v     [3],
*       ConstSpiceDouble  axis  [3],
*       SpiceDouble       theta,
*       SpiceDouble       r     [3] ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* v          I   Vector to be rotated. 
* axis       I   Axis of the rotation. 
* theta      I   Angle of rotation (radians). 
* r          O   Result of rotating v about axis by theta. 
***********************************************************************/

%rename (vrotv) vrotv_c;

%apply (double  IN_ARRAY1[ANY]) {double v[3]};
%apply (double  IN_ARRAY1[ANY]) {double axis[3]};
%apply (double OUT_ARRAY1[ANY]) {double r[3]};
%apply (void RETURN_VOID) {void vrotv_c};

extern void vrotv_c (
        double v[3],
        double axis [3],
        double theta,
        double r[3] );

/***********************************************************************
* -Procedure      vscl_c ( Vector scaling, 3 dimensions )
*
* -Abstract
*
* Multiply a scalar and a 3-dimensional double precision vector. 
*
* void vscl_c (
*       SpiceDouble        s,
*       ConstSpiceDouble   v1[3],
*       SpiceDouble        vout[3] ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* s         I     Scalar to multiply a vector. 
* v1        I     Vector to be multiplied. 
* vout      O     Product vector, s*v1. vout can overwrite v1. 
***********************************************************************/

%rename (vscl) vscl_c;

%apply (double  IN_ARRAY1[ANY]) {double v1[3]};
%apply (double OUT_ARRAY1[ANY]) {double vout[3]};
%apply (void RETURN_VOID) {void vscl_c};

extern void vscl_c (
        double s,
        double v1[3],
        double vout[3] );

/***********************************************************************
* -Procedure vsclg_c ( Vector scaling, general dimension )
*
* -Abstract
*
* Multiply a scalar and a double precision vector of arbitrary
* dimension.
*
* void vsclg_c (
*       SpiceDouble          s,
*       ConstSpiceDouble   * v1,
*       SpiceInt             ndim,
*       SpiceDouble        * vout )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* s          I     Scalar to multiply a vector.
* v1         I     Vector to be multiplied.
* ndim       I     Dimension of v1 (and also vout).
* vout       O     Product vector, s*v1. vout can overwrite v1.
***********************************************************************/

%rename (vsclg) my_vsclg_c;

%apply (double   *IN_ARRAY1, int    DIM1) {(double  *v1,  int  nd1)};
%apply (double **OUT_ARRAY1, int *SIZE1) {(double **v2, int *nd2)};
%apply (void RETURN_VOID) {void my_vsclg_c};

%inline %{
    void my_vsclg_c(double    s,
                    double  *v1,  int  nd1,
                    double **v2, int *nd2) {

        double *result = NULL;

        *v2 = NULL;
        *nd2 = 0;

        result = my_malloc(nd1);
        if (!result) return;

        vsclg_c(s, v1, nd1, result);
        *v2 = result;
        *nd2 = nd1;
    }
%}

/***********************************************************************
* -Procedure vsep_c  ( Angular separation of vectors, 3 dimensions )
*
* -Abstract
*
* Find the separation angle in radians between two double 
* precision, 3-dimensional vectors.  This angle is defined as zero 
* if either vector is zero. 
*
* SpiceDouble vsep_c (
*       ConstSpiceDouble v1[3], ConstSpiceDouble v2[3] ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* v1        I     First vector. 
* v2        I     Second vector. 
***********************************************************************/

%rename (vsep) vsep_c;

%apply (double IN_ARRAY1[ANY]) {double v1[3]};
%apply (double IN_ARRAY1[ANY]) {double v2[3]};
%apply (double RETURN_DOUBLE) {double vsep_c};

extern double vsep_c (
        double v1[3],
        double v2[3] );

/***********************************************************************
* -Procedure vsepg_c ( Angular separation of vectors, general dimension )
*
* -Abstract
*
* vsepg_c finds the separation angle in radians between two double
* precision vectors of arbitrary dimension. This angle is defined
* as zero if either vector is zero.
*
* SpiceDouble vsepg_c (
*       ConstSpiceDouble * v1,
*       ConstSpiceDouble * v2,
*       SpiceInt           ndim )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* v1        I     First vector.
* v2        I     Second vector.
* ndim      I     The number of elements in v1 and v2.
***********************************************************************/

%rename (vsepg) my_vsepg_c;

%apply (double *IN_ARRAY1, int  DIM1) {(double *v1, int nd1)}
%apply (double *IN_ARRAY1, int  DIM1) {(double *v2, int nd2)}
%apply (double RETURN_DOUBLE) {double my_vsepg_c};

%inline %{
    double my_vsepg_c(double *v1, int  nd1,
                      double *v2, int  nd2) {

        if (!my_assert_eq(nd1, nd2,
                          "Vector size mismatch in VSEPG")) return NAN;

        return vsepg_c(v1, v2, nd2);
    }
%}

/***********************************************************************
* -Procedure vsub_c ( Vector subtraction, 3 dimensions )
*
* -Abstract
*
* Compute the difference between two 3-dimensional, double 
* precision vectors. 
*
* void vsub_c (
*       ConstSpiceDouble   v1[3],
*       ConstSpiceDouble   v2[3],
*       SpiceDouble        vout[3] ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* v1         I     First vector (minuend). 
* v2         I     Second vector (subtrahend). 
* vout       O     Difference vector, v1 - v2. vout can overwrite 
* either v1 or v2. 
***********************************************************************/

%rename (vsub) vsub_c;

%apply (double  IN_ARRAY1[ANY]) {double v1  [3]};
%apply (double  IN_ARRAY1[ANY]) {double v2  [3]};
%apply (double OUT_ARRAY1[ANY]) {double vout[3]};
%apply (void RETURN_VOID) {void vsub_c};

extern void vsub_c (
        double v1[3],
        double v2[3],
        double vout[3] );

/***********************************************************************
* -Procedure vsubg_c ( Vector subtraction, general dimension )
*
* -Abstract
*
* Compute the difference between two double precision vectors of
* arbitrary dimension.
*
* void vsubg_c (
*       ConstSpiceDouble  * v1,
*       ConstSpiceDouble  * v2,
*       SpiceInt            ndim,
*       SpiceDouble       * vout )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* v1        I     First vector (minuend).
* v2        I     Second vector (subtrahend).
* ndim      I     Dimension of v1, v2, and vout.
* vout      O     Difference vector, v1 - v2.
* vout can overwrite either v1 or v2.
***********************************************************************/

%rename (vsubg) my_vsubg_c;

%apply (double   *IN_ARRAY1, int    DIM1) {(double  *v1, int   nd1)};
%apply (double   *IN_ARRAY1, int    DIM1) {(double  *v2, int   nd2)};
%apply (double **OUT_ARRAY1, int *SIZE1) {(double **v3, int *nd3)};
%apply (void RETURN_VOID) {void my_vsubg_c};

%inline %{
    void my_vsubg_c(double  *v1, int   nd1,
                    double  *v2, int   nd2,
                    double **v3, int *nd3) {

        double *result = NULL;

        *v3 = NULL;
        *nd3 = 0;

        if (!my_assert_eq(nd1, nd2,
            "Vector size mismatch in VSUBG")) return;

        result = my_malloc(nd1);
        if (!result) return;

        vsubg_c(v1, v2, nd1, result);
        *v3 = result;
        *nd3 = nd1;
    }
%}

/***********************************************************************
* -Procedure vtmv_c ( Vector transpose times matrix times vector, 3 dim )
*
* -Abstract
*
* Multiply the transpose of a 3-dimensional column vector, 
* a 3x3 matrix, and a 3-dimensional column vector. 
*
* SpiceDouble vtmv_c (
*       ConstSpiceDouble v1     [3],
*       ConstSpiceDouble matrix [3][3],
*       ConstSpiceDouble v2     [3] ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* v1        I     3 dimensional double precision column vector. 
* matrix    I     3x3 double precision matrix. 
* v2        I     3 dimensional double precision column vector. 
* The function returns the result of (v1**t * matrix * v2 ). 
***********************************************************************/

%rename (vtmv) vtmv_c;

%apply (double  IN_ARRAY1[ANY]     ) {double v1[3]};
%apply (double  IN_ARRAY2[ANY][ANY]) {double matrix[3][3]};
%apply (double OUT_ARRAY1[ANY]     ) {double v2[3]};
%apply (double RETURN_DOUBLE) {double vtmv_c};

extern double vtmv_c (
        double v1[3],
        double matrix[3][3],
        double v2[3] );

/***********************************************************************
* -Procedure vtmvg_c  ( Vector transpose times matrix times vector )
*
* -Abstract
*
* Multiply the transpose of a n-dimensional column vector,
* a nxm matrix, and a m-dimensional column vector.
*
* SpiceDouble vtmvg_c (
*       void                * v1,
*       const void          * matrix,
*       const void          * v2,
*       SpiceInt              nrow,
*       SpiceInt              ncol    )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* v1        I   n-dimensional double precision column vector.
* matrix    I   nxm double precision matrix.
* v2        I   m-dimensional double porecision column vector.
* nrow      I   Number of rows in matrix (number of rows in v1.)
* ncol      I   Number of columns in matrix (number of rows in
*               v2.)
* The function returns the result of (v1**t * matrix * v2 ).
***********************************************************************/

%rename (vtmvg) my_vtmvg_c;

%apply (double *IN_ARRAY1, int DIM1) {(double *v1, int nrow1)};
%apply (double *IN_ARRAY1, int DIM1) {(double *v2, int ncol2)};
%apply (double *IN_ARRAY2, int DIM1, int DIM2)
                {(double *matrix, int nrow, int ncol)};
%apply (double RETURN_DOUBLE) {double my_vtmvg_c};

%inline %{
    double my_vtmvg_c(double *v1, int nrow1,
                      double *matrix, int nrow, int ncol,
                      double *v2, int ncol2) {

        if (!my_assert_eq(nrow1, nrow,
                          "Row size mismatch in VTMVG")) return NAN;

        if (!my_assert_eq(ncol2, ncol,
                          "Column size mismatch in VTMVG")) return NAN;

        return vtmvg_c(v1, matrix, v2, nrow, ncol);
    }
%}

/***********************************************************************
* -Procedure vupack_c ( Unpack three scalar components from a vector )
*
* -Abstract
*
* Unpack three scalar components from a vector. 
*
* void vupack_c (
*       ConstSpiceDouble     v[3],
*       SpiceDouble        * x,
*       SpiceDouble        * y,
*       SpiceDouble        * z     ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* v          I   3-vector.
* x, 
* y, 
* z          O   Scalar components of 3-vector. 
***********************************************************************/

%rename (vupack) vupack_c;

%apply (double IN_ARRAY1[ANY]) {double v[3]};
%apply (void RETURN_VOID) {void vupack_c};

extern void vupack_c (
        double v[3],
        double *OUTPUT,
        double *OUTPUT,
        double *OUTPUT );

/***********************************************************************
* -Procedure vzero_c ( Is a vector the zero vector? )
*
* -Abstract
*
* Indicate whether a 3-vector is the zero vector. 
*
* SpiceBoolean vzero_c (
*       ConstSpiceDouble v[3] ) 
*
* -Brief_I/O
*
* Variable  I/O  Description 
* --------  ---  -------------------------------------------------- 
* v          I   Vector to be tested. 
* The function returns the value SPICETRUE if and only if v is the 
* zero vector. 
***********************************************************************/

%rename (vzero) vzero_c;

%apply (double IN_ARRAY1[ANY]) {double v[3]};
%apply (int RETURN_BOOLEAN) {int vzero_c};

extern int vzero_c (
        double v[3] );

/***********************************************************************
* -Procedure vzerog_c ( Is a vector the zero vector?---general dim. )
*
* -Abstract
*
* Indicate whether a general-dimensional vector is the zero vector.
*
* SpiceBoolean vzerog_c (
*       ConstSpiceDouble * v, SpiceInt ndim )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* v          I   Vector to be tested.
* ndim       I   Dimension of v.
* The function returns the value SPICETRUE if and only if v is the
* zero vector.
***********************************************************************/

%rename (vzerog) vzerog_c;

%apply (double *IN_ARRAY1, int DIM1) {(double *v, int ndim)};
%apply (int RETURN_BOOLEAN) {int vzerog_c};

extern int vzerog_c (
        double *v, int ndim);

/***********************************************************************
* -Procedure xf2eul_c ( State transformation to Euler angles )
*
* -Abstract
*
* Convert a state transformation matrix to Euler angles and their 
* derivatives with respect to a specified set of axes. 
* The companion routine eul2xf_c converts Euler angles and their 
* derivatives with respect to a specified set of axes to a state 
* transformation matrix. 
*
* void xf2eul_c (
*       ConstSpiceDouble     xform  [6][6],
*       SpiceInt             axisa,
*       SpiceInt             axisb,
*       SpiceInt             axisc,
*       SpiceDouble          eulang [6],
*       SpiceBoolean       * unique         ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* xform      I   A state transformation matrix. 
* axisa      I   Axis A of the Euler angle factorization. 
* axisb      I   Axis B of the Euler angle factorization. 
* axisc      I   Axis C of the Euler angle factorization. 
* eulang     O   An array of Euler angles and their derivatives. 
* unique     O   Indicates if eulang is a unique representation. 
***********************************************************************/

%rename (xf2eul) xf2eul_c;

%apply (double   IN_ARRAY2[ANY][ANY]) {double xform [6][6]};
%apply (double  OUT_ARRAY1[ANY]     ) {double eulang[6]};
%apply (int    *OUT_BOOLEAN         ) {int *unique};
%apply (void RETURN_VOID) {void xf2eul_c};

extern void xf2eul_c (
        double xform[6][6],
        int axisa,
        int axisb,
        int axisc,
        double eulang[6],
        int *unique );

/***********************************************************************
* -Procedure xf2rav_c ( Transform to rotation and angular velocity)
*
* -Abstract
*
* This routine determines from a state transformation matrix 
* the associated rotation matrix and angular velocity of the 
* rotation. 
*
* void xf2rav_c (
*       ConstSpiceDouble   xform [6][6],
*       SpiceDouble        rot   [3][3],
*       SpiceDouble        av    [3]     ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* xform      I   is a state transformation matrix. 
* rot        O   is the rotation associated with xform. 
* av         O   is the angular velocity associated with xform. 
***********************************************************************/

%rename (xf2rav) xf2rav_c;

%apply (double  IN_ARRAY2[ANY][ANY]) {double xform[6][6]};
%apply (double OUT_ARRAY2[ANY][ANY]) {double rot  [3][3]};
%apply (double OUT_ARRAY1[ANY]     ) {double av   [3]}; 
%apply (void RETURN_VOID) {void xf2rav_c};

extern void xf2rav_c (
        double xform[6][6],
        double rot  [3][3],
        double av   [3]    );

/***********************************************************************
* -Procedure  xpose6_c ( Transpose a matrix, 6x6 )
*
* -Abstract
*
* Transpose a 6x6 matrix.
*
* void xpose6_c (
*       ConstSpiceDouble m1[6][6]
        doublemout[6][6] )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* m1        I   6x6 matrix to be transposed.
* mout      I   Transpose of m1.  mout can overwrite m1.
***********************************************************************/

%rename (xpose6) xpose6_c;

%apply (double  IN_ARRAY2[ANY][ANY]) {double   m1[6][6]};
%apply (double OUT_ARRAY2[ANY][ANY]) {double mout[6][6]};
%apply (void RETURN_VOID) {void xpose6_c};

extern void xpose6_c (
        double m1  [6][6],
        double mout[6][6] );

/***********************************************************************
* -Procedure  xpose_c ( Transpose a matrix, 3x3 )
*
* -Abstract
*
* Transpose a 3x3 matrix.
*
* void xpose_c (
*       ConstSpiceDouble m1[3][3]
        doublemout[3][3] )
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION
* --------  ---  --------------------------------------------------
* m1        I   3x3 matrix to be transposed.
* mout      I   Transpose of m1.  mout can overwrite m1.
***********************************************************************/

%rename (xpose) xpose_c;

%apply (double  IN_ARRAY2[ANY][ANY]) {double m1  [3][3]};
%apply (double OUT_ARRAY2[ANY][ANY]) {double mout[3][3]};
%apply (void RETURN_VOID) {void xpose_c};

extern void xpose_c (
        double m1  [3][3],
        double mout[3][3] );

/***********************************************************************
* -Procedure      xposeg_c ( Transpose a matrix, general )
*
* -Abstract
*
* Transpose a matrix of arbitrary size (in place, the matrix 
* need not be square). 
*
* void xposeg_c (
*       void         * matrix, 
*       SpiceInt       nrow, 
*       SpiceInt       ncol, 
*       void         * xposem ) 
*
* -Brief_I/O
*
* VARIABLE  I/O  DESCRIPTION 
* --------  ---  -------------------------------------------------- 
* matrix     I   Matrix to be transposed. 
* nrow       I   Number of rows of input matrix. 
* ncol       I   Number of columns of input matrix. 
* xposem     O   Transposed matrix (xposem can overwrite matrix). 
***********************************************************************/

%rename (xposeg) my_xposeg_c;

%apply (double *IN_ARRAY2, int DIM1, int DIM2)
                {(double *matrix, int nrow,  int ncol)};
%apply (double **OUT_ARRAY2, int *SIZE1, int *SIZE2)
                {(double **xposem, int *nrow1,  int *ncol1)};
%apply (void RETURN_VOID) {void my_xposeg_c};

/* Helper function to deal with missing arguments */
%inline %{
    void my_xposeg_c(double *matrix,  int nrow,   int  ncol,
                     double **xposem, int *nrow1, int *ncol1) {

        double *result = NULL;

        *xposem = NULL;
        *nrow1 = 0;
        *ncol1 = 0;

        result = my_malloc(nrow * ncol);
        if (!result) return;

        xposeg_c(matrix, nrow, ncol, result);
        *xposem = result;
        *nrow1 = ncol;
        *ncol1 = nrow;
    }
%}

/***********************************************************************
***********************************************************************/
