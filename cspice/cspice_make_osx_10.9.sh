#!/bin/sh
#
# Create __init__.py and _cspice.so for Apple OSX 10.9
#
# This script depends on swig.
#
# You must also have an appropriate (32-bit or 64-bit) version of Python
# installed.
#
# For OSX 32-bit, download the CSPICE toolkit from:
#    http://naif.jpl.nasa.gov/naif/toolkit_C_MacIntel_OSX_AppleC_32bit.html
# and uncompress and untar it in this directory. This will create a new
# subdirectory pds-tools/cspice/cspice.
#
# For OSX 64-bit, download the CSPICE toolkit from:
#    http://naif.jpl.nasa.gov/naif/toolkit_C_MacIntel_OSX_AppleC_64bit.html
# and uncompress and untar it in this directory. This will create a new
# subdirectory pds-tools/cspice/cspice.
#
# Execute this shell script: ./cspice_make_osx_10.9.sh
#
# To test the installation, the following should display the CSPICE
# toolkit version string:
#
#    $ python
#    >>> import cspice
#    >>> cspice.tkvrsn("toolkit")
#
# *** NOTE ***
# Adjust the following variables to point at your Python directories:

PYTHON_INCLUDE=/usr/include/python2.7
PYTHON_PKGS=/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python

rm -f cspice.py cspice_wrap.c cspice_wrap.o

swig -python cspice.i

rm -f __init__.py
mv cspice.py __init__.py

gcc -c `python-config --cflags` cspice_wrap.c -I$PYTHON_INCLUDE \
    -I$PYTHON_PKGS/numpy/core/include -Icspice/src/cspice

rm -f _cspice.so

ld -bundle `python-config --ldflags` -flat_namespace -undefined suppress \
    -o _cspice.so cspice_wrap.o cspice/lib/cspice.a -lm

rm -f cspice_wrap.c cspice_wrap.o
