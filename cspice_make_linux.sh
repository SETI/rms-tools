#!/bin/sh
#
# Create cspice.py and _cspice.pyd for Ubuntu Linux
#
# This script depends on the python-dev and swig packages:
#    apt-get install python-dev
#    apt-get install swig
#
# You must also have an appropriate (32-bit or 64-bit) version of Python
# installed.
#
# For Linux 32-bit, download the CSPICE toolkit from:
#    http://naif.jpl.nasa.gov/naif/toolkit_C_PC_Linux_GCC_32bit.html
# and uncompress and untar it in this directory.
#
# For Linux 64-bit, download the CSPICE toolkit from:
#    http://naif.jpl.nasa.gov/naif/toolkit_C_PC_Linux_GCC_64bit.html
# and uncompress and untar it in this directory.
#
# Execute this shell script: ./cspice_make_linux.sh
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
PYTHON_PKGS=/usr/local/lib/python2.7/site-packages

rm -f cspice.py cspice_wrap.c cspice_wrap.o

swig -python cspice.i

gcc -c cspice_wrap.c -fPIC -I$PYTHON_INCLUDE \
    -I$PYTHON_PKGS/numpy/core/include -Icspice/src/cspice

rm -f _cspice.so

ld -o _cspice.so cspice_wrap.o -shared cspice/lib/cspice.a -lm

rm -f cspice_wrap.c cspice_wrap.o
