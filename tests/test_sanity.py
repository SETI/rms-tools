'''Simple sanity tests.  Currently these tests simply import the
modules and packages to ensure that they load.  These tests should be
expanded to test functionality.'''

import pytest

# module tests

def test_colornames():
    import colornames

def test_gravity():
    import gravity

def test_interval():
    import interval

def test_julian():
    import julian

def test_julian_dateparser():
    import julian_dateparser

def test_pdsparser():
    import pdsparser

def test_pdstable():
    import pdstable

def test_picmaker():
    import picmaker

def test_solar():
    import solar

def test_tabulation():
    import tabulation

def test_textkernel():
    import textkernel

def test_tiff16():
    import tiff16

def test_vicar():
    import vicar

# package tests

@pytest.mark.skip(reason='incomplete implementation; need binary library')
def test_cspice():
    import cspice

@pytest.mark.skip(reason='incomplete implementation; to be investigated')
def test_starcat():
    import starcat


