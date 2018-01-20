:: Create __init__.py and _cspice.pyd for Windows
::
:: This batch file depends on the Microsoft Visual Studio C++
:: compiler being installed. It can be found (for free) as part of the
:: .NET software development kit here:
::    http://msdn.microsoft.com/en-us/windowsserver/bb980924.aspx
::
:: You must also have an appropriate (32-bit or 64-bit) version of Python
:: installed along with swig.
::
:: NOTE: In the following, the choice of 32-bit or 64-bit depends solely
:: on the version of Python you have installed. For example, you can create
:: a 32-bit version of CSPICE on a 64-bit machine as long as you are running
:: a 32-bit version of Python.
::
:: For Windows 32-bit, download the CSPICE toolkit from:
::    http://naif.jpl.nasa.gov/naif/toolkit_C_PC_Windows_VisualC_32bit.html
:: and unzip it in this (pds-tools/cspice) directory. This will create a new
:: subdirectory pds-tools/cspice/cspice.
::
:: For Windows 64-bit, download the CSPICE toolkit from:
::    http://naif.jpl.nasa.gov/naif/toolkit_C_PC_Windows_VisualC_64bit.html
:: and unzip it in this (pds-tools/cspice) directory. This will create a new
:: subdirectory pds-tools/cspice/cspice.
::
:: Create a Visual Studio command line window by selecting
::    All Programs > Microsoft Windows SDK v7.1 > 
::                   Windows SDK v7.1 Command Prompt
::
:: For Windows 32-bit, type:
::    setenv /x86
:: For Windows 64-bit, type:
::    setenv /x64
::
:: Then execute this batch file: .\cspice_make_windows.bat
::
:: To test the installation, the following should display the CSPICE
:: toolkit version string. Run python in the top-level pds-tools directory
:: or make sure pds-tools is in your PYTHONPATH.
::
::    > python
::    >>> import cspice
::    >>> cspice.tkvrsn("toolkit")
::
:: *** NOTE ***
:: Adjust the following variable to point at your top-level Python directory:

set PYTHON_PATH=C:\Users\rfrench\AppData\Local\Enthought\Canopy\App\appdata\canopy-1.7.4.3348.win-x86_64

del cspice.py
del cspice_wrap.c
del cspice_wrap.dll
del cspice_wrap.exp
del cspice_wrap.lib
del cspice_wrap.obj

swig -python cspice.i

cl /LD /I%PYTHON_PATH%/include /I%PYTHON_PATH%/Lib/site-packages/numpy/core/include /Icspice/src/cspice cspice_wrap.c %PYTHON_PATH%/libs/python27.lib cspice/lib/cspice.lib cspice/lib/csupport.lib

del _cspice.pyd
ren cspice_wrap.dll _cspice.pyd
del __init__.py
ren cspice.py __init__.py

del cspice_wrap.c
del cspice_wrap.dll
del cspice_wrap.exp
del cspice_wrap.lib
del cspice_wrap.obj
