"""test ColumnWithWaterfall-module"""

from clean_business_chart.columnchartwithwaterfall import *
import pandas as pd
from pandas import Timestamp                                # Needed in test__dataframe_date_to_year_and_month()
import io                                                   # Needed in test_ColumnWithWaterfall()
import hashlib                                              # Needed in test_ColumnWithWaterfall()
import requests                                             # Needed in test_ColumnWithWaterfall()
import pytest
        

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
    with pytest.raises(TypeError):
        testvar = ColumnWithWaterfall(test=True)
        testvar._dataframe_aggregate("This is a string")

    # Test 3 - a dataframe with missing column
    with pytest.raises(ValueError):
        dataset = pd.DataFrame({'Year' : ['2022', '2021'], 
                                'AC': [35, 33]})
        testvar  = ColumnWithWaterfall(test=True)
        actual   = testvar._dataframe_aggregate(dataset)


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
    with pytest.raises(TypeError):
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
        actual   = testvar._dataframe_full_year(dataset)


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
    with pytest.raises(TypeError):
        testvar = ColumnWithWaterfall(test=True)
        testvar._dataframe_handle_previous_year("This is a string")


def test__dataframe_to_dictionary():
    # Test 1 - good dataframe with one complete year of information
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
    with pytest.raises(TypeError):
        testvar = ColumnWithWaterfall(test=True)
        testvar._dataframe_to_dictionary("This is a string")


def test_ColumnWithWaterfall():
    # Test columnchart_001
    dataset =  {'PY'  : [14, 16, 14, 17, 19, 17, 19, 22, 16, 17, 16, 22],
                'PL'  : [11, 10, 10, 10, 10, 10, 15, 14, 15, 15, 15, 19],
                'AC'  : [15, 13, 16,  7,  5,  6, 17, 11],
                'FC'  : [ 0,  0,  0,  0,  0,  0,  0,  0, 26, 22, 13, 29],
                'Year': 2021}
    title_dict = dict()
    title_dict['Reporting_unit']   = 'ACME inc.'          # Name of the company or the department
    title_dict['Business_measure'] = 'Net sales'          # Name of the business measure
    title_dict['Unit']             = 'USD'                # Unit: USD or EUR (monetary) or # (count)
    title_dict['Time']             = '2021'               # More specific information about the time selection
    buf = io.BytesIO()                                    # Declare a buffer to put the chart-output in
    testchart = ColumnWithWaterfall(data=dataset, preferred_base_scenario='PL', title=title_dict, 
                                 multiplier='m', force_zero_decimals=True,
                                 filename=buf, do_not_show=True)
    buf.seek(0)
    sha256_hash = hashlib.sha256()                        # Initialize sha256
    for byte_block in iter(lambda: buf.read(4096),b""):
        sha256_hash.update(byte_block)
    actual=sha256_hash.hexdigest()
    buf.close()
    url = "https://raw.githubusercontent.com/MarcelW1323/clean_business_chart/main/test_charts/columnchart_001.png"
    sha256_hash = hashlib.sha256()                        # Initialize sha256
    response = requests.get(url)
    sha256_hash.update(response.content)
    expected=sha256_hash.hexdigest()
    message  = "Test columnchart_001.png - ColumnWithWaterfall returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message