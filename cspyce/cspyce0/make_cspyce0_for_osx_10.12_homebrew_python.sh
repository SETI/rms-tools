#!/bin/sh
#
# Create cspyce0.py and _cspyce0.so for Apple OSX 10.12 and Homebrew Python
#
# This script depends on swig.
#
# You must also have an appropriate 64-bit version of Python installed.
#
# For OSX 64-bit, download the CSPICE toolkit from:
#    http://naif.jpl.nasa.gov/naif/toolkit_C_MacIntel_OSX_AppleC_64bit.html
# and uncompress and untar it in this directory. This will create a new
# subdirectory pds-tools/cspyce/cspyce0/cspice.
#
# Alternatively, type
#   ln -s [cspice_path] cspice
# where "[cspice_path]" is replaced by the path to your existing cspice
# directory.
#
# Execute this shell script: ./cspyce_make_osx_10.12_homebrew_python.sh
#
# To test the installation, the following should display the CSPICE
# toolkit version string:
#
#    $ python
#    >>> importc spyce
#    >>> cspyce.tkvrsn("toolkit")
#
# *** NOTE ***
# Adjust the following variables to point at your Python directories:

PYTHON_INCLUDE=/usr/include/python2.7
PYTHON_PKGS=/usr/local/lib/python2.7/site-packages

rm -f cspyce0_wrap.c cspyce0_wrap.o

swig -python cspyce0.i

gcc -c `python-config --cflags` cspyce0_wrap.c -I$PYTHON_INCLUDE \
    -I$PYTHON_PKGS/numpy/core/include -Icspice/src/cspice
# This returns many warnings but should not report any errors

# Use this version to limit Python exceptions to RuntimeErrors.
# gcc -c `python-config --cflags` cspyce0_wrap.c -I$PYTHON_INCLUDE \
#     -I$PYTHON_PKGS/numpy/core/include -Icspice/src/cspice \
#     -D RUNTIME_ERRORS_ONLY

rm -f _cspyce0.so

ld -bundle `python-config --ldflags` -flat_namespace -undefined suppress \
    -macosx_version_min 10.12 \
    -o _cspyce0.so cspyce0_wrap.o cspice/lib/cspice.a -lm

rm -f cspyce0_wrap.c cspyce0_wrap.o
