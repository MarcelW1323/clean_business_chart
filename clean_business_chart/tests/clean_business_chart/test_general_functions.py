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

    # Test 7 - Optimizing with other numerator and denominator and decimals
    data     = 123456789
    expected = 370.37
    actual   = optimize_data(data=data, numerator=3, denominator=1000000, decimals=2)
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

    # Test 3 - list1 is not present
    with pytest.raises(ValueError):
        list2    = ['PY', 'AC', 'FC']
        filter_lists(list2=list2)

    # Test 4 - list2 is not present
    with pytest.raises(ValueError):
        list1    = ['PY', 'AC', 'FC']
        filter_lists(list1=list1)


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
    expected = {'Year': {0: '2021', 1: '2021', 2: '2021', 3: '2021', 4: '2021', 5: '2021', 6: '2021', 7: '2021', 8: '2021', 9: '2021', 
                         10: '2021', 11: '2021', 12: '2020', 13: '2020', 14: '2020', 15: '2022', 16: '2022', 17: '2022', 18: '2022', 19: '2022', 
                         20: '2022', 21: '2022', 22: '2022', 23: '2022', 24: '2022', 25: '2022', 26: '2022'}, 
                'Month': {0: '1', 1: '5', 2: '6', 3: '7', 4: '2', 5: '3', 6: '4', 7: '8', 8: '9', 9: '10',
                          10: '11', 11: '12', 12: '10', 13: '11', 14: '12', 15: '1', 16: '2', 17: '3', 18: '4', 19: '5', 
                          20: '6', 21: '7', 22: '8', 23: '9', 24: '10', 25: '11', 26: '12'}, 
                'PL': {0: '0', 1: '0', 2: '0', 3: '0', 4: '0', 5: '0', 6: '0', 7: '0', 8: '0', 9: '0', 
                       10: '0', 11: '24', 12: '0', 13: '0', 14: '0', 15: '33', 16: '35', 17: '37', 18: '40', 19: '38', 
                       20: '36', 21: '35', 22: '40', 23: '45.0328', 24: '50.8000', 25: '45', 26: '40'}, 
                'AC': {0: '32', 1: '41', 2: '37', 3: '33', 4: '38', 5: '29', 6: '35', 7: '38', 8: '42', 9: '44', 
                       10: '39', 11: '31', 12: '44', 13: '39', 14: '31', 15: '35', 16: '33', 17: '41', 18: '41', 19: '37', 
                       20: '37', 21: '0', 22: '0', 23: '0', 24: '0', 25: '0', 26: '0'}, 
                'FC': {0: '0', 1: '0', 2: '0', 3: '0', 4: '0', 5: '0', 6: '0', 7: '0', 8: '0', 9: '0', 
                       10: '0', 11: '48', 12: '0', 13: '0', 14: '0', 15: '0', 16: '0', 17: '0', 18: '0', 19: '0', 
                       20: '0', 21: '38', 22: '44', 23: '46', 24: '48', 25: '44', 26: '44'}, 
                'PY': {0: '0', 1: '0', 2: '0', 3: '0', 4: '0', 5: '0', 6: '0', 7: '0', 8: '0', 9: '0', 
                       10: '0', 11: '0', 12: '0', 13: '0', 14: '0', 15: '32', 16: '38', 17: '29', 18: '35', 19: '41', 
                       20: '37', 21: '33', 22: '38', 23: '42', 24: '44', 25: '39', 26: '31'}}
    actual   = convert_data_string_to_pandas_dataframe(dataset)
    actual   = actual.to_dict()
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
    expected =  {'Year': {0: 2022, 1: 2022, 2: 2022}, 
                 'Month': {0: 1, 1: 2, 2: 3}, 
                 'AC': {0: 35, 1: 38, 2: 29}, 
                 'PL': {0: 33, 1: 40, 2: 35}, 
                 'FC': {0: 0, 1: 0, 2: 0}}
    actual   = convert_data_list_of_lists_to_pandas_dataframe(dataset)
    actual   = actual.to_dict()
    message  = "Test 1 - convert_data_list_of_lists_to_pandas_dataframe returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 2 - only list (of lists) supported, we try it with a string
    with pytest.raises(TypeError):
        convert_data_list_of_lists_to_pandas_dataframe("This is a string")

    # Test 3 - only list (of lists) supported, we try it with a string element in a list
    with pytest.raises(TypeError):
        dataset = [['Year', 'Month', 'AC', 'PL', 'FC'], [2022, 1, 35, 33, 0], "This element is a string", [2022, 3, 29, 35, 0]]
        convert_data_list_of_lists_to_pandas_dataframe(dataset)


#### Need to add more test-functions for automatic testing
