"""test General functions"""

from clean_business_chart.general_functions import *
import pytest


#####################    
# GENERAL FUNCTIONS #
#####################

def test_islist():
    # Test with a list
    expected = True
    actual   = islist(['list'])
    assert actual == expected, "islist(['list']) gives back "+str(actual)+" instead of "+str(expected)
    # Test with a string
    expected = False
    actual   = islist('not a list')
    assert actual == expected, "islist('not a list') gives back "+str(actual)+" instead of "+str(expected)


def test_isdictionary():
    # Test with a dictionary
    expected = True
    actual   = isdictionary({'dictionary':'yes'})
    assert actual == expected, "isdictionary({'dictionary':'yes'}) gives back "+str(actual)+" instead of "+str(expected)
    # Test with a string
    expected = False
    actual   = isdictionary('not a dictionary')
    assert actual == expected, "isdictionary('not a dictionary') gives back "+str(actual)+" instead of "+str(expected)

def test_isinteger():
    # Test with an integer
    expected = True
    actual   = isinteger(3)
    assert actual == expected, "isinteger(3) gives back "+str(actual)+" instead of "+str(expected)
    # Test with a string
    expected = False
    actual   = isinteger('not an integer')
    assert actual == expected, "isinteger('not an integer') gives back "+str(actual)+" instead of "+str(expected)

def test_isstring():
    # Test with a string
    expected = True
    actual   = isstring('this is a string')
    assert actual == expected, "isstring('this is a string') gives back "+str(actual)+" instead of "+str(expected)
    # Test with a string
    expected = False
    actual   = isstring(100)
    assert actual == expected, "isstring(100) gives back "+str(actual)+" instead of "+str(expected)

def test_isfloat():
    # Test with a float
    expected = True
    actual   = isfloat(3.14)
    assert actual == expected, "isfloat(3.14) gives back "+str(actual)+" instead of "+str(expected)
    # Test with a string
    expected = False
    actual   = isfloat('not a float')
    assert actual == expected, "isfloat('not a float') gives back "+str(actual)+" instead of "+str(expected)

def test_isboolean():
    # Test with a boolean
    expected = True
    actual   = isboolean(True)
    assert actual == expected, "isboolean(True) gives back "+str(actual)+" instead of "+str(expected)
    # Test with a string
    expected = False
    actual   = isboolean('not a boolean')
    assert actual == expected, "isboolean('not a boolean') gives back "+str(actual)+" instead of "+str(expected)

def test_isdataframe():
    # Test with a DataFrame
    expected = True
    actual   = isdataframe(pd.DataFrame({'Column1': ['Value1', 'Value2']}))
    assert actual == expected, "isdataframe(pd.DataFrame({'Column1': ['Value1', 'Value2']}) gives back "+str(actual)+" instead of "+str(expected)
    # Test with a string
    expected = False
    actual   = isdataframe('not a DataFrame')
    assert actual == expected, "isdataframe('not a DataFrame') gives back "+str(actual)+" instead of "+str(expected)

def test_plot_line_accross_axes():
    # The function plot_line_accross_axes() draws a line in a figure object.
    #### At the moment I have no idea how to test this function
    assert 1 == 1

def test_plot_line_within_ax():
    # The function plot_line_within_ax() draws a line in a figure object.
    #### At the moment I have no idea how to test this function
    assert 1 == 1


def test_plot_endpoint():
    # Only testing the parameters, not the functionality of the function
    with pytest.raises(ValueError):
        plot_endpoint(ax=1, x=2, y=3, endpointcolor=dict())
    with pytest.raises(ValueError):
        plot_endpoint(ax=1, x=2, y=3, endpointcolor=[1,2,3])
    with pytest.raises(ValueError):
        plot_endpoint(ax=1, x=2, y=3, endpointcolor=[1,2], markersize_outercircle=5, markersize_innercircle=7)


def test_string_to_value():
    # Test with None
    expected = None
    actual   = string_to_value(None)
    assert actual == expected, "string_to_value(None) gives back "+str(actual)+" instead of "+str(expected)
    actual   = string_to_value('None')
    assert actual == expected, "string_to_value('None') gives back "+str(actual)+" instead of "+str(expected)
    # Test with list
    expected = [1, 1.2, None]
    actual   = string_to_value(['1', '1.2', 'None'])
    assert actual == expected, "string_to_value(['1', '1.2', 'None']) gives back "+str(actual)+" instead of "+str(expected)
    # Test with integer
    expected = 1000
    actual   = string_to_value(1000)
    assert actual == expected, "string_to_value(1000) gives back "+str(actual)+" instead of "+str(expected)
    expected = 2000
    actual   = string_to_value('2000')
    assert actual == expected, "string_to_value('2000') gives back "+str(actual)+" instead of "+str(expected)
    expected = -3000
    actual   = string_to_value('-3000')
    assert actual == expected, "string_to_value('-3000') gives back "+str(actual)+" instead of "+str(expected)
    # Test with float
    expected = 324.71
    actual   = string_to_value(324.71)
    assert actual == expected, "string_to_value(324.71) gives back "+str(actual)+" instead of "+str(expected)
    expected = 867.16
    actual   = string_to_value('867.16')
    assert actual == expected, "string_to_value('867.16') gives back "+str(actual)+" instead of "+str(expected)
    expected = -123.45
    actual   = string_to_value('-123.45')
    assert actual == expected, "string_to_value('-123.45') gives back "+str(actual)+" instead of "+str(expected)
    expected = '1.867.16'
    actual   = string_to_value('1.867.16')
    assert actual == expected, "string_to_value('1.867.16') gives back "+str(actual)+" instead of "+str(expected)


#### Need to add more test-functions for automatic testing
