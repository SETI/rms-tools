                        ************
                        ** CSPICE **
                        ************

The cspice package is a Python interface to the NAIF cspice library.
To use the cspice package, you must either copy an existing shared
object file or compile a new one for your operating system as
described below. Pre-compiled shared objects are provided for Ubuntu
Linux (64-bit), Mac OSX (64-bit), and Windows (32-bit and 64-bit).

         OS                  COPY FROM             COPY TO
=====================  =====================   ================
Ubuntu Linux 64-bit    cspice/_cspice_l64.so   cspice/_cspice.so
Mac OSX 64-bit         cspice/_cspice_m64.so   cspice/_cspice.so
Windows 32-bit         cspice/_cspice_w32.pyd  cspice/_cspice.pyd
Windows 64-bit         cspice/_cspice_w64.pyd  cspice/_cspice.pyd

TO COMPILE FOR               FOLLOW INSTRUCTIONS IN
=====================  =================================
Ubuntu Linux 64-bit    cspice/cspice_make_linux.sh
Mac OSX 64-bit         cspice/cspice_make_osx.sh
Windows 32-bit         cspice/cspice_make_windows.bat
Windows 64-bit         cspice/cspice_make_windows.bat
