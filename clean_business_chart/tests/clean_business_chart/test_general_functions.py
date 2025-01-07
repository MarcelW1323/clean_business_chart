"""test General functions"""

from clean_business_chart.general_functions import *
import pandas as pd
from pandas import Timestamp  # Needed in test_dataframe_date_to_year_and_month()
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


def test_istuple():
    # Test with a tuple
    expected = True
    actual   = istuple(('tuplevalue 1', 'tuplevalue 2'))
    assert actual == expected, "istuple(('tuplevalue 1', 'tuplevalue 2')) gives back "+str(actual)+" instead of "+str(expected)
    # Test with a string
    expected = False
    actual   = istuple('not a tuple')
    assert actual == expected, "istuple('not a tuple') gives back "+str(actual)+" instead of "+str(expected)


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


def test_isaxes():
    # Test with an axes
    expected = True
    _, axes1 = plt.subplots()
    actual   = isaxes(axes1)
    assert actual == expected, "isaxes(axes1) gives back "+str(actual)+" instead of "+str(expected)
    # Test with a string
    expected = False
    actual   = isaxes('not an axes')
    assert actual == expected, "isaxes('not an axes') gives back "+str(actual)+" instead of "+str(expected)
    plt.close(_)


def test_isfigure():
    # Test with a figure
    expected = True
    figure1, _ = plt.subplots()
    actual   = isfigure(figure1)
    assert actual == expected, "isfigure(figure1) gives back "+str(actual)+" instead of "+str(expected)
    # Test with a string
    expected = False
    actual   = isfigure('not a figure')
    assert actual == expected, "isfigure('not a figure') gives back "+str(actual)+" instead of "+str(expected)
    plt.close(figure1)


def test_error_not_islist():
    # Test 1 with a list only, no error will occur
    list1 = [ 'Value1', 'Value2']
    error_not_islist(list1)

    # Test 2 with a list and name of variable, no error will occur
    list1 = [ 'Value1', 'Value2']
    error_not_islist(list1, name_inputvariable_in_text='list1')

    # Test 3 with a string
    with pytest.raises(TypeListError) as exceptioninfo:
        list1 = 'This is a string'
        error_not_islist(list1)
    assert str(exceptioninfo.value) == 'Variable is not of type list, but of type '+str(type(list1))

    # Test 4 with an integer and name of variable
    with pytest.raises(TypeListError) as exceptioninfo:
        list1 = 404
        error_not_islist(list1, name_inputvariable_in_text='list1')
    assert str(exceptioninfo.value) == 'Variable "list1" is not of type list, but of type '+str(type(list1))

    # Test 5 with a string and name of variable as positional argument
    with pytest.raises(TypeListError) as exceptioninfo:
        list1 = 'This is a string'
        error_not_islist(list1, 'list1')
    assert str(exceptioninfo.value) == 'Variable "list1" is not of type list, but of type '+str(type(list1))


def test_error_not_istuple():
    # Test 1 with a tuple only, no error will occur
    tuple1 = ('Value1', 'Value2')
    error_not_istuple(tuple1)

    # Test 2 with a tuple and name of variable, no error will occur
    tuple1 = ('Value1', 'Value2')
    error_not_istuple(tuple1, name_inputvariable_in_text='tuple1')

    # Test 3 with a string
    with pytest.raises(TypeTupleError) as exceptioninfo:
        tuple1 = 'This is a string'
        error_not_istuple(tuple1)
    assert str(exceptioninfo.value) == 'Variable is not of type tuple, but of type '+str(type(tuple1))

    # Test 4 with an integer and name of variable
    with pytest.raises(TypeTupleError) as exceptioninfo:
        tuple1 = 404
        error_not_istuple(tuple1, name_inputvariable_in_text='tuple1')
    assert str(exceptioninfo.value) == 'Variable "tuple1" is not of type tuple, but of type '+str(type(tuple1))

    # Test 5 with a string and name of variable as positional argument
    with pytest.raises(TypeTupleError) as exceptioninfo:
        tuple1 = 'This is a string'
        error_not_istuple(tuple1, 'tuple1')
    assert str(exceptioninfo.value) == 'Variable "tuple1" is not of type tuple, but of type '+str(type(tuple1))


def test_error_not_isdictionary():
    # Test 1 with a dictionary only, no error will occur
    dict1 = {'Label1':'Value1', 'Label2':'Value2'}
    error_not_isdictionary(dict1)

    # Test 2 with a dictionary and name of variable, no error will occur
    dict1 = {'Label1':'Value1', 'Label2':'Value2'}
    error_not_isdictionary(dict1, name_inputvariable_in_text='dict1')

    # Test 3 with a string
    with pytest.raises(TypeDictionaryError) as exceptioninfo:
        dict1 = 'This is a string'
        error_not_isdictionary(dict1)
    assert str(exceptioninfo.value) == 'Variable is not of type dictionary, but of type '+str(type(dict1))

    # Test 4 with a int and name of variable
    with pytest.raises(TypeDictionaryError) as exceptioninfo:
        dict1 = 404
        error_not_isdictionary(dict1, name_inputvariable_in_text='dict1')
    assert str(exceptioninfo.value) == 'Variable "dict1" is not of type dictionary, but of type '+str(type(dict1))

    # Test 5 with a string and name of variable as positional argument
    with pytest.raises(TypeDictionaryError) as exceptioninfo:
        dict1 = 'This is a string'
        error_not_isdictionary(dict1, 'dict1')
    assert str(exceptioninfo.value) == 'Variable "dict1" is not of type dictionary, but of type '+str(type(dict1))


def test_error_not_isinteger():
    # Test 1 with an integer only, no error will occur
    integer1 = 101
    error_not_isinteger(integer1)

    # Test 2 with an integer and name of variable, no error will occur
    integer1 = 101
    error_not_isinteger(integer1, name_inputvariable_in_text='integer1')

    # Test 3 with a string
    with pytest.raises(TypeIntegerError) as exceptioninfo:
        integer1 = 'This is a string'
        error_not_isinteger(integer1)
    assert str(exceptioninfo.value) == 'Variable is not of type integer, but of type '+str(type(integer1))

    # Test 4 with a float and name of variable
    with pytest.raises(TypeIntegerError) as exceptioninfo:
        integer1 = 404.505
        error_not_isinteger(integer1, name_inputvariable_in_text='integer1')
    assert str(exceptioninfo.value) == 'Variable "integer1" is not of type integer, but of type '+str(type(integer1))

    # Test 5 with a string and name of variable as positional argument
    with pytest.raises(TypeIntegerError) as exceptioninfo:
        integer1 = 'This is a string'
        error_not_isinteger(integer1, 'integer1')
    assert str(exceptioninfo.value) == 'Variable "integer1" is not of type integer, but of type '+str(type(integer1))


def test_error_not_isnumber():
    # Test 1 with an integer only, no error will occur
    number1 = 101
    error_not_isnumber(number1)

    # Test 2 with an integer and name of variable, no error will occur
    number1 = 101
    error_not_isnumber(number1, name_inputvariable_in_text='number1')

    # Test 3 with a float only, no error will occur
    number1 = 101.23
    error_not_isnumber(number1)

    # Test 4 with a float and name of variable, no error will occur
    number1 = 101.23
    error_not_isnumber(number1, name_inputvariable_in_text='number1')

    # Test 5 with a string
    with pytest.raises(TypeNumberError) as exceptioninfo:
        number1 = 'This is a string'
        error_not_isnumber(number1)
    assert str(exceptioninfo.value) == 'Variable is not of type integer and not of type float, but of type '+str(type(number1))

    # Test 6 with a list and name of variable
    with pytest.raises(TypeNumberError) as exceptioninfo:
        number1 = [404, 505]
        error_not_isnumber(number1, name_inputvariable_in_text='number1')
    assert str(exceptioninfo.value) == 'Variable "number1" is not of type integer and not of type float, but of type '+str(type(number1))

    # Test 7 with a string and name of variable as positional argument
    with pytest.raises(TypeNumberError) as exceptioninfo:
        number1 = 'This is a string'
        error_not_isnumber(number1, 'number1')
    assert str(exceptioninfo.value) == 'Variable "number1" is not of type integer and not of type float, but of type '+str(type(number1))


def test_error_not_isstring():
    # Test 1 with a string only, no error will occur
    string1 = 'This is a string'
    error_not_isstring(string1)

    # Test 2 with a string and name of variable, no error will occur
    string1 = 'This is a string'
    error_not_isstring(string1, name_inputvariable_in_text='string1')

    # Test 3 with a list
    with pytest.raises(TypeStringError) as exceptioninfo:
        string1 = ['This', 'is', 'a', 'list', 'of', 'strings']
        error_not_isstring(string1)
    assert str(exceptioninfo.value) == 'Variable is not of type string, but of type '+str(type(string1))

    # Test 4 with a int and name of variable
    with pytest.raises(TypeStringError) as exceptioninfo:
        string1 = 404
        error_not_isstring(string1, name_inputvariable_in_text='string1')
    assert str(exceptioninfo.value) == 'Variable "string1" is not of type string, but of type '+str(type(string1))

    # Test 5 with a list of strings and name of variable as positional argument
    with pytest.raises(TypeStringError) as exceptioninfo:
        string1 = ['This', 'is', 'a', 'list', 'of', 'strings']
        error_not_isstring(string1, 'string1')
    assert str(exceptioninfo.value) == 'Variable "string1" is not of type string, but of type '+str(type(string1))


def test_error_not_isboolean():
    # Test 1 with a boolean only, no error will occur
    bool1 = True
    error_not_isboolean(bool1)

    # Test 2 with a boolean and name of variable, no error will occur
    bool1 = False
    error_not_isboolean(bool1, name_inputvariable_in_text='bool')

    # Test 3 with a string
    with pytest.raises(TypeBooleanError) as exceptioninfo:
        bool1 = 'This is a string'
        error_not_isboolean(bool1)
    assert str(exceptioninfo.value) == 'Variable is not of type boolean, but of type '+str(type(bool1))

    # Test 4 with a int and name of variable
    with pytest.raises(TypeBooleanError) as exceptioninfo:
        bool1 = 404
        error_not_isboolean(bool1, name_inputvariable_in_text='bool1')
    assert str(exceptioninfo.value) == 'Variable "bool1" is not of type boolean, but of type '+str(type(bool1))

    # Test 5 with a string and name of variable as positional argument
    with pytest.raises(TypeBooleanError) as exceptioninfo:
        bool1 = 'This is a string'
        error_not_isboolean(bool1, 'bool1')
    assert str(exceptioninfo.value) == 'Variable "bool1" is not of type boolean, but of type '+str(type(bool1))


def test_error_not_isdataframe():
    # Test 1 with a DataFrame only, no error will occur
    df = pd.DataFrame({'Column1': ['Value1', 'Value2']})
    error_not_isdataframe(df)
    
    # Test 2 with a DataFrame and name of variable, no error will occur
    df = pd.DataFrame({'Column1': ['Value1', 'Value2']})
    error_not_isdataframe(df, name_inputvariable_in_text='df')

    # Test 3 with a string 
    with pytest.raises(TypeDataFrameError) as exceptioninfo:
        df = 'This is a string'
        error_not_isdataframe(df)
    assert str(exceptioninfo.value) == 'Variable is not of type dataframe, but of type '+str(type(df))

    # Test 4 with a int and name of variable
    with pytest.raises(TypeDataFrameError) as exceptioninfo:
        df = 404
        error_not_isdataframe(df, name_inputvariable_in_text='df')
    assert str(exceptioninfo.value) == 'Variable "df" is not of type dataframe, but of type '+str(type(df))

    # Test 5 with a string and name of variable as positional argument
    with pytest.raises(TypeDataFrameError) as exceptioninfo:
        df = 'This is a string'
        error_not_isdataframe(df, 'df')
    assert str(exceptioninfo.value) == 'Variable "df" is not of type dataframe, but of type '+str(type(df))


def test_error_not_isaxes():
    # Test 1 with an axes only, no error will occur
    _, axes1 = plt.subplots()
    error_not_isaxes(axes1)
    plt.close(_)

    # Test 2 with an axes and name of variable, no error will occur
    _, axes1 = plt.subplots()
    error_not_isaxes(axes1, name_inputvariable_in_text='axes1')
    plt.close(_)

    # Test 3 with a list
    with pytest.raises(TypeAxesError) as exceptioninfo:
        axes1 = 'This is a string'
        error_not_isaxes(axes1)
    assert str(exceptioninfo.value) == 'Variable is not of type Axes, but of type '+str(type(axes1))

    # Test 4 with a int and name of variable
    with pytest.raises(TypeAxesError) as exceptioninfo:
        axes1 = 404
        error_not_isaxes(axes1, name_inputvariable_in_text='axes1')
    assert str(exceptioninfo.value) == 'Variable "axes1" is not of type Axes, but of type '+str(type(axes1))

    # Test 5 with a string and name of variable as positional argument
    with pytest.raises(TypeAxesError) as exceptioninfo:
        axes1 = 'This is a string'
        error_not_isaxes(axes1, 'axes1')
    assert str(exceptioninfo.value) == 'Variable "axes1" is not of type Axes, but of type '+str(type(axes1))


def test_error_not_isfigure():
    # Test 1 with a figure only, no error will occur
    figure1, _ = plt.subplots()
    error_not_isfigure(figure1)
    plt.close(figure1)

    # Test 2 with a figure and name of variable, no error will occur
    figure1, _ = plt.subplots()
    error_not_isfigure(figure1, name_inputvariable_in_text='figure1')
    plt.close(figure1)

    # Test 3 with a list
    with pytest.raises(TypeFigureError) as exceptioninfo:
        figure1 = 'This is a string'
        error_not_isfigure(figure1)
    assert str(exceptioninfo.value) == 'Variable is not of type Figure, but of type '+str(type(figure1))

    # Test 4 with a int and name of variable
    with pytest.raises(TypeFigureError) as exceptioninfo:
        figure1 = 404
        error_not_isfigure(figure1, name_inputvariable_in_text='figure1')
    assert str(exceptioninfo.value) == 'Variable "figure1" is not of type Figure, but of type '+str(type(figure1))

    # Test 5 with a string and name of variable as positional argument
    with pytest.raises(TypeFigureError) as exceptioninfo:
        figure1 = 'This is a string'
        error_not_isfigure(figure1, 'figure1')
    assert str(exceptioninfo.value) == 'Variable "figure1" is not of type Figure, but of type '+str(type(figure1))


def test_convert_to_native_python_type():
    # Test 1 - Max float
    data     = pd.DataFrame({'PY'       : [32, 38.2, 40, 39, 38],        # Float
                             'AC'       : [35, 33, 39, 37, 36]})         # Integer
    expected1 = 40.0
    actual1   = convert_to_native_python_type(data['PY'].max())
    message   = "Test 1a - convert_to_native_python_type returned {0} instead of {1}".format(actual1, expected1)
    assert actual1 == expected1, message
    expected2 = type(expected1)
    actual2   = type(actual1)
    message   = "Test 1b - convert_to_native_python_type returned type {0} instead of type {1}".format(actual2, expected2)
    assert actual2 == expected2, message

    # Test 2 - Min integer
    data     = pd.DataFrame({'PY'       : [32, 38.2, 40, 39, 38],        # Float
                             'AC'       : [35, 33, 39, 37, 36]})         # Integer
    expected1 = 33
    actual1   = convert_to_native_python_type(data['AC'].min())
    message   = "Test 2a - convert_to_native_python_type returned {0} instead of {1}".format(actual1, expected1)
    assert actual1 == expected1, message
    expected2 = type(expected1)
    actual2   = type(actual1)
    message   = "Test 2b - convert_to_native_python_type returned type {0} instead of type {1}".format(actual2, expected2)
    assert actual2 == expected2, message

    # Test 3 - Mean float
    data     = pd.DataFrame({'PY'       : [32, 38.2, 40, 39, 38],        # Float
                             'AC'       : [35, 33, 39, 37, 36]})         # Integer
    expected1 = 37.44
    actual1   = convert_to_native_python_type(data['PY'].mean())
    message   = "Test 3a - convert_to_native_python_type returned {0} instead of {1}".format(actual1, expected1)
    assert actual1 == expected1, message
    expected2 = type(expected1)
    actual2   = type(actual1)
    message   = "Test 3b - convert_to_native_python_type returned type {0} instead of type {1}".format(actual2, expected2)
    assert actual2 == expected2, message

    # Test 4 - Sum integer
    data     = pd.DataFrame({'PY'       : [32, 38.2, 40, 39, 38],        # Float
                             'AC'       : [35, 33, 39, 37, 36]})         # Integer
    expected1 = 180
    actual1   = convert_to_native_python_type(data['AC'].sum())
    message   = "Test 4a - convert_to_native_python_type returned {0} instead of {1}".format(actual1, expected1)
    assert actual1 == expected1, message
    expected2 = type(expected1)
    actual2   = type(actual1)
    message   = "Test 4b - convert_to_native_python_type returned type {0} instead of type {1}".format(actual2, expected2)
    assert actual2 == expected2, message


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
    # Test 1 - data-list to be rounded with 0 decimals
    data     = [15, 3.56, 4.876, 45.932, 100]
    expected = [15, 4, 5, 46, 100]
    actual   = optimize_data(data=data, numerator=1, denominator=1, decimals=0)
    message  = "Test 1 - optimize_data returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message
    
    # Test 2 - data-list to be rounded with 1 decimals
    data     = [15, 3.56, 4.876, 45.932, 100]
    expected = [15.0, 3.6, 4.9, 45.9, 100.0]
    actual   = optimize_data(data=data, numerator=1, denominator=1, decimals=1)
    message  = "Test 2 - optimize_data returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 3 - data-list to be rounded with 2 decimals
    # Be aware (before output) that some values won't get trailing zeros to get to two decimals
    data     = [15, 3.56, 4.876, 45.932, 100]
    expected = [15.0, 3.56, 4.88, 45.93, 100.0]
    actual   = optimize_data(data=data, numerator=1, denominator=1, decimals=2)
    message  = "Test 3 - optimize_data returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 4 - data-list with no rounding
    data     = [15, 3.56, 4.876, 45.932, 100]
    expected = [5.142857142857143, 1.2205714285714286, 1.6717714285714287, 15.748114285714285, 34.285714285714285]
    actual   = optimize_data(data=data, numerator=12, denominator=35, decimals=None)
    message  = "Test 4 - optimize_data returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message

    # Test 5 - integer rounded with 0 decimals
    data     = 16
    expected = 16
    actual   = optimize_data(data=data, numerator=1, denominator=1, decimals=0)
    message  = "Test 5 - optimize_data returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 6 - integer rounded with 1 decimals
    data     = 16
    expected = 16.0
    actual   = optimize_data(data=data, numerator=1, denominator=1, decimals=1)
    message  = "Test 6 - optimize_data returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 7 - integer rounded with 2 decimals
    # Be aware (before output) that some values won't get trailing zeros to get to two decimals
    data     = 16
    expected = 16.0
    actual   = optimize_data(data=data, numerator=1, denominator=1, decimals=2)
    message  = "Test 7 - optimize_data returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 8 - float rounded with 0 decimals
    data     = 16.37682
    expected = 16
    actual   = optimize_data(data=data, numerator=1, denominator=1, decimals=0)
    message  = "Test 8 - optimize_data returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 9 - float rounded with 1 decimals
    data     = 16.37682
    expected = 16.4
    actual   = optimize_data(data=data, numerator=1, denominator=1, decimals=1)
    message  = "Test 9 - optimize_data returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 10 - float rounded with 2 decimals
    data     = 16.37682
    expected = 16.38
    actual   = optimize_data(data=data, numerator=1, denominator=1, decimals=2)
    message  = "Test 10 - optimize_data returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 11 - None
    data     = None
    expected = None
    actual   = optimize_data(data=data, numerator=1, denominator=1, decimals=1)
    message  = "Test 11 - optimize_data returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 12 - String
    data     = "This is a string"
    expected = "This is a string"
    actual   = optimize_data(data=data, numerator=1, denominator=1, decimals=1)
    message  = "Test 12 - optimize_data returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 13 - Optimizing with other numerator and denominator and decimals
    data     = 123456789
    expected = 370.37
    actual   = optimize_data(data=data, numerator=3, denominator=1000000, decimals=2)
    message  = "Test 13 - optimize_data returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 14 - Optimizing with other numerator and denominator and no rounding
    data     = 123456789
    expected = 370.370367
    actual   = optimize_data(data=data, numerator=3, denominator=1000000, decimals=None)
    message  = "Test 14 - optimize_data returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message

    # Test 15 - Denominator = 0
    with pytest.raises(ValueError):
        data    = 3
        optimize_data(data=data, numerator=3, denominator=0, decimals=1)

    # Test 16 - Denominator = string
    with pytest.raises(TypeError):
        data    = 3
        optimize_data(data=data, numerator=3, denominator="This is a string", decimals=1)

    # Test 17 - Nominator = string
    with pytest.raises(TypeError):
        data    = 3
        optimize_data(data=data, numerator="This is a string", denominator=1, decimals=1)

    # Test 18 - Decimals = string
    with pytest.raises(TypeIntegerError):
        data    = 3
        optimize_data(data=data, numerator=1, denominator=1, decimals="This is a string")

    # Test 19 - Decimals = float
    with pytest.raises(TypeIntegerError):
        data    = 3
        optimize_data(data=data, numerator=1, denominator=1, decimals=1.1)

def test_convert_number_to_string():
    # Test 1 - floats rounded with 1 decimals and delta_value=False
    data     = (16.37682, -106.839, 387, -85726.4923)
    expected = ('16.4', '-106.8', '387.0', '-85726.5')
    for data_item, expected_item in zip(data, expected):
        actual   = convert_number_to_string(data=data_item, decimals=1, delta_value=False)
        message  = "Test 1 - convert_number_to_string returned {0} instead of {1}".format(actual, expected_item)
        assert actual == expected_item, message

    # Test 2 - floats rounded with 1 decimals and delta_value=True
    data     = (16.37682, -106.839, 387, -85726.4923)
    expected = ('+16.4', '-106.8', '+387.0', '-85726.5')
    for data_item, expected_item in zip(data, expected):
        actual   = convert_number_to_string(data=data_item, decimals=1, delta_value=True)
        message  = "Test 2 - convert_number_to_string returned {0} instead of {1}".format(actual, expected_item)
        assert actual == expected_item, message

    # Test 3 - floats rounded with 2 decimals and delta_value=False
    data     = (16.37682, -106.839, 387, -85726.4963)
    expected = ('16.38', '-106.84', '387.00', '-85726.50')
    for data_item, expected_item in zip(data, expected):
        actual   = convert_number_to_string(data=data_item, decimals=2, delta_value=False)
        message  = "Test 3 - convert_number_to_string returned {0} instead of {1}".format(actual, expected_item)
        assert actual == expected_item, message

    # Test 4 - floats rounded with 2 decimals and delta_value=True
    data     = (16.37682, -106.839, 387, -85726.4923)
    expected = ('+16.38', '-106.84', '+387.00', '-85726.49')
    for data_item, expected_item in zip(data, expected):
        actual   = convert_number_to_string(data=data_item, decimals=2, delta_value=True)
        message  = "Test 4 - convert_number_to_string returned {0} instead of {1}".format(actual, expected_item)
        assert actual == expected_item, message

    # Test 5 - floats rounded with 3 decimals and delta_value=False
    data     = (16.37682, -106.8395, 387, -85726.4966, 85726.49651)
    expected = ('16.377', '-106.840', '387.000', '-85726.497', '85726.497')
    for data_item, expected_item in zip(data, expected):
        actual   = convert_number_to_string(data=data_item, decimals=3, delta_value=False)
        message  = "Test 5 - convert_number_to_string returned {0} instead of {1}".format(actual, expected_item)
        assert actual == expected_item, message

    # Test 6 - floats rounded with 3 decimals and delta_value=True
    data     = (16.37682, -106.839, 387, -85726.4923)
    expected = ('+16.377', '-106.839', '+387.000', '-85726.492')
    for data_item, expected_item in zip(data, expected):
        actual   = convert_number_to_string(data=data_item, decimals=3, delta_value=True)
        message  = "Test 6 - convert_number_to_string returned {0} instead of {1}".format(actual, expected_item)
        assert actual == expected_item, message

    # Test 7 - floats rounded with 0 decimals and delta_value=False
    data     = (16.37682, -106.8395, 387, -85726.4966, 85726.49651)
    expected = ('16', '-107', '387', '-85726', '85726')
    for data_item, expected_item in zip(data, expected):
        actual   = convert_number_to_string(data=data_item, decimals=0, delta_value=False)
        message  = "Test 7 - convert_number_to_string returned {0} instead of {1}".format(actual, expected_item)
        assert actual == expected_item, message

    # Test 8 - floats rounded with 0 decimals and delta_value=True
    data     = (16.37682, -106.839, 387, -85726.4923)
    expected = ('+16', '-107', '+387', '-85726')
    for data_item, expected_item in zip(data, expected):
        actual   = convert_number_to_string(data=data_item, decimals=0, delta_value=True)
        message  = "Test 8 - convert_number_to_string returned {0} instead of {1}".format(actual, expected_item)
        assert actual == expected_item, message

    # Test 9 - list of floats rounded with 1 decimals and delta_value=False
    data     = [16.37682, -106.839, 387, -85726.4923]
    expected = ['16.4', '-106.8', '387.0', '-85726.5']
    actual   = convert_number_to_string(data=data, decimals=1, delta_value=False)
    message  = "Test 9 - convert_number_to_string returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 10 - list of floats rounded with 1 decimals and delta_value=True
    data     = [16.37682, -106.839, 387, -85726.4923]
    expected = ['+16.4', '-106.8', '+387.0', '-85726.5']
    actual   = convert_number_to_string(data=data, decimals=1, delta_value=True)
    message  = "Test 10 - convert_number_to_string returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 11 - list of floats rounded with 2 decimals and delta_value=False
    data     = [16.37682, -106.839, 387, -85726.4963]
    expected = ['16.38', '-106.84', '387.00', '-85726.50']
    actual   = convert_number_to_string(data=data, decimals=2, delta_value=False)
    message  = "Test 11 - convert_number_to_string returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 12 - list of floats rounded with 2 decimals and delta_value=True
    data     = [16.37682, -106.839, 387, -85726.4923]
    expected = ['+16.38', '-106.84', '+387.00', '-85726.49']
    actual   = convert_number_to_string(data=data, decimals=2, delta_value=True)
    message  = "Test 12 - convert_number_to_string returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 13 - list of floats rounded with 3 decimals and delta_value=False
    data     = [16.37682, -106.8395, 387, -85726.4966, 85726.49651]
    expected = ['16.377', '-106.840', '387.000', '-85726.497', '85726.497']
    actual   = convert_number_to_string(data=data, decimals=3, delta_value=False)
    message  = "Test 13 - convert_number_to_string returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 14 - list of floats rounded with 3 decimals and delta_value=True
    data     = [16.37682, -106.839, 387, -85726.4923]
    expected = ['+16.377', '-106.839', '+387.000', '-85726.492']
    actual   = convert_number_to_string(data=data, decimals=3, delta_value=True)
    message  = "Test 14 - convert_number_to_string returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 15 - list of floats rounded with 0 decimals and delta_value=False
    data     = [16.37682, -106.8395, 387, -85726.4966, 85726.49651]
    expected = ['16', '-107', '387', '-85726', '85726']
    actual   = convert_number_to_string(data=data, decimals=0, delta_value=False)
    message  = "Test 15 - convert_number_to_string returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 16 - list of floats rounded with 0 decimals and delta_value=True
    data     = [16.37682, -106.839, 387, -85726.4923]
    expected = ['+16', '-107', '+387', '-85726']
    actual   = convert_number_to_string(data=data, decimals=0, delta_value=True)
    message  = "Test 16 - convert_number_to_string returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 17 - tuple of floats rounded with 1 decimals and delta_value=False returns a string
    data     = (16.37682, -106.8395, 387, -85726.4966, 85726.49651)
    expected = '(16.37682, -106.8395, 387, -85726.4966, 85726.49651)'
    actual   = convert_number_to_string(data=data, decimals=1, delta_value=False)
    message  = "Test 17 - convert_number_to_string returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 18 - list of floats rounded with None decimals and delta_value=True
    data     = [16.37682, -106.8395, 387, -85726.4966, 85726.49651]
    expected = [16.37682, -106.8395, 387, -85726.4966, 85726.49651]
    actual   = convert_number_to_string(data=data, decimals=None, delta_value=True)
    message  = "Test 18 - convert_number_to_string returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 19 - String
    data     = "This is a string"
    expected = "This is a string"
    actual   = convert_number_to_string(data=data, decimals=None, delta_value=True)
    message  = "Test 19 - convert_number_to_string returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 20 - delta_value = None
    with pytest.raises(TypeBooleanError):
        convert_number_to_string(data=1, decimals=1, delta_value=None)

    # Test 21 - decimals = float
    with pytest.raises(TypeIntegerError):
        convert_number_to_string(data=1, decimals=1.23, delta_value=False)

    # Test 22 - decimals = 4
    with pytest.raises(ValueError):
        convert_number_to_string(data=1, decimals=4, delta_value=False)


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


def test_filter_lists():
    # Test 1 - list1 is a subset of list 2 and the order of the elements is different
    list1    = ['AC', 'PY']
    list2    = ['PY', 'PL', 'AC', 'FC']
    expected = ['AC', 'PY']
    actual   = filter_lists(list1=list1, list2=list2)
    message  = "Test 1 - filter_lists returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 2 - list1 is not a subset of list 2 and the order of the elements is different
    list1    = ['AC', 'PL']
    list2    = ['PY', 'AC', 'FC']
    expected = ['AC']
    actual   = filter_lists(list1=list1, list2=list2)
    message  = "Test 2 - filter_lists returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 3 - list1 is not present, expect a TypeError, for the default of list1 is None
    with pytest.raises(TypeError):
        list2    = ['PY', 'AC', 'FC']
        filter_lists(list2=list2)

    # Test 4 - list2 is not present, expect a TypeError, for the default of list2 is None
    with pytest.raises(TypeError):
        list1    = ['PY', 'AC', 'FC']
        filter_lists(list1=list1)


def test_list1_is_subset_list2():
    # Test 1 - list1 is a subset of list 2
    list1    = ['AC', 'PY']
    list2    = ['PY', 'PL', 'AC', 'FC']
    expected = True
    actual   = list1_is_subset_list2(list1=list1, list2=list2)
    message  = "Test 1 - list1_is_subset_list2 returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 2 - list1 is not a subset of list 2
    list1    = ['AC', 'PL']
    list2    = ['PY', 'AC', 'FC']
    expected = False
    actual   = list1_is_subset_list2(list1=list1, list2=list2)
    message  = "Test 2 - list1_is_subset_list2 returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 3 - list1 is not present, expect a TypeError, for the default of list1 is None
    with pytest.raises(TypeListError):
        list2    = ['PY', 'AC', 'FC']
        list1_is_subset_list2(list2=list2)

    # Test 4 - list2 is not present, expect a TypeError, for the default of list2 is None
    with pytest.raises(TypeListError):
        list1    = ['PY', 'AC', 'FC']
        list1_is_subset_list2(list1=list1)


def test_convert_data_string_to_pandas_dataframe():
    # Test 1 - good string to pandas DataFrame conversion 
    dataset  = """
               Year,Month,PL,AC,FC,PY
               2021,1,0,32,0,0
               2021,5,0,41,0,0

               2021,6,0,37,0,0
               2021,7,0,33,0,0
               2021,2,0,38,0,0
               2021,3,0,29,0,0
               2021,4,0,35,0,0
               2021,8,0,38,0,0
               2021,9,0,42,0,0
               2021,10,0,44,0,0
               2021,11,0,39,0,0
               2021,12,24,31,48,0
               2020,10,0,44,0,0
               2020,11,0,39,0,0
               2020,12,0,31,0,0
               2022,1,33,35,0,32
               2022,2,35,33,0,38
               2022,3,37,41,0,29
               2022,4,40,41,0,35
               2022,5,38,37,0,41
               2022,6,36,37,0,37
               2022,7,35,0,38,33
               2022,8,40,0,44,38
               2022,9,45.0328,0,46,42
               2022,10,50.8000,0,48,44
               2022,11,45,0,44,39
               2022,12,40,0,44,31
               """
    expected = {'Year' : ['2021', '2021', '2021', '2021', '2021', '2021', '2021', '2021', '2021', '2021', '2021', '2021', '2020', '2020',
                          '2020', '2022', '2022', '2022', '2022', '2022', '2022', '2022', '2022', '2022', '2022', '2022', '2022'],
                'Month': ['1', '5', '6', '7', '2', '3', '4', '8', '9', '10', '11', '12', '10', '11', '12',
                          '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
                'PL'   : ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '24', '0', '0', '0',
                          '33', '35', '37', '40', '38', '36', '35', '40', '45.0328', '50.8000', '45', '40'],
                'AC'   : ['32', '41', '37', '33', '38', '29', '35', '38', '42', '44', '39', '31', '44',
                          '39', '31', '35', '33', '41', '41', '37', '37', '0', '0', '0', '0', '0', '0'],
                'FC'   : ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '48', '0', '0', '0', '0',
                          '0', '0', '0', '0', '0', '38', '44', '46', '48', '44', '44'],
                'PY'   : ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
                          '32', '38', '29', '35', '41', '37', '33', '38', '42', '44', '39', '31']}
    actual   = convert_data_string_to_pandas_dataframe(dataset)
    actual   = actual.to_dict(orient='list')
    message  = "Test 1 - convert_data_string_to_pandas_dataframe returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 2 - good string to pandas DataFrame conversion (extra white lines are intended for the test)
    dataset  = """

                 Country,       PY , PL , AC , FC 
                 Spain,         30 , 33 , 53 ,  0 
                 Greece,        38 , 33 , 39 ,  0
                 Sweden,        38 , 35 , 40 ,  0

                 Germany,       90 , 89 , 93 ,  0
                 Russia,        60 , 56 , 60 ,  0
                 Italy,         15 , 12 , 14 ,  0

                 Great Britain, 15 , 13 , 15 ,  0
                 Slovenia,       4 ,  5 ,  4 ,  0
                 Denmark,       29 , 35 , 33 ,  0
                 Netherlands,   39 , 42 , 38 ,  0
                 France,        60 , 77 , 63 ,  0
                 OTHER,         40 , 37 , 44 ,  0    
                 
               """
    expected = {'Country': ['Spain', 'Greece', 'Sweden', 'Germany', 'Russia', 'Italy', 'Great Britain', 'Slovenia', 'Denmark', 'Netherlands', 'France', 'OTHER'],
                     'PY': ['30', '38', '38', '90', '60', '15', '15', '4', '29', '39', '60', '40'], 
                     'PL': ['33', '33', '35', '89', '56', '12', '13', '5', '35', '42', '77', '37'], 
                     'AC': ['53', '39', '40', '93', '60', '14', '15', '4', '33', '38', '63', '44'], 
                     'FC': [ '0',  '0',  '0',  '0',  '0',  '0',  '0', '0',  '0',  '0',  '0',  '0']}
    actual   = convert_data_string_to_pandas_dataframe(dataset)
    actual   = actual.to_dict(orient='list')
    message  = "Test 2 - convert_data_string_to_pandas_dataframe returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 3 - only string supported, we try it with a float
    with pytest.raises(TypeError):
        convert_data_string_to_pandas_dataframe(1.2)


def test_convert_data_list_of_lists_to_pandas_dataframe():
    # Test 1 - good list of lists 
    dataset = [['Year', 'Month', 'AC', 'PL', 'FC'], [2022, 1, 35, 33, 0], [2022, 2, 38, 40, 0], [2022, 3, 29, 35, 0]]
    expected = {'Year' : [2022, 2022, 2022], 
                'Month': [1, 2, 3], 
                'AC'   : [35, 38, 29], 
                'PL'   : [33, 40, 35], 
                'FC'   : [0, 0, 0]} 
    actual   = convert_data_list_of_lists_to_pandas_dataframe(dataset)
    actual   = actual.to_dict(orient='list')
    message  = "Test 1 - convert_data_list_of_lists_to_pandas_dataframe returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 2 - only list (of lists) supported, we try it with a string
    with pytest.raises(TypeError):
        convert_data_list_of_lists_to_pandas_dataframe("This is a string")

    # Test 3 - only list (of lists) supported, we try it with a string element in a list
    with pytest.raises(TypeError):
        dataset = [['Year', 'Month', 'AC', 'PL', 'FC'], [2022, 1, 35, 33, 0], "This element is a string", [2022, 3, 29, 35, 0]]
        convert_data_list_of_lists_to_pandas_dataframe(dataset)


def test_dataframe_translate_field_headers():
    # Test 1 - good dataframe with column names to be translated
    dataset = pd.DataFrame({'Invoicedate' : [1, 2, 3], 
                            'Revenue'     : [4, 5, 6],
                            'Budget'      : [7, 8, 9]})
    translate_headers = {'Invoicedate':'Date', 'Revenue':'AC', 'Budget':'PL'}
    expected =  {'Date': [1, 2, 3], 
                 'AC'  : [4, 5, 6], 
                 'PL'  : [7, 8, 9]}
    actual   = dataframe_translate_field_headers(dataset, translate_headers=translate_headers)
    actual   = actual.to_dict(orient='list')
    message  = "Test 1 - dataframe_translate_field_headers returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 2 - only dataframe supported
    with pytest.raises(TypeError):
        dataframe_translate_field_headers("This is a string")

    # Test 3 - a dataframe with missing column
    with pytest.raises(TypeError):
        dataset = pd.DataFrame({'Invoicedate' : [1, 2, 3], 
                                'Revenue'     : [4, 5, 6],
                                'Budget'      : [7, 8, 9]})
        translate_headers=['list item 1', 'list item 2']
        dataframe_translate_field_headers(dataset, translate_headers=translate_headers)


def test_dataframe_search_for_headers():
    # Test 1 - good dataframe, search for available headers and error when not found
    dataset = pd.DataFrame({'Year' : [2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022], 
                            'Month': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                            'PY': [32, 38, 29, 35, 41, 37, 33, 38, 42, 44, 39, 31], 
                            'PL': [33, 35, 37, 40, 38, 36, 35, 40, 45.0328, 50.8, 45, 40], 
                            'AC': [35, 33, 41, 41, 37, 37, 0, 0, 0, 0, 0, 0], 
                            'FC': [0, 0, 0, 0, 0, 0, 38, 44, 46, 48, 44, 44]})
    search_for_headers = ['Year', 'Month', 'PY', 'PL', 'AC', 'FC']
    error_not_found    = True
    expected = search_for_headers
    actual   = dataframe_search_for_headers(dataframe=dataset, search_for_headers=search_for_headers, error_not_found=error_not_found)
    message  = "Test 1 - dataframe_search_for_headers returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 2 - good dataframe, search for other headers also and no error when not found
    dataset = pd.DataFrame({'Year' : [2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022], 
                            'Month': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                            'PY': [32, 38, 29, 35, 41, 37, 33, 38, 42, 44, 39, 31], 
                            'PL': [33, 35, 37, 40, 38, 36, 35, 40, 45.0328, 50.8, 45, 40], 
                            'AC': [35, 33, 41, 41, 37, 37, 0, 0, 0, 0, 0, 0], 
                            'FC': [0, 0, 0, 0, 0, 0, 38, 44, 46, 48, 44, 44]})
    search_for_headers = ['Date', 'AC', 'Other']
    error_not_found    = False
    expected = ['AC']
    actual   = dataframe_search_for_headers(dataframe=dataset, search_for_headers=search_for_headers, error_not_found=error_not_found)
    message  = "Test 2 - dataframe_search_for_headers returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 3 - good dataframe, search for other headers also and error when not found
    with pytest.raises(ValueError):
        dataset = pd.DataFrame({'Year' : [2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022], 
                                'Month': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                                'PY': [32, 38, 29, 35, 41, 37, 33, 38, 42, 44, 39, 31], 
                                'PL': [33, 35, 37, 40, 38, 36, 35, 40, 45.0328, 50.8, 45, 40], 
                                'AC': [35, 33, 41, 41, 37, 37, 0, 0, 0, 0, 0, 0], 
                                'FC': [0, 0, 0, 0, 0, 0, 38, 44, 46, 48, 44, 44]})
        search_for_headers = ['Date', 'AC', 'Other']
        error_not_found    = True
        dataframe_search_for_headers(dataframe=dataset, search_for_headers=search_for_headers, error_not_found=error_not_found)

    # Test 4 - only DataFrame supported as first parameter
    with pytest.raises(TypeDataFrameError):
        dataframe_search_for_headers(dataframe="This is a string", search_for_headers=list())

    # Test 5 - only list supported as second parameter
    with pytest.raises(TypeListError):
        dataset = pd.DataFrame({'Year' : [2023]})
        dataframe_search_for_headers(dataframe=dataset, search_for_headers="This is a string")

    # Test 6 - only boolean supported as third parameter
    with pytest.raises(TypeBooleanError):
        dataset = pd.DataFrame({'Year' : [2023]})
        dataframe_search_for_headers(dataframe=dataset, search_for_headers=list(), error_not_found="This is a string")


def test_dataframe_date_to_year_and_month():
    # Test 1 - good dataframe with date, but without year and month
    dataset = pd.DataFrame({'Date' : ['20220101', '2022-02-21', '2022-03-01', '2022-04-01', '2022-05-01', '20220628', '2022-07-25', '2022-08-05', '20220916',
                                      '20221015', '2022-11-12', '2022-12-23'], 
                            'PY': [32, 38, 29, 35, 41, 37, 33, 38, 42, 44, 39, 31], 
                            'PL': [33, 35, 37, 40, 38, 36, 35, 40, 45.0328, 50.8, 45, 40], 
                            'AC': [35, 33, 41, 41, 37, 37, 0, 0, 0, 0, 0, 0],
                            'FC': [0, 0, 0, 0, 0, 0, 38, 44, 46, 48, 44, 44]})
    expected = {'Date' : [Timestamp('2022-01-01 00:00:00'), Timestamp('2022-02-21 00:00:00'), Timestamp('2022-03-01 00:00:00'),
                          Timestamp('2022-04-01 00:00:00'), Timestamp('2022-05-01 00:00:00'), Timestamp('2022-06-28 00:00:00'),
                          Timestamp('2022-07-25 00:00:00'), Timestamp('2022-08-05 00:00:00'), Timestamp('2022-09-16 00:00:00'),
                          Timestamp('2022-10-15 00:00:00'), Timestamp('2022-11-12 00:00:00'), Timestamp('2022-12-23 00:00:00')],
                'Year' : [2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022],
                'Month': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                'PY'   : [32, 38, 29, 35, 41, 37, 33, 38, 42, 44, 39, 31],
                'PL'   : [33.0, 35.0, 37.0, 40.0, 38.0, 36.0, 35.0, 40.0, 45.0328, 50.8, 45.0, 40.0],
                'AC'   : [35, 33, 41, 41, 37, 37, 0, 0, 0, 0, 0, 0],
                'FC'   : [0, 0, 0, 0, 0, 0, 38, 44, 46, 48, 44, 44]}
    actual   = dataframe_date_to_year_and_month(dataset, date_field=['Date'], year_field=['Year'], month_field=['Month'])
    actual   = actual.to_dict(orient='list')
    message  = "Test 1 - dataframe_date_to_year_and_month returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 2 - good dataframe with date but with 'random' year and 'random' month
    # Note: There is NO TESTING in the productive function if the year and month out of the date are equal to the 'Year' and 'Month' columns provided.
    #       The columns 'Year' and 'Month' are overwritten.
    dataset = pd.DataFrame({'Date' : ['20220101', '2022-02-21', '2022-03-01', '2022-04-01', '2022-05-01', '20220628', '2022-07-25', '2022-08-05', '20220916',
                                      '20221015', '2022-11-12', '2022-12-23'],
                            'Year' : [2020, 2023, 2002, 2032, 1980, 1990, 2019, 2018, 2025, 2027, 2024, 2037],
                            'Month': [4, 2, 3, 1, 5, 9, 7, 8, 6, 12, 11, 10],
                            'PY': [32, 38, 29, 35, 41, 37, 33, 38, 42, 44, 39, 31],
                            'PL': [33, 35, 37, 40, 38, 36, 35, 40, 45.0328, 50.8, 45, 40],
                            'AC': [35, 33, 41, 41, 37, 37, 0, 0, 0, 0, 0, 0],
                            'FC': [0, 0, 0, 0, 0, 0, 38, 44, 46, 48, 44, 44]})
    expected = {'Date' : [Timestamp('2022-01-01 00:00:00'), Timestamp('2022-02-21 00:00:00'), Timestamp('2022-03-01 00:00:00'),
                          Timestamp('2022-04-01 00:00:00'), Timestamp('2022-05-01 00:00:00'), Timestamp('2022-06-28 00:00:00'),
                          Timestamp('2022-07-25 00:00:00'), Timestamp('2022-08-05 00:00:00'), Timestamp('2022-09-16 00:00:00'),
                          Timestamp('2022-10-15 00:00:00'), Timestamp('2022-11-12 00:00:00'), Timestamp('2022-12-23 00:00:00')],
                'Year' : [2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022],
                'Month': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                'PY'   : [32, 38, 29, 35, 41, 37, 33, 38, 42, 44, 39, 31],
                'PL'   : [33.0, 35.0, 37.0, 40.0, 38.0, 36.0, 35.0, 40.0, 45.0328, 50.8, 45.0, 40.0],
                'AC'   : [35, 33, 41, 41, 37, 37, 0, 0, 0, 0, 0, 0],
                'FC'   : [0, 0, 0, 0, 0, 0, 38, 44, 46, 48, 44, 44]}
    actual   = dataframe_date_to_year_and_month(dataset, date_field=['Date'], year_field=['Year'], month_field=['Month'])
    actual   = actual.to_dict(orient='list')
    message  = "Test 2 - dataframe_date_to_year_and_month returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 3 - good dataframe with date but with 'random' year and 'random' month - no month_field in function parameters
    # Note: There is NO TESTING in the productive function if the year and month out of the date are equal to the 'Year' and 'Month' columns provided.
    #       The columns 'Year' is overwritten, but 'Month' is not overwritten.
    dataset = pd.DataFrame({'Date' : ['20220101', '2022-02-21', '2022-03-01', '2022-04-01', '2022-05-01', '20220628', '2022-07-25', '2022-08-05', '20220916',
                                      '20221015', '2022-11-12', '2022-12-23'], 
                            'Year' : [2020, 2023, 2002, 2032, 1980, 1990, 2019, 2018, 2025, 2027, 2024, 2037], 
                            'Month': [4, 2, 3, 1, 5, 9, 7, 8, 6, 12, 11, 10],
                            'PY'   : [32, 38, 29, 35, 41, 37, 33, 38, 42, 44, 39, 31], 
                            'PL'   : [33, 35, 37, 40, 38, 36, 35, 40, 45.0328, 50.8, 45, 40], 
                            'AC'   : [35, 33, 41, 41, 37, 37, 0, 0, 0, 0, 0, 0],
                            'FC'   : [0, 0, 0, 0, 0, 0, 38, 44, 46, 48, 44, 44]})
    expected = {'Date' : [Timestamp('2022-01-01 00:00:00'), Timestamp('2022-02-21 00:00:00'), Timestamp('2022-03-01 00:00:00'),
                          Timestamp('2022-04-01 00:00:00'), Timestamp('2022-05-01 00:00:00'), Timestamp('2022-06-28 00:00:00'),
                          Timestamp('2022-07-25 00:00:00'), Timestamp('2022-08-05 00:00:00'), Timestamp('2022-09-16 00:00:00'),
                          Timestamp('2022-10-15 00:00:00'), Timestamp('2022-11-12 00:00:00'), Timestamp('2022-12-23 00:00:00')],
                'Year' : [2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022],
                'Month': [4, 2, 3, 1, 5, 9, 7, 8, 6, 12, 11, 10],
                'PY'   : [32, 38, 29, 35, 41, 37, 33, 38, 42, 44, 39, 31],
                'PL'   : [33.0, 35.0, 37.0, 40.0, 38.0, 36.0, 35.0, 40.0, 45.0328, 50.8, 45.0, 40.0],
                'AC'   : [35, 33, 41, 41, 37, 37, 0, 0, 0, 0, 0, 0],
                'FC'   : [0, 0, 0, 0, 0, 0, 38, 44, 46, 48, 44, 44]}
    actual   = dataframe_date_to_year_and_month(dataset, date_field=['Date'], year_field=['Year'], month_field=None)
    actual   = actual.to_dict(orient='list')
    message  = "Test 3 - dataframe_date_to_year_and_month returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 4 - only dataframe supported for first parameter
    with pytest.raises(TypeDataFrameError):
        dataframe_date_to_year_and_month(dataframe="This is a string", date_field=[1], year_field=[2], month_field=[3])

    # Test 5a - only list supported for date_field
    with pytest.raises(TypeError):
        dataframe_date_to_year_and_month(dataframe=pd.DataFrame({'Year' : [2022, 2023]}), date_field="This is a string", year_field=[2], month_field=[3])

    # Test 5b - only one element in list supported for date_field
    with pytest.raises(ValueError):
        dataframe_date_to_year_and_month(dataframe=pd.DataFrame({'Year' : [2022, 2023]}), date_field=[], year_field=[2], month_field=[3])

    # Test 5c - only one element in list supported for date_field
    with pytest.raises(ValueError):
        dataframe_date_to_year_and_month(dataframe=pd.DataFrame({'Year' : [2022, 2023]}), date_field=['one', 'two'], year_field=[2], month_field=[3])

    # Test 6a - only list supported for year_field
    with pytest.raises(TypeError):
        dataframe_date_to_year_and_month(dataframe=pd.DataFrame({'Year' : [2022, 2023]}), date_field=["one"], year_field=2023, month_field=[3])

    # Test 6b - only one element in list supported for year_field
    with pytest.raises(ValueError):
        dataframe_date_to_year_and_month(dataframe=pd.DataFrame({'Year' : [2022, 2023]}), date_field=["one"], year_field=[], month_field=[3])

    # Test 6c - only one element in list supported for year_field
    with pytest.raises(ValueError):
        dataframe_date_to_year_and_month(dataframe=pd.DataFrame({'Year' : [2022, 2023]}), date_field=["one"], year_field=['one', 'two'], month_field=[3])

    # Test 7a - only list supported for month_field
    with pytest.raises(TypeError):
        dataframe_date_to_year_and_month(dataframe=pd.DataFrame({'Year' : [2022, 2023]}), date_field=["one"], year_field=["year"], month_field=1.2)

    # Test 7b - only one element in list supported for month_field
    with pytest.raises(ValueError):
        dataframe_date_to_year_and_month(dataframe=pd.DataFrame({'Year' : [2022, 2023]}), date_field=["one"], year_field=["year"], month_field=[])

    # Test 7c - only one element in list supported for month_field
    with pytest.raises(ValueError):
        dataframe_date_to_year_and_month(dataframe=pd.DataFrame({'Year' : [2022, 2023]}), date_field=["one"], year_field=["year"], month_field=['one', 'two'])


def test_dataframe_keep_only_relevant_columns():
    # Test 1 - good dataframe with extra columns
    dataset = pd.DataFrame({'Year' : [2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022], 
                            'Month': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                            'PY': [32, 38, 29, 35, 41, 37, 33, 38, 42, 44, 39, 31], 
                            'PL': [33, 35, 37, 40, 38, 36, 35, 40, 45.0328, 50.8, 45, 40], 
                            'AC': [35, 33, 41, 41, 37, 37, 0, 0, 0, 0, 0, 0],
                            'AX': [10, 10, 10, 10, 10, 10, 10, 10, 10 ,10 ,10, 10],
                            'FC': [0, 0, 0, 0, 0, 0, 38, 44, 46, 48, 44, 44]})
    expected = {'Year': {0: 2022, 1: 2022, 2: 2022, 3: 2022, 4: 2022, 5: 2022, 6: 2022, 7: 2022, 8: 2022, 9: 2022, 10: 2022, 11: 2022}, 
                'Month': {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10, 10: 11, 11: 12}, 
                'PY': {0: 32, 1: 38, 2: 29, 3: 35, 4: 41, 5: 37, 6: 33, 7: 38, 8: 42, 9: 44, 10: 39, 11: 31}, 
                'PL': {0: 33.0, 1: 35.0, 2: 37.0, 3: 40.0, 4: 38.0, 5: 36.0, 6: 35.0, 7: 40.0, 8: 45.0328, 9: 50.8, 10: 45.0, 11: 40.0}, 
                'AC': {0: 35, 1: 33, 2: 41, 3: 41, 4: 37, 5: 37, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0}, 
                'FC': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 38, 7: 44, 8: 46, 9: 48, 10: 44, 11: 44}}
    wanted_headers = ['Year', 'Month', 'PY', 'PL', 'AC', 'FC']
    actual   = dataframe_keep_only_relevant_columns(dataset, wanted_headers=wanted_headers)
    actual   = actual.to_dict()
    message  = "Test 1 - ColumnWithWaterfall._dataframe_keep_only_relevant_columns returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 2 - only dataframe supported as dataset
    with pytest.raises(TypeDataFrameError):
        dataframe_keep_only_relevant_columns(dataframe="This is a string", wanted_headers=[1,2])

    # Test 3 - only list supported as wanted headers
    with pytest.raises(TypeListError):
        dataframe_keep_only_relevant_columns(dataframe=pd.DataFrame({'Year' : [2022, 2023]}), wanted_headers="This is a string")


def test_dataframe_convert_year_month_to_string():
    # Test 1 - good dataframe with string year values and integer and float values
    dataset   = pd.DataFrame({'Year' : [2022.0, '2021', '2018', 2019],
                              'Month': ['02', 4, '07', 8.0],
                              'AC'   : [35, 33, 17, 41]})
    expected1 = {'Year': {2: '2018', 3: '2019', 1: '2021', 0: '2022'},
                'Month': {2: '07', 3: '08', 1: '04', 0: '02'},
                'AC': {2: 17, 3: 41, 1: 33, 0: 35}}
    expected2 = {'Year': {2: '2018', 3: '2019', 1: '2021', 0: '2022'},
                 'Month': {2: '07', 3: '08', 1: '04', 0: '02'},
                 'AC': {2: 17, 3: 41, 1: 33, 0: 35}}
    wanted_headers = ['Year', 'Month']
    actual1   = dataframe_convert_year_month_to_string(dataset, wanted_headers=wanted_headers, year_field=['Year'], month_field=['Month'], sort_dataframe_parameter=True)
    actual1   = actual1.to_dict()
    message1  = "Test 1a - dataframe_convert_year_month_to_string returned {0} instead of {1}".format(actual1, expected1)
    actual2   = dataframe_convert_year_month_to_string(dataset, wanted_headers=wanted_headers, year_field=['Year'], month_field=['Month'], sort_dataframe_parameter=False)
    actual2   = actual2.to_dict()
    message2  = "Test 1b - dataframe_convert_year_month_to_string returned {0} instead of {1}".format(actual2, expected2)
    assert actual1 == expected1, message1
    assert actual2 == expected2, message2

    # Test 2 - good dataframe with string year values and integer and float values, also a category of interest is available
    dataset   = pd.DataFrame({'_Category' : ['sales', 'finance', 'sales', 'marketing', 'finance', 'sales'],
                            'Year'      : [2022.0 , '2021'   , '2018' , 2018       , 2018     , 2019   ],
                            'Month'     : ['02'   , 4        , '07'   , 6          , '6'      , 8.0    ],
                            'AC'        : [35     , 33       , 17     , 3          , 26       , 41     ]})
    expected1 = {'_Category': ['finance', 'marketing', 'sales', 'sales', 'finance', 'sales'],
                 'Year'     : ['2018', '2018', '2018', '2019', '2021', '2022'],
                 'Month'    : ['06', '06', '07', '08', '04', '02'],
                 'AC'       : [26, 3, 17, 41, 33, 35]}
    expected2 = {'_Category': ['sales', 'finance', 'sales', 'marketing', 'finance', 'sales'],
                 'Year': ['2022', '2021', '2018', '2018', '2018', '2019'],
                 'Month': ['02', '04', '07', '06', '06', '08'],
                 'AC': [35, 33, 17, 3, 26, 41]}
    wanted_headers = ['Year', 'Month', '_Category']
    actual1   = dataframe_convert_year_month_to_string(dataset, wanted_headers=wanted_headers, year_field=['Year'], month_field=['Month'], sort_dataframe_parameter=True)
    actual1   = actual1.to_dict(orient='list')
    message1  = "Test 2a - dataframe_convert_year_month_to_string returned {0} instead of {1}".format(actual1, expected1)
    actual2   = dataframe_convert_year_month_to_string(dataset, wanted_headers=wanted_headers, year_field=['Year'], month_field=['Month'], sort_dataframe_parameter=False)
    actual2   = actual2.to_dict(orient='list')
    message2  = "Test 2b - dataframe_convert_year_month_to_string returned {0} instead of {1}".format(actual2, expected2)
    assert actual1 == expected1, message1
    assert actual2 == expected2, message2

    # Test 3 - good dataframe without year values or month values, but with a category-of-interest
    dataset   = pd.DataFrame({'_Category' : ['sales', 'finance', 'operations', 'marketing'],
                            'AC'        : [35     , 33       , 17          , 3          ],
                            'PY'        : [32     , 37       , 19          , 2          ]})
    expected1 = {'_Category': ['sales', 'finance', 'operations', 'marketing'], 
                'AC': [35, 33, 17, 3], 
                'PY': [32, 37, 19, 2]}
    expected2 = {'_Category': ['sales', 'finance', 'operations', 'marketing'], 
                'AC': [35, 33, 17, 3], 
                'PY': [32, 37, 19, 2]}
    wanted_headers = ['_Category']
    actual1   = dataframe_convert_year_month_to_string(dataset, wanted_headers=wanted_headers, year_field=['Year'], month_field=['Month'], sort_dataframe_parameter=True)
    actual1   = actual1.to_dict(orient='list')
    message1  = "Test 3a - dataframe_convert_year_month_to_string returned {0} instead of {1}".format(actual1, expected1)
    actual2   = dataframe_convert_year_month_to_string(dataset, wanted_headers=wanted_headers, year_field=['Year'], month_field=['Month'], sort_dataframe_parameter=False)
    actual2   = actual2.to_dict(orient='list')
    message2  = "Test 3b - dataframe_convert_year_month_to_string returned {0} instead of {1}".format(actual2, expected2)
    assert actual1 == expected1, message1
    assert actual2 == expected2, message2

    # Test 4 - only dataframe supported
    with pytest.raises(TypeDataFrameError):
        dataframe_convert_year_month_to_string("This is a string", wanted_headers=['Year', 'Month'], year_field=['Year'], month_field=['Month'], sort_dataframe_parameter=True)

    # Test 5 - only list supported
    with pytest.raises(TypeListError):
        dataframe_convert_year_month_to_string(pd.DataFrame({'_Category' : ['sales'], 'AC' : [35]}), wanted_headers="This is a string", year_field=['Year'], month_field=['Month'], sort_dataframe_parameter=True)

    # Test 6 - only list supported
    with pytest.raises(TypeListError):
        dataframe_convert_year_month_to_string(pd.DataFrame({'_Category' : ['sales'], 'AC' : [35]}), wanted_headers=['Year', 'Month'], year_field="This is a string", month_field=['Month'], sort_dataframe_parameter=True)

    # Test 7 - only list supported
    with pytest.raises(TypeListError):
        dataframe_convert_year_month_to_string(pd.DataFrame({'_Category' : ['sales'], 'AC' : [35]}), wanted_headers=['Year', 'Month'], year_field=['Year'], month_field="This is a string", sort_dataframe_parameter=True)

    # Test 8 - only boolean supported
    with pytest.raises(TypeBooleanError):
        dataframe_convert_year_month_to_string(pd.DataFrame({'_Category' : ['sales'], 'AC' : [35]}), wanted_headers=['Year', 'Month'], year_field=['Year'], month_field=['Month'], sort_dataframe_parameter="This is a string")


def test_convert_dataframe_scenario_columns_to_value():
    # Test 1 - good dataframe with string year values and integer and float values
    dataset = pd.DataFrame({'Year' : [2022.0, '2021', '2018', 2019],
                            'Month': ['02', 4, '07', 8.0],
                            'AC'   : [351, '332.6238', 317.8, 341],
                            'PY'   : ['203.47', '178', 195, 201.1],
                            'PL'   : ['223', '199', '215', '185']})
    expected = {'Year' : [2022.0, '2021', '2018', 2019],
                'Month': ['02', 4, '07', 8.0],
                'AC'   : [351.0, 332.6238, 317.8, 341.0],
                'PY'   : [203.47, 178.0, 195.0, 201.1],
                'PL'   : [223, 199, 215, 185]}
    wanted_headers = ['Year', 'Month']
    actual   = convert_dataframe_scenario_columns_to_value(dataset, ['AC', 'PY', 'PL'])
    actual   = actual.to_dict(orient='list')
    message  = "Test 1 - dataframe_convert_year_month_to_string returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 2 - string instead of dataframe
    with pytest.raises(TypeDataFrameError):
        convert_dataframe_scenario_columns_to_value(dataframe="This is a string", scenariolist=['AC', 'PL'])

    # Test 3 - string instead of list
    with pytest.raises(TypeError):
        convert_dataframe_scenario_columns_to_value(dataframe=pd.DataFrame(), scenariolist="This is a string")

    # Test 4 - list has more scenarios than available in dataframe
    with pytest.raises(ValueError):
        dataset = pd.DataFrame({'Year' : [2022.0, '2021', '2018', 2019],
                                'Month': ['02', 4, '07', 8.0],
                                'AC'   : [351, '332.6238', 317.8, 341],
                                'PY'   : ['203.47', '178', 195, 201.1],
                                'PL'   : ['223', '199', '215', '185']})
        convert_dataframe_scenario_columns_to_value(dataframe=dataset, scenariolist=['AC', 'PY', 'PL', 'FC'])


def test_get_default_scenarios():
    # Test 1 - base scenarios out of all scenarios
    scenarios = ['PY', 'PL', 'FC', 'AC']
    expected  = ['PL', 'PY']
    actual    = get_default_scenarios('base', scenarios)
    message   = "Test 1 - get_default_scenarios returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 2 - base scenarios out of a subset of scenarios
    scenarios = ['PY', 'FC', 'AC']
    expected  = ['FC', 'PY']
    actual    = get_default_scenarios('base', scenarios)
    message   = "Test 2 - get_default_scenarios returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 3 - base scenarios out of a subset of scenarios
    scenarios = ['PL', 'FC', 'AC']
    expected  = ['FC', 'PL']
    actual    = get_default_scenarios('base', scenarios)
    message   = "Test 3 - get_default_scenarios returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 4 - base scenarios out of a subset of scenarios
    scenarios = ['FC', 'AC']
    expected  = ['FC']
    actual    = get_default_scenarios('base', scenarios)
    message   = "Test 4 - get_default_scenarios returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 5 - compare scenarios out of all scenarios
    scenarios = ['PY', 'PL', 'FC', 'AC']
    expected  = ['AC']
    actual    = get_default_scenarios('compare', scenarios)
    message   = "Test 5 - get_default_scenarios returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 6 - float instead of string
    with pytest.raises(TypeStringError):
        get_default_scenarios(1.2, ['AC', 'PL'])

    # Test 7 - wrong value as string
    with pytest.raises(ValueError):
        get_default_scenarios('This is a string with wrong value', ['AC', 'PL'])

    # Test 8 - string instead of list
    with pytest.raises(TypeListError):
        get_default_scenarios('base', 'This is a string')


def test_check_scenario_translation():
    # Test 1 - One correct key, one other key
    translation = {'PY':'PP', 'ZZ':'AA'}
    expected    = {'PY':'PP', 'PL':'PL', 'AC':'AC', 'FC':'FC'}
    actual      = check_scenario_translation(standardscenarios={'PY':'PY', 'PL':'PL', 'AC':'AC', 'FC':'FC'}, translation=translation)
    message     = "Test 1 - check_scenario_translation returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 2 - No translation
    translation = None
    expected    = {'PY':'PY', 'PL':'PL', 'AC':'AC', 'FC':'FC'}
    actual      = check_scenario_translation(standardscenarios={'PY':'PY', 'PL':'PL', 'AC':'AC', 'FC':'FC'}, translation=translation)
    message     = "Test 2 - check_scenario_translation returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 3 - Complete translation, different order
    translation = {'AC':'WK', 'FC':'EAC', 'PY':'VJ', 'PL':'BUD'}
    expected    = {'PY':'VJ', 'PL':'BUD', 'AC':'WK', 'FC':'EAC'}
    actual      = check_scenario_translation(standardscenarios={'PY':'PY', 'PL':'PL', 'AC':'AC', 'FC':'FC'}, translation=translation)
    message     = "Test 3 - check_scenario_translation returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 4 - string instead of dictionary
    with pytest.raises(TypeDictionaryError):
        check_scenario_translation(standardscenarios="This is a string", translation={'AC':'AC'})

    # Test 5 - string instead of dictionary
    with pytest.raises(TypeDictionaryError):
        check_scenario_translation(standardscenarios={'PY':'PY', 'PL':'PL', 'AC':'AC', 'FC':'FC'}, translation="This is a string")


def test_footnote_figure():
    # Test 1 - No footnote
    expected = False
    actual   = footnote_figure(figure=None, x=None, y=None, footnote=None, footnote_size=None, footnote_fontsize=None, font=None, colors=None)
    message     = "Test 1 - footnote_figure returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 2 - footnote is float instead of string
    with pytest.raises(TypeStringError):
        footnote_figure(figure=None, x=None, y=None, footnote=3.14, footnote_size=None, footnote_fontsize=None, font=None, colors=None)

    # Test 3 - footnote_fontsize is text instead of dictionary
    with pytest.raises(TypeDictionaryError):
        footnote_figure(figure=None, x=None, y=None, footnote="Source: clean_business_chart", footnote_size=None, footnote_fontsize="This is a text", font=None, colors=None)

    # Test 4 - footnote_size is integer instead of text
    with pytest.raises(TypeStringError):
        footnote_fontsize = {'great': 10, 'super': 12}
        footnote_figure(figure=None, x=None, y=None, footnote="Source: clean_business_chart", footnote_size=12, footnote_fontsize=footnote_fontsize, font=None, colors=None)

    # Test 5 - footnote_size is text but has wrong value
    with pytest.raises(ValueError):
        footnote_fontsize = {'great': 10, 'super': 12}
        footnote_figure(figure=None, x=None, y=None, footnote="Source: clean_business_chart", footnote_size="big", footnote_fontsize=footnote_fontsize, font=None, colors=None)

    # Test 6 - figure is text instead of figure
    with pytest.raises(TypeFigureError):
        footnote_fontsize = {'great': 10, 'super': 12}
        footnote_figure(figure="This is a text", x=None, y=None, footnote="Source: clean_business_chart", footnote_size="great", footnote_fontsize=footnote_fontsize,
                        font=None, colors=None)

    # Test 7 - x is text instead of integer or float
    with pytest.raises(TypeNumberError):
        footnote_fontsize = {'great': 10, 'super': 12}
        figure1, _        = plt.subplots()
        footnote_figure(figure=figure1, x="This is a text", y=None, footnote="Source: clean_business_chart", footnote_size="great", footnote_fontsize=footnote_fontsize,
                        font=None, colors=None)
        plt.close(figure1)

    # Test 8 - y is text instead of integer or float
    with pytest.raises(TypeNumberError):
        footnote_fontsize = {'great': 10, 'super': 12}
        figure1, _        = plt.subplots()
        footnote_figure(figure=figure1, x=0, y="This is a text", footnote="Source: clean_business_chart", footnote_size="great", footnote_fontsize=footnote_fontsize,
                        font=None, colors=None)
        plt.close(figure1)

    # Test 9 - colors is text instead of dictionary
    with pytest.raises(TypeDictionaryError):
        footnote_fontsize = {'great': 10, 'super': 12}
        figure1, _        = plt.subplots()
        footnote_figure(figure=figure1, x=0, y=0.01, footnote="Source: clean_business_chart", footnote_size="great", footnote_fontsize=footnote_fontsize,
                        font=None, colors="This is a text")
        plt.close(figure1)

    # Test 10 - colors is dictionary but missing entry for 'text'
    with pytest.raises(ValueError):
        footnote_fontsize = {'great': 10, 'super': 12}
        figure1, _        = plt.subplots()
        colors            = {'black': '#000000'}
        footnote_figure(figure=figure1, x=0, y=0.01, footnote="Source: clean_business_chart", footnote_size="great", footnote_fontsize=footnote_fontsize,
                        font=None, colors=colors)
        plt.close(figure1)

    # Test 11 - font is integer instead of text
    with pytest.raises(TypeStringError):
        footnote_fontsize = {'great': 10, 'super': 12}
        figure1, _        = plt.subplots()
        colors            = {'text': '#000000'}
        footnote_figure(figure=figure1, x=0, y=0.01, footnote="Source: clean_business_chart", footnote_size="great", footnote_fontsize=footnote_fontsize,
                        font=15, colors=colors)
        plt.close(figure1)


def test_convert_to_native_python_type():
    # Test 1 - integer
    expected = 3
    actual = convert_to_native_python_type(3)
    message = "Test 1 - convert_to_native_python_type returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 2 - float
    expected = 3.14
    actual = convert_to_native_python_type(3.14)
    message = "Test 2 - convert_to_native_python_type returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 3 - pandas Series integer
    expected = 5
    actual = convert_to_native_python_type(pd.Series([5])[0])
    message = "Test 3 - convert_to_native_python_type returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 4 - pandas Series float
    expected = 6.28
    actual = convert_to_native_python_type(pd.Series([6.28])[0])
    message = "Test 4 - convert_to_native_python_type returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 5 - string
    expected = 0
    actual = convert_to_native_python_type("This is a string")
    message = "Test 5 - convert_to_native_python_type returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message


def test_plot_line_accross_axes():
    # Test 1 - plot a line accross 2 axes
    fig, (ax1, ax2) = plt.subplots(1, 2)
    plot_line_accross_axes(fig, ax1, 0, 0, ax2, 1, 1)
    artist = fig.artists[0]  #first artists object
    artist_path = artist.get_path()
    expected_len = 1
    expected_xyA = [0.125, 0.11]
    expected_xyB = [0.5125, 0.495]
    actual_len = len(fig.artists)
    actual_xyA = list(artist_path.vertices[0])
    actual_xyB = list(artist_path.vertices[1])
    ## Print the attributes of the artist object
    #if isinstance(artist, ConnectionPatch):
    #    path = artist.get_path()
    #    xyA, xyB = path.vertices[0], path.vertices[1]
    #    coords1, coords2 = artist.coords1, artist.coords2
    #    print(f"ConnectionPatch attributes:\n"
    #          f"  xyA: {xyA}\n"
    #          f"  xyB: {xyB}\n"
    #          f"  coords1: {coords1}\n"
    #          f"  coords2: {coords2}\n"
    #          f"  axesA: {artist.axesA}\n"
    #          f"  axesB: {artist.axesB}\n"
    #          f"  color: {artist.get_edgecolor()}")
    message_len = "Test 1a - plot_line_accross_axes returned {0} artists instead of {1}".format(actual_len, expected_len)
    assert actual_len == expected_len, message_len
    message_xyA = "Test 1b - plot_line_accross_axes returned {0} instead of {1}".format(actual_xyA, expected_xyA)
    assert len(actual_xyA) == len(expected_xyA) and all([pytest.approx(a) == pytest.approx(b) for a, b in zip(actual_xyA, expected_xyA)]), message_xyA
    message_xyB = "Test 1c - plot_line_accross_axes returned {0} instead of {1}".format(actual_xyB, expected_xyB)
    assert len(actual_xyB) == len(expected_xyB) and all([pytest.approx(a) == pytest.approx(b) for a, b in zip(actual_xyB, expected_xyB)]), message_xyB
    plt.close(fig)

    # Test 2 - no axbegin-object
    with pytest.raises(TypeAxesError):
        fig, (ax1, ax2) = plt.subplots(1, 2)
        plot_line_accross_axes(fig=fig, axbegin="This is a string", xbegin=0, ybegin=0, axend=ax2, xend=1, yend=1)
        plt.close(fig)

    # Test 3 - no axend-object
    with pytest.raises(TypeAxesError):
        fig, (ax1, ax2) = plt.subplots(1, 2)
        plot_line_accross_axes(fig=fig, axbegin=ax1, xbegin=0, ybegin=0, axend="This is a string", xend=1, yend=1)
        plt.close(fig)


def test_plot_line_within_ax():
    # Test 1 - plot a line within 1 ax-object
    fig, ax = plt.subplots()
    plot_line_within_ax(ax, 1, 2, 3, 4.5)
    line_object = ax.lines[0]  #first lines object
    expected_len = 1
    expected_xdata = [1, 3]
    expected_ydata = [2, 4.5]
    actual_len = len(ax.lines)
    actual_xdata = list(line_object.get_xdata())
    actual_ydata = list(line_object.get_ydata())
    ## Print the attributes of the Line2D object
    #for line in ax.lines:
    #    print(f"Line2D attributes:\n"
    #          f"  xdata: {line.get_xdata()}\n"
    #          f"  ydata: {line.get_ydata()}\n"
    #          f"  color: {line.get_color()}\n"
    #          f"  linewidth: {line.get_linewidth()}\n"
    #          f"  linestyle: {line.get_linestyle()}")
    message_len = "Test 1a - plot_line_within_ax returned {0} lines instead of {1}".format(actual_len, expected_len)
    assert actual_len == expected_len, message_len
    message_xdata = "Test 1b - plot_line_within_ax returned {0} instead of {1}".format(actual_xdata, expected_xdata)
    assert len(actual_xdata) == len(expected_xdata) and all([pytest.approx(a) == pytest.approx(b) for a, b in zip(actual_xdata, expected_xdata)]), message_xdata
    message_ydata = "Test 1c - plot_line_within_ax returned {0} instead of {1}".format(actual_ydata, expected_ydata)
    assert len(actual_ydata) == len(expected_ydata) and all([pytest.approx(a) == pytest.approx(b) for a, b in zip(actual_ydata, expected_ydata)]), message_ydata
    plt.close(fig)

    # Test 2 - no ax-object
    with pytest.raises(TypeAxesError):
        plot_line_within_ax(ax='This is a string', xbegin=1, ybegin=2, xend=3, yend=4.5)


def test_plot_endpoint():
    # Test 1 - plot an endpoint with default optional parameters
    fig, ax = plt.subplots()
    plot_endpoint(ax, 2, 5)
    expected = {0: [ [2], [5], '#FFFFFF', 1.5, 'o', 7],
                1: [ [2], [5], '#000000', 1.5, 'o', 3]}
    for i, line in enumerate(ax.lines):
        actual = [list(line.get_xdata()), list(line.get_ydata()), line.get_color(), 
                  line.get_linewidth(), line.get_marker(), line.get_markersize()]
        message = "Test 1.{0} - plot_endpoint returned {1} instead of {2}".format(i, actual, expected[i])
        assert actual == expected[i], message
    ## Print the attributes of the Line2D object
    #for line in ax.lines:
    #    print(f"Line2D attributes:\n"
    #          f"  xdata: {line.get_xdata()}\n"
    #          f"  ydata: {line.get_ydata()}\n"
    #          f"  color: {line.get_color()}\n"
    #          f"  linewidth: {line.get_linewidth()}\n"
    #          f"  marker: {line.get_marker()}\n"
    #          f"  markersize: {line.get_markersize()}")
    plt.close(fig)

    # Test 2 - no ax-object
    with pytest.raises(TypeAxesError):
        plot_endpoint(ax='This is a string', x=1, y=2)

    # Test 3 - x is a string
    with pytest.raises(TypeNumberError):
        fig, ax = plt.subplots()
        plot_endpoint(ax=ax, x='This is a string', y=2)
        plt.close(fig)

    # Test 4 - y is a string
    with pytest.raises(TypeNumberError):
        fig, ax = plt.subplots()
        plot_endpoint(ax=ax, x=1, y='This is a string')
        plt.close(fig)

    # Test 5 - endpointcolor is a string
    with pytest.raises(TypeError):
        fig, ax = plt.subplots()
        plot_endpoint(ax=ax, x=1, y=2, endpointcolor='This is a string')
        plt.close(fig)

    # Test 6 - endpointcolor is a too long list
    with pytest.raises(ValueError):
        fig, ax = plt.subplots()
        plot_endpoint(ax=ax, x=1, y=2, endpointcolor=['#000000', '#FFFFFF', '#0F0F0F'])
        plt.close(fig)

    # Test 7 - endpointcolor is a too short list
    with pytest.raises(ValueError):
        fig, ax = plt.subplots()
        plot_endpoint(ax=ax, x=1, y=2, endpointcolor=['#000000'])
        plt.close(fig)

    # Test 8 - markersize_outercircle is a string
    with pytest.raises(TypeNumberError):
        fig, ax = plt.subplots()
        plot_endpoint(ax=ax, x=1, y=2, markersize_outercircle='This is a string')
        plt.close(fig)

    # Test 9 - markersize_innercircle is a string 
    with pytest.raises(TypeNumberError):
        fig, ax = plt.subplots()
        plot_endpoint(ax=ax, x=1, y=2, markersize_innercircle='This is a string')
        plt.close(fig)

     # Test 10 - markersize_innercircle is a negative number
    with pytest.raises(ValueError):
        fig, ax = plt.subplots()
        plot_endpoint(ax=ax, x=1, y=2, markersize_innercircle=-1)
        plt.close(fig)

    # Test 11 - markersize_outercircle <= markersize_innercircle
    with pytest.raises(ValueError):
        fig, ax = plt.subplots()
        plot_endpoint(ax=ax, x=1, y=2, markersize_outercircle=5, markersize_innercircle=7)
        plt.close(fig)


def test_prepare_title():
    # Test 1 - Complete title
    title = {'Reporting_unit': 'Global Corporation',
             'Business_measure': 'Net profit',
             'Unit': 'CHF',
             'Time': '2022: AC Jan..Aug, FC Sep..Dec'}
    expected    = 'Global Corporation\n$\\bf{Net\\ profit}$ in mCHF\n2022: AC Jan..Aug, FC Sep..Dec'
    actual      = prepare_title(title=title, multiplier='m')
    message     = "Test 1a - prepare_title returned {0} instead of {1}".format(repr(actual), repr(expected))
    assert actual == expected, message
    if not actual is None:
        if len(actual) > 0:
            assert actual[-1:] != '\n', "Test 1b - prepare_title ended with a newline"

    # Test 2 - No title
    title         = None
    expected      = None
    actual        = prepare_title(title=title, multiplier='m')
    message       = "Test 2 - prepare_title returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 3 - multiplier is None
    title = {'Reporting_unit'  : 'ACME',
             'Business_measure': 'Cost of goods sold',
             'Unit': 'USD',
             'Time': '2023'}
    expected    = 'ACME\n$\\bf{Cost\\ of\\ goods\\ sold}$ in USD\n2023'
    actual      = prepare_title(title=title, multiplier=None)
    message     = "Test 3 - prepare_title returned {0} instead of {1}".format(repr(actual), repr(expected))
    assert actual == expected, message

    # Test 4 - multiplier is '1'
    title = {'Reporting_unit'  : 'ACME',
             'Business_measure': 'Cost of goods sold',
             'Unit': 'EUR',
             'Time': '2023'}
    expected    = 'ACME\n$\\bf{Cost\\ of\\ goods\\ sold}$ in EUR\n2023'
    actual      = prepare_title(title=title, multiplier='1')
    message     = "Test 4 - prepare_title returned {0} instead of {1}".format(repr(actual), repr(expected))
    assert actual == expected, message

    # Test 5 - multiplier is ''
    title = {'Reporting_unit'  : 'ACME',
             'Business_measure': 'Cost of goods sold',
             'Unit': 'USD',
             'Time': '2024'}
    expected    = 'ACME\n$\\bf{Cost\\ of\\ goods\\ sold}$ in USD\n2024'
    actual      = prepare_title(title=title, multiplier='')
    message     = "Test 5 - prepare_title returned {0} instead of {1}".format(repr(actual), repr(expected))
    assert actual == expected, message

