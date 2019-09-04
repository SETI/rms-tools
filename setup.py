from distutils.core import setup

setup(
    name='pds-tools',
    version='0.1.dev1',
    license='LICENSE.txt',
    maintainer='Mark Showalter',
    maintainer_email='mshowalter@seti.org',
    url='http://github.com/SETI/pds-tools',
    packages=['cspice', 'starcat'],
    py_modules=['colornames', 'gravity', 'interval', 'julian', 
                'julian_dateparser', 'pdsparser', 'pdstable', 'picmaker',
                'solar', 'tabulation', 'textkernel', 'tiff16', 'vicar'],

    )
