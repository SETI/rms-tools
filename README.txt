                        ************
                        ** CSPICE **
                        ************

The cspice package is a Python interface to the NAIF cspice library.
To use the cspice package, you must either copy an existing shared
object file or compile a new one for your operating system as
described below. Pre-compiled shared objects are provided for Ubuntu
Linux (64-bit), Mac OSX (64-bit), and Windows (32-bit and 64-bit).
These shared objects may not always be up-to-date, and it is
recommended that you compile your own from scratch if you need the
most recent CSPICE code.

Ubuntu Linux 64-bit
        COPY FROM      cspice/_cspice_linux_ubuntu_64bit_python273.so
        COPY TO        cspice/_cspice.so
Mac OSX 64-bit
        COPY FROM      cspice/_cspice_osx_10.9_64bit_python275.so
        COPY TO        cspice/_cspice.so
Windows 32-bit
	* No binaries provided - you need to build your own *
Windows 64-bit
        COPY FROM      cspice/_cspice_win7_64bit_python2_7_11.pyd
        COPY TO        cspice/_cspice.pyd

TO COMPILE FOR               FOLLOW INSTRUCTIONS IN
=====================  =================================
Ubuntu Linux 64-bit    cspice/cspice_make_linux_ubuntu.sh
Mac OSX 64-bit         cspice/cspice_make_osx_10.9.sh
Windows 32-bit         cspice/cspice_make_windows.bat
Windows 64-bit         cspice/cspice_make_windows.bat

To test your installation:

    % python
    >>> import cspice
    >>> cspice.tkvrsn("toolkit")
