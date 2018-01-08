%module cspyce0
%{
#define SWIG_FILE_WITH_INIT

#include "SpiceUsr.h"
#include "SpiceCel.h"
#include "SpiceOsc.h"
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
SpiceDouble *my_malloc(int count, const char *fname) {
    SpiceDouble *result = (SpiceDouble *) PyMem_Malloc(count *
                                                       sizeof(SpiceDouble));
    if (!result) {
        chkin_c(fname);
        setmsg_c("Failed to allocate memory");
        sigerr_c("SPICE(MALLOCFAILURE)");
        chkout_c(fname);
    }

    return result;
}

SpiceInt *my_int_malloc(int count, const char *fname) {
    SpiceInt *result = (SpiceInt *) PyMem_Malloc(count * sizeof(SpiceInt));
    if (!result) {
        chkin_c(fname);
        setmsg_c("Failed to allocate memory");
        sigerr_c("SPICE(MALLOCFAILURE)");
        chkout_c(fname);
    }

    return result;
}

SpiceInt *my_bool_malloc(int count, const char *fname) {
    SpiceInt *result = (SpiceInt *) PyMem_Malloc(count * sizeof(SpiceBoolean));
    if (!result) {
        chkin_c(fname);
        setmsg_c("Failed to allocate memory");
        sigerr_c("SPICE(MALLOCFAILURE)");
        chkout_c(fname);
    }

    return result;
}

/* Internal routine to compare integers for equality */
int my_assert_eq(int a, int b, const char *fname, const char *message) {

    if (a != b) {
        chkin_c(fname);
        setmsg_c(message);
        errint_c("#", a);
        errint_c("#", b);
        sigerr_c("SPICE(ARRAYSHAPEMISMATCH)");
        chkout_c(fname);
        return 0;
    }
    return 1;
}

// Prototypes
int frmchg_(SpiceInt    *frame1,
            SpiceInt    *frame2,
            SpiceDouble *et,
            SpiceDouble *xform);

int refchg_(SpiceInt    *frame1,
            SpiceInt    *frame2,
            SpiceDouble *et,
            SpiceDouble *rotate);

int stcf01_(ConstSpiceChar *catnam,
            SpiceDouble    *westra,
            SpiceDouble    *eastra,
            SpiceDouble    *sthdec,
            SpiceDouble    *nthdec,
            SpiceInt       *nstars,
            int            catnam_len);

int stcg01_(SpiceInt    *index,
            SpiceDouble *ra,
            SpiceDouble *dec,
            SpiceDouble *rasig,
            SpiceDouble *decsig,
            SpiceInt    *catnum,
            SpiceChar   *sptype,
            SpiceDouble *vmag,
            int         sptype_len);

int stcl01_(ConstSpiceChar *catfnm,
            SpiceChar      *tabnam,
            SpiceInt       *handle,
            int            catfnm_len,
            int            tabnam_len);

void stlabx_(ConstSpiceDouble pobj[3],
             ConstSpiceDouble vobs[3],
             SpiceDouble      corpos[3]);

// From cspyce_typemaps.i
void set_python_exception_flag(int flag);
int get_python_exception_flag(void);
char *get_message_after_reset(int option);
void reset_messages(void);

%}

%include "typemaps.i"
%include "cspyce_typemaps.i"
%include "vectorize.i"

%init %{
        import_array(); /* For numpy interface */
        erract_c("SET", 256, "RETURN");
        errdev_c("SET", 256, "NULL");   /* Suppresses default error messages */
%}

%feature("autodoc", "1");

// Copy standard typemaps for Spice types
%apply int {SpiceInt, SpiceBoolean, ConstSpiceInt, ConstSpiceBoolean};
%apply char {SpiceChar, ConstSpiceChar}
%apply double {SpiceDouble, ConstSpiceDouble};

%apply int *OUTPUT {SpiceInt *OUTPUT, SpiceBoolean *OUTPUT};
%apply char *OUTPUT {SpiceChar *OUTPUT}
%apply double *OUTPUT {SpiceDouble *OUTPUT};

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

%apply (ConstSpiceDouble  IN_ARRAY1[ANY]) {ConstSpiceDouble axis[3]};
%apply (SpiceDouble OUT_ARRAY2[ANY][ANY]) {SpiceDouble rout[3][3]};
%apply (void RETURN_VOID) {void axisar_c};

extern void axisar_c(
        ConstSpiceDouble axis[3],
        SpiceDouble angle,
        SpiceDouble rout[3][3]);

// Vector version
VECTORIZE_dX_d__dMN(axisar, axisar_c, 3, 3)

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

extern SpiceDouble b1900_c(void);

/***********************************************************************
* -Procedure b1950_c ( Besselian Date 1950.0 )
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

extern SpiceDouble b1950_c (void);

/***********************************************************************
* -Procedure bltfrm_c ( Built-in frame IDs )
*
* -Abstract
*
*    Return a SPICE set containing the frame IDs of all built-in frames
*    of a specified class.
*
*    void bltfrm_c ( SpiceInt      frmcls,
*                    SpiceCell   * idset  ) 
*
* -Brief_I/O
*
*    VARIABLE  I/O  DESCRIPTION 
*    --------  ---  -------------------------------------------------- 
*    frmcls     I   Frame class. 
*    idset      O   Set of ID codes of frames of the specified class. 
*
***********************************************************************/

%rename (bltfrm) my_bltfrm_c;

%apply (SpiceInt OUT_ARRAY1[ANY], SpiceInt *SIZE1)
                          {(SpiceInt idset[1000], SpiceInt *count)};
%apply (void RETURN_VOID) {void my_bltfrm_c};

%inline %{
    /* Helper function to create an array of results */
    void my_bltfrm_c(SpiceInt frmcls,
                     SpiceInt idset[1000], SpiceInt *count) {

        int j;
        SPICEINT_CELL(ids, 1000);

        scard_c(0, &ids);
        bltfrm_c(frmcls, &ids);

        *count = card_c(&ids);
        for (j = 0; j < *count; j++) {
            idset[j] = SPICE_CELL_ELEM_I(&ids, j);
        }
    }
%}

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

%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
                                    {(SpiceInt lenout, SpiceChar name[256])};
%apply (void RETURN_VOID) {void bodc2n_c};

extern void bodc2n_c(
        SpiceInt code,
        SpiceInt lenout, SpiceChar name[256],
        SpiceBoolean *OUT_BOOLEAN);

/***********************************************************************
* -Procedure bodc2s_c ( Body ID code to string translation )
*
* -Abstract
*
*    Translate a body ID code to either the corresponding name or if no
*    name to ID code mapping exists, the string representation of the
*    body ID value.
*
*    void bodc2s_c ( SpiceInt        code,
*                    SpiceInt        lenout,
*                    SpiceChar     * name )
*
* -Brief_I/O
*
*    Variable  I/O  Description
*    --------  ---  --------------------------------------------------
*    code       I   Integer ID code to translate to a string.
*    lenout     I   Maximum length of output name.
*    name       O   String corresponding to 'code'.
*
***********************************************************************/

%rename (bodc2s) bodc2s_c;

%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
                          {(SpiceInt lenout, SpiceChar name[256])};
%apply (void RETURN_VOID) {void bodc2s_c};

extern void bodc2s_c(
        SpiceInt code,
        SpiceInt lenout, SpiceChar name[256]);

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

extern void boddef_c(
        ConstSpiceChar *CONST_STRING,
        SpiceInt code);

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

%apply (SpiceBoolean RETURN_BOOLEAN) {SpiceBoolean bodfnd_c};

extern SpiceBoolean bodfnd_c(
        SpiceInt       body,
        ConstSpiceChar *CONST_STRING);

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
        ConstSpiceChar *CONST_STRING,
        SpiceInt       *OUTPUT,
        SpiceBoolean   *OUT_BOOLEAN);

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

extern void bods2c_c(
        ConstSpiceChar *CONST_STRING,
        SpiceInt       *OUTPUT,
        SpiceBoolean   *OUT_BOOLEAN);

/***********************************************************************
* -Procedure  bodvar_c ( Return values from the kernel pool )
* 
* -Abstract
* 
*    Deprecated: This routine has been superseded by bodvcd_c and
*    bodvrd_c.  This routine is supported for purposes of backward
*    compatibility only.
* 
*    Return the values of some item for any body in the
*    kernel pool.
* 
*    void bodvar_c ( SpiceInt           body,
*                    ConstSpiceChar   * item,
*                    SpiceInt         * dim,
*                    SpiceDouble      * values )
* 
* -Brief_I/O
* 
*    VARIABLE  I/O  DESCRIPTION
*    --------  ---  --------------------------------------------------
*    body       I   ID code of body.
*    item       I   Item for which values are desired. ("RADII",
*                   "NUT_PREC_ANGLES", etc. )
*    dim        O   Number of values returned.
*    values     O   Values.
* 
***********************************************************************/

%rename (bodvar) bodvar_c;

%apply (SpiceInt *SIZE1, SpiceDouble OUT_ARRAY1[ANY])
                          {(SpiceInt *dim, SpiceDouble values[80])};
%apply (void RETURN_VOID) {void bodvar_c};

extern void bodvar_c(
        SpiceInt       body,
        ConstSpiceChar *CONST_STRING,
        SpiceInt       *dim, SpiceDouble values[80]);

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

%apply (SpiceInt DIM1, SpiceInt *SIZE1, SpiceDouble OUT_ARRAY1[ANY])
                       {(SpiceInt maxn, SpiceInt *dim, SpiceDouble values[80])};
%apply (void RETURN_VOID) {void bodvcd_c};

extern void bodvcd_c(
        SpiceInt       bodyid,
        ConstSpiceChar *CONST_STRING,
        SpiceInt maxn, SpiceInt *dim, SpiceDouble values[80]);

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

%apply (SpiceInt DIM1, SpiceInt *SIZE1, SpiceDouble OUT_ARRAY1[ANY])
                    {(SpiceInt maxn, SpiceInt *dim, SpiceDouble values[80])};
%apply (void RETURN_VOID) {void bodvrd_c};

extern void bodvrd_c(
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceInt maxn, SpiceInt *dim, SpiceDouble values[80]);

/***********************************************************************
* -Procedure ccifrm_c ( Class and class ID to associated frame )
* 
* -Abstract
*  
*    Return the frame name, frame ID, and center associated with 
*    a given frame class and class ID. 
*  
* -   void ccifrm_c ( SpiceInt          frclss,
*                    SpiceInt          clssid,
*                    SpiceInt          lenout,
*                    SpiceInt        * frcode,
*                    SpiceChar       * frname,
*                    SpiceInt        * center,
*                    SpiceBoolean    * found   )
* 
* -Brief_I/O
*  
*    VARIABLE  I/O  DESCRIPTION 
*    --------  ---  -------------------------------------------------- 
*    frclss     I   Class of frame. 
*    clssid     I   Class ID of frame. 
*    lenout     I   Maximum length of output string.
*    frcode     O   ID code of the frame.
*    frname     O   Name of the frame.
*    center     O   ID code of the center of the frame.
*    found      O   SPICETRUE if the requested information is available. 
***********************************************************************/

%rename (ccifrm) my_ccifrm_c;

%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
                                   {(SpiceInt lenout, SpiceChar frname[256])};
%apply (SpiceInt *OUTPUT)          {SpiceInt *frcode};
%apply (SpiceInt *OUTPUT)          {SpiceInt *center};
%apply (SpiceBoolean *OUT_BOOLEAN) {SpiceBoolean *found};
%apply (void RETURN_VOID)          {void my_ccifrm_c};

/* Helper function to reorder arguments */
%inline %{
    void my_ccifrm_c(SpiceInt frclss,
                     SpiceInt clssid,
                     SpiceInt *frcode,
                     SpiceInt lenout, SpiceChar frname[256],
                     SpiceInt *center,
                     SpiceBoolean *found) {

        ccifrm_c(frclss, clssid, lenout, frcode, frname, center, found);
    }
%}

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble center[3]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble vec1[3]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble vec2[3]};
%apply (SpiceDouble OUT_ARRAY1[ANY])     {SpiceDouble ellipse[NELLIPSE]};
%apply (void RETURN_VOID) {void cgv2el_c};

extern void cgv2el_c(
        ConstSpiceDouble center[3],
        ConstSpiceDouble vec1[3],
        ConstSpiceDouble vec2[3],
        SpiceDouble      ellipse[NELLIPSE]);

// Vector version
VECTORIZE_dX_dX_dX__dN(cgv2el, cgv2el_c, NELLIPSE)

/***********************************************************************
*-Procedure chkin_c ( module Check In )
*
*-Abstract
*
*   Inform the CSPICE error handling mechanism of entry into a
*   routine.
*
*   void chkin_c ( ConstSpiceChar * module )
*
* -Brief_I/O
*
*   VARIABLE  I/O  DESCRIPTION
*   --------  ---  ---------------------------------------------------
*   module     I   The name of the calling routine.
***********************************************************************/

%rename (chkin) chkin_c;

extern void chkin_c(ConstSpiceChar *CONST_STRING);

/***********************************************************************
*-Procedure chkout_c ( Module Check Out )
*
*-Abstract
*
*   Inform the CSPICE error handling mechanism of exit from a
*   routine.
*
*   void chkout_c ( ConstSpiceChar  * module )
*
* -Brief_I/O
*
*   VARIABLE  I/O  DESCRIPTION
*   --------  ---  --------------------------------------------------
*   module     I   The name of the calling routine.
***********************************************************************/

%rename (chkout) chkout_c;

extern void chkout_c(ConstSpiceChar *CONST_STRING);

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

%apply (SpiceInt *OUTPUT)          {SpiceInt *frcode};
%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
                                   {(SpiceInt lenout, SpiceChar frname[256])};
%apply (SpiceBoolean *OUT_BOOLEAN) {SpiceBoolean *found};
%apply (void RETURN_VOID)          {void my_cidfrm_c};

/* Helper function to reorder arguments */
%inline %{
    void my_cidfrm_c(SpiceInt cent,
                     SpiceInt *frcode,
                     SpiceInt lenout, SpiceChar frname[256],
                     SpiceBoolean *found) {

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

%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *ck};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *level};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *timsys};
%apply (SpiceDouble OUT_ARRAY2[ANY][ANY], SpiceInt *SIZE1)
                          {(SpiceDouble array[500][2], SpiceInt *intervals)};
%apply (void RETURN_VOID) {void my_ckcov_c};

%inline %{
    /* Helper function to create a 2-D array of results */
    void my_ckcov_c(ConstSpiceChar *ck,
                    SpiceInt       idcode,
                    SpiceBoolean   needav,
                    ConstSpiceChar *level,
                    SpiceDouble    tol,
                    ConstSpiceChar *timsys,
                    SpiceDouble array[500][2], SpiceInt *intervals) {

        int j;
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
* -Procedure ckgp_c ( C-kernel, get pointing )
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

%apply (SpiceDouble OUT_ARRAY2[ANY][ANY]) {SpiceDouble cmat[3][3]};
%apply (void RETURN_VOID) {void ckgp_c};

extern void ckgp_c(
        SpiceInt       inst,
        SpiceDouble    sclkdp,
        SpiceDouble    tol,
        ConstSpiceChar *CONST_STRING,
        SpiceDouble    cmat[3][3],
        SpiceDouble    *OUTPUT,
        SpiceBoolean   *OUT_BOOLEAN);

// Vector version
VECTORIZE_i_2d_s__dMN_d_b(ckgp, ckgp_c, 3, 3)

/***********************************************************************
* -Procedure ckgpav_c ( C-kernel, get pointing and angular velocity )
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

%apply (SpiceDouble OUT_ARRAY2[ANY][ANY]) {SpiceDouble cmat[3][3]};
%apply (SpiceDouble OUT_ARRAY1[ANY])      {SpiceDouble   av[3]   };
%apply (void RETURN_VOID) {void ckgpav_c};

extern void ckgpav_c(
        SpiceInt       inst,
        SpiceDouble    sclkdp,
        SpiceDouble    tol,
        ConstSpiceChar *CONST_STRING,
        SpiceDouble    cmat[3][3],
        SpiceDouble    av[3],
        SpiceDouble    *OUTPUT,
        SpiceBoolean   *OUT_BOOLEAN);

// Vector version
VECTORIZE_i_2d_s__dLM_dN_d_b(ckgpav, ckgpav_c, 3, 3, 3)

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

%apply (ConstSpiceChar *CONST_STRING)    {ConstSpiceChar *ck};
%apply (int OUT_ARRAY1[ANY], int *SIZE1) {(int body_ids[200], int *bodies)};
%apply (void RETURN_VOID) {void my_ckobj_c};

/* Helper function to create a 1-D array of results */
%inline %{
    void my_ckobj_c(ConstSpiceChar *ck, int body_ids[200], int *bodies) {
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
* -Procedure clight_c ( C, Speed of light in a vacuum )
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

extern SpiceDouble clight_c(void);

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

extern void clpool_c(void);

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

%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *cname};
%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
                                     {(SpiceInt lenout, SpiceChar frname[256])};
%apply (SpiceInt *OUTPUT)            {SpiceInt *frcode};
%apply (SpiceBoolean *OUT_BOOLEAN)   {SpiceBoolean *found};
%apply (void RETURN_VOID) {void my_cnmfrm_c};

%inline %{
    /* Helper function to reorder arguments */
    void my_cnmfrm_c(ConstSpiceChar *cname,
                     SpiceInt       *frcode,
                     SpiceInt lenout, SpiceChar frname[256],
                     SpiceBoolean   *found) {

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble elts[8]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble state[6]};
%apply (void RETURN_VOID)                {void conics_c};

extern void conics_c(
        ConstSpiceDouble elts[8],
        SpiceDouble      et,
        SpiceDouble      state[6]);

// Vector version
VECTORIZE_dX_d__dN(conics, conics_c, 6)

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

extern void convrt_c(
        SpiceDouble    x,
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceDouble    *OUTPUT);

// Vector version
VECTORIZE_d_2s__d(convrt, convrt_c)

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

extern void cyllat_c(
        SpiceDouble r,
        SpiceDouble lonc,
        SpiceDouble z,
        SpiceDouble *OUTPUT,
        SpiceDouble *OUTPUT,
        SpiceDouble *OUTPUT);

// Vector version
VECTORIZE_3d__3d(cyllat, cyllat_c)

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

%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble rectan[3]};
%apply (void RETURN_VOID) {void cylrec_c};

extern void cylrec_c(
        SpiceDouble r,
        SpiceDouble lon,
        SpiceDouble z,
        SpiceDouble rectan[3]);

// Vector version
VECTORIZE_3d__dN(cylrec, cylrec_c, 3)

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

extern void cylsph_c(
        SpiceDouble r,
        SpiceDouble lonc,
        SpiceDouble z,
        SpiceDouble *OUTPUT,
        SpiceDouble *OUTPUT,
        SpiceDouble *OUTPUT);

// Vector version
VECTORIZE_3d__3d(cylsph, cylsph_c)

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

extern void dafbfs_c(
        SpiceInt handle);

/***********************************************************************
* -Procedure dafcls_c ( DAF, close )
* 
* -Abstract
* 
* Close the DAF associated with a given handle.
* 
* void dafcls_c ( SpiceInt handle )
* 
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle of DAF to be closed.
***********************************************************************/

%rename (dafcls) dafcls_c;
%apply (void RETURN_VOID) {void dafcls_c};

extern void dafcls_c(
        SpiceInt handle);

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
%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble data[256]};
%apply (void RETURN_VOID) {void dafgda_c};

extern void dafgda_c(
        SpiceInt    handle,
        SpiceInt    begin,
        SpiceInt    end,
        SpiceDouble data[256]);

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

%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
                          {(SpiceInt lenout, SpiceChar string[256])};
%apply (void RETURN_VOID) {void dafgn_c};

extern void dafgn_c(
        SpiceInt lenout, SpiceChar string[256]);

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

%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble sum[128]};
%apply (void RETURN_VOID) {void dafgs_c};

extern void dafgs_c(
        SpiceDouble sum[128]);

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

extern void daffna_c(
        SpiceBoolean *OUT_BOOLEAN);

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

extern void dafopr_c(
        ConstSpiceChar *CONST_STRING,
        SpiceInt       *OUTPUT);

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble sum[128]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble dc[128]};
%apply (SpiceInt        OUT_ARRAY1[ANY]) {SpiceInt ic[256]};
%apply (void RETURN_VOID) {void my_dafus_c};

extern void dafus_c(
        ConstSpiceDouble sum[128],
        SpiceInt nd,
        SpiceInt ni,
        SpiceDouble dc[128],
        SpiceInt ic[256]);

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

%apply (SpiceDouble OUT_ARRAY2[ANY][ANY]) {SpiceDouble jacobi[3][3]};
%apply (void RETURN_VOID) {void dcyldr_c};

extern void dcyldr_c(
        SpiceDouble x,
        SpiceDouble y,
        SpiceDouble z,
        SpiceDouble jacobi[3][3]);

//Vector version
VECTORIZE_3d__dMN(dcyldr, dcyldr_c, 3, 3)

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

extern void deltet_c(
        SpiceDouble    epoch,
        ConstSpiceChar *CONST_STRING,
        SpiceDouble    *OUTPUT);

//Vector version
VECTORIZE_d_s__d(deltet, deltet_c)

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

%apply (ConstSpiceDouble IN_ARRAY2[ANY][ANY]) {ConstSpiceDouble m1[3][3]};
%apply (SpiceDouble RETURN_DOUBLE) {SpiceDouble det_c};

extern SpiceDouble det_c(
        ConstSpiceDouble m1[3][3]);

//Vector version
VECTORIZE_dXY__RETURN_d(det, det_c)

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

%apply (SpiceDouble OUT_ARRAY2[ANY][ANY]) {SpiceDouble jacobi[3][3]};
%apply (void RETURN_VOID) {void dgeodr_c};

extern void dgeodr_c(
        SpiceDouble x,
        SpiceDouble y,
        SpiceDouble z,
        SpiceDouble re,
        SpiceDouble f,
        SpiceDouble jacobi[3][3]);

//Vector version
VECTORIZE_5d__dMN(dgeodr, dgeodr_c, 3, 3)

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

%apply (ConstSpiceDouble IN_ARRAY2[ANY][ANY]) {ConstSpiceDouble symmat[2][2]};
%apply (SpiceDouble     OUT_ARRAY2[ANY][ANY]) {SpiceDouble      diag  [2][2]};
%apply (SpiceDouble     OUT_ARRAY2[ANY][ANY]) {SpiceDouble      rotate[2][2]};
%apply (void RETURN_VOID) {void diags2_c};

extern void diags2_c(
        ConstSpiceDouble symmat[2][2],
        SpiceDouble      diag  [2][2],
        SpiceDouble      rotate[2][2]);

//Vector version
VECTORIZE_dXY__dKL_dMN(diags2, diags2_c, 2, 2, 2, 2)

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

%apply (SpiceDouble OUT_ARRAY2[ANY][ANY]) {SpiceDouble jacobi[3][3]};
%apply (void RETURN_VOID) {void dlatdr_c};

extern void dlatdr_c(
        SpiceDouble x,
        SpiceDouble y,
        SpiceDouble z,
        SpiceDouble jacobi[3][3]);

//Vector version
VECTORIZE_3d__dMN(dlatdr, dlatdr_c, 3, 3)

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

%apply (SpiceDouble OUT_ARRAY2[ANY][ANY]) {SpiceDouble jacobi[3][3]};
%apply (void RETURN_VOID) {void dpgrdr_c};

extern void dpgrdr_c(
        ConstSpiceChar *CONST_STRING,
        SpiceDouble x,
        SpiceDouble y,
        SpiceDouble z,
        SpiceDouble re,
        SpiceDouble f,
        SpiceDouble jacobi[3][3]);

//Vector version
VECTORIZE_s_5d__dMN(dpgrdr, dpgrdr_c, 3, 3)

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

extern SpiceDouble dpmax_c(void);

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

extern SpiceDouble dpmin_c(void);

/***********************************************************************
* -Procedure dpr_c ( Degrees per radian )
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

extern SpiceDouble dpr_c(void);

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

%apply (SpiceDouble OUT_ARRAY2[ANY][ANY]) {SpiceDouble jacobi[3][3]};
%apply (void RETURN_VOID) {void drdcyl_c};

extern void drdcyl_c(
        SpiceDouble r,
        SpiceDouble lon,
        SpiceDouble z,
        SpiceDouble jacobi[3][3]);

//Vector version
VECTORIZE_3d__dMN(drdcyl, drdcyl_c, 3, 3)

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

%apply (SpiceDouble OUT_ARRAY2[ANY][ANY]) {SpiceDouble jacobi[3][3]};
%apply (void RETURN_VOID) {void drdgeo_c};

extern void drdgeo_c(
        SpiceDouble lon,
        SpiceDouble lat,
        SpiceDouble alt,
        SpiceDouble re,
        SpiceDouble f,
        SpiceDouble jacobi[3][3]);

//Vector version
VECTORIZE_5d__dMN(drdgeo, drdgeo_c, 3, 3)

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

%apply (SpiceDouble OUT_ARRAY2[ANY][ANY]) {SpiceDouble jacobi[3][3]};
%apply (void RETURN_VOID) {void drdlat_c};

extern void drdlat_c(
        SpiceDouble r,
        SpiceDouble lon,
        SpiceDouble lat,
        SpiceDouble jacobi[3][3]);

//Vector version
VECTORIZE_3d__dMN(drdlat, drdlat_c, 3, 3)

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

%apply (SpiceDouble OUT_ARRAY2[ANY][ANY]) {SpiceDouble jacobi[3][3]};
%apply (void RETURN_VOID) {void drdpgr_c};

extern void drdpgr_c(
        ConstSpiceChar *CONST_STRING,
        SpiceDouble lon,
        SpiceDouble lat,
        SpiceDouble alt,
        SpiceDouble re,
        SpiceDouble f,
        SpiceDouble jacobi[3][3]);

//Vector version
VECTORIZE_s_5d__dMN(drdpgr, drdpgr_c, 3, 3)

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

%apply (SpiceDouble OUT_ARRAY2[ANY][ANY]) {SpiceDouble jacobi[3][3]};
%apply (void RETURN_VOID) {void drdsph_c};

extern void drdsph_c(
        SpiceDouble r,
        SpiceDouble colat,
        SpiceDouble lon,
        SpiceDouble jacobi[3][3]);

//Vector version
VECTORIZE_3d__dMN(drdsph, drdsph_c, 3, 3)

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

%apply (SpiceDouble OUT_ARRAY2[ANY][ANY]) {SpiceDouble jacobi[3][3]};
%apply (void RETURN_VOID) {void dsphdr_c};

extern void dsphdr_c(
        SpiceDouble x,
        SpiceDouble y,
        SpiceDouble z,
        SpiceDouble jacobi[3][3]);

//Vector version
VECTORIZE_3d__dMN(dsphdr, dsphdr_c, 3, 3)

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

extern void dtpool_c(
        ConstSpiceChar *CONST_STRING,
        SpiceBoolean   *OUT_BOOLEAN,
        SpiceInt       *OUTPUT,
        SpiceChar      OUT_STRING[2]);

/***********************************************************************
* -Procedure ducrss_c ( Unit Normalized Cross Product and Derivative )
*
* -Abstract
*
*    Compute the unit vector parallel to the cross product of
*    two 3-dimensional vectors and the derivative of this unit vector.
*
*    void ducrss_c ( ConstSpiceDouble s1  [6],
*                    ConstSpiceDouble s2  [6],
*                    SpiceDouble      sout[6] )
*
* -Brief_I/O
*
*
*    VARIABLE  I/O  DESCRIPTION
*    --------  ---  --------------------------------------------------
*    s1        I   Left hand state for cross product and derivative.
*    s2        I   Right hand state for cross product and derivative.
*    sout      O   Unit vector and derivative of the cross product.
***********************************************************************/

%rename (ducrss) ducrss_c;

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble s1[6]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble s2[6]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble    sout[6]};
%apply (void RETURN_VOID) {void ducrss_c};

extern void ducrss_c(
        ConstSpiceDouble   s1[6],
        ConstSpiceDouble   s2[6],
        SpiceDouble      sout[6]);

//Vector version
VECTORIZE_dX_dX__dN(ducrss, ducrss_c, 6)

/***********************************************************************
* -Procedure dvcrss_c ( Derivative of Vector cross product )
*
* -Abstract
*
*    Compute the cross product of two 3-dimensional vectors
*    and the derivative of this cross product.
*
*    void dvcrss_c ( ConstSpiceDouble s1  [6],
*                    ConstSpiceDouble s2  [6],
*                    SpiceDouble      sout[6] )
*
* -Brief_I/O
*
*    VARIABLE  I/O  DESCRIPTION
*    --------  ---  --------------------------------------------------
*    s1        I   Left hand state for cross product and derivative.
*    s2        I   Right hand state for cross product and derivative.
*    sout      O   State associated with cross product of positions.
***********************************************************************/

%rename (dvcrss) dvcrss_c;

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble s1[6]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble s2[6]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble    sout[6]};
%apply (void RETURN_VOID) {void dvcrss_c};

extern void dvcrss_c(
        ConstSpiceDouble s1[6],
        ConstSpiceDouble s2[6],
        SpiceDouble      sout[6]);

//Vector version
VECTORIZE_dX_dX__dN(dvcrss, dvcrss_c, 6)

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble s1[6]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble s2[6]};
%apply (SpiceDouble RETURN_DOUBLE)       {SpiceDouble dvdot_c};

extern SpiceDouble dvdot_c(
        ConstSpiceDouble s1[6],
        ConstSpiceDouble s2[6]);

//Vector version
VECTORIZE_dX_dX__RETURN_d(dvdot, dvdot_c)

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble s1[6]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble    sout[6]};
%apply (void RETURN_VOID) {void dvhat_c};

extern void dvhat_c(
        ConstSpiceDouble s1[6],
        SpiceDouble      sout[6]);

//Vector version
VECTORIZE_dX__dN(dvhat, dvhat_c, 6)

/***********************************************************************
* -Procedure dvnorm_c ( Derivative of vector norm )
*
* -Abstract
*
*    Function to calculate the derivative of the norm of a 3-vector.
*
*    SpiceDouble       dvnorm_c ( ConstSpiceDouble state[6] )
*
* -Brief_I/O
*
*    VARIABLE  I/O  DESCRIPTION
*    --------  ---  --------------------------------------------------
*    state      I   A 6-vector composed of three coordinates and their
*                   derivatives.
***********************************************************************/

%rename (dvnorm) dvnorm_c;

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble state[6]};
%apply (SpiceDouble RETURN_DOUBLE)  {SpiceDouble dvnorm_c};

extern SpiceDouble dvnorm_c(
        ConstSpiceDouble state[6]);

//Vector version
VECTORIZE_dX__RETURN_d(dvnorm, dvnorm_c)

/***********************************************************************
* -Procedure dvpool_c  ( Delete a variable from the kernel pool )
*
* -Abstract
*
*    Delete a variable from the kernel pool.
*
*    void dvpool_c ( ConstSpiceChar  * name )
*
* -Brief_I/O
*
*    VARIABLE  I/O  DESCRIPTION
*    --------  ---  --------------------------------------------------
*    name       I   Name of the kernel variable to be deleted.
***********************************************************************/

%rename (dvpool) dvpool_c;

extern void dvpool_c(
        ConstSpiceChar *CONST_STRING);

%apply (void RETURN_VOID) {void dvpool_c};

/***********************************************************************
* -Procedure dvsep_c ( Time derivative of separation angle )
*
* -Abstract
*
*    Calculate the time derivative of the separation angle between
*    two input states, S1 and S2.
*
*    SpiceDouble dvsep_c (ConstSpiceDouble s1[6], ConstSpiceDouble s2[6] )
*
* -Brief_I/O
*
*    VARIABLE  I/O  DESCRIPTION
*    --------  ---  --------------------------------------------------
*    s1         I   State vector of the first body
*    s2         I   State vector of the second  body
***********************************************************************/

%rename (dvsep) dvsep_c;

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble s1[6]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble s2[6]};
%apply (SpiceDouble       RETURN_DOUBLE) {SpiceDouble dvsep_c};

extern SpiceDouble dvsep_c(
        ConstSpiceDouble s1[6],
        ConstSpiceDouble s2[6]);

//Vector version
VECTORIZE_dX_dX__RETURN_d(dvsep, dvsep_c)

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble viewpt[3]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble    limb[NELLIPSE]};
%apply (void RETURN_VOID) {void edlimb_c};

extern void edlimb_c(
        SpiceDouble      a,
        SpiceDouble      b,
        SpiceDouble      c,
        ConstSpiceDouble viewpt[3],
        SpiceDouble      limb[NELLIPSE]);

//Vector version
VECTORIZE_3d_dX__dN(edlimb, edlimb_c, NELLIPSE)

/***********************************************************************
* -Procedure edterm_c ( Ellipsoid terminator )
*
* -Abstract
*
*    Compute a set of points on the umbral or penumbral terminator of
*    a specified target body, where the target shape is modeled as an
*    ellipsoid.
*
*    void edterm_c ( ConstSpiceChar     * trmtyp,
*                    ConstSpiceChar     * source,
*                    ConstSpiceChar     * target,
*                    SpiceDouble          et,
*                    ConstSpiceChar     * fixref,
*                    ConstSpiceChar     * abcorr,
*                    ConstSpiceChar     * obsrvr,
*                    SpiceInt             npts,
*                    SpiceDouble        * trgepc,
*                    SpiceDouble          obspos  [3],
*                    SpiceDouble          trmpts  [ ][3] )
*
* -Brief_I/O
*
*    Variable  I/O  Description
*    --------  ---  --------------------------------------------------
*    trmtyp     I   Terminator type.
*    source     I   Light source.
*    target     I   Target body.
*    et         I   Observation epoch.
*    fixref     I   Body-fixed frame associated with target.
*    abcorr     I   Aberration correction.
*    obsrvr     I   Observer.
*    npts       I   Number of points in terminator set.
*    trgepc     O   Epoch associated with target center.
*    obspos     O   Position of observer in body-fixed frame.
*    trmpts     O   Terminator point set.
***********************************************************************/

%rename (edterm) my_edterm_c;

%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *trmtyp};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *source};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *target};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *fixref};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *abcorr};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *obsrvr};
%apply (SpiceDouble *OUTPUT)          {SpiceDouble *trgepc};
%apply (SpiceDouble OUT_ARRAY1[ANY])  {SpiceDouble obspos[3]};
%apply (SpiceDouble **OUT_ARRAY2, int *SIZE1, int *SIZE2)
                                {(SpiceDouble **trmpts, int *dim1, int *dim2)};
%apply (void RETURN_VOID)       {void my_edterm_c};

/* Helper function to deal with order of arguments */
%inline %{
    void my_edterm_c(ConstSpiceChar *trmtyp,
                     ConstSpiceChar *source,
                     ConstSpiceChar *target,
                     SpiceDouble    et,
                     ConstSpiceChar *fixref,
                     ConstSpiceChar *abcorr,
                     ConstSpiceChar *obsrvr,
                     SpiceInt       npts,
                     SpiceDouble    *trgepc,
                     SpiceDouble    obspos[3],
                     SpiceDouble    **trmpts, int *dim1, int *dim2) {

        SpiceDouble *result = my_malloc(npts * 3, "edterm");
        if (!result) return;

        edterm_c(trmtyp, source, target, et, fixref, abcorr, obsrvr, npts,
                 trgepc, obspos, result);

        if (failed_c()) {
            free(result);
            *trmpts = NULL;
            *dim1 = 0;
            *dim2 = 3;
        }
        else {
            *trmpts = result;
            *dim1 = npts;
            *dim2 = 3;
        }
    }
%}

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble ellipse[NELLIPSE]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble center[3]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble smajor[3]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble sminor[3]};
%apply (void RETURN_VOID) {void el2cgv_c};

extern void el2cgv_c(
        ConstSpiceDouble ellipse[NELLIPSE],
        SpiceDouble      center[3],
        SpiceDouble      smajor[3],
        SpiceDouble      sminor[3]);

//Vector version
VECTORIZE_dX__dL_dM_dN(el2cgv, el2cgv_c, 3, 3, 3)

/***********************************************************************
* -Procedure eqncpv_c (Equinoctial Elements to position and velocity)
*
* -Abstract
*
*    Compute the state (position and velocity of an object whose
*    trajectory is described via equinoctial elements relative to some
*    fixed plane (usually the equatorial plane of some planet).
*
*    void eqncpv_c ( SpiceDouble        et,
*                    SpiceDouble        epoch,
*                    ConstSpiceDouble   eqel[9],
*                    SpiceDouble        rapol,
*                    SpiceDouble        decpol,
*                    SpiceDouble        state[6] )
*
*
* -Brief_I/O
*
*    VARIABLE  I/O  DESCRIPTION
*    --------  ---  --------------------------------------------------
*    et         I   Epoch in seconds past J2000 to find state
*    epoch      I   Epoch of elements in seconds past J2000
*    eqel       I   Array of equinoctial elements
*    rapol      I   Right Ascension of the pole of the reference plane
*    decpol     I   Declination of the pole of the reference plane
*    state      O   State of the object described by eqel.
***********************************************************************/

%rename (eqncpv) eqncpv_c;

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble eqel[9]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble state[6]};
%apply (void RETURN_VOID) {void eqncpv_c};

extern void eqncpv_c(
        SpiceDouble      et,
        SpiceDouble      epoch,
        ConstSpiceDouble eqel[9],
        SpiceDouble      rapol,
        SpiceDouble      decpol,
        SpiceDouble      state[6]);

//Vector version
VECTORIZE_2d_dX_2d__dN(eqncpv, eqncpv_c, 6)

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

%rename (erract) my_erract_c;

%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *op};
%apply (SpiceInt DIM1, SpiceChar INOUT_STRING[ANY])
                          {(SpiceInt lenout, SpiceChar action[256])};
%apply (void RETURN_VOID) {void erract_c};

// Overlay the "EXCEPTION" option
%inline %{
    void my_erract_c(
        ConstSpiceChar *op,
        SpiceInt lenout, SpiceChar action[256]) {

        if (eqstr_c(op,"GET") && get_python_exception_flag() == 2) {
            strncpy(action, "RUNTIME", lenout);
            return;
        }

        if (eqstr_c(op,"GET") && get_python_exception_flag()) {
            strncpy(action, "EXCEPTION", lenout);
            return;
        }

        if (eqstr_c(op, "SET")) {
            if (eqstr_c(action, "EXCEPTION")) {
                set_python_exception_flag(1);
                action = "RETURN";
            }
            else if (eqstr_c(action, "RUNTIME")) {
                set_python_exception_flag(2);
                action = "RETURN";
            }
            else if (eqstr_c(action, "IGNORE")) {
                set_python_exception_flag(0);
                reset_c();  // Clear existing messages and failed condition
                reset_messages();
            }
            else {
                set_python_exception_flag(0);
            }
        }

        erract_c(op, lenout, action);
    }
%}

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

extern void errch_c(
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING);

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

%apply (SpiceInt DIM1, SpiceChar INOUT_STRING[ANY])
                          {(SpiceInt lenout, SpiceChar device[256])};
%apply (void RETURN_VOID) {void errdev_c};

extern void errdev_c(
        ConstSpiceChar *CONST_STRING,
        SpiceInt lenout, SpiceChar device[256]);

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

extern void errdp_c(
        ConstSpiceChar *CONST_STRING,
        SpiceDouble    number);

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

extern void errint_c(
        ConstSpiceChar *CONST_STRING,
        SpiceInt       number);

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

%apply (SpiceInt DIM1, SpiceChar INOUT_STRING[ANY])
                          {(SpiceInt lenout, SpiceChar list[256])};
%apply (void RETURN_VOID) {void errprt_c};

extern void errprt_c(
        ConstSpiceChar *CONST_STRING,
        SpiceInt lenout, SpiceChar list[256]);

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

%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *ltype};
%apply (SpiceInt *OUTPUT)             {SpiceInt *hr};
%apply (SpiceInt *OUTPUT)             {SpiceInt *mn};
%apply (SpiceInt *OUTPUT)             {SpiceInt *sc};
%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
                                      {(SpiceInt timlen,  SpiceChar time[256])};
%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
                                      {(SpiceInt ampmlen, SpiceChar ampm[10])};
%apply (void RETURN_VOID) {void my_et2lst_c};

%inline %{
    void my_et2lst_c(SpiceDouble    et,
                     SpiceInt       body,
                     SpiceDouble    lon,
                     ConstSpiceChar *ltype,
                     SpiceInt       *hr,
                     SpiceInt       *mn,
                     SpiceInt       *sc,
                     SpiceInt timlen,  SpiceChar time[256],
                     SpiceInt ampmlen, SpiceChar ampm[10]) {

        et2lst_c(et, body, lon, ltype, timlen, ampmlen,
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

%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
                          {(SpiceInt lenout, SpiceChar utcstr[256])};
%apply (void RETURN_VOID) {void et2utc_c};

extern void et2utc_c(
        SpiceDouble    et,
        ConstSpiceChar *CONST_STRING,
        SpiceInt       prec,
        SpiceInt lenout, SpiceChar utcstr[256]);

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

%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
                          {(SpiceInt lenout, SpiceChar string[256])};
%apply (void RETURN_VOID) {void etcal_c};

extern void etcal_c(
        SpiceDouble et,
        SpiceInt lenout, SpiceChar string[256]);

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

%apply (SpiceDouble OUT_ARRAY2[ANY][ANY]) {SpiceDouble rout[3][3]};
%apply (void RETURN_VOID) {void eul2m_c};

extern void eul2m_c(
        SpiceDouble angle3,
        SpiceDouble angle2,
        SpiceDouble angle1,
        SpiceInt    axis3,
        SpiceInt    axis2,
        SpiceInt    axis1,
        SpiceDouble rout[3][3]);

//Vector version
VECTORIZE_3d_3i__dMN(eul2m, eul2m_c, 3, 3)

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

%apply (ConstSpiceDouble  IN_ARRAY1[ANY]) {ConstSpiceDouble eulang[6]};
%apply (SpiceDouble OUT_ARRAY2[ANY][ANY]) {SpiceDouble xform[6][6]};
%apply (void RETURN_VOID) {void eul2xf_c};

extern void eul2xf_c(
        ConstSpiceDouble eulang[6],
        SpiceInt         axisa,
        SpiceInt         axisb,
        SpiceInt         axisc,
        SpiceDouble      xform[6][6]);

//Vector version
VECTORIZE_dX_3i__dMN(eul2xf, eul2xf_c, 6, 6)

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

extern void expool_c(
        ConstSpiceChar *CONST_STRING,
        SpiceBoolean   *OUT_BOOLEAN);

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

%apply (SpiceBoolean RETURN_BOOLEAN) {SpiceBoolean failed_c};

extern SpiceBoolean failed_c(void);

/***********************************************************************
* -Procedure fovray_c ( Is target in FOV at time? )
*
* -Abstract
*
*    Determine if a specified ray is within the field-of-view (FOV) of
*    a specified instrument at a given time.
*
*    void fovray_c ( ConstSpiceChar   * inst,
*                    ConstSpiceDouble   raydir [3],
*                    ConstSpiceChar   * rframe,
*                    ConstSpiceChar   * abcorr,
*                    ConstSpiceChar   * observer,
*                    SpiceDouble      * et,
*                    SpiceBoolean     * visible  )
*
* -Brief_I/O
*
*    VARIABLE         I/O  DESCRIPTION
*    ---------------  ---  ------------------------------------------------
*    inst              I   Name or ID code string of the instrument.
*    raydir            I   Ray's direction vector.
*    rframe            I   Body-fixed, body-centered frame for target body.
*    abcorr            I   Aberration correction flag.
*    observer          I   Name or ID code string of the observer.
*    et                I   Time of the observation (seconds past J2000).
*    visible           O   Visibility flag (SPICETRUE/SPICEFALSE).
***********************************************************************/

%rename (fovray) my_fovray_c;

%apply (ConstSpiceChar    *CONST_STRING) {ConstSpiceChar *inst};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble raydir[3]};
%apply (ConstSpiceChar    *CONST_STRING) {ConstSpiceChar *rframe};
%apply (ConstSpiceChar    *CONST_STRING) {ConstSpiceChar *abcorr};
%apply (ConstSpiceChar    *CONST_STRING) {ConstSpiceChar *observer};
%apply (void RETURN_VOID) {void my_fovray_c};

/* Helper function deals with et passed by pointer not value */

%inline %{
    void my_fovray_c(ConstSpiceChar   *inst,
                     ConstSpiceDouble raydir[3],
                     ConstSpiceChar   *rframe,
                     ConstSpiceChar   *abcorr,
                     ConstSpiceChar   *observer,
                     SpiceDouble      et,
                     SpiceBoolean     *visible) {

        fovray_c(inst, raydir, rframe, abcorr, observer, &et, visible);
    }
%}

//Vector version
VECTORIZE_s_dX_3s_d__b(fovray, my_fovray_c)

/***********************************************************************
* -Procedure fovtrg_c ( Is target in FOV at time? )
*
* -Abstract
*
*    Determine if a specified ephemeris object is within the
*    field-of-view (FOV) of a specified instrument at a given time.
*
*    void fovtrg_c ( ConstSpiceChar   * inst,
*                    ConstSpiceChar   * target,
*                    ConstSpiceChar   * tshape,
*                    ConstSpiceChar   * tframe,
*                    ConstSpiceChar   * abcorr,
*                    ConstSpiceChar   * obsrvr,
*                    SpiceDouble      * et,
*                    SpiceBoolean     * visible  )
*
* -Brief_I/O
*
*    VARIABLE         I/O  DESCRIPTION
*    ---------------  ---  ------------------------------------------------
*    inst              I   Name or ID code string of the instrument.
*    target            I   Name or ID code string of the target.
*    tshape            I   Type of shape model used for the target.
*    tframe            I   Body-fixed, body-centered frame for target body.
*    abcorr            I   Aberration correction flag.
*    obsrvr            I   Name or ID code string of the observer.
*    et                I   Time of the observation (seconds past J2000).
*    visible           O   Visibility flag (SPICETRUE/SPICEFALSE).
***********************************************************************/

%rename (fovtrg) my_fovtrg_c;

%apply (void RETURN_VOID) {void my_fovtrg_c};

%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *inst};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *target};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *tshape};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *tframe};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *abcorr};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *observer};
%apply (void RETURN_VOID) {void my_fovtrg_c};

/* Helper function deals with et passed by pointer not value */

%inline %{
    void my_fovtrg_c(ConstSpiceChar *inst,
                     ConstSpiceChar *target,
                     ConstSpiceChar *tshape,
                     ConstSpiceChar *tframe,
                     ConstSpiceChar *abcorr,
                     ConstSpiceChar *observer,
                     SpiceDouble    et,
                     SpiceBoolean   *visible) {

        fovtrg_c(inst, target, tshape, tframe, abcorr, observer, &et, visible);
    }
%}

//Vector version
VECTORIZE_6s_d__b(fovtrg, my_fovtrg_c)

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

%apply (SpiceDouble IN_ARRAY1[ANY])  {SpiceDouble xin[3]};
%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble x[3]};
%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble y[3]};
%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble z[3]};
%apply (void RETURN_VOID) {void my_frame_c};

/* Helper function deals with in-out argument */

%inline %{
    void my_frame_c(SpiceDouble xin[3],
                    SpiceDouble x[3], SpiceDouble y[3], SpiceDouble z[3]) {
        x[0] = xin[0];
        x[1] = xin[1];
        x[2] = xin[2];
        frame_c(x, y, z);
    }
%}

//Vector version
VECTORIZE_eX__dL_dM_dN(frame, my_frame_c, 3, 3, 3)

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

extern void frinfo_c(
        SpiceInt     frcode,
        SpiceInt     *OUTPUT,
        SpiceInt     *OUTPUT,
        SpiceInt     *OUTPUT,
        SpiceBoolean *OUT_BOOLEAN);

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

%apply (SpiceDouble OUT_ARRAY2[ANY][ANY]) {SpiceDouble xform[6][6]};
%apply (void RETURN_VOID) {void my_frmchg};

/* Helper function to deal with pointers to input arguments */
%inline %{
    void my_frmchg(SpiceInt    frame1,
                   SpiceInt    frame2,
                   SpiceDouble et,
                   SpiceDouble xform[6][6]) {
        frmchg_(&frame1, &frame2, &et, xform);
    }
%}

extern void frmchg_(SpiceInt    *frame1,
                    SpiceInt    *frame2,
                    SpiceDouble *et,
                    SpiceDouble *xform);

//Vector version
VECTORIZE_2i_d__dMN(frmchg, my_frmchg, 6, 6)

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

%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
                          {(SpiceInt lenout, SpiceChar frname[256])};
%apply (void RETURN_VOID) {void frmnam_c};

extern void frmnam_c(
        SpiceInt  frcode,
        SpiceInt  lenout,
        SpiceChar frname[256]);

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

extern void furnsh_c(
        ConstSpiceChar *CONST_STRING);

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

%apply (SpiceInt DIM1, SpiceInt DIM2,
                       SpiceInt *NSTRINGS, char OUT_STRINGS[ANY][ANY])
                {(SpiceInt room, SpiceInt lenout,
                                 SpiceInt *n, char cvals[80][256])};
%apply (void RETURN_VOID) {void gcpool_c};

extern void gcpool_c(
        ConstSpiceChar *CONST_STRING,
        SpiceInt       start,
        SpiceInt room, SpiceInt lenout, SpiceInt *n, char cvals[80][256],
        SpiceBoolean   *OUT_BOOLEAN);

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

%apply (SpiceInt DIM1, SpiceInt *SIZE1, SpiceDouble OUT_ARRAY1[ANY])
                        {(SpiceInt room, SpiceInt *n, SpiceDouble values[80])};
%apply (void RETURN_VOID) {void gdpool_c};

extern void gdpool_c(
        ConstSpiceChar *CONST_STRING,
        SpiceInt       start,
        SpiceInt room, SpiceInt *n, SpiceDouble values[80],
        SpiceBoolean   *OUT_BOOLEAN);

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

%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble rectan[3]};
%apply (void RETURN_VOID) {void georec_c};

extern void georec_c(
        SpiceDouble lon,
        SpiceDouble lat,
        SpiceDouble alt,
        SpiceDouble re,
        SpiceDouble f,
        SpiceDouble rectan[3]);

//Vector version
VECTORIZE_5d__dN(georec, georec_c, 3)

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

%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
                        {(SpiceInt shapelen, SpiceChar shape[256])};
%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
                        {(SpiceInt framelen, SpiceChar frame[256])};
%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble bsight[3]};
%apply (int *SIZE1, int *SIZE2, SpiceDouble OUT_ARRAY2[ANY][ANY])
                        {(int *size1, int *size2, SpiceDouble bounds[1000][3])};
%apply (void RETURN_VOID) {void my_getfov_c};

/* Helper function to deal with order of arguments */
%inline %{
    void my_getfov_c(SpiceInt instid,
                     SpiceInt shapelen, SpiceChar shape[256],
                     SpiceInt framelen, SpiceChar frame[256],
                     SpiceDouble bsight[3],
                     int *size1, int *size2, SpiceDouble bounds[1000][3]) {

        getfov_c(instid, 1000, shapelen, framelen, shape, frame,
                 bsight, size1, bounds);
        *size2 = 3;
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

%rename (getmsg) my_getmsg_c;

%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *option};
%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
                          {(SpiceInt lenout, SpiceChar msg[10000])};
%apply (void RETURN_VOID) {void my_getmsg_c};

// Overlay the "EXCEPTION" option
%inline %{
    void my_getmsg_c(
        ConstSpiceChar *option,
        SpiceInt lenout, SpiceChar msg[10000]) {

        if (get_python_exception_flag()) {
            if (eqstr_c(option,"SHORT")) {
                strncpy(msg, get_message_after_reset(0), 10000);
            }
            else if (eqstr_c(option,"LONG")) {
                strncpy(msg, get_message_after_reset(1), 10000);
            }
            else if (eqstr_c(option,"EXPLAIN")) {
                strncpy(msg, get_message_after_reset(2), 10000);
            }
            else {
                msg[0] = '\0';
            }

            // If this message is blank, a new message might be in progress
            if (msg[0] != '\0') return;
        }

        getmsg_c(option, lenout, msg);
    }
%}

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

%apply (SpiceInt DIM1, SpiceInt *SIZE1, SpiceInt OUT_ARRAY1[ANY])
                            {(SpiceInt room, SpiceInt *n, SpiceInt ivals[80])}
%apply (void RETURN_VOID) {void gipool_c};

extern void gipool_c(
        ConstSpiceChar *CONST_STRING,
        SpiceInt       start,
        SpiceInt room, SpiceInt *n, SpiceInt ivals[80],
        SpiceBoolean   *OUT_BOOLEAN);

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

%apply (SpiceInt DIM1, SpiceInt DIM2,
                       SpiceInt *NSTRINGS, char OUT_STRINGS[ANY][ANY])
        {(SpiceInt room, SpiceInt lenout,
                         SpiceInt *n, char kvars[80][256])};
%apply (void RETURN_VOID) {void gnpool_c};

extern void gnpool_c(
        ConstSpiceChar *CONST_STRING,
        SpiceInt       start,
        SpiceInt room, SpiceInt lenout, SpiceInt *n, char kvars[80][256],
        SpiceBoolean   *OUT_BOOLEAN);

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

%apply (SpiceDouble RETURN_DOUBLE) {SpiceDouble halfpi_c};

extern SpiceDouble halfpi_c(void);

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

%apply (SpiceDouble OUT_ARRAY2[ANY][ANY]) {SpiceDouble matrix[3][3]};
%apply (void RETURN_VOID) {void ident_c};

extern void ident_c(
        SpiceDouble matrix[3][3]);

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble spoint[3]};
%apply (void RETURN_VOID) {void illum_c};

extern void illum_c(
        ConstSpiceChar   *CONST_STRING,
        SpiceDouble      et,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceDouble spoint[3],
        SpiceDouble      *OUTPUT,
        SpiceDouble      *OUTPUT,
        SpiceDouble      *OUTPUT);

//Vector version
VECTORIZE_s_d_2s_dX__3d(illum, illum_c)

/***********************************************************************
* -Procedure illumf_c ( Illumination angles, general source, return flags )
*
* -Abstract
*
*    Compute the illumination angles---phase, incidence, and
*    emission---at a specified point on a target body. Return logical
*    flags indicating whether the surface point is visible from
*    the observer's position and whether the surface point is
*    illuminated.
*
*    The target body's surface is represented using topographic data
*    provided by DSK files, or by a reference ellipsoid.
*
*    The illumination source is a specified ephemeris object.
*
*    void illumf_c ( ConstSpiceChar        * method,
*                    ConstSpiceChar        * target,
*                    ConstSpiceChar        * ilusrc,
*                    SpiceDouble             et,
*                    ConstSpiceChar        * fixref,
*                    ConstSpiceChar        * abcorr,
*                    ConstSpiceChar        * obsrvr,
*                    ConstSpiceDouble        spoint [3],
*                    SpiceDouble           * trgepc,
*                    SpiceDouble             srfvec [3],
*                    SpiceDouble           * phase,
*                    SpiceDouble           * incdnc,
*                    SpiceDouble           * emissn,
*                    SpiceBoolean          * visibl,
*                    SpiceBoolean          * lit       )
*
* -Brief_I/O
*
*    Variable  I/O  Description
*    --------  ---  --------------------------------------------------
*    method     I   Computation method.
*    target     I   Name of target body.
*    ilusrc     I   Name of illumination source.
*    et         I   Epoch in TDB seconds past J2000 TDB.
*    fixref     I   Body-fixed, body-centered target body frame.
*    abcorr     I   Aberration correction flag.
*    obsrvr     I   Name of observing body.
*    spoint     I   Body-fixed coordinates of a target surface point.
*    trgepc     O   Target surface point epoch.
*    srfvec     O   Vector from observer to target surface point.
*    phase      O   Phase angle at the surface point.
*    incdnc     O   Source incidence angle at the surface point.
*    emissn     O   Emission angle at the surface point.
*    visibl     O   Visibility flag (SPICETRUE == visible).
*    lit        O   Illumination flag (SPICETRUE == illuminated).
***********************************************************************/

%rename (illumf) illumf_c;

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble spoint[3]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble srfvec[3]};
%apply (void RETURN_VOID) {void illumf_c};

extern void illumf_c(
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceChar   *CONST_STRING,
        SpiceDouble      et,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceDouble spoint[3],
        SpiceDouble      *OUTPUT,
        SpiceDouble      srfvec[3],
        SpiceDouble      *OUTPUT,
        SpiceDouble      *OUTPUT,
        SpiceDouble      *OUTPUT,
        SpiceBoolean     *OUT_BOOLEAN,
        SpiceBoolean     *OUT_BOOLEAN);

//Vector version
VECTORIZE_3s_d_3s_dX__d_dN_3d_2b(illumf, illumf_c, 3)

/***********************************************************************
* -Procedure illumg_c ( Illumination angles, general source )
*
* -Abstract
*
*    Find the illumination angles (phase, incidence, and
*    emission) at a specified surface point of a target body.
*
*    The surface of the target body may be represented by a triaxial
*    ellipsoid or by topographic data provided by DSK files.
*
*    The illumination source is a specified ephemeris object.
*
*    void illumg_c ( ConstSpiceChar        * method,
*                    ConstSpiceChar        * target,
*                    ConstSpiceChar        * ilusrc,
*                    SpiceDouble             et,
*                    ConstSpiceChar        * fixref,
*                    ConstSpiceChar        * abcorr,
*                    ConstSpiceChar        * obsrvr,
*                    ConstSpiceDouble        spoint [3],
*                    SpiceDouble           * trgepc,
*                    SpiceDouble             srfvec [3],
*                    SpiceDouble           * phase,
*                    SpiceDouble           * incdnc,
*                    SpiceDouble           * emissn     )
*
* -Brief_I/O
*
*    Variable  I/O  Description
*    --------  ---  --------------------------------------------------
*    method     I   Computation method.
*    target     I   Name of target body.
*    ilusrc     I   Name of illumination source.
*    et         I   Epoch in TDB seconds past J2000 TDB.
*    fixref     I   Body-fixed, body-centered target body frame.
*    abcorr     I   Aberration correction flag.
*    obsrvr     I   Name of observing body.
*    spoint     I   Body-fixed coordinates of a target surface point.
*    trgepc     O   Target surface point epoch.
*    srfvec     O   Vector from observer to target surface point.
*    phase      O   Phase angle at the surface point.
*    incdnc     O   Source incidence angle at the surface point.
*    emissn     O   Emission angle at the surface point.
***********************************************************************/

%rename (illumg) illumg_c;

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble spoint[3]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble srfvec[3]};
%apply (void RETURN_VOID) {void illumg_c};

extern void illumg_c(
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceChar   *CONST_STRING,
        SpiceDouble      et,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceDouble spoint[3],
        SpiceDouble      *OUTPUT,
        SpiceDouble      srfvec[3],
        SpiceDouble      *OUTPUT,
        SpiceDouble      *OUTPUT,
        SpiceDouble      *OUTPUT);

//Vector version
VECTORIZE_3s_d_3s_dX__d_dN_3d(illumg, illumg_c, 3)

/***********************************************************************
* -Procedure ilumin_c ( Illumination angles )
*
* -Abstract
*
*    Find the illumination angles (phase, solar incidence, and
*    emission) at a specified surface point of a target body.
*
*    This routine supersedes illum_c.
*
*    void ilumin_c ( ConstSpiceChar        * method,
*                    ConstSpiceChar        * target,
*                    SpiceDouble             et,
*                    ConstSpiceChar        * fixref,
*                    ConstSpiceChar        * abcorr,
*                    ConstSpiceChar        * obsrvr,
*                    ConstSpiceDouble        spoint [3],
*                    SpiceDouble           * trgepc,
*                    SpiceDouble             srfvec [3],
*                    SpiceDouble           * phase,
*                    SpiceDouble           * incdnc,
*                    SpiceDouble           * emissn     )
*
* -Brief_I/O
*
*    Variable  I/O  Description
*    --------  ---  --------------------------------------------------
*    method     I   Computation method.
*    target     I   Name of target body.
*    et         I   Epoch in TDB seconds past J2000 TDB.
*    fixref     I   Body-fixed, body-centered target body frame.
*    abcorr     I   Aberration correction flag.
*    obsrvr     I   Name of observing body.
*    spoint     I   Body-fixed coordinates of a target surface point.
*    trgepc     O   Target surface point epoch.
*    srfvec     O   Vector from observer to target surface point.
*    phase      O   Phase angle at the surface point.
*    incdnc     O   Solar incidence angle at the surface point.
*    emissn     O   Emission angle at the surface point.
***********************************************************************/

%rename (ilumin) ilumin_c;

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble spoint[3]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble srfvec[3]};
%apply (void RETURN_VOID) {void ilumin_c};

extern void ilumin_c(
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceChar   *CONST_STRING,
        SpiceDouble      et,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceDouble spoint[3],
        SpiceDouble      *OUTPUT,
        SpiceDouble      srfvec[3],
        SpiceDouble      *OUTPUT,
        SpiceDouble      *OUTPUT,
        SpiceDouble      *OUTPUT);

//Vector version
VECTORIZE_2s_d_3s_dX__d_dN_3d(ilumin, ilumin_c, 3)

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble plane[NPLANE]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble ellipse[NELLIPSE]};
%apply (void RETURN_VOID) {void inedpl_c};

extern void inedpl_c(
        SpiceDouble      a,
        SpiceDouble      b,
        SpiceDouble      c,
        ConstSpiceDouble plane[NPLANE],
        SpiceDouble      ellipse[NELLIPSE],
        SpiceBoolean     *OUT_BOOLEAN);

//Vector version
VECTORIZE_3d_dX__dN_b(inedpl, inedpl_c, NELLIPSE)

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble ellipse[NELLIPSE]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble plane[NPLANE]};
%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble xpt1[3]};
%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble xpt2[3]};
%apply (void RETURN_VOID) {void inelpl_c};

extern void inelpl_c(
        ConstSpiceDouble ellipse[NELLIPSE],
        ConstSpiceDouble plane[NPLANE],
        SpiceInt         *OUTPUT,
        SpiceDouble      xpt1[3],
        SpiceDouble      xpt2[3]);

//Vector version
VECTORIZE_dX_dX__i_dM_dN(inelpl, inelpl_c, 3, 3)

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble vertex[3]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble dir[3]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble plane[NPLANE]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble xpt[3]};
%apply (void RETURN_VOID) {void inrypl_c};

extern void inrypl_c(
        ConstSpiceDouble vertex[3],
        ConstSpiceDouble dir[3],
        ConstSpiceDouble plane[NPLANE],
        SpiceInt         *OUTPUT,
        SpiceDouble      xpt[3]);

//Vector version
VECTORIZE_dX_dX_dX__i_dN(inrypl, inrypl_c, 3)

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

%apply (SpiceInt RETURN_INT) {SpiceInt intmax_c};

extern SpiceInt intmax_c(void);

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

%apply (SpiceInt RETURN_INT) {SpiceInt intmin_c};

extern SpiceInt intmin_c ();

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

%apply (ConstSpiceDouble IN_ARRAY2[ANY][ANY]) {ConstSpiceDouble m1[3][3]};
%apply (SpiceDouble     OUT_ARRAY2[ANY][ANY]) {SpiceDouble    mout[3][3]};
%apply (void RETURN_VOID) {void invert_c};

extern void invert_c(
        ConstSpiceDouble m1[3][3],
        SpiceDouble    mout[3][3]);

//Vector version
VECTORIZE_dXY__dMN(invert, invert_c, 3, 3)

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

%apply (ConstSpiceDouble IN_ARRAY2[ANY][ANY]) {ConstSpiceDouble m[3][3]};
%apply (SpiceDouble     OUT_ARRAY2[ANY][ANY]) {SpiceDouble    mit[3][3]};
%apply (void RETURN_VOID) {void invort_c};

extern void invort_c(
        ConstSpiceDouble m[3][3],
        SpiceDouble    mit[3][3]);

//Vector version
VECTORIZE_dXY__dMN(invort, invort_c, 3, 3)

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

%apply (ConstSpiceDouble IN_ARRAY2[ANY][ANY]) {ConstSpiceDouble m[3][3]};
%apply (SpiceBoolean RETURN_BOOLEAN) {SpiceBoolean isrot_c};

extern SpiceBoolean isrot_c(
        ConstSpiceDouble m[3][3],
        SpiceDouble      ntol,
        SpiceDouble      dtol);

//Vector version
VECTORIZE_dXY_2d__RETURN_b(isrot, isrot_c)

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

%apply (SpiceDouble RETURN_DOUBLE) {SpiceDouble j1900_c};

extern SpiceDouble j1900_c(void);

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

%apply (SpiceDouble RETURN_DOUBLE) {SpiceDouble j1950_c};

extern SpiceDouble j1950_c(void);

/***********************************************************************
* -Procedure j2000_c ( Julian Date of 2000 JAN 1.5 )
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

%apply (SpiceDouble RETURN_DOUBLE) {SpiceDouble j2000_c};

extern SpiceDouble j2000_c(void);

/***********************************************************************
* -Procedure j2100_c ( Julian Date of 2100 JAN 1.5 )
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

%apply (SpiceDouble RETURN_DOUBLE) {SpiceDouble j2100_c};

extern SpiceDouble j2100_c(void);

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

%apply (SpiceDouble RETURN_DOUBLE) {SpiceDouble jyear_c};

extern SpiceDouble jyear_c(void);

/***********************************************************************
* -Procedure kplfrm_c ( Kernel pool frame IDs )
* 
* -Abstract
*  
*    Return a SPICE set containing the frame IDs of all reference 
*    frames of a given class having specifications in the kernel pool. 
*  
*    void kplfrm_c ( SpiceInt      frmcls,
*                    SpiceCell   * idset   ) 
* /*
* 
* -Brief_I/O
*  
*    VARIABLE  I/O  DESCRIPTION 
*    --------  ---  -------------------------------------------------- 
*    frmcls     I   Frame class. 
*    idset      O   Set of ID codes of frames of the specified class. 
***********************************************************************/

%rename (kplfrm) my_kplfrm_c;

%apply (SpiceInt OUT_ARRAY1[ANY], SpiceInt *SIZE1)
                          {(SpiceInt idset[1000], SpiceInt *count)};
%apply (void RETURN_VOID) {void my_bltfrm_c};

%inline %{
    /* Helper function to create an array of results */
    void my_kplfrm_c(SpiceInt frmcls,
                     SpiceInt idset[1000], SpiceInt *count) {

        int j;
        SPICEINT_CELL(ids, 1000);

        scard_c(0, &ids);
        bltfrm_c(frmcls, &ids);

        *count = card_c(&ids);
        for (j = 0; j < *count; j++) {
            idset[j] = SPICE_CELL_ELEM_I(&ids, j);
        }
    }
%}

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

extern void latcyl_c(
        SpiceDouble radius,
        SpiceDouble lon,
        SpiceDouble lat,
        SpiceDouble *OUTPUT,
        SpiceDouble *OUTPUT,
        SpiceDouble *OUTPUT);

// Vector version
VECTORIZE_3d__3d(latcyl, latcyl_c)

/***********************************************************************
* -Procedure latrec_c ( Latitudinal to rectangular coordinates )
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

%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble rectan[3]};
%apply (void RETURN_VOID) {void latrec_c};

extern void latrec_c(
        SpiceDouble radius,
        SpiceDouble longitude,
        SpiceDouble latitude,
        SpiceDouble rectan[3]);

// Vector version
VECTORIZE_3d__dN(latrec, latrec_c, 3)

/***********************************************************************
* -Procedure latsrf_c ( Latitudinal grid to surface points )
*
* -Abstract
*
*    Map array of planetocentric longitude/latitude coordinate pairs
*    to surface points on a specified target body.
*
*    The surface of the target body may be represented by a triaxial
*    ellipsoid or by topographic data provided by DSK files.
*
*    void latsrf_c ( ConstSpiceChar     * method,
*                    ConstSpiceChar     * target,
*                    SpiceDouble          et,
*                    ConstSpiceChar     * fixref,
*                    SpiceInt             npts,
*                    ConstSpiceDouble     lonlat[][2],
*                    SpiceDouble          srfpts[][3]  )
*
* -Brief_I/O
*
*    Variable  I/O  Description
*    --------  ---  --------------------------------------------------
*    method     I   Computation method.
*    target     I   Name of target body.
*    et         I   Epoch in TDB seconds past J2000 TDB.
*    fixref     I   Body-fixed, body-centered target body frame.
*    npts       I   Number of coordinate pairs in input array.
*    lonlat     I   Array of longitude/latitude coordinate pairs.
*    srfpts     O   Array of surface points.
***********************************************************************/

%rename (latsrf) my_latsrf_c;

%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *method};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *target};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *fixref};
%apply (ConstSpiceDouble IN_ARRAY2[ANY][ANY], SpiceInt DIM1)
                            {(ConstSpiceDouble lonlat[1][2], SpiceInt npts)};
%apply (SpiceDouble **OUT_ARRAY2, int *SIZE1, int *SIZE2)
                            {(SpiceDouble **srfpts, int *sdim1, int *sdim2)};
%apply (void RETURN_VOID)   {void my_latsrf_c};

/* Helper function to deal with order of arguments */
%inline %{
    void my_latsrf_c(ConstSpiceChar   *method,
                     ConstSpiceChar   *target,
                     SpiceDouble      et,
                     ConstSpiceChar   *fixref,
                     ConstSpiceDouble lonlat[1][2], SpiceInt npts,
                     SpiceDouble      **srfpts, int *sdim1, int *sdim2) {

        SpiceDouble *srfpts1 = my_malloc(npts * 3, "latsrf");
        if (!srfpts1) {
            return;
        }

        latsrf_c(method, target, et, fixref, npts, lonlat, srfpts1);

        if (failed_c()) {
            free(srfpts1);
            *srfpts = NULL;
            *sdim1 = 0;
            *sdim2 = 3;
        }
        else {
            *srfpts = srfpts1;
            *sdim1 = npts;
            *sdim2 = 3;
        }
    }
%}

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

extern void latsph_c(
        SpiceDouble radius,
        SpiceDouble lon,
        SpiceDouble lat,
        SpiceDouble *OUTPUT,
        SpiceDouble *OUTPUT,
        SpiceDouble *OUTPUT);

// Vector version
VECTORIZE_3d__3d(latsph, latsph_c)

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

extern void ldpool_c(
        ConstSpiceChar *CONST_STRING);

/***********************************************************************
* -Procedure limbpt_c ( Limb points on an extended object )
*
* -Abstract
*
*    Find limb points on a target body. The limb is the set of points
*    of tangency on the target of rays emanating from the observer.
*    The caller specifies half-planes bounded by the observer-target
*    center vector in which to search for limb points.
*
*    The surface of the target body may be represented either by a
*    triaxial ellipsoid or by topographic data.
*
*    void limbpt_c ( ConstSpiceChar    * method,
*                    ConstSpiceChar    * target,
*                    SpiceDouble         et,
*                    ConstSpiceChar    * fixref,
*                    ConstSpiceChar    * abcorr,
*                    ConstSpiceChar    * corloc,
*                    ConstSpiceChar    * obsrvr,
*                    ConstSpiceDouble    refvec[3],
*                    SpiceDouble         rolstp,
*                    SpiceInt            ncuts,
*                    SpiceDouble         schstp,
*                    SpiceDouble         soltol,
*                    SpiceInt            maxn,
*                    SpiceInt            npts  [],
*                    SpiceDouble         points[][3],
*                    SpiceDouble         epochs[],
*                    SpiceDouble         tangts[][3]  )
*
*    Variable  I/O  Description
*    --------  ---  --------------------------------------------------
*    method     I   Computation method.
*    target     I   Name of target body.
*    et         I   Epoch in ephemeris seconds past J2000 TDB.
*    fixref     I   Body-fixed, body-centered target body frame.
*    abcorr     I   Aberration correction.
*    corloc     I   Aberration correction locus.
*    obsrvr     I   Name of observing body.
*    refvec     I   Reference vector for cutting half-planes.
*    rolstp     I   Roll angular step for cutting half-planes.
*    ncuts      I   Number of cutting half-planes.
*    schstp     I   Angular step size for searching.
*    soltol     I   Solution convergence tolerance.
*    maxn       I   Maximum number of entries in output arrays.
*    npts       O   Counts of limb points corresponding to cuts.
*    points     O   Limb points.
*    epochs     O   Times associated with limb points.
*    tangts     O   Tangent vectors emanating from the observer.
***********************************************************************/

%rename (limbpt) my_limbpt_c;

%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *method};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *target};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *fixref};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *abcorr};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *corloc};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *obsrvr};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble refvec[3]};

%apply (SpiceInt **OUT_ARRAY1, SpiceInt *SIZE1)
                               {(SpiceInt **npts, SpiceInt *ndim1)};
%apply (SpiceDouble **OUT_ARRAY2, int *SIZE1, int *SIZE2)
                               {(SpiceDouble **points, int *pdim1, int *pdim2)};
%apply (SpiceDouble **OUT_ARRAY1, int *SIZE1)
                               {(SpiceDouble **epochs, int *edim1)};
%apply (SpiceDouble **OUT_ARRAY2, int *SIZE1, int *SIZE2)
                               {(SpiceDouble **tangts, int *tdim1, int *tdim2)};

%apply (void RETURN_VOID) {void my_limbpt_c};

/* Helper function to deal with order of arguments */
%inline %{  
    void my_limbpt_c(ConstSpiceChar   *method,
                     ConstSpiceChar   *target,
                     SpiceDouble      et,
                     ConstSpiceChar   *fixref,
                     ConstSpiceChar   *abcorr,
                     ConstSpiceChar   *corloc,
                     ConstSpiceChar   *obsrvr,
                     ConstSpiceDouble refvec[3],
                     SpiceDouble      rolstp,
                     SpiceInt         ncuts,
                     SpiceDouble      schstp,
                     SpiceDouble      soltol,
                     SpiceInt         maxn,
                     SpiceInt         **npts,
                     SpiceInt         *ndim1,
                     SpiceDouble **points, int *pdim1, int *pdim2,
                     SpiceDouble **epochs, int *edim1,
                     SpiceDouble **tangts, int *tdim1, int *tdim2) {

        SpiceInt    *npts1 = my_int_malloc(maxn,   "limbpt");
        SpiceDouble *points1 = my_malloc(maxn * 3, "limbpt");
        SpiceDouble *epochs1 = my_malloc(maxn,     "limbpt");
        SpiceDouble *tangts1 = my_malloc(maxn * 3, "limbpt");

        if (!tangts1) {
            free(npts1);
            free(points1);
            free(epochs1);
            free(tangts1);
            return;
        }

        limbpt_c(method, target, et, fixref, abcorr, corloc, obsrvr, refvec,
                 rolstp, ncuts, schstp, soltol, maxn,
                 npts1, points1, epochs1, tangts1);

        if (failed_c()) {
            free(npts1);
            *npts = NULL;
            *ndim1 = 0;

            free(points1);
            *points = NULL;
            *pdim1 = 0;
            *pdim2 = 3;

            free(epochs1);
            *epochs = NULL;
            *edim1 = 0;

            free(tangts1);
            *tangts = NULL;
            *tdim1 = 0;
            *tdim2 = 3;
        }
        else {
            *npts = npts1;
            *ndim1 = maxn;

            *points = points1;
            *pdim1 = maxn;
            *pdim2 = 3;

            *epochs = epochs1;
            *edim1 = maxn;

            *tangts = tangts1;
            *tdim1 = maxn;
            *tdim2 = 3;
        }
    }
%}

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

%apply (SpiceDouble RETURN_DOUBLE) {SpiceDouble lspcn_c};

extern SpiceDouble lspcn_c(
        ConstSpiceChar *CONST_STRING,
        SpiceDouble    et,
        ConstSpiceChar *CONST_STRING);

//Vector version
VECTORIZE_s_d_s__RETURN_d(lspcn, lspcn_c)

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

extern void ltime_c(
        SpiceDouble    etobs,
        SpiceInt       obs,
        ConstSpiceChar *CONST_STRING,
        SpiceInt       targ,
        SpiceDouble    *OUTPUT,
        SpiceDouble    *OUTPUT);

//Vector version
VECTORIZE_d_i_s_i__2d(ltime, ltime_c)

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

%apply (ConstSpiceDouble IN_ARRAY2[ANY][ANY]) {ConstSpiceDouble rin[3][3]};
%apply (void RETURN_VOID) {void m2eul_c};

extern void m2eul_c(
        ConstSpiceDouble rin[3][3],
        SpiceInt         axis3,
        SpiceInt         axis2,
        SpiceInt         axis1,
        SpiceDouble      *OUTPUT,
        SpiceDouble      *OUTPUT,
        SpiceDouble      *OUTPUT);

//Vector version
VECTORIZE_dXY_3i__3d(m2eul, m2eul_c)

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

%apply (ConstSpiceDouble IN_ARRAY2[ANY][ANY]) {ConstSpiceDouble rin[3][3]};
%apply (SpiceDouble OUT_ARRAY1[ANY])      {SpiceDouble qout[4]};
%apply (void RETURN_VOID) {void m2q_c};

extern void m2q_c(
        ConstSpiceDouble rin[3][3],
        SpiceDouble qout[4]);

//Vector version
VECTORIZE_dXY__dN(m2q, m2q_c, 4)

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

%apply (ConstSpiceDouble IN_ARRAY2[ANY][ANY]) {ConstSpiceDouble m1[3][3]};
%apply (SpiceDouble OUT_ARRAY2[ANY][ANY]) {SpiceDouble mout[3][3]};
%apply (void RETURN_VOID) {void mequ_c};

extern void mequ_c(
        ConstSpiceDouble m1  [3][3],
        SpiceDouble      mout[3][3]);

//Vector version
VECTORIZE_dXY__dMN(mequ, mequ_c, 3, 3)

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

%apply (ConstSpiceDouble *IN_ARRAY2, SpiceInt  DIM1, SpiceInt DIM2)
                          {(ConstSpiceDouble *m1, SpiceInt nr1, SpiceInt nc1)};
%apply (SpiceDouble **OUT_ARRAY2, int *SIZE1, int *SIZE2)
                          {(SpiceDouble **mout, int *nr_out, int *nc_out)};
%apply (void RETURN_VOID) {void my_mequg_c};

%inline %{
    void my_mequg_c(ConstSpiceDouble *m1, SpiceInt nr1, SpiceInt nc1,
                    SpiceDouble   **mout, int *nr_out, int *nc_out) {

        *mout = NULL;
        *nr_out = 0;
        *nc_out = 0;

        SpiceDouble *result = my_malloc(nr1 * nc1, "mequg");
        if (!result) return;

        mequg_c(m1, nr1, nc1, result);
        *mout = result;
        *nr_out = nr1;
        *nc_out = nc1;
    }

    void my_mequg_nomalloc(ConstSpiceDouble *m1, SpiceInt nr1, SpiceInt nc1,
                           SpiceDouble    *mout, int *nr_out, int *nc_out) {

        mequg_c(m1, nr1, nc1, mout);
        *nr_out = nr1;
        *nc_out = nc1;
    }
%}

//Vector version
VECTORIZE_dij__dij(mequg, my_mequg_nomalloc)

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

%apply (ConstSpiceDouble IN_ARRAY2[ANY][ANY]) {ConstSpiceDouble m1[3][3]};
%apply (ConstSpiceDouble IN_ARRAY2[ANY][ANY]) {ConstSpiceDouble m2[3][3]};
%apply (SpiceDouble OUT_ARRAY2[ANY][ANY]) {SpiceDouble mout[3][3]};
%apply (void RETURN_VOID) {void mtxm_c};

extern void mtxm_c(
        ConstSpiceDouble m1  [3][3],
        ConstSpiceDouble m2  [3][3],
        SpiceDouble      mout[3][3]);

//Vector version
VECTORIZE_dXY_dXY__dMN(mtxm, mtxm_c, 3, 3)

/***********************************************************************
* -Procedure mtxmg_c ( Matrix transpose times matrix, general dimension )
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

%apply (ConstSpiceDouble *IN_ARRAY2, SpiceInt  DIM1, SpiceInt  DIM2)
                        {(ConstSpiceDouble *m1, SpiceInt nr1, SpiceInt nc1)};
%apply (ConstSpiceDouble *IN_ARRAY2, SpiceInt  DIM1, SpiceInt  DIM2)
                        {(ConstSpiceDouble *m2, SpiceInt nr2, SpiceInt nc2)};
%apply (SpiceDouble **OUT_ARRAY2, int *SIZE1, int *SIZE2)
                        {(SpiceDouble **m3, int *nr3, int *nc3)};
%apply (void RETURN_VOID) {void my_mtxmg_c};

%inline %{
    void my_mtxmg_c(ConstSpiceDouble *m1, SpiceInt nr1, SpiceInt nc1,
                    ConstSpiceDouble *m2, SpiceInt nr2, SpiceInt nc2,
                    SpiceDouble     **m3, int     *nr3, int     *nc3) {

        *m3 = NULL;
        *nr3 = 0;
        *nc3 = 0;

        if (!my_assert_eq(nr1, nr2, "mtmxg",
            "Array dimension mismatch in mtmxg: "
            "matrix 1 rows = #; matrix 2 rows = #")) return;

        SpiceDouble *result = my_malloc(nc1 * nc2, "mtmxg");
        if (!result) return;

        mtxmg_c(m1, m2, nc1, nr1, nc2, result);
        *m3 = result;
        *nr3 = nc1;
        *nc3 = nc2;
    }

    void my_mtxmg_nomalloc(ConstSpiceDouble *m1, SpiceInt nr1, SpiceInt nc1,
                           ConstSpiceDouble *m2, SpiceInt nr2, SpiceInt nc2,
                           SpiceDouble      *m3, int     *nr3, int     *nc3) {

        if (!my_assert_eq(nr1, nr2, "mtmxg",
            "Array dimension mismatch in mtmxg: "
            "matrix 1 rows = #; matrix 2 rows = #")) return;

        mtxmg_c(m1, m2, nc1, nr1, nc2, m3);
        *nr3 = nc1;
        *nc3 = nc2;
    }
%}

//Vector version
VECTORIZE_dji_djk__dik(mtxmg, my_mtxmg_nomalloc)

/***********************************************************************
* -Procedure mtxv_c ( Matrix transpose times vector, 3x3 )
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

%apply (ConstSpiceDouble  IN_ARRAY2[ANY][ANY]) {ConstSpiceDouble m1[3][3]};
%apply (ConstSpiceDouble       IN_ARRAY1[ANY]) {ConstSpiceDouble   vin[3]};
%apply (SpiceDouble           OUT_ARRAY1[ANY]) {SpiceDouble       vout[3]};
%apply (void RETURN_VOID) {void mtxv_c};

extern void mtxv_c(
        ConstSpiceDouble m1[3][3],
        ConstSpiceDouble   vin[3],
        SpiceDouble       vout[3]);

//Vector version
VECTORIZE_dXY_dX__dN(mtxv, mtxv_c, 3)

/***********************************************************************
* -Procedure mtxvg_c ( Matrix transpose times vector, general dimension )
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

%apply (ConstSpiceDouble *IN_ARRAY2, SpiceInt DIM1, SpiceInt DIM2)
                          {(ConstSpiceDouble *m1, SpiceInt nr1, SpiceInt nc1)};
%apply (ConstSpiceDouble *IN_ARRAY1, SpiceInt DIM1)
                          {(ConstSpiceDouble *v2, SpiceInt nr2)};
%apply (SpiceDouble **OUT_ARRAY1, int *SIZE1)
                          {(SpiceDouble **v3, int *nr3)};
%apply (void RETURN_VOID) {void my_mtxvg_c};

%inline %{
    void my_mtxvg_c(ConstSpiceDouble  *m1, SpiceInt nr1, SpiceInt nc1,
                    ConstSpiceDouble  *v2, SpiceInt nr2,
                    SpiceDouble      **v3, int      *nr3) {

        *v3 = NULL;
        *nr3 = 0;

        if (!my_assert_eq(nr1, nr2, "mtxvg",
            "Array dimension mismatch in mtxvg: "
            "matrix rows = #; vector dimension = #")) return;

        SpiceDouble *result = my_malloc(nc1, "mtxvg");
        if (!result) return;

        mtxvg_c(m1, v2, nc1, nr1, result);
        *v3 = result;
        *nr3 = nc1;
    }

    void my_mtxvg_nomalloc(ConstSpiceDouble *m1, SpiceInt nr1, SpiceInt nc1,
                           ConstSpiceDouble *v2, SpiceInt nr2,
                           SpiceDouble      *v3, int      *nr3) {

        if (!my_assert_eq(nr1, nr2, "mtxvg",
            "Array dimension mismatch in mtxvg: "
            "matrix rows = #; vector dimension = #")) return;

        mtxvg_c(m1, v2, nc1, nr1, v3);
        *nr3 = nc1;
    }
%}

//Vector version
VECTORIZE_dji_dj__di(mtxvg, my_mtxvg_nomalloc)

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

%apply (ConstSpiceDouble IN_ARRAY2[ANY][ANY]) {ConstSpiceDouble m1[3][3]};
%apply (ConstSpiceDouble IN_ARRAY2[ANY][ANY]) {ConstSpiceDouble m2[3][3]};
%apply (SpiceDouble     OUT_ARRAY2[ANY][ANY]) {SpiceDouble    mout[3][3]};
%apply (void RETURN_VOID) {void mxm_c};

extern void mxm_c(
        ConstSpiceDouble m1  [3][3],
        ConstSpiceDouble m2  [3][3],
        SpiceDouble      mout[3][3]);

//Vector version
VECTORIZE_dXY_dXY__dMN(mxm, mxm_c, 3, 3)

/***********************************************************************
* -Procedure mxmg_c ( Matrix times matrix, general dimension )
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

%apply (ConstSpiceDouble *IN_ARRAY2, SpiceInt  DIM1, SpiceInt  DIM2)
                          {(ConstSpiceDouble *m1, SpiceInt nr1, SpiceInt nc1)};
%apply (ConstSpiceDouble *IN_ARRAY2, SpiceInt  DIM1, SpiceInt  DIM2)
                          {(ConstSpiceDouble *m2, SpiceInt nr2, SpiceInt nc2)};
%apply (SpiceDouble **OUT_ARRAY2, int *SIZE1, int *SIZE2)
                          {(SpiceDouble **m3, int *nr3, int *nc3)};
%apply (void RETURN_VOID) {void my_mxmg_c};

%inline %{
    void my_mxmg_c(ConstSpiceDouble  *m1, SpiceInt  nr1, SpiceInt  nc1,
                   ConstSpiceDouble  *m2, SpiceInt  nr2, SpiceInt  nc2,
                   SpiceDouble      **m3, int *nr3, int *nc3) {

        *m3 = NULL;
        *nr3 = 0;
        *nc3 = 0;

        if (!my_assert_eq(nc1, nr2, "mxmg",
            "Array dimension mismatch in mxmg: "
            "matrix 1 columns = #; matrix 2 rows = #")) return;

        SpiceDouble *result = my_malloc(nr1 * nc2, "mxmg");
        if (!result) return;

        mxmg_c(m1, m2, nr1, nc1, nc2, result);
        *m3 = result;
        *nr3 = nr1;
        *nc3 = nc2;
    }

    void my_mxmg_nomalloc(ConstSpiceDouble *m1, SpiceInt  nr1, SpiceInt  nc1,
                          ConstSpiceDouble *m2, SpiceInt  nr2, SpiceInt  nc2,
                          SpiceDouble      *m3, int      *nr3, int      *nc3) {

        if (!my_assert_eq(nc1, nr2, "mxmg",
            "Array dimension mismatch in mxmg: "
            "matrix 1 columns = #; matrix 2 rows = #")) return;

        mxmg_c(m1, m2, nr1, nc1, nc2, m3);
        *nr3 = nr1;
        *nc3 = nc2;
    }
%}

//Vector version
VECTORIZE_dij_djk__dik(mxmg, my_mxmg_nomalloc)

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

%apply (ConstSpiceDouble IN_ARRAY2[ANY][ANY]) {ConstSpiceDouble m1[3][3]};
%apply (ConstSpiceDouble IN_ARRAY2[ANY][ANY]) {ConstSpiceDouble m2[3][3]};
%apply (SpiceDouble     OUT_ARRAY2[ANY][ANY]) {SpiceDouble    mout[3][3]};
%apply (void RETURN_VOID) {void mxmt_c};

extern void mxmt_c(
        ConstSpiceDouble m1  [3][3],
        ConstSpiceDouble m2  [3][3],
        SpiceDouble      mout[3][3]);

//Vector version
VECTORIZE_dXY_dXY__dMN(mxmt, mxmt_c, 3, 3)

/***********************************************************************
* -Procedure mxmtg_c ( Matrix times matrix transpose, general dimension )
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

%apply (ConstSpiceDouble *IN_ARRAY2, SpiceInt  DIM1, SpiceInt  DIM2)
                        {(ConstSpiceDouble *m1, SpiceInt nr1, SpiceInt nc1)};
%apply (ConstSpiceDouble *IN_ARRAY2, SpiceInt  DIM1, SpiceInt  DIM2)
                        {(ConstSpiceDouble *m2, SpiceInt nr2, SpiceInt nc2)};
%apply (SpiceDouble **OUT_ARRAY2, int *SIZE1, int *SIZE2)
                        {(SpiceDouble **m3, int *nr3, int *nc3)};
%apply (void RETURN_VOID) {void my_mxmtg_c};

%inline %{
    void my_mxmtg_c(ConstSpiceDouble  *m1, SpiceInt  nr1, SpiceInt  nc1,
                    ConstSpiceDouble  *m2, SpiceInt  nr2, SpiceInt  nc2,
                    SpiceDouble      **m3, int      *nr3, int      *nc3) {

        *m3 = NULL;
        *nr3 = 0;
        *nc3 = 0;

        if (!my_assert_eq(nc1, nc2, "mxmtg",
            "Array dimension mismatch in mxmtg: "
            "matrix 1 columns = #; matrix 2 columns = #")) return;

        SpiceDouble *result = my_malloc(nr1 * nr2, "mxmtg");
        if (!result) return;

        mxmtg_c(m1, m2, nr1, nc1, nr2, result);
        *m3 = result;
        *nr3 = nr1;
        *nc3 = nr2;
    }

    void my_mxmtg_nomalloc(ConstSpiceDouble *m1, SpiceInt  nr1, SpiceInt  nc1,
                           ConstSpiceDouble *m2, SpiceInt  nr2, SpiceInt  nc2,
                           SpiceDouble      *m3, int      *nr3, int      *nc3) {

        if (!my_assert_eq(nc1, nc2, "mxmtg",
            "Array dimension mismatch in mxmtg: "
            "matrix 1 columns = #; matrix 2 columns = #")) return;

        mxmtg_c(m1, m2, nr1, nc1, nr2, m3);
        *nr3 = nr1;
        *nc3 = nr2;
    }
%}

//Vector version
VECTORIZE_dij_dkj__dik(mxmtg, my_mxmtg_nomalloc)

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

%apply (ConstSpiceDouble IN_ARRAY2[ANY][ANY]) {ConstSpiceDouble m1[3][3]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY])      {ConstSpiceDouble vin[3]};
%apply (SpiceDouble     OUT_ARRAY1[ANY])      {SpiceDouble     vout[3]};
%apply (void RETURN_VOID) {void mxv_c};

extern void mxv_c(
        ConstSpiceDouble m1  [3][3],
        ConstSpiceDouble vin [3],
        SpiceDouble      vout[3]);

//Vector version
VECTORIZE_dXY_dX__dN(mxv, mxv_c, 3)

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

%apply (ConstSpiceDouble *IN_ARRAY2, SpiceInt DIM1, SpiceInt DIM2)
                          {(ConstSpiceDouble *m1, SpiceInt nr1, SpiceInt nc1)};
%apply (ConstSpiceDouble *IN_ARRAY1, SpiceInt DIM1)
                          {(ConstSpiceDouble *v2, SpiceInt nr2)};
%apply (SpiceDouble **OUT_ARRAY1, int *SIZE1)
                          {(SpiceDouble **v3, int *nr3)};
%apply (void RETURN_VOID) {void my_mxvg_c};

%inline %{
    void my_mxvg_c(ConstSpiceDouble  *m1, SpiceInt nr1, SpiceInt nc1,
                   ConstSpiceDouble  *v2, SpiceInt nr2,
                   SpiceDouble      **v3, int     *nr3) {

        *v3 = NULL;
        *nr3 = 0;

        if (!my_assert_eq(nc1, nr2, "mxvg",
            "Array dimension mismatch in mxvg: "
            "matrix columns = #; vector length = #")) return;

        SpiceDouble *result = my_malloc(nr1, "mxvg");
        if (!result) return;

        mxvg_c(m1, v2, nr1, nc1, result);
        *v3 = result;
        *nr3 = nr1;
    }

    void my_mxvg_nomalloc(ConstSpiceDouble *m1, SpiceInt nr1, SpiceInt nc1,
                          ConstSpiceDouble *v2, SpiceInt nr2,
                          SpiceDouble      *v3, int     *nr3) {

        if (!my_assert_eq(nc1, nr2, "mxvg",
            "Array dimension mismatch in mxvg: "
            "matrix columns = #; vector dimension = #")) return;

        mxvg_c(m1, v2, nr1, nc1, v3);
        *nr3 = nr1;
    }
%}

//Vector version
VECTORIZE_dij_dj__di(mxvg, my_mxvg_nomalloc)

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

extern void namfrm_c(
        ConstSpiceChar *CONST_STRING,
        SpiceInt       *OUTPUT);

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble positn[3]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble      npoint[3]};
%apply (void RETURN_VOID) {void nearpt_c};

extern void nearpt_c(
        ConstSpiceDouble positn[3],
        SpiceDouble      a,
        SpiceDouble      b,
        SpiceDouble      c,
        SpiceDouble      npoint[3],
        SpiceDouble      *OUTPUT);

//Vector version
VECTORIZE_dX_3d__dN_d(nearpt, nearpt_c, 3)

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble linept[3]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble linedr[3]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble       pnear[3]};
%apply (void RETURN_VOID) {void npedln_c};

extern void npedln_c(
        SpiceDouble      a,
        SpiceDouble      b,
        SpiceDouble      c,
        ConstSpiceDouble linept[3],
        ConstSpiceDouble linedr[3],
        SpiceDouble      pnear[3],
        SpiceDouble      *OUTPUT);

//Vector version
VECTORIZE_3d_dX_dX__dN_d(npedln, npedln_c, 3)

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble point[3]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble ellipse[NELLIPSE]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble      pnear[3]};
%apply (void RETURN_VOID) {void npelpt_c};

extern void npelpt_c(
        ConstSpiceDouble point[3],
        ConstSpiceDouble ellipse[NELLIPSE],
        SpiceDouble      pnear[3],
        SpiceDouble      *OUTPUT);

//Vector version
VECTORIZE_dX_dX__dN_d(npelpt, npelpt_c, 3)

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble linpt [3]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble lindir[3]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble point [3]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble      pnear [3]};
%apply (void RETURN_VOID) {void nplnpt_c};

extern void nplnpt_c(
        ConstSpiceDouble linpt [3],
        ConstSpiceDouble lindir[3],
        ConstSpiceDouble point [3],
        SpiceDouble      pnear [3],
        SpiceDouble      *OUTPUT);

//Vector version
VECTORIZE_dX_dX_dX__dN_d(nplnpt, nplnpt_c, 3)

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble normal[3]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble      plane[NPLANE]};
%apply (void RETURN_VOID) {void nvc2pl_c};

extern void nvc2pl_c(
        ConstSpiceDouble normal[3],
        SpiceDouble      constant,
        SpiceDouble      plane[NPLANE]);

//Vector version
VECTORIZE_dX_d__dN(nvc2pl, nvc2pl_c, NPLANE)

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble normal[3]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble point[3]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble      plane[NPLANE]};
%apply (void RETURN_VOID) {void nvp2pl_c};

extern void nvp2pl_c(
        ConstSpiceDouble normal[3],
        ConstSpiceDouble point[3],
        SpiceDouble      plane[NPLANE]);

//Vector version
VECTORIZE_dX_dX__dN(nvp2pl, nvp2pl_c, NPLANE)

/***********************************************************************
-Procedure occult_c ( find occultation type at time )

-Abstract

   Determines the occultation condition (not occulted, partially,
   etc.) of one target relative to another target as seen by
   an observer at a given time.

   The surfaces of the target bodies may be represented by triaxial
   ellipsoids or by topographic data provided by DSK files.

   void occult_c ( ConstSpiceChar   * targ1,
                   ConstSpiceChar   * shape1,
                   ConstSpiceChar   * frame1,
                   ConstSpiceChar   * targ2,
                   ConstSpiceChar   * shape2,
                   ConstSpiceChar   * frame2,
                   ConstSpiceChar   * abcorr,
                   ConstSpiceChar   * obsrvr,
                   SpiceDouble        et,
                   SpiceInt         * ocltid )

-Brief_I/O

   VARIABLE    I/O  DESCRIPTION
   --------    ---  -------------------------------------------
   targ1        I   Name or ID of first target.
   shape1       I   Type of shape model used for first target.
   frame1       I   Body-fixed, body-centered frame for first body.
   targ2        I   Name or ID of second target.
   shape2       I   Type of shape model used for second target.
   frame2       I   Body-fixed, body-centered frame for second body.
   abcorr       I   Aberration correction flag.
   obsrvr       I   Name or ID of the observer.
   et           I   Time of the observation (seconds past J2000).
   ocltid       O   Occultation identification code.
***********************************************************************/

%rename (occult) occult_c;

extern void occult_c(
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceDouble    et,
        SpiceInt       *OUTPUT);

//Vector version
VECTORIZE_8s_d__i(occult, occult_c)

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble state[6]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble      elts[8]};
%apply (void RETURN_VOID) {void oscelt_c};

extern void oscelt_c(
        ConstSpiceDouble state[6],
        SpiceDouble      et,
        SpiceDouble      mu,
        SpiceDouble      elts[8]);

//Vector version
VECTORIZE_dX_2d__dN(oscelt, oscelt_c, 8)

/***********************************************************************
* -Procedure oscltx_c ( Extended osculating elements from state )
*
* -Abstract
*
*    Determine the set of osculating conic orbital elements that
*    corresponds to the state (position, velocity) of a body at some
*    epoch. In additional to the classical elements, return the true
*    anomaly, semi-major axis, and period, if applicable.
*
*    void oscltx_c ( ConstSpiceDouble state [6],
*                    SpiceDouble      et,
*                    SpiceDouble      mu,
*                    SpiceDouble      elts  [SPICE_OSCLTX_NELTS] )
*
* -Brief_I/O
*
*    VARIABLE  I/O  DESCRIPTION
*    --------  ---  --------------------------------------------------
*    state      I   State of body at epoch of elements.
*    et         I   Epoch of elements.
*    mu         I   Gravitational parameter (GM) of primary body.
*    elts       O   Extended set of classical conic elements.
***********************************************************************/

%rename (oscltx) oscltx_c;

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble state[6]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble elts[SPICE_OSCLTX_NELTS]};
%apply (void RETURN_VOID) {void oscltx_c};

extern void oscltx_c(
        ConstSpiceDouble state[6],
        SpiceDouble      et,
        SpiceDouble      mu,
        SpiceDouble      elts[SPICE_OSCLTX_NELTS]);

//Vector version
VECTORIZE_dX_2d__dN(oscltx, oscltx_c, SPICE_OSCLTX_NELTS)

/***********************************************************************
* -Procedure pckcov_c ( PCK coverage )
*
* -Abstract
*
*    Find the coverage window for a specified reference frame in a
*    specified binary PCK file.
*
*    void pckcov_c ( ConstSpiceChar   * pck,
*                    SpiceInt           idcode,
*                    SpiceCell        * cover   )
*
* -Brief_I/O
*
*    Variable  I/O  Description
*    --------  ---  --------------------------------------------------
*    pck        I   Name of PCK file.
*    idcode     I   Class ID code of PCK reference frame.
*    cover     I/O  Window giving coverage in `pck' for `idcode'.
*
***********************************************************************/

%rename (pckcov) my_pckcov_c;

%apply (ConstSpiceChar *CONST_STRING)
                          {ConstSpiceChar *pck};
%apply (SpiceDouble OUT_ARRAY2[ANY][ANY], int *SIZE1)
                          {(SpiceDouble array[500][2], int *intervals)};
%apply (void RETURN_VOID) {void my_pckcov_c};

%inline %{
    /* Helper function to create a 2-D array of results */
    void my_pckcov_c(ConstSpiceChar *pck,
                     SpiceInt idcode,
                     SpiceDouble array[500][2], int *intervals) {

        int j;
        SPICEDOUBLE_CELL(coverage, 2 * 500);

        scard_c(0, &coverage);
        pckcov_c(pck, idcode, &coverage);

        *intervals = (int) card_c(&coverage) / 2;
        for (j = 0; j < *intervals; j++) {
            wnfetd_c(&coverage, j, &(array[j][0]), &(array[j][1]));
        }
    }
%}

/***********************************************************************
*
*-Procedure pckfrm_c ( PCK reference frame class ID set )
*
*-Abstract
* 
*   Find the set of reference frame class ID codes of all frames  
*   in a specified binary PCK file. 
* 
*   void pckfrm_c ( ConstSpiceChar  * pck,
*                   SpiceCell       * ids  ) 
*
*-Brief_I/O
* 
*   Variable  I/O  Description 
*   --------  ---  -------------------------------------------------- 
*   pck        I   Name of PCK file. 
*   ids       I/O  Set of frame class ID codes of frames in PCK file. 
* 
***********************************************************************/

%rename (pckfrm) my_pckfrm_c;

%apply (ConstSpiceChar *CONST_STRING)    {ConstSpiceChar *pck};
%apply (int OUT_ARRAY1[ANY], int *SIZE1) {(int frame_ids[200], int *frames)};
%apply (void RETURN_VOID) {void my_pckfrm_c};

/* Helper function to create a 1-D array of results */
%inline %{
    void my_pckfrm_c(ConstSpiceChar *pck,
                     int frame_ids[200], int *frames) {

        int j;
        SPICEINT_CELL(ids, 200);

        scard_c(0, &ids);
        pckfrm_c(pck, &ids);

        *frames = card_c(&ids);
        for (j = 0; j < *frames; j++) {
            frame_ids[j] = SPICE_CELL_ELEM_I(&ids, j);
        }
    }
%}

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

%apply (SpiceInt DIM1, SpiceInt DIM2, SpiceChar *IN_STRINGS)
                      {(SpiceInt n, SpiceInt lenvals, SpiceChar *cvals)};
%apply (void RETURN_VOID) {void pcpool_c};

extern void pcpool_c(
        ConstSpiceChar *CONST_STRING,
        SpiceInt n, SpiceInt lenvals, SpiceChar *cvals);

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

%apply (SpiceInt DIM1, ConstSpiceDouble *IN_ARRAY1)
                          {(SpiceInt n, ConstSpiceDouble *dvals)};
%apply (void RETURN_VOID) {void pdpool_c};

extern void pdpool_c(
        ConstSpiceChar *CONST_STRING,
        SpiceInt n, ConstSpiceDouble *dvals);

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

%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble rectan[3]};
%apply (void RETURN_VOID) {void pgrrec_c};

extern void pgrrec_c(
        ConstSpiceChar *CONST_STRING,
        SpiceDouble    lon,
        SpiceDouble    lat,
        SpiceDouble    alt,
        SpiceDouble    re,
        SpiceDouble    f,
        SpiceDouble    rectan[3]);

//Vector version
VECTORIZE_s_5d__dN(pgrrec, pgrrec_c, 3)

/***********************************************************************
* -Procedure phaseq_c ( Phase angle quantity between bodies centers )
*
* -Abstract
*
*    Compute the apparent phase angle for a target, observer,
*    illuminator set of ephemeris objects.
*
*    SpiceDouble phaseq_c ( SpiceDouble       et,
*                           ConstSpiceChar  * target,
*                           ConstSpiceChar  * illmn,
*                           ConstSpiceChar  * obsrvr,
*                           ConstSpiceChar  * abcorr )
*
* -Brief_I/O
*
*    VARIABLE  I/O  DESCRIPTION
*    --------  ---  --------------------------------------------------
*    et         I   Ephemeris seconds past J2000 TDB.
*    target     I   Target body name.
*    illmn      I   Illuminating body name.
*    obsrvr     I   Observer body.
*    abcorr     I   Aberration correction flag.
*    retval     O   Value of phase angle.
***********************************************************************/

%rename (phaseq) phaseq_c;

%apply (SpiceDouble RETURN_DOUBLE) {SpiceDouble phaseq_c};

extern SpiceDouble phaseq_c(
        SpiceDouble    et,
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING);

//Vector version
VECTORIZE_d_4s__RETURN_d(phaseq, phaseq_c)

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

%apply (SpiceDouble RETURN_DOUBLE) {SpiceDouble pi_c};

extern SpiceDouble pi_c(void);

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

%apply (SpiceInt DIM1, ConstSpiceInt *IN_ARRAY1)
                          {(SpiceInt n, ConstSpiceInt *ivals)};
%apply (void RETURN_VOID) {void pipool_c};

extern void pipool_c(
        ConstSpiceChar *CONST_STRING,
        SpiceInt n, ConstSpiceInt *ivals);

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble elin [NELLIPSE]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble plane[NPLANE]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble      elout[NELLIPSE]};
%apply (void RETURN_VOID) {void pjelpl_c};

extern void pjelpl_c(
        ConstSpiceDouble elin [NELLIPSE],
        ConstSpiceDouble plane[NPLANE],
        SpiceDouble      elout[NELLIPSE]);

//Vector version
VECTORIZE_dX_dX__dN(pjelpl, pjelpl_c, NELLIPSE)

/***********************************************************************
* -Procedure pltar_c ( Compute area of plate set )
*
* -Abstract
*
*    Compute the total area of a collection of triangular plates.
*
*    SpiceDouble pltar_c ( SpiceInt           nv,
*                          ConstSpiceDouble   vrtces [][3],
*                          SpiceInt           np,
*                          ConstSpiceInt      plates [][3]  )
*
* -Brief_I/O
*
*    Variable  I/O  Description
*    --------  ---  --------------------------------------------------
*    nv         I   Number of vertices.
*    vrtces     I   Array of vertices.
*    np         I   Number of triangular plates.
*    plates     I   Array of plates.
***********************************************************************/

%rename (pltar) pltar_c;

%apply (SpiceInt DIM1, ConstSpiceDouble IN_ARRAY2[ANY][ANY])
                                {(SpiceInt nv, ConstSpiceDouble vrtces[1][3])};
%apply (SpiceInt DIM1, ConstSpiceInt IN_ARRAY2[ANY][ANY])
                                {(SpiceInt np, ConstSpiceInt plates[1][3])};
%apply (SpiceDouble RETURN_DOUBLE) {SpiceDouble pltar_c};

extern SpiceDouble pltar_c(
        SpiceInt nv, ConstSpiceDouble vrtces[1][3],
        SpiceInt np, ConstSpiceInt    plates[1][3]);

/***********************************************************************
* -Procedure pltexp_c ( Plate expander )
*
* -Abstract
*
*    Expand a triangular plate by a specified amount. The expanded
*    plate is co-planar with, and has the same orientation as, the
*    original. The centroids of the two plates coincide.
*
*    void pltexp_c ( ConstSpiceDouble   iverts[3][3],
*                    SpiceDouble        delta,
*                    SpiceDouble        overts[3][3] )
*
* -Brief_I/O
*
*    Variable  I/O  Description
*    --------  ---  --------------------------------------------------
*    iverts     I   Vertices of the plate to be expanded.
*    delta      I   Fraction by which the plate is to be expanded.
*    overts     O   Vertices of the expanded plate.
***********************************************************************/

%rename (pltexp) pltexp_c;

%apply (ConstSpiceDouble IN_ARRAY2[ANY][ANY]) {ConstSpiceDouble iverts[3][3]};
%apply (SpiceDouble     OUT_ARRAY2[ANY][ANY]) {SpiceDouble      overts[3][3]};
%apply (void RETURN_VOID) {void pltexp_c};

extern void pltexp_c(
        ConstSpiceDouble iverts[3][3],
        SpiceDouble      delta,
        SpiceDouble      overts[3][3]);

//Vector version
VECTORIZE_dXY_d__dMN(pltexp, pltexp_c, 3, 3)

/***********************************************************************
* -Procedure pltnp_c ( Nearest point on triangular plate )
*
* -Abstract
*
*    Find the nearest point on a triangular plate to a given point.
*
*    void pltnp_c ( ConstSpiceDouble    point[3],
*                   ConstSpiceDouble    v1   [3],
*                   ConstSpiceDouble    v2   [3],
*                   ConstSpiceDouble    v3   [3],
*                   SpiceDouble         pnear[3],
*                   SpiceDouble       * dist      )
*
*
* -Brief_I/O
*
*    Variable  I/O  Description
*    --------  ---  --------------------------------------------------
*    point      I   A point in 3-dimensional space.
*    v1,
*    v2,
*    v3         I   Vertices of a triangular plate.
*    pnear      O   Nearest point on the plate to `point'.
*    dist       O   Distance between `pnear' and `point'.
***********************************************************************/

%rename (pltnp) pltnp_c;

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble point[3]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble v1[3]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble v2[3]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble v3[3]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble      pnear[3]};
%apply (void RETURN_VOID) {void pltnp_c};

extern void pltnp_c(
        ConstSpiceDouble point[3],
        ConstSpiceDouble v1[3],
        ConstSpiceDouble v2[3],
        ConstSpiceDouble v3[3],
        SpiceDouble      pnear[3],
        SpiceDouble      *OUTPUT);

//Vector version
VECTORIZE_dX_dX_dX_dX__dN_d(pltnp, pltnp_c, 3)

/***********************************************************************
* -Procedure pltvol_c ( Compute volume of plate model )
*
* -Abstract
*
*    Compute the volume of a three-dimensional region bounded by a
*    collection of triangular plates.
*
*    SpiceDouble pltvol_c ( SpiceInt           nv,
*                           ConstSpiceDouble   vrtces[][3],
*                           SpiceInt           np,
*                           ConstSpiceInt      plates[][3] )
*
* -Brief_I/O
*
*    Variable  I/O  Description
*    --------  ---  --------------------------------------------------
*    nv         I   Number of vertices.
*    vrtces     I   Array of vertices.
*    np         I   Number of triangular plates.
*    plates     I   Array of plates.
*
*    The function returns the volume of the spatial region bounded
*    by the plates.
*
***********************************************************************/

%rename (pltvol) pltvol_c;

%apply (SpiceInt DIM1, ConstSpiceDouble IN_ARRAY2[ANY][ANY])
                                {(SpiceInt nv, ConstSpiceDouble vrtces[1][3])};
%apply (SpiceInt DIM1, ConstSpiceInt IN_ARRAY2[ANY][ANY])
                                {(SpiceInt np, ConstSpiceInt    plates[1][3])};
%apply (SpiceDouble RETURN_DOUBLE) {SpiceDouble pltvol_c};

extern SpiceDouble pltvol_c(
        SpiceInt nv, ConstSpiceDouble vrtces[1][3],
        SpiceInt np, ConstSpiceInt    plates[1][3]);

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble plane[NPLANE]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble      normal[3]};
%apply (void RETURN_VOID) {void pl2nvc_c};

extern void pl2nvc_c(
        ConstSpiceDouble plane[NPLANE],
        SpiceDouble      normal[3],
        SpiceDouble      *OUTPUT);

//Vector version
VECTORIZE_dX__dN_d(pl2nvc, pl2nvc_c, 3)

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble plane[NPLANE]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble      normal[3]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble      point [3]};
%apply (void RETURN_VOID) {void pl2nvp_c};

extern void pl2nvp_c(
        ConstSpiceDouble plane[NPLANE],
        SpiceDouble      normal[3],
        SpiceDouble      point [3]);

//Vector version
VECTORIZE_dX__dM_dN(pl2nvp, pl2nvp_c, 3, 3)

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble plane[NPLANE]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble      point[3]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble      span1[3]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble      span2[3]};
%apply (void RETURN_VOID) {void pl2psv_c};

extern void pl2psv_c(
        ConstSpiceDouble plane[NPLANE],
        SpiceDouble      point[3],
        SpiceDouble      span1[3],
        SpiceDouble      span2[3]);

//Vector version
VECTORIZE_dX__dL_dM_dN(pl2psv, pl2psv_c, 3, 3, 3)

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble pvinit[6]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble      pvprop[6]};
%apply (void RETURN_VOID) {void prop2b_c};

extern void prop2b_c(
        SpiceDouble      gm,
        ConstSpiceDouble pvinit[6],
        SpiceDouble      dt,
        SpiceDouble      pvprop[6]);

//Vector version
VECTORIZE_d_dX_d__dN(prop2b, prop2b_c, 6)

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble point[3]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble span1[3]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble span2[3]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble      plane[NPLANE]};
%apply (void RETURN_VOID) {void psv2pl_c};

extern void psv2pl_c(
        ConstSpiceDouble point[3],
        ConstSpiceDouble span1[3],
        ConstSpiceDouble span2[3],
        SpiceDouble      plane[NPLANE]);

//Vector version
VECTORIZE_dX_dX_dX__dN(psv2pl, psv2pl_c, NPLANE)

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

%apply (SpiceDouble OUT_ARRAY2[ANY][ANY]) {SpiceDouble rotate[3][3]};
%apply (void RETURN_VOID) {void pxform_c};

extern void pxform_c(
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceDouble    et,
        SpiceDouble    rotate[3][3]);

//Vector version
VECTORIZE_2s_d__dMN(pxform, pxform_c, 3, 3)

/***********************************************************************
* -Procedure pxfrm2_c ( Position Transform Matrix, Different Epochs )
*
* -Abstract
*
*    Return the 3x3 matrix that transforms position vectors from one
*    specified frame at a specified epoch to another specified
*    frame at another specified epoch.
*
*    void pxfrm2_c ( ConstSpiceChar   * from,
*                    ConstSpiceChar   * to,
*                    SpiceDouble        etfrom,
*                    SpiceDouble        etto,
*                    SpiceDouble        rotate[3][3]     )
*
*
* -Brief_I/O
*
*    VARIABLE  I/O  DESCRIPTION
*    --------  ---  --------------------------------------------------
*    from       I   Name of the frame to transform from.
*    to         I   Name of the frame to transform to.
*    etfrom     I   Evaluation time of `from' frame.
*    etto       I   Evaluation time of `to' frame.
*    rotate     O   A position transformation matrix from
*                   frame `from' to frame `to'.
***********************************************************************/

%rename (pxfrm2) pxfrm2_c;

%apply (SpiceDouble OUT_ARRAY2[ANY][ANY]) {SpiceDouble rotate[3][3]};
%apply (void RETURN_VOID) {void pxform_c};

extern void pxfrm2_c(
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceDouble    etfrom,
        SpiceDouble    et2,
        SpiceDouble    rotate[3][3]);

//Vector version
VECTORIZE_2s_2d__dMN(pxfrm2, pxfrm2_c, 3, 3)

/***********************************************************************
* -Procedure q2m_c ( Quaternion to matrix )
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

%apply (ConstSpiceDouble  IN_ARRAY1[ANY]) {ConstSpiceDouble qin[4]};
%apply (SpiceDouble OUT_ARRAY2[ANY][ANY]) {SpiceDouble      rout[3][3]};
%apply (void RETURN_VOID) {void q2m_c};

extern void q2m_c(
        ConstSpiceDouble qin[4],
        SpiceDouble      rout[3][3]);

//Vector version
VECTORIZE_dX__dMN(q2m, q2m_c, 3, 3)

/***********************************************************************
* -Procedure qcktrc_c ( Get Quick Traceback )
* 
* -Abstract
*  
*    Return a string containing a traceback. 
*  
*    void qcktrc_c ( SpiceInt     tracelen,
*                    SpiceChar  * trace    )
* 
* -Brief_I/O
*  
*    VARIABLE  I/O  DESCRIPTION 
*    --------  ---  -------------------------------------------------- 
*    tracelen   I   Maximum length of output traceback string.
*    trace      O   A traceback string. 
*    SPICE_ERROR_MAXMOD   
*               P   Maximum traceback module count.
*    SPICE_ERROR_MODLEN 
*               P   Maximum module name length. 
*    SPICE_ERROR_TRCLEN
*               P   Maximum length of output traceback string.
***********************************************************************/

%rename (qcktrc) qcktrc_c;

%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
                          {(SpiceInt tracelen, SpiceChar trace[1000])};
%apply (void RETURN_VOID) {void qcktrc_c};

extern void qcktrc_c(
        SpiceInt tracelen, SpiceChar trace[1000]);

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble qin[4]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble dq[4]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble      av[3]};
%apply (void RETURN_VOID) {void qdq2av_c};

extern void qdq2av_c(
        ConstSpiceDouble qin[4],
        ConstSpiceDouble dq[4],
        SpiceDouble      av[3]);

//Vector version
VECTORIZE_dX_dX__dN(qdq2av, qdq2av_c, 3)

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble q1  [4]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble q2  [4]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble      qout[4]};
%apply (void RETURN_VOID) {void qxq_c};

extern void qxq_c(
        ConstSpiceDouble q1  [4],
        ConstSpiceDouble q2  [4],
        SpiceDouble      qout[4]);

//Vector version
VECTORIZE_dX_dX__dN(qxq, qxq_c, 4)

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

%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble rectan[3]};
%apply (void RETURN_VOID) {void radrec_c};

extern void radrec_c(
        SpiceDouble range,
        SpiceDouble ra,
        SpiceDouble dec,
        SpiceDouble rectan[3]);

// Vector version
VECTORIZE_3d__dN(radrec, radrec_c, 3)

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

%apply (ConstSpiceDouble IN_ARRAY2[ANY][ANY]) {ConstSpiceDouble rot[3][3]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]     ) {ConstSpiceDouble av [3]};
%apply (SpiceDouble     OUT_ARRAY2[ANY][ANY]) {SpiceDouble    xform[6][6]};
%apply (void RETURN_VOID) {void rav2xf_c};

extern void rav2xf_c(
        ConstSpiceDouble rot  [3][3],
        ConstSpiceDouble av   [3],
        SpiceDouble      xform[6][6]);

//Vector version
VECTORIZE_dXY_dX__dMN(rav2xf, rav2xf_c, 6, 6)

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

%apply (ConstSpiceDouble IN_ARRAY2[ANY][ANY]) {ConstSpiceDouble matrix[3][3]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]     ) {SpiceDouble      axis  [3]};
%apply (void RETURN_VOID) {void raxisa_c};

extern void raxisa_c(
        ConstSpiceDouble matrix[3][3],
        SpiceDouble      axis  [3],
        SpiceDouble      *OUTPUT);

//Vector version
VECTORIZE_dXY__dN_d(raxisa, raxisa_c, 3)

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble rectan1[3]};
%apply (void RETURN_VOID) {void reccyl_c};

extern void reccyl_c(
        ConstSpiceDouble rectan1[3],
        SpiceDouble      *OUTPUT,
        SpiceDouble      *OUTPUT,
        SpiceDouble      *OUTPUT);

// Vector version
VECTORIZE_dX__3d(reccyl, reccyl_c)

/***********************************************************************
* -Procedure recgeo_c ( Rectangular to geodetic )
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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble rectan1[3]};
%apply (void RETURN_VOID) {void recgeo_c};

extern void recgeo_c(
        ConstSpiceDouble rectan1[3],
        SpiceDouble      re,
        SpiceDouble      f,
        SpiceDouble      *OUTPUT,
        SpiceDouble      *OUTPUT,
        SpiceDouble      *OUTPUT);

//Vector version
VECTORIZE_dX_2d__3d(recgeo, recgeo_c)

/***********************************************************************
* -Procedure reclat_c ( Rectangular to latitudinal coordinates )
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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble rectan1[3]};
%apply (void RETURN_VOID) {void reclat_c};

extern void reclat_c(
        ConstSpiceDouble rectan1[3],
        SpiceDouble      *OUTPUT,
        SpiceDouble      *OUTPUT,
        SpiceDouble      *OUTPUT);

// Vector version
VECTORIZE_dX__3d(reclat, reclat_c)

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

%apply (SpiceDouble IN_ARRAY1[ANY]) {SpiceDouble rectan1[3]};
%apply (void RETURN_VOID) {void recpgr_c};

extern void recpgr_c(
        ConstSpiceChar *CONST_STRING,
        SpiceDouble    rectan1[3],
        SpiceDouble    re,
        SpiceDouble    f,
        SpiceDouble    *OUTPUT,
        SpiceDouble    *OUTPUT,
        SpiceDouble    *OUTPUT);

// Vector version
VECTORIZE_s_eX_2d__3d(recpgr, recpgr_c)

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble rectan[3]};
%apply (void RETURN_VOID) {void recrad_c};

extern void recrad_c(
        ConstSpiceDouble rectan[3],
        SpiceDouble      *OUTPUT,
        SpiceDouble      *OUTPUT,
        SpiceDouble      *OUTPUT);

// Vector version
VECTORIZE_dX__3d(recrad, recrad_c)

/***********************************************************************
* -Procedure recsph_c ( Rectangular to spherical coordinates )
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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble rectan[3]};
%apply (void RETURN_VOID) {void recsph_c};

extern void recsph_c(
        ConstSpiceDouble rectan[3],
        SpiceDouble      *OUTPUT,
        SpiceDouble      *OUTPUT,
        SpiceDouble      *OUTPUT);

// Vector version
VECTORIZE_dX__3d(recsph, recsph_c)

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

%apply (SpiceDouble OUT_ARRAY2[ANY][ANY]) {SpiceDouble rotate[3][3]};
%apply (void RETURN_VOID) {void my_refchg};

/* Helper function to deal with pointers to input arguments */
%inline %{
    void my_refchg(SpiceInt    frame1,
                   SpiceInt    frame2,
                   SpiceDouble et,
                   SpiceDouble rotate[3][3]) {
        refchg_(&frame1, &frame2, &et, rotate);
    }
%}

extern void refchg_(SpiceInt    *frame1,
                    SpiceInt    *frame2,
                    SpiceDouble *et,
                    SpiceDouble *rotate);

// Vector version
VECTORIZE_2i_d__dMN(refchg, my_refchg, 3, 3)

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

%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
                          {(SpiceInt lenout, SpiceChar out[1024])};
%apply (void RETURN_VOID) {void repmc_c};

extern void repmc_c(
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceInt lenout, SpiceChar out[1024]);

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

%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
                          {(SpiceInt lenout, SpiceChar out[1024])};
%apply (void RETURN_VOID) {void repmct_c};

extern void repmct_c(
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceInt       value,
        SpiceChar      IN_STRING,
        SpiceInt lenout, SpiceChar out[1024]);

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

%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
                          {(SpiceInt lenout, SpiceChar out[1024])};
%apply (void RETURN_VOID) {void repmd_c};

extern void repmd_c(
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceDouble    value,
        SpiceInt sigdig,
        SpiceInt lenout, SpiceChar out[1024]);

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

%apply (SpiceChar IN_STRING) {SpiceChar format};
%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
                             {(SpiceInt lenout, SpiceChar out[1024])};
%apply (void RETURN_VOID)    {void repmf_c};

extern void repmf_c(
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceDouble    value,
        SpiceInt       sigdig,
        SpiceChar      format,
        SpiceInt lenout, SpiceChar out[1024]);

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

%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
                          {(SpiceInt lenout, SpiceChar out[1024])};
%apply (void RETURN_VOID) {void repmi_c};

extern void repmi_c(
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceInt       value,
        SpiceInt lenout, SpiceChar out[1024]);

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

%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
                          {(SpiceInt lenout, SpiceChar out[1024])};
%apply (void RETURN_VOID) {void repmot_c};

extern void repmot_c(
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceInt       value,
        SpiceChar      IN_STRING,
        SpiceInt lenout, SpiceChar out[1024]);

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

%rename (reset) my_reset_c;

%apply (void RETURN_VOID) {void reset_c};

extern void my_reset_c(void);

// An explict call to reset also clears the stored messages used for the
// erract EXCEPTION option
%inline %{
    void my_reset_c(void) {

        // Do a full reset even if erract == "IGNORE"
        char action[100];
        int ignoring = 0;
        erract_c("GET", 100, action);
        if (strcmp(action, "IGNORE") == 0) {
            ignoring = 1;
            erract_c("SET", 100, "RETURN");
        }

        reset_c();
        reset_messages();

        if (ignoring) {
            erract_c("SET", 100, "IGNORE");
        }
    }
%}

/***********************************************************************
* -Procedure rotate_c ( Generate a rotation matrix )
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

%apply (SpiceDouble OUT_ARRAY2[ANY][ANY]) {SpiceDouble mout[3][3]};
%apply (void RETURN_VOID) {void rotate_c};

extern void rotate_c(
        SpiceDouble angle,
        SpiceInt    iaxis,
        SpiceDouble mout[3][3]);

// Vector version
VECTORIZE_d_i__dMN(rotate, rotate_c, 3, 3)

/***********************************************************************
* -Procedure rotmat_c ( Rotate a matrix )
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

%apply (ConstSpiceDouble IN_ARRAY2[ANY][ANY]) {ConstSpiceDouble m1[3][3]};
%apply (SpiceDouble     OUT_ARRAY2[ANY][ANY]) {SpiceDouble    mout[3][3]};
%apply (void RETURN_VOID) {void rotmat_c};

extern void rotmat_c(
        ConstSpiceDouble m1[3][3],
        SpiceDouble      angle,
        SpiceInt         iaxis,
        SpiceDouble      mout[3][3]);

// Vector version
VECTORIZE_dXY_d_i__dMN(rotmat, rotmat_c, 3, 3)

/***********************************************************************
* -Procedure rotvec_c ( Transform a vector via a rotation )
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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble v1[3]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble    vout[3]};
%apply (void RETURN_VOID) {void rotvec_c};

extern void rotvec_c(
        ConstSpiceDouble v1[3],
        SpiceDouble      angle,
        SpiceInt         iaxis,
        SpiceDouble      vout[3]);

// Vector version
VECTORIZE_dX_d_i__dN(rotvec, rotvec_c, 3)

/***********************************************************************
* -Procedure rpd_c ( Radians per degree )
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

%apply (SpiceDouble RETURN_DOUBLE) {SpiceDouble rpd_c};

extern SpiceDouble rpd_c(void);

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

%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble root1[2]};
%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble root2[2]};
%apply (void RETURN_VOID) {void rquad_c};

extern void rquad_c(
        SpiceDouble a,
        SpiceDouble b,
        SpiceDouble c,
        SpiceDouble root1[2],
        SpiceDouble root2[2]);

// Vector version
VECTORIZE_3d__dM_dN(rquad, rquad_c, 2, 2)

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble vec1  [3]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble vec2  [3]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble      smajor[3]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble      sminor[3]};
%apply (void RETURN_VOID) {void saelgv_c};

extern void saelgv_c(
        ConstSpiceDouble vec1  [3],
        ConstSpiceDouble vec2  [3],
        SpiceDouble      smajor[3],
        SpiceDouble      sminor[3]);

// Vector version
VECTORIZE_dX_dX__dM_dN(saelgv, saelgv_c, 3, 3)

/***********************************************************************
* -Procedure scdecd_c ( Decode spacecraft clock )
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

%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
                          {(SpiceInt lenout, SpiceChar sclkch[256])};
%apply (void RETURN_VOID) {void scdecd_c};

extern void scdecd_c(
        SpiceInt    sc,
        SpiceDouble sclkdp,
        SpiceInt lenout, SpiceChar sclkch[256]);

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

extern void sce2c_c(
        SpiceInt    sc,
        SpiceDouble et,
        SpiceDouble *OUTPUT);

// Vector version
VECTORIZE_i_d__d(sce2c, sce2c_c)

/***********************************************************************
* -Procedure sce2s_c ( ET to SCLK string )
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

%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
                          {(SpiceInt lenout, SpiceChar sclkch[256])};
%apply (void RETURN_VOID) {void sce2s_c};

extern void sce2s_c(
        SpiceInt sc,
        SpiceDouble et,
        SpiceInt lenout, SpiceChar sclkch[256]);

/***********************************************************************
* -Procedure sce2t_c ( ET to SCLK ticks )
*
* -Abstract
*
* Convert ephemeris seconds past J2000 (ET) to integral
* encoded spacecraft clock (`ticks'). For conversion to
* fractional ticks, (required for C-kernel production), see
* the routine sce2c_c.
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

extern void sce2t_c(
        SpiceInt    sc,
        SpiceDouble et,
        SpiceDouble *OUTPUT);

// Vector version
VECTORIZE_i_d__d(sce2t, sce2t_c)

/***********************************************************************
* -Procedure scencd_c ( Encode spacecraft clock )
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

extern void scencd_c(
        SpiceInt       sc,
        ConstSpiceChar *CONST_STRING,
        SpiceDouble    *OUTPUT);

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

%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
                          {(SpiceInt lenout, SpiceChar clkstr[256])};
%apply (void RETURN_VOID) {void scfmt_c};

extern void scfmt_c(
        SpiceInt sc,
        SpiceDouble ticks,
        SpiceInt lenout, SpiceChar clkstr[256]);

/***********************************************************************
* -Procedure scpart_c ( Spacecraft Clock Partition Information )
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
%apply (SpiceDouble OUT_ARRAY2[ANY][ANY], SpiceInt *SIZE1)
                          {(SpiceDouble pstartstop[100][2], SpiceInt *nparts)};
%apply (void RETURN_VOID) {void my_scpart_c};

%inline %{
    void my_scpart_c(SpiceInt sc,
                     SpiceDouble pstartstop[100][2], SpiceInt *nparts) {

        SpiceDouble pstart[100], pstop[100];
        int         j;

        scpart_c(sc, nparts, pstart, pstop);

        for (j = 0; j < *nparts; j++) {
            pstartstop[j][0] = pstart[j];
            pstartstop[j][1] = pstop[j];
        }
    }
%}

/***********************************************************************
* -Procedure scs2e_c ( SCLK string to ET )
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

extern void scs2e_c(
        SpiceInt       sc,
        ConstSpiceChar *CONST_STRING,
        SpiceDouble    *OUTPUT);

/***********************************************************************
* -Procedure sct2e_c ( SCLK ticks to ET )
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

extern void sct2e_c(
        SpiceInt    sc,
        SpiceDouble sclkdp,
        SpiceDouble *OUTPUT);

// Vector version
VECTORIZE_i_d__d(sct2e, sct2e_c)

/***********************************************************************
* -Procedure sctiks_c ( Convert spacecraft clock string to ticks. )
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

extern void sctiks_c(
        SpiceInt       sc,
        ConstSpiceChar *CONST_STRING,
        SpiceDouble    *OUTPUT);

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

%rename (setmsg) my_setmsg_c;

%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *message};
%apply (void RETURN_VOID) {void setmsg_c};

// A call to setmsg also clears the saved errors
%inline %{
    void my_setmsg_c(ConstSpiceChar *message) {

        char action[100];
        erract_c("GET", 100, action);
        if (strcmp(action, "IGNORE") != 0) {
            setmsg_c(message);
        }

        reset_messages();
    }
%}

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

%apply (void RETURN_VOID_SIGERR) {void sigerr_c};

extern void sigerr_c(
        ConstSpiceChar *CONST_STRING);

/***********************************************************************
* -Procedure sincpt_c ( Surface intercept )
*
* -Abstract
*
*    Given an observer and a direction vector defining a ray, compute
*    the surface intercept of the ray on a target body at a specified
*    epoch, optionally corrected for light time and stellar
*    aberration.
*
*    The surface of the target body may be represented by a triaxial
*    ellipsoid or by topographic data provided by DSK files.
*
*    This routine supersedes srfxpt_c.
*
*    void sincpt_c ( ConstSpiceChar      * method,
*                    ConstSpiceChar      * target,
*                    SpiceDouble           et,
*                    ConstSpiceChar      * fixref,
*                    ConstSpiceChar      * abcorr,
*                    ConstSpiceChar      * obsrvr,
*                    ConstSpiceChar      * dref,
*                    ConstSpiceDouble      dvec   [3],
*                    SpiceDouble           spoint [3],
*                    SpiceDouble         * trgepc,
*                    SpiceDouble           srfvec [3],
*                    SpiceBoolean        * found       )
*
* -Brief_I/O
*
*    Variable  I/O  Description
*    --------  ---  --------------------------------------------------
*    method     I   Computation method.
*    target     I   Name of target body.
*    et         I   Epoch in TDB seconds past J2000 TDB.
*    fixref     I   Body-fixed, body-centered target body frame.
*    abcorr     I   Aberration correction flag.
*    obsrvr     I   Name of observing body.
*    dref       I   Reference frame of ray's direction vector.
*    dvec       I   Ray's direction vector.
*    spoint     O   Surface intercept point on the target body.
*    trgepc     O   Intercept epoch.
*    srfvec     O   Vector from observer to intercept point.
*    found      O   Flag indicating whether intercept was found.
***********************************************************************/

%rename (sincpt) sincpt_c;

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble dvec[3]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble    spoint[3]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble    srfvec[3]};
%apply (void RETURN_VOID) {void sincpt_c};

extern void sincpt_c(
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceChar   *CONST_STRING,
        SpiceDouble      et,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceDouble dvec[3],
        SpiceDouble      spoint[3],
        SpiceDouble      *OUTPUT,
        SpiceDouble      srfvec[3],
        SpiceBoolean     *OUT_BOOLEAN);

// Vector version
VECTORIZE_2s_d_4s_dX__dM_d_dN_b(sincpt, sincpt_c, 3, 3)

/***********************************************************************
* -Procedure spd_c ( Seconds per day )
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

%apply (SpiceDouble RETURN_DOUBLE) {SpiceDouble spd_c};

extern SpiceDouble spd_c(void);

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

extern void sphcyl_c(
        SpiceDouble radius,
        SpiceDouble colat,
        SpiceDouble slon,
        SpiceDouble *OUTPUT,
        SpiceDouble *OUTPUT,
        SpiceDouble *OUTPUT);

// Vector version
VECTORIZE_3d__3d(sphcyl, sphcyl_c)

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

extern void sphlat_c(
        SpiceDouble r,
        SpiceDouble colat,
        SpiceDouble lons,
        SpiceDouble *OUTPUT,
        SpiceDouble *OUTPUT,
        SpiceDouble *OUTPUT);

//Vector version
VECTORIZE_3d__3d(sphlat, sphlat_c)

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

%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble rectan[3]};
%apply (void RETURN_VOID) {void sphrec_c};

extern void sphrec_c(
        SpiceDouble r,
        SpiceDouble colat,
        SpiceDouble lon,
        SpiceDouble rectan[3]);

//Vector version
VECTORIZE_3d__dN(sphrec, sphrec_c, 3)

/***********************************************************************
* -Procedure spkacs_c ( S/P Kernel, aberration corrected state )
*
* -Abstract
*
*    Return the state (position and velocity) of a target body
*    relative to an observer, optionally corrected for light time
*    and stellar aberration, expressed relative to an inertial
*    reference frame.
*
*    void spkacs_c ( SpiceInt           targ,
*                    SpiceDouble        et,
*                    ConstSpiceChar   * ref,
*                    ConstSpiceChar   * abcorr,
*                    SpiceInt           obs,
*                    SpiceDouble        starg[6],
*                    SpiceDouble      * lt,
*                    SpiceDouble      * dlt      )
*
* -Brief_I/O
*
*    Variable  I/O  Description
*    --------  ---  --------------------------------------------------
*    targ       I   Target body.
*    et         I   Observer epoch.
*    ref        I   Inertial reference frame of output state.
*    abcorr     I   Aberration correction flag.
*    obs        I   Observer.
*    starg      O   State of target.
*    lt         O   One way light time between observer and target.
*    dlt        O   Derivative of light time with respect to time.
***********************************************************************/

%rename (spkacs) spkacs_c;

%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble starg[6]};
%apply (void RETURN_VOID) {void spkacs_c};

extern void spkacs_c(
        SpiceInt       targ,
        SpiceDouble    et,
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceInt       obs,
        SpiceDouble    starg[6],
        SpiceDouble    *OUTPUT,
        SpiceDouble    *OUTPUT);

//Vector version
VECTORIZE_i_d_2s_i__dN_d_d(spkacs, spkacs_c, 6)

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble sobs[6]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble     ptarg[3]};
%apply (void RETURN_VOID) {void spkapo_c};

extern void spkapo_c(
        SpiceInt         targ,
        SpiceDouble      et,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceDouble sobs[6],
        ConstSpiceChar   *CONST_STRING,
        SpiceDouble      ptarg[3],
        SpiceDouble      *OUTPUT);

//Vector version
VECTORIZE_i_d_s_dX_s__dN_d(spkapo, spkapo_c, 3)

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble sobs[6]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble     starg[6]};
%apply (void RETURN_VOID) {void spkapp_c};

extern void spkapp_c(
        SpiceInt         targ,
        SpiceDouble      et,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceDouble sobs[6],
        ConstSpiceChar   *CONST_STRING,
        SpiceDouble      starg[6],
        SpiceDouble      *OUTPUT);

//Vector version
VECTORIZE_i_d_s_dX_s__dN_d(spkapp, spkapp_c, 6)

/***********************************************************************
* -Procedure spkaps_c ( SPK, apparent state )
*
* -Abstract
*
*    Given the state and acceleration of an observer relative to the
*    solar system barycenter, return the state (position and velocity)
*    of a target body relative to the observer, optionally corrected
*    for light time and stellar aberration. All input and output
*    vectors are expressed relative to an inertial reference frame.
*
*    This routine supersedes spkapp_c.
*
*    SPICE users normally should call the high-level API routines
*    spkezr_c or spkez_c rather than this routine.
*
*    void spkaps_c ( SpiceInt           targ,
*                    SpiceDouble        et,
*                    ConstSpiceChar   * ref,
*                    ConstSpiceChar   * abcorr,
*                    ConstSpiceDouble   stobs [6],
*                    ConstSpiceDouble   accobs[6],
*                    SpiceDouble        starg [6],
*                    SpiceDouble      * lt,
*                    SpiceDouble      * dlt      )
*
* -Brief_I/O
*
*    Variable  I/O  Description
*    --------  ---  --------------------------------------------------
*    targ       I   Target body.
*    et         I   Observer epoch.
*    ref        I   Inertial reference frame of output state.
*    abcorr     I   Aberration correction flag.
*    stobs      I   State of the observer relative to the SSB.
*    accobs     I   Acceleration of the observer relative to the SSB.
*    starg      O   State of target.
*    lt         O   One way light time between observer and target.
*    dlt        O   Derivative of light time with respect to time.
***********************************************************************/

%rename (spkaps) spkaps_c;

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble stobs [6]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble accobs[3]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble      starg [6]};
%apply (void RETURN_VOID) {void spkaps_c};

extern void spkaps_c(
        SpiceInt         targ,
        SpiceDouble      et,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceDouble stobs[6],
        ConstSpiceDouble accobs[3],
        SpiceDouble      starg[6],
        SpiceDouble      *OUTPUT,
        SpiceDouble      *OUTPUT);

//Vector version
VECTORIZE_i_d_2s_dX_dX__dN_d_d(spkaps, spkaps_c, 6)

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

%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *spk};
%apply (SpiceDouble OUT_ARRAY2[ANY][ANY], int *SIZE1)
                        {(SpiceDouble array[500][2], int *intervals)};
%apply (void RETURN_VOID) {void my_spkcov_c};

%inline %{
    /* Helper function to create a 2-D array of results */
    void my_spkcov_c(ConstSpiceChar *spk,
                     SpiceInt       idcode,
                     SpiceDouble array[500][2], int *intervals) {

        int j;
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

%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble starg[6]};
%apply (void RETURN_VOID) {void spkez_c};

extern void spkez_c(
        SpiceInt       targ,
        SpiceDouble    et,
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceInt       obs,
        SpiceDouble    starg[6],
        SpiceDouble    *OUTPUT);

//Vector version
VECTORIZE_i_d_2s_i__dN_d(spkez, spkez_c, 6)

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

%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble ptarg[3]};
%apply (void RETURN_VOID) {void spkezp_c};

extern void spkezp_c(
        SpiceInt       targ,
        SpiceDouble    et,
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceInt       obs,
        SpiceDouble    ptarg[3],
        SpiceDouble    *OUTPUT);

//Vector version
VECTORIZE_i_d_2s_i__dN_d(spkezp, spkezp_c, 3)

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

%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble starg[6]};
%apply (void RETURN_VOID) {void spkezr_c};

extern void spkezr_c(
        ConstSpiceChar *CONST_STRING,
        SpiceDouble    et,
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceDouble    starg[6],
        SpiceDouble    *OUTPUT);

//Vector version
VECTORIZE_s_d_3s__dN_d(spkezr, spkezr_c, 6)

/*******************************************
* Vector version
*******************************************/

// %apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *targ};
// %apply (ConstSpiceDouble *IN_ARRAY1, int DIM1)
//                 {(ConstSpiceDouble *et, int et_dim1)};
// %apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *ref};
// %apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *abcorr};
// %apply (SpiceDouble **OUT_ARRAY2, int *SIZE1, int *SIZE2)
//                 {(SpiceDouble **starg, int *starg_dim1, int *starg_dim2)};
// %apply (SpiceDouble **OUT_ARRAY1, int *SIZE1)
//                 {(SpiceDouble **lt, int *lt_dim1)};
// %apply (void RETURN_VOID) {void spkezr_vector};
// 
// %inline %{
//     void spkezr_vector(ConstSpiceChar *targ,
//                        ConstSpiceDouble *et, int et_dim1,
//                        ConstSpiceChar *ref,
//                        ConstSpiceChar *abcorr,
//                        ConstSpiceChar *obs,
//                        SpiceDouble **starg, int *starg_dim1, int *starg_dim2,
//                        SpiceDouble **lt, int *lt_dim1) {
// 
//         SpiceInt        targ_id, targ_found;
//         SpiceBoolean    obs_id,  obs_found;
//         SpiceDouble     temp_state[6], temp_lt;
// 
//         //Look up target
//         bodn2c(targ, &targ_id, &targ_found);
//         bodn2c(obs,  &obs_id,  &obs_found);
// 
//         //If target is found, use spkez_vector
//         if (targ_found && obs_found) {
//             spkez_vector(targ_id, et, et_dim1, ref, abcorr, obs_id,
//                          starg, starg_dim1, starg_dim2,
//                          lt, lt_dim1);
//         }
//         //Otherwise, let the scalar version set the error condition
//         else {
//             spkezr_c(targ, et[0], ref, abcorr, obs,
//                     temp_state, &temp_lt);
//         }
//     }
// %}

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

%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble state[6]};
%apply (void RETURN_VOID) {void spkgeo_c};

extern void spkgeo_c(
        SpiceInt       targ,
        SpiceDouble    et,
        ConstSpiceChar *CONST_STRING,
        SpiceInt       obs,
        SpiceDouble    state[6],
        SpiceDouble    *OUTPUT);

//Vector version
VECTORIZE_i_d_s_i__dN_d(spkgeo, spkgeo_c, 6)

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

%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble pos[3]};
%apply (void RETURN_VOID) {void spkgps_c};

extern void spkgps_c(
        SpiceInt       targ,
        SpiceDouble    et,
        ConstSpiceChar *CONST_STRING,
        SpiceInt       obs,
        SpiceDouble    pos[3],
        SpiceDouble    *OUTPUT);

//Vector version
VECTORIZE_i_d_s_i__dN_d(spkgps, spkgps_c, 3)

/***********************************************************************
* -Procedure spkltc_c ( S/P Kernel, light time corrected state )
*
* -Abstract
*
*    Return the state (position and velocity) of a target body
*    relative to an observer, optionally corrected for light time,
*    expressed relative to an inertial reference frame.
*
*    void spkltc_c ( SpiceInt           targ,
*                    SpiceDouble        et,
*                    ConstSpiceChar   * ref,
*                    ConstSpiceChar   * abcorr,
*                    ConstSpiceDouble   stobs[6],
*                    SpiceDouble        starg[6],
*                    SpiceDouble      * lt,
*                    SpiceDouble      * dlt      )
*
* -Brief_I/O
*
*    Variable  I/O  Description
*    --------  ---  --------------------------------------------------
*    targ       I   Target body.
*    et         I   Observer epoch.
*    ref        I   Inertial reference frame of output state.
*    abcorr     I   Aberration correction flag.
*    stobs      I   State of the observer relative to the SSB.
*    starg      O   State of target.
*    lt         O   One way light time between observer and target.
*    dlt        O   Derivative of light time with respect to time.
***********************************************************************/

%rename (spkltc) spkltc_c;

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble stobs[6]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble      starg[6]};
%apply (void RETURN_VOID) {void spkltc_c};

extern void spkltc_c(
        SpiceInt         targ,
        SpiceDouble      et,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceDouble stobs[6],
        SpiceDouble      starg[6],
        SpiceDouble      *OUTPUT,
        SpiceDouble      *OUTPUT);

//Vector version
VECTORIZE_i_d_2s_dX__dN_d_d(spkltc, spkltc_c, 6)

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

%apply (ConstSpiceChar *CONST_STRING)    {ConstSpiceChar *spk};
%apply (int OUT_ARRAY1[ANY], int *SIZE1) {(int body_ids[200], int *bodies)};
%apply (void RETURN_VOID) {void my_spkobj_c};

/* Helper function to create a 1-D array of results */
%inline %{
    void my_spkobj_c(ConstSpiceChar *spk,
                     int body_ids[200], int *bodies) {

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

%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble ptarg[3]};
%apply (void RETURN_VOID) {void spkpos_c};

extern void spkpos_c(
        ConstSpiceChar *CONST_STRING,
        SpiceDouble    et,
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceDouble    ptarg[3],
        SpiceDouble    *OUTPUT);

//Vector version
VECTORIZE_s_d_3s__dN_d(spkpos, spkpos_c, 3)

/*******************************************
* Vector version
*******************************************/
// 
// %apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *targ};
// %apply (ConstSpiceDouble *IN_ARRAY1, int DIM1)
//                 {(ConstSpiceDouble *et, int et_dim1)};
// %apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *ref};
// %apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *abcorr};
// %apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *obs};
// %apply (SpiceDouble **OUT_ARRAY2, int *SIZE1, int *SIZE2)
//                 {(SpiceDouble **starg, int *starg_dim1, int *starg_dim2)};
// %apply (SpiceDouble **OUT_ARRAY1, int *SIZE1)
//                 {(SpiceDouble **lt, int *lt_dim1)};
// %apply (void RETURN_VOID) {void spkpos_vector};
// 
// %inline %{
//     void spkpos_vector(ConstSpiceChar   *targ,
//                        ConstSpiceDouble *et, int et_dim1,
//                        ConstSpiceChar   *ref,
//                        ConstSpiceChar   *abcorr,
//                        ConstSpiceChar   *obs,
//                        SpiceDouble **ptarg, int *ptarg_dim1, int *ptarg_dim2,
//                        SpiceDouble    **lt, int *lt_dim1) {
// 
//         SpiceInt        targ_id, obs_id;
//         SpiceBoolean    targ_found, obs_found;
//         SpiceDouble     temp_state[6], temp_lt;
// 
//         //Look up target and observer
//         bodn2c(targ, &targ_id, &targ_found);
//         bodn2c(obs,  &obs_id,  &obs_found);
// 
//         //If target and observer are found, use spkezp_vector
//         if (targ_found && obs_found) {
//             spkezp_vector(targ_id, et, et_dim1, ref, abcorr, obs_id,
//                           ptarg, ptarg_dim1, ptarg_dim2,
//                           lt, lt_dim1);
//         }
//         //Otherwise, let the scalar version set the error condition
//         else {
//             spkpos_c(targ, et[0], ref, abcorr, obs,
//                      temp_state, &temp_lt);
//         }
//     }
// %}

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

%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble starg[6]};
%apply (void RETURN_VOID) {void spkssb_c};

extern void spkssb_c(
        SpiceInt       targ,
        SpiceDouble    et,
        ConstSpiceChar *CONST_STRING,
        SpiceDouble    starg[6]);

//Vector version
VECTORIZE_i_d_s__dN(spkssb, spkssb_c, 6)

/***********************************************************************
* -Procedure srfc2s_c ( Surface and body ID codes to surface string )
*
* -Abstract
*
*    Translate a surface ID code, together with a body ID code, to the
*    corresponding surface name. If no such name exists, return a
*    string representation of the surface ID code.
*
*    void srfc2s_c ( SpiceInt        code,
*                    SpiceInt        bodyid,
*                    SpiceInt        srflen,
*                    SpiceChar     * srfstr,
*                    SpiceBoolean  * isname )
*
* -Brief_I/O
*
*    Variable  I/O  Description
*    --------  ---  --------------------------------------------------
*    code       I   Integer surface ID code to translate to a string.
*    bodyid     I   ID code of body associated with surface.
*    srflen     I   Length of output string `srfstr'.
*    srfstr     O   String corresponding to surface ID code.
*    isname     O   Logical flag indicating output is a surface name.
*    SPICE_SRF_SFNMLN
*               P   Maximum length of surface name.
***********************************************************************/

%rename (srfc2s) srfc2s_c;

%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
                          {(SpiceInt srflen, SpiceChar srfstr[256])}
%apply (void RETURN_VOID) {void srfc2s_c};

extern void srfc2s_c(
        SpiceInt     code,
        SpiceInt     bodyid,
        SpiceInt srflen, SpiceChar srfstr[256],
        SpiceBoolean *OUT_BOOLEAN);

/***********************************************************************
* -Procedure srfcss_c ( Surface ID and body string to surface string )
*
* -Abstract
*
*    Translate a surface ID code, together with a body string, to the
*    corresponding surface name. If no such surface name exists,
*    return a string representation of the surface ID code.
*
*    void srfcss_c ( SpiceInt          code,
*                    ConstSpiceChar  * bodstr,
*                    SpiceInt          srflen,
*                    SpiceChar       * srfstr,
*                    SpiceBoolean    * isname )
*
* -Brief_I/O
*
*    Variable  I/O  Description
*    --------  ---  --------------------------------------------------
*    code       I   Integer surface ID code to translate to a string.
*    bodstr     I   Name or ID of body associated with surface.
*    srflen     I   Length of output string `srfstr'.
*    srfstr     O   String corresponding to surface ID code.
*    isname     O   Flag indicating whether output is a surface name.
*    SPICE_SRF_SFNMLN
*               P   Maximum length of surface name.
***********************************************************************/

%rename (srfcss) srfcss_c;

%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
                          {(SpiceInt srflen, SpiceChar srfstr[256])}
%apply (void RETURN_VOID) {void srfcss_c};

extern void srfcss_c(
        SpiceInt       code,
        ConstSpiceChar *CONST_STRING,
        SpiceInt srflen, SpiceChar srfstr[256],
        SpiceBoolean   *OUT_BOOLEAN);

/***********************************************************************
* -Procedure srfnrm_c ( Map surface points to outward normal vectors )
*
* -Abstract
*
*    Map array of surface points on a specified target body to
*    the corresponding unit length outward surface normal vectors.
*
*    The surface of the target body may be represented by a triaxial
*    ellipsoid or by topographic data provided by DSK files.
*
*    void srfnrm_c ( ConstSpiceChar    * method,
*                    ConstSpiceChar    * target,
*                    SpiceDouble         et,
*                    ConstSpiceChar    * fixref,
*                    SpiceInt            npts,
*                    ConstSpiceDouble    srfpts[][3],
*                    SpiceDouble         normls[][3]  )
*
* -Brief_I/O
*
*    Variable  I/O  Description
*    --------  ---  --------------------------------------------------
*    method     I   Computation method.
*    target     I   Name of target body.
*    et         I   Epoch in TDB seconds past J2000 TDB.
*    fixref     I   Body-fixed, body-centered target body frame.
*    npts       I   Number of surface points in input array.
*    srfpts     I   Array of surface points.
*    normls     O   Array of outward, unit length normal vectors.
*
*    SPICE_DSKTOL_PTMEMM
*               P   Default point-surface membership margin.
***********************************************************************/

%rename (srfnrm) my_srfnrm_c;

%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *method};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *target};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *fixref};
%apply (SpiceInt DIM1, ConstSpiceDouble IN_ARRAY2[ANY][ANY])
                          {(SpiceInt npts, SpiceDouble srfpts[1][3])};
%apply (SpiceDouble **OUT_ARRAY2, int *SIZE1, int *SIZE2)
                          {(SpiceDouble **normls, int *dim1, int *dim2)};
%apply (void RETURN_VOID) {void my_srfnrm_c};

/* Helper function to deal with order of arguments */
%inline %{
    void my_srfnrm_c(ConstSpiceChar *method,
                     ConstSpiceChar *target,
                     SpiceDouble    et,
                     ConstSpiceChar *fixref,
                     SpiceInt npts, SpiceDouble srfpts[1][3],
                     SpiceDouble **normls, int *dim1, int *dim2) {

        *normls = NULL;
        *dim1 = 0;
        *dim2 = 3;

        SpiceDouble *result = my_malloc(npts * 3, "srfnrm");
        if (!result) return;

        srfnrm_c(method, target, et, fixref, npts, srfpts, result);

        if (failed_c()) {
            free(result);
        }
        else {
            *normls = result;
            *dim1 = npts;
            *dim2 = 3;
        }
    }
%}

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

%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble rectan[3]};
%apply (void RETURN_VOID) {void srfrec_c};

extern void srfrec_c(
        SpiceInt    body,
        SpiceDouble longitude,
        SpiceDouble latitude,
        SpiceDouble rectan[3]);

//Vector version
VECTORIZE_i_2d__dN(srfrec, srfrec_c, 3)

/***********************************************************************
* -Procedure srfs2c_c ( Surface and body strings to surface ID code )
*
* -Abstract
*
*    Translate a surface string, together with a body string, to the
*    corresponding surface ID code. The input strings may contain
*    names or integer ID codes.
*
*    void srfs2c_c ( ConstSpiceChar  * srfstr,
*                    ConstSpiceChar  * bodstr,
*                    SpiceInt        * code,
*                    SpiceBoolean    * found )
*
* -Brief_I/O
*
*    Variable  I/O  Description
*    --------  ---  --------------------------------------------------
*    srfstr     I   Surface name or ID string.
*    bodstr     I   Body name or ID string.
*    code       O   Integer surface ID code.
*    found      O   Flag indicating whether surface ID was found.
***********************************************************************/

%rename (srfs2c) srfs2c_c;

%apply (void RETURN_VOID) {void srfs2c_c};

extern void srfs2c_c(
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceInt       *OUTPUT,
        SpiceBoolean   *OUT_BOOLEAN);

/***********************************************************************
* -Procedure srfscc_c (Surface string and body ID code to surface ID code)
*
* -Abstract
*
*    Translate a surface string, together with a body ID code, to the
*    corresponding surface ID code. The input surface string may
*    contain a name or an integer ID code.
*
*    void srfscc_c ( ConstSpiceChar  * srfstr,
*                    SpiceInt          bodyid,
*                    SpiceInt        * code,
*                    SpiceBoolean    * found  )
*
* -Brief_I/O
*
*    Variable  I/O  Description
*    --------  ---  --------------------------------------------------
*    srfstr     I   Surface name or ID string.
*    bodyid     I   Body ID code.
*    code       O   Integer surface ID code.
*    found      O   Flag indicating whether surface ID was found.
***********************************************************************/

%rename (srfscc) srfscc_c;

%apply (void RETURN_VOID) {void srfscc_c};

extern void srfscc_c(
        ConstSpiceChar *CONST_STRING,
        SpiceInt       body_id,
        SpiceInt       *OUTPUT,
        SpiceBoolean   *OUT_BOOLEAN);

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble dvec[3]};
%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble spoint[3]};
%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble obspos[3]};
%apply (void RETURN_VOID) {void srfxpt_c};

extern void srfxpt_c(
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceChar   *CONST_STRING,
        SpiceDouble      et,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceDouble dvec[3],
        SpiceDouble      spoint[3],
        SpiceDouble      *OUTPUT,
        SpiceDouble      *OUTPUT,
        SpiceDouble      obspos[3],
        SpiceBoolean     *OUT_BOOLEAN);

//Vector version
VECTORIZE_2s_d_3s_dX__dM_2d_dN_b(srfxpt, srfxpt_c, 3, 3)

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
*               eastra, doublereal *sthdec, doublereal *nthdec, integer *nstars,
*               ftnlen catnam_len)
*
* New arguments with wrapper:
*   int my_stcf01_c(char *catnam, SpiceDouble westra, SpiceDoubleSpiceDouble eastra,
*                   SpiceDouble sthdec, SpiceDouble nthdec,
*                   int *nstars)
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

%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *catnam};
%apply (SpiceInt *OUTPUT) {SpiceInt *nstars};
%apply (void RETURN_VOID) {void my_stcf01_c};

/* Helper function to reorder arguments */
%inline %{
    void my_stcf01_c(ConstSpiceChar *catnam,
                     SpiceDouble westra,
                     SpiceDouble eastra,
                     SpiceDouble sthdec,
                     SpiceDouble nthdec,
                     SpiceInt    *nstars) {
        stcf01_(catnam, &westra, &eastra, &sthdec, &nthdec, nstars,
                (int) strlen(catnam));
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
*               doublereal *rasig, doublereal *decsig, integer *catnum,
*               char *sptype, doublereal *vmag, ftnlen sptype_len)
*
* New arguments with wrapper:
*   int my_stcg01_c(int index, SpiceDouble *ra, SpiceDouble *dec,
*                   SpiceDouble *rasig, SpiceDouble *decsig, int *catnum,
*                   char *sptype, doublel *vmag)
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

%apply (SpiceDouble *OUTPUT)       {SpiceDouble *ra};
%apply (SpiceDouble *OUTPUT)       {SpiceDouble *dec};
%apply (SpiceDouble *OUTPUT)       {SpiceDouble *rasig};
%apply (SpiceDouble *OUTPUT)       {SpiceDouble *decsig};
%apply (SpiceInt *OUTPUT)          {SpiceInt *catnum};
%apply (SpiceChar OUT_STRING[ANY]) {SpiceChar sptype[20]};
%apply (SpiceDouble *OUTPUT)       {SpiceDouble *vmag};
%apply (void RETURN_VOID) {void my_stcg01_c};

/* Helper function to reorder arguments */
%inline %{
   void my_stcg01_c(SpiceInt    index,
                    SpiceDouble *ra,
                    SpiceDouble *dec,
                    SpiceDouble *rasig,
                    SpiceDouble *decsig,
                    SpiceInt    *catnum,
                    SpiceChar   sptype[20],
                    SpiceDouble *vmag) {

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
*               ftnlen catfnm_len, ftnlen tabnam_len)
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

%apply (SpiceChar OUT_STRING[ANY]) {SpiceChar tabnam[256]};
%apply (SpiceInt *OUTPUT)          {SpiceInt *handle};
%apply (void RETURN_VOID) {void my_stcl01_c};

/* Helper function to convert strings and reorder arguments */
%inline %{
    void my_stcl01_c(ConstSpiceChar *catfnm,
                     SpiceChar      tabnam[256],
                     SpiceInt       *handle) {
        char *s;
        stcl01_(catfnm, tabnam, handle, (int) strlen(catfnm), 256);
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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble pobj  [3]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble vobs  [3]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble      appobj[3]};
%apply (void RETURN_VOID) {void stelab_c};

extern void stelab_c(
        ConstSpiceDouble pobj  [3],
        ConstSpiceDouble vobs  [3],
        SpiceDouble      appobj[3]);

//Vector version
VECTORIZE_dX_dX__dN(stelab, stelab_c, 3)

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble pobj  [3]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble vobs  [3]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble      corpos[3]};
%apply (void RETURN_VOID) {void stlabx_c};

extern void stlabx_ (
        ConstSpiceDouble pobj  [3],
        ConstSpiceDouble vobs  [3],
        SpiceDouble      corpos[3]);

//Vector version
VECTORIZE_dX_dX__dN(stlabx, stlabx_, 3)

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

%rename (stpool) my_stpool_c;

%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *item};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *contin};
%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
                {(SpiceInt lenout, SpiceChar string[1024])};
%apply (SpiceBoolean *OUT_BOOLEAN) {SpiceBoolean *found};
%apply (void RETURN_VOID) {void stpool_c};

/* Helper function to deal with extraneous return argument */
%inline %{
    void my_stpool_c(ConstSpiceChar *item,
                     SpiceInt       nth,
                     ConstSpiceChar *contin,
                     SpiceInt lenout, SpiceChar string[1024],
                     SpiceBoolean   *found) {

        SpiceInt size = 0;

        stpool_c(item, nth, contin,
                 lenout, string, &size, found);
    }
%}

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

extern void str2et_c(
        ConstSpiceChar *CONST_STRING,
        SpiceDouble    *OUTPUT);

/***********************************************************************
* -Procedure subpnt_c ( Sub-observer point )
*
* -Abstract
*
*    Compute the rectangular coordinates of the sub-observer point on
*    a target body at a specified epoch, optionally corrected for
*    light time and stellar aberration.
*
*    The surface of the target body may be represented by a triaxial
*    ellipsoid or by topographic data provided by DSK files.
*
*    This routine supersedes subpt_c.
*
*    void subpnt_c ( ConstSpiceChar       * method,
*                    ConstSpiceChar       * target,
*                    SpiceDouble            et,
*                    ConstSpiceChar       * fixref,
*                    ConstSpiceChar       * abcorr,
*                    ConstSpiceChar       * obsrvr,
*                    SpiceDouble            spoint [3],
*                    SpiceDouble          * trgepc,
*                    SpiceDouble            srfvec [3] )
*
* -Brief_I/O
*
*    Variable  I/O  Description
*    --------  ---  --------------------------------------------------
*    method     I   Computation method.
*    target     I   Name of target body.
*    et         I   Epoch in TDB seconds past J2000 TDB.
*    fixref     I   Body-fixed, body-centered target body frame.
*    abcorr     I   Aberration correction flag.
*    obsrvr     I   Name of observing body.
*    spoint     O   Sub-observer point on the target body.
*    trgepc     O   Sub-observer point epoch.
*    srfvec     O   Vector from observer to sub-observer point.
***********************************************************************/

%rename (subpnt) subpnt_c;

%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble spoint[3]};
%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble srfvec[3]};
%apply (void RETURN_VOID) {void subpnt_c};

extern void subpnt_c(
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceDouble    et,
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceDouble    spoint[3],
        SpiceDouble    *OUTPUT,
        SpiceDouble    srfvec[3]);

//Vector version
VECTORIZE_2s_d_3s__dM_d_dN(subpnt, subpnt_c, 3, 3)

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

%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble spoint[3]};
%apply (void RETURN_VOID) {void subpt_c};

extern void subpt_c(
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceDouble    et,
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceDouble    spoint[3],
        SpiceDouble    *OUTPUT);

//Vector version
VECTORIZE_2s_d_2s__dN_d(subpt, subpt_c, 3)

/***********************************************************************
* -Procedure subslr_c ( Sub-solar point )
*
* -Abstract
*
*    Compute the rectangular coordinates of the sub-solar point on
*    a target body at a specified epoch, optionally corrected for
*    light time and stellar aberration.
*
*    The surface of the target body may be represented by a triaxial
*    ellipsoid or by topographic data provided by DSK files.
*
*    This routine supersedes subsol_c.
*
*    void subslr_c ( ConstSpiceChar       * method,
*                    ConstSpiceChar       * target,
*                    SpiceDouble            et,
*                    ConstSpiceChar       * fixref,
*                    ConstSpiceChar       * abcorr,
*                    ConstSpiceChar       * obsrvr,
*                    SpiceDouble            spoint [3],
*                    SpiceDouble          * trgepc,
*                    SpiceDouble            srfvec [3] )
*
* -Brief_I/O
*
*    Variable  I/O  Description
*    --------  ---  --------------------------------------------------
*    method     I   Computation method.
*    target     I   Name of target body.
*    et         I   Epoch in ephemeris seconds past J2000 TDB.
*    fixref     I   Body-fixed, body-centered target body frame.
*    abcorr     I   Aberration correction.
*    obsrvr     I   Name of observing body.
*    spoint     O   Sub-solar point on the target body.
*    trgepc     O   Sub-solar point epoch.
*    srfvec     O   Vector from observer to sub-solar point.
***********************************************************************/

%rename (subslr) subslr_c;

%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble spoint[3]};
%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble srfvec[3]};
%apply (void RETURN_VOID) {void subslr_c};

extern void subslr_c(
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceDouble    et,
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceDouble    spoint[3],
        SpiceDouble    *OUTPUT,
        SpiceDouble    srfvec[3]);

//Vector version
VECTORIZE_2s_d_3s__dM_d_dN(subslr, subslr_c, 3, 3)

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

%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble spoint[3]};
%apply (void RETURN_VOID) {void subsol_c};

extern void subsol_c(
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceDouble    et,
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceDouble    spoint[3]);

//Vector version
VECTORIZE_2s_d_2s__dN(subsol, subsol_c, 3)

/***********************************************************************
* -Procedure surfnm_c ( Surface normal vector on an ellipsoid )
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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble point [3]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble      normal[3]};
%apply (void RETURN_VOID) {void surfnm_c};

extern void surfnm_c(
        SpiceDouble      a,
        SpiceDouble      b,
        SpiceDouble      c,
        ConstSpiceDouble point[ 3],
        SpiceDouble      normal[3]);

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble positn[3]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble u[     3]};
%apply (SpiceDouble  OUT_ARRAY1[ANY]) {SpiceDouble point [3]};
%apply (void RETURN_VOID) {void surfpt_c};

extern void surfpt_c(
        ConstSpiceDouble positn[3],
        ConstSpiceDouble u[3],
        SpiceDouble      a,
        SpiceDouble      b,
        SpiceDouble      c,
        SpiceDouble      point[3],
        SpiceBoolean     *OUT_BOOLEAN);

//Vector version
VECTORIZE_dX_dX_3d__dN_b(surfpt, surfpt_c, 3)

/***********************************************************************
* -Procedure surfpv_c ( Surface point and velocity )
*
* -Abstract
*
*    Find the state (position and velocity) of the surface intercept
*    defined by a specified ray, ray velocity, and ellipsoid.
*
*    void surfpv_c ( ConstSpiceDouble      stvrtx[6],
*                    ConstSpiceDouble      stdir [6],
*                    SpiceDouble           a,
*                    SpiceDouble           b,
*                    SpiceDouble           c,
*                    SpiceDouble           stx   [6],
*                    SpiceBoolean        * found      )
*
* -Brief_I/O
*
*    Variable  I/O  Description
*    --------  ---  --------------------------------------------------
*    stvrtx     I   State of ray's vertex.
*    stdir      I   State of ray's direction vector.
*    a          I   Length of ellipsoid semi-axis along the x-axis.
*    b          I   Length of ellipsoid semi-axis along the y-axis.
*    c          I   Length of ellipsoid semi-axis along the z-axis.
*    stx        O   State of surface intercept.
*    found      O   Flag indicating whether intercept state was found.
***********************************************************************/

%rename (surfpv) surfpv_c;

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble stvrtx[6]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble stdir[6]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble      stx[6]};
%apply (void RETURN_VOID) {void surfpv_c};

extern void surfpv_c(
        ConstSpiceDouble stvrtx[6],
        ConstSpiceDouble stdir[6],
        SpiceDouble      a,
        SpiceDouble      b,
        SpiceDouble      c,
        SpiceDouble      stx[6],
        SpiceBoolean     *OUT_BOOLEAN);

//Vector version
VECTORIZE_dX_dX_3d__dN_b(surfpv, surfpv_c, 6)

/***********************************************************************
* -Procedure sxform_c ( State Transformation Matrix )
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

%apply (SpiceDouble OUT_ARRAY2[ANY][ANY]) {SpiceDouble xform[6][6]};
%apply (void RETURN_VOID) {void sxform_c};

extern void sxform_c(
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceDouble    et,
        SpiceDouble    xform[6][6]);

//Vector version
VECTORIZE_2s_d__dMN(sxform, sxform_c, 6, 6)

/***********************************************************************
* -Procedure termpt_c ( Terminator points on an extended object )
* 
* -Abstract
*  
*    Find terminator points on a target body. The caller specifies
*    half-planes, bounded by the illumination source center-target center
*    vector, in which to search for terminator points.
*  
*    The terminator can be either umbral or penumbral. The umbral 
*    terminator is the boundary of the region on the target surface 
*    where no light from the source is visible. The penumbral 
*    terminator is the boundary of the region on the target surface 
*    where none of the light from the source is blocked by the target 
*    itself. 
*  
*    The surface of the target body may be represented either by a 
*    triaxial ellipsoid or by topographic data. 
*  
*    void termpt_c ( ConstSpiceChar      * method,
*                    ConstSpiceChar      * ilusrc,
*                    ConstSpiceChar      * target,
*                    SpiceDouble           et,
*                    ConstSpiceChar      * fixref,
*                    ConstSpiceChar      * abcorr,
*                    ConstSpiceChar      * corloc,
*                    ConstSpiceChar      * obsrvr,
*                    ConstSpiceDouble      refvec[3],
*                    SpiceDouble           rolstp,
*                    SpiceInt              ncuts,
*                    SpiceDouble           schstp,
*                    SpiceDouble           soltol,
*                    SpiceInt              maxn,
*                    SpiceInt              npts  [],
*                    SpiceDouble           points[][3],
*                    SpiceDouble           epochs[],
*                    SpiceDouble           trmvcs[][3]  )         
* 
* -Brief_I/O
*  
*    Variable  I/O  Description 
*    --------  ---  -------------------------------------------------- 
*    method     I   Computation method. 
*    ilusrc     I   Illumination source. 
*    target     I   Name of target body. 
*    et         I   Epoch in ephemeris seconds past J2000 TDB. 
*    fixref     I   Body-fixed, body-centered target body frame. 
*    abcorr     I   Aberration correction. 
*    corloc     I   Aberration correction locus. 
*    obsrvr     I   Name of observing body. 
*    refvec     I   Reference vector for cutting half-planes. 
*    rolstp     I   Roll angular step for cutting half-planes. 
*    ncuts      I   Number of cutting planes. 
*    schstp     I   Angular step size for searching. 
*    soltol     I   Solution convergence tolerance. 
*    maxn       I   Maximum number of entries in output arrays. 
*    npts       O   Counts of terminator points corresponding to cuts. 
*    points     O   Terminator points. 
*    epochs     O   Times associated with terminator points. 
*    trmvcs     O   Terminator vectors emanating from the observer. 
***********************************************************************/

%rename (termpt) my_termpt_c;

%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *method};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *ilusrc};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *target};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *fixref};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *abcorr};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *corloc};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *obsrvr};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble refvec[3]};

%apply (SpiceInt **OUT_ARRAY1, SpiceInt *SIZE1)
                               {(SpiceInt **npts, SpiceInt *ndim1)};
%apply (SpiceDouble **OUT_ARRAY2, int *SIZE1, int *SIZE2)
                               {(SpiceDouble **points, int *pdim1, int *pdim2)};
%apply (SpiceDouble **OUT_ARRAY1, int *SIZE1)
                               {(SpiceDouble **epochs, int *edim1)};
%apply (SpiceDouble **OUT_ARRAY2, int *SIZE1, int *SIZE2)
                               {(SpiceDouble **trmvcs, int *tdim1, int *tdim2)};

%apply (void RETURN_VOID) {void my_termpt_c};

/* Helper function to deal with order of arguments */
%inline %{  
    void my_termpt_c(ConstSpiceChar   *method,
                     ConstSpiceChar   *ilusrc,
                     ConstSpiceChar   *target,
                     SpiceDouble      et,
                     ConstSpiceChar   *fixref,
                     ConstSpiceChar   *abcorr,
                     ConstSpiceChar   *corloc,
                     ConstSpiceChar   *obsrvr,
                     ConstSpiceDouble refvec[3],
                     SpiceDouble      rolstp,
                     SpiceInt         ncuts,
                     SpiceDouble      schstp,
                     SpiceDouble      soltol,
                     SpiceInt         maxn,
                     SpiceInt    **npts,   SpiceInt *ndim1,
                     SpiceDouble **points, int      *pdim1, int *pdim2,
                     SpiceDouble **epochs, int      *edim1,
                     SpiceDouble **trmvcs, int      *tdim1, int *tdim2) {

        SpiceInt    *npts1 = my_int_malloc(maxn,   "termpt");
        SpiceDouble *points1 = my_malloc(maxn * 3, "termpt");
        SpiceDouble *epochs1 = my_malloc(maxn,     "termpt");
        SpiceDouble *trmvcs1 = my_malloc(maxn * 3, "termpt");

        if (!trmvcs1) {
            free(npts1);
            free(points1);
            free(epochs1);
            free(trmvcs1);
            return;
        }

        termpt_c(method, ilusrc, target, et, fixref, abcorr, corloc, obsrvr,
                 refvec, rolstp, ncuts, schstp, soltol, maxn,
                 npts1, points1, epochs1, trmvcs1);

        if (failed_c()) {
            free(npts1);
            *npts = NULL;
            *ndim1 = 0;

            free(points1);
            *points = NULL;
            *pdim1 = 0;
            *pdim2 = 3;

            free(epochs1);
            *epochs = NULL;
            *edim1 = 0;

            free(trmvcs1);
            *trmvcs = NULL;
            *tdim1 = 0;
            *tdim2 = 3;
        }
        else {
            *npts = npts1;
            *ndim1 = maxn;

            *points = points1;
            *pdim1 = maxn;
            *pdim2 = 3;

            *epochs = epochs1;
            *edim1 = maxn;

            *trmvcs = trmvcs1;
            *tdim1 = maxn;
            *tdim2 = 3;
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

%apply (SpiceInt DIM1, SpiceChar INOUT_STRING[ANY])
                          {(SpiceInt lenout, SpiceChar value[256])};
%apply (void RETURN_VOID) {void timdef_c};

extern void timdef_c(
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceInt lenout, SpiceChar value[256]);

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

%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
                          {(SpiceInt lenout, SpiceChar action[256])};
%apply (void RETURN_VOID) {void timout_c};

extern void timout_c(
        SpiceDouble    et,
        ConstSpiceChar *CONST_STRING,
        SpiceInt lenout, SpiceChar action[256]);

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

%apply (SpiceDouble OUT_ARRAY2[ANY][ANY]) {SpiceDouble tipm[3][3]};
%apply (void RETURN_VOID) {void tipbod_c};

extern void tipbod_c(
        ConstSpiceChar *CONST_STRING,
        SpiceInt       body,
        SpiceDouble    et,
        SpiceDouble    tipm[3][3]);

//Vector version
VECTORIZE_s_i_d__dMN(tipbod, tipbod_c, 3, 3)

/***********************************************************************
* -Procedure tisbod_c ( Transformation, inertial state to bodyfixed )
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

%apply (SpiceDouble OUT_ARRAY2[ANY][ANY]) {SpiceDouble tsipm[6][6]};
%apply (void RETURN_VOID) {void tisbod_c};

extern void tisbod_c(
        ConstSpiceChar *CONST_STRING,
        SpiceInt       body,
        SpiceDouble    et,
        SpiceDouble    tsipm[6][6]);

//Vector version
VECTORIZE_s_i_d__dMN(tisbod, tisbod_c, 6, 6)

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

extern char *tkvrsn_c(ConstSpiceChar *CONST_STRING);

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

%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *string};
%apply (SpiceDouble *OUTPUT) {SpiceDouble *sp2000};
%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
                          {(SpiceInt lenout, SpiceChar errmsg[1024])};
%apply (void RETURN_VOID) {void my_tparse_c};

/* Helper function to deal with order of arguments */
%inline %{
    void my_tparse_c(ConstSpiceChar *string,
                     SpiceDouble *sp2000,
                     SpiceInt lenout, SpiceChar errmsg[1024]) {

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

%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *sample};
%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
                  {(SpiceInt lenout, SpiceChar pictur[256])};
%apply (SpiceBoolean *OUTPUT) {SpiceBoolean *ok};
%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
                  {(SpiceInt lenerr, SpiceChar errmsg[1024])};
%apply (void RETURN_VOID) {void my_tpictr_c};

/* Helper function to deal with order of arguments */
%inline %{
    void my_tpictr_c(ConstSpiceChar *sample,
                     SpiceInt lenout, SpiceChar pictur[256],
                     SpiceBoolean *ok,
                     SpiceInt lenerr, SpiceChar errmsg[1024]) {

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

%apply (ConstSpiceDouble IN_ARRAY2[ANY][ANY]) {ConstSpiceDouble matrix[3][3]};
%apply (SpiceDouble RETURN_DOUBLE) {SpiceDouble trace_c};

extern SpiceDouble trace_c(
        ConstSpiceDouble matrix[3][3]);

//Vector version
VECTORIZE_dXY__RETURN_d(trace, trace_c)

/***********************************************************************
* -Procedure trcoff_c  ( Turn tracing off )
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

extern void trcoff_c(void);

/***********************************************************************
* -Procedure trcdep_c ( Traceback depth )
*
* -Abstract
*
*    Return the number of modules in the traceback representation.
*
*    void trcdep_c ( SpiceInt  * depth )
*
* -Brief_I/O
*
*    VARIABLE  I/O  DESCRIPTION
*    --------  ---  ---------------------------------------------------
*    depth      O   The number of modules in the traceback.
***********************************************************************/

%rename (trcdep) trcdep_c;

%apply (void RETURN_VOID) {void trcdep_c};

extern void trcdep_c(
        SpiceInt *OUTPUT);

/***********************************************************************
*-Procedure trcnam_c ( Get module name from traceback )
*
*-Abstract
* 
*   Return the name of the module having the specified position in 
*   the trace representation. The first module to check in is at 
*   index 0. 
* 
*
*   void trcnam_c ( SpiceInt       index,
*                   SpiceInt       namelen,
*                   SpiceChar    * name     )
*
*-Brief_I/O
* 
*   VARIABLE  I/O  DESCRIPTION 
*   --------  ---  -------------------------------------------------- 
*   index      I   The position of the requested module name. 
*   namelen    I   Available space in output name string.
*   name       O   The name at position `index' in the traceback. 
*   SPICE_ERROR_MODLEN
*              P   Maximum length of stored module names.
***********************************************************************/

%rename (trcnam) trcnam_c;

%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
                          {(SpiceInt namelen, SpiceChar name[100])};
%apply (void RETURN_VOID) {void trcnam_c};

extern void trcnam_c(
        SpiceInt index,
        SpiceInt namelen, SpiceChar name[100]);

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

extern void tsetyr_c(
        SpiceInt year);

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

%apply (SpiceDouble RETURN_DOUBLE) {SpiceDouble twopi_c};

extern SpiceDouble twopi_c(void);

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

%apply (ConstSpiceDouble  IN_ARRAY1[ANY]) {ConstSpiceDouble axdef  [3]};
%apply (ConstSpiceDouble  IN_ARRAY1[ANY]) {ConstSpiceDouble plndef [3]};
%apply (SpiceDouble OUT_ARRAY2[ANY][ANY]) {SpiceDouble      mout[3][3]};
%apply (void RETURN_VOID) {void twovec_c};

extern void twovec_c(
        ConstSpiceDouble axdef[3],
        SpiceInt         indexa,
        ConstSpiceDouble plndef[3],
        SpiceInt         indexp,
        SpiceDouble      mout[3][3]);

//Vector version
VECTORIZE_dX_i_dX_i__dMN(twovec, twovec_c, 3, 3)

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

extern SpiceDouble tyear_c(void);

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble v1  [3]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble v2  [3]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble      vout[3]};
%apply (void RETURN_VOID) {void ucrss_c};

extern void ucrss_c(
        ConstSpiceDouble v1  [3],
        ConstSpiceDouble v2  [3],
        SpiceDouble      vout[3]);

//Vector version
VECTORIZE_dX_dX__dN(ucrss, ucrss_c, 3)

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

%apply (SpiceDouble RETURN_DOUBLE) {SpiceDouble unitim_c};

extern SpiceDouble unitim_c(
        SpiceDouble    epoch,
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING);

//Vector version
VECTORIZE_d_2s__RETURN_d(unitim, unitim_c)

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

extern void unload_c(
        ConstSpiceChar *CONST_STRING);

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble v1  [3]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble      vout[3]};
%apply (void RETURN_VOID) {void unorm_c};

extern void unorm_c(
        ConstSpiceDouble v1  [3],
        SpiceDouble      vout[3],
        SpiceDouble      *OUTPUT);

//Vector version
VECTORIZE_dX__dN_d(unorm, unorm_c, 3)

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

%apply (ConstSpiceDouble *IN_ARRAY1, SpiceInt DIM1)
                             {(ConstSpiceDouble *v1, SpiceInt ndim)};
%apply (SpiceDouble **OUT_ARRAY1, int *SIZE1)
                             {(SpiceDouble **v2, int *nd2)};
%apply (SpiceDouble *OUTPUT) {SpiceDouble *vmag};
%apply (void RETURN_VOID)    {void my_unormg_c};

%inline %{
    void my_unormg_c(ConstSpiceDouble *v1, SpiceInt ndim,
                     SpiceDouble     **v2, int      *nd2,
                     SpiceDouble    *vmag) {

        *v2 = NULL;
        *nd2 = 0;

        SpiceDouble *result = my_malloc(ndim, "unormg");
        if (!result) return;

        unormg_c(v1, ndim, result, vmag);
        *v2 = result;
        *nd2 = ndim;
    }

    void my_unormg_nomalloc(ConstSpiceDouble *v1, SpiceInt ndim,
                            SpiceDouble      *v2, int      *nd2,
                            SpiceDouble      *vmag) {

        unormg_c(v1, ndim, v2, vmag);
        *nd2 = ndim;
    }
%}

//Vector version
VECTORIZE_di__di_d(unormg, my_unormg_nomalloc)

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

extern void utc2et_c(
        ConstSpiceChar *CONST_STRING,
        SpiceDouble    *OUTPUT);

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble v1[3]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble v2[3]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble    vout[3]};
%apply (void RETURN_VOID) {void vadd_c};

extern void vadd_c(
        ConstSpiceDouble v1  [3],
        ConstSpiceDouble v2  [3],
        SpiceDouble      vout[3]);

//Vector version
VECTORIZE_dX_dX__dN(vadd, vadd_c, 3)

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

%apply (ConstSpiceDouble *IN_ARRAY1, SpiceInt DIM1)
                          {(ConstSpiceDouble *v1, SpiceInt ndim)};
%apply (ConstSpiceDouble *IN_ARRAY1, int DIM1)
                          {(ConstSpiceDouble *v2, int nd2)};
%apply (SpiceDouble **OUT_ARRAY1, int *SIZE1)
                          {(SpiceDouble **v3, int *nd3)};
%apply (void RETURN_VOID) {void my_vaddg_c};

%inline %{
    void my_vaddg_c(ConstSpiceDouble *v1, SpiceInt ndim,
                    ConstSpiceDouble *v2, int      nd2,
                    SpiceDouble     **v3, int     *nd3) {

        SpiceDouble *result = NULL;

        *v3 = NULL;
        *nd3 = 0;

        if (!my_assert_eq(ndim, nd2, "vaddg",
            "Vector dimension mismatch in vaddg: "
            "vector 1 dimension = #; vector 2 dimension = #")) return;

        result = my_malloc(ndim, "vaddg");
        if (!result) return;

        vaddg_c(v1, v2, ndim, result);
        *v3 = result;
        *nd3 = ndim;
    }

    void my_vaddg_nomalloc(ConstSpiceDouble *v1, SpiceInt ndim,
                    ConstSpiceDouble *v2, int      nd2,
                    SpiceDouble      *v3, int     *nd3) {

        if (!my_assert_eq(ndim, nd2, "vaddg",
            "Vector dimension mismatch in vaddg: "
            "vector 1 dimension = #; vector 2 dimension = #")) return;

        vaddg_c(v1, v2, ndim, v3);
        *nd3 = ndim;
    }
%}

//Vector version
VECTORIZE_di_di__di(vaddg, my_vaddg_nomalloc)

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble v1  [3]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble v2  [3]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble      vout[3]};
%apply (void RETURN_VOID) {void vcrss_c};

extern void vcrss_c(
        ConstSpiceDouble v1  [3],
        ConstSpiceDouble v2  [3],
        SpiceDouble      vout[3]);

//Vector version
VECTORIZE_dX_dX__dN(vcrss, vcrss_c, 3)

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {SpiceDouble v1[3]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {SpiceDouble v2[3]};
%apply (SpiceDouble RETURN_DOUBLE) {SpiceDouble vdist_c};

extern SpiceDouble vdist_c(
        ConstSpiceDouble v1[3],
        ConstSpiceDouble v2[3]);

//Vector version
VECTORIZE_dX_dX__RETURN_d(vdist, vdist_c)

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

%apply (ConstSpiceDouble *IN_ARRAY1, SpiceInt DIM1)
                                    {(ConstSpiceDouble *v1, SpiceInt ndim)}
%apply (ConstSpiceDouble *IN_ARRAY1, int DIM1)
                                    {(ConstSpiceDouble *v2, int nd2)}
%apply (SpiceDouble RETURN_DOUBLE)  {SpiceDouble my_vdistg_c};

%inline %{
    SpiceDouble my_vdistg_c(ConstSpiceDouble *v1, SpiceInt ndim,
                            ConstSpiceDouble *v2, int nd2) {

        if (!my_assert_eq(ndim, nd2, "vdistg",
            "Vector dimension mismatch in vdistg: "
            "vector 1 dimension = #; vector 2 dimension = #")) return NAN;

        return vdistg_c(v1, v2, ndim);
    }
%}

//Vector version
VECTORIZE_di_di__RETURN_d(vdistg, my_vdistg_c)

/***********************************************************************
* -Procedure vdot_c ( Vector dot product, 3 dimensions )
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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble v1[3]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble v2[3]};
%apply (SpiceDouble RETURN_DOUBLE) {SpiceDouble vdot_c};

extern SpiceDouble vdot_c(
        ConstSpiceDouble v1[3],
        ConstSpiceDouble v2[3]);

//Vector version
VECTORIZE_dX_dX__RETURN_d(vdot, vdot_c)

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

%apply (ConstSpiceDouble *IN_ARRAY1, SpiceInt DIM1)
                                   {(ConstSpiceDouble *v1, SpiceInt ndim)};
%apply (ConstSpiceDouble *IN_ARRAY1, int DIM1)
                                   {(ConstSpiceDouble *v2, int nd2)};
%apply (SpiceDouble RETURN_DOUBLE) {SpiceDouble my_vdotg_c};

%inline %{
    SpiceDouble my_vdotg_c(ConstSpiceDouble *v1, SpiceInt ndim,
                           ConstSpiceDouble *v2, int nd2) {

        if (!my_assert_eq(ndim, nd2, "vdotg",
            "Vector dimension mismatch in vdotg: "
            "vector 1 dimension = #; vector 2 dimension = #")) return NAN;

        return vdotg_c(v1, v2, ndim);
    }
%}

//Vector version
VECTORIZE_di_di__RETURN_d(vdotg, my_vdotg_c)

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble vin [3]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble      vout[3]};
%apply (void RETURN_VOID) {void vequ_c};

extern void vequ_c(
        ConstSpiceDouble vin [3],
        SpiceDouble      vout[3]);

//Vector version
VECTORIZE_dX__dN(vequ, vequ_c, 3)

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

%apply (ConstSpiceDouble *IN_ARRAY1, SpiceInt DIM1)
                          {(ConstSpiceDouble *v1, SpiceInt ndim)};
%apply (SpiceDouble **OUT_ARRAY1, int *SIZE1)
                          {(SpiceDouble **v2, int *nd2)};
%apply (void RETURN_VOID) {void my_vequg_c};

%inline %{
    void my_vequg_c(ConstSpiceDouble *v1, SpiceInt ndim,
                    SpiceDouble     **v2, int      *nd2) {

        *v2 = NULL;
        *nd2 = 0;

        SpiceDouble *result = my_malloc(ndim, "vequg");
        if (!result) return;

        vequg_c(v1, ndim, result);
        *v2 = result;
        *nd2 = ndim;
    }

    void my_vequg_nomalloc(ConstSpiceDouble *v1, SpiceInt ndim,
                           SpiceDouble      *v2, int      *nd2) {

        vequg_c(v1, ndim, v2);
        *nd2 = ndim;
    }
%}

//Vector version
VECTORIZE_di__di(vequg, my_vequg_nomalloc)

/***********************************************************************
* -Procedure vhat_c ( "V-Hat", unit vector along V, 3 dimensions )
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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble v1  [3]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble      vout[3]};
%apply (void RETURN_VOID) {void vhat_c};

extern void vhat_c(
        ConstSpiceDouble v1  [3],
        SpiceDouble      vout[3]);

//Vector version
VECTORIZE_dX__dN(vhat, vhat_c, 3)

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

%apply (ConstSpiceDouble *IN_ARRAY1, SpiceInt DIM1)
                          {(ConstSpiceDouble  *v1, SpiceInt ndim)};
%apply (SpiceDouble **OUT_ARRAY1, int *SIZE1)
                          {(SpiceDouble **v2, int *nd2)};
%apply (void RETURN_VOID) {void my_vhatg_c};

%inline %{
    void my_vhatg_c(ConstSpiceDouble  *v1, SpiceInt ndim,
                    SpiceDouble      **v2, int      *nd2) {

        *v2 = NULL;
        *nd2 = 0;

        SpiceDouble *result = my_malloc(ndim, "vhatg");
        if (!result) return;

        vhatg_c(v1, ndim, result);
        *v2 = result;
        *nd2 = ndim;
    }

    void my_vhatg_nomalloc(ConstSpiceDouble *v1, SpiceInt ndim,
                           SpiceDouble      *v2, int      *nd2) {

        vhatg_c(v1, ndim, v2);
        *nd2 = ndim;
    }
%}

//Vector version
VECTORIZE_di__di(vhatg, my_vhatg_nomalloc)

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble v1 [3]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble v2 [3]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble v3 [3]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble      sum[3]};
%apply (void RETURN_VOID) {void vlcom3_c};

extern void vlcom3_c(
        SpiceDouble      a,
        ConstSpiceDouble v1[3],
        SpiceDouble      b,
        ConstSpiceDouble v2[3],
        SpiceDouble      c,
        ConstSpiceDouble v3[3],
        SpiceDouble      sum[3]);

//Vector version
VECTORIZE_d_dX_d_dX_d_dX__dN(vlcom3, vlcom3_c, 3)

/***********************************************************************
* -Procedure vlcom_c ( Vector linear combination, 3 dimensions )
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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble v1 [3]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble v2 [3]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble      sum[3]};
%apply (void RETURN_VOID) {void vlcom_c};

extern void vlcom_c(
        SpiceDouble      a,
        ConstSpiceDouble v1[3],
        SpiceDouble      b,
        ConstSpiceDouble v2[3],
        SpiceDouble      sum[3]);

//Vector version
VECTORIZE_d_dX_d_dX__dN(vlcom, vlcom_c, 3)

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

%apply (ConstSpiceDouble *IN_ARRAY1, SpiceInt DIM1)
                          {(ConstSpiceDouble  *v1, SpiceInt   n)};
%apply (ConstSpiceDouble *IN_ARRAY1, int DIM1)
                          {(ConstSpiceDouble  *v2, int      nd2)};
%apply (SpiceDouble **OUT_ARRAY1, int *SIZE1)
                          {(SpiceDouble **v3, int *nd3)};
%apply (void RETURN_VOID) {void my_vlcomg_c};

%inline %{
    void my_vlcomg_c(SpiceDouble       a,
                     ConstSpiceDouble *v1, SpiceInt  n,
                     SpiceDouble       b,
                     ConstSpiceDouble *v2, int nd2,
                     SpiceDouble     **v3, int *nd3) {

        *v3 = NULL;
        *nd3 = 0;

        if (!my_assert_eq(n, nd2, "vlcomg",
            "Vector dimension mismatch in vlcomg: "
            "vector 1 dimension = #; vector 2 dimension = #")) return;

        SpiceDouble *result = my_malloc(n, "vlcomg");
        if (!result) return;

        vlcomg_c(n, a, v1, b, v2, result);
        *v3 = result;
        *nd3 = n;
    }

    void my_vlcomg_nomalloc(SpiceDouble       a,
                            ConstSpiceDouble *v1, SpiceInt  n,
                            SpiceDouble       b,
                            ConstSpiceDouble *v2, int nd2,
                            SpiceDouble      *v3, int *nd3) {

        if (!my_assert_eq(n, nd2, "vlcomg",
            "Vector dimension mismatch in vlcomg: "
            "vector 1 dimension = #; vector 2 dimension = #")) return;

        vlcomg_c(n, a, v1, b, v2, v3);
        *nd3 = n;
    }
%}

//Vector version
VECTORIZE_d_di_d_di__di(vlcomg, my_vlcomg_nomalloc)

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

%apply (ConstSpiceDouble *IN_ARRAY1, SpiceInt DIM1)
                          {(ConstSpiceDouble  *v1,  SpiceInt ndim)};
%apply (SpiceDouble **OUT_ARRAY1, int *SIZE1)
                          {(SpiceDouble **v2, int *nd2)};
%apply (void RETURN_VOID) {void my_vminug_c};

%inline %{
    void my_vminug_c(ConstSpiceDouble *v1, SpiceInt ndim,
                     SpiceDouble     **v2, int      *nd2) {

        *v2 = NULL;
        *nd2 = 0;

        SpiceDouble *result = my_malloc(ndim, "vminug");
        if (!result) return;

        vminug_c(v1, ndim, result);
        *v2 = result;
        *nd2 = ndim;
    }

    void my_vminug_nomalloc(ConstSpiceDouble *v1, SpiceInt ndim,
                            SpiceDouble      *v2, int      *nd2) {

        vminug_c(v1, ndim, v2);
        *nd2 = ndim;
    }
%}

//Vector version
VECTORIZE_di__di(vminug, my_vminug_nomalloc)

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble v1  [3]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble      vout[3]};
%apply (void RETURN_VOID) {void vminus_c};

extern void vminus_c(
        ConstSpiceDouble v1  [3],
        SpiceDouble      vout[3]);

//Vector version
VECTORIZE_dX__dN(vminus, vminus_c, 3)

/***********************************************************************
* -Procedure vnorm_c ( Vector norm, 3 dimensions )
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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble v1[3]};
%apply (SpiceDouble RETURN_DOUBLE)       {SpiceDouble vnorm_c};

extern SpiceDouble vnorm_c(
        ConstSpiceDouble v1[3]);

//Vector version
VECTORIZE_dX__RETURN_d(vnorm, vnorm_c)

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

%apply (ConstSpiceDouble *IN_ARRAY1, SpiceInt DIM1)
                                   {(ConstSpiceDouble *v1, SpiceInt ndim)};
%apply (SpiceDouble RETURN_DOUBLE) {SpiceDouble vnormg_c};

extern SpiceDouble vnormg_c(
        ConstSpiceDouble *v1, SpiceInt ndim);

//Vector version
VECTORIZE_di__RETURN_d(vnormg, vnormg_c)

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

%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble v[3]};
%apply (void RETURN_VOID) {void vpack_c};

extern void vpack_c(
        SpiceDouble x,
        SpiceDouble y,
        SpiceDouble z,
        SpiceDouble v[3]);

//Vector version
VECTORIZE_3d__dN(vpack, vpack_c, 3)

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble a[3]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble b[3]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble      p[3]};
%apply (void RETURN_VOID) {void vperp_c};

extern void vperp_c(
        ConstSpiceDouble a[3],
        ConstSpiceDouble b[3],
        SpiceDouble      p[3]);

//Vector version
VECTORIZE_dX_dX__dN(vperp, vperp_c, 3)

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble vin[3]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble plane[NPLANE]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble      vout[3]};
%apply (void RETURN_VOID) {void vprjp_c};

extern void vprjp_c(
        ConstSpiceDouble vin[3],
        ConstSpiceDouble plane[NPLANE],
        SpiceDouble      vout[3]);

//Vector version
VECTORIZE_dX_dX__dN(vprjp, vprjp_c, 3)

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble vin[3]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble projpl[NPLANE]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble invpl[NPLANE]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble      vout[3]};
%apply (void RETURN_VOID) {void vprjpi_c};

extern void vprjpi_c(
        ConstSpiceDouble vin[3],
        ConstSpiceDouble projpl[NPLANE],
        ConstSpiceDouble invpl [NPLANE],
        SpiceDouble      vout[3],
        SpiceBoolean     *OUT_BOOLEAN);

//Vector version
VECTORIZE_dX_dX_dX__dN_b(vprjpi, vprjpi_c, 3)

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble a[3]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble b[3]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble      p[3]};
%apply (void RETURN_VOID) {void vproj_c};

extern void vproj_c(
        ConstSpiceDouble a[3],
        ConstSpiceDouble b[3],
        SpiceDouble      p[3]);

//Vector version
VECTORIZE_dX_dX__dN(vproj, vproj_c, 3)

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble v1[3]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble v2[3]};
%apply (SpiceDouble RETURN_DOUBLE) {SpiceDouble vrel_c};

extern SpiceDouble vrel_c(
        ConstSpiceDouble v1[3],
        ConstSpiceDouble v2[3]);

//Vector version
VECTORIZE_dX_dX__RETURN_d(vrel, vrel_c)

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

%apply (ConstSpiceDouble *IN_ARRAY1, SpiceInt DIM1)
                          {(ConstSpiceDouble *v1, SpiceInt ndim)};
%apply (ConstSpiceDouble *IN_ARRAY1, int DIM1)
                          {(ConstSpiceDouble *v2, int nd2)};
%apply (SpiceDouble RETURN_DOUBLE) {void my_vrelg_c};

%inline %{
    SpiceDouble my_vrelg_c(ConstSpiceDouble *v1, SpiceInt ndim,
                           ConstSpiceDouble *v2, int nd2) {

        if (!my_assert_eq(ndim, nd2, "vrelg",
            "Vector dimension mismatch in vrelg: "
            "vector 1 dimension = #; vector 2 dimension = #")) return NAN;


        return vrelg_c(v1, v2, ndim);
    }
%}

//Vector version
VECTORIZE_di_di__RETURN_d(vrelg, my_vrelg_c)

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble v[3]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble axis[3]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble      r[3]};
%apply (void RETURN_VOID) {void vrotv_c};

extern void vrotv_c(
        ConstSpiceDouble v[3],
        ConstSpiceDouble axis [3],
        SpiceDouble      theta,
        SpiceDouble      r[3]);

//Vector version
VECTORIZE_dX_dX_d__dN(vrotv, vrotv_c, 3)

/***********************************************************************
* -Procedure vscl_c ( Vector scaling, 3 dimensions )
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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble v1[3]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble    vout[3]};
%apply (void RETURN_VOID) {void vscl_c};

extern void vscl_c(
        SpiceDouble s,
        ConstSpiceDouble v1[3],
        SpiceDouble    vout[3]);

//Vector version
VECTORIZE_d_dX__dN(vscl, vscl_c, 3)

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

%apply (ConstSpiceDouble *IN_ARRAY1, SpiceInt DIM1)
                          {(ConstSpiceDouble  *v1, SpiceInt ndim)};
%apply (SpiceDouble **OUT_ARRAY1, int *SIZE1)
                          {(SpiceDouble **v2, int *nd2)};
%apply (void RETURN_VOID) {void my_vsclg_c};

%inline %{
    void my_vsclg_c(SpiceDouble      s,
                    ConstSpiceDouble *v1, SpiceInt  ndim,
                    SpiceDouble     **v2, int *nd2) {

        *v2 = NULL;
        *nd2 = 0;

        SpiceDouble *result = my_malloc(ndim, "vsclg");
        if (!result) return;

        vsclg_c(s, v1, ndim, result);
        *v2 = result;
        *nd2 = ndim;
    }

    void my_vsclg_nomalloc(SpiceDouble s,
                    ConstSpiceDouble   *v1, SpiceInt  ndim,
                    SpiceDouble        *v2, int       *nd2) {

        vsclg_c(s, v1, ndim, v2);
        *nd2 = ndim;
    }
%}

//Vector version
VECTORIZE_d_di__di(vsclg, my_vsclg_nomalloc)

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble v1[3]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble v2[3]};
%apply (SpiceDouble RETURN_DOUBLE) {SpiceDouble vsep_c};

extern SpiceDouble vsep_c(
        ConstSpiceDouble v1[3],
        ConstSpiceDouble v2[3]);

//Vector version
VECTORIZE_dX_dX__RETURN_d(vsep, vsep_c)

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

%apply (ConstSpiceDouble *IN_ARRAY1, SpiceInt DIM1)
                                   {(ConstSpiceDouble *v1, SpiceInt ndim)}
%apply (ConstSpiceDouble *IN_ARRAY1, int  DIM1)
                                   {(ConstSpiceDouble *v2, int nd2)}
%apply (SpiceDouble RETURN_DOUBLE) {SpiceDouble my_vsepg_c};

%inline %{
    SpiceDouble my_vsepg_c(ConstSpiceDouble *v1, SpiceInt ndim,
                           ConstSpiceDouble *v2, int nd2) {

        if (!my_assert_eq(ndim, nd2, "vsepg",
            "Vector dimension mismatch in vsepg: "
            "vector 1 dimension = #; vector 2 dimension = #")) return NAN;

        return vsepg_c(v1, v2, ndim);
    }
%}

//Vector version
VECTORIZE_di_di__RETURN_d(vsepg, my_vsepg_c)

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble v1  [3]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble v2  [3]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble      vout[3]};
%apply (void RETURN_VOID) {void vsub_c};

extern void vsub_c(
        ConstSpiceDouble v1[3],
        ConstSpiceDouble v2[3],
        SpiceDouble    vout[3]);

//Vector version
VECTORIZE_dX_dX__dN(vsub, vsub_c, 3)

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

%apply (ConstSpiceDouble *IN_ARRAY1, SpiceInt DIM1)
                          {(ConstSpiceDouble  *v1, SpiceInt ndim)};
%apply (ConstSpiceDouble   *IN_ARRAY1, int DIM1)
                          {(ConstSpiceDouble  *v2, int nd2)};
%apply (SpiceDouble **OUT_ARRAY1, int *SIZE1)
                          {(SpiceDouble **v3, int *nd3)};
%apply (void RETURN_VOID) {void my_vsubg_c};

%inline %{
    void my_vsubg_c(ConstSpiceDouble *v1, SpiceInt ndim,
                    ConstSpiceDouble *v2, int      nd2,
                    SpiceDouble     **v3, int     *nd3) {

        *v3 = NULL;
        *nd3 = 0;

        if (!my_assert_eq(ndim, nd2, "vsubg",
            "Vector dimension mismatch in vsubg: "
            "vector 1 dimension = #; vector 2 dimension = #")) return;

        SpiceDouble *result = my_malloc(ndim, "vsubg");
        if (!result) return;

        vsubg_c(v1, v2, ndim, result);
        *v3 = result;
        *nd3 = ndim;
    }

    void my_vsubg_nomalloc(ConstSpiceDouble *v1, SpiceInt ndim,
                           ConstSpiceDouble *v2, int      nd2,
                           SpiceDouble      *v3, int     *nd3) {

        if (!my_assert_eq(ndim, nd2, "vsubg",
            "Vector dimension mismatch in vsubg: "
            "vector 1 dimension = #; vector 2 dimension = #")) return;

        vsubg_c(v1, v2, ndim, v3);
        *nd3 = ndim;
    }
%}

//Vector version
VECTORIZE_di_di__di(vsubg, my_vsubg_nomalloc)

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]     ) {ConstSpiceDouble v1[3]};
%apply (ConstSpiceDouble IN_ARRAY2[ANY][ANY]) {ConstSpiceDouble matrix[3][3]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]     ) {ConstSpiceDouble v2[3]};
%apply (SpiceDouble RETURN_DOUBLE) {SpiceDouble vtmv_c};

extern SpiceDouble vtmv_c(
        ConstSpiceDouble v1[3],
        ConstSpiceDouble matrix[3][3],
        ConstSpiceDouble v2[3]);

//Vector version
VECTORIZE_dX_dXY_dX__RETURN_d(vtmv, vtmv_c)

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
* v2        I   m-dimensional double precision column vector.
* nrow      I   Number of rows in matrix (number of rows in v1.)
* ncol      I   Number of columns in matrix (number of rows in
*               v2.)
* The function returns the result of (v1**t * matrix * v2 ).
***********************************************************************/

%rename (vtmvg) my_vtmvg_c;

%apply (ConstSpiceDouble *IN_ARRAY1, int DIM1)
                    {(ConstSpiceDouble *v1, int nrow1)};
%apply (ConstSpiceDouble *IN_ARRAY1, int DIM1)
                    {(ConstSpiceDouble *v2, int ncol2)};
%apply (ConstSpiceDouble *IN_ARRAY2, SpiceInt DIM1, SpiceInt DIM2)
                    {(ConstSpiceDouble *matrix, SpiceInt nrow, SpiceInt ncol)};
%apply (SpiceDouble RETURN_DOUBLE) {SpiceDouble my_vtmvg_c};

%inline %{
    SpiceDouble my_vtmvg_c(ConstSpiceDouble *v1, int nrow1,
                           ConstSpiceDouble *matrix, SpiceInt nrow, SpiceInt ncol,
                           ConstSpiceDouble *v2, int ncol2) {

        if (!my_assert_eq(nrow1, nrow, "vtmvg",
            "Array dimension mismatch in vtmvg: "
            "vector 1 dimension = #; matrix rows = #")) return NAN;

        if (!my_assert_eq(ncol2, ncol, "vtmvg",
            "Array dimension mismatch in vtmvg: "
            "column rows = #; vector 2 dimension = #")) return NAN;

        return vtmvg_c(v1, matrix, v2, nrow, ncol);
    }
%}

//Vector version
VECTORIZE_di_dij_dj__RETURN_d(vtmvg, my_vtmvg_c)

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble v[3]};
%apply (void RETURN_VOID) {void vupack_c};

extern void vupack_c(
        ConstSpiceDouble v[3],
        SpiceDouble *OUTPUT,
        SpiceDouble *OUTPUT,
        SpiceDouble *OUTPUT);

// Vector version
VECTORIZE_dX__3d(vupack, vupack_c)

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

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble v[3]};
%apply (SpiceBoolean RETURN_BOOLEAN) {SpiceBoolean vzero_c};

extern SpiceBoolean vzero_c(
        ConstSpiceDouble v[3]);

// Vector version
VECTORIZE_dX__RETURN_b(vzero, vzero_c)

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

%apply (ConstSpiceDouble *IN_ARRAY1, SpiceInt DIM1)
                                     {(ConstSpiceDouble *v, SpiceInt ndim)};
%apply (SpiceBoolean RETURN_BOOLEAN) {SpiceBoolean vzerog_c};

extern SpiceBoolean vzerog_c(
        ConstSpiceDouble *v, SpiceInt ndim);

//Vector version
VECTORIZE_di__RETURN_b(vzerog, vzerog_c)

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

%apply (ConstSpiceDouble IN_ARRAY2[ANY][ANY]) {ConstSpiceDouble xform [6][6]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]     ) {SpiceDouble      eulang[6]};
%apply (SpiceBoolean *OUT_BOOLEAN) {SpiceBoolean *unique};
%apply (void RETURN_VOID) {void xf2eul_c};

extern void xf2eul_c(
        ConstSpiceDouble xform[6][6],
        SpiceInt         axisa,
        SpiceInt         axisb,
        SpiceInt         axisc,
        SpiceDouble      eulang[6],
        SpiceBoolean     *unique);

// Vector version
VECTORIZE_dXY_3d__dN_b(xf2eul, xf2eul_c, 6)

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

%apply (ConstSpiceDouble IN_ARRAY2[ANY][ANY]) {ConstSpiceDouble xform[6][6]};
%apply (SpiceDouble     OUT_ARRAY2[ANY][ANY]) {SpiceDouble      rot  [3][3]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]     ) {SpiceDouble      av   [3]};
%apply (void RETURN_VOID) {void xf2rav_c};

extern void xf2rav_c(
        ConstSpiceDouble xform[6][6],
        SpiceDouble      rot  [3][3],
        SpiceDouble      av   [3]);

// Vector version
VECTORIZE_dXY__dLM_dN(xf2rav, xf2rav_c, 3, 3, 3)

/***********************************************************************
* -Procedure xfmsta_c ( Transform state between coordinate systems )
* 
* -Abstract
*  
*    Transform a state between coordinate systems.
*  
*    void xfmsta_c ( ConstSpiceDouble     input_state[6],
*                    ConstSpiceChar     * input_coord_sys,
*                    ConstSpiceChar     * output_coord_sys,
*                    ConstSpiceChar     * body,
*                    SpiceDouble          output_state[6]  )
*                    
* /*
* 
* -Brief_I/O
*  
*    VARIABLE         I/O  DESCRIPTION
*    --------         ---  -------------------------------------------
*    input_state       I   Input state.
*    input_coord_sys   I   Current (input) coordinate system.
*    output_coord_sys  I   Desired (output) coordinate system.
*    body              I   Name or NAIF ID of body with which
*                          coordinates are associated (if applicable).
*    output_state      O   Converted output state.
***********************************************************************/

%rename (xfmsta) xfmsta_c;

%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble input_state[6]};
%apply (SpiceDouble     OUT_ARRAY1[ANY]) {SpiceDouble output_state[6]};
%apply (void RETURN_VOID) {void xfmsta_c};

extern void xfmsta_c(
        ConstSpiceDouble input_state[6],
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceDouble output_state[6]);

//Vector version
VECTORIZE_dX_3s__dN(xfmsta, xfmsta_c, 6)

/***********************************************************************
* -Procedure xpose6_c ( Transpose a matrix, 6x6 )
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

%apply (ConstSpiceDouble IN_ARRAY2[ANY][ANY]) {ConstSpiceDouble   m1[6][6]};
%apply (SpiceDouble     OUT_ARRAY2[ANY][ANY]) {SpiceDouble      mout[6][6]};
%apply (void RETURN_VOID) {void xpose6_c};

extern void xpose6_c(
        ConstSpiceDouble m1  [6][6],
        SpiceDouble      mout[6][6]);

// Vector version
VECTORIZE_dXY__dMN(xpose6, xpose6_c, 6, 6)

/***********************************************************************
* -Procedure xpose_c ( Transpose a matrix, 3x3 )
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

%apply (ConstSpiceDouble IN_ARRAY2[ANY][ANY]) {ConstSpiceDouble m1 [3][3]};
%apply (SpiceDouble     OUT_ARRAY2[ANY][ANY]) {SpiceDouble     mout[3][3]};
%apply (void RETURN_VOID) {void xpose_c};

extern void xpose_c(
        ConstSpiceDouble m1  [3][3],
        SpiceDouble      mout[3][3]);

// Vector version
VECTORIZE_dXY__dMN(xpose, xpose_c, 3, 3)

/***********************************************************************
* -Procedure xposeg_c ( Transpose a matrix, general )
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

%apply (ConstSpiceDouble *IN_ARRAY2, SpiceInt DIM1, SpiceInt DIM2)
                {(ConstSpiceDouble *matrix, SpiceInt nrow, SpiceInt ncol)};
%apply (SpiceDouble **OUT_ARRAY2, int *SIZE1, int *SIZE2)
                {(SpiceDouble **xposem, int *nrow1,  int *ncol1)};
%apply (void RETURN_VOID) {void my_xposeg_c};

/* Helper function to deal with missing arguments */
%inline %{
    void my_xposeg_c(ConstSpiceDouble *matrix, SpiceInt nrow, SpiceInt  ncol,
                     SpiceDouble     **xposem, int    *nrow1,     int *ncol1) {

        *xposem = NULL;
        *nrow1 = 0;
        *ncol1 = 0;

        SpiceDouble *result = my_malloc(nrow * ncol, "xposeg");
        if (!result) return;

        xposeg_c(matrix, nrow, ncol, result);
        *xposem = result;
        *nrow1 = ncol;
        *ncol1 = nrow;
    }

    void my_xposeg_nomalloc(
                ConstSpiceDouble *matrix, SpiceInt nrow, SpiceInt  ncol,
                SpiceDouble      *xposem, int    *nrow1,     int *ncol1) {

        xposeg_c(matrix, nrow, ncol, xposem);
        *nrow1 = ncol;
        *ncol1 = nrow;
    }
%}

// Vector version
VECTORIZE_dij__dji(xposeg, my_xposeg_nomalloc)

/***********************************************************************
***********************************************************************/
