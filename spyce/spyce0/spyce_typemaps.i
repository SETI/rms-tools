/* -*- C -*-  (not really, but good for syntax highlighting) */

/*******************************************************************************
* This is a major rewrite of numpy.i to support the CSPICE library
* from JPL. Many bugs have been fixed and new typemaps added, supporting
* 1-D and 2-D numeric arrays of fixed or variable dimensions, plus
* character strings, string arrays, and booleans.
*
* See the details in the clearly identified header sections below.
*
* Mark Showalter, PDS Rings Node, SETI Institute, July 2009.
*
* Modified 1/4/12 (MRS) to handle error messages more consistently.
* Modified 3/21/13 (MRS) to define IN_ARRAY3.
* Modified 12/15/17 (MRS) to define OUT_ARRAY3, IN_ARRAY01, IN_ARRAY12, and
*   IN_ARRAY23, OUT_ARRAY23, OUT_ARRAY12, OUT_ARRAY01. Typemaps now support
*   Spice types explicitly. Spice errors now raise appropriate exceptions, not
*   just RuntimeErrors.
*******************************************************************************/

%{
#ifndef SWIG_FILE_WITH_INIT
#  define NO_IMPORT_ARRAY
#endif
#include "stdio.h"
#include <numpy/arrayobject.h>

/* The following code originally appeared in enthought/kiva/agg/src/numeric.i,
 * author unknown.  It was translated from C++ to C by John Hunter.  Bill
 * Spotz has modified it slightly to fix some minor bugs, add some comments
 * and some functionality.
 */

/* Macros to extract array attributes.
 */
#define is_array(a)            ((a) && PyArray_Check((PyArrayObject *)a))
#define array_type(a)          (int)(PyArray_TYPE(a))
#define array_dimensions(a)    (((PyArrayObject *)a)->nd)
#define array_size(a,i)        (((PyArrayObject *)a)->dimensions[i])
#define array_is_contiguous(a) (PyArray_ISCONTIGUOUS(a))

/* Given a PyObject, return a string describing its type.
 */
char* pytype_string(PyObject* py_obj) {
    if (py_obj == NULL          ) return "C NULL value";
    if (PyCallable_Check(py_obj)) return "callable"    ;
    if (PyString_Check(  py_obj)) return "string"      ;
    if (PyInt_Check(     py_obj)) return "int"         ;
    if (PyFloat_Check(   py_obj)) return "float"       ;
    if (PyDict_Check(    py_obj)) return "dict"        ;
    if (PyList_Check(    py_obj)) return "list"        ;
    if (PyTuple_Check(   py_obj)) return "tuple"       ;
    if (PyFile_Check(    py_obj)) return "file"        ;
    if (PyModule_Check(  py_obj)) return "module"      ;
    if (PyInstance_Check(py_obj)) return "instance"    ;

    return "unkown type";
}

/* Given a Numeric typecode, return a string describing the type.
 */
// char* typecode_string(int typecode) {
//     char* type_names[20] = {"char","unsigned byte","byte","short",
//                             "unsigned short","int","unsigned int","long",
//                             "float","double","complex float","complex double",
//                             "object","ntype","unkown"};
//     return type_names[typecode];

char* typecode_string(int typecode) {
    switch (typecode) {
        case PyArray_DOUBLE: return "double";
        case PyArray_INT:    return "int";
        case PyArray_BOOL:   return "bool";
        case PyArray_CHAR:   return "char";
        case PyArray_STRING: return "string";
        case PyArray_BYTE:   return "byte";
        case PyArray_UBYTE:  return "unsigned byte";
        case PyArray_SHORT:  return "short";
        case PyArray_USHORT: return "unsigned short";
        case PyArray_UINT:   return "unsigned int";
        case PyArray_LONG:   return "long";
        case PyArray_FLOAT:  return "float";
        case PyArray_OBJECT: return "object";
        default:             return "unknown";
    }
}

/* Make sure input has correct numeric type.  Allow character and byte
 * to match.  Also allow int and long to match.
 */
int type_match(int actual_type, int desired_type) {
    return PyArray_EquivTypenums(actual_type, desired_type);
}

/* Given a PyObject pointer, cast it to a PyArrayObject pointer if
 * legal.  If not, set the python error string appropriately and
 * return NULL./
 */
PyArrayObject *obj_to_array_no_conversion(PyObject *input, int typecode,
                                                           char *symname)
{
    if (is_array(input)) {
        if (type_match(array_type(input), typecode)) {
            return (PyArrayObject *) input;
        }

        setmsg_c("Array of type \"#\" required in module #; "
                 "array of type \"#\" was given");
        errch_c("#", typecode_string(typecode));
        errch_c("#", symname);
        errch_c("#", typecode_string(array_type(input)));
        sigerr_c("SPICE(INVALIDARRAYTYPE)");
        return NULL;
    }

    setmsg_c("Array of type \"#\" required in module #; "
             "input argument was not an array");
    errch_c("#", typecode_string(typecode));
    errch_c("#", symname);
    sigerr_c("SPICE(INVALIDTYPE)");
    return NULL;
}

/* Convert the given PyObject to a Numeric array with the given
 * typecode.  On Success, return a valid PyArrayObject* with the
 * correct type.  On failure, the python error string will be set and
 * the routine returns NULL.
 */

PyArrayObject* obj_to_array_allow_conversion(PyObject *input, int typecode,
                                             int *is_new_object, char *symname)
{
    if (is_array(input) && type_match(array_type(input), typecode)) {
        *is_new_object = 0;
        return (PyArrayObject *) input;
    }

    PyArrayObject *ary = (PyArrayObject *) PyArray_FromObject(input, typecode,
                                                              0, 0);
    if (ary) {
        *is_new_object = 1;
        return ary;
    }

    *is_new_object = 0;

    if is_array(input) {
        setmsg_c("Array of type \"#\" required in module #; "
                 "array of type \"#\" could not be converted");
        errch_c("#", typecode_string(typecode));
        errch_c("#", symname);
        errch_c("#", typecode_string(array_type(input)));
        sigerr_c("SPICE(INVALIDARRAYTYPE)");
    }
    else {
        setmsg_c("Array of type \"#\" required in module #; "
                 "input argument could not be converted");
        errch_c("#", typecode_string(typecode));
        errch_c("#", symname);
        sigerr_c("SPICE(INVALIDTYPE)");
    }
    return NULL;
}

/* Given a PyArrayObject, check to see if it is contiguous.  If so,
 * return the input pointer and flag it as not a new object.  If it is
 * not contiguous, create a new PyArrayObject using the original data,
 * flag it as a new object and return the pointer.
 */

PyArrayObject *make_contiguous(PyArrayObject *ary, int *is_new_object,
                                                   char *symname)
{
    if (array_is_contiguous(ary)) {
        *is_new_object = 0;
        return ary;
    }

    PyArrayObject *ary2 = (PyArrayObject *) PyArray_ContiguousFromObject(
                                    (PyObject*) ary, array_type(ary), 0, 0);
    if (ary2) {
        *is_new_object = 1;
        return ary2;
    }

    *is_new_object = 0;
    setmsg_c("Contiguous array of type \"#\" required in module #: "
             "input argument could not be made contiguous");
    errch_c("#", typecode_string(array_type(ary)));
    errch_c("#", symname);
    sigerr_c("SPICE(INVALIDARRAYTYPE)");
    return NULL;
}

/* Convert a given PyObject to a contiguous PyArrayObject of the
 * specified type.  If the input object is not a contiguous
 * PyArrayObject, a new one will be created and the new object flag
 * will be set.
 */

PyArrayObject* obj_to_array_contiguous_allow_conversion(PyObject* input,
                                                        int typecode,
                                                        int* is_new_object,
                                                        char *symname)
{
    PyArrayObject* ary1 = obj_to_array_allow_conversion(input, typecode,
                                                        is_new_object,
                                                        symname);
    if (!ary1) return NULL;

    int is_new_object2 = 0;
    PyArrayObject *ary2 = make_contiguous(ary1, &is_new_object2, symname);
    if (!ary2) {
        if (is_new_object) {
            Py_DECREF((PyObject *) ary1);
        }
        is_new_object = 0;
        return NULL;
    }

    if (is_new_object && is_new_object2) {
        Py_DECREF((PyObject *) ary1);
    }

    is_new_object = (is_new_object || is_new_object2);
    return ary2;
}

/*******************************************************************************
*******************************************************************************/

// Global variables
int USE_PYTHON_EXCEPTIONS = 1;  // 1 to turn on; 0 to turn off; 2 for
                                // RuntimeError only.
char SHORT_MESSAGE[ 100] = "";
char LONG_MESSAGE[10000] = "";
char EXPLANATION[ 10000] = "";
char EXCEPTION_MESSAGE[10000] = "";

// flag = 1 uses meaningful exception; flag = 2 uses RuntimeErrors under most
// circumstances.
void set_python_exception_flag(int flag) {
    USE_PYTHON_EXCEPTIONS = flag;
}

int get_python_exception_flag(void) {
    return USE_PYTHON_EXCEPTIONS;
}

char *get_message_after_reset(int option) {
    switch (option) {
        case 0: return SHORT_MESSAGE;
        case 1: return LONG_MESSAGE;
        case 2: return EXPLANATION;
        default: return "";
    }
}

void reset_messages(void) {
    SHORT_MESSAGE[0] = '\0';
    LONG_MESSAGE[0]  = '\0';
    EXPLANATION[0]   = '\0';
}

void flush_traceback(void) {
    // Empty the traceback list
    int depth;
    trcdep_c(&depth);
    for (int k = depth-1; k >= 0; k--) {
        char module[100];
        trcnam_c(k, 100, module);
        chkout_c(module);
    }
}

void flush_traceback_to(char *name) {
    int depth;
    trcdep_c(&depth);
    for (int k = depth-1; k >= 0; k--) {
        char module[100];
        trcnam_c(k, 100, module);
        chkout_c(module);
        if (strcmp(module, name) == 0) return;
    }
}

void pop_traceback() {
    int depth;
    trcdep_c(&depth);
    if (depth) {
        char module[100];
        trcnam_c(depth-1, 100, module);
        chkout_c(module);
    }
}

typedef enum {
    IOError = 0,
    MemoryError = 1,
    TypeError = 2,
    KeyError = 3,
    IndexError = 4,
    ZeroDivisionError = 5,
    RuntimeError = 6,
    ValueError = 7,
} Exception;

Exception select_exception(char *shortmsg) {

    // Decide on the exception class to raise
    const char *ioerrors[] = {
        "SPICE(BADARCHTYPE)",           // IOError
        "SPICE(BADATTRIBUTES)",         // IOError
        "SPICE(BADCOMMENTAREA)",        // IOError
        "SPICE(BADCOORDSYSTEM)",        // IOError
        "SPICE(BADDASCOMMENTAREA)",     // IOError
        "SPICE(BADFILETYPE)",           // IOError
        "SPICE(BADVARNAME)",            // IOError
        "SPICE(BLANKFILENAME)",         // IOError
        "SPICE(CKINSUFFDATA)",          // IOError
        "SPICE(COVERAGEGAP)",           // IOError
        "SPICE(DAFBEGGTEND)",           // IOError
        "SPICE(DAFFRNOTFOUND)",         // IOError
        "SPICE(DAFIMPROPOPEN)",         // IOError
        "SPICE(DAFNEGADDR)",            // IOError
        "SPICE(DAFNOSEARCH)",           // IOError
        "SPICE(DAFOPENFAIL)",           // IOError
        "SPICE(DAFRWCONFLICT)",         // IOError
        "SPICE(DASFILEREADFAILED)",     // IOError
        "SPICE(DASIMPROPOPEN)",         // IOError
        "SPICE(DASNOSUCHHANDLE)",       // IOError
        "SPICE(DASOPENCONFLICT)",       // IOError
        "SPICE(DASOPENFAIL)",           // IOError
        "SPICE(DASRWCONFLICT)",         // IOError
        "SPICE(EKNOSEGMENTS)",          // IOError
        "SPICE(FILECURRENTLYOPEN)",     // IOError
        "SPICE(FILEDOESNOTEXIST)",      // IOError
        "SPICE(FILEISNOTSPK)",          // IOError
        "SPICE(FILENOTFOUND)",          // IOError
        "SPICE(FILEOPENFAILED)",        // IOError
        "SPICE(FILEREADFAILED)",        // IOError
        "SPICE(INQUIREERROR)",          // IOError
        "SPICE(INQUIREFAILED)",         // IOError
        "SPICE(INVALIDARCHTYPE)",       // IOError
        "SPICE(NOCURRENTARRAY)",        // IOError
        "SPICE(NOLOADEDFILES)",         // IOError
        "SPICE(NOSEGMENTSFOUND)",       // IOError
        "SPICE(NOSUCHFILE)",            // IOError
        "SPICE(NOTADAFFILE)",           // IOError
        "SPICE(NOTADASFILE)",           // IOError
        "SPICE(RECURSIVELOADING)",      // IOError
        "SPICE(SPKINSUFFDATA)",         // IOError
        "SPICE(SPKINVALIDOPTION)",      // IOError
        "SPICE(SPKNOTASUBSET)",         // IOError
        "SPICE(SPKTYPENOTSUPP)",        // IOError
        "SPICE(TABLENOTLOADED)",        // IOError
        "SPICE(TOOMANYFILESOPEN)",      // IOError
        "SPICE(UNKNOWNSPKTYPE)",        // IOError
        "SPICE(UNSUPPORTEDBFF)",        // IOError
        "SPICE(UNSUPPORTEDSPEC)",       // IOError
        ""
    };

    const char *memoryerrors[] = {
        "SPICE(ARRAYTOOSMALL)",         // MemoryError
        "SPICE(BADARRAYSIZE)",          // MemoryError
        "SPICE(BOUNDARYTOOBIG)",        // MemoryError
        "SPICE(BUFFEROVERFLOW)",        // MemoryError
        "SPICE(CELLTOOSMALL)",          // MemoryError
        "SPICE(CKTOOMANYFILES)",        // MemoryError
        "SPICE(COLUMNTOOSMALL)",        // MemoryError
        "SPICE(COMMENTTOOLONG)",        // MemoryError
        "SPICE(DAFFTFULL)",             // MemoryError
        "SPICE(DASFTFULL)",             // MemoryError
        "SPICE(DEVICENAMETOOLONG)",     // MemoryError
        "SPICE(EKCOLATTRTABLEFULL)",    // MemoryError
        "SPICE(EKCOLDESCTABLEFULL)",    // MemoryError
        "SPICE(EKFILETABLEFULL)",       // MemoryError
        "SPICE(EKIDTABLEFULL)",         // MemoryError
        "SPICE(EKSEGMENTTABLEFULL)",    // MemoryError
        "SPICE(GRIDTOOLARGE)",          // MemoryError
        "SPICE(INSUFFLEN)",             // MemoryError
        "SPICE(KERNELPOOLFULL)",        // MemoryError
        "SPICE(MALLOCFAILED)",          // MemoryError
        "SPICE(MALLOCFAILURE)",         // MemoryError
        "SPICE(MEMALLOCFAILED)",        // MemoryError
        "SPICE(MESSAGETOOLONG)",        // MemoryError
        "SPICE(NOMOREROOM)",            // MemoryError
        "SPICE(OUTOFROOM)",             // MemoryError
        "SPICE(PCKFILETABLEFULL)",      // MemoryError
        "SPICE(SETEXCESS)",             // MemoryError
        "SPICE(SPKFILETABLEFULL)",      // MemoryError
        "SPICE(TRACEBACKOVERFLOW)",     // MemoryError
        "SPICE(WINDOWEXCESS)",          // MemoryError
        "SPICE(WORKSPACETOOSMALL)",     // MemoryError
        ""
    };

    const char *typeerrors[] = {
        "SPICE(BADVARIABLETYPE)",       // TypeError
        "SPICE(INVALIDTYPE)",           // TypeError
        "SPICE(INVALIDARRAYTYPE)",      // TypeError
        "SPICE(NOTASET)",               // TypeError
        "SPICE(TYPEMISMATCH)",          // TypeError
        "SPICE(WRONGDATATYPE)",         // TypeError
        ""
    };

    const char *keyerrors[] = {
        "SPICE(BODYIDNOTFOUND)",        // KeyError
        "SPICE(BODYNAMENOTFOUND)",      // KeyError
        "SPICE(CANTFINDFRAME)",         // KeyError
        "SPICE(FRAMEIDNOTFOUND)",       // KeyError
        "SPICE(FRAMENAMENOTFOUND)",     // KeyError
        "SPICE(IDCODENOTFOUND)",        // KeyError
        "SPICE(KERNELVARNOTFOUND)",     // KeyError
        "SPICE(NOTRANSLATION)",         // KeyError
        "SPICE(UNKNOWNFRAME)",          // KeyError
        "SPICE(VARIABLENOTFOUND)",      // KeyError
        ""
    };

    const char *indexerrors[] = {
        "SPICE(BADVERTEXINDEX)",        // IndexError
        "SPICE(INDEXOUTOFRANGE)",       // IndexError
        "SPICE(INVALDINDEX)",           // IndexError
        "SPICE(INVALIDINDEX)",          // IndexError
        ""
    };

    const char *zerodivisionerrors[] = {
        "SPICE(DIVIDEBYZERO)",          // ZeroDivisionError
        ""
    };

    const char *runtimeerrors[] = {
        "SPICE(BADINITSTATE)",          // RuntimeError
        "SPICE(BUG)",                   // RuntimeError
        "SPICE(IMMUTABLEVALUE)",        // RuntimeError
        "SPICE(INVALIDSIGNAL)",         // RuntimeError
        "SPICE(NOTINITIALIZED)",        // RuntimeError
        "SPICE(SIGNALFAILED)",          // RuntimeError
        "SPICE(SIGNALFAILURE)",         // RuntimeError
        "SPICE(TRACESTACKEMPTY)",       // RuntimeError
        ""
    };

    const char *valueerrors[] = {
        "SPICE(ARRAYSHAPEMISMATCH)",    // ValueError
        "SPICE(BADACTION)",             // ValueError
        "SPICE(BADAXISLENGTH)",         // ValueError
        "SPICE(BADAXISNUMBERS)",        // ValueError
        "SPICE(BADBORESIGHTSPEC)",      // ValueError
        "SPICE(BADBOUNDARY)",           // ValueError
        "SPICE(BADCOARSEVOXSCALE)",     // ValueError
        "SPICE(BADDEFAULTVALUE)",       // ValueError
        "SPICE(BADDESCRTIMES)",         // ValueError
        "SPICE(BADDIRECTION)",          // ValueError
        "SPICE(BADECCENTRICITY)",       // ValueError
        "SPICE(BADENDPOINTS)",          // ValueError
        "SPICE(BADFINEVOXELSCALE)",     // ValueError
        "SPICE(BADFRAME)",              // ValueError
        "SPICE(BADFRAMECLASS)",         // ValueError
        "SPICE(BADGM)",                 // ValueError
        "SPICE(BADINDEX)",              // ValueError
        "SPICE(BADLATUSRECTUM)",        // ValueError
        "SPICE(BADLIMBLOCUSMIX)",       // ValueError
        "SPICE(BADPARTNUMBER)",         // ValueError
        "SPICE(BADPERIAPSEVALUE)",      // ValueError
        "SPICE(BADPLATECOUNT)",         // ValueError
        "SPICE(BADRADIUS)",             // ValueError
        "SPICE(BADRADIUSCOUNT)",        // ValueError
        "SPICE(BADREFVECTORSPEC)",      // ValueError
        "SPICE(BADSEMIAXIS)",           // ValueError
        "SPICE(BADSTOPTIME)",           // ValueError
        "SPICE(BADTIMEITEM)",           // ValueError
        "SPICE(BADTIMESTRING)",         // ValueError
        "SPICE(BADTIMETYPE)",           // ValueError
        "SPICE(BADVARIABLESIZE)",       // ValueError
        "SPICE(BADVECTOR)",             // ValueError
        "SPICE(BADVERTEXCOUNT)",        // ValueError
        "SPICE(BARYCENTEREPHEM)",       // ValueError
        "SPICE(BLANKMODULENAME)",       // ValueError
        "SPICE(BODIESNOTDISTINCT)",     // ValueError
        "SPICE(BODYANDCENTERSAME)",     // ValueError
        "SPICE(BORESIGHTMISSING)",      // ValueError
        "SPICE(BOUNDARYMISSING)",       // ValueError
        "SPICE(BOUNDSOUTOFORDER)",      // ValueError
        "SPICE(COORDSYSNOTREC)",        // ValueError
        "SPICE(CROSSANGLEMISSING)",     // ValueError
        "SPICE(DEGENERATECASE)",        // ValueError
        "SPICE(DEGENERATEINTERVAL)",    // ValueError
        "SPICE(DEGENERATESURFACE)",     // ValueError
        "SPICE(DEPENDENTVECTORS)",      // ValueError
        "SPICE(NONCONTIGUOUSARRAY)",    // ValueError
        "SPICE(DSKTARGETMISMATCH)",     // ValueError
        "SPICE(DTOUTOFRANGE)",          // ValueError
        "SPICE(DUBIOUSMETHOD)",         // ValueError
        "SPICE(ECCOUTOFRANGE)",         // ValueError
        "SPICE(ELEMENTSTOOSHORT)",      // ValueError
        "SPICE(EMPTYSEGMENT)",          // ValueError
        "SPICE(EMPTYSTRING)",           // ValueError
        "SPICE(FRAMEMISSING)",          // ValueError
        "SPICE(ILLEGALCHARACTER)",      // ValueError
        "SPICE(INCOMPATIBLESCALE)",     // ValueError
        "SPICE(INCOMPATIBLEUNITS)",     // ValueError
        "SPICE(INPUTOUTOFRANGE)",       // ValueError
        "SPICE(INPUTSTOOLARGE)",        // ValueError
        "SPICE(INSUFFICIENTANGLES)",    // ValueError
        "SPICE(INTINDEXTOOSMALL)",      // ValueError
        "SPICE(INTLENNOTPOS)",          // ValueError
        "SPICE(INTOUTOFRANGE)",         // ValueError
        "SPICE(INVALIDACTION)",         // ValueError
        "SPICE(INVALIDARGUMENT)",       // ValueError
        "SPICE(INVALIDARRAYRANK)",      // ValueError
        "SPICE(INVALIDARRAYSHAPE)",     // ValueError
        "SPICE(INVALIDAXISLENGTH)",     // ValueError
        "SPICE(INVALIDCARDINALITY)",    // ValueError
        "SPICE(INVALIDCOUNT)",          // ValueError
        "SPICE(INVALIDDEGREE)",         // ValueError
        "SPICE(INVALIDDESCRTIME)",      // ValueError
        "SPICE(INVALIDDIMENSION)",      // ValueError
        "SPICE(INVALIDELLIPSE)",        // ValueError
        "SPICE(INVALIDENDPNTSPEC)",     // ValueError
        "SPICE(INVALIDEPOCH)",          // ValueError
        "SPICE(INVALIDFORMAT)",         // ValueError
        "SPICE(INVALIDFRAME)",          // ValueError
        "SPICE(INVALIDFRAMEDEF)",       // ValueError
        "SPICE(INVALIDLIMBTYPE)",       // ValueError
        "SPICE(INVALIDLISTITEM)",       // ValueError
        "SPICE(INVALIDLOCUS)",          // ValueError
        "SPICE(INVALIDLONEXTENT)",      // ValueError
        "SPICE(INVALIDMETHOD)",         // ValueError
        "SPICE(INVALIDMSGTYPE)",        // ValueError
        "SPICE(INVALIDNUMINTS)",        // ValueError
        "SPICE(INVALIDNUMRECS)",        // ValueError
        "SPICE(INVALIDOCCTYPE)",        // ValueError
        "SPICE(INVALIDOPERATION)",      // ValueError
        "SPICE(INVALIDOPTION)",         // ValueError
        "SPICE(INVALIDPLANE)",          // ValueError
        "SPICE(INVALIDPOINT)",          // ValueError
        "SPICE(INVALIDRADIUS)",         // ValueError
        "SPICE(INVALIDREFFRAME)",       // ValueError
        "SPICE(INVALIDROLLSTEP)",       // ValueError
        "SPICE(INVALIDSCLKSTRING)",     // ValueError
        "SPICE(INVALIDSCLKTIME)",       // ValueError
        "SPICE(INVALIDSEARCHSTEP)",     // ValueError
        "SPICE(INVALIDSIZE)",           // ValueError
        "SPICE(INVALIDSTARTTIME)",      // ValueError
        "SPICE(INVALIDSTATE)",          // ValueError
        "SPICE(INVALIDSTEP)",           // ValueError
        "SPICE(INVALIDSTEPSIZE)",       // ValueError
        "SPICE(INVALIDSUBTYPE)",        // ValueError
        "SPICE(INVALIDTARGET)",         // ValueError
        "SPICE(INVALIDTERMTYPE)",       // ValueError
        "SPICE(INVALIDTIMEFORMAT)",     // ValueError
        "SPICE(INVALIDTIMESTRING)",     // ValueError
        "SPICE(INVALIDTOL)",            // ValueError
        "SPICE(INVALIDTOLERANCE)",      // ValueError
        "SPICE(INVALIDVALUE)",          // ValueError
        "SPICE(INVALIDVERTEX)",         // ValueError
        "SPICE(MISSINGDATA)",           // ValueError
        "SPICE(MISSINGTIMEINFO)",       // ValueError
        "SPICE(MISSINGVALUE)",          // ValueError
        "SPICE(NAMESDONOTMATCH)",       // ValueError
        "SPICE(NOCLASS)",               // ValueError
        "SPICE(NOCOLUMN)",              // ValueError
        "SPICE(NOFRAME)",               // ValueError
        "SPICE(NOFRAMEINFO)",           // ValueError
        "SPICE(NOINTERCEPT)",           // ValueError
        "SPICE(NOINTERVAL)",            // ValueError
        "SPICE(NONCONICMOTION)",        // ValueError
        "SPICE(NONPOSITIVEMASS)",       // ValueError
        "SPICE(NONPOSITIVESCALE)",      // ValueError
        "SPICE(NONPRINTABLECHARS)",     // ValueError
        "SPICE(NOPARTITION)",           // ValueError
        "SPICE(NOPATHVALUE)",           // ValueError
        "SPICE(NOPRIORITIZATION)",      // ValueError
        "SPICE(NOSEPARATION)",          // ValueError
        "SPICE(NOTADPNUMBER)",          // ValueError
        "SPICE(NOTANINTEGER)",          // ValueError
        "SPICE(NOTAROTATION)",          // ValueError
        "SPICE(NOTINPART)",             // ValueError
        "SPICE(NOTPRINTABLECHARS)",     // ValueError
        "SPICE(NOTRECOGNIZED)",         // ValueError
        "SPICE(NOTSUPPORTED)",          // ValueError
        "SPICE(NULLPOINTER)",           // ValueError
        "SPICE(NUMCOEFFSNOTPOS)",       // ValueError
        "SPICE(NUMERICOVERFLOW)",       // ValueError
        "SPICE(NUMPARTSUNEQUAL)",       // ValueError
        "SPICE(NUMSTATESNOTPOS)",       // ValueError
        "SPICE(PLATELISTTOOSMALL)",     // ValueError
        "SPICE(POINTNOTONSURFACE)",     // ValueError
        "SPICE(POINTONZAXIS)",          // ValueError
        "SPICE(PTRARRAYTOOSMALL)",      // ValueError
        "SPICE(REFANGLEMISSING)",       // ValueError
        "SPICE(REFVECTORMISSING)",      // ValueError
        "SPICE(SCLKTRUNCATED)",         // ValueError
        "SPICE(SEGIDTOOLONG)",          // ValueError
        "SPICE(SHAPEMISSING)",          // ValueError
        "SPICE(SHAPENOTSUPPORTED)",     // ValueError
        "SPICE(SINGULARMATRIX)",        // ValueError
        "SPICE(STRINGTOOLSHORT)",       // ValueError
        "SPICE(STRINGTOOSHORT)",        // ValueError
        "SPICE(SUBPOINTNOTFOUND)",      // ValueError
        "SPICE(TARGETMISMATCH)",        // ValueError
        "SPICE(TIMECONFLICT)",          // ValueError
        "SPICE(TIMESDONTMATCH)",        // ValueError
        "SPICE(TIMESOUTOFORDER)",       // ValueError
        "SPICE(TOOFEWPACKETS)",         // ValueError
        "SPICE(TOOFEWPLATES)",          // ValueError
        "SPICE(TOOFEWSTATES)",          // ValueError
        "SPICE(TOOFEWVERTICES)",        // ValueError
        "SPICE(TOOMANYPARTS)",          // ValueError
        "SPICE(UNDEFINEDFRAME)",        // ValueError
        "SPICE(UNITSMISSING)",          // ValueError
        "SPICE(UNITSNOTREC)",           // ValueError
        "SPICE(UNKNOWNCOMPARE)",        // ValueError
        "SPICE(UNKNOWNSYSTEM)",         // ValueError
        "SPICE(UNMATCHENDPTS)",         // ValueError
        "SPICE(UNORDEREDTIMES)",        // ValueError
        "SPICE(UNPARSEDTIME)",          // ValueError
        "SPICE(VALUEOUTOFRANGE)",       // ValueError
        "SPICE(VECTORTOOBIG)",          // ValueError
        "SPICE(WINDOWTOOSMALL)",        // ValueError
        "SPICE(YEAROUTOFRANGE)",        // ValueError
        "SPICE(ZEROBOUNDSEXTENT)",      // ValueError
        "SPICE(ZEROLENGTHCOLUMN)",      // ValueError
        "SPICE(ZEROPOSITION)",          // ValueError
        "SPICE(ZEROQUATERNION)",        // ValueError
        "SPICE(ZEROVECTOR)",            // ValueError
        "SPICE(ZEROVELOCITY)",          // ValueError
        ""
    };

    const char **errors[] = {
        ioerrors,
        memoryerrors,
        typeerrors,
        keyerrors,
        indexerrors,
        zerodivisionerrors,
        runtimeerrors,
        valueerrors,
    };

    // RuntimeErrors only
    if (USE_PYTHON_EXCEPTIONS == 2) {
        return RuntimeError;
    }

    // Find the short error message in one of the lists
    int errtype = 0;
    for (errtype = 0; errtype < 8; errtype++) {
        const char **these_errors = errors[errtype];
        for (int imsg = 0; these_errors[imsg][0] != '\0'; imsg++) {
            if (strcmp(shortmsg, these_errors[imsg]) == 0) {
                return (Exception) errtype;
            }
        }
    }

    return RuntimeError;
}

char *get_exception_message(char *name) {

    // Save the messages globally
    getmsg_c("SHORT",     100, SHORT_MESSAGE);
    getmsg_c("LONG",    10000, LONG_MESSAGE );
    getmsg_c("EXPLAIN", 10000, EXPLANATION  );

    // Create the exception message
    getmsg_c("SHORT", 100, EXCEPTION_MESSAGE);
    strcat(EXCEPTION_MESSAGE, " -- ");
    if (name[0]) {
        strcat(EXCEPTION_MESSAGE, name);
        strcat(EXCEPTION_MESSAGE, " -- ");
    }
    strcat(EXCEPTION_MESSAGE, LONG_MESSAGE);

    return EXCEPTION_MESSAGE;
}

#define GE0(x) ((x) < 0 ? 0 : (x))
#define GE1(x) ((x) < 1 ? 1 : (x))
#define GE2(x) ((x) < 2 ? 2 : (x))

%}

%define TEST_FOR_EXCEPTION
{
    if (failed_c() && USE_PYTHON_EXCEPTIONS) {
        chkin_c("$symname");
        char *message = get_exception_message("$symname");
        Exception errtype = select_exception(SHORT_MESSAGE);

        switch (errtype) {
            case IOError:
                PyErr_SetString(PyExc_IOError, message);
                break;

            case MemoryError:
                PyErr_SetString(PyExc_MemoryError, message);
                break;

            case TypeError:
                PyErr_SetString(PyExc_TypeError, message);
                break;

            case KeyError:
                PyErr_SetString(PyExc_KeyError, message);
                break;

            case IndexError:
                PyErr_SetString(PyExc_IndexError, message);
                break;

            case ZeroDivisionError:
                PyErr_SetString(PyExc_ZeroDivisionError, message);
                break;

            case RuntimeError:
                PyErr_SetString(PyExc_RuntimeError, message);
                break;

            case ValueError:
                PyErr_SetString(PyExc_ValueError, message);
                break;

            default:
                PyErr_SetString(PyExc_RuntimeError, message);
                break;
        }

        chkout_c("$symname");
        reset_c();
        SWIG_fail;
    }
}
%enddef

%define RAISE_SIGERR_EXCEPTION
{
    if (USE_PYTHON_EXCEPTIONS) {
        int depth;
        char symname[100];

        trcdep_c(&depth);
        if (depth > 0) {
            trcnam_c(depth-1, 100, symname);
        }
        else {
            symname[0] = '\0';
        }

        char *message = get_exception_message(symname);
        Exception errtype = select_exception(SHORT_MESSAGE);

        switch (errtype) {
            case IOError:
                PyErr_SetString(PyExc_IOError, message);
                break;

            case MemoryError:
                PyErr_SetString(PyExc_MemoryError, message);
                break;

            case TypeError:
                PyErr_SetString(PyExc_TypeError, message);
                break;

            case KeyError:
                PyErr_SetString(PyExc_KeyError, message);
                break;

            case IndexError:
                PyErr_SetString(PyExc_IndexError, message);
                break;

            case ZeroDivisionError:
                PyErr_SetString(PyExc_ZeroDivisionError, message);
                break;

            case RuntimeError:
                PyErr_SetString(PyExc_RuntimeError, message);
                break;

            case ValueError:
                PyErr_SetString(PyExc_ValueError, message);
                break;

            default:
                PyErr_SetString(PyExc_RuntimeError, message);
                break;
        }

        pop_traceback();
        reset_c();
        SWIG_fail;
    }
    else {
        pop_traceback();
    }
}
%enddef

%define TEST_MALLOCFAILURE(arg, force)
{
    if (!(arg)) {
        chkin_c("$symname");
        setmsg_c("Failed to allocate memory");
        sigerr_c("SPICE(MALLOCFAILURE)");
        chkout_c("$symname");

        if (USE_PYTHON_EXCEPTIONS == 2) {
            PyErr_SetString(PyExc_RuntimeError,
                            get_exception_message("$symname"));
            reset_c();
            SWIG_fail;
        }
        else if (USE_PYTHON_EXCEPTIONS || (force)) {
            PyErr_SetString(PyExc_MemoryError,
                            get_exception_message("$symname"));
            reset_c();
            SWIG_fail;
        }
    }
}
%enddef

%define TEST_INVALIDARRAYRANK(pyarr, required_rank)
{
    if ((pyarr) && ((pyarr)->nd != (required_rank))) {
        chkin_c("$symname");
        setmsg_c("Invalid array rank #; # is required");
        errint_c("#", (int) ((pyarr)->nd));
        errint_c("#", (int) (required_rank));
        sigerr_c("SPICE(INVALIDARRAYRANK)");
        chkout_c("$symname");

        if (USE_PYTHON_EXCEPTIONS == 2) {
            PyErr_SetString(PyExc_RuntimeError,
                            get_exception_message("$symname"));
            reset_c();
            SWIG_fail;
        }
        else if (USE_PYTHON_EXCEPTIONS) {
            PyErr_SetString(PyExc_ValueError,
                            get_exception_message("$symname"));
            reset_c();
            SWIG_fail;
        }

        Py_DECREF(pyarr);
        pyarr = NULL;
    }
}
%enddef

%define TEST_INVALIDARRAYRANK_OR(pyarr, option1, option2)
{
    if ((pyarr) && ((pyarr)->nd != (option1)) &&
                   ((pyarr)->nd != (option2))) {
        chkin_c("$symname");
        setmsg_c("Invalid array rank # in module #; # or # is required");
        errint_c("#", (int) (pyarr)->nd);
        errch_c( "#", "$symname");
        errint_c("#", (int) (option1));
        errint_c("#", (int) (option2));
        sigerr_c("SPICE(INVALIDARRAYRANK)");
        chkout_c("$symname");

        if (USE_PYTHON_EXCEPTIONS == 2) {
            PyErr_SetString(PyExc_RuntimeError,
                            get_exception_message("$symname"));
            reset_c();
            SWIG_fail;
        }
        else if (USE_PYTHON_EXCEPTIONS) {
            PyErr_SetString(PyExc_ValueError,
                            get_exception_message("$symname"));
            reset_c();
            SWIG_fail;
        }

        Py_DECREF(pyarr);
        pyarr = NULL;
    }
}
%enddef

%define TEST_INVALIDARRAYSHAPE_1D(pyarr, req0)
{
    if ((pyarr) && ((pyarr)->dimensions[0] != (req0))) {
        chkin_c("$symname");
        setmsg_c("Invalid array shape (#) in module #; (#) is required");
        errint_c("#", (int) (pyarr)->dimensions[0]);
        errch_c( "#", "$symname");
        errint_c("#", (int) (req0));
        sigerr_c("SPICE(INVALIDARRAYSHAPE)");
        chkout_c("$symname");

        if (USE_PYTHON_EXCEPTIONS == 2) {
            PyErr_SetString(PyExc_RuntimeError,
                            get_exception_message("$symname"));
            reset_c();
            SWIG_fail;
        }
        else if (USE_PYTHON_EXCEPTIONS) {
            PyErr_SetString(PyExc_ValueError,
                            get_exception_message("$symname"));
            reset_c();
            SWIG_fail;
        }

        Py_DECREF(pyarr);
        pyarr = NULL;
    }
}
%enddef

%define TEST_INVALIDARRAYSHAPE_2D(pyarr, req0, req1)
{
    if ((pyarr) && ((pyarr)->dimensions[0] != (req0) ||
                    (pyarr)->dimensions[1] != (req1))) {
        chkin_c("$symname");
        setmsg_c("Invalid array shape (#,#) in module #; (#,#) is required");
        errint_c("#", (int) (pyarr)->dimensions[0]);
        errint_c("#", (int) (pyarr)->dimensions[1]);
        errch_c( "#", "$symname");
        errint_c("#", (int) (req0));
        errint_c("#", (int) (req1));
        sigerr_c("SPICE(INVALIDARRAYSHAPE)");
        chkout_c("$symname");

        if (USE_PYTHON_EXCEPTIONS == 2) {
            PyErr_SetString(PyExc_RuntimeError,
                            get_exception_message("$symname"));
            reset_c();
            SWIG_fail;
        }
        else if (USE_PYTHON_EXCEPTIONS) {
            PyErr_SetString(PyExc_ValueError,
                            get_exception_message("$symname"));
            reset_c();
            SWIG_fail;
        }

        Py_DECREF(pyarr);
        pyarr = NULL;
    }
}
%enddef

%define TEST_INVALIDARRAYSHAPE_x2D(pyarr, req1)
{
    if ((pyarr) && ((pyarr)->dimensions[1] != (req1))) {
        chkin_c("$symname");
        setmsg_c("Invalid array shape (#,#) in module #; (*,#) is required");
        errint_c("#", (int) (pyarr)->dimensions[0]);
        errint_c("#", (int) (pyarr)->dimensions[1]);
        errch_c( "#", "$symname");
        errint_c("#", (int) (req1));
        sigerr_c("SPICE(INVALIDARRAYSHAPE)");
        chkout_c("$symname");

        if (USE_PYTHON_EXCEPTIONS == 2) {
            PyErr_SetString(PyExc_RuntimeError,
                            get_exception_message("$symname"));
            reset_c();
            SWIG_fail;
        }
        else if (USE_PYTHON_EXCEPTIONS) {
            PyErr_SetString(PyExc_ValueError,
                            get_exception_message("$symname"));
            reset_c();
            SWIG_fail;
        }

        Py_DECREF(pyarr);
        pyarr = NULL;
    }
}
%enddef

%define TEST_INVALIDARRAYSHAPE_x3D(pyarr, req1, req2)
{
    if ((pyarr) && ((pyarr)->dimensions[1] != (req1) ||
                    (pyarr)->dimensions[2] != (req2))) {
        chkin_c("$symname");
        setmsg_c("Invalid array shape (#,#,#) in module #; (*,#,#) is required");
        errint_c("#", (int) (pyarr)->dimensions[0]);
        errint_c("#", (int) (pyarr)->dimensions[1]);
        errint_c("#", (int) (pyarr)->dimensions[2]);
        errch_c( "#", "$symname");
        errint_c("#", (int) (req1));
        errint_c("#", (int) (req2));
        sigerr_c("SPICE(INVALIDARRAYSHAPE)");
        chkout_c("$symname");

        if (USE_PYTHON_EXCEPTIONS == 2) {
            PyErr_SetString(PyExc_RuntimeError,
                            get_exception_message("$symname"));
            reset_c();
            SWIG_fail;
        }
        else if (USE_PYTHON_EXCEPTIONS) {
            PyErr_SetString(PyExc_ValueError,
                            get_exception_message("$symname"));
            reset_c();
            SWIG_fail;
        }

        Py_DECREF(pyarr);
        pyarr = NULL;
    }
}
%enddef

%define TEST_NONCONTIGUOUSARRAY(pyarr, force)
{
    if ((pyarr) && !array_is_contiguous(pyarr)) {
        chkin_c("$symname");
        setmsg_c("Contiguous array required in module #: "
                 "input/output array is not contiguous");
        errch_c("#", "$symname");
        sigerr_c("SPICE(NONCONTIGUOUSARRAY)");
        chkout_c("$symname");

        if (USE_PYTHON_EXCEPTIONS == 2) {
            PyErr_SetString(PyExc_RuntimeError,
                            get_exception_message("$symname"));
            reset_c();
            SWIG_fail;
        }
        else if (USE_PYTHON_EXCEPTIONS || (force)) {
            PyErr_SetString(PyExc_ValueError,
                            get_exception_message("$symname"));
            reset_c();
            SWIG_fail;
        }

        Py_DECREF(pyarr);
        pyarr = NULL;
    }
}
%enddef

%define TEST_INVALIDTYPE_STRING_SEQUENCE(arg)
{
    if (!PySequence_Check(arg)) {
        chkin_c("$symname");
        setmsg_c("Input argument must be a sequence of strings in module #");
        errch_c( "#", "$symname");
        sigerr_c("SPICE(INVALIDTYPE)");
        chkout_c("$symname");

        if (USE_PYTHON_EXCEPTIONS == 2) {
            PyErr_SetString(PyExc_RuntimeError,
                            get_exception_message("$symname"));
            reset_c();
            SWIG_fail;
        }
        else if (USE_PYTHON_EXCEPTIONS) {
            PyErr_SetString(PyExc_TypeError,
                            get_exception_message("$symname"));
            reset_c();
            SWIG_fail;
        }

        Py_DECREF(arg);
        arg = NULL;
    }

    if (arg) {
        for (int i = 0; i < PySequence_Length(arg); i++) {
            PyObject *obj = PySequence_GetItem(arg, i);
            if (!PyString_Check(obj)) {
                chkin_c("$symname");
                setmsg_c("Input argument must be a sequence of strings "
                         "in module #");
                errch_c( "#", "$symname");
                sigerr_c("SPICE(INVALIDTYPE)");
                chkout_c("$symname");

                if (USE_PYTHON_EXCEPTIONS == 2) {
                    PyErr_SetString(PyExc_RuntimeError,
                                    get_exception_message("$symname"));
                    reset_c();
                    SWIG_fail;
                }
                else if (USE_PYTHON_EXCEPTIONS) {
                    PyErr_SetString(PyExc_TypeError,
                                    get_exception_message("$symname"));
                    reset_c();
                    SWIG_fail;
                }

                Py_DECREF(arg);
                arg = NULL;
            }
        }
    }
}
%enddef

/*******************************************************************************
* 1-D numeric typemaps for input
*
* This family of typemaps allows Python sequences and Numpy 1-D arrays to be
* read as arrays in C functions.
*
* If the size of the array is fixed and can be specified in the SWIG interface:
*       (type IN_ARRAY1[ANY])
*       (type IN_ARRAY1[ANY], int DIM1)
*       (int DIM1, type IN_ARRAY1[ANY])
* In these cases, an error condition will be raised if the dimension of the
* structure passed from Python does not match that specified in braces within
* the C function call.
*
* If the size of the array is defined by the Python structure:
*       (type *IN_ARRAY1, int DIM1)
*       (int DIM1, type *IN_ARRAY1)
* In these cases, there is no limit on the number of elements that can be passed
* to the C function. Internal memory is allocated as needed based on the size of
* the array passed from Python.
*
* If a scalar should be shaped into an array of shape (1,):
*       (type *IN_ARRAY01, int DIM1)
* If a scalar is given, then DIM1 = 0.
*******************************************************************************/

%define TYPEMAP_IN(Type, Typecode) // Use to fill in numeric types below

/*******************************************************
* (Type IN_ARRAY1[ANY])
*******************************************************/

%typemap(in)
    (Type IN_ARRAY1[ANY])                                       // PATTERN
            (PyArrayObject* pyarr=NULL, int is_new_object=0)
{
//      (Type IN_ARRAY1[ANY])

    pyarr = obj_to_array_contiguous_allow_conversion($input, Typecode,
                                                     &is_new_object,
                                                     "$symname");
    TEST_FOR_EXCEPTION;
    TEST_INVALIDARRAYRANK(pyarr, 1);
    TEST_INVALIDARRAYSHAPE_1D(pyarr, $1_dim0);

    if (!pyarr) {
        npy_intp dims[] = {$1_dim0};
        pyarr = (PyArrayObject *) PyArray_SimpleNew(1, dims, Typecode);
        is_new_object = 1;
    }
    TEST_MALLOCFAILURE(pyarr,1);

    $1 = (Type *) pyarr->data;                                  // ARRAY
//  $2 = (int) pyarr->dimensions[0];                            // DIM1
}

/*******************************************************
* (Type IN_ARRAY1[ANY], int DIM1)
*******************************************************/

%typemap(in)
    (Type IN_ARRAY1[ANY], int DIM1)                             // PATTERN
        (PyArrayObject* pyarr=NULL, int is_new_object=0),
    (Type IN_ARRAY1[ANY], SpiceInt DIM1)                        // PATTERN
        (PyArrayObject* pyarr=NULL, int is_new_object=0)
{
//      (Type IN_ARRAY1[ANY], int DIM1)

    pyarr = obj_to_array_contiguous_allow_conversion($input, Typecode,
                                                     &is_new_object,
                                                     "$symname");
    TEST_FOR_EXCEPTION;
    TEST_INVALIDARRAYRANK(pyarr, 1);
    TEST_INVALIDARRAYSHAPE_1D(pyarr, $1_dim0);

    if (!pyarr) {
        npy_intp dims[] = {$1_dim0};
        pyarr = (PyArrayObject *) PyArray_SimpleNew(1, dims, Typecode);
        is_new_object = 1;
    }
    TEST_MALLOCFAILURE(pyarr,1);

    $1 = (Type *) pyarr->data;                                  // ARRAY
    $2 = (int) pyarr->dimensions[0];                            // DIM1
}

/*******************************************************
* (int DIM1, Type IN_ARRAY1[ANY])
*******************************************************/

%typemap(in)
    (int DIM1, Type IN_ARRAY1[ANY])                             // PATTERN
        (PyArrayObject* pyarr=NULL, int is_new_object=0),
    (SpiceInt DIM1, Type IN_ARRAY1[ANY])                        // PATTERN
        (PyArrayObject* pyarr=NULL, int is_new_object=0)
{
//      (int DIM1, Type IN_ARRAY1[ANY])

    pyarr = obj_to_array_contiguous_allow_conversion($input, Typecode,
                                                     &is_new_object,
                                                     "$symname");
    TEST_FOR_EXCEPTION;
    TEST_INVALIDARRAYRANK(pyarr, 1);
    TEST_INVALIDARRAYSHAPE_1D(pyarr, $2_dim0);

    if (!pyarr) {
        npy_intp dims[] = {$2_dim0};
        pyarr = (PyArrayObject *) PyArray_SimpleNew(1, dims, Typecode);
        is_new_object = 1;
    }
    TEST_MALLOCFAILURE(pyarr,1);

    $2 = (Type *) pyarr->data;                                  // ARRAY
    $1 = (int) pyarr->dimensions[0];                            // DIM1
}

/*******************************************************
* (Type *IN_ARRAY1, int DIM1)
*******************************************************/

%typemap(in)
    (Type *IN_ARRAY1, int DIM1)                                 // PATTERN
        (PyArrayObject* pyarr=NULL, int is_new_object=0),
    (Type *IN_ARRAY1, SpiceInt DIM1)                            // PATTERN
        (PyArrayObject* pyarr=NULL, int is_new_object=0)
{
//      (Type *IN_ARRAY1, int DIM1)

    pyarr = obj_to_array_contiguous_allow_conversion($input, Typecode,
                                                     &is_new_object,
                                                     "$symname");
    TEST_FOR_EXCEPTION;
    TEST_INVALIDARRAYRANK(pyarr, 1);

    if (!pyarr) {
        npy_intp dims[] = {1};
        pyarr = (PyArrayObject *) PyArray_SimpleNew(1, dims, Typecode);
        is_new_object = 1;
    }
    TEST_MALLOCFAILURE(pyarr,1);

    $1 = (Type *) pyarr->data;                                  // ARRAY
    $2 = (int) pyarr->dimensions[0];                            // DIM1
}

/*******************************************************
* (int DIM1, Type *IN_ARRAY1)
*******************************************************/

%typemap(in)
    (int DIM1, Type *IN_ARRAY1)                                 // PATTERN
        (PyArrayObject* pyarr=NULL, int is_new_object=0),
    (SpiceInt DIM1, Type *IN_ARRAY1)                            // PATTERN
        (PyArrayObject* pyarr=NULL, int is_new_object=0)
{
//      (int DIM1, Type *IN_ARRAY1)

    pyarr = obj_to_array_contiguous_allow_conversion($input, Typecode,
                                                     &is_new_object,
                                                     "$symname");
    TEST_FOR_EXCEPTION;
    TEST_INVALIDARRAYRANK(pyarr, 1);

    if (!pyarr) {
        npy_intp dims[] = {1};
        pyarr = (PyArrayObject *) PyArray_SimpleNew(1, dims, Typecode);
        is_new_object = 1;
    }
    TEST_MALLOCFAILURE(pyarr,1);

    $2 = (Type *) pyarr->data;                                  // ARRAY
    $1 = (int) pyarr->dimensions[0];                            // DIM1
}

/*******************************************************
* (Type *IN_ARRAY01, int DIM1)
*******************************************************/

%typemap(in)
    (Type *IN_ARRAY01, int DIM1)                                // PATTERN
        (PyArrayObject* pyarr=NULL, int is_new_object=0),
    (Type *IN_ARRAY01, SpiceInt DIM1)                           // PATTERN
        (PyArrayObject* pyarr=NULL, int is_new_object=0)
{
//      (Type *IN_ARRAY01, int DIM1)

    pyarr = obj_to_array_contiguous_allow_conversion($input, Typecode,
                                                     &is_new_object,
                                                     "$symname");
    TEST_FOR_EXCEPTION;
    TEST_INVALIDARRAYRANK_OR(pyarr, 0, 1);

    if (!pyarr) {
        npy_intp dims[] = {1};
        pyarr = (PyArrayObject *) PyArray_SimpleNew(1, dims, Typecode);
        is_new_object = 1;
    }
    TEST_MALLOCFAILURE(pyarr,1);

    if (pyarr->nd == 0) {
        $1 = (Type *) pyarr->data;                              // ARRAY
        $2 = 0;                                                 // DIM1
    }
    else {
        $1 = (Type *) pyarr->data;                              // ARRAY
        $2 = (int) pyarr->dimensions[0];                        // DIM1
    }
}

/*******************************************************
* %typemap(check)
* %typemap(argout)
* %typemap(freearg)
*******************************************************/

%typemap(check)
    (Type IN_ARRAY1[ANY]),
    (Type IN_ARRAY1[ANY], int DIM1),
    (Type IN_ARRAY1[ANY], SpiceInt DIM1),
    (int DIM1, Type IN_ARRAY1[ANY]),
    (SpiceInt DIM1, Type IN_ARRAY1[ANY]),
    (Type *IN_ARRAY1, int DIM1),
    (Type *IN_ARRAY1, SpiceInt DIM1),
    (int DIM1, Type *IN_ARRAY1),
    (SpiceInt DIM1, Type *IN_ARRAY1),
    (Type *IN_ARRAY01, int DIM1),
    (Type *IN_ARRAY01, SpiceInt DIM1)
{}

%typemap(argout)
    (Type IN_ARRAY1[ANY]),
    (Type IN_ARRAY1[ANY], int DIM1),
    (Type IN_ARRAY1[ANY], SpiceInt DIM1),
    (int DIM1, Type IN_ARRAY1[ANY]),
    (SpiceInt DIM1, Type IN_ARRAY1[ANY]),
    (Type *IN_ARRAY1, int DIM1),
    (Type *IN_ARRAY1, SpiceInt DIM1),
    (int DIM1, Type *IN_ARRAY1),
    (SpiceInt DIM1, Type *IN_ARRAY1),
    (Type *IN_ARRAY01, int DIM1),
    (Type *IN_ARRAY01, SpiceInt DIM1)
{}

%typemap(freearg)
    (Type IN_ARRAY1[ANY]),
    (Type IN_ARRAY1[ANY], int DIM1),
    (Type IN_ARRAY1[ANY], SpiceInt DIM1),
    (int DIM1, Type IN_ARRAY1[ANY]),
    (SpiceInt DIM1, Type IN_ARRAY1[ANY]),
    (Type *IN_ARRAY1, int DIM1),
    (Type *IN_ARRAY1, SpiceInt DIM1),
    (int DIM1, Type *IN_ARRAY1),
    (SpiceInt DIM1, Type *IN_ARRAY1),
    (Type *IN_ARRAY01, int DIM1),
    (Type *IN_ARRAY01, SpiceInt DIM1)
{
//      (Type ...IN_ARRAY1[ANY]...)

    if (is_new_object$argnum && pyarr$argnum) Py_DECREF(pyarr$argnum);
}

/*******************************************************
* Now apply to all data types
*******************************************************/

%enddef

// Define concrete examples of the TYPEMAP_IN1 macros
TYPEMAP_IN(char,             PyArray_CHAR  )
TYPEMAP_IN(SpiceChar,        PyArray_CHAR  )
TYPEMAP_IN(unsigned char,    PyArray_UBYTE )
TYPEMAP_IN(signed char,      PyArray_SBYTE )
TYPEMAP_IN(short,            PyArray_SHORT )
TYPEMAP_IN(int,              PyArray_INT   )
TYPEMAP_IN(SpiceInt,         PyArray_INT   )
TYPEMAP_IN(ConstSpiceInt,    PyArray_INT   )
TYPEMAP_IN(SpiceBoolean,     PyArray_INT   )
TYPEMAP_IN(long,             PyArray_LONG  )
TYPEMAP_IN(float,            PyArray_FLOAT )
TYPEMAP_IN(double,           PyArray_DOUBLE)
TYPEMAP_IN(SpiceDouble,      PyArray_DOUBLE)
TYPEMAP_IN(ConstSpiceDouble, PyArray_DOUBLE)
TYPEMAP_IN(PyObject,         PyArray_OBJECT)

#undef TYPEMAP_IN

/*******************************************************************************
* 2-D numeric typemaps for input
*
* This family of typemaps allows Python 2-D sequences and Numpy 2-D arrays to be
* read as arrays in C functions.
*
* If the size of the array is fixed and can be specified in the SWIG interface:
*       (type IN_ARRAY2[ANY][ANY])
*       (type IN_ARRAY2[ANY][ANY], int DIM1, int DIM2)
*       (int DIM1, int DIM2, type IN_ARRAY2[ANY][ANY])
* In these cases, an error condition will be raised if the dimensions of the
* structure passed from Python do not match what was specified in braces within
* the C function call.
*
* If the size of the array is defined by the Python structure:
*       (type *IN_ARRAY2, int DIM1, int DIM2)
*       (int DIM1, int DIM2, type *IN_ARRAY2)
* In these cases, there is no limit on the number of elements that can be passed
* to the C function. Internal memory is allocated as needed based on the size of
* the array passed from Python.
*
* NEW variations...
* 
* If the size of the last array axis is fixed and can be specified in the
* SWIG interface:
*       (type IN_ARRAY2[ANY][ANY], int DIM1)
*       (int DIM1, type IN_ARRAY2[ANY][ANY])
* In these cases, an error condition will be raised if the second dimension of
* the structure passed from Python does not match what was specified in braces
* within the C function call. The value of the first dimension is ignored and
* can be set to one.
*
* If the first dimension can be missing:
*       (type *IN_ARRAY12, int DIM1, int DIM2)
* If it is missing, DIM1 = 0.
*******************************************************************************/

%define TYPEMAP_IN(Type, Typecode) /* Use to fill in numeric types below!

/*******************************************************
* (Type IN_ARRAY2[ANY][ANY])
*******************************************************/

%typemap(in)
    (Type IN_ARRAY2[ANY][ANY])                                  // PATTERN
            (PyArrayObject* pyarr=NULL, int is_new_object=0)
{
//      (Type IN_ARRAY2[ANY][ANY])

    pyarr = obj_to_array_contiguous_allow_conversion($input, Typecode,
                                                     &is_new_object,
                                                     "$symname");
    TEST_FOR_EXCEPTION;
    TEST_INVALIDARRAYRANK(pyarr, 2);
    TEST_INVALIDARRAYSHAPE_2D(pyarr, $1_dim0, $1_dim1);

    if (!pyarr) {
        npy_intp dims[] = {$1_dim0, $1_dim1};
        pyarr = (PyArrayObject *) PyArray_SimpleNew(2, dims, Typecode);
        is_new_object = 1;
    }
    TEST_MALLOCFAILURE(pyarr,1);

    $1 = (Type *) pyarr->data;                                  // ARRAY
//  $2 = (int) pyarr->dimensions[0];                            // DIM1
//  $3 = (int) pyarr->dimensions[1];                            // DIM2
}

/*******************************************************
* (Type IN_ARRAY2[ANY][ANY], int DIM1, int DIM2)
*******************************************************/

%typemap(in)
    (Type IN_ARRAY2[ANY][ANY], int DIM1, int DIM2)              // PATTERN
        (PyArrayObject* pyarr=NULL, int is_new_object=0),
    (Type IN_ARRAY2[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2)    // PATTERN
        (PyArrayObject* pyarr=NULL, int is_new_object=0)
{
//      (Type IN_ARRAY2[ANY][ANY], int DIM1, int DIM2)

    pyarr = obj_to_array_contiguous_allow_conversion($input, Typecode,
                                                     &is_new_object,
                                                     "$symname");
    TEST_FOR_EXCEPTION;
    TEST_INVALIDARRAYRANK(pyarr, 2);
    TEST_INVALIDARRAYSHAPE_2D(pyarr, $1_dim0, $1_dim1);

    if (!pyarr) {
        npy_intp dims[] = {$1_dim0, $1_dim1};
        pyarr = (PyArrayObject *) PyArray_SimpleNew(2, dims, Typecode);
        is_new_object = 1;
    }
    TEST_MALLOCFAILURE(pyarr,1);

    $1 = (Type *) pyarr->data;                                  // ARRAY
    $2 = (int) pyarr->dimensions[0];                            // DIM1
    $3 = (int) pyarr->dimensions[1];                            // DIM2
}

/*******************************************************
* (int DIM1, int DIM2, Type IN_ARRAY2[ANY][ANY])
*******************************************************/

%typemap(in)
    (int DIM1, int DIM2, Type IN_ARRAY2[ANY][ANY])              // PATTERN
            (PyArrayObject* pyarr=NULL, int is_new_object=0),
    (SpiceInt DIM1, SpiceInt DIM2, Type IN_ARRAY2[ANY][ANY])    // PATTERN
            (PyArrayObject* pyarr=NULL, int is_new_object=0)
{
//      (int DIM1, int DIM2, Type IN_ARRAY2[ANY][ANY])

    pyarr = obj_to_array_contiguous_allow_conversion($input, Typecode,
                                                     &is_new_object,
                                                     "$symname");
    TEST_FOR_EXCEPTION;
    TEST_INVALIDARRAYRANK(pyarr, 2);
    TEST_INVALIDARRAYSHAPE_2D(pyarr, $3_dim0, $3_dim1);

    if (!pyarr) {
        npy_intp dims[] = {$3_dim0, $3_dim1};
        pyarr = (PyArrayObject *) PyArray_SimpleNew(2, dims, Typecode);
        is_new_object = 1;
    }
    TEST_MALLOCFAILURE(pyarr,1);

    $3 = (Type *) pyarr->data;                                  // ARRAY
    $1 = (int) pyarr->dimensions[0];                            // DIM1
    $2 = (int) pyarr->dimensions[1];                            // DIM2
}

/*******************************************************
* (Type IN_ARRAY2[ANY][ANY], int DIM1)
*******************************************************/

%typemap(in)
    (Type IN_ARRAY2[ANY][ANY], int DIM1)                        // PATTERN
            (PyArrayObject* pyarr=NULL, int is_new_object=0),
    (Type IN_ARRAY2[ANY][ANY], SpiceInt DIM1)                   // PATTERN
            (PyArrayObject* pyarr=NULL, int is_new_object=0)
{
//      (Type IN_ARRAY2[ANY][ANY], int DIM1)

    pyarr = obj_to_array_contiguous_allow_conversion($input, Typecode,
                                                     &is_new_object,
                                                     "$symname");
    TEST_FOR_EXCEPTION;
    TEST_INVALIDARRAYRANK(pyarr, 2);
    TEST_INVALIDARRAYSHAPE_x2D(pyarr, $1_dim1);

    if (!pyarr) {
        npy_intp dims[] = {$1_dim0, $1_dim1};
        pyarr = (PyArrayObject *) PyArray_SimpleNew(2, dims, Typecode);
        is_new_object = 1;
    }
    TEST_MALLOCFAILURE(pyarr,1);

    $1 = (Type *) pyarr->data;                                  // ARRAY
    $2 = (int) pyarr->dimensions[0];                            // DIM1
}

/*******************************************************
* (int DIM1, Type IN_ARRAY2[ANY][ANY])
*******************************************************/

%typemap(in)
    (int DIM1, Type IN_ARRAY2[ANY][ANY])                        // PATTERN
            (PyArrayObject* pyarr=NULL, int is_new_object=0),
    (SpiceInt DIM1, Type IN_ARRAY2[ANY][ANY])                   // PATTERN
            (PyArrayObject* pyarr=NULL, int is_new_object=0)
{
//      (int DIM1, Type IN_ARRAY2[ANY][ANY])

    pyarr = obj_to_array_contiguous_allow_conversion($input, Typecode,
                                                     &is_new_object,
                                                     "$symname");
    TEST_FOR_EXCEPTION;
    TEST_INVALIDARRAYRANK(pyarr, 2);
    TEST_INVALIDARRAYSHAPE_x2D(pyarr, $2_dim1);

    if (!pyarr) {
        npy_intp dims[] = {1, $2_dim1};
        pyarr = (PyArrayObject *) PyArray_SimpleNew(2, dims, Typecode);
        is_new_object = 1;
    }
    TEST_MALLOCFAILURE(pyarr,1);

    $2 = (Type *) pyarr->data;                                  // ARRAY
    $1 = (int) pyarr->dimensions[0];                            // DIM1
}

/*******************************************************
* (Type *IN_ARRAY2, int DIM1, int DIM2)
*******************************************************/

%typemap(in)
    (Type *IN_ARRAY2, int DIM1, int DIM2)                       // PATTERN
        (PyArrayObject* pyarr=NULL, int is_new_object=0),
    (Type *IN_ARRAY2, SpiceInt DIM1, SpiceInt DIM2)             // PATTERN
        (PyArrayObject* pyarr=NULL, int is_new_object=0)
{
//      (Type *IN_ARRAY2, int DIM1, int DIM2)

    pyarr = obj_to_array_contiguous_allow_conversion($input, Typecode,
                                                     &is_new_object,
                                                     "$symname");
    TEST_FOR_EXCEPTION;
    TEST_INVALIDARRAYRANK(pyarr, 2);

    if (!pyarr) {
        npy_intp dims[] = {1, 1};
        pyarr = (PyArrayObject *) PyArray_SimpleNew(2, dims, Typecode);
        is_new_object = 1;
    }
    TEST_MALLOCFAILURE(pyarr,1);

    $1 = (Type *) pyarr->data;                              // ARRAY
    $2 = (int) pyarr->dimensions[0];                        // DIM1
    $3 = (int) pyarr->dimensions[1];                        // DIM2
}

/*******************************************************
* (int DIM1, int DIM2, Type *IN_ARRAY2)
*******************************************************/

%typemap(in)
    (int DIM1, int DIM2, Type *IN_ARRAY2)                       // PATTERN
        (PyArrayObject* pyarr=NULL, int is_new_object=0),
    (SpiceInt DIM1, SpiceInt DIM2, Type *IN_ARRAY2)             // PATTERN
        (PyArrayObject* pyarr=NULL, int is_new_object=0)
{
//      (int DIM1, int DIM2, Type *IN_ARRAY2)

    pyarr = obj_to_array_contiguous_allow_conversion($input, Typecode,
                                                     &is_new_object,
                                                     "$symname");
    TEST_FOR_EXCEPTION;
    TEST_INVALIDARRAYRANK(pyarr, 2);

    if (!pyarr) {
        npy_intp dims[] = {1, 1};
        pyarr = (PyArrayObject *) PyArray_SimpleNew(2, dims, Typecode);
        is_new_object = 1;
    }
    TEST_MALLOCFAILURE(pyarr,1);

    $3 = (Type *) pyarr->data;                              // ARRAY
    $1 = (int) pyarr->dimensions[0];                        // DIM1
    $2 = (int) pyarr->dimensions[1];                        // DIM2
}

/*******************************************************
* (Type *IN_ARRAY12, int DIM1, int DIM2)
*******************************************************/

%typemap(in)
    (Type *IN_ARRAY12, int DIM1, int DIM2)                      // PATTERN
        (PyArrayObject* pyarr=NULL, int is_new_object=0),
    (Type *IN_ARRAY12, SpiceInt DIM1, SpiceInt DIM2)            // PATTERN
        (PyArrayObject* pyarr=NULL, int is_new_object=0)
{
//      (Type *IN_ARRAY12, int DIM1, int DIM2)

    pyarr = obj_to_array_contiguous_allow_conversion($input, Typecode,
                                                     &is_new_object,
                                                     "$symname");
    TEST_FOR_EXCEPTION;
    TEST_INVALIDARRAYRANK_OR(pyarr, 1, 2);

    if (!pyarr) {
        npy_intp dims[] = {1};
        pyarr = (PyArrayObject *) PyArray_SimpleNew(1, dims, Typecode);
        is_new_object = 1;
    }
    TEST_MALLOCFAILURE(pyarr,1);

    if (pyarr->nd == 1) {
        $1 = (Type *) pyarr->data;                              // ARRAY
        $2 = 0;                                                 // DIM1
        $3 = (int) pyarr->dimensions[0];                        // DIM2
    }
    else {
        $1 = (Type *) pyarr->data;                              // ARRAY
        $2 = (int) pyarr->dimensions[0];                        // DIM1
        $3 = (int) pyarr->dimensions[1];                        // DIM2
    }
}

/*******************************************************
* %typemap(check)
* %typemap(argout)
* %typemap(freearg)
*******************************************************/

%typemap(check)
    (Type IN_ARRAY2[ANY][ANY]),
    (Type IN_ARRAY2[ANY][ANY], int DIM1, int DIM2),
    (Type IN_ARRAY2[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2),
    (int DIM1, int DIM2, Type IN_ARRAY2[ANY][ANY]),
    (SpiceInt DIM1, SpiceInt DIM2, Type IN_ARRAY2[ANY][ANY]),
    (Type IN_ARRAY2[ANY][ANY], int DIM1),
    (Type IN_ARRAY2[ANY][ANY], SpiceInt DIM1),
    (int DIM1, Type IN_ARRAY2[ANY][ANY]),
    (SpiceInt DIM1, Type IN_ARRAY2[ANY][ANY]),
    (Type *IN_ARRAY2, int DIM1, int DIM2),
    (Type *IN_ARRAY2, SpiceInt DIM1, SpiceInt DIM2),
    (int DIM1, int DIM2, Type *IN_ARRAY2),
    (SpiceInt DIM1, SpiceInt DIM2, Type *IN_ARRAY2),
    (Type *IN_ARRAY12, int DIM1, int DIM2),
    (Type *IN_ARRAY12, SpiceInt DIM1, SpiceInt DIM2)
{}

%typemap(argout)
    (Type IN_ARRAY2[ANY][ANY]),
    (Type IN_ARRAY2[ANY][ANY], int DIM1, int DIM2),
    (Type IN_ARRAY2[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2),
    (int DIM1, int DIM2, Type IN_ARRAY2[ANY][ANY]),
    (SpiceInt DIM1, SpiceInt DIM2, Type IN_ARRAY2[ANY][ANY]),
    (Type IN_ARRAY2[ANY][ANY], int DIM1),
    (Type IN_ARRAY2[ANY][ANY], SpiceInt DIM1),
    (int DIM1, Type IN_ARRAY2[ANY][ANY]),
    (SpiceInt DIM1, Type IN_ARRAY2[ANY][ANY]),
    (Type *IN_ARRAY2, int DIM1, int DIM2),
    (Type *IN_ARRAY2, SpiceInt DIM1, SpiceInt DIM2),
    (int DIM1, int DIM2, Type *IN_ARRAY2),
    (SpiceInt DIM1, SpiceInt DIM2, Type *IN_ARRAY2),
    (Type *IN_ARRAY12, int DIM1, int DIM2),
    (Type *IN_ARRAY12, SpiceInt DIM1, SpiceInt DIM2)
{}

%typemap(freearg)
    (Type IN_ARRAY2[ANY][ANY]),
    (Type IN_ARRAY2[ANY][ANY], int DIM1, int DIM2),
    (Type IN_ARRAY2[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2),
    (int DIM1, int DIM2, Type IN_ARRAY2[ANY][ANY]),
    (SpiceInt DIM1, SpiceInt DIM2, Type IN_ARRAY2[ANY][ANY]),
    (Type IN_ARRAY2[ANY][ANY], int DIM1),
    (Type IN_ARRAY2[ANY][ANY], SpiceInt DIM1),
    (int DIM1, Type IN_ARRAY2[ANY][ANY]),
    (SpiceInt DIM1, Type IN_ARRAY2[ANY][ANY]),
    (Type *IN_ARRAY2, int DIM1, int DIM2),
    (Type *IN_ARRAY2, SpiceInt DIM1, SpiceInt DIM2),
    (int DIM1, int DIM2, Type *IN_ARRAY2),
    (SpiceInt DIM1, SpiceInt DIM2, Type *IN_ARRAY2),
    (Type *IN_ARRAY12, int DIM1, int DIM2),
    (Type *IN_ARRAY12, SpiceInt DIM1, SpiceInt DIM2)
{
//      (Type ...IN_ARRAY2...)

    if (is_new_object$argnum && pyarr$argnum) Py_DECREF(pyarr$argnum);
}

/*******************************************************
* Now apply to all data types
*******************************************************/

%enddef

// Define concrete examples of the TYPEMAP_IN1 macros
TYPEMAP_IN(char,             PyArray_CHAR  )
TYPEMAP_IN(SpiceChar,        PyArray_CHAR  )
TYPEMAP_IN(ConstSpiceChar,   PyArray_CHAR  )
TYPEMAP_IN(unsigned char,    PyArray_UBYTE )
TYPEMAP_IN(signed char,      PyArray_SBYTE )
TYPEMAP_IN(short,            PyArray_SHORT )
TYPEMAP_IN(int,              PyArray_INT   )
TYPEMAP_IN(SpiceInt,         PyArray_INT   )
TYPEMAP_IN(ConstSpiceInt,    PyArray_INT   )
TYPEMAP_IN(SpiceBoolean,     PyArray_INT   )
TYPEMAP_IN(long,             PyArray_LONG  )
TYPEMAP_IN(float,            PyArray_FLOAT )
TYPEMAP_IN(double,           PyArray_DOUBLE)
TYPEMAP_IN(SpiceDouble,      PyArray_DOUBLE)
TYPEMAP_IN(ConstSpiceDouble, PyArray_DOUBLE)
TYPEMAP_IN(PyObject,         PyArray_OBJECT)

#undef TYPEMAP_IN

/*******************************************************************************
* 3-D numeric typemaps for input
*
* This family of typemaps allows Python 3-D sequences and Numpy 3-D arrays to be
* read as arrays in C functions.
*
* If the sizes of the last two array axes are fixed and can be specified in the
* SWIG interface:
*       (type IN_ARRAY3[ANY][ANY][ANY], int DIM1)
*       (int DIM1, type IN_ARRAY3[ANY][ANY][ANY])
* In these cases, an error condition will be raised if the last two dimensions
* of the structure passed from Python do not match what was specified in braces
* within the C function call. The first dimension is ignored and can be set to
* one.
*
* If the size of the array is defined by the Python structure:
*       (type *IN_ARRAY3, int DIM1, int DIM2, int DIM3)
*       (int DIM1, int DIM2, int DIM3, type *IN_ARRAY2)
* In these cases, there is no limit on the number of elements that can be passed
* to the C function. Internal memory is allocated as needed based on the size of
* the array passed from Python.
*
* If the first dimension can be missing:
*       (type *IN_ARRAY23, int DIM1, int DIM2, int DIM3)
* If so, DIM1 = 0.
*******************************************************************************/

%define TYPEMAP_IN(Type, Typecode) /* Use to fill in numeric types below!

/*******************************************************
* (Type IN_ARRAY3[ANY][ANY][ANY], int DIM1)
*******************************************************/

%typemap(in)
    (Type IN_ARRAY3[ANY][ANY][ANY], int DIM1)                   // PATTERN
        (PyArrayObject* pyarr=NULL, int is_new_object=0),
    (Type IN_ARRAY3[ANY][ANY][ANY], SpiceInt DIM1)              // PATTERN
        (PyArrayObject* pyarr=NULL, int is_new_object=0)
{
//      (Type IN_ARRAY3[ANY][ANY][ANY], int DIM1)

    pyarr = obj_to_array_contiguous_allow_conversion($input, Typecode,
                                                     &is_new_object,
                                                     "$symname");
    TEST_FOR_EXCEPTION;
    TEST_INVALIDARRAYRANK(pyarr, 3);
    TEST_INVALIDARRAYSHAPE_x3D(pyarr, $1_dim1, $1_dim2);

    if (!pyarr) {
        npy_intp dims[] = {1, $1_dim1, $1_dim2};
        pyarr = (PyArrayObject *) PyArray_SimpleNew(3, dims, Typecode);
        is_new_object = 1;
    }
    TEST_MALLOCFAILURE(pyarr,1);

    $1 = (Type *) pyarr->data;                                  // ARRAY
    $2 = (int) pyarr->dimensions[0];                            // DIM1
}

/*******************************************************
* (int DIM1, Type IN_ARRAY3[ANY][ANY][ANY])
*******************************************************/

%typemap(in)
    (int DIM1, Type IN_ARRAY3[ANY][ANY][ANY])                   // PATTERN
        (PyArrayObject* pyarr=NULL, int is_new_object=0),
    (SpiceInt DIM1, Type IN_ARRAY3[ANY][ANY][ANY])              // PATTERN
        (PyArrayObject* pyarr=NULL, int is_new_object=0)
{
//      (int DIM1, Type IN_ARRAY3[ANY][ANY][ANY])

    pyarr = obj_to_array_contiguous_allow_conversion($input, Typecode,
                                                     &is_new_object,
                                                     "$symname");
    TEST_FOR_EXCEPTION;
    TEST_INVALIDARRAYRANK(pyarr, 3);
    TEST_INVALIDARRAYSHAPE_x3D(pyarr, $2_dim1, $2_dim2);

    if (!pyarr) {
        npy_intp dims[] = {1, $2_dim1, $2_dim2};
        pyarr = (PyArrayObject *) PyArray_SimpleNew(3, dims, Typecode);
        is_new_object = 1;
    }
    TEST_MALLOCFAILURE(pyarr,1);

    $2 = (Type *) pyarr->data;                                  // ARRAY
    $1 = (int) pyarr->dimensions[0];                            // DIM1
}

/*******************************************************
* (Type *IN_ARRAY3, int DIM1, int DIM2, int DIM3)
*******************************************************/

%typemap(in)
    (Type *IN_ARRAY3, int DIM1, int DIM2, int DIM3)             // PATTERN
        (PyArrayObject* pyarr=NULL, int is_new_object=0),
    (Type *IN_ARRAY3, SpiceInt DIM1, SpiceInt DIM2, SpiceInt DIM3) // PATTERN
        (PyArrayObject* pyarr=NULL, int is_new_object=0)
{
//      (Type *IN_ARRAY3, int DIM1, int DIM2, int DIM3)

    pyarr = obj_to_array_contiguous_allow_conversion($input, Typecode,
                                                     &is_new_object,
                                                     "$symname");
    TEST_FOR_EXCEPTION;
    TEST_INVALIDARRAYRANK(pyarr, 3);

    if (!pyarr) {
        npy_intp dims[] = {1, 1, 1};
        pyarr = (PyArrayObject *) PyArray_SimpleNew(3, dims, Typecode);
        is_new_object = 1;
    }
    TEST_MALLOCFAILURE(pyarr,1);

    $1 = (Type *) pyarr->data;                                  // ARRAY
    $2 = (int) pyarr->dimensions[0];                            // DIM1
    $3 = (int) pyarr->dimensions[1];                            // DIM2
    $4 = (int) pyarr->dimensions[2];                            // DIM3
}

/*******************************************************
* (int DIM1, int DIM2, int DIM3, Type *IN_ARRAY3)
*******************************************************/

%typemap(in)
    (int DIM1, int DIM2, int DIM3, Type *IN_ARRAY3)             // PATTERN
        (PyArrayObject* pyarr=NULL, int is_new_object=0),
    (SpiceInt DIM1, SpiceInt DIM2, SpiceInt DIM3, Type *IN_ARRAY3) // PATTERN
        (PyArrayObject* pyarr=NULL, int is_new_object=0)
{
//      (int DIM1, int DIM2, int DIM3, Type *IN_ARRAY3)

    pyarr = obj_to_array_contiguous_allow_conversion($input, Typecode,
                                                     &is_new_object,
                                                     "$symname");
    TEST_FOR_EXCEPTION;
    TEST_INVALIDARRAYRANK(pyarr, 3);

    if (!pyarr) {
        npy_intp dims[] = {1, 1, 1};
        pyarr = (PyArrayObject *) PyArray_SimpleNew(3, dims, Typecode);
        is_new_object = 1;
    }
    TEST_MALLOCFAILURE(pyarr,1);

    $4 = (Type *) pyarr->data;                                  // ARRAY
    $1 = (int) pyarr->dimensions[0];                            // DIM1
    $2 = (int) pyarr->dimensions[1];                            // DIM2
    $3 = (int) pyarr->dimensions[2];                            // DIM3
}

/*******************************************************
* (Type *IN_ARRAY23, int DIM1, int DIM2, int DIM3)
*******************************************************/

%typemap(in)
    (Type *IN_ARRAY23, int DIM1, int DIM2, int DIM3)            // PATTERN
        (PyArrayObject* pyarr=NULL, int is_new_object=0),
    (Type *IN_ARRAY23, SpiceInt DIM1, SpiceInt DIM2, SpiceInt DIM3) // PATTERN
        (PyArrayObject* pyarr=NULL, int is_new_object=0)
{
//      (Type *IN_ARRAY23, int DIM1, int DIM2, int DIM3)

    pyarr = obj_to_array_contiguous_allow_conversion($input, Typecode,
                                                     &is_new_object,
                                                     "$symname");
    TEST_FOR_EXCEPTION;
    TEST_INVALIDARRAYRANK_OR(pyarr, 2, 3);

    if (!pyarr) {
        npy_intp dims[] = {1, 1};
        pyarr = (PyArrayObject *) PyArray_SimpleNew(2, dims, Typecode);
        is_new_object = 1;
    }
    TEST_MALLOCFAILURE(pyarr,1);

    if (pyarr->nd == 2) {
        $1 = (Type *) pyarr->data;                              // ARRAY
        $2 = 0;                                                 // DIM1
        $3 = (int) pyarr->dimensions[0];                        // DIM2
        $4 = (int) pyarr->dimensions[1];                        // DIM3
    }
    else {
        $1 = (Type *) pyarr->data;                              // ARRAY
        $2 = (int) pyarr->dimensions[0];                        // DIM1
        $3 = (int) pyarr->dimensions[1];                        // DIM2
        $4 = (int) pyarr->dimensions[2];                        // DIM3
    }
}

/*******************************************************
* %typemap(check)
* %typemap(argout)
* %typemap(freearg)
*******************************************************/

%typemap(check)
    (Type IN_ARRAY3[ANY][ANY][ANY], int DIM1),
    (Type IN_ARRAY3[ANY][ANY][ANY], SpiceInt DIM1),
    (int DIM1, Type IN_ARRAY3[ANY][ANY][ANY]),
    (SpiceInt DIM1, Type IN_ARRAY3[ANY][ANY][ANY]),
    (Type *IN_ARRAY3, int DIM1, int DIM2, int DIM3),
    (Type *IN_ARRAY3, SpiceInt DIM1, SpiceInt DIM2, SpiceInt DIM3),
    (int DIM1, int DIM2, int DIM3, Type *IN_ARRAY3),
    (SpiceInt DIM1, SpiceInt DIM2, SpiceInt DIM3, Type *IN_ARRAY3),
    (Type *IN_ARRAY23, int DIM1, int DIM2, int DIM3),
    (Type *IN_ARRAY23, SpiceInt DIM1, SpiceInt DIM2, SpiceInt DIM3)
{}

%typemap(argout)
    (Type IN_ARRAY3[ANY][ANY][ANY], int DIM1),
    (Type IN_ARRAY3[ANY][ANY][ANY], SpiceInt DIM1),
    (int DIM1, Type IN_ARRAY3[ANY][ANY][ANY]),
    (SpiceInt DIM1, Type IN_ARRAY3[ANY][ANY][ANY]),
    (Type *IN_ARRAY3, int DIM1, int DIM2, int DIM3),
    (Type *IN_ARRAY3, SpiceInt DIM1, SpiceInt DIM2, SpiceInt DIM3),
    (int DIM1, int DIM2, int DIM3, Type *IN_ARRAY3),
    (SpiceInt DIM1, SpiceInt DIM2, SpiceInt DIM3, Type *IN_ARRAY3),
    (Type *IN_ARRAY23, int DIM1, int DIM2, int DIM3),
    (Type *IN_ARRAY23, SpiceInt DIM1, SpiceInt DIM2, SpiceInt DIM3)
{}

%typemap(freearg)
    (Type IN_ARRAY3[ANY][ANY][ANY], int DIM1),
    (Type IN_ARRAY3[ANY][ANY][ANY], SpiceInt DIM1),
    (int DIM1, Type IN_ARRAY3[ANY][ANY][ANY]),
    (SpiceInt DIM1, Type IN_ARRAY3[ANY][ANY][ANY]),
    (Type *IN_ARRAY3, int DIM1, int DIM2, int DIM3),
    (Type *IN_ARRAY3, SpiceInt DIM1, SpiceInt DIM2, SpiceInt DIM3),
    (int DIM1, int DIM2, int DIM3, Type *IN_ARRAY3),
    (SpiceInt DIM1, SpiceInt DIM2, SpiceInt DIM3, Type *IN_ARRAY3),
    (Type *IN_ARRAY23, int DIM1, int DIM2, int DIM3),
    (Type *IN_ARRAY23, SpiceInt DIM1, SpiceInt DIM2, SpiceInt DIM3)
{
//      (Type ...IN_ARRAY3...)

    if (is_new_object$argnum && pyarr$argnum) Py_DECREF(pyarr$argnum);
}

/*******************************************************
* Now apply to all data types
*******************************************************/

%enddef

// Define concrete examples of the TYPEMAP_IN1 macros
TYPEMAP_IN(char,             PyArray_CHAR  )
TYPEMAP_IN(SpiceChar,        PyArray_CHAR  )
TYPEMAP_IN(unsigned char,    PyArray_UBYTE )
TYPEMAP_IN(signed char,      PyArray_SBYTE )
TYPEMAP_IN(short,            PyArray_SHORT )
TYPEMAP_IN(int,              PyArray_INT   )
TYPEMAP_IN(SpiceInt,         PyArray_INT   )
TYPEMAP_IN(ConstSpiceInt,    PyArray_INT   )
TYPEMAP_IN(SpiceBoolean,     PyArray_INT   )
TYPEMAP_IN(long,             PyArray_LONG  )
TYPEMAP_IN(float,            PyArray_FLOAT )
TYPEMAP_IN(double,           PyArray_DOUBLE)
TYPEMAP_IN(SpiceDouble,      PyArray_DOUBLE)
TYPEMAP_IN(ConstSpiceDouble, PyArray_DOUBLE)
TYPEMAP_IN(PyObject,         PyArray_OBJECT)

#undef TYPEMAP_IN

/*******************************************************************************
* 1-D numeric typemaps for output
*
* This family of typemaps allows arrays of numbers in a C to be hidden as inputs
* but to be returned as Numpy arrays inside Python. However, the size (or an
* upper limit) must be specified in advance so that adequate memory can be
* allocated.
*
* If the size of the array can be specified in the SWIG interface:
*       (type OUT_ARRAY1[ANY])
*       (type OUT_ARRAY1[ANY], int DIM1)
*       (int DIM1, type OUT_ARRAY1[ANY])
*
* If the upper limit on the size of the array can be specified in the SWIG
* interface, but the size returned by C is variable:
*       (type OUT_ARRAY1[ANY], int DIM1, int *SIZE1)
*       (type OUT_ARRAY1[ANY], int *SIZE1, int DIM1)
*       (int DIM1, int *SIZE1, type OUT_ARRAY1[ANY])
*       (int *SIZE1, int DIM1, type OUT_ARRAY1[ANY])
*
* If the total size of a temporary memory buffer can be specified in advance,
* and the shape of the array then returned afterward.
*       (type OUT_ARRAY1[ANY], int *SIZE1)
*       (int *SIZE1, type OUT_ARRAY1[ANY])
*
* If the C function will allocate the memory it needs and will return the size:
*       (type **OUT_ARRAY1, int *DIM1)
*       (int *DIM1, type **OUT_ARRAY1)
*******************************************************************************/

%define TYPEMAP_ARGOUT(Type, Typecode) // Use to fill in numeric types below!

/*******************************************************
* (Type OUT_ARRAY1[ANY])
*******************************************************/

%typemap(check)
    (Type OUT_ARRAY1[ANY])                                      // PATTERN
        (PyArrayObject* pyarr = NULL)
{
//      (Type OUT_ARRAY1[ANY])

    npy_intp dims$argnum[1] = {$1_dim0};                        // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(1, dims$argnum, Typecode);
    TEST_MALLOCFAILURE(pyarr,1);

    $1 = (Type *) pyarr->data;                                  // ARRAY
//  $2 = (int) pyarr->dimensions[0];                            // DIM1
//  $3 = &size[0];                                              // SIZE1
}

/*******************************************************
* (Type OUT_ARRAY1[ANY], int DIM1)
*******************************************************/

%typemap(check)
    (Type OUT_ARRAY1[ANY], int DIM1)                            // PATTERN
        (PyArrayObject* pyarr = NULL),
    (Type OUT_ARRAY1[ANY], SpiceInt DIM1)                       // PATTERN
        (PyArrayObject* pyarr = NULL)
{
//      (Type OUT_ARRAY1[ANY], int DIM1)

    npy_intp dims$argnum[1] = {$1_dim0};                        // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(1, dims$argnum, Typecode);
    TEST_MALLOCFAILURE(pyarr,1);

    $1 = (Type *) pyarr->data;                                  // ARRAY
    $2 = (int) pyarr->dimensions[0];                            // DIM1
//  $3 = &size[0];                                              // SIZE1
}

/*******************************************************
* (int DIM1, Type OUT_ARRAY1[ANY])
*******************************************************/

%typemap(check)
    (int DIM1, Type OUT_ARRAY1[ANY])                            // PATTERN
        (PyArrayObject* pyarr = NULL),
    (SpiceInt DIM1, Type OUT_ARRAY1[ANY])                       // PATTERN
        (PyArrayObject* pyarr = NULL)
{
//      (int DIM1, Type OUT_ARRAY1[ANY])

    npy_intp dims$argnum[1] = {$2_dim0};                        // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(1, dims$argnum, Typecode);
    TEST_MALLOCFAILURE(pyarr,1);

    $2 = (Type *) pyarr->data;                                  // ARRAY
    $1 = (int) pyarr->dimensions[0];                            // DIM1
//  $3 = &size[0];                                              // SIZE1
}

/*******************************************************
* (Type OUT_ARRAY1[ANY], int DIM1, int *SIZE1)
*******************************************************/

%typemap(check)
    (Type OUT_ARRAY1[ANY], int DIM1, int *SIZE1)                // PATTERN
        (PyArrayObject* pyarr = NULL, int size[1]),
    (Type OUT_ARRAY1[ANY], SpiceInt DIM1, SpiceInt *SIZE1)      // PATTERN
        (PyArrayObject* pyarr = NULL, int size[1])
{
//      (Type OUT_ARRAY1[ANY], int DIM1, int *SIZE1)

    npy_intp dims$argnum[1] = {$1_dim0};                        // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(1, dims$argnum, Typecode);
    TEST_MALLOCFAILURE(pyarr,1);

    $1 = (Type *) pyarr->data;                                  // ARRAY
    $2 = (int) pyarr->dimensions[0];                            // DIM1
    $3 = &size[0];                                              // SIZE1
}

/*******************************************************
* (Type OUT_ARRAY1[ANY], int *SIZE1, int DIM1)
*******************************************************/

%typemap(check)
    (Type OUT_ARRAY1[ANY], int *SIZE1, int DIM1)                // PATTERN
        (PyArrayObject* pyarr = NULL, int size[1]),
    (Type OUT_ARRAY1[ANY], SpiceInt *SIZE1, SpiceInt DIM1)      // PATTERN
        (PyArrayObject* pyarr = NULL, int size[1])
{
//      (Type OUT_ARRAY1[ANY], int *SIZE1, int DIM1)

    npy_intp dims$argnum[1] = {$1_dim0};                        // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(1, dims$argnum, Typecode);
    TEST_MALLOCFAILURE(pyarr,1);

    $1 = (Type *) pyarr->data;                                  // ARRAY
    $3 = (int) pyarr->dimensions[0];                            // DIM1
    $2 = &size[0];                                              // SIZE1
}

/*******************************************************
* (int DIM1, int *SIZE1, Type OUT_ARRAY1[ANY])
*******************************************************/

%typemap(check)
    (int DIM1, int *SIZE1, Type OUT_ARRAY1[ANY])                // PATTERN
        (PyArrayObject* pyarr = NULL, int size[1]),
    (SpiceInt DIM1, SpiceInt *SIZE1, Type OUT_ARRAY1[ANY])      // PATTERN
        (PyArrayObject* pyarr = NULL, int size[1])
{
//      (int DIM1, int *SIZE1, Type OUT_ARRAY1[ANY])

    npy_intp dims$argnum[1] = {$3_dim0};                       // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(1, dims$argnum, Typecode);
    TEST_MALLOCFAILURE(pyarr,1);

    $3 = (Type *) pyarr->data;                              // ARRAY
    $1 = (int) pyarr->dimensions[0];                        // DIM1
    $2 = &size[0];                                          // SIZE1
}

/*******************************************************
* (int *SIZE1, int DIM1, Type OUT_ARRAY1[ANY])
*******************************************************/

%typemap(check)
    (int *SIZE1, int DIM1, Type OUT_ARRAY1[ANY])                // PATTERN
        (PyArrayObject* pyarr = NULL, int size[1]),
    (SpiceInt *SIZE1, SpiceInt DIM1, Type OUT_ARRAY1[ANY])      // PATTERN
        (PyArrayObject* pyarr = NULL, int size[1])
{
//      (int *SIZE1, int DIM1, Type OUT_ARRAY1[ANY])

    npy_intp dims$argnum[1] = {$3_dim0};                        // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(1, dims$argnum, Typecode);
    TEST_MALLOCFAILURE(pyarr,1);

    $3 = (Type *) pyarr->data;                                  // ARRAY
    $2 = (int) pyarr->dimensions[0];                            // DIM1
    $1 = &size[0];                                              // SIZE1
}

/*******************************************************
* (Type OUT_ARRAY1[ANY], int *SIZE1)
*******************************************************/

%typemap(check)
    (Type OUT_ARRAY1[ANY], int *SIZE1)                          // PATTERN
        (PyArrayObject* pyarr = NULL, int size[1]),
    (Type OUT_ARRAY1[ANY], SpiceInt *SIZE1)                     // PATTERN
        (PyArrayObject* pyarr = NULL, int size[1])
{
//      (Type OUT_ARRAY1[ANY], int *SIZE1)

    npy_intp dims$argnum[1] = {$1_dim0};                        // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(1, dims$argnum, Typecode);
    TEST_MALLOCFAILURE(pyarr,1);

    $1 = (Type *) pyarr->data;                                  // ARRAY
//  $3 = (int) pyarr->dimensions[0];                            // DIM1
    $2 = &size[0];                                              // SIZE1
}

/*******************************************************
* (int *SIZE1, Type OUT_ARRAY1[ANY])
*******************************************************/

%typemap(check)
    (int *SIZE1, Type OUT_ARRAY1[ANY])                          // PATTERN
        (PyArrayObject* pyarr = NULL, int size[1]),
    (SpiceInt *SIZE1, Type OUT_ARRAY1[ANY])                     // PATTERN
        (PyArrayObject* pyarr = NULL, int size[1])
{
//      (int *SIZE1, Type OUT_ARRAY1[ANY])

    npy_intp dims$argnum[1] = {$2_dim0};                        // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(1, dims$argnum, Typecode);
    TEST_MALLOCFAILURE(pyarr,1);

    $2 = (Type *) pyarr->data;                                  // ARRAY
//  $3 = (int) pyarr->dimensions[0];                            // DIM1
    $1 = &size[0];                                              // SIZE1
}

/*******************************************************
* %typemap(argout)
* %typemap(freearg)
*******************************************************/

%typemap(in, numinputs=0)
    (Type OUT_ARRAY1[ANY]),
    (Type OUT_ARRAY1[ANY], int DIM1),
    (Type OUT_ARRAY1[ANY], SpiceInt DIM1),
    (int DIM1, Type OUT_ARRAY1[ANY]),
    (SpiceInt DIM1, Type OUT_ARRAY1[ANY]),
    (Type OUT_ARRAY1[ANY], int DIM1, int  *SIZE1),
    (Type OUT_ARRAY1[ANY], SpiceInt DIM1, SpiceInt *SIZE1),
    (Type OUT_ARRAY1[ANY], int  *SIZE1, int DIM1),
    (Type OUT_ARRAY1[ANY], SpiceInt *SIZE1, SpiceInt DIM1),
    (int DIM1, int *SIZE1, Type OUT_ARRAY1[ANY]),
    (SpiceInt DIM1, SpiceInt *SIZE1, Type OUT_ARRAY1[ANY]),
    (int *SIZE1, int DIM1, Type OUT_ARRAY1[ANY]),
    (SpiceInt *SIZE1, SpiceInt DIM1, Type OUT_ARRAY1[ANY]),
    (Type OUT_ARRAY1[ANY], int *SIZE1),
    (Type OUT_ARRAY1[ANY], SpiceInt *SIZE1),
    (int *SIZE1, Type OUT_ARRAY1[ANY]),
    (SpiceInt *SIZE1, Type OUT_ARRAY1[ANY])
{}

%typemap(argout)
    (Type OUT_ARRAY1[ANY]),
    (Type OUT_ARRAY1[ANY], int DIM1),
    (Type OUT_ARRAY1[ANY], Spiceint DIM1),
    (int DIM1, Type OUT_ARRAY1[ANY]),
    (Spiceint DIM1, Type OUT_ARRAY1[ANY])
{
    $result = SWIG_Python_AppendOutput($result, (PyObject *) pyarr$argnum);
    Py_INCREF(pyarr$argnum);    // Prevents freearg from freeing
}

%typemap(argout)
    (Type OUT_ARRAY1[ANY], int DIM1, int  *SIZE1),
    (Type OUT_ARRAY1[ANY], SpiceInt DIM1, SpiceInt *SIZE1),
    (Type OUT_ARRAY1[ANY], int  *SIZE1, int DIM1),
    (Type OUT_ARRAY1[ANY], SpiceInt *SIZE1, SpiceInt DIM1),
    (int DIM1, int *SIZE1, Type OUT_ARRAY1[ANY]),
    (SpiceInt DIM1, SpiceInt *SIZE1, Type OUT_ARRAY1[ANY]),
    (int *SIZE1, int DIM1, Type OUT_ARRAY1[ANY]),
    (SpiceInt *SIZE1, SpiceInt DIM1, Type OUT_ARRAY1[ANY]),
    (Type OUT_ARRAY1[ANY], int *SIZE1),
    (Type OUT_ARRAY1[ANY], SpiceInt *SIZE1),
    (int *SIZE1, Type OUT_ARRAY1[ANY]),
    (SpiceInt *SIZE1, Type OUT_ARRAY1[ANY])
{
    if (pyarr$argnum) {
        npy_intp dims$argnum[1] = {size$argnum[0]};
        PyArray_Dims shape = {dims$argnum, 1};
        PyArray_Resize(pyarr$argnum, &shape, 0, NPY_CORDER);

        $result = SWIG_Python_AppendOutput($result, (PyObject *) pyarr$argnum);
        Py_INCREF(pyarr$argnum);    // Prevents freearg from freeing
    }
    else {
        $result = SWIG_Python_AppendOutput($result, Py_None);
    }
}

%typemap(freearg)
    (Type OUT_ARRAY1[ANY]),
    (Type OUT_ARRAY1[ANY], int DIM1),
    (Type OUT_ARRAY1[ANY], SpiceInt DIM1),
    (int DIM1, Type OUT_ARRAY1[ANY]),
    (SpiceInt DIM1, Type OUT_ARRAY1[ANY]),
    (Type OUT_ARRAY1[ANY], int DIM1, int  *SIZE1),
    (Type OUT_ARRAY1[ANY], SpiceInt DIM1, SpiceInt *SIZE1),
    (Type OUT_ARRAY1[ANY], int  *SIZE1, int DIM1),
    (Type OUT_ARRAY1[ANY], SpiceInt *SIZE1, SpiceInt DIM1),
    (int DIM1, int *SIZE1, Type OUT_ARRAY1[ANY]),
    (SpiceInt DIM1, SpiceInt *SIZE1, Type OUT_ARRAY1[ANY]),
    (int *SIZE1, int DIM1, Type OUT_ARRAY1[ANY]),
    (SpiceInt *SIZE1, SpiceInt DIM1, Type OUT_ARRAY1[ANY]),
    (Type OUT_ARRAY1[ANY], int  *SIZE1),
    (Type OUT_ARRAY1[ANY], SpiceInt *SIZE1),
    (int *SIZE1, Type OUT_ARRAY1[ANY]),
    (SpiceInt *SIZE1, Type OUT_ARRAY1[ANY])
{
    if (pyarr$argnum) {
        Py_DECREF(pyarr$argnum);
    }
}

/***************************************************************
* (Type **OUT_ARRAY1, int *SIZE1)
***************************************************************/

%typemap(check)
    (Type **OUT_ARRAY1, int *SIZE1)
        (PyArrayObject* pyarr=NULL, Type *buffer=NULL, int dimsize[1]),
    (Type **OUT_ARRAY1, SpiceInt *SIZE1)
        (PyArrayObject* pyarr=NULL, Type *buffer=NULL, int dimsize[1])
{
//      (Type **OUT_ARRAY1, int *SIZE1)

    $1 = &buffer;                                               // ARRAY
    $2 = &dimsize[0];                                           // SIZE1
}

/***************************************************************
* (int *SIZE1, Type **OUT_ARRAY1)
***************************************************************/

%typemap(check)
    (int *SIZE1, Type **OUT_ARRAY1)
        (PyArrayObject* pyarr=NULL, Type *buffer=NULL, int dimsize[1]),
    (SpiceInt *SIZE1, Type **OUT_ARRAY1)
        (PyArrayObject* pyarr=NULL, Type *buffer=NULL, int dimsize[1])
{
//      (int *SIZE1, Type **OUT_ARRAY1)

    $2 = &buffer;                                               // ARRAY
    $1 = &dimsize[0];                                           // SIZE1
}

/*******************************************************
* %typemap(argout)
* %typemap(freearg)
*******************************************************/

%typemap(in, numinputs=0)
    (Type **OUT_ARRAY1, int *SIZE1),
    (Type **OUT_ARRAY1, SpiceInt *SIZE1),
    (int *SIZE1, Type **OUT_ARRAY1),
    (SpiceInt *SIZE1, Type **OUT_ARRAY1)
{}

%typemap(argout)
    (Type **OUT_ARRAY1, int *SIZE1),
    (Type **OUT_ARRAY1, SpiceInt *SIZE1),
    (int *SIZE1, Type **OUT_ARRAY1),
    (SpiceInt *SIZE1, Type **OUT_ARRAY1)
{
//      (Type **OUT_ARRAY1, int *SIZE1)
//      (int *SIZE1, Type **OUT_ARRAY1)

    npy_intp dims$argnum[1] = {dimsize$argnum[0]};
    pyarr$argnum = (PyArrayObject *) PyArray_SimpleNew(1, dims$argnum,
                                                          Typecode);
    TEST_MALLOCFAILURE(pyarr$argnum,0);

    if (pyarr$argnum) {
        memcpy(pyarr$argnum->data, buffer$argnum, dims$argnum[0] * sizeof(Type));
        PyMem_Free((void *) buffer$argnum);

        $result = SWIG_Python_AppendOutput($result, (PyObject *) pyarr$argnum);
        Py_INCREF(pyarr$argnum);    // Prevents freearg from freeing
    }
    else {
        $result = SWIG_Python_AppendOutput($result, Py_None);
    }
}

%typemap(freearg)
    (Type **OUT_ARRAY1, int *SIZE1),
    (Type **OUT_ARRAY1, SpiceInt *SIZE1),
    (int *SIZE1, Type **OUT_ARRAY1),
    (SpiceInt *SIZE1, Type **OUT_ARRAY1)
{
    if (pyarr$argnum) {
        Py_DECREF(pyarr$argnum);
    }
}

/*******************************************************
* Now define these typemaps for every numeric type
*******************************************************/

%enddef

TYPEMAP_ARGOUT(char,          PyArray_CHAR  )
TYPEMAP_ARGOUT(SpiceChar,     PyArray_CHAR  )
TYPEMAP_ARGOUT(unsigned char, PyArray_UBYTE )
TYPEMAP_ARGOUT(signed char,   PyArray_SBYTE )
TYPEMAP_ARGOUT(short,         PyArray_SHORT )
TYPEMAP_ARGOUT(int,           PyArray_INT   )
TYPEMAP_ARGOUT(SpiceInt,      PyArray_INT   )
TYPEMAP_ARGOUT(SpiceBoolean,  PyArray_INT   )
TYPEMAP_ARGOUT(long,          PyArray_LONG  )
TYPEMAP_ARGOUT(float,         PyArray_FLOAT )
TYPEMAP_ARGOUT(double,        PyArray_DOUBLE)
TYPEMAP_ARGOUT(SpiceDouble,   PyArray_DOUBLE)
TYPEMAP_ARGOUT(PyObject,      PyArray_OBJECT)

#undef TYPEMAP_ARGOUT

/*******************************************************************************
* If the function should return a Python scalar on size = 0:
*       (type **OUT_ARRAY01, int *DIM1)
*******************************************************************************/

%define TYPEMAP_ARGOUT(Type, Typecode, Scalarobj) // To fill in types below!

/***************************************************************
* (Type **OUT_ARRAY01, int *SIZE1)
***************************************************************/

%typemap(check)
    (Type **OUT_ARRAY01, int *SIZE1)
        (PyArrayObject* pyarr=NULL, PyObject* scalar=NULL, Type *buffer=NULL,
                                                           int dimsize[1]),
    (Type **OUT_ARRAY01, SpiceInt *SIZE1)
        (PyArrayObject* pyarr=NULL, PyObject* scalar=NULL, Type *buffer=NULL,
                                                           int dimsize[1])
{
//      (Type **OUT_ARRAY01, int *SIZE1)

    $1 = &buffer;                                               // ARRAY
    $2 = &dimsize[0];                                           // SIZE1
}

/*******************************************************
* %typemap(argout)
* %typemap(freearg)
*******************************************************/

%typemap(in, numinputs=0)
    (Type **OUT_ARRAY01, int *SIZE1),
    (Type **OUT_ARRAY01, SpiceInt *SIZE1)
{}

%typemap(argout)
    (Type **OUT_ARRAY01, int *SIZE1),
    (Type **OUT_ARRAY01, SpiceInt *SIZE1)
{
//      (Type **OUT_ARRAY01, int *SIZE1)

    if (dimsize$argnum[0] == 0) {
        scalar$argnum = Scalarobj(buffer$argnum[0]);
        PyMem_Free((void *) buffer$argnum);

        $result = SWIG_Python_AppendOutput($result, (PyObject *) scalar$argnum);
        Py_INCREF(scalar$argnum);    // Prevents freearg from freeing
    }

    else {
        npy_intp dims$argnum[1] = {dimsize$argnum[0]};
        pyarr$argnum = (PyArrayObject *) PyArray_SimpleNew(1, dims$argnum,
                                                              Typecode);
        TEST_MALLOCFAILURE(pyarr$argnum,0);

        if (buffer$argnum) {
            memcpy(pyarr$argnum->data, buffer$argnum,
                                       dims$argnum[0] * sizeof(Type));
            PyMem_Free((void *) buffer$argnum);

            $result = SWIG_Python_AppendOutput($result,
                                               (PyObject *) pyarr$argnum);
            Py_INCREF(pyarr$argnum);    // Prevents freearg from freeing
        }
        else {
            $result = SWIG_Python_AppendOutput($result, Py_None);
        }
    }
}

%typemap(freearg)
    (Type **OUT_ARRAY01, int *SIZE1),
    (Type **OUT_ARRAY01, SpiceInt *SIZE1)
{
    if (pyarr$argnum) {
        Py_DECREF(pyarr$argnum);
    }
    if (scalar$argnum) {
        Py_DECREF(scalar$argnum);
    }
}

%enddef

/*******************************************************
* Now define these typemaps for every numeric type
*******************************************************/

TYPEMAP_ARGOUT(short,         PyArray_SHORT , PyInt_FromLong)
TYPEMAP_ARGOUT(int,           PyArray_INT   , PyInt_FromLong)
TYPEMAP_ARGOUT(SpiceInt,      PyArray_INT   , PyInt_FromLong)
TYPEMAP_ARGOUT(SpiceBoolean,  PyArray_INT   , PyBool_FromLong)
TYPEMAP_ARGOUT(long,          PyArray_LONG  , PyInt_FromLong)
TYPEMAP_ARGOUT(float,         PyArray_FLOAT , PyFloat_FromDouble)
TYPEMAP_ARGOUT(double,        PyArray_DOUBLE, PyFloat_FromDouble)
TYPEMAP_ARGOUT(SpiceDouble,   PyArray_DOUBLE, PyFloat_FromDouble)

#undef TYPEMAP_ARGOUT

/*******************************************************************************
* 2-D numeric typemaps for output
*
* This family of typemaps allows arrays of numbers returned by C to appear as
* Numpy arrays inside Python.
*
* If the size of the array can be specified in the SWIG interface:
*       (type OUT_ARRAY2[ANY][ANY])
*       (type OUT_ARRAY2[ANY][ANY], int DIM1, int DIM2)
*       (int DIM1, int DIM2, type OUT_ARRAY2[ANY][ANY])
*
* If the upper limit on the size of the array's first axis can be specified in
* the SWIG interface, but the size of the first axis returned by C is variable:
*       (type OUT_ARRAY2[ANY][ANY], int DIM1, int DIM2, int *SIZE1)
*       (type OUT_ARRAY2[ANY][ANY], int *SIZE1, int DIM1, int DIM2)
*       (int DIM1, int DIM2, int *SIZE1, type OUT_ARRAY2[ANY][ANY])
*       (int *SIZE1, int DIM1, int DIM2, type OUT_ARRAY2[ANY][ANY])
*
* If an upper limit on the total size of a temporary memory buffer can be
* specified in advance, and the shape of the array then returned afterward.
* Upon return, the large buffer is freed and only the required amount of memory
* is retained.
*       (type OUT_ARRAY2[ANY][ANY], int *SIZE1, int *SIZE2)
*       (int *SIZE1, int *SIZE2, type OUT_ARRAY2[ANY][ANY])
*
* If the C function will allocate the memory it needs and will return the
* dimensions:
*       (type **OUT_ARRAY2, int *DIM1, int *DIM2)
*       (int *DIM1, int *DIM2, type **OUT_ARRAY2)
*
* This version will return a 1-D array if the first dimension is 0; otherwise
* a 2-D array:
*       (type **OUT_ARRAY12, int *DIM1, int *DIM2)
*******************************************************************************/

%define TYPEMAP_ARGOUT(Type, Typecode) // Use to fill in numeric types below!

/***************************************************************
* (Type OUT_ARRAY2[ANY][ANY])
***************************************************************/

%typemap(check)
    (Type OUT_ARRAY2[ANY][ANY])                                 // PATTERN
        (PyArrayObject* pyarr = NULL, int dimsize[2])
{
//      (Type OUT_ARRAY2[ANY][ANY])

    npy_intp dims$argnum[2] = {$1_dim0, $1_dim1};               // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(2, dims$argnum, Typecode);
    TEST_MALLOCFAILURE(pyarr,1);

    dimsize[0] = (int) dims$argnum[0];
    dimsize[1] = (int) dims$argnum[1];

    $1 = (Type *) pyarr->data;                                  // ARRAY
//  $2 = (int) pyarr->dimensions[0];                            // DIM1
//  $3 = (int) pyarr->dimensions[1];                            // DIM2
//  $4 = &dimsize[0];                                           // SIZE1
//  $5 = &dimsize[1];                                           // SIZE2
}

/***************************************************************
* (Type OUT_ARRAY2[ANY][ANY], int DIM1, int DIM2)
***************************************************************/

%typemap(check)
    (Type OUT_ARRAY2[ANY][ANY], int DIM1, int DIM2)             // PATTERN
        (PyArrayObject* pyarr = NULL, int dimsize[2]),
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2)   // PATTERN
        (PyArrayObject* pyarr = NULL, int dimsize[2])
{
//      (Type OUT_ARRAY2[ANY][ANY], int DIM1, int DIM2)

    npy_intp dims$argnum[2] = {$1_dim0, $1_dim1};               // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(2, dims$argnum, Typecode);
    TEST_MALLOCFAILURE(pyarr,1);

    dimsize[0] = (int) dims$argnum[0];
    dimsize[1] = (int) dims$argnum[1];

    $1 = (Type *) pyarr->data;                                  // ARRAY
    $2 = (int) pyarr->dimensions[0];                            // DIM1
    $3 = (int) pyarr->dimensions[1];                            // DIM2
//  $4 = &dimsize[0];                                           // SIZE1
//  $5 = &dimsize[1];                                           // SIZE2
}

/***************************************************************
* (int DIM1, int DIM2, Type OUT_ARRAY2[ANY][ANY])
***************************************************************/

%typemap(check)
    (int DIM1, int DIM2, Type OUT_ARRAY2[ANY][ANY])             // PATTERN
        (PyArrayObject* pyarr = NULL, int dimsize[2]),
    (SpiceInt DIM1, SpiceInt DIM2, Type OUT_ARRAY2[ANY][ANY])   // PATTERN
        (PyArrayObject* pyarr = NULL, int dimsize[2])
{
//      (int DIM1, int DIM2, Type OUT_ARRAY2[ANY][ANY])

    npy_intp dims$argnum[2] = {$3_dim0, $3_dim1};               // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(2, dims$argnum, Typecode);
    TEST_MALLOCFAILURE(pyarr,1);

    dimsize[0] = (int) dims$argnum[0];
    dimsize[1] = (int) dims$argnum[1];

    $3 = (Type *) pyarr->data;                                  // ARRAY
    $1 = (int) pyarr->dimensions[0];                            // DIM1
    $2 = (int) pyarr->dimensions[1];                            // DIM2
//  $4 = &dimsize[0];                                           // SIZE1
//  $5 = &dimsize[1];                                           // SIZE2
}

/***************************************************************
* (Type OUT_ARRAY2[ANY][ANY], int DIM1, int DIM2, int *SIZE1)
***************************************************************/

%typemap(check)
    (Type OUT_ARRAY2[ANY][ANY], int DIM1, int DIM2, int *SIZE1)
        (PyArrayObject* pyarr = NULL, int dimsize[2]),
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2, SpiceInt *SIZE1)
        (PyArrayObject* pyarr = NULL, int dimsize[2])
{
//      (Type OUT_ARRAY2[ANY][ANY], int DIM1, int DIM2, int *SIZE1)

    npy_intp dims$argnum[2] = {$1_dim0, $1_dim1};               // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(2, dims$argnum, Typecode);
    TEST_MALLOCFAILURE(pyarr,1);

    dimsize[0] = (int) dims$argnum[0];
    dimsize[1] = dim$argnums[1];

    $1 = (Type *) pyarr->data;                                  // ARRAY
    $2 = (int) pyarr->dimensions[0];                            // DIM1
    $3 = (int) pyarr->dimensions[1];                            // DIM2
    $4 = &dimsize[0];                                           // SIZE1
//  $5 = &dimsize[1];                                           // SIZE2

}

/***************************************************************
* (Type OUT_ARRAY2[ANY][ANY], int *SIZE1, int DIM1, int DIM2)
***************************************************************/

%typemap(check)
    (Type OUT_ARRAY2[ANY][ANY], int *SIZE1, int DIM1, int DIM2)
        (PyArrayObject* pyarr = NULL, int dimsize[2]),
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt *SIZE1, SpiceInt DIM1, SpiceInt DIM2)
        (PyArrayObject* pyarr = NULL, int dimsize[2])
{
//      (Type OUT_ARRAY2[ANY][ANY], int *SIZE1, int DIM1, int DIM2)

    npy_intp dims$argnum[2] = {$1_dim0, $1_dim1};               // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(2, dims$argnum, Typecode);
    TEST_MALLOCFAILURE(pyarr,1);

    dimsize[0] = (int) dims$argnum[0];
    dimsize[1] = (int) dims$argnum[1];

    $1 = (Type *) pyarr->data;                                  // ARRAY
    $3 = (int) pyarr->dimensions[0];                            // DIM1
    $4 = (int) pyarr->dimensions[1];                            // DIM2
    $2 = &dimsize[0];                                           // SIZE1
//  $5 = &dimsize[1];                                           // SIZE2
}

/***************************************************************
* (int DIM1, int DIM2, int *SIZE1, Type OUT_ARRAY2[ANY][ANY])
***************************************************************/

%typemap(check)
    (int DIM1, int DIM2, int *SIZE1, Type OUT_ARRAY2[ANY][ANY])
        (PyArrayObject* pyarr = NULL, int dimsize[2]),
    (SpiceInt DIM1, SpiceInt DIM2, SpiceInt *SIZE1, Type OUT_ARRAY2[ANY][ANY])
        (PyArrayObject* pyarr = NULL, int dimsize[2])
{
//      (int DIM1, int DIM2, int *SIZE1, Type OUT_ARRAY2[ANY][ANY])

    npy_intp dims$argnum[2] = {$4_dim0, $4_dim1};               // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(2, dims$argnum, Typecode);
    TEST_MALLOCFAILURE(pyarr,1);

    dimsize[0] = (int) dims$argnum[0];
    dimsize[1] = (int) dims$argnum[1];

    $4 = (Type *) pyarr->data;                                  // ARRAY
    $1 = (int) pyarr->dimensions[0];                            // DIM1
    $2 = (int) pyarr->dimensions[1];                            // DIM2
    $3 = &dimsize[0];                                           // SIZE1
//  $5 = &dimsize[1];                                           // SIZE2
}

/***************************************************************
* (int *SIZE1, int DIM1, int DIM2, Type OUT_ARRAY2[ANY][ANY])
***************************************************************/

%typemap(check)
    (int *SIZE1, int DIM1, int DIM2, Type OUT_ARRAY2[ANY][ANY]),
        (PyArrayObject* pyarr = NULL, int dimsize[2]),
    (SpiceInt *SIZE1, SpiceInt DIM1, SpiceInt DIM2, Type OUT_ARRAY2[ANY][ANY])
        (PyArrayObject* pyarr = NULL, int dimsize[2])
{
//      (int *SIZE1, int DIM1, int DIM2, Type OUT_ARRAY2[ANY][ANY])

    npy_intp dims$argnum[2] = {$4_dim0, $4_dim1};               // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(2, dims$argnum, Typecode);
    TEST_MALLOCFAILURE(pyarr,1);

    dimsize[0] = (int) dims$argnum[0];
    dimsize[1] = (int) dims$argnum[1];

    $4 = (Type *) pyarr->data;                                  // ARRAY
    $2 = (int) pyarr->dimensions[0];                            // DIM1
    $3 = (int) pyarr->dimensions[1];                            // DIM2
    $1 = &dimsize[0];                                           // SIZE1
//  $5 = &dimsize[1];                                           // SIZE2
}

/***************************************************************
* (Type OUT_ARRAY2[ANY][ANY], int *SIZE1)
***************************************************************/

%typemap(check)
    (Type OUT_ARRAY2[ANY][ANY], int *SIZE1)
        (PyArrayObject* pyarr = NULL, int dimsize[2]),
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt *SIZE1)
        (PyArrayObject* pyarr = NULL, int dimsize[2])
{
//      (Type OUT_ARRAY2[ANY][ANY], int *SIZE1)

    npy_intp dims$argnum[2] = {$1_dim0, $1_dim1};               // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(2, dims$argnum, Typecode);
    TEST_MALLOCFAILURE(pyarr,1);

    dimsize[0] = (int) dims$argnum[0];
    dimsize[1] = (int) dims$argnum[1];

    $1 = (Type *) pyarr->data;                                  // ARRAY
//  $3 = (int) pyarr->dimensions[0];                            // DIM1
//  $4 = (int) pyarr->dimensions[1];                            // DIM2
    $2 = &dimsize[0];                                           // SIZE1
//  $5 = &dimsize[1];                                           // SIZE2
}

/***************************************************************
* (int *SIZE1, Type OUT_ARRAY2[ANY][ANY])
***************************************************************/

%typemap(check)
    (int *SIZE1, Type OUT_ARRAY2[ANY][ANY]),
        (PyArrayObject* pyarr = NULL, int dimsize[2]),
    (SpiceInt *SIZE1, Type OUT_ARRAY2[ANY][ANY])
        (PyArrayObject* pyarr = NULL, int dimsize[2])
{
//      (int *SIZE1, Type OUT_ARRAY2[ANY][ANY])

    npy_intp dims$argnum[2] = {$2_dim0, $2_dim1};               // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(2, dims$argnum, Typecode);
    TEST_MALLOCFAILURE(pyarr,1);

    dimsize[0] = (int) dims$argnum[0];
    dimsize[1] = (int) dims$argnum[1];

    $2 = (Type *) pyarr->data;                                  // ARRAY
//  $3 = (int) pyarr->dimensions[0];                            // DIM1
//  $4 = (int) pyarr->dimensions[1];                            // DIM2
    $1 = &dimsize[0];                                           // SIZE1
//  $5 = &dimsize[1];                                           // SIZE2
}

/***************************************************************
* (Type OUT_ARRAY2[ANY][ANY], int *SIZE1, int *SIZE2)
***************************************************************/

%typemap(check)
    (Type OUT_ARRAY2[ANY][ANY], int *SIZE1, int *SIZE2)
        (PyArrayObject* pyarr = NULL, int dimsize[2]),
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt *SIZE1, SpiceInt *SIZE2)
        (PyArrayObject* pyarr = NULL, int dimsize[2])
{
//      (Type OUT_ARRAY2[ANY][ANY], int *SIZE1, int *SIZE2)

    npy_intp dims$argnum[2] = {$1_dim0, $1_dim1};               // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(2, dims$argnum, Typecode);
    TEST_MALLOCFAILURE(pyarr,1);

    dimsize[0] = (int) dims$argnum[0];
    dimsize[1] = (int) dims$argnum[1];

    $1 = (Type *) pyarr->data;                                  // ARRAY
//  $4 = (int) pyarr->dimensions[0];                            // DIM1
//  $5 = (int) pyarr->dimensions[1];                            // DIM2
    $2 = &dimsize[0];                                           // SIZE1
//  $3 = &dimsize[1];                                           // SIZE2
}

/***************************************************************
* (int *SIZE1, int *SIZE2, Type OUT_ARRAY2[ANY][ANY])
***************************************************************/

%typemap(check)
    (int *SIZE1, int *SIZE2, Type OUT_ARRAY2[ANY][ANY])
        (PyArrayObject* pyarr = NULL, int dimsize[2]),
    (SpiceInt *SIZE1, SpiceInt *SIZE2, Type OUT_ARRAY2[ANY][ANY])
        (PyArrayObject* pyarr = NULL, int dimsize[2])
{
//      (int *SIZE1, int *SIZE2, Type OUT_ARRAY2[ANY][ANY])

    npy_intp dims$argnum[2] = {$3_dim0, $3_dim1};               // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(2, dims$argnum, Typecode);
    TEST_MALLOCFAILURE(pyarr,1);

    dimsize[0] = (int) dims$argnum[0];
    dimsize[1] = (int) dims$argnum[1];

    $3 = (Type *) pyarr->data;                                  // ARRAY
//  $4 = (int) pyarr->dimensions[0];                            // DIM1
//  $5 = (int) pyarr->dimensions[1];                            // DIM2
    $1 = &dimsize[0];                                           // SIZE1
//  $2 = &dimsize[1];                                           // SIZE2
}

/*******************************************************
* %typemap(argout)
* %typemap(freearg)
*******************************************************/

%typemap(in, numinputs=0)
    (Type OUT_ARRAY2[ANY][ANY]),
    (Type OUT_ARRAY2[ANY][ANY], int DIM1, int DIM2),
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2),
    (int DIM1, int DIM2, Type OUT_ARRAY2[ANY][ANY]),
    (SpiceInt DIM1, SpiceInt DIM2, Type OUT_ARRAY2[ANY][ANY]),
    (Type OUT_ARRAY2[ANY][ANY], int DIM1, int DIM2, int *SIZE1),
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2, SpiceInt *SIZE1),
    (Type OUT_ARRAY2[ANY][ANY], int *SIZE1, int DIM1, int DIM2),
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt *SIZE1, SpiceInt DIM1, SpiceInt DIM2),
    (int DIM1, int DIM2, int *SIZE1, Type OUT_ARRAY2[ANY][ANY]),
    (SpiceInt DIM1, SpiceInt DIM2, SpiceInt *SIZE1, Type OUT_ARRAY2[ANY][ANY]),
    (int *SIZE1, int DIM1, int DIM2, Type OUT_ARRAY2[ANY][ANY]),
    (SpiceInt *SIZE1, SpiceInt DIM1, SpiceInt DIM2, Type OUT_ARRAY2[ANY][ANY]),
    (Type OUT_ARRAY2[ANY][ANY], int *SIZE1),
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt *SIZE1),
    (int *SIZE1, Type OUT_ARRAY2[ANY][ANY]),
    (SpiceInt *SIZE1, Type OUT_ARRAY2[ANY][ANY]),
    (Type OUT_ARRAY2[ANY][ANY], int *SIZE1, int *SIZE2),
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt *SIZE1, SpiceInt *SIZE2),
    (int *SIZE1, int *SIZE2, Type OUT_ARRAY2[ANY][ANY]),
    (SpiceInt *SIZE1, SpiceInt *SIZE2, Type OUT_ARRAY2[ANY][ANY])
{}

%typemap(argout)
    (Type OUT_ARRAY2[ANY][ANY]),
    (Type OUT_ARRAY2[ANY][ANY], int DIM1, int DIM2),
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2),
    (int DIM1, int DIM2, Type OUT_ARRAY2[ANY][ANY]),
    (SpiceInt DIM1, SpiceInt DIM2, Type OUT_ARRAY2[ANY][ANY])
{
    if (pyarr$argnum) {
        $result = SWIG_Python_AppendOutput($result, (PyObject *) pyarr$argnum);
        Py_INCREF(pyarr$argnum);    // Prevents freearg from freeing
    }
    else {
        $result = SWIG_Python_AppendOutput($result, Py_None);
    }
}

%typemap(argout)
    (Type OUT_ARRAY2[ANY][ANY], int DIM1, int DIM2, int *SIZE1),
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2, SpiceInt *SIZE1),
    (Type OUT_ARRAY2[ANY][ANY], int *SIZE1, int DIM1, int DIM2),
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt *SIZE1, SpiceInt DIM1, SpiceInt DIM2),
    (int DIM1, int DIM2, int *SIZE1, Type OUT_ARRAY2[ANY][ANY]),
    (SpiceInt DIM1, SpiceInt DIM2, SpiceInt *SIZE1, Type OUT_ARRAY2[ANY][ANY]),
    (int *SIZE1, int DIM1, int DIM2, Type OUT_ARRAY2[ANY][ANY]),
    (SpiceInt *SIZE1, SpiceInt DIM1, SpiceInt DIM2, Type OUT_ARRAY2[ANY][ANY]),
    (Type OUT_ARRAY2[ANY][ANY], int *SIZE1),
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt *SIZE1),
    (int *SIZE1, Type OUT_ARRAY2[ANY][ANY]),
    (SpiceInt *SIZE1, Type OUT_ARRAY2[ANY][ANY]),
    (Type OUT_ARRAY2[ANY][ANY], int *SIZE1, int *SIZE2),
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt *SIZE1, SpiceInt *SIZE2),
    (int *SIZE1, int *SIZE2, Type OUT_ARRAY2[ANY][ANY]),
    (SpiceInt *SIZE1, SpiceInt *SIZE2, Type OUT_ARRAY2[ANY][ANY])
{
    npy_intp dims$argnum[2] = {dimsize$argnum[0], dimsize$argnum[1]};
    PyArray_Dims shape = {dims$argnum, 2};

    if (pyarr$argnum) {
        PyArray_Resize(pyarr$argnum, &shape, 0, NPY_CORDER);
        $result = SWIG_Python_AppendOutput($result, (PyObject *) pyarr$argnum);
        Py_INCREF(pyarr$argnum);    // Prevents freearg from freeing
    }
    else {
        $result = SWIG_Python_AppendOutput($result, Py_None);
    }
}

%typemap(freearg)
    (Type OUT_ARRAY2[ANY][ANY]),
    (Type OUT_ARRAY2[ANY][ANY], int DIM1, int DIM2),
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2),
    (int DIM1, int DIM2, Type OUT_ARRAY2[ANY][ANY]),
    (SpiceInt DIM1, SpiceInt DIM2, Type OUT_ARRAY2[ANY][ANY]),
    (Type OUT_ARRAY2[ANY][ANY], int DIM1, int DIM2, int *SIZE1),
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2, SpiceInt *SIZE1),
    (Type OUT_ARRAY2[ANY][ANY], int *SIZE1, int DIM1, int DIM2),
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt *SIZE1, SpiceInt DIM1, SpiceInt DIM2),
    (int DIM1, int DIM2, int *SIZE1, Type OUT_ARRAY2[ANY][ANY]),
    (SpiceInt DIM1, SpiceInt DIM2, SpiceInt *SIZE1, Type OUT_ARRAY2[ANY][ANY]),
    (int *SIZE1, int DIM1, int DIM2, Type OUT_ARRAY2[ANY][ANY]),
    (SpiceInt *SIZE1, SpiceInt DIM1, SpiceInt DIM2, Type OUT_ARRAY2[ANY][ANY]),
    (Type OUT_ARRAY2[ANY][ANY], int *SIZE1),
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt *SIZE1),
    (int *SIZE1, Type OUT_ARRAY2[ANY][ANY]),
    (SpiceInt *SIZE1, Type OUT_ARRAY2[ANY][ANY]),
    (Type OUT_ARRAY2[ANY][ANY], int *SIZE1, int *SIZE2),
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt *SIZE1, SpiceInt *SIZE2),
    (int *SIZE1, int *SIZE2, Type OUT_ARRAY2[ANY][ANY]),
    (SpiceInt *SIZE1, SpiceInt *SIZE2, Type OUT_ARRAY2[ANY][ANY])
{
    if (pyarr$argnum) {
        Py_DECREF(pyarr$argnum);
    }
}

/***************************************************************
* (Type **OUT_ARRAY2, int *SIZE1, int *SIZE2)
***************************************************************/

%typemap(check)
    (Type **OUT_ARRAY2, int *SIZE1, int *SIZE2)
        (PyArrayObject* pyarr=NULL, Type *buffer=NULL, int dimsize[2]),
    (Type **OUT_ARRAY2, SpiceInt *SIZE1, SpiceInt *SIZE2)
        (PyArrayObject* pyarr=NULL, Type *buffer=NULL, int dimsize[2]),
    (Type **OUT_ARRAY12, int *SIZE1, int *SIZE2)
        (PyArrayObject* pyarr=NULL, Type *buffer=NULL, int dimsize[2]),
    (Type **OUT_ARRAY12, SpiceInt *SIZE1, SpiceInt *SIZE2)
        (PyArrayObject* pyarr=NULL, Type *buffer=NULL, int dimsize[2])
{
//      (Type **OUT_ARRAY2, int *SIZE1, int *SIZE2)

    $1 = &buffer;                                               // ARRAY
    $2 = &dimsize[0];                                           // SIZE1
    $3 = &dimsize[1];                                           // SIZE2
}

/***************************************************************
* (int *SIZE1, int *SIZE2, Type **OUT_ARRAY2)
***************************************************************/

%typemap(check)
    (int *SIZE1, int *SIZE2, Type **OUT_ARRAY2)
        (PyArrayObject* pyarr=NULL, Type *buffer=NULL, int dimsize[2]),
    (SpiceInt *SIZE1, SpiceInt *SIZE2, Type **OUT_ARRAY2)
        (PyArrayObject* pyarr=NULL, Type *buffer=NULL, int dimsize[2])
{
//      (int *SIZE1, int *SIZE2, Type **OUT_ARRAY2)

    $3 = &buffer;                                               // ARRAY
    $1 = &dimsize[0];                                           // SIZE1
    $2 = &dimsize[1];                                           // SIZE2
}

/*******************************************************
* %typemap(argout)
* %typemap(freearg)
*******************************************************/

%typemap(in, numinputs=0)
    (Type **OUT_ARRAY2, int *SIZE1, int *SIZE2),
    (Type **OUT_ARRAY2, SpiceInt *SIZE1, SpiceInt *SIZE2),
    (Type **OUT_ARRAY12, int *SIZE1, int *SIZE2),
    (Type **OUT_ARRAY12, SpiceInt *SIZE1, SpiceInt *SIZE2),
    (int *SIZE1, int *SIZE2, Type **OUT_ARRAY2),
    (SpiceInt *SIZE1, SpiceInt *SIZE2, Type **OUT_ARRAY2)
{}

%typemap(argout)
    (Type **OUT_ARRAY2, int *SIZE1, int *SIZE2),
    (Type **OUT_ARRAY2, SpiceInt *SIZE1, SpiceInt *SIZE2),
    (int *SIZE1, int *SIZE2, Type **OUT_ARRAY2),
    (SpiceInt *SIZE1, SpiceInt *SIZE2, Type **OUT_ARRAY2)
{
//      (Type **OUT_ARRAY2, int *SIZE1, int *SIZE2)
//      (int *SIZE1, int *SIZE2, Type **OUT_ARRAY2)

    npy_intp dims$argnum[2] = {dimsize$argnum[0], dimsize$argnum[1]};
    pyarr$argnum = (PyArrayObject *) PyArray_SimpleNew(2, dims$argnum,
                                                          Typecode);
    TEST_MALLOCFAILURE(pyarr$argnum,0);

    if (pyarr$argnum->data) {
        memcpy(pyarr$argnum->data, buffer$argnum,
                               dims$argnum[0] * dims$argnum[1] * sizeof(Type));
        PyMem_Free((void *) buffer$argnum);

        $result = SWIG_Python_AppendOutput($result, (PyObject *) pyarr$argnum);
        Py_INCREF(pyarr$argnum);    // Prevents freearg from freeing
    }
    else {
        $result = SWIG_Python_AppendOutput($result, Py_None);
    }
}

%typemap(argout)
    (Type **OUT_ARRAY12, int *SIZE1, int *SIZE2),
    (Type **OUT_ARRAY12, SpiceInt *SIZE1, SpiceInt *SIZE2)
{
//      (Type **OUT_ARRAY12, int *SIZE1, int *SIZE2)

    npy_intp dims$argnum[2] = {dimsize$argnum[0], dimsize$argnum[1]};
    if (dimsize$argnum[0] == 0) {
        pyarr$argnum = (PyArrayObject *) PyArray_SimpleNew(1, dims$argnum+1,
                                                              Typecode);
    }
    else {
        pyarr$argnum = (PyArrayObject *) PyArray_SimpleNew(2, dims$argnum,
                                                              Typecode);
    }

    TEST_MALLOCFAILURE(pyarr$argnum,0);

    if (buffer$argnum) {
        memcpy(pyarr$argnum->data, buffer$argnum,
               GE1(dims$argnum[0]) * dims$argnum[1] * sizeof(Type));
        PyMem_Free((void *) buffer$argnum);
        $result = SWIG_Python_AppendOutput($result, (PyObject *) pyarr$argnum);
        Py_INCREF(pyarr$argnum);    // Prevents freearg from freeing
    }
    else {
        $result = SWIG_Python_AppendOutput($result, Py_None);
    }
}

%typemap(freearg)
        (Type **OUT_ARRAY2, int *SIZE1, int *SIZE2),
        (Type **OUT_ARRAY2, SpiceInt *SIZE1, SpiceInt *SIZE2),
        (Type **OUT_ARRAY12, int *SIZE1, int *SIZE2),
        (Type **OUT_ARRAY12, SpiceInt *SIZE1, SpiceInt *SIZE2),
        (int *SIZE1, int *SIZE2, Type **OUT_ARRAY2),
        (SpiceInt *SIZE1, SpiceInt *SIZE2, Type **OUT_ARRAY2)
{
    if (pyarr$argnum) {
        Py_DECREF(pyarr$argnum);
    }
}

/*******************************************************
* Now define these typemaps for every numeric type
*******************************************************/

%enddef

TYPEMAP_ARGOUT(char,          PyArray_CHAR  )
TYPEMAP_ARGOUT(SpiceChar,     PyArray_CHAR  )
TYPEMAP_ARGOUT(unsigned char, PyArray_UBYTE )
TYPEMAP_ARGOUT(signed char,   PyArray_SBYTE )
TYPEMAP_ARGOUT(short,         PyArray_SHORT )
TYPEMAP_ARGOUT(int,           PyArray_INT   )
TYPEMAP_ARGOUT(SpiceInt,      PyArray_INT   )
TYPEMAP_ARGOUT(SpiceBoolean,  PyArray_INT   )
TYPEMAP_ARGOUT(long,          PyArray_LONG  )
TYPEMAP_ARGOUT(float,         PyArray_FLOAT )
TYPEMAP_ARGOUT(double,        PyArray_DOUBLE)
TYPEMAP_ARGOUT(SpiceDouble,   PyArray_DOUBLE)
TYPEMAP_ARGOUT(PyObject,      PyArray_OBJECT)

#undef TYPEMAP_ARGOUT

/*******************************************************************************
* Basic 3-D numeric typemaps for output
*       (type **OUT_ARRAY3, int *SIZE1, int *SIZE2, int *SIZE3)
*
* This version returns at 2-D array if the first axis size is zero.
*       (type **OUT_ARRAY23, int *SIZE1, int *SIZE2, int *SIZE3)
*******************************************************************************/

%define TYPEMAP_ARGOUT(Type, Typecode) // Use to fill in numeric types below!

/***************************************************************
* (Type **OUT_ARRAY3, int *SIZE1, int *SIZE2, int *SIZE3)
***************************************************************/

%typemap(check)
    (Type **OUT_ARRAY3, int *SIZE1, int *SIZE2, int *SIZE3)
        (PyArrayObject* pyarr=NULL, Type *buffer=NULL, int dimsize[3]),
    (Type **OUT_ARRAY3, SpiceInt *SIZE1, SpiceInt *SIZE2, SpiceInt *SIZE3)
        (PyArrayObject* pyarr=NULL, Type *buffer=NULL, int dimsize[3]),
    (Type **OUT_ARRAY23, int *SIZE1, int *SIZE2, int *SIZE3)
        (PyArrayObject* pyarr=NULL, Type *buffer=NULL, int dimsize[3]),
    (Type **OUT_ARRAY23, SpiceInt *SIZE1, SpiceInt *SIZE2, SpiceInt *SIZE3)
        (PyArrayObject* pyarr=NULL, Type *buffer=NULL, int dimsize[3])
{
//      (Type **OUT_ARRAY3, int *SIZE1, int *SIZE2, int *SIZE3)

    $1 = &buffer;                                               // ARRAY
    $2 = &dimsize[0];                                           // SIZE1
    $3 = &dimsize[1];                                           // SIZE2
    $4 = &dimsize[2];                                           // SIZE3
}

/*******************************************************
* %typemap(argout)
* %typemap(freearg)
*******************************************************/

%typemap(in, numinputs=0)
    (Type **OUT_ARRAY3, int *SIZE1, int *SIZE2, int *SIZE3),
    (Type **OUT_ARRAY3, SpiceInt *SIZE1, SpiceInt *SIZE2, SpiceInt *SIZE3),
    (Type **OUT_ARRAY23, int *SIZE1, int *SIZE2, int *SIZE3),
    (Type **OUT_ARRAY23, SpiceInt *SIZE1, SpiceInt *SIZE2, SpiceInt *SIZE3)
{}

%typemap(argout)
    (Type **OUT_ARRAY3, int *SIZE1, int *SIZE2, int *SIZE3),
    (Type **OUT_ARRAY3, SpiceInt *SIZE1, SpiceInt *SIZE2, SpiceInt *SIZE3)
{
//      (Type **OUT_ARRAY3, int *SIZE1, int *SIZE2, int *SIZE3)

    npy_intp dims$argnum[3] = {dimsize$argnum[0], dimsize$argnum[1],
                                                  dimsize$argnum[2]};
    pyarr$argnum = (PyArrayObject *) PyArray_SimpleNew(3, dims$argnum,
                                                          Typecode);
    TEST_MALLOCFAILURE(pyarr$argnum,0);

    if (pyarr$argnum) {
        memcpy(pyarr$argnum->data, buffer$argnum,
               dims$argnum[0] * dims$argnum[1] * dims$argnum[2] * sizeof(Type));
        PyMem_Free((void *) buffer$argnum);
        $result = SWIG_Python_AppendOutput($result, (PyObject *) pyarr$argnum);
        Py_INCREF(pyarr$argnum);    // Prevents freearg from freeing
    }
    else {
        $result = SWIG_Python_AppendOutput($result, Py_None);
    }
}

%typemap(argout)
    (Type **OUT_ARRAY23, int *SIZE1, int *SIZE2, int *SIZE3),
    (Type **OUT_ARRAY23, SpiceInt *SIZE1, SpiceInt *SIZE2, SpiceInt *SIZE3)
{
//      (Type **OUT_ARRAY23, int *SIZE1, int *SIZE2, int *SIZE3)

    npy_intp dims$argnum[3] = {dimsize$argnum[0], dimsize$argnum[1],
                                                  dimsize$argnum[2]};
    if (dimsize$argnum[0] == 0) {
        pyarr$argnum = (PyArrayObject *) PyArray_SimpleNew(2, dims$argnum+1,
                                                              Typecode);
//         dimsize$argnum[0] = 1;  // update for memcpy below
    }
    else {
        pyarr$argnum = (PyArrayObject *) PyArray_SimpleNew(3, dims$argnum,
                                                              Typecode);
    }

    TEST_MALLOCFAILURE(pyarr$argnum,0);

    if (buffer$argnum) {
        memcpy(pyarr$argnum->data, buffer$argnum,
               GE1(dims$argnum[0]) * dims$argnum[1] * dims$argnum[2] *
                                                      sizeof(Type));
        PyMem_Free((void *) buffer$argnum);
        $result = SWIG_Python_AppendOutput($result, (PyObject *) pyarr$argnum);
        Py_INCREF(pyarr$argnum);    // Prevents freearg from freeing
    }
    else {
        $result = SWIG_Python_AppendOutput($result, Py_None);
    }
}

%typemap(freearg)
    (Type **OUT_ARRAY3, int *SIZE1, int *SIZE2, int *SIZE3),
    (Type **OUT_ARRAY3, SpiceInt *SIZE1, SpiceInt *SIZE2, SpiceInt *SIZE3),
    (Type **OUT_ARRAY23, int *SIZE1, int *SIZE2, int *SIZE3),
    (Type **OUT_ARRAY23, SpiceInt *SIZE1, SpiceInt *SIZE2, SpiceInt *SIZE3)
{
    if (pyarr$argnum) {
        Py_DECREF(pyarr$argnum);
    }
}

/*******************************************************
* Now define these typemaps for every numeric type
*******************************************************/

%enddef

TYPEMAP_ARGOUT(double,      PyArray_DOUBLE)
TYPEMAP_ARGOUT(SpiceDouble, PyArray_DOUBLE)

#undef TYPEMAP_ARGOUT

/*******************************************************************************
* Numeric typemaps for input/output
*
* This family of typemaps allows the data values in a Numpy array to be
* overwritten by a C function. Care should be exercised: the array must be large
* enough and must be contiguous. The elements could appear in the wrong order if
* the Numpy array uses a non-standard set of strides.
*******************************************************************************/

%define TYPEMAP_INOUT(Type, Typecode) // Use to fill in numeric types below

/*******************************************************
* (Type *INOUT_ARRAY)
*******************************************************/

%typemap(in)
    (Type *INOUT_ARRAY)                                         // PATTERN
{
//      (Type *INOUT_ARRAY)

    PyArrayObject* pyarr = obj_to_array_no_conversion($input, Typecode,
                                                              "$symname");
    TEST_FOR_EXCEPTION;
    TEST_NONCONTIGUOUSARRAY(pyarr,1)

    $1 = (Type *) pyarr->data;                              // ARRAY
}

/*******************************************************
* Now apply to all data types
*******************************************************/

%enddef

// Define concrete examples of the TYPEMAP_IN1 macros
TYPEMAP_INOUT(char,          PyArray_CHAR  )
TYPEMAP_INOUT(SpiceChar,     PyArray_CHAR  )
TYPEMAP_INOUT(unsigned char, PyArray_UBYTE )
TYPEMAP_INOUT(signed char,   PyArray_SBYTE )
TYPEMAP_INOUT(short,         PyArray_SHORT )
TYPEMAP_INOUT(int,           PyArray_INT   )
TYPEMAP_INOUT(SpiceInt,      PyArray_INT   )
TYPEMAP_INOUT(SpiceBoolean,  PyArray_INT   )
TYPEMAP_INOUT(long,          PyArray_LONG  )
TYPEMAP_INOUT(float,         PyArray_FLOAT )
TYPEMAP_INOUT(double,        PyArray_DOUBLE)
TYPEMAP_INOUT(SpiceDouble,   PyArray_DOUBLE)
TYPEMAP_INOUT(PyObject,      PyArray_OBJECT)

#undef TYPEMAP_INOUT

/*******************************************************************************
* Typemap for string input
*
* These typemaps handle string input.
*
*       (char *IN_STRING)
*       (char *CONST_STRING)
*       (char IN_STRING)
*
* The differences between the options are:
*
*       (char *IN_STRING): The string is taken as input. It is copied to ensure
*               that the Python string remains immutable.
*
*       (char *CONST_STRING): The string is taken as input. It is not copied so
*               one must ensure that it does not get changed by the C function.
*
*       (char IN_STRING): If the C function accepts a single character, not a
*               pointer to a string, any you wish to provide the Python input
*               as a string.
*******************************************************************************/

%define TYPEMAP_IN(Type) // Use to fill in types below

/***********************************************
* (Type *IN_STRING)
***********************************************/

%typemap(in) (Type *IN_STRING) {
//      (Type *IN_STRING)
    char *instr = PyString_AsString($input);
    int len = (int) strlen(instr);

    char *buffer = (char *) PyMem_Malloc((len+1) * sizeof(char));
    TEST_MALLOCFAILURE(buffer,1);

    strncpy(buffer, instr, len+1);
    $1 = buffer;
}

%typemap(argout) (char *IN_STRING) {
}

%typemap(freearg) (char *IN_STRING) {
    PyMem_Free((void *) $1);
}

/***********************************************
* (char *CONST_STRING)
***********************************************/

%typemap(in) (Type *CONST_STRING) {
//      (Type *CONST_STRING)
    $1 = PyString_AsString($input);
}

%typemap(argout) (char *CONST_STRING) {
}

%typemap(freearg) (char *CONST_STRING) {
}

/***********************************************
* (char IN_STRING)
***********************************************/

%typemap(in) (Type IN_STRING) {
//      (Type IN_STRING)
    char *instr = PyString_AsString($input);
    $1 = instr[0];
}

%typemap(argout) (Type IN_STRING) {
}

%typemap(freearg) (Type IN_STRING) {
}

/*******************************************************
* Now apply to all data types
*******************************************************/

%enddef

// Define concrete examples of the TYPEMAP_IN macros
TYPEMAP_IN(char)
TYPEMAP_IN(SpiceChar)
TYPEMAP_IN(ConstSpiceChar)

#undef TYPEMAP_IN

/*******************************************************************************
* String typemaps for input and output
*
* These typemaps allow C-format strings to be passed to the C function and for
* a string value to be returned.
*
*       (char INOUT_STRING[ANY])
*       (char *INOUT_STRING)
*
*       (int DIM1, char INOUT_STRING[ANY])
*       (int DIM1, char *INOUT_STRING)
*
*       (char INOUT_STRING[ANY], int DIM1)
*       (char *INOUT_STRING, int DIM1)
*
* The differences between the options are:
*
*       (char *INOUT_STRING): The string is taken as input. A buffer of the
*               size is used to construct the returned string.
*
*       (char INOUT_STRING[ANY]): The string is taken as input. A buffer of the
*               size specified in braces is used to construct the output.
*
* The integer DIM1 parameter carries the dimensioned length of the string.
*******************************************************************************/

/*******************************************************************************
* String typemaps for output
*
* These typemaps allow C-format strings to be returned by the C program as
* Python string values. They are part of the Python return value and do not
* appear as arguments when the function is called from Python.
*
*       (char OUT_STRING[ANY])
*       (char OUT_STRING[ANY], int DIM1)
*       (int DIM1, char OUT_STRING[ANY])
*
* In each case, the dimensioned length of the string is defined in the SWIG
* interface by a number inside the brackets. The differences between the three
* options are:
*
*       (char OUT_STRING[ANY]): one argument to the C function of type char*
*               is consumed; no information about the string's dimensioned
*               length is passed to the function.
*
*       ((char OUT_STRING[ANY], int DIM1): two arguments to the C function are
*               consumed; the dimensioned length of the the character string
*               (which is one greater than the maximum allowed string length)
*               is passed as the next argument after the char* pointer.
*
*       ((int DIM1, char OUT_STRING[ANY]): two arguments to the C function are
*               consumed; the dimensioned length of the the character string is
*               passed as the argument before the char* pointer.
*
* Example:
*
* The C source code:
*
*       void yesno(int status, char *str, int lstr) {
*           if (status) {
*               strncpy(str, "yes", lstr);
*           } else {
*               strncpy(str, "no", lstr);
*           }
*       }
*
* In the interface file:
*
*       %apply (char OUT_STRING[ANY], int LEN) {(char str[4], int lstr)};
*       extern void yesno(int status, char str[4], int lstr);
*
* In Python:
*
*       >>> yesno(3)
*       'yes'
*       >>> yesno(0)
*       'no'
*******************************************************************************/

%define TYPEMAP_INOUT_OUT(Type) // Use to fill in types below

/***********************************************
* (char INOUT_STRING[ANY])
***********************************************/

%typemap(in)
    (Type INOUT_STRING[ANY])                                    // PATTERN
        (Type *buffer = NULL, int dim1)
{
//      (char INOUT_STRING[ANY])

    Type *instr = PyString_AsString($input);
    dim1 = (int) strlen(instr) + 1;

    if (dim1 < $1_dim0) dim1 = $1_dim0;                         // STRING_dim0
    if (dim1 < 2) dim1 = 2;

    buffer = (Type *) PyMem_Malloc(dim1 * sizeof(Type));
    TEST_MALLOCFAILURE(buffer,1);

    strcpy(buffer, instr);
    $1 = buffer;                                                // STRING
//  $2 = dim1; */                                               // DIM1
}

/***********************************************
* (char INOUT_STRING[ANY], int DIM1)
***********************************************/

%typemap(in)
    (Type INOUT_STRING[ANY], int DIM1)                          // PATTERN
        (Type *buffer = NULL, int dim1),
    (Type INOUT_STRING[ANY], SpiceInt DIM1)                     // PATTERN
        (Type *buffer = NULL, SpiceInt dim1)
{
//      (char INOUT_STRING[ANY], int DIM1)

    Type *instr = PyString_AsString($input);
    dim1 = (int) strlen(instr) + 1;

    if (dim1 < $1_dim0) dim1 = $1_dim0;                         // STRING_dim0
    if (dim1 < 2) dim1 = 2;

    buffer = (Type *) PyMem_Malloc(dim1 * sizeof(Type));
    TEST_MALLOCFAILURE(buffer,1);

    strcpy(buffer, instr);
    $1 = buffer;                                                // STRING
    $2 = dim1;                                                  // DIM1
}

/***********************************************
* (int DIM1, char INOUT_STRING[ANY])
***********************************************/

%typemap(in)
    (int DIM1, Type INOUT_STRING[ANY])                          // PATTERN
        (Type *buffer = NULL, int dim1),
    (SpiceInt DIM1, Type INOUT_STRING[ANY])                     // PATTERN
        (Type *buffer = NULL, SpiceInt dim1)
{
//      (int DIM1, char INOUT_STRING[ANY])

    Type *instr = PyString_AsString($input);
    dim1 = (int) strlen(instr) + 1;

    if (dim1 < $2_dim0) dim1 = $2_dim0;                         // STRING_dim0
    if (dim1 < 2) dim1 = 2;

    buffer = (Type *) PyMem_Malloc(dim1 * sizeof(Type));
    TEST_MALLOCFAILURE(buffer,1);

    strcpy(buffer, instr);
    $2 = buffer;                                                // STRING
    $1 = dim1;                                                  // DIM1
}

/***********************************************
* (char *INOUT_STRING)
***********************************************/

%typemap(in)
    (Type *INOUT_STRING)                                        // PATTERN
        (Type *buffer = NULL, int dim1)
{
//      (char *INOUT_STRING)

    Type *instr = PyString_AsString($input);
    dim1 = (int) strlen(instr) + 1;

//  if (dim1 < $1_dim0) dim1 = $1_dim0;                         // STRING_dim0
    if (dim1 < 2) dim1 = 2;

    buffer = (Type *) PyMem_Malloc(dim1 * sizeof(Type));
    TEST_MALLOCFAILURE(buffer,1);

    strcpy(buffer, instr);
    $1 = buffer;                                                // STRING
//  $2 = dim1;                                                  // DIM1
}

/***********************************************
* (char *INOUT_STRING, int DIM1)
***********************************************/

%typemap(in)
    (Type *INOUT_STRING, int DIM1)                              // PATTERN
        (Type *buffer = NULL, int dim1),
    (Type *INOUT_STRING, SpiceInt DIM1)                         // PATTERN
        (Type *buffer = NULL, SpiceInt dim1)
{
//      (char *INOUT_STRING, int DIM1)

    Type *instr = PyString_AsString($input);
    dim1 = (int) strlen(instr) + 1;

    if (dim1 < $1_dim0) dim1 = $1_dim0;                         // STRING_dim0
    if (dim1 < 2) dim1 = 2;

    buffer = (Type *) PyMem_Malloc(dim1 * sizeof(Type));
    TEST_MALLOCFAILURE(buffer,1);

    strcpy(buffer, instr);
    $1 = buffer;                                                // STRING
    $2 = dim1;                                                  // DIM1
}

/***********************************************
* (int DIM1, char *INOUT_STRING)
***********************************************/

%typemap(in)
    (int DIM1, Type *INOUT_STRING)                              // PATTERN
        (Type *buffer = NULL, int dim1),
    (SpiceInt DIM1, Type *INOUT_STRING)                         // PATTERN
        (Type *buffer = NULL, SpiceInt dim1)
{
//      (int DIM1, char *INOUT_STRING)

    char *instr = PyString_AsString($input);
    dim1 = (int) strlen(instr) + 1;

    if (dim1 < $2_dim0) dim1 = $2_dim0;                         // STRING_dim0
    if (dim1 < 2) dim1 = 2;

    buffer = (Type *) PyMem_Malloc(dim1 * sizeof(Type));
    TEST_MALLOCFAILURE(buffer,1);

    strcpy(buffer, instr);
    $2 = buffer;                                                // STRING
    $1 = dim1;                                                  // DIM1
}

/***********************************************
* (char OUT_STRING[ANY])
***********************************************/

%typemap(in, numinputs=0)
    (Type OUT_STRING[ANY])                                      // PATTERN
        (Type *buffer = NULL, int dim1)
{
//      (char OUT_STRING[ANY])

    dim1 = $1_dim0;                                             // STRING_dim0
    if (dim1 < 2) dim1 = 2;

    buffer = (char *) PyMem_Malloc(dim1 * sizeof(char));
    TEST_MALLOCFAILURE(buffer,1);

    buffer[0] = '\0';   // String begins empty
    $1 = buffer;                                                // STRING
//     $2 = dim1;                                               // DIM1
}

/***********************************************
* (char OUT_STRING[ANY], int DIM1)
***********************************************/

%typemap(in, numinputs=0)
    (Type OUT_STRING[ANY], int DIM1)                            // PATTERN
        (Type *buffer = NULL, int dim1),
    (Type OUT_STRING[ANY], SpiceInt DIM1)                       // PATTERN
        (Type *buffer = NULL, SpiceInt dim1)
{
//      (char OUT_STRING[ANY], int DIM1)

    dim1 = $1_dim0;                                             // STRING_dim0
    if (dim1 < 2) dim1 = 2;

    buffer = (Type *) PyMem_Malloc(dim1 * sizeof(Type));
    TEST_MALLOCFAILURE(buffer,1);

    buffer[0] = '\0';   // String begins empty
    $1 = buffer;                                                // STRING
    $2 = dim1;                                                  // DIM1
}

/***********************************************
* (int DIM1, char OUT_STRING[ANY])
***********************************************/

%typemap(in, numinputs=0)
    (int DIM1, Type OUT_STRING[ANY])                            // PATTERN
        (Type *buffer = NULL, int dim1),
    (SpiceInt DIM1, Type OUT_STRING[ANY])                       // PATTERN
        (Type *buffer = NULL, SpiceInt dim1)
{
//      (int DIM1, char OUT_STRING[ANY])

    dim1 = $2_dim0;                                             // STRING_dim0
    if (dim1 < 2) dim1 = 2;

    buffer = (Type *) PyMem_Malloc(dim1 * sizeof(Type));
    TEST_MALLOCFAILURE(buffer,1);

    buffer[0] = '\0';   // String begins empty
    $2 = buffer;                                                // STRING
    $1 = dim1;                                                  // DIM1
}

/*******************************************************
* %typemap(argout)
* %typemap(freearg)
*******************************************************/

%typemap(argout)
    (Type INOUT_STRING[ANY]),
    (Type INOUT_STRING[ANY], int DIM1),
    (Type INOUT_STRING[ANY], SpiceInt DIM1),
    (int DIM1, Type INOUT_STRING[ANY]),
    (SpiceInt DIM1, Type INOUT_STRING[ANY]),
    (Type *INOUT_STRING),
    (Type *INOUT_STRING, int DIM1),
    (Type *INOUT_STRING, SpiceInt DIM1),
    (int DIM1, Type *INOUT_STRING),
    (SpiceInt DIM1, Type *INOUT_STRING),
    (Type OUT_STRING[ANY]),
    (Type OUT_STRING[ANY], int DIM1),
    (Type OUT_STRING[ANY], SpiceInt DIM1),
    (int DIM1, Type OUT_STRING[ANY]),
    (SpiceInt DIM1, Type OUT_STRING[ANY])
{
//      (... Type INOUT_STRING[ANY] ...)
//      (... Type *INOUT_STRING ...)
//      (... Type OUT_STRING[ANY] ...)

    if (buffer$argnum) {
        buffer$argnum[dim1$argnum-1] = '\0';  // Make sure string is terminated
        PyObject *obj = PyString_FromString((Type *) buffer$argnum);
        $result = SWIG_Python_AppendOutput($result, obj);
    }
    else {
        $result = SWIG_Python_AppendOutput($result, Py_None);
    }
}

%typemap(freearg)
    (Type INOUT_STRING[ANY]),
    (Type INOUT_STRING[ANY], int DIM1),
    (Type INOUT_STRING[ANY], SpiceInt DIM1),
    (int DIM1, Type INOUT_STRING[ANY]),
    (SpiceInt DIM1, Type INOUT_STRING[ANY]),
    (Type *INOUT_STRING),
    (Type *INOUT_STRING, int DIM1),
    (Type *INOUT_STRING, SpiceInt DIM1),
    (int DIM1, Type *INOUT_STRING),
    (SpiceInt DIM1, Type *INOUT_STRING),
    (Type OUT_STRING[ANY]),
    (Type OUT_STRING[ANY], int DIM1),
    (Type OUT_STRING[ANY], SpiceInt DIM1),
    (int DIM1, Type OUT_STRING[ANY]),
    (SpiceInt DIM1, Type OUT_STRING[ANY])
{
//      (... Type INOUT_STRING[ANY] ...)
//      (... Type *INOUT_STRING ...)
//      (... Type OUT_STRING[ANY] ...)

    PyMem_Free((void *) buffer$argnum);
}

/*******************************************************
* Now apply to all data types
*******************************************************/

%enddef

// Define concrete examples of the TYPEMAP_IN macros
TYPEMAP_INOUT_OUT(char)
TYPEMAP_INOUT_OUT(SpiceChar)

#undef TYPEMAP_INOUT_OUT

/*******************************************************************************
* String array typemaps for input
*
* These typemaps allow C-format string arrays to be passed into the C function.
*
*       (char *IN_STRINGS, int DIM1, int DIM2)
*       (int DIM1, int DIM2, char *IN_STRINGS)
*
* Because Python strings are immutable, these strings should not be modified by
* the C function.
*******************************************************************************/

%define TYPEMAP_IN(Type) // Use to fill in types below

/***********************************************************************
* (Type *IN_STRINGS, int DIM1, int DIM2)
***********************************************************************/

%typemap(in)
    (Type *IN_STRINGS, int DIM1, int DIM2)
        (Type *buffer),
    (Type *IN_STRINGS, SpiceInt DIM1, SpiceInt DIM2)
        (Type *buffer)
{
//      (Type *IN_STRINGS, int DIM1, int DIM2)

    TEST_INVALIDTYPE_STRING_SEQUENCE($input);

    $1 = NULL;
    $2 = 0;
    $3 = 0;

    if ($input) {
        int dim = (int) PySequence_Length($input);
        int maxlen = 2;
        for (int i = 0; i < dim; i++) {
            PyObject *obj = PySequence_GetItem($input, i);
            int thislen = (int) PyString_Size(obj);
            if (maxlen < thislen) maxlen = thislen;
        }

        buffer = (Type *) PyMem_Malloc(dim * (maxlen+1) * sizeof(Type));
        TEST_MALLOCFAILURE(buffer,1);
        if (buffer) {
            for (int i = 0; i < dim; i++) {
                PyObject *obj = PySequence_GetItem($input, i);
                strncpy((buffer + i*(maxlen+1)), PyString_AsString(obj),
                                                 maxlen+1);
            }

            $1 = buffer;
            $2 = dim;
            $3 = maxlen + 1;
        }
    }
}

/***********************************************************************
* (int DIM1, int DIM2, Type *IN_STRINGS)
***********************************************************************/

%typemap(in)
    (int DIM1, int DIM2, Type *IN_STRINGS)
        (Type *buffer),
    (SpiceInt DIM1, SpiceInt DIM2, Type *IN_STRINGS)
        (Type *buffer)
{
//      (int DIM1, int DIM2, Type *IN_STRINGS)

    TEST_INVALIDTYPE_STRING_SEQUENCE($input);

    $3 = NULL;
    $1 = 0;
    $2 = 0;

    if ($input) {
        int dim = (int) PySequence_Length($input);
        int maxlen = 2;
        for (int i = 0; i < dim; i++) {
            PyObject *obj = PySequence_GetItem($input, i);
            int thislen = (int) PyString_Size(obj);
            if (maxlen < thislen) maxlen = thislen;
        }

        buffer = (Type *) PyMem_Malloc(dim * (maxlen+1) * sizeof(Type));
        TEST_MALLOCFAILURE(buffer,1);

        for (int i = 0; i < dim; i++) {
            PyObject *obj = PySequence_GetItem($input, i);
            strncpy((buffer + i*(maxlen+1)), PyString_AsString(obj), maxlen+1);
        }

        $3 = buffer;
        $1 = dim;
        $2 = maxlen + 1;
    }
}

/***********************************************************************
* %typemap(argout)
* %typemap(freearg)
***********************************************************************/

%typemap(argout)
    (Type *IN_STRINGS, int DIM1, int DIM2),
    (Type *IN_STRINGS, SpiceInt DIM1, SpiceInt DIM2),
    (int DIM1, int DIM2, Type *IN_STRINGS)
    (SpiceInt DIM1, SpiceInt DIM2, Type *IN_STRINGS)
{}

%typemap(freearg)
    (Type *IN_STRINGS, int DIM1, int DIM2),
    (Type *IN_STRINGS, SpiceInt DIM1, SpiceInt DIM2),
    (int DIM1, int DIM2, Type *IN_STRINGS)
    (SpiceInt DIM1, SpiceInt DIM2, Type *IN_STRINGS)
{
    if (buffer$argnum) {
        PyMem_Free((void *) buffer$argnum);
    }
}

/*******************************************************
* Now apply to all data types
*******************************************************/

%enddef

// Define concrete examples of the TYPEMAP_IN macros
TYPEMAP_IN(char)
TYPEMAP_IN(SpiceChar)
TYPEMAP_IN(ConstSpiceChar)

#undef TYPEMAP_IN

/*******************************************************************************
* String array typemaps for output
*
* These typemaps allow C-format string arrays to be returned by the program as
* a list of Python string values. They are part of the return value and do not
* appear as arguments to the Python function.
*
*       (char OUT_STRINGS[ANY][ANY], int DIM1, int DIM1, int *NSTRINGS)
*       (int DIM1, int DIM2, int *NSTRINGS, char OUT_STRINGS[ANY][ANY])
*
* As above, the maximum size and number of strings must be defined in the SWIG
* interface file (to ensure adequate memory is allocated). The typemaps could
* easily be written for alternative orderings of the arguments or for cases
* where one or more arguments are missing.
*******************************************************************************/

%define TYPEMAP_OUT(Type) // Use to fill in types below

/***********************************************************************
* (char OUT_STRINGS[ANY][ANY], int DIM1, int DIM2, int *NSTRINGS)
***********************************************************************/

%typemap(in,numinputs=0)
    (Type OUT_STRINGS[ANY][ANY], int DIM1, int DIM2, int *NSTRINGS)
        (Type *buffer, int dimsize[2]),
    (Type OUT_STRINGS[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2, SpiceInt *NSTRINGS)
        (Type *buffer, int dimsize[2])
{
//      (char OUT_STRINGS[ANY][ANY], int DIM1, int DIM2, int *NSTRINGS)

    dimsize[0] = $1_dim0;                                       // ARRAY_dim0
    dimsize[1] = $1_dim1;                                       // ARRAY_dim1
    if (dimsize[1] < 2) dimsize[1] = 2;

    buffer = (Type *) PyMem_Malloc(dimsize[0] * dimsize[1] * sizeof(Type));
    TEST_MALLOCFAILURE(buffer,1);

    $1 = buffer;                                                // ARRAY
    $2 = dimsize[0];                                            // DIM1
    $3 = dimsize[1];                                            // DIM2
    $4 = &dimsize[0];                                           // NSTRINGS
}

/***********************************************************************
* (int DIM1, int DIM2, int *NSTRINGS, char OUT_STRINGS[ANY][ANY])
***********************************************************************/

%typemap(in,numinputs=0)
    (int DIM1, int DIM2, int *NSTRINGS, Type OUT_STRINGS[ANY][ANY])
        (Type *buffer, int dimsize[2]),
    (SpiceInt DIM1, SpiceInt DIM2, SpiceInt *NSTRINGS, Type OUT_STRINGS[ANY][ANY])
        (Type *buffer, int dimsize[2])
{
//      (int DIM1, int DIM2, int *NSTRINGS, char OUT_STRINGS[ANY][ANY])

    dimsize[0] = $4_dim0;                                       // ARRAY_dim0
    dimsize[1] = $4_dim1;                                       // ARRAY_dim1
    if (dimsize[1] < 2) dimsize[1] = 2;

    buffer = (Type *) PyMem_Malloc(dimsize[0] * dimsize[1] * sizeof(Type));
    TEST_MALLOCFAILURE(buffer,1);

    $4 = buffer;                                                // ARRAY
    $1 = dimsize[0];                                            // DIM1
    $2 = dimsize[1];                                            // DIM2
    $3 = &dimsize[0];                                           // NSTRINGS
}

/***********************************************************************
* %typemap(argout)
* %typemap(freearg)
***********************************************************************/

%typemap(argout)
    (Type OUT_STRINGS[ANY][ANY], int DIM1, int DIM2, int *NSTRINGS),
    (Type OUT_STRINGS[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2, SpiceInt *NSTRINGS),
    (int DIM1, int DIM2, int *NSTRINGS, Type OUT_STRINGS[ANY][ANY]),
    (SpiceInt DIM1, SpiceInt DIM2, SpiceInt *NSTRINGS, Type OUT_STRINGS[ANY][ANY])
{
//      (char OUT_STRINGS[ANY][ANY], int DIM1, int DIM2, int *NSTRINGS)

    // Allocate a Python list with the correct number of elements.
    PyObject *obj = PyList_New(0);

    // Convert the results to Python strings and add them to the list
    for (int i = 0; i < dimsize$argnum[0]; i++) {
        PyList_Append(obj,
                      PyString_FromString((char *) (buffer$argnum +
                                                    i * dimsize$argnum[1])));
    }

    PyObject *wrapper = PyList_New(1);
    PyList_SetItem(wrapper, 0, obj);
    $result = SWIG_Python_AppendOutput($result, wrapper);
}

%typemap(freearg)
    (Type OUT_STRINGS[ANY][ANY], int DIM1, int DIM2, int *NSTRINGS),
    (Type OUT_STRINGS[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2, SpiceInt *NSTRINGS),
    (int DIM1, int DIM2, int *NSTRINGS, Type OUT_STRINGS[ANY][ANY]),
    (SpiceInt DIM1, SpiceInt DIM2, SpiceInt *NSTRINGS, Type OUT_STRINGS[ANY][ANY])
{
//      (char OUT_STRINGS[ANY][ANY], int DIM1, int DIM2, int *NSTRINGS)

    PyMem_Free((void *) buffer$argnum);
}

/*******************************************************
* Now apply to all data types
*******************************************************/

%enddef

// Define concrete examples of the TYPEMAP_IN macros
TYPEMAP_OUT(char)
TYPEMAP_OUT(SpiceChar)

#undef TYPEMAP_OUT

/*******************************************************************************
* Typemap for boolean output
*
*       (Type *OUT_BOOLEAN)
*
* This typemap allows ints to be returned by the program as Python booleans.
* They are part of the return value and do not appear as arguments to the
* Python function. A zero value is False; anything else is True.
*******************************************************************************/

%define TYPEMAP_ARGOUT(Type, Typecode)

%typemap(in, numinputs=0)
    (Type *OUT_BOOLEAN)
        (Type mybool)
{
//      (Type *OUT_BOOLEAN)

    $1 = &mybool;
}

%typemap(argout)
    (Type *OUT_BOOLEAN)
{
//      (Type *OUT_BOOLEAN)

    long test = (*$1 != 0);
    $result = SWIG_Python_AppendOutput($result, PyBool_FromLong(test));
}

%typemap(freearg) (Type *OUT_BOOLEAN) {
}

// Now define these typemaps for every numeric type

%enddef

TYPEMAP_ARGOUT(char,          PyArray_CHAR  )
TYPEMAP_ARGOUT(SpiceChar,     PyArray_CHAR  )
TYPEMAP_ARGOUT(unsigned char, PyArray_UBYTE )
TYPEMAP_ARGOUT(signed char,   PyArray_SBYTE )
TYPEMAP_ARGOUT(short,         PyArray_SHORT )
TYPEMAP_ARGOUT(int,           PyArray_INT   )
TYPEMAP_ARGOUT(SpiceInt,      PyArray_INT   )
TYPEMAP_ARGOUT(SpiceBoolean,  PyArray_INT   )
TYPEMAP_ARGOUT(long,          PyArray_LONG  )
TYPEMAP_ARGOUT(float,         PyArray_FLOAT )
TYPEMAP_ARGOUT(double,        PyArray_DOUBLE)
TYPEMAP_ARGOUT(SpiceDouble,   PyArray_DOUBLE)

#undef TYPEMAP_ARGOUT

/*******************************************************************************
* Typemap for return values. They also check for error status and raise a
* runtime exception if necessary.
*
*       (void   RETURN_VOID   )
*       (int    RETURN_BOOLEAN)
*       (int    RETURN_INT    )
*       (double RETURN_DOUBLE )
*       (char  *RETURN_STRING )
*******************************************************************************/

%typemap(out) (void RETURN_VOID) {

    TEST_FOR_EXCEPTION;
    $result = SWIG_Py_Void();
}

%typemap(out) (int RETURN_BOOLEAN) {

    TEST_FOR_EXCEPTION;
    $result = SWIG_Python_AppendOutput($result, PyBool_FromLong((long) $1));
}

%typemap(out) (SpiceBoolean RETURN_BOOLEAN) {

    TEST_FOR_EXCEPTION;
    $result = SWIG_Python_AppendOutput($result, PyBool_FromLong((long) $1));
}

%typemap(out) (int RETURN_INT) {

    TEST_FOR_EXCEPTION;
    $result = SWIG_Python_AppendOutput($result, PyInt_FromLong((long) $1));
}

%typemap(out) (SpiceInt RETURN_INT) {

    TEST_FOR_EXCEPTION;
    $result = SWIG_Python_AppendOutput($result, PyInt_FromLong((long) $1));
}

%typemap(out) (double RETURN_DOUBLE) {

    TEST_FOR_EXCEPTION;
    $result = SWIG_Python_AppendOutput($result,
                                       PyFloat_FromDouble((double) $1));
}

%typemap(out) (SpiceDouble RETURN_DOUBLE) {

    TEST_FOR_EXCEPTION;
    $result = SWIG_Python_AppendOutput($result,
                                       PyFloat_FromDouble((double) $1));
}

%typemap(out) (char *RETURN_STRING) {

    TEST_FOR_EXCEPTION;
    $result = SWIG_Python_AppendOutput($result,
                                       PyString_FromString((char *) $1));
}

%typemap(out) (SpiceChar *RETURN_STRING) {

    TEST_FOR_EXCEPTION;
    $result = SWIG_Python_AppendOutput($result,
                                       PyString_FromString((char *) $1));
}

// Special handler just for direct calls to sigerr()
%typemap(out) (void RETURN_VOID_SIGERR) {

    RAISE_SIGERR_EXCEPTION;
    $result = SWIG_Py_Void();
}

/*******************************************************************************
*******************************************************************************/
