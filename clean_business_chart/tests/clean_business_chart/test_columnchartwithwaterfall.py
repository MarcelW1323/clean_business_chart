"""test ColumnWithWaterfall-module"""

from clean_business_chart.columnchartwithwaterfall import *
import pandas as pd
from pandas import Timestamp  # Needed in test__dataframe_date_to_year_and_month()
import pytest
        
def test__convert_data_string_to_dataframe():
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
    testvar  = ColumnWithWaterfall(test=True)
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
    actual   = testvar._convert_data_string_to_dataframe(dataset)
    actual   = actual.to_dict()
    message  = "Test 1 - ColumnWithWaterfall._convert_data_string_to_dataframe returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 2 - only string supported
    with pytest.raises(ValueError):
        testvar = ColumnWithWaterfall(test=True)
        testvar._convert_data_string_to_dataframe(1.2)


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


def test__dataframe_date_to_year_and_month():
    # Test 1 - good dataframe with date, but without year and month
    dataset = pd.DataFrame({'Date' : ['20220101', '2022-02-21', '2022-03-01', '2022-04-01', '2022-05-01', '20220628', '2022-07-25', '2022-08-05', '20220916',
                                      '20221015', '2022-11-12', '2022-12-23'], 
                            'PY': [32, 38, 29, 35, 41, 37, 33, 38, 42, 44, 39, 31], 
                            'PL': [33, 35, 37, 40, 38, 36, 35, 40, 45.0328, 50.8, 45, 40], 
                            'AC': [35, 33, 41, 41, 37, 37, 0, 0, 0, 0, 0, 0],
                            'FC': [0, 0, 0, 0, 0, 0, 38, 44, 46, 48, 44, 44]})
    testvar  = ColumnWithWaterfall(test=True)
    expected = {'Date': {0: Timestamp('2022-01-01 00:00:00'), 1: Timestamp('2022-02-21 00:00:00'), 2: Timestamp('2022-03-01 00:00:00'), 
                         3: Timestamp('2022-04-01 00:00:00'), 4: Timestamp('2022-05-01 00:00:00'), 5: Timestamp('2022-06-28 00:00:00'), 
                         6: Timestamp('2022-07-25 00:00:00'), 7: Timestamp('2022-08-05 00:00:00'), 8: Timestamp('2022-09-16 00:00:00'), 
                         9: Timestamp('2022-10-15 00:00:00'), 10: Timestamp('2022-11-12 00:00:00'), 11: Timestamp('2022-12-23 00:00:00')}, 
                'PY': {0: 32, 1: 38, 2: 29, 3: 35, 4: 41, 5: 37, 6: 33, 7: 38, 8: 42, 9: 44, 10: 39, 11: 31}, 
                'PL': {0: 33.0, 1: 35.0, 2: 37.0, 3: 40.0, 4: 38.0, 5: 36.0, 6: 35.0, 7: 40.0, 8: 45.0328, 9: 50.8, 10: 45.0, 11: 40.0}, 
                'AC': {0: 35, 1: 33, 2: 41, 3: 41, 4: 37, 5: 37, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0}, 
                'FC': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 38, 7: 44, 8: 46, 9: 48, 10: 44, 11: 44}, 
                'Year': {0: 2022, 1: 2022, 2: 2022, 3: 2022, 4: 2022, 5: 2022, 6: 2022, 7: 2022, 8: 2022, 9: 2022, 10: 2022, 11: 2022}, 
                'Month': {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10, 10: 11, 11: 12}} 
    actual   = testvar._dataframe_date_to_year_and_month(dataset)
    actual   = actual.to_dict()
    message  = "Test 1 - ColumnWithWaterfall._dataframe_date_to_year_and_month returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 2 - good dataframe with date and year and month
    # Note: There is NO TESTING in the productive function if the year and month out of the date are equal to the 'Year' and 'Month' columns provided.
    #       The columns 'Year' and 'Month' are overwritten.
    dataset = pd.DataFrame({'Date' : ['20220101', '2022-02-21', '2022-03-01', '2022-04-01', '2022-05-01', '20220628', '2022-07-25', '2022-08-05', '20220916',
                                      '20221015', '2022-11-12', '2022-12-23'], 
                            'Year' : [2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022], 
                            'Month': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                            'PY': [32, 38, 29, 35, 41, 37, 33, 38, 42, 44, 39, 31], 
                            'PL': [33, 35, 37, 40, 38, 36, 35, 40, 45.0328, 50.8, 45, 40], 
                            'AC': [35, 33, 41, 41, 37, 37, 0, 0, 0, 0, 0, 0],
                            'FC': [0, 0, 0, 0, 0, 0, 38, 44, 46, 48, 44, 44]})
    testvar  = ColumnWithWaterfall(test=True)
    expected = {'Date': {0: Timestamp('2022-01-01 00:00:00'), 1: Timestamp('2022-02-21 00:00:00'), 2: Timestamp('2022-03-01 00:00:00'), 
                         3: Timestamp('2022-04-01 00:00:00'), 4: Timestamp('2022-05-01 00:00:00'), 5: Timestamp('2022-06-28 00:00:00'), 
                         6: Timestamp('2022-07-25 00:00:00'), 7: Timestamp('2022-08-05 00:00:00'), 8: Timestamp('2022-09-16 00:00:00'), 
                         9: Timestamp('2022-10-15 00:00:00'), 10: Timestamp('2022-11-12 00:00:00'), 11: Timestamp('2022-12-23 00:00:00')}, 
                'Year': {0: 2022, 1: 2022, 2: 2022, 3: 2022, 4: 2022, 5: 2022, 6: 2022, 7: 2022, 8: 2022, 9: 2022, 10: 2022, 11: 2022}, 
                'Month': {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10, 10: 11, 11: 12}, 
                'PY': {0: 32, 1: 38, 2: 29, 3: 35, 4: 41, 5: 37, 6: 33, 7: 38, 8: 42, 9: 44, 10: 39, 11: 31}, 
                'PL': {0: 33.0, 1: 35.0, 2: 37.0, 3: 40.0, 4: 38.0, 5: 36.0, 6: 35.0, 7: 40.0, 8: 45.0328, 9: 50.8, 10: 45.0, 11: 40.0}, 
                'AC': {0: 35, 1: 33, 2: 41, 3: 41, 4: 37, 5: 37, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0}, 
                'FC': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 38, 7: 44, 8: 46, 9: 48, 10: 44, 11: 44}} 
    actual   = testvar._dataframe_date_to_year_and_month(dataset)
    actual   = actual.to_dict()
    message  = "Test 2 - ColumnWithWaterfall._dataframe_date_to_year_and_month returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 3 - only dataframe supported
    with pytest.raises(ValueError):
        testvar = ColumnWithWaterfall(test=True)
        testvar._dataframe_date_to_year_and_month("This is a string")

    
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

    # Test 2 - only dataframe supported
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

    # Test 2 - only dataframe supported
    with pytest.raises(ValueError):
        testvar = ColumnWithWaterfall(test=True)
        testvar._dataframe_aggregate("This is a string")

    # Test 3 - a dataframe with missing column
    with pytest.raises(ValueError):
        dataset = pd.DataFrame({'Year' : ['2022', '2021'], 
                                'AC': [35, 33]})
        testvar  = ColumnWithWaterfall(test=True)
        actual   = testvar._dataframe_convert_year_month_to_string(dataset)


def test__dataframe_full_year():
    # Test 1 - good dataframe with missing month entries from one year
    dataset = pd.DataFrame({'Year' : ['2022', '2022', '2022', '2022'], 
                            'Month': ['02', '04', '07', '08'],
                            'PY'   : [32, 38, 12, 29], 
                            'PL'   : [33, 35, 15, 37], 
                            'AC'   : [35, 33, 17, 41],
                            'FC'   : [ 0,  0,  0,  0]})
    testvar  = ColumnWithWaterfall(test=True)
    expected = {'Year': {0: '2022', 1: '2022', 2: '2022', 3: '2022', 4: '2022', 5: '2022', 6: '2022', 7: '2022', 8: '2022', 9: '2022', 10: '2022', 11: '2022'}, 
                'Month': {0: '01', 1: '02', 2: '03', 3: '04', 4: '05', 5: '06', 6: '07', 7: '08', 8: '09', 9: '10', 10: '11', 11: '12'}, 
                'PY': {0: 0.0, 1: 32.0, 2: 0.0, 3: 38.0, 4: 0.0, 5: 0.0, 6: 12.0, 7: 29.0, 8: 0.0, 9: 0.0, 10: 0.0, 11: 0.0}, 
                'PL': {0: 0.0, 1: 33.0, 2: 0.0, 3: 35.0, 4: 0.0, 5: 0.0, 6: 15.0, 7: 37.0, 8: 0.0, 9: 0.0, 10: 0.0, 11: 0.0}, 
                'AC': {0: 0.0, 1: 35.0, 2: 0.0, 3: 33.0, 4: 0.0, 5: 0.0, 6: 17.0, 7: 41.0, 8: 0.0, 9: 0.0, 10: 0.0, 11: 0.0}, 
                'FC': {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 0.0, 6: 0.0, 7: 0.0, 8: 0.0, 9: 0.0, 10: 0.0, 11: 0.0}}
    actual   = testvar._dataframe_full_year(dataset)
    actual   = actual.to_dict()
    message  = "Test 1 - ColumnWithWaterfall._dataframe_full_year returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 2 - good empty dataframe with year and month columns
    dataset = pd.DataFrame({'Year' : [], 
                            'Month': [],
                            'AC'   : []})
    testvar  = ColumnWithWaterfall(test=True)
    expected = {'Year': {}, 'Month': {}, 'AC': {}}
    actual   = testvar._dataframe_full_year(dataset)
    actual   = actual.to_dict()
    message  = "Test 2 - ColumnWithWaterfall._dataframe_full_year returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 3 - only dataframe supported
    with pytest.raises(ValueError):
        testvar = ColumnWithWaterfall(test=True)
        testvar._dataframe_full_year("This is a string")

    # Test 4 - a dataframe with more than one year
    with pytest.raises(ValueError):
        dataset = pd.DataFrame({'Year' : ['2022', '2021'], 
                                'Month': ['01', '02'],
                                'AC': [35, 33]})
        testvar  = ColumnWithWaterfall(test=True)
        actual   = testvar._dataframe_full_year(dataset)

    # Test 5 - a dataframe with missing column
    with pytest.raises(ValueError):
        dataset = pd.DataFrame({'Year' : ['2022', '2022'], 
                                'AC': [35, 33]})
        testvar  = ColumnWithWaterfall(test=True)
        actual   = testvar._dataframe_convert_year_month_to_string(dataset)


def test__dataframe_convert_year_month_to_string():
    # Test 1 - good dataframe with string year values and integer and float values
    dataset = pd.DataFrame({'Year' : [2022.0, '2021', '2018', 2019], 
                            'Month': ['02', 4, '07', 8.0],
                            'AC'   : [35, 33, 17, 41]})
    testvar  = ColumnWithWaterfall(test=True)
    expected = {'Year': {2: '2018', 3: '2019', 1: '2021', 0: '2022'}, 
                'Month': {2: '07', 3: '08', 1: '04', 0: '02'}, 
                'AC': {2: 17, 3: 41, 1: 33, 0: 35}}
    actual   = testvar._dataframe_convert_year_month_to_string(dataset)
    actual   = actual.to_dict()
    message  = "Test 1 - ColumnWithWaterfall._dataframe_convert_year_month_to_string returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 2 - only dataframe supported
    with pytest.raises(ValueError):
        testvar = ColumnWithWaterfall(test=True)
        testvar._dataframe_convert_year_month_to_string("This is a string")

    # Test 3 - a dataframe with missing column
    with pytest.raises(ValueError):
        dataset = pd.DataFrame({'Year' : ['2022', '2021'], 
                                'AC': [35, 33]})
        testvar  = ColumnWithWaterfall(test=True)
        actual   = testvar._dataframe_convert_year_month_to_string(dataset)


def test__dataframe_translate_field_headers():
    # Test 1 - good dataframe with column names to be translated
    dataset = pd.DataFrame({'Invoicedate' : [1, 2, 3], 
                            'Revenue'     : [4, 5, 6],
                            'Budget'      : [7, 8, 9]})
    translate_headers = {'Invoicedate':'Date', 'Revenue':'AC', 'Budget':'PL'}
    testvar  = ColumnWithWaterfall(test=True)
    testvar.translate_headers=translate_headers
    expected = {'Date': {0: 1, 1: 2, 2: 3}, 
                'AC': {0: 4, 1: 5, 2: 6}, 
                'PL': {0: 7, 1: 8, 2: 9}}
    actual   = testvar._dataframe_translate_field_headers(dataset)
    actual   = actual.to_dict()
    message  = "Test 1 - ColumnWithWaterfall._dataframe_translate_field_headers returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 2 - only dataframe supported
    with pytest.raises(ValueError):
        testvar = ColumnWithWaterfall(test=True)
        testvar._dataframe_translate_field_headers("This is a string")

    # Test 3 - a dataframe with missing column
    with pytest.raises(ValueError):
        dataset = pd.DataFrame({'Invoicedate' : [1, 2, 3], 
                                'Revenue'     : [4, 5, 6],
                                'Budget'      : [7, 8, 9]})
        testvar  = ColumnWithWaterfall(test=True)
        testvar.translate_headers=['list item 1', 'list item 2']
        actual   = testvar._dataframe_translate_field_headers(dataset)


def test__convert_data_list_of_lists_to_dataframe():
    # Test 1 - good list of lists 
    dataset = [['Year', 'Month', 'AC', 'PL', 'FC'], [2022, 1, 35, 33, 0], [2022, 2, 38, 40, 0], [2022, 3, 29, 35, 0]]
    testvar  = ColumnWithWaterfall(test=True)
    expected =  {'Year': {0: 2022, 1: 2022, 2: 2022}, 
                 'Month': {0: 1, 1: 2, 2: 3}, 
                 'AC': {0: 35, 1: 38, 2: 29}, 
                 'PL': {0: 33, 1: 40, 2: 35}, 
                 'FC': {0: 0, 1: 0, 2: 0}}
    actual   = testvar._convert_data_list_of_lists_to_dataframe(dataset)
    actual   = actual.to_dict()
    message  = "Test 1 - ColumnWithWaterfall._convert_data_list_of_lists_to_dataframe returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 2 - only list (of lists) supported
    with pytest.raises(ValueError):
        testvar = ColumnWithWaterfall(test=True)
        testvar._convert_data_list_of_lists_to_dataframe("This is a string")

    # Test 3 - only list (of lists) supported
    with pytest.raises(ValueError):
        dataset = [['Year', 'Month', 'AC', 'PL', 'FC'], [2022, 1, 35, 33, 0], "This element is a string", [2022, 3, 29, 35, 0]]
        testvar = ColumnWithWaterfall(test=True)
        testvar._convert_data_list_of_lists_to_dataframe(dataset)


def test__dataframe_handle_previous_year():
    # Test 1 - good dataframe with two years of information and actual of previous year matches previous year of highest year
    dataset = pd.DataFrame({'Year' : ['2021', '2021', '2021', '2021']+['2022', '2022', '2022', '2022'], 
                            'Month': ['02', '04', '07', '08']+['02', '04', '07', '08'],
                            'PY'   : [32, 38, 12, 29]+[35, 33, 17, 41], 
                            'AC'   : [35, 33, 17, 41]+[37, 36, 25, 38]})
    testvar  = ColumnWithWaterfall(test=True)
    expected =  {'Year': {0: '2022', 1: '2022', 2: '2022', 3: '2022', 4: '2022', 5: '2022', 6: '2022', 7: '2022', 8: '2022', 9: '2022', 10: '2022', 11: '2022'}, 
                 'Month': {0: '01', 1: '02', 2: '03', 3: '04', 4: '05', 5: '06', 6: '07', 7: '08', 8: '09', 9: '10', 10: '11', 11: '12'}, 
                 'PY': {0: 0.0, 1: 35.0, 2: 0.0, 3: 33.0, 4: 0.0, 5: 0.0, 6: 17.0, 7: 41.0, 8: 0.0, 9: 0.0, 10: 0.0, 11: 0.0}, 
                 'AC': {0: 0.0, 1: 37.0, 2: 0.0, 3: 36.0, 4: 0.0, 5: 0.0, 6: 25.0, 7: 38.0, 8: 0.0, 9: 0.0, 10: 0.0, 11: 0.0}}
    actual   = testvar._dataframe_handle_previous_year(dataset)
    actual   = actual.to_dict()
    message  = "Test 1 - ColumnWithWaterfall._dataframe_handle_previous_year returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 2 - good dataframe with one year of information
    dataset = pd.DataFrame({'Year' : ['2022', '2022', '2022', '2022'], 
                            'Month': ['02', '04', '07', '08'],
                            'PY'   : [32, 38, 12, 29], 
                            'AC'   : [35, 33, 17, 41]})
    testvar  = ColumnWithWaterfall(test=True)
    expected = {'Year': {0: '2022', 1: '2022', 2: '2022', 3: '2022', 4: '2022', 5: '2022', 6: '2022', 7: '2022', 8: '2022', 9: '2022', 10: '2022', 11: '2022'}, 
                'Month': {0: '01', 1: '02', 2: '03', 3: '04', 4: '05', 5: '06', 6: '07', 7: '08', 8: '09', 9: '10', 10: '11', 11: '12'}, 
                'PY': {0: 0.0, 1: 32.0, 2: 0.0, 3: 38.0, 4: 0.0, 5: 0.0, 6: 12.0, 7: 29.0, 8: 0.0, 9: 0.0, 10: 0.0, 11: 0.0}, 
                'AC': {0: 0.0, 1: 35.0, 2: 0.0, 3: 33.0, 4: 0.0, 5: 0.0, 6: 17.0, 7: 41.0, 8: 0.0, 9: 0.0, 10: 0.0, 11: 0.0}}
    actual   = testvar._dataframe_handle_previous_year(dataset)
    actual   = actual.to_dict()
    message  = "Test 2 - ColumnWithWaterfall._dataframe_handle_previous_year returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 3 - good dataframe with two years of information and actual of previous year does not match previous year of highest year
    with pytest.raises(ValueError):
        dataset = pd.DataFrame({'Year' : ['2021', '2021', '2021', '2021']+['2022', '2022', '2022', '2022'], 
                                'Month': ['02', '04', '07', '08']+['02', '04', '07', '08'],
                                'PY'   : [32, 38, 12, 29]+[135, 233, 317, 441], 
                                'AC'   : [35, 33, 17, 41]+[37, 36, 25, 38]})
        testvar = ColumnWithWaterfall(test=True)
        testvar._dataframe_handle_previous_year(dataset)

    # Test 4 - good dataframe missing the year column
    with pytest.raises(ValueError):
        dataset = pd.DataFrame({'Month': ['02', '04', '07', '08'],
                                'PY'   : [32, 38, 12, 29], 
                                'AC'   : [35, 33, 17, 41]})
        testvar = ColumnWithWaterfall(test=True)
        testvar._dataframe_handle_previous_year(dataset)

    # Test 5 - only dataframe supported
    with pytest.raises(ValueError):
        testvar = ColumnWithWaterfall(test=True)
        testvar._dataframe_handle_previous_year("This is a string")


def test__dataframe_to_dictionary():
    # Test 1 - good dataframe with one complete years of information
    dataset = pd.DataFrame({'Year' : ['2022', '2022', '2022', '2022', '2022', '2022', '2022', '2022', '2022', '2022', '2022', '2022'], 
                            'Month': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'],
                            'PY'   : [35, 33, 17, 41, 25, 32, 28, 34, 27, 24, 37, 36], 
                            'AC'   : [37, 36, 25, 38, 28, 27, 34, 33, 29, 26, 38, 39]})
    testvar  = ColumnWithWaterfall(test=True)
    expected =  {'Year': '2022', 
                 'PY': [35, 33, 17, 41, 25, 32, 28, 34, 27, 24, 37, 36], 
                 'AC': [37, 36, 25, 38, 28, 27, 34, 33, 29, 26, 38, 39]}
    actual   = testvar._dataframe_to_dictionary(dataset)
    message  = "Test 1 - ColumnWithWaterfall._dataframe_to_dictionary returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 2 - good dataframe with four months of one year of information
    dataset = pd.DataFrame({'Year' : ['2022', '2022', '2022', '2022'], 
                            'Month': ['02', '04', '07', '08'],
                            'PY'   : [32, 38, 12, 29], 
                            'AC'   : [35, 33, 17, 41]})
    testvar  = ColumnWithWaterfall(test=True)
    expected =  {'Year': '2022', 'PY': [32, 38, 12, 29], 'AC': [35, 33, 17, 41]}
    actual   = testvar._dataframe_to_dictionary(dataset)
    message  = "Test 2 - ColumnWithWaterfall._dataframe_to_dictionary returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 3 - good dataframe with four months of one year of information and with string values in scenarios
    dataset = pd.DataFrame({'Year' : ['2022', '2022', '2022', '2022'], 
                            'Month': ['02', '04', '07', '08'],
                            'PY'   : [32, '38', 12, 29], 
                            'AC'   : [35, 33, '17', 41]})
    testvar  = ColumnWithWaterfall(test=True)
    expected =  {'Year': '2022', 'PY': [32, 38, 12, 29], 'AC': [35, 33, 17, 41]}
    actual   = testvar._dataframe_to_dictionary(dataset)
    message  = "Test 3 - ColumnWithWaterfall._dataframe_to_dictionary returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message


    # Test 4 - good dataframe missing the year column
    with pytest.raises(ValueError):
        dataset = pd.DataFrame({'Month': ['02', '04', '07', '08'],
                                'PY'   : [32, 38, 12, 29], 
                                'AC'   : [35, 33, 17, 41]})
        testvar = ColumnWithWaterfall(test=True)
        testvar._dataframe_to_dictionary(dataset)

    # Test 5 - only dataframe supported
    with pytest.raises(ValueError):
        testvar = ColumnWithWaterfall(test=True)
        testvar._dataframe_to_dictionary("This is a string")