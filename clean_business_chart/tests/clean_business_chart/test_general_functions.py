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


def test_optimize_data():
    # Test 1 - data-list to be rounded with 1 decimals
    data     = [15, 3.56, 4.876, 45.932, 100]
    expected = [15.0, 3.6, 4.9, 45.9, 100.0]
    actual   = optimize_data(data=data, numerator=1, denominator=1, decimals=1)
    message  = "Test 1 - optimize_data returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message
    
    # Test 2 - data-list to be rounded with 0 decimals
    data     = [15, 3.56, 4.876, 45.932, 100]
    expected = [15, 4, 5, 46, 100]
    actual   = optimize_data(data=data, numerator=1, denominator=1, decimals=0)
    message  = "Test 2 - optimize_data returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 3 - integer rounded with 1 decimals
    data     = 16
    expected = 16.0
    actual   = optimize_data(data=data, numerator=1, denominator=1, decimals=1)
    message  = "Test 3 - optimize_data returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 4 - float rounded with 0 decimals
    data     = 16.37682
    expected = 16
    actual   = optimize_data(data=data, numerator=1, denominator=1, decimals=0)
    message  = "Test 4 - optimize_data returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 5 - None
    data     = None
    expected = None
    actual   = optimize_data(data=data, numerator=1, denominator=1, decimals=1)
    message  = "Test 5 - optimize_data returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 6 - String
    data     = "This is a string"
    expected = "This is a string"
    actual   = optimize_data(data=data, numerator=1, denominator=1, decimals=1)
    message  = "Test 6 - optimize_data returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 7 - Optimizing with other numerator and denominator
    data     = 123456789
    expected = 370.4
    actual   = optimize_data(data=data, numerator=3, denominator=1000000, decimals=1)
    message  = "Test 7 - optimize_data returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 8 - Denominator = 0
    with pytest.raises(ValueError):
        data    = 3
        optimize_data(data=data, numerator=3, denominator=0, decimals=1)

    # Test 9 - Denominator = string
    with pytest.raises(ValueError):
        data    = 3
        optimize_data(data=data, numerator=3, denominator="This is a string", decimals=1)

    # Test 10 - Nominator = string
    with pytest.raises(ValueError):
        data    = 3
        optimize_data(data=data, numerator="This is a string", denominator=1, decimals=1)

    # Test 11 - Decimals = string
    with pytest.raises(ValueError):
        data    = 3
        optimize_data(data=data, numerator=1, denominator=1, decimals="This is a string")

    # Test 12 - Decimals = float
    with pytest.raises(ValueError):
        data    = 3
        optimize_data(data=data, numerator=1, denominator=1, decimals=1.1)

def test_formatstring():
    # Test 1 - zero decimals
    data     = 0
    expected = '%0i'
    actual   = formatstring(decimals=data)
    message  = "Test 1 - formatstring returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 2 - one decimal
    data     = 1
    expected = '%0.1f'
    actual   = formatstring(decimals=data)
    message  = "Test 2 - formatstring returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 3 - two decimals
    data     = 2
    expected = '%0.2f'
    actual   = formatstring(decimals=data)
    message  = "Test 3 - formatstring returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 4 - three decimals
    data     = 3
    expected = '%0.3f'
    actual   = formatstring(decimals=data)
    message  = "Test 4 - formatstring returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 5 - Decimals = float
    with pytest.raises(ValueError):
        data    = 1.15
        formatstring(decimals=data)

    # Test 6 - Decimals = too high integer
    with pytest.raises(ValueError):
        data    = 4
        formatstring(decimals=data)

    # Test 7 - Decimals = string
    with pytest.raises(ValueError):
        data    = "This is a string"
        formatstring(decimals=data)


#### Need to add more test-functions for automatic testing
