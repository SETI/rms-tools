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
char* typecode_string(int typecode) {
  char* type_names[20] = {"char","unsigned byte","byte","short",
                          "unsigned short","int","unsigned int","long",
                          "float","double","complex float","complex double",
                          "object","ntype","unkown"};
  return type_names[typecode];
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
PyArrayObject* obj_to_array_no_conversion(PyObject* input, int typecode) {
  PyArrayObject* ary = NULL;
  if (is_array(input) && (typecode == PyArray_NOTYPE || 
                          PyArray_EquivTypenums(array_type(input), 
                                                typecode))) {
        ary = (PyArrayObject*) input;
    }
    else if is_array(input) {
      char* desired_type = typecode_string(typecode);
      char* actual_type = typecode_string(array_type(input));
      PyErr_Format(PyExc_TypeError, 
                   "Array of type '%s' required; array of type '%s' given", 
                   desired_type, actual_type);
      ary = NULL;
    }
    else {
      char * desired_type = typecode_string(typecode);
      char * actual_type = pytype_string(input);
      PyErr_Format(PyExc_TypeError, 
                   "Array of type '%s' required; a %s was given", 
                   desired_type, actual_type);
      ary = NULL;
    }
  return ary;
}

/* Convert the given PyObject to a Numeric array with the given
 * typecode.  On Success, return a valid PyArrayObject* with the
 * correct type.  On failure, the python error string will be set and
 * the routine returns NULL.
 */
PyArrayObject* obj_to_array_allow_conversion(PyObject* input, int typecode,
                                             int* is_new_object)
{
  PyArrayObject* ary = NULL;
  PyObject* py_obj;
  if (is_array(input) && (typecode == PyArray_NOTYPE || type_match(array_type(input),typecode))) {
    ary = (PyArrayObject*) input;
    *is_new_object = 0;
  }
  else {
    py_obj = PyArray_FromObject(input, typecode, 0, 0);
    /* If NULL, PyArray_FromObject will have set python error value.*/
    ary = (PyArrayObject*) py_obj;
    *is_new_object = 1;
  }
  return ary;
}

/* Given a PyArrayObject, check to see if it is contiguous.  If so,
 * return the input pointer and flag it as not a new object.  If it is
 * not contiguous, create a new PyArrayObject using the original data,
 * flag it as a new object and return the pointer.
 */
PyArrayObject* make_contiguous(PyArrayObject* ary, int* is_new_object,
                               int min_dims, int max_dims)
{
  PyArrayObject* result;
  if (array_is_contiguous(ary)) {
    result = ary;
    *is_new_object = 0;
  }
  else {
    result = (PyArrayObject*) PyArray_ContiguousFromObject((PyObject*)ary, 
                                                           array_type(ary), 
                                                           min_dims,
                                                           max_dims);
    *is_new_object = 1;
  }
  return result;
}

/* Convert a given PyObject to a contiguous PyArrayObject of the
 * specified type.  If the input object is not a contiguous
 * PyArrayObject, a new one will be created and the new object flag
 * will be set.
 */
PyArrayObject* obj_to_array_contiguous_allow_conversion(PyObject* input,
                                                        int typecode,
                                                        int* is_new_object) {
  int is_new1 = 0;
  int is_new2 = 0;
  PyArrayObject* ary2;
  PyArrayObject* ary1 = obj_to_array_allow_conversion(input, typecode, 
                                                      &is_new1);
  if (ary1) {
    ary2 = make_contiguous(ary1, &is_new2, 0, 0);
    if ( is_new1 && is_new2) {
      Py_DECREF(ary1);
    }
    ary1 = ary2;    
  }
  *is_new_object = is_new1 || is_new2;
  return ary1;
}

%}

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
* Mark R. Showalter, PDS Rings Node, SETI Institue, July 2009
*******************************************************************************/

%define TYPEMAP_IN(Type, Typecode) // Use to fill in numeric types below

/*******************************************************
* (Type IN_ARRAY1[ANY])
*******************************************************/

%typemap(in)
        (Type IN_ARRAY1[ANY])                                   // PATTERN
                (PyArrayObject* array=NULL, int is_new_object)
{
//      (Type IN_ARRAY1[ANY])

    array = obj_to_array_contiguous_allow_conversion($input, Typecode,
                                                     &is_new_object);
    if (!array) {
        PyErr_SetString(PyExc_TypeError, "Array conversion failure");
        SWIG_fail;
    }

    if (array->nd != 1) {
        PyErr_SetString(PyExc_ValueError, "Array rank is not 1");
        SWIG_fail;
    }

    if (array->dimensions[0] != $1_dim0) {                      // ARRAY_dim0
        PyErr_Format(PyExc_ValueError,
            "Array of shape (%d) was expected; shape (%d) was given",
            $1_dim0, (int) array->dimensions[0]);
        SWIG_fail;
    }

    $1 = (Type *) array->data;                                  // ARRAY
//  $2 = array->dimensions[0];                                  // DIM1
}

/*******************************************************
* (Type IN_ARRAY1[ANY], int DIM1)
*******************************************************/

%typemap(in)
        (Type IN_ARRAY1[ANY], int DIM1)                         // PATTERN
        (PyArrayObject* array=NULL, int is_new_object)
{
//      (Type IN_ARRAY1[ANY], int DIM1)

    array = obj_to_array_contiguous_allow_conversion($input, Typecode,
                                                     &is_new_object);
    if (!array) {
        PyErr_SetString(PyExc_TypeError, "Array conversion failure");
        SWIG_fail;
    }

    if (array->nd != 1) {
        PyErr_SetString(PyExc_ValueError, "Array rank is not 1");
        SWIG_fail;
    }

    if (array->dimensions[0] != $1_dim0) {                      // ARRAY_dim0
        PyErr_Format(PyExc_ValueError,
            "Array of shape (%d) was expected; shape (%d) was given",
            $1_dim0, (int) array->dimensions[0]);
        SWIG_fail;
    }

    $1 = (Type *) array->data;                                  // ARRAY
    $2 = array->dimensions[0];                                  // DIM1
}

/*******************************************************
* (int DIM1, Type IN_ARRAY1[ANY])
*******************************************************/

%typemap(in)
        (int DIM1, Type IN_ARRAY1[ANY])                         // PATTERN
        (PyArrayObject* array=NULL, int is_new_object)
{
//      (int DIM1, Type IN_ARRAY1[ANY])

    array = obj_to_array_contiguous_allow_conversion($input, Typecode,
                                                     &is_new_object);
    if (!array) {
        PyErr_SetString(PyExc_TypeError, "Array conversion failure");
        SWIG_fail;
    }

    if (array->nd != 1) {
        PyErr_SetString(PyExc_ValueError, "Array rank is not 1");
        SWIG_fail;
    }

    if (array->dimensions[0] != $2_dim0) {                      // ARRAY_dim0
        PyErr_Format(PyExc_ValueError,
            "Array of shape (%d) was expected; shape (%d) was given",
            $2_dim0, (int) array->dimensions[0]);
        SWIG_fail;
    }

    $2 = (Type *) array->data;                                  // ARRAY
    $1 = array->dimensions[0];                                  // DIM1
}

/*******************************************************
* (Type *IN_ARRAY1, int DIM1)
*******************************************************/

%typemap(in)
        (Type *IN_ARRAY1, int DIM1)                             // PATTERN
        (PyArrayObject* array=NULL, int is_new_object)
{
//      (Type *IN_ARRAY1, int DIM1)

    array = obj_to_array_contiguous_allow_conversion($input, Typecode,
                                                     &is_new_object);
    if (!array) {
        PyErr_SetString(PyExc_TypeError, "Array conversion failure");
        SWIG_fail;
    }

    if (array->nd != 1) {
        PyErr_SetString(PyExc_ValueError, "Array rank is not 1");
        SWIG_fail;
    }

    $1 = (Type *) array->data;                                  // ARRAY
    $2 = array->dimensions[0];                                  // DIM1
}

/*******************************************************
* (int DIM1, Type *IN_ARRAY1)
*******************************************************/

%typemap(in)
        (int DIM1, Type *IN_ARRAY1)                             // PATTERN
        (PyArrayObject* array=NULL, int is_new_object)
{
//      (int DIM1, Type *IN_ARRAY1)

    array = obj_to_array_contiguous_allow_conversion($input, Typecode,
                                                     &is_new_object);
    if (!array) {
        PyErr_SetString(PyExc_TypeError, "Array conversion failure");
        SWIG_fail;
    }

    if (array->nd != 1) {
        PyErr_SetString(PyExc_ValueError, "Array rank is not 1");
        SWIG_fail;
    }

    $2 = (Type *) array->data;                                  // ARRAY
    $1 = array->dimensions[0];                                  // DIM1
}

/*******************************************************
* %typemap(check)
* %typemap(argout)
* %typemap(freearg)
*******************************************************/

%typemap(check)
        (Type IN_ARRAY1[ANY]),
        (Type IN_ARRAY1[ANY], int DIM1),
        (int DIM1, Type IN_ARRAY1[ANY]),
        (Type *IN_ARRAY1, int DIM1),
        (int DIM1, Type *IN_ARRAY1)
{}

%typemap(argout)
        (Type IN_ARRAY1[ANY]),
        (Type IN_ARRAY1[ANY], int DIM1),
        (int DIM1, Type IN_ARRAY1[ANY]),
        (Type *IN_ARRAY1, int DIM1),
        (int DIM1, Type *IN_ARRAY1)
{}

%typemap(freearg)
        (Type IN_ARRAY1[ANY]),
        (Type IN_ARRAY1[ANY], int DIM1),
        (int DIM1, Type IN_ARRAY1[ANY]),
        (Type *IN_ARRAY1, int DIM1),
        (int DIM1, Type *IN_ARRAY1)
{
//      (Type ...IN_ARRAY1[ANY]...)

    if (is_new_object$argnum && array$argnum) Py_DECREF(array$argnum);
}

/*******************************************************
* Now apply to all data types
*******************************************************/

%enddef

// Define concrete examples of the TYPEMAP_IN1 macros
TYPEMAP_IN(char,          PyArray_CHAR  )
TYPEMAP_IN(unsigned char, PyArray_UBYTE )
TYPEMAP_IN(signed char,   PyArray_SBYTE )
TYPEMAP_IN(short,         PyArray_SHORT )
TYPEMAP_IN(int,           PyArray_INT   )
TYPEMAP_IN(long,          PyArray_LONG  )
TYPEMAP_IN(float,         PyArray_FLOAT )
TYPEMAP_IN(double,        PyArray_DOUBLE)
TYPEMAP_IN(PyObject,      PyArray_OBJECT)

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
* Mark R. Showalter, PDS Rings Node, SETI Institue, July 2009
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
* Mark R. Showalter, PDS Rings Node, SETI Institue, March 2013
*******************************************************************************/

%define TYPEMAP_IN(Type, Typecode) /* Use to fill in numeric types below!

/*******************************************************
* (Type IN_ARRAY2[ANY][ANY])
*******************************************************/

%typemap(in)
        (Type IN_ARRAY2[ANY][ANY])                              // PATTERN
                (PyArrayObject* array=NULL, int is_new_object)
{
//      (Type IN_ARRAY2[ANY][ANY])

    array = obj_to_array_contiguous_allow_conversion($input, Typecode,
                                                     &is_new_object);
    if (!array) {
        PyErr_SetString(PyExc_TypeError, "Array conversion failure");
        SWIG_fail;
    }

    if (array->nd != 2) {
        PyErr_SetString(PyExc_ValueError, "Array rank is not 2");
        SWIG_fail;
    }

    if (array->dimensions[0] != $1_dim0 ||                      // ARRAY_dim0
        array->dimensions[1] != $1_dim1) {                      // ARRAY_dim1
        PyErr_Format(PyExc_ValueError,
            "Array of shape (%d,%d) was expected; shape (%d,%d) was given",
            $1_dim0, $1_dim1, (int) array->dimensions[0],
                              (int) array->dimensions[1]);
        SWIG_fail;
    }

    $1 = (Type *) array->data;                                  // ARRAY
//  $2 = array->dimensions[0];                                  // DIM1
//  $3 = array->dimensions[1];                                  // DIM2
}

/*******************************************************
* (Type IN_ARRAY2[ANY][ANY], int DIM1, int DIM2)
*******************************************************/

%typemap(in)
        (Type IN_ARRAY2[ANY][ANY], int DIM1, int DIM2)          // PATTERN
                (PyArrayObject* array=NULL, int is_new_object)
{
//      (Type IN_ARRAY2[ANY][ANY], int DIM1, int DIM2)

    array = obj_to_array_contiguous_allow_conversion($input, Typecode,
                                                     &is_new_object);
    if (!array) {
        PyErr_SetString(PyExc_TypeError, "Array conversion failure");
        SWIG_fail;
    }

    if (array->nd != 2) {
        PyErr_SetString(PyExc_ValueError, "Array rank is not 2");
        SWIG_fail;
    }

    if (array->dimensions[0] != $1_dim0 ||                      // ARRAY_dim0
        array->dimensions[1] != $1_dim1) {                      // ARRAY_dim1
        PyErr_Format(PyExc_ValueError,
            "Array of shape (%d,%d) was expected; shape (%d,%d) was given",
            $1_dim0, $1_dim1, (int) array->dimensions[0],
                              (int) array->dimensions[1]);
        SWIG_fail;
    }

    $1 = (Type *) array->data;                                  // ARRAY
    $2 = array->dimensions[0];                                  // DIM1
    $3 = array->dimensions[1];                                  // DIM2
}

/*******************************************************
* (int DIM1, int DIM2, Type IN_ARRAY2[ANY][ANY])
*******************************************************/

%typemap(in)
        (int DIM1, int DIM2, Type IN_ARRAY2[ANY][ANY])          // PATTERN
                (PyArrayObject* array=NULL, int is_new_object)
{
//      (int DIM1, int DIM2, Type IN_ARRAY2[ANY][ANY])

    array = obj_to_array_contiguous_allow_conversion($input, Typecode,
                                                     &is_new_object);
    if (!array) {
        PyErr_SetString(PyExc_TypeError, "Array conversion failure");
        SWIG_fail;
    }

    if (array->nd != 2) {
        PyErr_SetString(PyExc_ValueError, "Array rank is not 2");
        SWIG_fail;
    }

    if (array->dimensions[0] != $3_dim0 ||                      // ARRAY_dim0
        array->dimensions[1] != $3_dim1) {                      // ARRAY_dim1
        PyErr_Format(PyExc_ValueError,
            "Array of shape (%d,%d) was expected; shape (%d,%d) was given",
            $3_dim0, $3_dim1, (int) array->dimensions[0],
                              (int) array->dimensions[1]);
        SWIG_fail;
    }

    $3 = (Type *) array->data;                                  // ARRAY
    $1 = array->dimensions[0];                                  // DIM1
    $2 = array->dimensions[1];                                  // DIM2
}

/*******************************************************
* (Type IN_ARRAY2[ANY][ANY], int DIM1)
*******************************************************/

%typemap(in)
        (Type IN_ARRAY2[ANY][ANY], int DIM1)                    // PATTERN
                (PyArrayObject* array=NULL, int is_new_object)
{
//      (Type IN_ARRAY2[ANY][ANY], int DIM1)

    array = obj_to_array_contiguous_allow_conversion($input, Typecode,
                                                     &is_new_object);
    if (!array) {
        PyErr_SetString(PyExc_TypeError, "Array conversion failure");
        SWIG_fail;
    }

    if (array->nd != 2) {
        PyErr_SetString(PyExc_ValueError, "Array rank is not 2");
        SWIG_fail;
    }

    if (array->dimensions[1] != $1_dim1) {                      // ARRAY_dim1
        PyErr_Format(PyExc_ValueError,
            "Array of shape (*,%d) was expected; shape (*,%d) was given",
            $1_dim1, (int) array->dimensions[1]);
        SWIG_fail;
    }

    $1 = (Type *) array->data;                                  // ARRAY
    $2 = array->dimensions[0];                                  // DIM1
}

/*******************************************************
* (int DIM1, Type IN_ARRAY2[ANY][ANY])
*******************************************************/

%typemap(in)
        (int DIM1, Type IN_ARRAY2[ANY][ANY])                    // PATTERN
                (PyArrayObject* array=NULL, int is_new_object)
{
//      (int DIM1, Type IN_ARRAY2[ANY][ANY])

    array = obj_to_array_contiguous_allow_conversion($input, Typecode,
                                                     &is_new_object);
    if (!array) {
        PyErr_SetString(PyExc_TypeError, "Array conversion failure");
        SWIG_fail;
    }

    if (array->nd != 2) {
        PyErr_SetString(PyExc_ValueError, "Array rank is not 2");
        SWIG_fail;
    }

    if (array->dimensions[1] != $2_dim1) {                      // ARRAY_dim1
        PyErr_Format(PyExc_ValueError,
            "Array of shape (*,%d) was expected; shape (*,%d) was given",
            $2_dim1, (int) array->dimensions[1]);
        SWIG_fail;
    }

    $2 = (Type *) array->data;                                  // ARRAY
    $1 = array->dimensions[0];                                  // DIM1
}

/*******************************************************
* (Type *IN_ARRAY2, int DIM1, int DIM2)
*******************************************************/

%typemap(in)
        (Type *IN_ARRAY2, int DIM1, int DIM2)                   // PATTERN
                (PyArrayObject* array=NULL, int is_new_object)
{
//      (Type *IN_ARRAY2, int DIM1, int DIM2)

    array = obj_to_array_contiguous_allow_conversion($input, Typecode,
                                                     &is_new_object);
    if (!array) {
        PyErr_SetString(PyExc_TypeError, "Array conversion failure");
        SWIG_fail;
    }

    if (array->nd != 2) {
        PyErr_SetString(PyExc_ValueError, "Array rank is not 2");
        SWIG_fail;
    }

    $1 = (Type *) array->data;                                  // ARRAY
    $2 = array->dimensions[0];                                  // DIM1
    $3 = array->dimensions[1];                                  // DIM2
}

/*******************************************************
* (int DIM1, int DIM2, Type *IN_ARRAY2)
*******************************************************/

%typemap(in)
        (int DIM1, int DIM2, Type *IN_ARRAY2)                   // PATTERN
                (PyArrayObject* array=NULL, int is_new_object)
{
//      (int DIM1, int DIM2, Type *IN_ARRAY2)

    array = obj_to_array_contiguous_allow_conversion($input, Typecode,
                                                     &is_new_object);
    if (!array) {
        PyErr_SetString(PyExc_TypeError, "Array conversion failure");
        SWIG_fail;
    }

    if (array->nd != 2) {
        PyErr_SetString(PyExc_ValueError, "Array rank is not 2");
        SWIG_fail;
    }

    $3 = (Type *) array->data;                                  // ARRAY
    $1 = array->dimensions[0];                                  // DIM1
    $2 = array->dimensions[1];                                  // DIM2
}

/*******************************************************
* %typemap(check)
* %typemap(argout)
* %typemap(freearg)
*******************************************************/

%typemap(check)
        (Type IN_ARRAY2[ANY][ANY]),
        (Type IN_ARRAY2[ANY][ANY], int DIM1, int DIM2),
        (int DIM1, int DIM2, Type IN_ARRAY2[ANY][ANY]),
        (Type IN_ARRAY2[ANY][ANY], int DIM1),
        (int DIM1, Type IN_ARRAY2[ANY][ANY]),
        (Type *IN_ARRAY2, int DIM1, int DIM2),
        (int DIM1, int DIM2, Type *IN_ARRAY2)
{}

%typemap(argout)
        (Type IN_ARRAY2[ANY][ANY]),
        (Type IN_ARRAY2[ANY][ANY], int DIM1, int DIM2),
        (int DIM1, int DIM2, Type IN_ARRAY2[ANY][ANY]),
        (Type IN_ARRAY2[ANY][ANY], int DIM1),
        (int DIM1, Type IN_ARRAY2[ANY][ANY]),
        (Type *IN_ARRAY2, int DIM1, int DIM2),
        (int DIM1, int DIM2, Type *IN_ARRAY2)
{}

%typemap(freearg)
        (Type IN_ARRAY2[ANY][ANY]),
        (Type IN_ARRAY2[ANY][ANY], int DIM1, int DIM2),
        (int DIM1, int DIM2, Type IN_ARRAY2[ANY][ANY]),
        (Type IN_ARRAY2[ANY][ANY], int DIM1),
        (int DIM1, Type IN_ARRAY2[ANY][ANY]),
        (Type *IN_ARRAY2, int DIM1, int DIM2),
        (int DIM1, int DIM2, Type *IN_ARRAY2)
{
//      (Type ...IN_ARRAY2...)

    if (is_new_object$argnum && array$argnum) Py_DECREF(array$argnum);
}

/*******************************************************
* Now apply to all data types
*******************************************************/

%enddef

// Define concrete examples of the TYPEMAP_IN1 macros
TYPEMAP_IN(char,          PyArray_CHAR  )
TYPEMAP_IN(unsigned char, PyArray_UBYTE )
TYPEMAP_IN(signed char,   PyArray_SBYTE )
TYPEMAP_IN(short,         PyArray_SHORT )
TYPEMAP_IN(int,           PyArray_INT   )
TYPEMAP_IN(long,          PyArray_LONG  )
TYPEMAP_IN(float,         PyArray_FLOAT )
TYPEMAP_IN(double,        PyArray_DOUBLE)
TYPEMAP_IN(PyObject,      PyArray_OBJECT)

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
* Mark R. Showalter, PDS Rings Node, SETI Institue, March 2013
*******************************************************************************/

%define TYPEMAP_IN(Type, Typecode) /* Use to fill in numeric types below!

/*******************************************************
* (Type IN_ARRAY3[ANY][ANY][ANY], int DIM1)
*******************************************************/

%typemap(in)
        (Type IN_ARRAY3[ANY][ANY][ANY], int DIM1)               // PATTERN
                (PyArrayObject* array=NULL, int is_new_object)
{
//      (Type IN_ARRAY3[ANY][ANY][ANY], int DIM1)

    array = obj_to_array_contiguous_allow_conversion($input, Typecode,
                                                     &is_new_object);
    if (!array) {
        PyErr_SetString(PyExc_TypeError, "Array conversion failure");
        SWIG_fail;
    }

    if (array->nd != 3) {
        PyErr_SetString(PyExc_ValueError, "Array rank is not 3");
        SWIG_fail;
    }

    if (array->dimensions[1] != $1_dim1 ||                      // ARRAY_dim1
        array->dimensions[2] != $1_dim2) {                      // ARRAY_dim2
        PyErr_Format(PyExc_ValueError,
            "Array of shape (*,%d,%d) was expected; shape (*,%d,%d) was given",
            $1_dim1, $1_dim2,
            (int) array->dimensions[1],
            (int) array->dimensions[2]);
        SWIG_fail;
    }

    $1 = (Type *) array->data;                                  // ARRAY
    $2 = array->dimensions[0];                                  // DIM1
}

/*******************************************************
* (int DIM1, Type IN_ARRAY3[ANY][ANY][ANY])
*******************************************************/

%typemap(in)
        (int DIM1, Type IN_ARRAY3[ANY][ANY][ANY]) // PATTERN
                (PyArrayObject* array=NULL, int is_new_object)
{
//      (int DIM1, Type IN_ARRAY3[ANY][ANY][ANY])

    array = obj_to_array_contiguous_allow_conversion($input, Typecode,
                                                     &is_new_object);
    if (!array) {
        PyErr_SetString(PyExc_TypeError, "Array conversion failure");
        SWIG_fail;
    }

    if (array->nd != 3) {
        PyErr_SetString(PyExc_ValueError, "Array rank is not 3");
        SWIG_fail;
    }

    if (array->dimensions[1] != $2_dim1 ||                      // ARRAY_dim1
        array->dimensions[2] != $2_dim2) {                      // ARRAY_dim2
        PyErr_Format(PyExc_ValueError,
            "Array of shape (*,%d,%d) was expected; shape (*,%d,%d) was given",
            $2_dim1, $2_dim2,
            (int) array->dimensions[1],
            (int) array->dimensions[2]);                        // ARRAY_dimX
        SWIG_fail;
    }

    $2 = (Type *) array->data;                                  // ARRAY
    $1 = array->dimensions[0];                                  // DIM1
}

/*******************************************************
* (Type *IN_ARRAY3, int DIM1, int DIM2, int DIM3)
*******************************************************/

%typemap(in)
        (Type *IN_ARRAY3, int DIM1, int DIM2, int DIM3)         // PATTERN
                (PyArrayObject* array=NULL, int is_new_object)
{
//      (Type *IN_ARRAY3, int DIM1, int DIM2, int DIM3)

    array = obj_to_array_contiguous_allow_conversion($input, Typecode,
                                                     &is_new_object);
    if (!array) {
        PyErr_SetString(PyExc_TypeError, "Array conversion failure");
        SWIG_fail;
    }

    if (array->nd != 3) {
        PyErr_SetString(PyExc_ValueError, "Array rank is not 3");
        SWIG_fail;
    }

    $1 = (Type *) array->data;                                  // ARRAY
    $2 = array->dimensions[0];                                  // DIM1
    $3 = array->dimensions[1];                                  // DIM2
    $4 = array->dimensions[2];                                  // DIM3
}

/*******************************************************
* (int DIM1, int DIM2, int DIM3, Type *IN_ARRAY3)
*******************************************************/

%typemap(in)
        (int DIM1, int DIM2, int DIM3, Type *IN_ARRAY3)         // PATTERN
                (PyArrayObject* array=NULL, int is_new_object)
{
//      (int DIM1, int DIM2, int DIM3, Type *IN_ARRAY3)

    array = obj_to_array_contiguous_allow_conversion($input, Typecode,
                                                     &is_new_object);
    if (!array) {
        PyErr_SetString(PyExc_TypeError, "Array conversion failure");
        SWIG_fail;
    }

    if (array->nd != 3) {
        PyErr_SetString(PyExc_ValueError, "Array rank is not 3");
        SWIG_fail;
    }

    $4 = (Type *) array->data;                                  // ARRAY
    $1 = array->dimensions[0];                                  // DIM1
    $2 = array->dimensions[1];                                  // DIM2
    $3 = array->dimensions[2];                                  // DIM3
}

/*******************************************************
* %typemap(check)
* %typemap(argout)
* %typemap(freearg)
*******************************************************/

%typemap(check)
        (Type IN_ARRAY3[ANY][ANY][ANY], int DIM1),
        (int DIM1, Type IN_ARRAY3[ANY][ANY][ANY]),
        (Type *IN_ARRAY3, int DIM1, int DIM2, int DIM3),
        (int DIM1, int DIM2, int DIM3, Type *IN_ARRAY3)
{}

%typemap(argout)
        (Type IN_ARRAY3[ANY][ANY][ANY], int DIM1),
        (int DIM1, Type IN_ARRAY3[ANY][ANY][ANY]),
        (Type *IN_ARRAY3, int DIM1, int DIM2, int DIM3),
        (int DIM1, int DIM2, int DIM3, Type *IN_ARRAY3)
{}

%typemap(freearg)
        (Type IN_ARRAY3[ANY][ANY][ANY], int DIM1),
        (int DIM1, Type IN_ARRAY3[ANY][ANY][ANY]),
        (Type *IN_ARRAY3, int DIM1, int DIM2, int DIM3),
        (int DIM1, int DIM2, int DIM3, Type *IN_ARRAY3)
{
//      (Type ...IN_ARRAY3...)

    if (is_new_object$argnum && array$argnum) Py_DECREF(array$argnum);
}

/*******************************************************
* Now apply to all data types
*******************************************************/

%enddef

// Define concrete examples of the TYPEMAP_IN1 macros
TYPEMAP_IN(char,          PyArray_CHAR  )
TYPEMAP_IN(unsigned char, PyArray_UBYTE )
TYPEMAP_IN(signed char,   PyArray_SBYTE )
TYPEMAP_IN(short,         PyArray_SHORT )
TYPEMAP_IN(int,           PyArray_INT   )
TYPEMAP_IN(long,          PyArray_LONG  )
TYPEMAP_IN(float,         PyArray_FLOAT )
TYPEMAP_IN(double,        PyArray_DOUBLE)
TYPEMAP_IN(PyObject,      PyArray_OBJECT)

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
*
* Mark R. Showalter, PDS Rings Node, SETI Institue, July 2009
*******************************************************************************/

%define TYPEMAP_ARGOUT(Type, Typecode) // Use to fill in numeric types below!

/*******************************************************
* (Type OUT_ARRAY1[ANY])
*******************************************************/

%typemap(check)
        (Type OUT_ARRAY1[ANY])                                  // PATTERN
                (PyArrayObject* array = NULL, int size[1])
{
//      (Type OUT_ARRAY1[ANY])

    npy_intp dims$argnum[1] = {$1_dim0};                        // ARRAY
    array = PyArray_SimpleNew(1, dims$argnum, Typecode);
    if (!array) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
        SWIG_fail;
    }

    $1 = (Type *) array->data;                                  // ARRAY
//  $2 = array->dimensions[0];                                  // DIM1
//  $3 = &size[0];                                              // SIZE1
}

/*******************************************************
* (Type OUT_ARRAY1[ANY], int DIM1)
*******************************************************/

%typemap(check)
        (Type OUT_ARRAY1[ANY], int DIM1)                        // PATTERN
                (PyArrayObject* array = NULL, int size[1])
{
//      (Type OUT_ARRAY1[ANY], int DIM1)

    npy_intp dims$argnum[1] = {$1_dim0};                        // ARRAY
    array = PyArray_SimpleNew(1, dims$argnum, Typecode);
    if (!array) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
        SWIG_fail;
    }

    $1 = (Type *) array->data;                                  // ARRAY
    $2 = array->dimensions[0];                                  // DIM1
//  $3 = &size[0];                                              // SIZE1
}

/*******************************************************
* (int DIM1, Type OUT_ARRAY1[ANY])
*******************************************************/

%typemap(check)
        (int DIM1, Type OUT_ARRAY1[ANY])                        // PATTERN
                (PyArrayObject* array = NULL, int size[1])
{
//      (int DIM1, Type OUT_ARRAY1[ANY])

    npy_intp dims$argnum[1] = {$2_dim0};                        // ARRAY
    array = PyArray_SimpleNew(1, dims$argnum, Typecode);
    if (!array) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
        SWIG_fail;
    }

    $2 = (Type *) array->data;                                  // ARRAY
    $1 = array->dimensions[0];                                  // DIM1
//  $3 = &size[0];                                              // SIZE1
}

/*******************************************************
* (Type OUT_ARRAY1[ANY], int DIM1, int *SIZE1)
*******************************************************/

%typemap(check)
        (Type OUT_ARRAY1[ANY], int DIM1, int *SIZE1)            // PATTERN
                (PyArrayObject* array = NULL, int size[1]),
        (Type OUT_ARRAY1[ANY], int DIM1, long *SIZE1)           // PATTERN
                (PyArrayObject* array = NULL, long size[1])
{
//      (Type OUT_ARRAY1[ANY], int DIM1, int *SIZE1)

    npy_intp dims$argnum[1] = {$1_dim0};                        // ARRAY
    array = PyArray_SimpleNew(1, dims$argnum, Typecode);
    if (!array) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
        SWIG_fail;
    }

    $1 = (Type *) array->data;                                  // ARRAY
    $2 = array->dimensions[0];                                  // DIM1
    $3 = &size[0];                                              // SIZE1
}

/*******************************************************
* (Type OUT_ARRAY1[ANY], int *SIZE1, int DIM1)
*******************************************************/

%typemap(check)
        (Type OUT_ARRAY1[ANY], int *SIZE1, int DIM1)            // PATTERN
                (PyArrayObject* array = NULL, int size[1]),
        (Type OUT_ARRAY1[ANY], long *SIZE1, int DIM1)           // PATTERN
                (PyArrayObject* array = NULL, long size[1])
{
//      (Type OUT_ARRAY1[ANY], int *SIZE1, int DIM1)

    npy_intp dims$argnum[1] = {$1_dim0};                        // ARRAY
    array = PyArray_SimpleNew(1, dims$argnum, Typecode);
    if (!array) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
        SWIG_fail;
    }

    $1 = (Type *) array->data;                                  // ARRAY
    $3 = array->dimensions[0];                                  // DIM1
    $2 = &size[0];                                              // SIZE1
}

/*******************************************************
* (int DIM1, int *SIZE1, Type OUT_ARRAY1[ANY])
*******************************************************/

%typemap(check)
        (int DIM1, int *SIZE1, Type OUT_ARRAY1[ANY])            // PATTERN
                (PyArrayObject* array = NULL, int size[1]),
        (int DIM1, long *SIZE1, Type OUT_ARRAY1[ANY])           // PATTERN
                (PyArrayObject* array = NULL, long size[1])
{
//      (int DIM1, int *SIZE1, Type OUT_ARRAY1[ANY])

    npy_intp dims$argnum[1] = {$3_dim0};                       // ARRAY
    array = PyArray_SimpleNew(1, dims$argnum, Typecode);
    if (!array) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
        SWIG_fail;
    }

    $3 = (Type *) array->data;                                  // ARRAY
    $1 = array->dimensions[0];                                  // DIM1
    $2 = &size[0];                                              // SIZE1
}

/*******************************************************
* (int *SIZE1, int DIM1, Type OUT_ARRAY1[ANY])
*******************************************************/

%typemap(check)
        (int *SIZE1, int DIM1, Type OUT_ARRAY1[ANY])            // PATTERN
                (PyArrayObject* array = NULL, int size[1]),
        (long *SIZE1, int DIM1, Type OUT_ARRAY1[ANY])           // PATTERN
                (PyArrayObject* array = NULL, long size[1])
{
//      (int *SIZE1, int DIM1, Type OUT_ARRAY1[ANY])

    npy_intp dims$argnum[1] = {$3_dim0};                        // ARRAY
    array = PyArray_SimpleNew(1, dims$argnum, Typecode);
    if (!array) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
        SWIG_fail;
    }

    $3 = (Type *) array->data;                                  // ARRAY
    $2 = array->dimensions[0];                                  // DIM1
    $1 = &size[0];                                              // SIZE1
}

/*******************************************************
* (Type OUT_ARRAY1[ANY], int *SIZE1)
*******************************************************/

%typemap(check)
        (Type OUT_ARRAY1[ANY], int *SIZE1)                      // PATTERN
                (PyArrayObject* array = NULL, int size[1]),
        (Type OUT_ARRAY1[ANY], long *SIZE1)                     // PATTERN
                (PyArrayObject* array = NULL, long size[1])
{
//      (Type OUT_ARRAY1[ANY], int *SIZE1)

    npy_intp dims$argnum[1] = {$1_dim0};                        // ARRAY
    array = PyArray_SimpleNew(1, dims$argnum, Typecode);
    if (!array) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
        SWIG_fail;
    }

    $1 = (Type *) array->data;                                  // ARRAY
//  $3 = array->dimensions[0];                                  // DIM1
    $2 = &size[0];                                              // SIZE1
}

/*******************************************************
* (int *SIZE1, Type OUT_ARRAY1[ANY])
*******************************************************/

%typemap(check)
        (int *SIZE1, Type OUT_ARRAY1[ANY])                      // PATTERN
                (PyArrayObject* array = NULL, int size[1]),
        (long *SIZE1, Type OUT_ARRAY1[ANY])                     // PATTERN
                (PyArrayObject* array = NULL, long size[1])
{
//      (int *SIZE1, Type OUT_ARRAY1[ANY])

    npy_intp dims$argnum[1] = {$2_dim0};                        // ARRAY
    array = PyArray_SimpleNew(1, dims$argnum, Typecode);
    if (!array) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
        SWIG_fail;
    }

    $2 = (Type *) array->data;                                  // ARRAY
//  $3 = array->dimensions[0];                                  // DIM1
    $1 = &size[0];                                              // SIZE1
}

/*******************************************************
* %typemap(argout)
* %typemap(freearg)
*******************************************************/

%typemap(in, numinputs=0)
        (Type OUT_ARRAY1[ANY]),
        (Type OUT_ARRAY1[ANY], int DIM1),
        (int DIM1, Type OUT_ARRAY1[ANY]),
        (Type OUT_ARRAY1[ANY], int DIM1, int  *SIZE1),
        (Type OUT_ARRAY1[ANY], int DIM1, long *SIZE1),
        (Type OUT_ARRAY1[ANY], int  *SIZE1, int DIM1),
        (Type OUT_ARRAY1[ANY], long *SIZE1, int DIM1),
        (int DIM1, int *SIZE1, Type OUT_ARRAY1[ANY]),
        (int DIM1, long *SIZE1, Type OUT_ARRAY1[ANY]),
        (int *SIZE1, int DIM1, Type OUT_ARRAY1[ANY]),
        (long *SIZE1, int DIM1, Type OUT_ARRAY1[ANY]),
        (Type OUT_ARRAY1[ANY], int  *SIZE1),
        (Type OUT_ARRAY1[ANY], long *SIZE1),
        (int  *SIZE1, Type OUT_ARRAY1[ANY]),
        (long *SIZE1, Type OUT_ARRAY1[ANY])
{}

%typemap(argout)
        (Type OUT_ARRAY1[ANY]),
        (Type OUT_ARRAY1[ANY], int DIM1),
        (int DIM1, Type OUT_ARRAY1[ANY])
{
    $result = SWIG_Python_AppendOutput($result, array$argnum);
    Py_INCREF(array$argnum);    // Prevents freearg from freeing
}

%typemap(argout)
        (Type OUT_ARRAY1[ANY], int DIM1, int  *SIZE1),
        (Type OUT_ARRAY1[ANY], int DIM1, long *SIZE1),
        (Type OUT_ARRAY1[ANY], int  *SIZE1, int DIM1),
        (Type OUT_ARRAY1[ANY], long *SIZE1, int DIM1),
        (int DIM1, int *SIZE1, Type OUT_ARRAY1[ANY]),
        (int DIM1, long *SIZE1, Type OUT_ARRAY1[ANY]),
        (int *SIZE1, int DIM1, Type OUT_ARRAY1[ANY]),
        (long *SIZE1, int DIM1, Type OUT_ARRAY1[ANY]),
        (Type OUT_ARRAY1[ANY], int  *SIZE1),
        (Type OUT_ARRAY1[ANY], long *SIZE1),
        (int  *SIZE1, Type OUT_ARRAY1[ANY]),
        (long *SIZE1, Type OUT_ARRAY1[ANY])
{
    npy_intp dims$argnum[1] = {size$argnum[0]};
    PyArray_Dims shape = {dims$argnum, 1};
    PyArray_Resize(array$argnum, &shape, 0, NPY_CORDER);

    $result = SWIG_Python_AppendOutput($result, array$argnum);
    Py_INCREF(array$argnum);    // Prevents freearg from freeing
}

%typemap(freearg)
        (Type OUT_ARRAY1[ANY]),
        (Type OUT_ARRAY1[ANY], int DIM1),
        (int DIM1, Type OUT_ARRAY1[ANY]),
        (Type OUT_ARRAY1[ANY], int DIM1, int  *SIZE1),
        (Type OUT_ARRAY1[ANY], int DIM1, long *SIZE1),
        (Type OUT_ARRAY1[ANY], int  *SIZE1, int DIM1),
        (Type OUT_ARRAY1[ANY], long *SIZE1, int DIM1),
        (int DIM1, int *SIZE1, Type OUT_ARRAY1[ANY]),
        (int DIM1, long *SIZE1, Type OUT_ARRAY1[ANY]),
        (int *SIZE1, int DIM1, Type OUT_ARRAY1[ANY]),
        (long *SIZE1, int DIM1, Type OUT_ARRAY1[ANY]),
        (Type OUT_ARRAY1[ANY], int  *SIZE1),
        (Type OUT_ARRAY1[ANY], long *SIZE1),
        (int  *SIZE1, Type OUT_ARRAY1[ANY]),
        (long *SIZE1, Type OUT_ARRAY1[ANY])
{
    if (array$argnum) {
        Py_DECREF(array$argnum);
    }
}

/***************************************************************
* (Type **OUT_ARRAY1, int *SIZE1)
***************************************************************/

%typemap(check)
        (Type **OUT_ARRAY1, int *SIZE1)
                (PyArrayObject* array=NULL, Type *buffer=NULL, int dimsize[1]),
        (Type **OUT_ARRAY1, long *SIZE1)
                (PyArrayObject* array=NULL, Type *buffer=NULL, long dimsize[1])
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
                (PyArrayObject* array=NULL, Type *buffer=NULL, int dimsize[1]),
        (long *SIZE1, Type **OUT_ARRAY1)
                (PyArrayObject* array=NULL, Type *buffer=NULL, long dimsize[1])
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
        (Type **OUT_ARRAY1, long *SIZE1),
        (int *SIZE1, Type **OUT_ARRAY1),
        (long *SIZE1, Type **OUT_ARRAY1)
{}

%typemap(argout)
        (Type **OUT_ARRAY1, int *SIZE1),
        (Type **OUT_ARRAY1, long *SIZE1),
        (int *SIZE1, Type **OUT_ARRAY1),
        (long *SIZE1, Type **OUT_ARRAY1)
{
//      (Type **OUT_ARRAY1, int *SIZE1)
//      (int *SIZE1, Type **OUT_ARRAY1)

    npy_intp dims$argnum[1] = {dimsize$argnum[0]};
    array$argnum = PyArray_SimpleNew(1, dims$argnum, Typecode);
    if (!array$argnum) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
        SWIG_fail;
    }

    memcpy(array$argnum->data, buffer$argnum, dims$argnum[0] * sizeof(Type));  
    PyMem_Free((void *) buffer$argnum);

    $result = SWIG_Python_AppendOutput($result, array$argnum);
    Py_INCREF(array$argnum);    // Prevents freearg from freeing
}

%typemap(freearg)
        (Type **OUT_ARRAY1, int *SIZE1),
        (Type **OUT_ARRAY1, long *SIZE1),
        (int *SIZE1, Type **OUT_ARRAY1),
        (long *SIZE1, Type **OUT_ARRAY1)
{
    if (array$argnum) {
        Py_DECREF(array$argnum);
    }
}

/*******************************************************
* Now define these typemaps for every numeric type
*******************************************************/

%enddef

TYPEMAP_ARGOUT(char,          PyArray_CHAR  )
TYPEMAP_ARGOUT(unsigned char, PyArray_UBYTE )
TYPEMAP_ARGOUT(signed char,   PyArray_SBYTE )
TYPEMAP_ARGOUT(short,         PyArray_SHORT )
TYPEMAP_ARGOUT(int,           PyArray_INT   )
TYPEMAP_ARGOUT(long,          PyArray_LONG  )
TYPEMAP_ARGOUT(float,         PyArray_FLOAT )
TYPEMAP_ARGOUT(double,        PyArray_DOUBLE)
TYPEMAP_ARGOUT(PyObject,      PyArray_OBJECT)

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
* Mark R. Showalter, PDS Rings Node, SETI Institue, July 2009
*******************************************************************************/

%define TYPEMAP_ARGOUT(Type, Typecode) // Use to fill in numeric types below!

/***************************************************************
* (Type OUT_ARRAY2[ANY][ANY])
***************************************************************/

%typemap(check)
        (Type OUT_ARRAY2[ANY][ANY])                             // PATTERN
                (PyArrayObject* array = NULL, int dimsize[2])
{
//      (Type OUT_ARRAY2[ANY][ANY])

    npy_intp dims$argnum[2] = {$1_dim0, $1_dim1};               // ARRAY
    array = PyArray_SimpleNew(2, dims$argnum, Typecode);
    if (!array) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
        SWIG_fail;
    }

    dimsize[0] = dims$argnum[0];
    dimsize[1] = dims$argnum[1];

    $1 = (Type *) array->data;                                  // ARRAY
//  $2 = array->dimensions[0];                                  // DIM1
//  $3 = array->dimensions[1];                                  // DIM2
//  $4 = &dimsize[0];                                           // SIZE1
//  $5 = &dimsize[1];                                           // SIZE2
}

/***************************************************************
* (Type OUT_ARRAY2[ANY][ANY], int DIM1, int DIM2)
***************************************************************/

%typemap(check)
        (Type OUT_ARRAY2[ANY][ANY], int DIM1, int DIM2)         // PATTERN
                (PyArrayObject* array = NULL, int dimsize[2])
{
//      (Type OUT_ARRAY2[ANY][ANY], int DIM1, int DIM2)

    npy_intp dims$argnum[2] = {$1_dim0, $1_dim1};               // ARRAY
    array = PyArray_SimpleNew(2, dims$argnum, Typecode);
    if (!array) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
        SWIG_fail;
    }

    dimsize[0] = dims$argnum[0];
    dimsize[1] = dims$argnum[1];

    $1 = (Type *) array->data;                                  // ARRAY
    $2 = array->dimensions[0];                                  // DIM1
    $3 = array->dimensions[1];                                  // DIM2
//  $4 = &dimsize[0];                                           // SIZE1
//  $5 = &dimsize[1];                                           // SIZE2
}

/***************************************************************
* (int DIM1, int DIM2, Type OUT_ARRAY2[ANY][ANY])
***************************************************************/

%typemap(check)
        (int DIM1, int DIM2, Type OUT_ARRAY2[ANY][ANY])         // PATTERN
                (PyArrayObject* array = NULL, int dimsize[2])
{
//      (int DIM1, int DIM2, Type OUT_ARRAY2[ANY][ANY])

    npy_intp dims$argnum[2] = {$3_dim0, $3_dim1};               // ARRAY
    array = PyArray_SimpleNew(2, dims$argnum, Typecode);
    if (!array) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
        SWIG_fail;
    }

    dimsize[0] = dims$argnum[0];
    dimsize[1] = dims$argnum[1];

    $3 = (Type *) array->data;                                  // ARRAY
    $1 = array->dimensions[0];                                  // DIM1
    $2 = array->dimensions[1];                                  // DIM2
//  $4 = &dimsize[0];                                           // SIZE1
//  $5 = &dimsize[1];                                           // SIZE2
}

/***************************************************************
* (Type OUT_ARRAY2[ANY][ANY], int DIM1, int DIM2, int *SIZE1)
***************************************************************/

%typemap(check)
        (Type OUT_ARRAY2[ANY][ANY], int DIM1, int DIM2, int *SIZE1)
                (PyArrayObject* array = NULL, int dimsize[2]),
        (Type OUT_ARRAY2[ANY][ANY], int DIM1, int DIM2, long *SIZE1)
                (PyArrayObject* array = NULL, long dimsize[2])
{
//      (Type OUT_ARRAY2[ANY][ANY], int DIM1, int DIM2, int *SIZE1)

    npy_intp dims$argnum[2] = {$1_dim0, $1_dim1};               // ARRAY
    array = PyArray_SimpleNew(2, dims$argnum, Typecode);
    if (!array) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
        SWIG_fail;
    }

    dimsize[0] = dims$argnum[0];
    dimsize[1] = dim$argnums[1];

    $1 = (Type *) array->data;                                  // ARRAY
    $2 = array->dimensions[0];                                  // DIM1
    $3 = array->dimensions[1];                                  // DIM2
    $4 = &dimsize[0];                                           // SIZE1
//  $5 = &dimsize[1];                                           // SIZE2
}

/***************************************************************
* (Type OUT_ARRAY2[ANY][ANY], int *SIZE1, int DIM1, int DIM2)
***************************************************************/

%typemap(check)
        (Type OUT_ARRAY2[ANY][ANY], int *SIZE1, int DIM1, int DIM2)
                (PyArrayObject* array = NULL, int dimsize[2]),
        (Type OUT_ARRAY2[ANY][ANY], long *SIZE1, int DIM1, int DIM2)
                (PyArrayObject* array = NULL, long dimsize[2])
{
//      (Type OUT_ARRAY2[ANY][ANY], int *SIZE1, int DIM1, int DIM2)

    npy_intp dims$argnum[2] = {$1_dim0, $1_dim1};               // ARRAY
    array = PyArray_SimpleNew(2, dims$argnum, Typecode);
    if (!array) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
        SWIG_fail;
    }

    dimsize[0] = dims$argnum[0];
    dimsize[1] = dims$argnum[1];

    $1 = (Type *) array->data;                                  // ARRAY
    $3 = array->dimensions[0];                                  // DIM1
    $4 = array->dimensions[1];                                  // DIM2
    $2 = &dimsize[0];                                           // SIZE1
//  $5 = &dimsize[1];                                           // SIZE2
}

/***************************************************************
* (int DIM1, int DIM2, int *SIZE1, Type OUT_ARRAY2[ANY][ANY])
***************************************************************/

%typemap(check)
        (int DIM1, int DIM2, int *SIZE1, Type OUT_ARRAY2[ANY][ANY])
                (PyArrayObject* array = NULL, int dimsize[2]),
        (int DIM1, int DIM2, long *SIZE1, Type OUT_ARRAY2[ANY][ANY])
                (PyArrayObject* array = NULL, long dimsize[2])
{
//      (int DIM1, int DIM2, int *SIZE1, Type OUT_ARRAY2[ANY][ANY])

    npy_intp dims$argnum[2] = {$4_dim0, $4_dim1};               // ARRAY
    array = PyArray_SimpleNew(2, dims$argnum, Typecode);
    if (!array) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
        SWIG_fail;
    }

    dimsize[0] = dims$argnum[0];
    dimsize[1] = dims$argnum[1];

    $4 = (Type *) array->data;                                  // ARRAY
    $1 = array->dimensions[0];                                  // DIM1
    $2 = array->dimensions[1];                                  // DIM2
    $3 = &dimsize[0];                                           // SIZE1
//  $5 = &dimsize[1];                                           // SIZE2
}

/***************************************************************
* (int *SIZE1, int DIM1, int DIM2, Type OUT_ARRAY2[ANY][ANY])
***************************************************************/

%typemap(check)
        (int *SIZE1, int DIM1, int DIM2, Type OUT_ARRAY2[ANY][ANY]),
                (PyArrayObject* array = NULL, int dimsize[2]),
        (long *SIZE1, int DIM1, int DIM2, Type OUT_ARRAY2[ANY][ANY])
                (PyArrayObject* array = NULL, long dimsize[2])
{
//      (int *SIZE1, int DIM1, int DIM2, Type OUT_ARRAY2[ANY][ANY])

    npy_intp dims$argnum[2] = {$4_dim0, $4_dim1};               // ARRAY
    array = PyArray_SimpleNew(2, dims$argnum, Typecode);
    if (!array) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
        SWIG_fail;
    }

    dimsize[0] = dims$argnum[0];
    dimsize[1] = dims$argnum[1];

    $4 = (Type *) array->data;                                  // ARRAY
    $2 = array->dimensions[0];                                  // DIM1
    $3 = array->dimensions[1];                                  // DIM2
    $1 = &dimsize[0];                                           // SIZE1
//  $5 = &dimsize[1];                                           // SIZE2
}

/***************************************************************
* (Type OUT_ARRAY2[ANY][ANY], int *SIZE1)
***************************************************************/

%typemap(check)
        (Type OUT_ARRAY2[ANY][ANY], int *SIZE1)
                (PyArrayObject* array = NULL, int dimsize[2]),
        (Type OUT_ARRAY2[ANY][ANY], long *SIZE1)
                (PyArrayObject* array = NULL, long dimsize[2])
{
//      (Type OUT_ARRAY2[ANY][ANY], int *SIZE1)

    npy_intp dims$argnum[2] = {$1_dim0, $1_dim1};               // ARRAY
    array = PyArray_SimpleNew(2, dims$argnum, Typecode);
    if (!array) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
        SWIG_fail;
    }

    dimsize[0] = dims$argnum[0];
    dimsize[1] = dims$argnum[1];

    $1 = (Type *) array->data;                                  // ARRAY
//  $3 = array->dimensions[0];                                  // DIM1
//  $4 = array->dimensions[1];                                  // DIM2
    $2 = &dimsize[0];                                           // SIZE1
//  $5 = &dimsize[1];                                           // SIZE2
}

/***************************************************************
* (int *SIZE1, Type OUT_ARRAY2[ANY][ANY])
***************************************************************/

%typemap(check)
        (int *SIZE1, Type OUT_ARRAY2[ANY][ANY]),
                (PyArrayObject* array = NULL, int dimsize[2]),
        (long *SIZE1, Type OUT_ARRAY2[ANY][ANY])
                (PyArrayObject* array = NULL, long dimsize[2])
{
//      (int *SIZE1, Type OUT_ARRAY2[ANY][ANY])

    npy_intp dims$argnum[2] = {$2_dim0, $2_dim1};               // ARRAY
    array = PyArray_SimpleNew(2, dims$argnum, Typecode);
    if (!array) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
        SWIG_fail;
    }

    dimsize[0] = dims$argnum[0];
    dimsize[1] = dims$argnum[1];

    $2 = (Type *) array->data;                                  // ARRAY
//  $3 = array->dimensions[0];                                  // DIM1
//  $4 = array->dimensions[1];                                  // DIM2
    $1 = &dimsize[0];                                           // SIZE1
//  $5 = &dimsize[1];                                           // SIZE2
}

/***************************************************************
* (Type OUT_ARRAY2[ANY][ANY], int *SIZE1, int *SIZE2)
***************************************************************/

%typemap(check)
        (Type OUT_ARRAY2[ANY][ANY], int *SIZE1, int *SIZE2)
                (PyArrayObject* array = NULL, int dimsize[2]),
        (Type OUT_ARRAY2[ANY][ANY], long *SIZE1, long *SIZE2)
                (PyArrayObject* array = NULL, long dimsize[2])
{
//      (Type OUT_ARRAY2[ANY][ANY], int *SIZE1, int *SIZE2)

    npy_intp dims$argnum[2] = {$1_dim0, $1_dim1};               // ARRAY
    array = PyArray_SimpleNew(2, dims$argnum, Typecode);
    if (!array) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
        SWIG_fail;
    }

    dimsize[0] = dims$argnum[0];
    dimsize[1] = dims$argnum[1];

    $1 = (Type *) array->data;                                  // ARRAY
//  $4 = array->dimensions[0];                                  // DIM1
//  $5 = array->dimensions[1];                                  // DIM2
    $2 = &dimsize[0];                                           // SIZE1
    $3 = &dimsize[1];                                           // SIZE2
}

/***************************************************************
* (int *SIZE1, int *SIZE2, Type OUT_ARRAY2[ANY][ANY])
***************************************************************/

%typemap(check)
        (int *SIZE1, int *SIZE2, Type OUT_ARRAY2[ANY][ANY])
                (PyArrayObject* array = NULL, int dimsize[2]),
        (long *SIZE1, long *SIZE2, Type OUT_ARRAY2[ANY][ANY])
                (PyArrayObject* array = NULL, long dimsize[2])
{
//      (int *SIZE1, int *SIZE2, Type OUT_ARRAY2[ANY][ANY])

    npy_intp dims$argnum[2] = {$3_dim0, $3_dim1};               // ARRAY
    array = PyArray_SimpleNew(2, dims$argnum, Typecode);
    if (!array) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
        SWIG_fail;
    }

    dimsize[0] = dims$argnum[0];
    dimsize[1] = dims$argnum[1];

    $3 = (Type *) array->data;                                  // ARRAY
//  $4 = array->dimensions[0];                                  // DIM1
//  $5 = array->dimensions[1];                                  // DIM2
    $1 = &dimsize[0];                                           // SIZE1
    $2 = &dimsize[1];                                           // SIZE2
}

/*******************************************************
* %typemap(argout)
* %typemap(freearg)
*******************************************************/

%typemap(in, numinputs=0)
        (Type OUT_ARRAY2[ANY][ANY]),
        (Type OUT_ARRAY2[ANY][ANY], int DIM1, int DIM2),
        (int DIM1, int DIM2, Type OUT_ARRAY2[ANY][ANY]),
        (Type OUT_ARRAY2[ANY][ANY], int DIM1, int DIM2, int *SIZE1),
        (Type OUT_ARRAY2[ANY][ANY], int DIM1, int DIM2, long *SIZE1),
        (Type OUT_ARRAY2[ANY][ANY], int *SIZE1, int DIM1, int DIM2),
        (Type OUT_ARRAY2[ANY][ANY], long *SIZE1, int DIM1, int DIM2),
        (int DIM1, int DIM2, int *SIZE1, Type OUT_ARRAY2[ANY][ANY]),
        (int DIM1, int DIM2, long *SIZE1, Type OUT_ARRAY2[ANY][ANY]),
        (int *SIZE1, int DIM1, int DIM2, Type OUT_ARRAY2[ANY][ANY]),
        (long *SIZE1, int DIM1, int DIM2, Type OUT_ARRAY2[ANY][ANY]),
        (Type OUT_ARRAY2[ANY][ANY], int *SIZE1),
        (Type OUT_ARRAY2[ANY][ANY], long *SIZE1),
        (int *SIZE1, Type OUT_ARRAY2[ANY][ANY]),
        (long *SIZE1, Type OUT_ARRAY2[ANY][ANY]),
        (Type OUT_ARRAY2[ANY][ANY], int *SIZE1, int *SIZE2),
        (Type OUT_ARRAY2[ANY][ANY], long *SIZE1, long *SIZE2),
        (int *SIZE1, int *SIZE2, Type OUT_ARRAY2[ANY][ANY]),
        (long *SIZE1, long *SIZE2, Type OUT_ARRAY2[ANY][ANY])
{}

%typemap(argout)
        (Type OUT_ARRAY2[ANY][ANY]),
        (Type OUT_ARRAY2[ANY][ANY], int DIM1, int DIM2),
        (int DIM1, int DIM2, Type OUT_ARRAY2[ANY][ANY])
{
    $result = SWIG_Python_AppendOutput($result, array$argnum);
    Py_INCREF(array$argnum);    // Prevents freearg from freeing
}

%typemap(argout)
        (Type OUT_ARRAY2[ANY][ANY], int DIM1, int DIM2, int *SIZE1),
        (Type OUT_ARRAY2[ANY][ANY], int DIM1, int DIM2, long *SIZE1),
        (Type OUT_ARRAY2[ANY][ANY], int *SIZE1, int DIM1, int DIM2),
        (Type OUT_ARRAY2[ANY][ANY], long *SIZE1, int DIM1, int DIM2),
        (int DIM1, int DIM2, int *SIZE1, Type OUT_ARRAY2[ANY][ANY]),
        (int DIM1, int DIM2, long *SIZE1, Type OUT_ARRAY2[ANY][ANY]),
        (int *SIZE1, int DIM1, int DIM2, Type OUT_ARRAY2[ANY][ANY]),
        (long *SIZE1, int DIM1, int DIM2, Type OUT_ARRAY2[ANY][ANY]),
        (Type OUT_ARRAY2[ANY][ANY], int *SIZE1),
        (Type OUT_ARRAY2[ANY][ANY], long *SIZE1),
        (int *SIZE1, Type OUT_ARRAY2[ANY][ANY]),
        (long *SIZE1, Type OUT_ARRAY2[ANY][ANY]),
        (Type OUT_ARRAY2[ANY][ANY], int *SIZE1, int *SIZE2),
        (Type OUT_ARRAY2[ANY][ANY], long *SIZE1, long *SIZE2),
        (int *SIZE1, int *SIZE2, Type OUT_ARRAY2[ANY][ANY]),
        (long *SIZE1, long *SIZE2, Type OUT_ARRAY2[ANY][ANY])
{
    npy_intp dims$argnum[2] = {dimsize$argnum[0], dimsize$argnum[1]};
    PyArray_Dims shape = {dims$argnum, 2};
    PyArray_Resize(array$argnum, &shape, 0, NPY_CORDER);

    $result = SWIG_Python_AppendOutput($result, array$argnum);
    Py_INCREF(array$argnum);    // Prevents freearg from freeing
}

%typemap(freearg)
        (Type OUT_ARRAY2[ANY][ANY]),
        (Type OUT_ARRAY2[ANY][ANY], int DIM1, int DIM2),
        (int DIM1, int DIM2, Type OUT_ARRAY2[ANY][ANY]),
        (Type OUT_ARRAY2[ANY][ANY], int DIM1, int DIM2, int *SIZE1),
        (Type OUT_ARRAY2[ANY][ANY], int DIM1, int DIM2, long *SIZE1),
        (Type OUT_ARRAY2[ANY][ANY], int *SIZE1, int DIM1, int DIM2),
        (Type OUT_ARRAY2[ANY][ANY], long *SIZE1, int DIM1, int DIM2),
        (int DIM1, int DIM2, int *SIZE1, Type OUT_ARRAY2[ANY][ANY]),
        (int DIM1, int DIM2, long *SIZE1, Type OUT_ARRAY2[ANY][ANY]),
        (int *SIZE1, int DIM1, int DIM2, Type OUT_ARRAY2[ANY][ANY]),
        (long *SIZE1, int DIM1, int DIM2, Type OUT_ARRAY2[ANY][ANY]),
        (Type OUT_ARRAY2[ANY][ANY], int *SIZE1),
        (Type OUT_ARRAY2[ANY][ANY], long *SIZE1),
        (int *SIZE1, Type OUT_ARRAY2[ANY][ANY]),
        (long *SIZE1, Type OUT_ARRAY2[ANY][ANY]),
        (Type OUT_ARRAY2[ANY][ANY], int *SIZE1, int *SIZE2),
        (Type OUT_ARRAY2[ANY][ANY], long *SIZE1, long *SIZE2),
        (int *SIZE1, int *SIZE2, Type OUT_ARRAY2[ANY][ANY]),
        (long *SIZE1, long *SIZE2, Type OUT_ARRAY2[ANY][ANY])
{
    if (array$argnum) {
        Py_DECREF(array$argnum);
    }
}

/***************************************************************
* (Type **OUT_ARRAY2, int *SIZE1, int *SIZE2)
***************************************************************/

%typemap(check)
        (Type **OUT_ARRAY2, int *SIZE1, int *SIZE2)
                (PyArrayObject* array=NULL, Type *buffer=NULL, int dimsize[2]),
        (Type **OUT_ARRAY2, long *SIZE1, long *SIZE2)
                (PyArrayObject* array=NULL, Type *buffer=NULL, long dimsize[2])
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
                (PyArrayObject* array=NULL, Type *buffer=NULL, int dimsize[2]),
        (long *SIZE1, long *SIZE2, Type **OUT_ARRAY2)
                (PyArrayObject* array=NULL, Type *buffer=NULL, long dimsize[2])
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
        (Type **OUT_ARRAY2, long *SIZE1, long *SIZE2),
        (int *SIZE1, int *SIZE2, Type **OUT_ARRAY2),
        (long *SIZE1, long *SIZE2, Type **OUT_ARRAY2)
{}

%typemap(argout)
        (Type **OUT_ARRAY2, int *SIZE1, int *SIZE2),
        (Type **OUT_ARRAY2, long *SIZE1, long *SIZE2),
        (int *SIZE1, int *SIZE2, Type **OUT_ARRAY2),
        (long *SIZE1, long *SIZE2, Type **OUT_ARRAY2)
{
//      (Type **OUT_ARRAY2, int *SIZE1, int *SIZE2)
//      (int *SIZE1, int *SIZE2, Type **OUT_ARRAY2)

    npy_intp dims$argnum[2] = {dimsize$argnum[0], dimsize$argnum[1]};
    array$argnum = PyArray_SimpleNew(2, dims$argnum, Typecode);
    if (!array$argnum) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
        SWIG_fail;
    }

    memcpy(array$argnum->data, buffer$argnum,
                               dims$argnum[0] * dims$argnum[1] * sizeof(Type));  
    PyMem_Free((void *) buffer$argnum);

    $result = SWIG_Python_AppendOutput($result, array$argnum);
    Py_INCREF(array$argnum);    // Prevents freearg from freeing
}

%typemap(freearg)
        (Type **OUT_ARRAY2, int *SIZE1, int *SIZE2),
        (Type **OUT_ARRAY2, long *SIZE1, long *SIZE2),
        (int *SIZE1, int *SIZE2, Type **OUT_ARRAY2),
        (long *SIZE1, long *SIZE2, Type **OUT_ARRAY2)
{
    if (array$argnum) {
        Py_DECREF(array$argnum);
    }
}

/*******************************************************
* Now define these typemaps for every numeric type
*******************************************************/

%enddef

TYPEMAP_ARGOUT(char,          PyArray_CHAR  )
TYPEMAP_ARGOUT(unsigned char, PyArray_UBYTE )
TYPEMAP_ARGOUT(signed char,   PyArray_SBYTE )
TYPEMAP_ARGOUT(short,         PyArray_SHORT )
TYPEMAP_ARGOUT(int,           PyArray_INT   )
TYPEMAP_ARGOUT(long,          PyArray_LONG  )
TYPEMAP_ARGOUT(float,         PyArray_FLOAT )
TYPEMAP_ARGOUT(double,        PyArray_DOUBLE)
TYPEMAP_ARGOUT(PyObject,      PyArray_OBJECT)

#undef TYPEMAP_ARGOUT

/*******************************************************************************
* Numeric typemaps for input/output
*
* This family of typemaps allows the data values in a Numpy array to be
* overwritten by a C function. Care should be exercised: the array must be large
* enough and must be contiguous. The elements could appear in the wrong order if
* the Numpy array uses a non-standard set of strides.
*
* Mark R. Showalter, PDS Rings Node, SETI Institue, July 2010
*******************************************************************************/

%define TYPEMAP_INOUT(Type, Typecode) // Use to fill in numeric types below

/*******************************************************
* (Type *INOUT_ARRAY)
*******************************************************/

%typemap(in)
        (Type *INOUT_ARRAY)                                     // PATTERN
{
//      (Type *INOUT_ARRAY)

    PyArrayObject* array = obj_to_array_no_conversion($input, Typecode);
    if (!array) {
        SWIG_fail;
    }

    if (!array_is_contiguous(array)) {
        PyErr_SetString(PyExc_TypeError, "Array is not contiguous");
        SWIG_fail;
    }

    $1 = (Type *) array->data;                                  // ARRAY
}

/*******************************************************
* Now apply to all data types
*******************************************************/

%enddef

// Define concrete examples of the TYPEMAP_IN1 macros
TYPEMAP_INOUT(char,          PyArray_CHAR  )
TYPEMAP_INOUT(unsigned char, PyArray_UBYTE )
TYPEMAP_INOUT(signed char,   PyArray_SBYTE )
TYPEMAP_INOUT(short,         PyArray_SHORT )
TYPEMAP_INOUT(int,           PyArray_INT   )
TYPEMAP_INOUT(long,          PyArray_LONG  )
TYPEMAP_INOUT(float,         PyArray_FLOAT )
TYPEMAP_INOUT(double,        PyArray_DOUBLE)
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
*
* Mark R. Showalter, PDS Rings Node, SETI Institue, July 2009
*******************************************************************************/

/***********************************************
* (char *IN_STRING)
***********************************************/

%typemap(in) (char *IN_STRING) {
//      (char *IN_STRING)
    char *instr = PyString_AsString($input);
    int len = strlen(instr);

    char *buffer = (char *) PyMem_Malloc((len+1) * sizeof(char));
    if (!buffer) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
        SWIG_fail;
    }

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

%typemap(in) (char *CONST_STRING) {
//      (char *CONST_STRING)
    $1 = PyString_AsString($input);
}

%typemap(argout) (char *CONST_STRING) {
}

%typemap(freearg) (char *CONST_STRING) {
}

/***********************************************
* (char IN_STRING)
***********************************************/

%typemap(in) (char IN_STRING) {
//      (char IN_STRING)
    char *instr = PyString_AsString($input);
    $1 = instr[0];
}

%typemap(argout) (char IN_STRING) {
}

%typemap(freearg) (char IN_STRING) {
}

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
*
* Mark R. Showalter, PDS Rings Node, SETI Institue, July 2009
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
*
* Mark R. Showalter, PDS Rings Node, SETI Institue, July 2009
*******************************************************************************/

/***********************************************
* (char INOUT_STRING[ANY])
***********************************************/

%typemap(in)
        (char INOUT_STRING[ANY])                                // PATTERN
                (char *buffer = NULL, int dim1)
{
//      (char INOUT_STRING[ANY])

    char *instr = PyString_AsString($input);
    dim1 = strlen(instr) + 1;

    if (dim1 < $1_dim0) dim1 = $1_dim0;                         // STRING_dim0

    buffer = (char *) PyMem_Malloc(dim1 * sizeof(char));
    if (!buffer) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
        SWIG_fail;
    }
    strcpy(buffer, instr);

    $1 = buffer;                                                // STRING
//  $2 = dim1; */                                               // DIM1
}

/***********************************************
* (char INOUT_STRING[ANY], int DIM1)
***********************************************/

%typemap(in)
        (char INOUT_STRING[ANY], int DIM1)                      // PATTERN
                (char *buffer = NULL, int dim1)
{
//      (char INOUT_STRING[ANY], int DIM1)

    char *instr = PyString_AsString($input);
    dim1 = strlen(instr) + 1;

    if (dim1 < $1_dim0) dim1 = $1_dim0;                         // STRING_dim0

    buffer = (char *) PyMem_Malloc(dim1 * sizeof(char));
    if (!buffer) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
        SWIG_fail;
    }
    strcpy(buffer, instr);

    $1 = buffer;                                                // STRING
    $2 = dim1;                                                  // DIM1
}

/***********************************************
* (int DIM1, char INOUT_STRING[ANY])
***********************************************/

%typemap(in)
        (int DIM1, char INOUT_STRING[ANY])                      // PATTERN
                (char *buffer = NULL, int dim1)
{
//      (int DIM1, char INOUT_STRING[ANY])

    char *instr = PyString_AsString($input);
    dim1 = strlen(instr) + 1;

    if (dim1 < $2_dim0) dim1 = $2_dim0;                         // STRING_dim0

    buffer = (char *) PyMem_Malloc(dim1 * sizeof(char));
    if (!buffer) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
        SWIG_fail;
    }
    strcpy(buffer, instr);

    $2 = buffer;                                                // STRING
    $1 = dim1;                                                  // DIM1
}

/***********************************************
* (char *INOUT_STRING)
***********************************************/

%typemap(in)
        (char *INOUT_STRING)                                    // PATTERN
                (char *buffer = NULL, int dim1)
{
//      (char *INOUT_STRING)

    char *instr = PyString_AsString($input);
    dim1 = strlen(instr) + 1;

//  if (dim1 < $1_dim0) dim1 = $1_dim0;                         // STRING_dim0

    buffer = (char *) PyMem_Malloc(dim1 * sizeof(char));
    if (!buffer) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
        SWIG_fail;
    }
    strcpy(buffer, instr);

    $1 = buffer;                                                // STRING
//  $2 = dim1;                                                  // DIM1
}

/***********************************************
* (char *INOUT_STRING, int DIM1)
***********************************************/

%typemap(in)
        (char *INOUT_STRING, int DIM1)                          // PATTERN
                (char *buffer = NULL, int dim1)
{
//      (char *INOUT_STRING, int DIM1)

    char *instr = PyString_AsString($input);
    dim1 = strlen(instr) + 1;

//  if (dim1 < $1_dim0) dim1 = $1_dim0;                         // STRING_dim0

    buffer = (char *) PyMem_Malloc(dim1 * sizeof(char));
    if (!buffer) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
        SWIG_fail;
    }
    strcpy(buffer, instr);

    $1 = buffer;                                                // STRING
    $2 = dim1;                                                  // DIM1
}

/***********************************************
* (int DIM1, char *INOUT_STRING)
***********************************************/

%typemap(in)
        (int DIM1, char *INOUT_STRING)                          // PATTERN
                (char *buffer = NULL, int dim1)
{
//      (int DIM1, char *INOUT_STRING)

    char *instr = PyString_AsString($input);
    dim1 = strlen(instr) + 1;

//  if (dim1 < $2_dim0) dim1 = $2_dim0;                 // STRING_dim0

    buffer = (char *) PyMem_Malloc(dim1 * sizeof(char));
    if (!buffer) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
        SWIG_fail;
    }
    strcpy(buffer, instr);

    $2 = buffer;                                                // STRING
    $1 = dim1;                                                  // DIM1
}

/***********************************************
* (char OUT_STRING[ANY])
***********************************************/

%typemap(in, numinputs=0)
        (char OUT_STRING[ANY])                                  // PATTERN
                (char *buffer = NULL, int dim1)
{
//      (char OUT_STRING[ANY])

    dim1 = $1_dim0;                                             // STRING_dim0

    buffer = (char *) PyMem_Malloc(dim1 * sizeof(char));
    if (!buffer) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
        SWIG_fail;
    }
    buffer[0] = '\0';   // String begins empty

    $1 = buffer;                                                // STRING
//  $2 = dim1; */                                               // DIM1
}

/***********************************************
* (char OUT_STRING[ANY], int DIM1)
***********************************************/

%typemap(in, numinputs=0)
        (char OUT_STRING[ANY], int DIM1)                        // PATTERN
                (char *buffer = NULL, int dim1)
{
//      (char OUT_STRING[ANY], int DIM1)

    dim1 = $1_dim0;                                             // STRING_dim0

    buffer = (char *) PyMem_Malloc(dim1 * sizeof(char));
    if (!buffer) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
        SWIG_fail;
    }
    buffer[0] = '\0';   // String begins empty

    $1 = buffer;                                                // STRING
    $2 = dim1;                                                  // DIM1
}

/***********************************************
* (int DIM1, char OUT_STRING[ANY])
***********************************************/

%typemap(in, numinputs=0)
        (int DIM1, char OUT_STRING[ANY])                        // PATTERN
                (char *buffer = NULL, int dim1)
{
//      (int DIM1, char OUT_STRING[ANY])

    dim1 = $2_dim0;                                             // STRING_dim0

    buffer = (char *) PyMem_Malloc(dim1 * sizeof(char));
    if (!buffer) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
        SWIG_fail;
    }
    buffer[0] = '\0';   // String begins empty

    $2 = buffer;                                                // STRING
    $1 = dim1;                                                  // DIM1
}

/*******************************************************
* %typemap(argout)
* %typemap(freearg)
*******************************************************/

%typemap(argout)
        (char INOUT_STRING[ANY]),
        (char INOUT_STRING[ANY], int DIM1),
        (int DIM1, char INOUT_STRING[ANY]),
        (char *INOUT_STRING),
        (char *INOUT_STRING, int DIM1),
        (int DIM1, char *INOUT_STRING),
        (char OUT_STRING[ANY]),
        (char OUT_STRING[ANY], int DIM1),
        (int DIM1, char OUT_STRING[ANY])
{
//      (... char INOUT_STRING[ANY] ...)
//      (... char *INOUT_STRING ...)
//      (... char OUT_STRING[ANY] ...)

    PyObject* obj;
    buffer$argnum[dim1$argnum-1] = '\0';    // Make sure string is terminated
    obj = PyString_FromString((char *) buffer$argnum);
    $result = SWIG_Python_AppendOutput($result, obj);
}

%typemap(freearg)
        (char INOUT_STRING[ANY]),
        (char INOUT_STRING[ANY], int DIM1),
        (int DIM1, char INOUT_STRING[ANY]),
        (char *INOUT_STRING),
        (char *INOUT_STRING, int DIM1),
        (int DIM1, char *INOUT_STRING),
        (char OUT_STRING[ANY]),
        (char OUT_STRING[ANY], int DIM1),
        (int DIM1, char OUT_STRING[ANY])
{
//      (... char INOUT_STRING[ANY] ...)
//      (... char *INOUT_STRING ...)
//      (... char OUT_STRING[ANY] ...)

    PyMem_Free((void *) buffer$argnum);
}

/*******************************************************************************
* String array typemaps for input
*
* These typemaps allow C-format string arrays to be passed into the C function.
*
*       (char *IN_STRINGS, int DIM1, int DIM2)
*       (int DIM1, int DIM2, char *IN_STRINGS)
*
* Because Python strings are immutable, these strings should not be modified by
# the C function.
*
* Mark R. Showalter, PDS Rings Node, SETI Institue, July 2009
*******************************************************************************/

/***********************************************************************
* (char *IN_STRINGS, int DIM1, int DIM2)
***********************************************************************/

%typemap(in)
        (char *IN_STRINGS, int DIM1, int DIM2)
                (char *buffer)
{
//      (char *IN_STRINGS, int DIM1, int DIM2)

    int dim, i, maxlen, thislen;
    PyObject *obj;

    if (!PySequence_Check($input)) {
        PyErr_SetString(PyExc_TypeError,
            "Object must be a sequence of strings");
        SWIG_fail;
    }
    dim = PySequence_Length($input);

    maxlen = 0;
    for (i = 0; i < dim; i++) {
        obj = PySequence_GetItem($input, i);
        if (!PyString_Check(obj)) {
            PyErr_SetString(PyExc_TypeError,
                "Object must be a sequence of strings");
            SWIG_fail;
        }

        thislen = PyString_Size(obj);
        if (maxlen < thislen) maxlen = thislen;
    }

    buffer = (char *) PyMem_Malloc(dim * (maxlen+1) * sizeof(char));
    if (!buffer) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
        SWIG_fail;
    }

    for (i = 0; i < dim; i++) {
        obj = PySequence_GetItem($input, i);
        strncpy((buffer + i*(maxlen+1)), PyString_AsString(obj), maxlen+1);
    }

    $1 = buffer
    $2 = dim;
    $3 = maxlen + 1;
}

/***********************************************************************
* (int DIM1, int DIM2, char *IN_STRINGS)
***********************************************************************/

%typemap(in)
        (int DIM1, int DIM2, char *IN_STRINGS)
                (char *buffer)
{
//      (int DIM1, int DIM2, char *IN_STRINGS)

    int dim, i, maxlen, thislen;
    PyObject *obj;

    if (!PySequence_Check($input)) {
        PyErr_SetString(PyExc_TypeError,
            "Object must be a sequence of strings");
        SWIG_fail;
    }
    dim = PySequence_Length($input);

    maxlen = 0;
    for (i = 0; i < dim; i++) {
        obj = PySequence_GetItem($input, i);
        if (!PyString_Check(obj)) {
            PyErr_SetString(PyExc_TypeError,
                "Object must be a sequence of strings");
            SWIG_fail;
        }

        thislen = PyString_Size(obj);
        if (maxlen < thislen) maxlen = thislen;
    }

    buffer = (char *) PyMem_Malloc(dim * (maxlen+1) * sizeof(char));
    if (!buffer) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
        SWIG_fail;
    }

    for (i = 0; i < dim; i++) {
        obj = PySequence_GetItem($input, i);
        strncpy((buffer + i*(maxlen+1)), PyString_AsString(obj), maxlen+1);
    }

    $2 = dim;
    $3 = maxlen + 1;
}

/***********************************************************************
* %typemap(argout)
* %typemap(freearg)
***********************************************************************/

%typemap(argout)
    (char *IN_STRINGS, int DIM1, int DIM2),
    (int DIM1, int DIM2, char *IN_STRINGS)
{}

%typemap(freearg)
    (char *IN_STRINGS, int DIM1, int DIM2),
    (int DIM1, int DIM2, char *IN_STRINGS)
{
    PyMem_Free((void *) buffer$argnum);
}

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
*
* Mark R. Showalter, PDS Rings Node, SETI Institue, July 2009
*******************************************************************************/

/***********************************************************************
* (char OUT_STRINGS[ANY][ANY], int DIM1, int DIM2, int *NSTRINGS)
***********************************************************************/

%typemap(in,numinputs=0)
        (char OUT_STRINGS[ANY][ANY], int DIM1, int DIM2, int *NSTRINGS)
                (char *buffer, int dimsize[2]),
        (char OUT_STRINGS[ANY][ANY], int DIM1, int DIM2, long *NSTRINGS)
                (char *buffer, long dimsize[2])
{
//      (char OUT_STRINGS[ANY][ANY], int DIM1, int DIM2, int *NSTRINGS)

    dimsize[0] = $1_dim0;                                       // ARRAY_dim0
    dimsize[1] = $1_dim1;                                       // ARRAY_dim1
    buffer = (char *) PyMem_Malloc(dimsize[0] * dimsize[0] * sizeof(char));
    if (!buffer) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
        SWIG_fail;
    }

    $1 = buffer;                                                // ARRAY
    $2 = dimsize[0];                                            // DIM1
    $3 = dimsize[1];                                            // DIM2
    $4 = &dimsize[0];                                           // NSTRINGS
}

/***********************************************************************
* (int DIM1, int DIM2, int *NSTRINGS, char OUT_STRINGS[ANY][ANY])
***********************************************************************/

%typemap(in,numinputs=0)
        (int DIM1, int DIM2, int *NSTRINGS, char OUT_STRINGS[ANY][ANY])
                (char *buffer, int dimsize[2]),
        (int DIM1, int DIM2, long *NSTRINGS, char OUT_STRINGS[ANY][ANY])
                (char *buffer, long dimsize[2])
{
//      (int DIM1, int DIM2, int *NSTRINGS, char OUT_STRINGS[ANY][ANY])

    dimsize[0] = $4_dim0;                                       // ARRAY_dim0
    dimsize[1] = $4_dim1;                                       // ARRAY_dim1
    buffer = (char *) PyMem_Malloc(dimsize[0] * dimsize[0] * sizeof(char));
    if (!buffer) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
        SWIG_fail;
    }

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
        (char OUT_STRINGS[ANY][ANY], int DIM1, int DIM2, int *NSTRINGS),
        (char OUT_STRINGS[ANY][ANY], int DIM1, int DIM2, long *NSTRINGS),
        (int DIM1, int DIM2, int *NSTRINGS, char OUT_STRINGS[ANY][ANY]),
        (int DIM1, int DIM2, long *NSTRINGS, char OUT_STRINGS[ANY][ANY])
{
//      (char OUT_STRINGS[ANY][ANY], int DIM1, int DIM2, int *NSTRINGS)

    // Allocate a Python list with the correct number of elements.
    PyObject *obj = PyList_New(dimsize$argnum[0]);

    // Convert the results to Python strings and add them to the list
    int i;
    for (i = 0; i < dimsize$argnum[0]; i++) {
        PyList_SetItem(obj, i,
                PyString_FromString((char *) (buffer$argnum +
                                              i * dimsize$argnum[1])));
    }

    $result = SWIG_Python_AppendOutput($result, obj);
}

%typemap(freearg)
        (char OUT_STRINGS[ANY][ANY], int DIM1, int DIM2, int *NSTRINGS),
        (char OUT_STRINGS[ANY][ANY], int DIM1, int DIM2, long *NSTRINGS),
        (int DIM1, int DIM2, int *NSTRINGS, char OUT_STRINGS[ANY][ANY]),
        (int DIM1, int DIM2, long *NSTRINGS, char OUT_STRINGS[ANY][ANY])
{
//      (char OUT_STRINGS[ANY][ANY], int DIM1, int DIM2, int *NSTRINGS)

    PyMem_Free((void *) buffer$argnum);
}

/*******************************************************************************
* Typemap for boolean output
*
*       (Type *OUT_BOOLEAN)
*
* This typemap allows ints to be returned by the program as Python booleans.
* They are part of the return value and do not appear as arguments to the
* Python function. A zero value is False; anything else is True.
*
* Mark R. Showalter, PDS Rings Node, SETI Institue, July 2009
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
TYPEMAP_ARGOUT(unsigned char, PyArray_UBYTE )
TYPEMAP_ARGOUT(signed char,   PyArray_SBYTE )
TYPEMAP_ARGOUT(short,         PyArray_SHORT )
TYPEMAP_ARGOUT(int,           PyArray_INT   )
TYPEMAP_ARGOUT(long,          PyArray_LONG  )
TYPEMAP_ARGOUT(float,         PyArray_FLOAT )
TYPEMAP_ARGOUT(double,        PyArray_DOUBLE)

#undef TYPEMAP_ARGOUT

/*******************************************************************************
* Error handlers
*
*       (Type *OUT_BOOLEAN_KEYERROR)
*       (Type *OUT_BOOLEAN_SYNTAXERROR)
*       (Type *OUT_BOOLEAN_LOOKUPERROR)
*
* If these functions return a value of 0, the associated exception is raised.
* The error message reports the name of the function.
*
*       (int DIM1, char *OUT_STRING_SYNTAXERROR)
*       (Type *FLAG, int DIM1, char *OUT_STRING_SYNTAXERROR)
*
* If this string is not empty upon return, its contents are treated as the
* message associated with a syntax error
*
* Mark R. Showalter, PDS Rings Node, SETI Institue, July 2009
*******************************************************************************/

%define TYPEMAP_ERROR(Type, Typecode)

%typemap(in, numinputs=0)
        (Type *OUT_BOOLEAN_KEYERROR)    (Type mybool = 1),
        (Type *OUT_BOOLEAN_LOOKUPERROR) (Type mybool = 1),
        (Type *OUT_BOOLEAN_SYNTAXERROR) (Type mybool = 1)
{
//      (Type *OUT_BOOLEAN_*ERROR)

    $1 = &mybool;
}

%typemap(argout)
        (Type *OUT_BOOLEAN_KEYERROR)
{
//      (Type *OUT_BOOLEAN_KEYERROR)

    if (!*$1) {
        PyErr_SetString(PyExc_KeyError, "Keyword lookup failure in $symname");
        SWIG_fail;
    }
}

%typemap(argout)
        (Type *OUT_BOOLEAN_LOOKUPERROR)
{
//      (Type *OUT_BOOLEAN_LOOKUPERROR)

    if (!*$1) {
        PyErr_SetString(PyExc_LookupError, "Lookup failure in $symname");
        SWIG_fail;
    }
}

%typemap(argout)
        (Type *OUT_BOOLEAN_SYNTAXERROR)
{
//      (Type *OUT_BOOLEAN_SYNTAXERROR)

    if (!*$1) {
        PyErr_SetString(PyExc_SyntaxError, "Syntax error in $symname");
        SWIG_fail;
    }
}

%typemap(freearg)
        (Type *OUT_BOOLEAN_KEYERROR),
        (Type *OUT_BOOLEAN_LOOKUPERROR),
        (Type *OUT_BOOLEAN_SYNTAXERROR)
{}

// Now define these typemaps for every numeric type

%enddef

TYPEMAP_ERROR(char,          PyArray_CHAR  )
TYPEMAP_ERROR(unsigned char, PyArray_UBYTE )
TYPEMAP_ERROR(signed char,   PyArray_SBYTE )
TYPEMAP_ERROR(short,         PyArray_SHORT )
TYPEMAP_ERROR(int,           PyArray_INT   )
TYPEMAP_ERROR(long,          PyArray_LONG  )
TYPEMAP_ERROR(float,         PyArray_FLOAT )
TYPEMAP_ERROR(double,        PyArray_DOUBLE)

#undef TYPEMAP_ERROR

/***********************************************
* (int DIM1, char OUT_STRING_SYNTAXERROR[ANY])
***********************************************/

%typemap(in, numinputs=0)
        (int DIM1, char OUT_STRING_SYNTAXERROR[ANY])
{
    $2 = (char *) PyMem_Malloc(($2_dim0 + 1) * sizeof(char));
    if (!$2) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
        SWIG_fail;
    }

    $2[0] = '\0'; // String begins empty
    $1 = $2_dim0;
}

%typemap(argout)
        (int DIM1, char OUT_STRING_SYNTAXERROR[ANY])
{

    if ($2[0]) {
        PyErr_SetString(PyExc_SyntaxError, $2);
        SWIG_fail;
    }
}

%typemap(freearg)
        (int DIM1, char OUT_STRING_SYNTAXERROR[ANY])
{
    PyMem_Free((void *) $2);
}

/***********************************************
* (int *OK, int DIM1, char OUT_STRING_SYNTAXERROR[ANY])
***********************************************/

%typemap(in, numinputs=0)
        (int *OK, int DIM1, char OUT_STRING_SYNTAXERROR[ANY])
                (long ok)
{
    $3 = (char *) PyMem_Malloc(($3_dim0 + 1) * sizeof(char));
    if (!$3) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
        SWIG_fail;
    }

    $3[0] = '\0'; // String begins empty
    $2 = $3_dim0;
    $1 = &ok;
}

%typemap(argout)
        (int *OK, int DIM1, char OUT_STRING_SYNTAXERROR[ANY])
{

    if ($3[0]) {
        PyErr_SetString(PyExc_SyntaxError, $3);
        SWIG_fail;
    }
}

%typemap(freearg)
        (int *OK, int DIM1, char OUT_STRING_SYNTAXERROR[ANY])
{
    PyMem_Free((void *) $3);
}

/*******************************************************************************
* Typemap for return values. They also check for error status and raise a
* runtime exception if necessary.
*
*       (void   RETURN_VOID   )
*       (int    RETURN_BOOLEAN)
*       (int    RETURN_INT    )
*       (double RETURN_DOUBLE )
*       (char  *RETURN_STRING )
*
* Mark R. Showalter, PDS Rings Node, SETI Institue, July 2009
*
* Updated 1/4/12 (MRS) to include the more detailed "LONG" error messages.
*******************************************************************************/

%typemap(out) (void RETURN_VOID) {

    char message[3000];
    const char buffer[2000];
    if (failed_c()) {
        getmsg_c("SHORT", 3000, message);
        strcat(message, " -- ");
        getmsg_c("LONG", 2000, buffer);
        strcat(message, buffer);
        PyErr_SetString(PyExc_RuntimeError, message);
        reset_c();
        SWIG_fail;
    }

    $result = SWIG_Py_Void();
}

%typemap(out) (int RETURN_BOOLEAN) {

    char message[3000];
    const char buffer[2000];
    if (failed_c()) {
        getmsg_c("SHORT", 3000, message);
        strcat(message, " -- ");
        getmsg_c("LONG", 2000, buffer);
        strcat(message, buffer);
        PyErr_SetString(PyExc_RuntimeError, message);
        reset_c();
        SWIG_fail;
    }

    $result = SWIG_Python_AppendOutput($result, PyBool_FromLong((long) $1));
}

%typemap(out) (int RETURN_INT) {

    char message[3000];
    const char buffer[2000];
    if (failed_c()) {
        getmsg_c("SHORT", 3000, message);
        strcat(message, " -- ");
        getmsg_c("LONG", 2000, buffer);
        strcat(message, buffer);
        PyErr_SetString(PyExc_RuntimeError, message);
        reset_c();
        SWIG_fail;
    }

    $result = SWIG_Python_AppendOutput($result, PyInt_FromLong((long) $1));
}

%typemap(out) (double RETURN_DOUBLE) {

    char message[3000];
    const char buffer[2000];
    if (failed_c()) {
        getmsg_c("SHORT", 3000, message);
        strcat(message, " -- ");
        getmsg_c("LONG", 2000, buffer);
        strcat(message, buffer);
        PyErr_SetString(PyExc_RuntimeError, message);
        reset_c();
        SWIG_fail;
    }

    $result = SWIG_Python_AppendOutput($result,
                                       PyFloat_FromDouble((double) $1));
}

%typemap(out) (char *RETURN_STRING) {

    char message[3000];
    const char buffer[2000];
    if (failed_c()) {
        getmsg_c("SHORT", 3000, message);
        strcat(message, " -- ");
        getmsg_c("LONG", 2000, buffer);
        strcat(message, buffer);
        PyErr_SetString(PyExc_RuntimeError, message);
        reset_c();
        SWIG_fail;
    }

    $result = SWIG_Python_AppendOutput($result,
                                       PyString_FromString((char *) $1));
}

/*******************************************************************************
*******************************************************************************/
