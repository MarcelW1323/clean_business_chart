"""test ColumnWithWaterfall-module"""

from clean_business_chart.columnchartwithwaterfall import *
import pandas as pd
import pytest
        
def test__convert_data_string_to_list_of_lists():
    # Test 1 - good string to list_of_lists conversion 
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
    testvar  = ColumnWithWaterfall(test=True)
    expected = [['Year', 'Month', 'PL', 'AC', 'FC', 'PY'], ['2021', '1', '0', '32', '0', '0'], ['2021', '5', '0', '41', '0', '0'], 
                ['2021', '6', '0', '37', '0', '0'], ['2021', '7', '0', '33', '0', '0'], ['2021', '2', '0', '38', '0', '0'], 
                ['2021', '3', '0', '29', '0', '0'], ['2021', '4', '0', '35', '0', '0'], ['2021', '8', '0', '38', '0', '0'], 
                ['2021', '9', '0', '42', '0', '0'], ['2021', '10', '0', '44', '0', '0'], ['2021', '11', '0', '39', '0', '0'], 
                ['2021', '12', '24', '31', '48', '0'], ['2020', '10', '0', '44', '0', '0'], ['2020', '11', '0', '39', '0', '0'], 
                ['2020', '12', '0', '31', '0', '0'], ['2022', '1', '33', '35', '0', '32'], ['2022', '2', '35', '33', '0', '38'], 
                ['2022', '3', '37', '41', '0', '29'], ['2022', '4', '40', '41', '0', '35'], ['2022', '5', '38', '37', '0', '41'], 
                ['2022', '6', '36', '37', '0', '37'], ['2022', '7', '35', '0', '38', '33'], ['2022', '8', '40', '0', '44', '38'], 
                ['2022', '9', '45.0328', '0', '46', '42'], ['2022', '10', '50.8000', '0', '48', '44'], ['2022', '11', '45', '0', '44', '39'], 
                ['2022', '12', '40', '0', '44', '31']]
    actual   = testvar._convert_data_string_to_list_of_lists(dataset)
    message  = "Test 1 - ColumnWithWaterfall._convert_data_string_to_list_of_lists returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 2 - only string supported
    with pytest.raises(ValueError):
        testvar = ColumnWithWaterfall(test=True)
        testvar._convert_data_string_to_list_of_lists(1.2)

def test___convert_data_list_of_lists_to_dict():
    # Test 1 - good list_of_lists to dictionary conversion 
    dataset  = [['Year', 'Month', 'PL', 'AC', 'FC', 'PY'], ['2021', '1', '0', '32', '0', '0'], ['2021', '5', '0', '41', '0', '0'], 
                ['2021', '6', '0', '37', '0', '0'], ['2021', '7', '0', '33', '0', '0'], ['2021', '2', '0', '38', '0', '0'], 
                ['2021', '3', '0', '29', '0', '0'], ['2021', '4', '0', '35', '0', '0'], ['2021', '8', '0', '38', '0', '0'], 
                ['2021', '9', '0', '42', '0', '0'], ['2021', '10', '0', '44', '0', '0'], ['2021', '11', '0', '39', '0', '0'], 
                ['2021', '12', '24', '31', '48', '0'], ['2020', '10', '0', '44', '0', '0'], ['2020', '11', '0', '39', '0', '0'], 
                ['2020', '12', '0', '31', '0', '0'], ['2022', '1', '33', '35', '0', '32'], ['2022', '2', '35', '33', '0', '38'], 
                ['2022', '3', '37', '41', '0', '29'], ['2022', '4', '40', '41', '0', '35'], ['2022', '5', '38', '37', '0', '41'], 
                ['2022', '6', '36', '37', '0', '37'], ['2022', '7', '35', '0', '38', '33'], ['2022', '8', '40', '0', '44', '38'], 
                ['2022', '9', '45.0328', '0', '46', '42'], ['2022', '10', '50.8000', '0', '48', '44'], ['2022', '11', '45', '0', '44', '39'], 
                ['2022', '12', '40', '0', '44', '31']]
    testvar  = ColumnWithWaterfall(test=True)
    expected = {'Year': 2022, 'PY': [32, 38, 29, 35, 41, 37, 33, 38, 42, 44, 39, 31], 'PL': [33, 35, 37, 40, 38, 36, 35, 40, 45.0328, 50.8, 45, 40], 
                'AC': [35, 33, 41, 41, 37, 37, 0, 0, 0, 0, 0, 0], 'FC': [0, 0, 0, 0, 0, 0, 38, 44, 46, 48, 44, 44]}
    actual   = testvar._convert_data_list_of_lists_to_dict(dataset)
    message  = "Test 1 - ColumnWithWaterfall._convert_data_list_of_lists_to_dict returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 2 - only string supported
    with pytest.raises(ValueError):
        testvar = ColumnWithWaterfall(test=True)
        testvar._convert_data_list_of_lists_to_dict("This is a string")

def test__dataframe_search_for_headers():
    # Test 1 - good dataframe, search for available headers and error when not found
    dataset = pd.DataFrame({'Year' : [2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022], 
                            'Month': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                            'PY': [32, 38, 29, 35, 41, 37, 33, 38, 42, 44, 39, 31], 
                            'PL': [33, 35, 37, 40, 38, 36, 35, 40, 45.0328, 50.8, 45, 40], 
                            'AC': [35, 33, 41, 41, 37, 37, 0, 0, 0, 0, 0, 0], 
                            'FC': [0, 0, 0, 0, 0, 0, 38, 44, 46, 48, 44, 44]})
    search_for_headers = ['Year', 'Month', 'PY', 'PL', 'AC', 'FC']
    error_not_found    = True
    testvar  = ColumnWithWaterfall(test=True)
    expected = search_for_headers
    actual   = testvar._dataframe_search_for_headers(dataframe=dataset, search_for_headers=search_for_headers, error_not_found=error_not_found)
    message  = "Test 1 - ColumnWithWaterfall._dataframe_search_for_headers returned {0} instead of {1}".format(actual, expected)
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
    testvar  = ColumnWithWaterfall(test=True)
    expected = ['AC']
    actual   = testvar._dataframe_search_for_headers(dataframe=dataset, search_for_headers=search_for_headers, error_not_found=error_not_found)
    message  = "Test 2 - ColumnWithWaterfall._dataframe_search_for_headers returned {0} instead of {1}".format(actual, expected)
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
        testvar = ColumnWithWaterfall(test=True)
        testvar._dataframe_search_for_headers(dataframe=dataset, search_for_headers=search_for_headers, error_not_found=error_not_found)

    # Test 4 - only DataFrame supported as first parameter
    with pytest.raises(ValueError):
        testvar = ColumnWithWaterfall(test=True)
        testvar._dataframe_search_for_headers(dataframe="This is a string", search_for_headers=list())

    # Test 5 - only list supported as second parameter
    with pytest.raises(ValueError):
        dataset = pd.DataFrame({'Year' : [2023]})
        testvar = ColumnWithWaterfall(test=True)
        testvar._dataframe_search_for_headers(dataframe=dataset, search_for_headers="This is a string")

    
def test__dataframe_keep_only_relevant_columns():
    # Test 1 - good dataframe with extra columns
    dataset = pd.DataFrame({'Year' : [2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022], 
                            'Month': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                            'PY': [32, 38, 29, 35, 41, 37, 33, 38, 42, 44, 39, 31], 
                            'PL': [33, 35, 37, 40, 38, 36, 35, 40, 45.0328, 50.8, 45, 40], 
                            'AC': [35, 33, 41, 41, 37, 37, 0, 0, 0, 0, 0, 0],
                            'AX': [10, 10, 10, 10, 10, 10, 10, 10, 10 ,10 ,10, 10],                            
                            'FC': [0, 0, 0, 0, 0, 0, 38, 44, 46, 48, 44, 44]})
    testvar  = ColumnWithWaterfall(test=True)
    expected = {'Year': {0: 2022, 1: 2022, 2: 2022, 3: 2022, 4: 2022, 5: 2022, 6: 2022, 7: 2022, 8: 2022, 9: 2022, 10: 2022, 11: 2022}, 
                'Month': {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10, 10: 11, 11: 12}, 
                'PY': {0: 32, 1: 38, 2: 29, 3: 35, 4: 41, 5: 37, 6: 33, 7: 38, 8: 42, 9: 44, 10: 39, 11: 31}, 
                'PL': {0: 33.0, 1: 35.0, 2: 37.0, 3: 40.0, 4: 38.0, 5: 36.0, 6: 35.0, 7: 40.0, 8: 45.0328, 9: 50.8, 10: 45.0, 11: 40.0}, 
                'AC': {0: 35, 1: 33, 2: 41, 3: 41, 4: 37, 5: 37, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0}, 
                'FC': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 38, 7: 44, 8: 46, 9: 48, 10: 44, 11: 44}}
    actual   = testvar._dataframe_keep_only_relevant_columns(dataset)
    actual   = actual.to_dict()
    message  = "Test 1 - ColumnWithWaterfall._dataframe_keep_only_relevant_columns returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 2 - only string supported
    with pytest.raises(ValueError):
        testvar = ColumnWithWaterfall(test=True)
        testvar._dataframe_keep_only_relevant_columns("This is a string")


def test__dataframe_aggregate():
    # Test 1 - good dataframe with extra month entries
    dataset = pd.DataFrame({'Year' : [2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022], 
                            'Month': [1, 2, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                            'PY': [32, 38, 12, 29, 35, 41, 37, 33, 38, 42, 44, 39, 31], 
                            'PL': [33, 35, 15, 37, 40, 38, 36, 35, 40, 45.0328, 50.8, 45, 40], 
                            'AC': [35, 33, 17, 41, 41, 37, 37, 0, 0, 0, 0, 0, 0],
                            'FC': [0, 0, 0, 0, 0, 0, 0, 38, 44, 46, 48, 44, 44]})
    testvar  = ColumnWithWaterfall(test=True)
    expected = {'Year': {0: 2022, 1: 2022, 2: 2022, 3: 2022, 4: 2022, 5: 2022, 6: 2022, 7: 2022, 8: 2022, 9: 2022, 10: 2022, 11: 2022}, 
                'Month': {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10, 10: 11, 11: 12}, 
                'PY': {0: 32, 1: 50, 2: 29, 3: 35, 4: 41, 5: 37, 6: 33, 7: 38, 8: 42, 9: 44, 10: 39, 11: 31}, 
                'PL': {0: 33.0, 1: 50.0, 2: 37.0, 3: 40.0, 4: 38.0, 5: 36.0, 6: 35.0, 7: 40.0, 8: 45.0328, 9: 50.8, 10: 45.0, 11: 40.0}, 
                'AC': {0: 35, 1: 50, 2: 41, 3: 41, 4: 37, 5: 37, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0}, 
                'FC': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 38, 7: 44, 8: 46, 9: 48, 10: 44, 11: 44}}
    actual   = testvar._dataframe_aggregate(dataset)
    actual   = actual.to_dict()
    message  = "Test 1 - ColumnWithWaterfall._dataframe_aggregate returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 2 - only string supported
    with pytest.raises(ValueError):
        testvar = ColumnWithWaterfall(test=True)
        testvar._dataframe_aggregate("This is a string")