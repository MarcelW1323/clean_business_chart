"""test BarWithWaterfall-module"""

from clean_business_chart.barchartwithwaterfall import *
import pandas as pd
from pandas import Timestamp                             # Needed in test__dataframe_date_to_year_and_month()
from clean_business_chart.multiplier import Multiplier   # Needed in test__optimize_data_calculate_denominator()
import io                                                # Needed in test_BarWithWaterfall()
import hashlib                                           # Needed in test_BarWithWaterfall()
import requests                                          # Needed in test_BarWithWaterfall()

import pytest

#### FIRST VERSION ONLY SUPPORTS 1 COMPARE SCENARIO in test__check_scenario_parameters()

def test__simple_first_check_scenario_parameters_one_variable():
    # Test 1 - all parameters are OK
    scenarios              = ['PY', 'PL']
    default_scenariolist   = ['PL', 'PY']
    technical_scenariolist = ['PY', 'PL', 'AC', 'FC']
    testvar  = BarWithWaterfall(test=True)
    expected = ['PY', 'PL']  # Same as the scenarios, because they are OK
    actual   = testvar._simple_first_check_scenario_parameters_one_variable(scenarios=scenarios, default_scenariolist=default_scenariolist, 
                                                                            technical_scenariolist=technical_scenariolist)
    message  = "Test 1 - BarWithWaterfall._simple_first_check_scenario_parameters_one_variable returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 2 - scenarios is None
    scenarios              = None
    default_scenariolist   = ['PL', 'PY']
    technical_scenariolist = ['PY', 'PL', 'AC', 'FC']
    testvar  = BarWithWaterfall(test=True)
    expected = ['PL', 'PY']  # Same as the default_scenariolist, because scenarios is None
    actual   = testvar._simple_first_check_scenario_parameters_one_variable(scenarios=scenarios, default_scenariolist=default_scenariolist, 
                                                                            technical_scenariolist=technical_scenariolist)
    message  = "Test 2 - BarWithWaterfall._simple_first_check_scenario_parameters_one_variable returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 3 - scenarios is string with one valid scenario
    scenarios              = 'FC'
    default_scenariolist   = ['PL', 'PY']
    technical_scenariolist = ['PY', 'PL', 'AC', 'FC']
    testvar  = BarWithWaterfall(test=True)
    expected = ['FC']
    actual   = testvar._simple_first_check_scenario_parameters_one_variable(scenarios=scenarios, default_scenariolist=default_scenariolist, 
                                                                            technical_scenariolist=technical_scenariolist)
    message  = "Test 3 - BarWithWaterfall._simple_first_check_scenario_parameters_one_variable returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 4 - default_scenariolist is integer (not a list)
    with pytest.raises(TypeListError):
        scenarios              = None
        default_scenariolist   = 15
        technical_scenariolist = ['PY', 'PL', 'AC', 'FC']
        testvar = BarWithWaterfall(test=True)
        testvar._simple_first_check_scenario_parameters_one_variable(scenarios=scenarios, default_scenariolist=default_scenariolist, 
                                                                     technical_scenariolist=technical_scenariolist)

    # Test 5 - technical_scenariolist is string (not a list)
    with pytest.raises(TypeListError):
        scenarios              = None
        default_scenariolist   = ['PL', 'PY']
        technical_scenariolist = 'I am a string'
        testvar = BarWithWaterfall(test=True)
        testvar._simple_first_check_scenario_parameters_one_variable(scenarios=scenarios, default_scenariolist=default_scenariolist, 
                                                                     technical_scenariolist=technical_scenariolist)

    # Test 6 - scenarios not in technical_scenariolist
    with pytest.raises(ValueError):
        scenarios              = ['ZZ', 'AA']
        default_scenariolist   = ['PL', 'PY']
        technical_scenariolist = ['PY', 'PL', 'AC', 'FC']
        testvar = BarWithWaterfall(test=True)
        testvar._simple_first_check_scenario_parameters_one_variable(scenarios=scenarios, default_scenariolist=default_scenariolist, 
                                                                     technical_scenariolist=technical_scenariolist)

    # Test 7 - empty scenarios, less than the minimum of one scenario
    with pytest.raises(ValueError):
        scenarios              = []
        default_scenariolist   = ['PL', 'PY']
        technical_scenariolist = ['PY', 'PL', 'AC', 'FC']
        testvar = BarWithWaterfall(test=True)
        testvar._simple_first_check_scenario_parameters_one_variable(scenarios=scenarios, default_scenariolist=default_scenariolist, 
                                                                     technical_scenariolist=technical_scenariolist)

    # Test 8 - more than the maximum of two scenarios
    with pytest.raises(ValueError):
        scenarios              = ['PL', 'PY', 'AC']
        default_scenariolist   = ['PL', 'PY']
        technical_scenariolist = ['PY', 'PL', 'AC', 'FC']
        testvar = BarWithWaterfall(test=True)
        testvar._simple_first_check_scenario_parameters_one_variable(scenarios=scenarios, default_scenariolist=default_scenariolist, 
                                                                     technical_scenariolist=technical_scenariolist)


def test_simple_first_check_scenario_parameters():
    # Test 1 - original_base_scenarios is None and original_compare_scenarios is None
    testvar  = BarWithWaterfall(test=True)
    testvar.original_base_scenarios = None
    testvar.original_compare_scenarios = None
    testvar.all_scenarios = ['PY', 'PL', 'AC', 'FC']
    expected1 = ['PL', 'PY']
    expected2 = ['AC', 'FC']
    testvar.simple_first_check_scenario_parameters()
    actual1 = testvar.base_scenarios
    actual2 = testvar.compare_scenarios
    message1  = "Test 1a - BarWithWaterfall.simple_first_check_scenario_parameters returned {0} instead of {1}".format(actual1, expected1)
    message2  = "Test 1b - BarWithWaterfall.simple_first_check_scenario_parameters returned {0} instead of {1}".format(actual2, expected2)
    assert actual1 == expected1, message1
    assert actual2 == expected2, message2

    # Test 2 - original_base_scenarios is PL and original_compare_scenarios is AC, both are stings with length two
    testvar  = BarWithWaterfall(test=True)
    testvar.original_base_scenarios = 'PL'
    testvar.original_compare_scenarios = 'AC'
    testvar.all_scenarios = ['PY', 'PL', 'AC', 'FC']
    expected1 = ['PL']
    expected2 = ['AC']
    testvar.simple_first_check_scenario_parameters()
    actual1 = testvar.base_scenarios
    actual2 = testvar.compare_scenarios
    message1  = "Test 2a - BarWithWaterfall.simple_first_check_scenario_parameters returned {0} instead of {1}".format(actual1, expected1)
    message2  = "Test 2b - BarWithWaterfall.simple_first_check_scenario_parameters returned {0} instead of {1}".format(actual2, expected2)
    assert actual1 == expected1, message1
    assert actual2 == expected2, message2

    # Test 3 - original_base_scenarios is ['PY'] and original_compare_scenarios is ['FC'], both are lists
    testvar  = BarWithWaterfall(test=True)
    testvar.original_base_scenarios = ['PY']
    testvar.original_compare_scenarios = ['FC']
    testvar.all_scenarios = ['PY', 'PL', 'AC', 'FC']
    expected1 = ['PY']
    expected2 = ['FC']
    testvar.simple_first_check_scenario_parameters()
    actual1 = testvar.base_scenarios
    actual2 = testvar.compare_scenarios
    message1  = "Test 3a - BarWithWaterfall.simple_first_check_scenario_parameters returned {0} instead of {1}".format(actual1, expected1)
    message2  = "Test 3b - BarWithWaterfall.simple_first_check_scenario_parameters returned {0} instead of {1}".format(actual2, expected2)
    assert actual1 == expected1, message1
    assert actual2 == expected2, message2

    # Test 4 - original_base_scenarios is ['FC', 'PL'] and original_compare_scenarios is ['AC', 'FC'], both are lists
    testvar  = BarWithWaterfall(test=True)
    testvar.original_base_scenarios = ['FC', 'PL']
    testvar.original_compare_scenarios = ['AC', 'FC']
    testvar.all_scenarios = ['PY', 'PL', 'AC', 'FC']
    expected1 = ['FC', 'PL']
    expected2 = ['AC', 'FC']
    testvar.simple_first_check_scenario_parameters()
    actual1 = testvar.base_scenarios
    actual2 = testvar.compare_scenarios
    message1  = "Test 4a - BarWithWaterfall.simple_first_check_scenario_parameters returned {0} instead of {1}".format(actual1, expected1)
    message2  = "Test 4b - BarWithWaterfall.simple_first_check_scenario_parameters returned {0} instead of {1}".format(actual2, expected2)
    assert actual1 == expected1, message1
    assert actual2 == expected2, message2

    # Test 5 - original_base_scenarios is 'AC, PY' and original_compare_scenarios is 'FC, PL', both are strings
    testvar  = BarWithWaterfall(test=True)
    testvar.original_base_scenarios = 'AC, PY'
    testvar.original_compare_scenarios = 'FC, PL'
    testvar.all_scenarios = ['PY', 'PL', 'AC', 'FC']
    expected1 = ['AC', 'PY']
    expected2 = ['FC', 'PL']
    testvar.simple_first_check_scenario_parameters()
    actual1 = testvar.base_scenarios
    actual2 = testvar.compare_scenarios
    message1  = "Test 5a - BarWithWaterfall.simple_first_check_scenario_parameters returned {0} instead of {1}".format(actual1, expected1)
    message2  = "Test 5b - BarWithWaterfall.simple_first_check_scenario_parameters returned {0} instead of {1}".format(actual2, expected2)
    assert actual1 == expected1, message1
    assert actual2 == expected2, message2

    # Test 6 - original_base_scenarios is ['FC', 'PL', 'AC'] and original_compare_scenarios is ['AC', 'FC'], both are lists but base is too long
    with pytest.raises(ValueError):
        testvar  = BarWithWaterfall(test=True)
        testvar.original_base_scenarios = ['FC', 'PL', 'AC']
        testvar.original_compare_scenarios = ['AC', 'FC']
        testvar.all_scenarios = ['PY', 'PL', 'AC', 'FC']
        testvar.simple_first_check_scenario_parameters()

    # Test 7 - original_base_scenarios is ['AA', 'PL'] and original_compare_scenarios is ['AC', 'FC'], both are lists but base has a not supported value
    with pytest.raises(ValueError):
        testvar  = BarWithWaterfall(test=True)
        testvar.original_base_scenarios = ['AA', 'PL']
        testvar.original_compare_scenarios = ['AC', 'FC']
        testvar.all_scenarios = ['PY', 'PL', 'AC', 'FC']
        testvar.simple_first_check_scenario_parameters()

    # Test 8 - original_base_scenarios is ['PY', 'PL'] and original_compare_scenarios is 1.2, compare is a float
    with pytest.raises(TypeError):
        testvar  = BarWithWaterfall(test=True)
        testvar.original_base_scenarios = ['PY', 'PL']
        testvar.original_compare_scenarios = 1.2
        testvar.all_scenarios = ['PY', 'PL', 'AC', 'FC']
        testvar.simple_first_check_scenario_parameters()


def test__check_scenario_parameters():
    # Test 1 - Test all good base_scenarios and compare_scenarios 
    testvar  = BarWithWaterfall(test=True)
    testvar.data_scenarios = ['PY', 'PL', 'AC', 'FC']
    scenarios = { ('PY', 'PL'): [ ['AC'], ['AC', 'FC'], ['AC', 'PL'], ['AC', 'PY'], ['FC'], ['PL'] ],
                  ('PL', 'FC'): [ ['AC'], ['AC', 'FC'], ['AC', 'PY'], ['AC', 'PL'], ['FC'] ],
                  ('FC', 'PY'): [ ['AC'], ['AC', 'FC'], ['AC', 'PY'], ['AC', 'PL'] ],
                  ('PY', )    : [ ['AC'], ['AC', 'FC'], ['AC', 'PL'], ['AC', 'PY'], ['FC'], ['PL'] ],
                  ('PL', )    : [ ['AC'], ['AC', 'FC'], ['AC', 'PY'], ['AC', 'PL'], ['FC'] ],
                  ('FC', )    : [ ['AC'], ['AC', 'FC'], ['AC', 'PY'], ['AC', 'PL'] ] }
    for base_scenarios in scenarios.keys():
        compare_scenarios = scenarios[base_scenarios]
        for element in compare_scenarios:
            if len(element) > 1 : continue    #### FIRST VERSION ONLY SUPPORTS 1 COMPARE SCENARIO
            testvar.base_scenarios = list(base_scenarios)
            testvar.compare_scenarios = element
            # If the function below doesn't give an error, it is good because all these tested scenarios are supported
            testvar._check_scenario_parameters()

    # Test 2 - Test bad combinations of values. 
    testvar  = BarWithWaterfall(test=True)
    testvar.data_scenarios = ['PY', 'PL', 'AC', 'FC']
    scenarios = { ('PY', 'PX'): [ ['AC'], ['AC', 'FC'], ['AC', 'PL'], ['AC', 'PY'], ['FC'], ['PL'] ],   # Key is bad
                  ('PX', 'FC'): [ ['AC'], ['AC', 'FC'], ['AC', 'PY'], ['AC', 'PL'], ['FC'] ],           # Key is bad
                  ('FC', 'PY'): [ ['AX'], ['AC', 'FX'], ['AX', 'PY'], ['AC', 'PX'] ],                   # Listvalues are bad
                  ('PX', )    : [ ['AC'], ['AC', 'FC'], ['AC', 'PL'], ['AC', 'PY'], ['FC'], ['PL'] ],   # Key is bad
                  ('PL', )    : [ ['XC'], ['AX', 'FC'], ['AC', 'PX'], ['AC', 'XL'], ['XC'] ],           # Listvalues are bad
                  ('XC', )    : [ ['AC'], ['AC', 'FC'], ['AC', 'PY'], ['AC', 'PL'] ] }                  # Key is bad
    for base_scenarios in scenarios.keys():
        compare_scenarios = scenarios[base_scenarios]
        for element in compare_scenarios:
            testvar.base_scenarios = list(base_scenarios)
            testvar.compare_scenarios = element
            # The function below shoud give an ValueError and that is exactly what it should do.
            with pytest.raises(ValueError):
                testvar._check_scenario_parameters()


def test__fill_data_scenarios():
    # Test 1 - good dataframe with all scenarios
    dataset  = pd.DataFrame({'Year' : ['2021', '2021'],
                             'Month': ['02', '04'],
                             'PY'   : [32, 38],
                             'PL'   : [32, 38],
                             'AC'   : [35, 33],
                             'FC'   : [32, 38]})
    testvar  = BarWithWaterfall(test=True)
    testvar.all_scenarios = ['PY', 'PL', 'AC', 'FC']
    expected = ['PY', 'PL', 'AC', 'FC']
    testvar._fill_data_scenarios(dataframe=dataset)
    actual   = testvar.data_scenarios
    message  = "Test 1 - BarWithWaterfall._fill_data_scenarios returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 2 - good dataframe with some scenarios
    dataset  = pd.DataFrame({'Year'     : ['2021', '2022'],
                             'AC'       : [32, 38],
                             'Month'    : ['02', '04'],
                             'Category' : ["Dog", "Cat"],
                             'PY'       : [32, 38]})
    testvar  = BarWithWaterfall(test=True)
    testvar.all_scenarios = ['PY', 'PL', 'AC', 'FC']
    expected = ['PY', 'AC']
    testvar._fill_data_scenarios(dataframe=dataset)
    actual   = testvar.data_scenarios
    message  = "Test 2 - BarWithWaterfall._fill_data_scenarios returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message
    
    # Test 3 - parameter is a string and not a dataframe
    with pytest.raises(TypeDataFrameError):
        testvar = BarWithWaterfall(test=True)
        testvar.all_scenarios = ['PY', 'PL', 'AC', 'FC']
        testvar._fill_data_scenarios(dataframe="This is a string")


def test__fill_data_total():
    # Test 1 - good dataframe with all scenarios. Decimals is 2
    dataset  = pd.DataFrame({'Year' : ['2021', '2022'],
                             'Month': ['02', '04'],
                             'PY'   : [32.453, 38.2],
                             'PL'   : [32.74532, 38.98899],
                             'AC'   : [35.3, 33],
                             'FC'   : [32, 38]})
    testvar  = BarWithWaterfall(test=True)
    testvar.data_scenarios = ['PY', 'PL', 'AC', 'FC']
    expected = {'PY': 70.65, 'PL': 71.73, 'AC': 68.3, 'FC': 70}
    testvar._fill_data_total(dataframe=dataset, decimals=2)
    actual   = testvar.data_total
    message  = "Test 1 - BarWithWaterfall._fill_data_total returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 2 - good dataframe with some scenarios. Decimals is 1
    dataset  = pd.DataFrame({'Year' : ['2021', '2022'],
                             'Month': ['02', '04'],
                             'PY'   : [32.453, 38.2],
                             'PL'   : [32.74532, 38.98899],
                             'AC'   : [35.3, 33],
                             'FC'   : [32, 38]})
    testvar  = BarWithWaterfall(test=True)
    testvar.data_scenarios = ['PY', 'PL', 'AC', 'FC']
    expected = {'PY': 70.7, 'PL': 71.7, 'AC': 68.3, 'FC': 70}
    testvar._fill_data_total(dataframe=dataset, decimals=1)
    actual   = testvar.data_total
    message  = "Test 2 - BarWithWaterfall._fill_data_total returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 3 - good dataframe with some scenarios. Decimals is 0
    dataset  = pd.DataFrame({'Year' : ['2021', '2022'],
                             'Month': ['02', '04'],
                             'PY'   : [32.453, 38.2],
                             'PL'   : [32.74532, 38.98899],
                             'AC'   : [35.3, 33],
                             'FC'   : [32, 38]})
    testvar  = BarWithWaterfall(test=True)
    testvar.data_scenarios = ['PY', 'PL', 'AC', 'FC']
    expected = {'PY': 71, 'PL': 72, 'AC': 68, 'FC': 70}
    testvar._fill_data_total(dataframe=dataset, decimals=0)
    actual   = testvar.data_total
    message  = "Test 3 - BarWithWaterfall._fill_data_total returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 4 - good dataframe with some scenarios. Decimals is None (default value)
    dataset  = pd.DataFrame({'Year' : ['2021', '2022'],
                             'Month': ['02', '04'],
                             'PY'   : [32.453, 38.2],
                             'PL'   : [32.74532, 38.98899],
                             'AC'   : [35.3, 33],
                             'FC'   : [32, 38]})
    testvar  = BarWithWaterfall(test=True)
    testvar.data_scenarios = ['PY', 'PL', 'AC', 'FC']
    expected = {'PY': 70.653, 'PL': 71.73431, 'AC': 68.3, 'FC': 70}
    testvar._fill_data_total(dataframe=dataset)
    actual   = testvar.data_total
    message  = "Test 4 - BarWithWaterfall._fill_data_total returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 5 - parameter dataframe is a string and not a dataframe
    with pytest.raises(TypeDataFrameError):
        testvar = BarWithWaterfall(test=True)
        testvar.data_scenarios = ['PY', 'PL', 'AC', 'FC']
        testvar._fill_data_total(dataframe="This is a string")  # Default parameter decimals is None and that is supported

    # Test 6 - parameter decimals is a string and not an integer
    with pytest.raises(TypeIntegerError):
        testvar = BarWithWaterfall(test=True)
        testvar.data_scenarios = ['PY', 'PL', 'AC', 'FC']
        dataset  = pd.DataFrame({'Year' : ['2021', '2022'],
                                 'Month': ['02', '04'],
                                 'PY'   : [32.453, 38.2],
                                 'PL'   : [32.74532, 38.98899],
                                 'AC'   : [35.3, 33],
                                 'FC'   : [32, 38]})
        testvar._fill_data_total(dataframe=dataset, decimals="This is a string")


def test__dataframe_find_category_of_interest():
    # Test 1 - good dataframe with all scenarios and a few extra categories. Parameter category provided
    dataset  = pd.DataFrame({'Year' : ['2021', '2022'],
                             'Month': ['02', '04'],
                             'PY'   : [32.453, 38.2],
                             'PL'   : [32.74532, 38.98899],
                             'Plane': ['Airbus', 'Boeing'],
                             'Type' : ['Passenger', 'Freight'],
                             'AC'   : [35.3, 33],
                             'FC'   : [32, 38]})
    testvar  = BarWithWaterfall(test=True)
    testvar.all_scenarios = ['Month', 'Date', 'Year', 'PY', 'PL', 'AC', 'FC']
    testvar.category = 'Type'
    expected = 'Type'
    actual = testvar._dataframe_find_category_of_interest(dataframe=dataset)
    message  = "Test 1 - BarWithWaterfall._dataframe_find_category_of_interest returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 2 - good dataframe with all scenarios and a few extra categories. Parameter category not provided
    dataset  = pd.DataFrame({'Year' : ['2021', '2022'],
                             'Month': ['02', '04'],
                             'PY'   : [32.453, 38.2],
                             'PL'   : [32.74532, 38.98899],
                             'Plane': ['Airbus', 'Boeing'],
                             'Type' : ['Passenger', 'Freight'],
                             'AC'   : [35.3, 33],
                             'FC'   : [32, 38]})
    testvar  = BarWithWaterfall(test=True)
    testvar.all_scenarios = ['Month', 'Date', 'Year', 'PY', 'PL', 'AC', 'FC']
    testvar.category = None
    expected = 'Plane'
    actual = testvar._dataframe_find_category_of_interest(dataframe=dataset)
    message  = "Test 2 - BarWithWaterfall._dataframe_find_category_of_interest returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 3 - good dataframe with all scenarios and a few extra categories. Parameter category is provided but value is not in column headers
    with pytest.raises(ValueError):
        dataset  = pd.DataFrame({'Year' : ['2021', '2022'],
                             'Month': ['02', '04'],
                             'PY'   : [32.453, 38.2],
                             'PL'   : [32.74532, 38.98899],
                             'Plane': ['Airbus', 'Boeing'],
                             'Type' : ['Passenger', 'Freight'],
                             'AC'   : [35.3, 33],
                             'FC'   : [32, 38]})
        testvar  = BarWithWaterfall(test=True)
        testvar.all_scenarios = ['Month', 'Date', 'Year', 'PY', 'PL', 'AC', 'FC']
        testvar.category = 'Airport'
        testvar._dataframe_find_category_of_interest(dataframe=dataset)

    # Test 4 - good dataframe with all scenarios, but no extra categories. Parameter category is not provided.
    with pytest.raises(ValueError):
        dataset  = pd.DataFrame({'Year' : ['2021', '2022'],
                             'Month': ['02', '04'],
                             'PY'   : [32.453, 38.2],
                             'PL'   : [32.74532, 38.98899],
                             'AC'   : [35.3, 33],
                             'FC'   : [32, 38]})
        testvar  = BarWithWaterfall(test=True)
        testvar.all_scenarios = ['Month', 'Date', 'Year', 'PY', 'PL', 'AC', 'FC']
        testvar.category = None
        testvar._dataframe_find_category_of_interest(dataframe=dataset)

    # Test 5 - good dataframe with all scenarios, but no extra categories. Parameter category is one of the supported date categories.
    with pytest.raises(ValueError):
        dataset  = pd.DataFrame({'Year' : ['2021', '2022'],
                             'Month': ['02', '04'],
                             'PY'   : [32.453, 38.2],
                             'PL'   : [32.74532, 38.98899],
                             'AC'   : [35.3, 33],
                             'FC'   : [32, 38]})
        testvar  = BarWithWaterfall(test=True)
        testvar.all_scenarios = ['Month', 'Date', 'Year', 'PY', 'PL', 'AC', 'FC']
        testvar.category = 'Year'
        testvar._dataframe_find_category_of_interest(dataframe=dataset)

    # Test 6 - parameter is a string and not a dataframe
    with pytest.raises(TypeDataFrameError):
        testvar  = BarWithWaterfall(test=True)
        testvar.all_scenarios = ['Month', 'Date', 'Year', 'PY', 'PL', 'AC', 'FC']
        testvar.category = None
        testvar._dataframe_find_category_of_interest(dataframe="This is a string")


def test__dataframe_aggregate():
    # Test 1 - good dataframe with all scenarios and a few extra categories, aggregate on _Category and Year
    dataset  = pd.DataFrame({'Year'     : ['2021', '2021', '2021', '2022', '2022'],
                             'Month'    : ['02', '04', '07', '08', '09'],
                             'PY'       : [32, 38.2, 40, 39, 38],
                             'PL'       : [33, 38.98899, 41, 40, 39],
                             '_Category': ['Airbus', 'Boeing', 'Airbus', 'Boeing', 'Airbus'],
                             'Type'     : ['Passenger', 'Freight', 'Freight', 'Passenger', 'Freight'],
                             'AC'       : [35, 33, 39, 37, 36],
                             'FC'       : [32, 38, 41, 39, 40]})
    testvar  = BarWithWaterfall(test=True)
    expected = {'_Category': ['Airbus', 'Boeing', 'Boeing', 'Airbus'], 'Year': ['2021', '2021', '2022', '2022'],
                'PY': [72.0, 38.2, 39.0, 38.0], 'PL': [74.0, 38.98899, 40.0, 39.0], 'AC': [74, 33, 37, 36], 'FC': [73, 38, 39, 40]}
    actual   = testvar._dataframe_aggregate(dataframe=dataset, wanted_headers=['_Category', 'Year'])
    actual   = actual.to_dict(orient='list')
    message  = "Test 1 - BarWithWaterfall._dataframe_aggregate returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 2 - good dataframe with all scenarios and a few extra categories, aggregate on _Category
    dataset  = pd.DataFrame({'Year'     : ['2021', '2021', '2021', '2022', '2022'],
                             'Month'    : ['02', '04', '07', '08', '09'],
                             'PY'       : [32, 38.2, 40, 39, 38],
                             'PL'       : [33, 38.98899, 41, 40, 39],
                             '_Category': ['Airbus', 'Boeing', 'Airbus', 'Boeing', 'Airbus'],
                             'Type'     : ['Passenger', 'Freight', 'Freight', 'Passenger', 'Freight'],
                             'AC'       : [35, 33, 39, 37, 36],
                             'FC'       : [32, 38, 41, 39, 40]})
    testvar  = BarWithWaterfall(test=True)
    expected =  {'_Category': ['Airbus', 'Boeing'], 'PY': [110.0, 77.2], 'PL': [113.0, 78.98899], 'AC': [110, 70], 'FC': [113, 77]}
    actual   = testvar._dataframe_aggregate(dataframe=dataset, wanted_headers=['_Category'])
    actual   = actual.to_dict(orient='list')
    message  = "Test 2 - BarWithWaterfall._dataframe_aggregate returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 3 - parameter dataframe is a string and not a dataframe
    with pytest.raises(TypeDataFrameError):
        testvar  = BarWithWaterfall(test=True)
        testvar._dataframe_aggregate(dataframe="This is a string", wanted_headers=['list-item 1', 'list-item 2'])

    # Test 4 - parameter wanted_headers is a string and not a list
    with pytest.raises(TypeListError):
        testvar  = BarWithWaterfall(test=True)
        dataset  = pd.DataFrame({'Year'     : ['2021', '2021', '2021', '2022', '2022'],
                                 'Month'    : ['02', '04', '07', '08', '09'],
                                 'PY'       : [32, 38.2, 40, 39, 38],
                                 'PL'       : [33, 38.98899, 41, 40, 39],
                                 '_Category': ['Airbus', 'Boeing', 'Airbus', 'Boeing', 'Airbus'],
                                 'Type'     : ['Passenger', 'Freight', 'Freight', 'Passenger', 'Freight'],
                                 'AC'       : [35, 33, 39, 37, 36],
                                 'FC'       : [32, 38, 41, 39, 40]})
        testvar._dataframe_aggregate(dataframe=dataset, wanted_headers="This is a string")

    # Test 5 - dataframe does not contain header _Category
    with pytest.raises(ValueError):
        testvar  = BarWithWaterfall(test=True)
        dataset  = pd.DataFrame({'Year'     : ['2021', '2021', '2021', '2022', '2022'],
                                 'Month'    : ['02', '04', '07', '08', '09'],
                                 'PY'       : [32, 38.2, 40, 39, 38],
                                 'PL'       : [33, 38.98899, 41, 40, 39],
                                 'Type'     : ['Passenger', 'Freight', 'Freight', 'Passenger', 'Freight'],
                                 'AC'       : [35, 33, 39, 37, 36],
                                 'FC'       : [32, 38, 41, 39, 40]})
        testvar._dataframe_aggregate(dataframe=dataset, wanted_headers=['_Category'])

    # Test 6 - dataframe does contain header _Category, but it is not in the wanted_headers
    with pytest.raises(ValueError):
        testvar  = BarWithWaterfall(test=True)
        dataset  = pd.DataFrame({'Year'     : ['2021', '2021', '2021', '2022', '2022'],
                                 'Month'    : ['02', '04', '07', '08', '09'],
                                 'PY'       : [32, 38.2, 40, 39, 38],
                                 '_Category': ['Airbus', 'Boeing', 'Airbus', 'Boeing', 'Airbus'],
                                 'PL'       : [33, 38.98899, 41, 40, 39],
                                 'Type'     : ['Passenger', 'Freight', 'Freight', 'Passenger', 'Freight'],
                                 'AC'       : [35, 33, 39, 37, 36],
                                 'FC'       : [32, 38, 41, 39, 40]})
        testvar._dataframe_aggregate(dataframe=dataset, wanted_headers=['Year'])


def test__optimize_data_total():
    # Test 1 - good dictionary and good parameters (with unusual, but valid values and two decimals)
    testvar   = BarWithWaterfall(test=True)
    testvar.data_total = {'AC':1357.2468, 'PL':862.64, 'PY':8723.85, 'FC':103020.76932}
    expected1 = {'AC': 48.85, 'PL': 31.05, 'PY': 313.97, 'FC': 3707.69}
    expected2 = 2425.09
    testvar.scalingvalue = 67382.9382718
    testvar._optimize_data_total(numerator=14, denominator=389, decimals=2)
    actual1   = testvar.data_total
    actual2   = testvar.scalingvalue
    message   = "Test 1a - BarWithWaterfall._optimize_data_total returned {0} instead of {1}".format(actual1, expected1)
    assert actual1 == expected1, message
    message   = "Test 1b - BarWithWaterfall._optimize_data_total returned {0} instead of {1}".format(actual2, expected2)
    assert actual2 == expected2, message

    # Test 2 - good dictionary and good parameters (with normal, valid values and one decimals)
    testvar   = BarWithWaterfall(test=True)
    testvar.data_total = {'AC':1357.2468, 'PL':862.64, 'PY':8723.85, 'FC':103020.76932}
    expected1 = {'AC': 1.4, 'PL': 0.9, 'PY': 8.7, 'FC': 103.0}
    expected2 = 67.4
    testvar.scalingvalue = 67382.9382718
    testvar._optimize_data_total(numerator=1, denominator=1000, decimals=1)
    actual1   = testvar.data_total
    actual2   = testvar.scalingvalue
    message   = "Test 2a - BarWithWaterfall._optimize_data_total returned {0} instead of {1}".format(actual1, expected1)
    assert actual1 == expected1, message
    message   = "Test 2b - BarWithWaterfall._optimize_data_total returned {0} instead of {1}".format(actual2, expected2)
    assert actual2 == expected2, message

    # Test 3 - good dictionary and good parameters (with unusual, valid values and no decimals)
    testvar   = BarWithWaterfall(test=True)
    testvar.data_total = {'AC':1357.2468, 'PL':862.64, 'PY':8723.85, 'FC':103020.76932}
    expected1 = {'AC': 68, 'PL': 43, 'PY': 436, 'FC': 5151}
    expected2 = 3369
    testvar.scalingvalue = 67382.9382718
    testvar._optimize_data_total(numerator=50, denominator=1000, decimals=0)
    actual1   = testvar.data_total
    actual2   = testvar.scalingvalue
    message   = "Test 3a - BarWithWaterfall._optimize_data_total returned {0} instead of {1}".format(actual1, expected1)
    assert actual1 == expected1, message
    message   = "Test 3b - BarWithWaterfall._optimize_data_total returned {0} instead of {1}".format(actual2, expected2)
    assert actual2 == expected2, message

    # Test 4 - repeat of test 3, but with scalingvalue None
    testvar   = BarWithWaterfall(test=True)
    testvar.data_total = {'AC':1357.2468, 'PL':862.64, 'PY':8723.85, 'FC':103020.76932}
    expected1 = {'AC': 68, 'PL': 43, 'PY': 436, 'FC': 5151}
    expected2 = None
    testvar.scalingvalue = None
    testvar._optimize_data_total(numerator=50, denominator=1000, decimals=0)
    actual1   = testvar.data_total
    actual2   = testvar.scalingvalue
    message   = "Test 4a - BarWithWaterfall._optimize_data_total returned {0} instead of {1}".format(actual1, expected1)
    assert actual1 == expected1, message
    message   = "Test 4b - BarWithWaterfall._optimize_data_total returned {0} instead of {1}".format(actual2, expected2)
    assert actual2 == expected2, message

    # Test 5 - Numerator is not an integer
    with pytest.raises(TypeIntegerError):
        testvar  = BarWithWaterfall(test=True)
        testvar.data_total = {'AC':1357.2468, 'PL':862.64, 'PY':8723.85, 'FC':103020.76932}
        testvar._optimize_data_total(numerator="This is a string", denominator=1, decimals=0)

    # Test 6 - Denominator is not an integer
    with pytest.raises(TypeIntegerError):
        testvar  = BarWithWaterfall(test=True)
        testvar.data_total = {'AC':1357.2468, 'PL':862.64, 'PY':8723.85, 'FC':103020.76932}
        testvar._optimize_data_total(numerator=1, denominator="This is a string", decimals=0)

    # Test 7 - Decimals is not an integer
    with pytest.raises(TypeIntegerError):
        testvar  = BarWithWaterfall(test=True)
        testvar.data_total = {'AC':1357.2468, 'PL':862.64, 'PY':8723.85, 'FC':103020.76932}
        testvar._optimize_data_total(numerator=1, denominator=1, decimals="This is a string")

    # Test 8 - Data_total is not a dictionary
    with pytest.raises(TypeDictionaryError):
        testvar  = BarWithWaterfall(test=True)
        testvar.data_total = "This is a string"
        testvar._optimize_data_total(numerator=1, denominator=1, decimals=1)


def test__dataframe_full_category():
    # Test 1 - good dataframe with all scenarios and a few extra categories
    dataset  = pd.DataFrame({'Year'     : ['2021', '2021', '2021', '2021', '2021'],
                             'Month'    : ['02', '04', '07', '08', '09'],
                             'PY'       : [32, 38.2, 40, 39, 38],
                             'PL'       : [33, 38.98899, 41, 40, 39],
                             '_Category': ['Airbus', 'Boeing', 'Airbus', 'Boeing', 'Airbus'],
                             'Type'     : ['Passenger', 'Freight', 'Freight', 'Passenger', 'Freight'],
                             'AC'       : [35, 33, 39, 37, 36],
                             'FC'       : [32, 38, 41, 39, 40]})
    category_list = ['Airbus', 'Boeing', 'General Dynamics', 'Lockheed Martin']
    testvar  = BarWithWaterfall(test=True)
    expected = {'Year'     : ['2021', '2021', '2021', '2021', '2021', '2021', '2021'], 
                '_Category': ['Airbus', 'Airbus', 'Airbus', 'Boeing', 'Boeing', 'General Dynamics', 'Lockheed Martin'], 
                'Month'    : ['02', '07', '09', '04', '08', '', ''], 
                'PY'       : [32.0, 40.0, 38.0, 38.2, 39.0, 0.0, 0.0], 
                'PL'       : [33.0, 41.0, 39.0, 38.98899, 40.0, 0.0, 0.0], 
                'Type'     : ['Passenger', 'Freight', 'Freight', 'Freight', 'Passenger', '', ''], 
                'AC'       : [35.0, 39.0, 36.0, 33.0, 37.0, 0.0, 0.0], 
                'FC'       : [32.0, 41.0, 40.0, 38.0, 39.0, 0.0, 0.0]}
    actual   = testvar._dataframe_full_category(dataframe=dataset, category_of_interest_values=category_list)
    actual   = actual.to_dict(orient='list')
    message  = "Test 1 - BarWithWaterfall._dataframe_full_category returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 2 - empty dataframe
    dataset  = pd.DataFrame()
    category_list = ['Airbus', 'Boeing', 'General Dynamics', 'Lockheed Martin']
    testvar  = BarWithWaterfall(test=True)
    expected = {}
    actual   = testvar._dataframe_full_category(dataframe=dataset, category_of_interest_values=category_list)
    actual   = actual.to_dict(orient='list')
    message  = "Test 2 - BarWithWaterfall._dataframe_full_category returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 3 - Good dataframe with all scenarios and a few extra categories, but with more unique category of interest entries than the related list
    with pytest.raises(ValueError):
        dataset  = pd.DataFrame({'Year'     : ['2021', '2021', '2021', '2021', '2021'],
                                 'Month'    : ['02', '04', '07', '08', '09'],
                                 'PY'       : [32, 38.2, 40, 39, 38],
                                 'PL'       : [33, 38.98899, 41, 40, 39],
                                 '_Category': ['Airbus', 'Boeing', 'General Dynamics', 'Lockheed Martin', 'Airbus'],
                                 'Type'     : ['Passenger', 'Freight', 'Freight', 'Passenger', 'Freight'],
                                 'AC'       : [35, 33, 39, 37, 36],
                                 'FC'       : [32, 38, 41, 39, 40]})
        category_list = ['Airbus', 'Boeing']
        testvar  = BarWithWaterfall(test=True)
        testvar._dataframe_full_category(dataframe=dataset, category_of_interest_values=category_list)

    # Test 4 - Two different years in dataframe
    with pytest.raises(ValueError):
        dataset  = pd.DataFrame({'Year'     : ['2021', '2021', '2022', '2022', '2021'],
                                 'Month'    : ['02', '04', '07', '08', '09'],
                                 'PY'       : [32, 38.2, 40, 39, 38],
                                 'PL'       : [33, 38.98899, 41, 40, 39],
                                 '_Category': ['Airbus', 'Boeing', 'Airbus', 'Boeing', 'Airbus'],
                                 'Type'     : ['Passenger', 'Freight', 'Freight', 'Passenger', 'Freight'],
                                 'AC'       : [35, 33, 39, 37, 36],
                                 'FC'       : [32, 38, 41, 39, 40]})
        category_list = ['Airbus', 'Boeing']
        testvar  = BarWithWaterfall(test=True)
        testvar._dataframe_full_category(dataframe=dataset, category_of_interest_values=category_list)

    # Test 5 - No year column in dataframe
    with pytest.raises(ValueError):
        dataset  = pd.DataFrame({'Month'    : ['02', '04', '07', '08', '09'],
                                 'PY'       : [32, 38.2, 40, 39, 38],
                                 'PL'       : [33, 38.98899, 41, 40, 39],
                                 '_Category': ['Airbus', 'Boeing', 'Airbus', 'Boeing', 'Airbus'],
                                 'Type'     : ['Passenger', 'Freight', 'Freight', 'Passenger', 'Freight'],
                                 'AC'       : [35, 33, 39, 37, 36],
                                 'FC'       : [32, 38, 41, 39, 40]})
        category_list = ['Airbus', 'Boeing']
        testvar  = BarWithWaterfall(test=True)
        testvar._dataframe_full_category(dataframe=dataset, category_of_interest_values=category_list)

    # Test 6 - No category column in dataframe
    with pytest.raises(ValueError):
        dataset  = pd.DataFrame({'Year'     : ['2021', '2021', '2021', '2021', '2021'],
                                 'Month'    : ['02', '04', '07', '08', '09'],
                                 'PY'       : [32, 38.2, 40, 39, 38],
                                 'PL'       : [33, 38.98899, 41, 40, 39],
                                 'Type'     : ['Passenger', 'Freight', 'Freight', 'Passenger', 'Freight'],
                                 'AC'       : [35, 33, 39, 37, 36],
                                 'FC'       : [32, 38, 41, 39, 40]})
        category_list = ['Airbus', 'Boeing']
        testvar  = BarWithWaterfall(test=True)
        testvar._dataframe_full_category(dataframe=dataset, category_of_interest_values=category_list)

    # Test 7 - Category of interest is not a list
    with pytest.raises(TypeListError):
        dataset  = pd.DataFrame({'Year'     : ['2021', '2021', '2021', '2021', '2021'],
                                 'Month'    : ['02', '04', '07', '08', '09'],
                                 'PY'       : [32, 38.2, 40, 39, 38],
                                 'PL'       : [33, 38.98899, 41, 40, 39],
                                 '_Category': ['Airbus', 'Boeing', 'Airbus', 'Boeing', 'Airbus'],
                                 'Type'     : ['Passenger', 'Freight', 'Freight', 'Passenger', 'Freight'],
                                 'AC'       : [35, 33, 39, 37, 36],
                                 'FC'       : [32, 38, 41, 39, 40]})
        testvar  = BarWithWaterfall(test=True)
        testvar._dataframe_full_category(dataframe=dataset, category_of_interest_values="this is a string")

    # Test 8 - Category of interest is an empty list
    with pytest.raises(ValueError):
        dataset  = pd.DataFrame({'Year'     : ['2021', '2021', '2021', '2021', '2021'],
                                 'Month'    : ['02', '04', '07', '08', '09'],
                                 'PY'       : [32, 38.2, 40, 39, 38],
                                 'PL'       : [33, 38.98899, 41, 40, 39],
                                 '_Category': ['Airbus', 'Boeing', 'Airbus', 'Boeing', 'Airbus'],
                                 'Type'     : ['Passenger', 'Freight', 'Freight', 'Passenger', 'Freight'],
                                 'AC'       : [35, 33, 39, 37, 36],
                                 'FC'       : [32, 38, 41, 39, 40]})
        category_list = []
        testvar  = BarWithWaterfall(test=True)
        testvar._dataframe_full_category(dataframe=dataset, category_of_interest_values=category_list)

    # Test 9 - No dataframe type
    with pytest.raises(TypeDataFrameError):
        category_list = ['Airbus', 'Boeing']
        testvar  = BarWithWaterfall(test=True)
        testvar._dataframe_full_category(dataframe='This is a string', category_of_interest_values=category_list)


def test__dataframe_handle_previous_year():
    # Test 1 - good dataframe with previous year scenario, aggregate on _Category and Year
    dataset  = pd.DataFrame({'Year'     : ['2021', '2021', '2021', '2022', '2022', '2022'],
                             'PY'       : [32, 38.2, 40, 38, 32, 43],
                             'PL'       : [33, 38.98899, 41, 40, 39, 27],
                             '_Category': ['Airbus', 'Boeing', 'General Dynamics', 'Boeing', 'Airbus', 'General Dynamics'],
                             'AC'       : [32, 38, 43, 34, 33.6, 39],
                             'FC'       : [38, 32, 41, 39, 40, 37]})
    testvar  = BarWithWaterfall(test=True)
    expected = {'Year': ['2022', '2022', '2022'], '_Category': ['Airbus', 'Boeing', 'General Dynamics'], 
                'PY': [32.0, 38.0, 43.0], 'PL': [39.0, 40.0, 27.0], 'AC': [33.6, 34.0, 39.0], 'FC': [40, 39, 37]}
    actual   = testvar._dataframe_handle_previous_year(dataframe=dataset)
    actual   = actual.to_dict(orient='list')
    message  = "Test 1 - BarWithWaterfall._dataframe_handle_previous_year returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 2 - good dataframe without previous year scenario, aggregate on _Category and Year. Number of previous year values are not equal to the number of this year values
    dataset  = pd.DataFrame({'Year'     : ['2021', '2021', '2021', '2022', '2022'],
                             'PL'       : [33, 38.98899, 41, 40, 39],
                             '_Category': ['Airbus', 'Boeing', 'Lockheed Martin', 'Boeing', 'Lockheed Martin'],
                             'AC'       : [32, 38, 43, 34, 33.6],
                             'FC'       : [38, 32, 41, 39, 40]})
    testvar  = BarWithWaterfall(test=True)
    expected = {'Year': ['2022', '2022', '2022'], '_Category': ['Airbus', 'Boeing', 'Lockheed Martin'],
                'PL': [0.0, 40.0, 39.0], 'AC': [0.0, 34.0, 33.6], 'FC': [0.0, 39.0, 40.0], 'PY': [32.0, 38.0, 43.0]}
    actual   = testvar._dataframe_handle_previous_year(dataframe=dataset)
    actual   = actual.to_dict(orient='list')
    message  = "Test 2 - BarWithWaterfall._dataframe_handle_previous_year returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 3 - good dataframe without year column
    dataset  = pd.DataFrame({'PY'       : [32, 38.2, 40, 39, 38],
                             'PL'       : [33, 38.98899, 41, 40, 39],
                             '_Category': ['Airbus', 'Boeing', 'Lockheed Martin', 'Boeing', 'Lockheed Martin'],
                             'AC'       : [32, 38, 43, 34, 33.6],
                             'FC'       : [38, 32, 41, 39, 40]})
    testvar  = BarWithWaterfall(test=True)
    expected = {'_Category': ['Airbus', 'Boeing', 'Lockheed Martin', 'Boeing', 'Lockheed Martin'],
                'PY': [32.0, 38.2, 40.0, 39.0, 38.0], 'PL': [33.0, 38.98899, 41.0, 40.0, 39.0],  
                'AC': [32.0, 38.0, 43.0, 34.0, 33.6], 'FC': [38, 32, 41, 39, 40]}
    actual   = testvar._dataframe_handle_previous_year(dataframe=dataset)
    actual   = actual.to_dict(orient='list')
    message  = "Test 2 - BarWithWaterfall._dataframe_handle_previous_year returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 4 - Number of columns are more than needed
    with pytest.raises(ValueError):
        dataset  = pd.DataFrame({'Year'     : ['2021', '2021', '2021', '2022', '2022'],
                                 'Month'    : ['02', '04', '07', '08', '09'],
                                 'PY'       : [32, 38.2, 40, 39, 38],
                                 'PL'       : [33, 38.98899, 41, 40, 39],
                                 '_Category': ['Airbus', 'Boeing', 'Airbus', 'Boeing', 'Airbus'],
                                 'Type'     : ['Passenger', 'Freight', 'Freight', 'Passenger', 'Freight'],
                                 'AC'       : [35, 33, 39, 37, 36],
                                 'FC'       : [32, 38, 41, 39, 40]})
        testvar  = BarWithWaterfall(test=True)
        testvar._dataframe_handle_previous_year(dataframe=dataset)

    # Test 5 - Dataframe with previous year scenario, aggregate on _Category and Year, Number of previous year values are not equal to the number of this year values
    with pytest.raises(ValueError):
        dataset  = pd.DataFrame({'Year'     : ['2021', '2021', '2021', '2022', '2022'],
                                 'PY'       : [32, 38.2, 40, 39, 38],
                                 'PL'       : [33, 38.98899, 41, 40, 39],
                                 '_Category': ['Airbus', 'Boeing', 'Airbus', 'Boeing', 'Airbus'],
                                 'AC'       : [35, 33, 39, 37, 36],
                                 'FC'       : [32, 38, 41, 39, 40]})
        testvar  = BarWithWaterfall(test=True)
        testvar._dataframe_handle_previous_year(dataframe=dataset)

    # Test 6 - Dataframe with previous year scenario, aggregate on _Category and Year, PY values 2022 are not equal to AC values 2021
    with pytest.raises(ValueError):
        dataset  = pd.DataFrame({'Year'     : ['2021', '2021', '2021', '2022', '2022', '2022'],
                                 'PY'       : [32, 38.2, 40, 32, 38, 43],
                                 'PL'       : [33, 38.98899, 41, 40, 39, 27],
                                 '_Category': ['Lockheed Martin', 'Boeing', 'Airbus', 'Boeing', 'Airbus', 'Lockheed Martin'],
                                 'AC'       : [35, 33, 39, 37, 36, 33],
                                 'FC'       : [32, 38, 41, 39, 40, 37]})
        testvar  = BarWithWaterfall(test=True)
        testvar._dataframe_handle_previous_year(dataframe=dataset)

    # Test 7 - Parameter dataframe is a string and not a dataframe
    with pytest.raises(TypeError):
        testvar  = BarWithWaterfall(test=True)
        testvar._dataframe_handle_previous_year(dataframe="This is a string")

    # Test 8 - dataframe does not contain header _Category
    with pytest.raises(ValueError):
        testvar  = BarWithWaterfall(test=True)
        dataset  = pd.DataFrame({'Year'     : ['2021', '2021', '2021', '2022', '2022'],
                                 'PL'       : [33, 38.98899, 41, 40, 39],
                                 'AC'       : [35, 33, 39, 37, 36],
                                 'FC'       : [32, 38, 41, 39, 40]})
        testvar._dataframe_handle_previous_year(dataframe=dataset)

def test__determine_bar_layers_in_dataframe():
    # Test 1 - Good dataframe with values for both compare-scenarios
    dataset  = pd.DataFrame({'Year'     : ['2022', '2022', '2022', '2022'],
                             'PY'       : [32.7, 38.2, 40, 38],
                             'PL'       : [33, 38.98899, 41, 40.3],
                             '_Category': ['Airbus', 'Boeing', 'General Dynamics', 'Lockheed Martin'],
                             'AC'       : [32.25, 38, 33.6, 39],
                             'FC'       : [38.65, 32, 41, 37.1]})
    testvar  = BarWithWaterfall(test=True)
    testvar.compare_scenarios = ['AC', 'FC']
    expected = {'Year': ['2022', '2022', '2022', '2022'], 'PY': [32.7, 38.2, 40.0, 38.0], 
                'PL': [33.0, 38.98899, 41.0, 40.3], '_Category': ['Airbus', 'Boeing', 'General Dynamics', 'Lockheed Martin'], 
                'AC': [32.25, 38.0, 33.6, 39.0], 'FC': [38.65, 32.0, 41.0, 37.1], 
                '_CBC_TOPLAYER': ['FC', 'FC', 'FC', 'FC']}
    actual   = testvar._determine_bar_layers_in_dataframe(dataframe=dataset)
    actual   = actual.to_dict(orient='list')
    message  = "Test 1 - BarWithWaterfall._determine_bar_layers_in_dataframe returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 2 - Good dataframe with all zeros for 2nd compare-scenario
    dataset  = pd.DataFrame({'Year'     : ['2022', '2022', '2022', '2022'],
                             'PY'       : [32.7, 38.2, 40, 38],
                             'PL'       : [33, 38.98899, 41, 40.3],
                             '_Category': ['Airbus', 'Boeing', 'General Dynamics', 'Lockheed Martin'],
                             'AC'       : [32.25, 38, 33.6, 39],
                             'FC'       : [0, 0, 0, 0]})
    testvar  = BarWithWaterfall(test=True)
    testvar.compare_scenarios = ['AC', 'FC']
    expected = {'Year': ['2022', '2022', '2022', '2022'], 'PY': [32.7, 38.2, 40.0, 38.0],
                'PL': [33.0, 38.98899, 41.0, 40.3], '_Category': ['Airbus', 'Boeing', 'General Dynamics', 'Lockheed Martin'],
                'AC': [32.25, 38.0, 33.6, 39.0], 'FC': [0, 0, 0, 0],
                '_CBC_TOPLAYER': ['AC', 'AC', 'AC', 'AC']} 
    actual   = testvar._determine_bar_layers_in_dataframe(dataframe=dataset)
    actual   = actual.to_dict(orient='list')
    message  = "Test 2 - BarWithWaterfall._determine_bar_layers_in_dataframe returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 3 - Good dataframe with some zeros for 2nd compare-scenario
    dataset  = pd.DataFrame({'Year'     : ['2022', '2022', '2022', '2022'],
                             'PY'       : [32.7, 38.2, 40, 38],
                             'PL'       : [33, 38.98899, 41, 40.3],
                             '_Category': ['Airbus', 'Boeing', 'General Dynamics', 'Lockheed Martin'],
                             'AC'       : [32.25, 38, 33.6, 39],
                             'FC'       : [38.65, 0, 0, 37.1]})
    testvar  = BarWithWaterfall(test=True)
    testvar.compare_scenarios = ['AC', 'FC']
    expected = {'Year': ['2022', '2022', '2022', '2022'], 'PY': [32.7, 38.2, 40.0, 38.0], 
                'PL': [33.0, 38.98899, 41.0, 40.3], '_Category': ['Airbus', 'Boeing', 'General Dynamics', 'Lockheed Martin'],
                'AC': [32.25, 38.0, 33.6, 39.0], 'FC': [38.65, 0.0, 0.0, 37.1], 
                '_CBC_TOPLAYER': ['FC', 'AC', 'AC', 'FC']}
    actual   = testvar._determine_bar_layers_in_dataframe(dataframe=dataset)
    actual   = actual.to_dict(orient='list')
    message  = "Test 3 - BarWithWaterfall._determine_bar_layers_in_dataframe returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 4 - Good dataframe with all zeros for first compare-scenario
    dataset  = pd.DataFrame({'Year'     : ['2022', '2022', '2022', '2022'],
                             'PY'       : [32.7, 38.2, 40, 38],
                             'PL'       : [33, 38.98899, 41, 40.3],
                             '_Category': ['Airbus', 'Boeing', 'General Dynamics', 'Lockheed Martin'],
                             'AC'       : [0, 0, 0, 0],
                             'FC'       : [38.65, 32, 41, 37.1]})
    testvar  = BarWithWaterfall(test=True)
    testvar.compare_scenarios = ['AC', 'FC']
    expected = {'Year': ['2022', '2022', '2022', '2022'], 'PY': [32.7, 38.2, 40.0, 38.0], 
                'PL': [33.0, 38.98899, 41.0, 40.3], '_Category': ['Airbus', 'Boeing', 'General Dynamics', 'Lockheed Martin'], 
                'AC': [0, 0, 0, 0], 'FC': [38.65, 32.0, 41.0, 37.1], 
                '_CBC_TOPLAYER': ['FC', 'FC', 'FC', 'FC']}
    actual   = testvar._determine_bar_layers_in_dataframe(dataframe=dataset)
    actual   = actual.to_dict(orient='list')
    message  = "Test 4 - BarWithWaterfall._determine_bar_layers_in_dataframe returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 5 - Good dataframe with some zero values for both compare-scenarios
    dataset  = pd.DataFrame({'Year'     : ['2022', '2022', '2022', '2022'],
                             'PY'       : [32.7, 38.2, 40, 38],
                             'PL'       : [33, 38.98899, 41, 40.3],
                             '_Category': ['Airbus', 'Boeing', 'General Dynamics', 'Lockheed Martin'],
                             'AC'       : [32.25, 0, 0, 39],
                             'FC'       : [0, 32, 0, 37.1]})
    testvar  = BarWithWaterfall(test=True)
    testvar.compare_scenarios = ['AC', 'FC']
    expected = {'Year': ['2022', '2022', '2022', '2022'], 'PY': [32.7, 38.2, 40.0, 38.0], 
                'PL': [33.0, 38.98899, 41.0, 40.3], '_Category': ['Airbus', 'Boeing', 'General Dynamics', 'Lockheed Martin'], 
                'AC': [32.25, 0.0, 0.0, 39.0], 'FC': [0.0, 32.0, 0.0, 37.1], 
                '_CBC_TOPLAYER': ['AC', 'FC', 'AC', 'FC']}
    actual   = testvar._determine_bar_layers_in_dataframe(dataframe=dataset)
    actual   = actual.to_dict(orient='list')
    message  = "Test 5 - BarWithWaterfall._determine_bar_layers_in_dataframe returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 6 - String instead of dataframe
    with pytest.raises(TypeDataFrameError):
        testvar  = BarWithWaterfall(test=True)
        testvar.compare_scenarios = ['AC', 'FC']
        testvar._determine_bar_layers_in_dataframe(dataframe='This is a string')

    # Test 7 - Too much items in compare_scenario-list (max 2 allowed)
    with pytest.raises(ValueError):
        testvar  = BarWithWaterfall(test=True)
        testvar.compare_scenarios = ['AC', 'FC', 'XC']
        dataset  = pd.DataFrame()
        testvar._determine_bar_layers_in_dataframe(dataframe=dataset)

    # Test 8 - Too less items in compare_scenario-list (min 1 allowed)
    with pytest.raises(ValueError):
        testvar  = BarWithWaterfall(test=True)
        testvar.compare_scenarios = []
        dataset  = pd.DataFrame()
        testvar._determine_bar_layers_in_dataframe(dataframe=dataset)

    # Test 9 - String instead of list
    with pytest.raises(TypeListError):
        testvar  = BarWithWaterfall(test=True)
        testvar.compare_scenarios = 'This is a string'
        dataset  = pd.DataFrame()
        testvar._determine_bar_layers_in_dataframe(dataframe=dataset)


def test__add_deltavalues_to_dataframe():
    # Test 1 - Good dataframe and one compare scenario
    dataset  = pd.DataFrame({'Year'     : ['2022', '2022', '2022', '2022'],
                             'PY'       : [32.7, 38.2, 40, 38],
                             'PL'       : [33, 38.98899, 41, 40.3],
                             '_Category': ['Airbus', 'Boeing', 'General Dynamics', 'Lockheed Martin'],
                             'AC'       : [32.25, 38, 33.6, 39],
                             'FC'       : [38.65, 32, 41, 37.1]})
    testvar  = BarWithWaterfall(test=True)
    testvar.base_scenarios = ['PL', 'PY']
    testvar.compare_scenarios = ['AC']
    expected = {'Year': ['2022', '2022', '2022', '2022'], 
                'PY': [32.7, 38.2, 40.0, 38.0], 
                'PL': [33.0, 38.98899, 41.0, 40.3], 
                '_Category': ['Airbus', 'Boeing', 'General Dynamics', 'Lockheed Martin'], 
                'AC': [32.25, 38.0, 33.6, 39.0], 
                'FC': [38.65, 32.0, 41.0, 37.1], 
                '_CBC_DELTA1': [-0.75, -0.9889900000000011, -7.399999999999999, -1.2999999999999972], 
                '_CBC_DELTA2': [0, 0, 0, 0]}
    actual   = testvar._add_deltavalues_to_dataframe(dataframe=dataset)
    actual   = actual.to_dict(orient='list')
    message  = "Test 1 - BarWithWaterfall._add_deltavalues_to_dataframe returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message

    # Test 2 - Good dataframe and one compare scenario
    dataset  = pd.DataFrame({'Year'     : ['2022', '2022', '2022', '2022'],
                             'PY'       : [32.7, 38.2, 40, 38],
                             'PL'       : [33, 38.98899, 41, 40.3],
                             '_Category': ['Airbus', 'Boeing', 'General Dynamics', 'Lockheed Martin'],
                             'AC'       : [32.25, 38, 33.6, 39],
                             'FC'       : [38.65, 32, 41, 37.1]})
    testvar  = BarWithWaterfall(test=True)
    testvar.base_scenarios = ['PL', 'PY']
    testvar.compare_scenarios = ['AC', 'FC']
    expected = {'Year': ['2022', '2022', '2022', '2022'],
                'PY': [32.7, 38.2, 40.0, 38.0],
                'PL': [33.0, 38.98899, 41.0, 40.3],
                '_Category': ['Airbus', 'Boeing', 'General Dynamics', 'Lockheed Martin'],
                'AC': [32.25, 38.0, 33.6, 39.0], 'FC': [38.65, 32.0, 41.0, 37.1], 
                '_CBC_DELTA1': [-0.75, -0.9889900000000011, -7.399999999999999, -1.2999999999999972],
                '_CBC_DELTA2': [37.9, 31.01101, 33.6, 35.800000000000004]}
    actual   = testvar._add_deltavalues_to_dataframe(dataframe=dataset)
    actual   = actual.to_dict(orient='list')
    message  = "Test 2 - BarWithWaterfall._add_deltavalues_to_dataframe returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message

    # Test 3 - String instead of dataframe
    with pytest.raises(TypeDataFrameError):
        testvar  = BarWithWaterfall(test=True)
        testvar.base_scenarios = ['PL', 'PY']
        testvar.compare_scenarios = ['AC', 'FC']
        testvar._add_deltavalues_to_dataframe(dataframe='This is a string')

    # Test 4 - Too much column names ('Month' is too much) in dataframe
    with pytest.raises(ValueError):
        dataset  = pd.DataFrame({'Year'     : ['2022', '2022', '2022', '2022'],
                                 'Month'    : ['01', '03', '07', '12'],
                                 'PY'       : [32.7, 38.2, 40, 38],
                                 'PL'       : [33, 38.98899, 41, 40.3],
                                 '_Category': ['Airbus', 'Boeing', 'General Dynamics', 'Lockheed Martin'],
                                 'AC'       : [32.25, 38, 33.6, 39],
                                 'FC'       : [38.65, 32, 41, 37.1]})
        testvar  = BarWithWaterfall(test=True)
        testvar.base_scenarios = ['PL', 'PY']
        testvar.compare_scenarios = ['AC', 'FC']
        testvar._add_deltavalues_to_dataframe(dataframe=dataset)

def test__sort_dataframe_with_other_last():
    # Test 1 - Good dataframe, OTHER has the lowest delta-value
    dataset  = pd.DataFrame({'Year'       : ['2022', '2022', '2022', '2022', '2022'],
                             'PY'         : [32.7, 38.2, 40.0, 38.0, 35.0],
                             'PL'         : [33.0, 38.9, 41.0, 40.3, 36.0],
                             '_Category'  : ['Airbus', 'Boeing', 'OTHER', 'General Dynamics', 'Lockheed Martin'],
                             'AC'         : [32.25, 38.0, 33.6, 39.0, 36.6],
                             'FC'         : [38.65, 32.0, 41.0, 37.1, 35.1],
                             '_CBC_DELTA1': [-0.75, -0.9, -7.4, -1.3, 0.6],
                             '_CBC_DELTA2': [37.9, 31.1, 33.6, 35.8, 35.7]})
    testvar  = BarWithWaterfall(test=True)
    testvar.sort_dataframe = True
    testvar.compare_scenarios = ['AC', 'FC']
    expected = {'Year'       : ['2022', '2022', '2022', '2022', '2022'],
                'PY'         : [35.0, 32.7, 38.2, 38.0, 40.0],
                'PL'         : [36.0, 33.0, 38.9, 40.3, 41.0],
                '_Category'  : ['Lockheed Martin', 'Airbus', 'Boeing', 'General Dynamics', 'OTHER'],
                'AC'         : [36.6, 32.25, 38.0, 39.0, 33.6],
                'FC'         : [35.1, 38.65, 32.0, 37.1, 41.0],
                '_CBC_DELTA1': [0.6, -0.75, -0.9, -1.3, -7.4],
                '_CBC_DELTA2': [35.7, 37.9, 31.1, 35.8, 33.6]}
    actual   = testvar._sort_dataframe_with_other_last(dataframe=dataset)
    actual   = actual.to_dict(orient='list')
    message  = "Test 1 - BarWithWaterfall._sort_dataframe_with_other_last returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message

    # Test 2 - Good dataframe, but OTHER doesn't have the lowest delta-value
    dataset  = pd.DataFrame({'Year'       : ['2022', '2022', '2022', '2022', '2022'],
                             'PY'         : [32.7, 38.2, 40.0, 38.0, 35.0],
                             'PL'         : [33.0, 38.9, 41.0, 40.3, 36.0],
                             '_Category'  : ['Airbus', 'OTHER', 'Boeing', 'General Dynamics', 'Lockheed Martin'],
                             'AC'         : [32.25, 38.0, 33.6, 39.0, 36.6],
                             'FC'         : [38.65, 32.0, 41.0, 37.1, 35.1],
                             '_CBC_DELTA1': [-0.75, -0.9, -7.4, -1.3, 0.6],
                             '_CBC_DELTA2': [37.9, 31.1, 33.6, 35.8, 35.7]})
    testvar  = BarWithWaterfall(test=True)
    testvar.sort_dataframe = True
    testvar.compare_scenarios = ['AC', 'FC']
    expected = {'Year'       : ['2022', '2022', '2022', '2022', '2022'],
                'PY'         : [35.0, 32.7, 38.0, 40.0, 38.2],
                'PL'         : [36.0, 33.0, 40.3, 41.0, 38.9],
                '_Category'  : ['Lockheed Martin', 'Airbus', 'General Dynamics', 'Boeing', 'OTHER'],
                'AC'         : [36.6, 32.25, 39.0, 33.6, 38.0],
                'FC'         : [35.1, 38.65, 37.1, 41.0, 32.0],
                '_CBC_DELTA1': [0.6, -0.75, -1.3, -7.4, -0.9],
                '_CBC_DELTA2': [35.7, 37.9, 35.8, 33.6, 31.1]}
    actual   = testvar._sort_dataframe_with_other_last(dataframe=dataset)
    actual   = actual.to_dict(orient='list')
    message  = "Test 2 - BarWithWaterfall._sort_dataframe_with_other_last returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message

    # Test 3 - Good dataframe, but don't sort the dataframe
    dataset  = pd.DataFrame({'PY'         : [32.7, 38.2, 40.0, 38.0, 35.0],
                             'PL'         : [33.0, 38.9, 41.0, 40.3, 36.0],
                             '_Category'  : ['0-30 days', '31-60 days', '61-90 days', '91-120 days', '> 120 days'],
                             'AC'         : [32.25, 38.0, 33.6, 39.0, 36.6],
                             'FC'         : [38.65, 32.0, 41.0, 37.1, 35.1],
                             '_CBC_DELTA1': [-0.75, -0.9, -7.4, -1.3, 0.6],
                             '_CBC_DELTA2': [37.9, 31.1, 33.6, 35.8, 35.7]})
    testvar  = BarWithWaterfall(test=True)
    testvar.sort_dataframe = False
    testvar.compare_scenarios = ['AC', 'FC']
    expected = {'PY'         : [32.7, 38.2, 40.0, 38.0, 35.0],
                'PL'         : [33.0, 38.9, 41.0, 40.3, 36.0],
                '_Category'  : ['0-30 days', '31-60 days', '61-90 days', '91-120 days', '> 120 days'],
                'AC'         : [32.25, 38.0, 33.6, 39.0, 36.6],
                'FC'         : [38.65, 32.0, 41.0, 37.1, 35.1],
                '_CBC_DELTA1': [-0.75, -0.9, -7.4, -1.3, 0.6],
                '_CBC_DELTA2': [37.9, 31.1, 33.6, 35.8, 35.7]}
    actual   = testvar._sort_dataframe_with_other_last(dataframe=dataset)
    actual   = actual.to_dict(orient='list')
    message  = "Test 3 - BarWithWaterfall._sort_dataframe_with_other_last returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message

    # Test 4 - String instead of dataframe
    with pytest.raises(TypeDataFrameError):
        testvar = BarWithWaterfall(test=True)
        testvar.sort_dataframe = True
        testvar.compare_scenarios = ['AC', 'FC']
        testvar._sort_dataframe_with_other_last(dataframe='This is a string')

    # Test 5 - Dataframe is missing the category-of-interest column
    with pytest.raises(ValueError):
        testvar = BarWithWaterfall(test=True)
        testvar.sort_dataframe = True
        testvar.compare_scenarios = ['AC', 'FC']
        dataset = pd.DataFrame({'Year'       : ['2022', '2022', '2022', '2022', '2022'],
                                'PY'         : [32.7, 38.2, 40.0, 38.0, 35.0],
                                'PL'         : [33.0, 38.9, 41.0, 40.3, 36.0],
                                'AC'         : [32.25, 38.0, 33.6, 39.0, 36.6],
                                'FC'         : [38.65, 32.0, 41.0, 37.1, 35.1],
                                '_CBC_DELTA1': [-0.75, -0.9, -7.4, -1.3, 0.6],
                                '_CBC_DELTA2': [37.9, 31.1, 33.6, 35.8, 35.7]})
        testvar._sort_dataframe_with_other_last(dataframe=dataset)

    # Test 6 - Dataframe is missing the delta1 column
    with pytest.raises(ValueError):
        testvar = BarWithWaterfall(test=True)
        testvar.sort_dataframe = True
        testvar.compare_scenarios = ['AC', 'FC']
        dataset = pd.DataFrame({'Year'       : ['2022', '2022', '2022', '2022', '2022'],
                                'PY'         : [32.7, 38.2, 40.0, 38.0, 35.0],
                                'PL'         : [33.0, 38.9, 41.0, 40.3, 36.0],
                                '_Category'  : ['Airbus', 'OTHER', 'Boeing', 'General Dynamics', 'Lockheed Martin'],
                                'AC'         : [32.25, 38.0, 33.6, 39.0, 36.6],
                                'FC'         : [38.65, 32.0, 41.0, 37.1, 35.1],
                                '_CBC_DELTA2': [37.9, 31.1, 33.6, 35.8, 35.7]})
        testvar._sort_dataframe_with_other_last(dataframe=dataset)

    # Test 7 - Dataframe is missing the delta2 column
    with pytest.raises(ValueError):
        testvar = BarWithWaterfall(test=True)
        testvar.sort_dataframe = True
        testvar.compare_scenarios = ['AC', 'FC']
        dataset = pd.DataFrame({'Year'       : ['2022', '2022', '2022', '2022', '2022'],
                                'PY'         : [32.7, 38.2, 40.0, 38.0, 35.0],
                                'PL'         : [33.0, 38.9, 41.0, 40.3, 36.0],
                                '_Category'  : ['Airbus', 'OTHER', 'Boeing', 'General Dynamics', 'Lockheed Martin'],
                                'AC'         : [32.25, 38.0, 33.6, 39.0, 36.6],
                                'FC'         : [38.65, 32.0, 41.0, 37.1, 35.1],
                                '_CBC_DELTA1': [-0.75, -0.9, -7.4, -1.3, 0.6]})
        testvar._sort_dataframe_with_other_last(dataframe=dataset)

    # Test 8 - Compare scenarios is not a list
    with pytest.raises(TypeListError):
        testvar = BarWithWaterfall(test=True)
        testvar.sort_dataframe = True
        testvar.compare_scenarios = 'This is a string'
        dataset = pd.DataFrame({'Year'       : ['2022', '2022', '2022', '2022', '2022'],
                                'PY'         : [32.7, 38.2, 40.0, 38.0, 35.0],
                                'PL'         : [33.0, 38.9, 41.0, 40.3, 36.0],
                                '_Category'  : ['Airbus', 'OTHER', 'Boeing', 'General Dynamics', 'Lockheed Martin'],
                                'AC'         : [32.25, 38.0, 33.6, 39.0, 36.6],
                                'FC'         : [38.65, 32.0, 41.0, 37.1, 35.1],
                                '_CBC_DELTA1': [-0.75, -0.9, -7.4, -1.3, 0.6],
                                '_CBC_DELTA2': [37.9, 31.1, 33.6, 35.8, 35.7]})
        testvar._sort_dataframe_with_other_last(dataframe=dataset)


def test__drop_zero_lines():
    # Test 1 - Good dataframe, one line with only zeros, one line with some zeros. We want to remove lines with zeros.
    dataset  = pd.DataFrame({'Year'       : ['2022', '2022', '2022', '2022', '2022'],
                             'PY'         : [32.7, 0, 0.2, 38.0, 35.0],
                             'PL'         : [33.0, 0.0, 0, 40.3, 36.0],
                             '_Category'  : ['Airbus', 'Boeing', 'OTHER', 'General Dynamics', 'Lockheed Martin'],
                             'AC'         : [32.25, 0.0, 0.0, 39.0, 36.6],
                             'FC'         : [38.65, 0, 0, 37.1, 35.1],
                             '_CBC_DELTA1': [-0.75, 0, 0, -1.3, 0.6],
                             '_CBC_DELTA2': [37.9, 0, 0, 35.8, 35.7]})
    testvar  = BarWithWaterfall(test=True)
    testvar.remove_lines_with_zeros = True
    testvar.data_scenarios = ['PY', 'PL', 'FC', 'AC']
    expected = {'Year': ['2022', '2022', '2022', '2022'],
                'PY': [32.7, 0.2, 38.0, 35.0],
                'PL': [33.0, 0.0, 40.3, 36.0],
                '_Category': ['Airbus', 'OTHER', 'General Dynamics', 'Lockheed Martin'],
                'AC': [32.25, 0.0, 39.0, 36.6],
                'FC': [38.65, 0.0, 37.1, 35.1],
                '_CBC_DELTA1': [-0.75, 0.0, -1.3, 0.6],
                '_CBC_DELTA2': [37.9, 0.0, 35.8, 35.7]}
    actual   = testvar._drop_zero_lines(dataframe=dataset)
    actual   = actual.to_dict(orient='list')
    message  = "Test 1 - BarWithWaterfall._drop_zero_lines returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message

    # Test 2 - Good dataframe, one line with only zeros, one line with some zeros. We don't want to remove lines with zeros.
    dataset  = pd.DataFrame({'Year'       : ['2022', '2022', '2022', '2022', '2022'],
                             'PY'         : [32.7, 0, 0.2, 38.0, 35.0],
                             'PL'         : [33.0, 0.0, 0, 40.3, 36.0],
                             '_Category'  : ['Airbus', 'Boeing', 'OTHER', 'General Dynamics', 'Lockheed Martin'],
                             'AC'         : [32.25, 0.0, 0.0, 39.0, 36.6],
                             'FC'         : [38.65, 0, 0, 37.1, 35.1],
                             '_CBC_DELTA1': [-0.75, 0, 0, -1.3, 0.6],
                             '_CBC_DELTA2': [37.9, 0, 0, 35.8, 35.7]})
    testvar  = BarWithWaterfall(test=True)
    testvar.remove_lines_with_zeros = False
    testvar.data_scenarios = ['PY', 'PL', 'FC', 'AC']
    expected = {'Year'       : ['2022', '2022', '2022', '2022', '2022'],
                'PY'         : [32.7, 0, 0.2, 38.0, 35.0],
                'PL'         : [33.0, 0.0, 0, 40.3, 36.0],
                '_Category'  : ['Airbus', 'Boeing', 'OTHER', 'General Dynamics', 'Lockheed Martin'],
                'AC'         : [32.25, 0.0, 0.0, 39.0, 36.6],
                'FC'         : [38.65, 0, 0, 37.1, 35.1],
                '_CBC_DELTA1': [-0.75, 0, 0, -1.3, 0.6],
                '_CBC_DELTA2': [37.9, 0, 0, 35.8, 35.7]}
    actual   = testvar._drop_zero_lines(dataframe=dataset)
    actual   = actual.to_dict(orient='list')
    message  = "Test 2 - BarWithWaterfall._drop_zero_lines returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message

    # Test 3 - String instead of dataframe
    with pytest.raises(TypeDataFrameError):
        testvar = BarWithWaterfall(test=True)
        testvar.remove_lines_with_zeros = True
        testvar.data_scenarios = ['PY', 'PL', 'FC', 'AC']
        testvar._drop_zero_lines(dataframe='This is a string')

    # Test 4 - String instead of boolean for remove_lines_with_zeros
    with pytest.raises(TypeBooleanError):
        testvar = BarWithWaterfall(test=True)
        testvar.remove_lines_with_zeros = "This is a string"
        testvar.data_scenarios = ['PY', 'PL', 'FC', 'AC']
        dataset = pd.DataFrame()
        testvar._drop_zero_lines(dataframe=dataset)

    # Test 5 - String instead of list for data_scenarios
    with pytest.raises(TypeListError):
        testvar = BarWithWaterfall(test=True)
        testvar.remove_lines_with_zeros = True
        testvar.data_scenarios = "This is a string"
        dataset = pd.DataFrame()
        testvar._drop_zero_lines(dataframe=dataset)

    # Test 6 - Empty list for data_scenarios
    with pytest.raises(ValueError):
        testvar = BarWithWaterfall(test=True)
        testvar.remove_lines_with_zeros = True
        testvar.data_scenarios = list()
        dataset = pd.DataFrame()
        testvar._drop_zero_lines(dataframe=dataset)


def test__optimize_data_get_big_total():
    # Test 1 - Good dictionary. The maximum is already a positive number
    testvar  = BarWithWaterfall(test=True)
    testvar.data_total = {'PY': 380, 'PL': -250, 'AC':4096.8192, 'FC':-2048.256}
    expected = 4096.8192
    actual   = testvar._optimize_data_get_big_total()
    message  = "Test 1 - BarWithWaterfall._optimize_data_get_big_total returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message

    # Test 2 - Good dictionary. The maximum is already a positive number
    testvar  = BarWithWaterfall(test=True)
    testvar.data_total = {'PY': 380, 'PL': -250, 'AC':4096.8192, 'FC':-16384.32768}
    expected = 16384.32768
    actual   = testvar._optimize_data_get_big_total()
    message  = "Test 2 - BarWithWaterfall._optimize_data_get_big_total returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message

    # Test 3 - String instead of dictionary for data_total
    with pytest.raises(TypeDictionaryError):
        testvar = BarWithWaterfall(test=True)
        testvar.data_total = "This is a string"
        testvar._optimize_data_get_big_total()

    # Test 4 - Empty dictionary for data_total
    with pytest.raises(ValueError):
        testvar = BarWithWaterfall(test=True)
        testvar.data_total = dict()
        testvar._optimize_data_get_big_total()

def test__optimize_data_get_big_detail():
    # Test 1 - Good dataframe with all data_scenarios
    dataset  = pd.DataFrame({'Year'       : ['2022', '2022', '2022', '2022', '2022'],
                             'PY'         : [32.7, 38.2, 40.0, 38.0, 35.0],
                             'PL'         : [33.0, 38.9, 41.0, 40.3, 36.0],
                             '_Category'  : ['Airbus', 'Boeing', 'OTHER', 'General Dynamics', 'Lockheed Martin'],
                             'AC'         : [32.25, 38.0, 33.6, 39.0, 36.6],
                             'FC'         : [38.65, 32.0, 42.0, 37.1, 35.1],
                             '_CBC_DELTA1': [-0.75, -0.9, -7.4, -1.3, 0.6],
                             '_CBC_DELTA2': [37.9, 31.1, 34.6, 35.8, 35.7]})
    testvar  = BarWithWaterfall(test=True)
    testvar.data_scenarios = ['PY', 'PL', 'FC', 'AC']
    expected = 42
    actual   = testvar._optimize_data_get_big_detail(dataframe=dataset)
    message  = "Test 1 - BarWithWaterfall._optimize_data_get_big_detail returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message

    # Test 2 - Good dataframe with not all data_scenarios
    dataset  = pd.DataFrame({'Year'       : ['2022', '2022', '2022', '2022', '2022'],
                             'PY'         : [32.7, 38.2, 40.0, 38.0, 35.0],
                             '_Category'  : ['Airbus', 'Boeing', 'OTHER', 'General Dynamics', 'Lockheed Martin'],
                             'AC'         : [32.25, 38.0, 33.6, 39.0, 36.6],
                             'FC'         : [38.65, 32.0, 42.0, 37.1, 35.1],
                             '_CBC_DELTA2': [37.9, 31.1, 34.6, 35.8, 35.7]})
    testvar  = BarWithWaterfall(test=True)
    testvar.data_scenarios = ['PY', 'PL', 'FC', 'AC']
    expected = 42
    actual   = testvar._optimize_data_get_big_detail(dataframe=dataset)
    message  = "Test 2 - BarWithWaterfall._optimize_data_get_big_detail returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message

    # Test 3 - Good dataframe with all data_scenarios, big value is a minus in the delta
    dataset  = pd.DataFrame({'Year'       : ['2022', '2022', '2022', '2022', '2022'],
                             'PY'         : [32.7, 38.2, 40.0, 38.0, 35.0],
                             'PL'         : [33.0, 38.9, 41.0, 40.3, 36.0],
                             '_Category'  : ['Airbus', 'Boeing', 'OTHER', 'General Dynamics', 'Lockheed Martin'],
                             'AC'         : [32.25, 2, 33.6, 39.0, 36.6],
                             'FC'         : [38.65, -30.0, 42.0, 37.1, 35.1],
                             '_CBC_DELTA1': [-0.75, -36.9, -7.4, -1.3, 0.6],
                             '_CBC_DELTA2': [37.9, -66.9, 34.6, 35.8, 35.7]})
    testvar  = BarWithWaterfall(test=True)
    testvar.data_scenarios = ['PY', 'PL', 'FC', 'AC']
    expected = 66.9
    actual   = testvar._optimize_data_get_big_detail(dataframe=dataset)
    message  = "Test 3 - BarWithWaterfall._optimize_data_get_big_detail returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message

    # Test 4 - String instead of dataframe
    with pytest.raises(TypeDataFrameError):
        testvar = BarWithWaterfall(test=True)
        testvar.data_scenarios = ['PY', 'PL', 'FC', 'AC']
        testvar._optimize_data_get_big_detail(dataframe='This is a string')

    # Test 5 - String instead of list
    with pytest.raises(TypeListError):
        testvar = BarWithWaterfall(test=True)
        dataset = pd.DataFrame()
        testvar.data_scenarios = "This is a string"
        testvar._optimize_data_get_big_detail(dataframe=dataset)

    # Test 6 - Empty list
    with pytest.raises(ValueError):
        testvar = BarWithWaterfall(test=True)
        dataset = pd.DataFrame()
        testvar.data_scenarios = list()
        testvar._optimize_data_get_big_detail(dataframe=dataset)


def test__optimize_data_calculate_denominator():
    # Test 1 - Good values, start with multiplier 1
    testvar = BarWithWaterfall(test=True)
    testvar.original_multiplier = Multiplier("1")
    big_detail = 12345678.921
    actual   = testvar._optimize_data_calculate_denominator(big_detail)
    expected = 1000000
    message  = "Test 1a - BarWithWaterfall._optimize_data_calculate_denominator returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message
    actual   = testvar.multiplier.get_multiplier()
    expected = 'm'
    message  = "Test 1b - BarWithWaterfall._optimize_data_calculate_denominator returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 2 - Good values, start with multiplier k
    testvar = BarWithWaterfall(test=True)
    testvar.original_multiplier = Multiplier("k")
    big_detail = 123478.921
    actual   = testvar._optimize_data_calculate_denominator(big_detail)
    expected = 1000
    message  = "Test 2a - BarWithWaterfall._optimize_data_calculate_denominator returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message
    actual   = testvar.multiplier.get_multiplier()
    expected = 'm'
    message  = "Test 2b - BarWithWaterfall._optimize_data_calculate_denominator returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 3 - Good values, start with multiplier m
    testvar = BarWithWaterfall(test=True)
    testvar.original_multiplier = Multiplier("m")
    big_detail = 178.921
    actual   = testvar._optimize_data_calculate_denominator(big_detail)
    expected = 1
    message  = "Test 3a - BarWithWaterfall._optimize_data_calculate_denominator returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message
    actual   = testvar.multiplier.get_multiplier()
    expected = 'm'
    message  = "Test 3b - BarWithWaterfall._optimize_data_calculate_denominator returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 4 - Good values, start with multiplier 1
    testvar = BarWithWaterfall(test=True)
    testvar.original_multiplier = Multiplier("1")
    big_detail = 1478.921
    actual   = testvar._optimize_data_calculate_denominator(big_detail)
    expected = 1000
    message  = "Test 4a - BarWithWaterfall._optimize_data_calculate_denominator returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message
    actual   = testvar.multiplier.get_multiplier()
    expected = 'k'
    message  = "Test 4b - BarWithWaterfall._optimize_data_calculate_denominator returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 5 - String instead of integer or float for big_detail
    with pytest.raises(TypeError):
        testvar = BarWithWaterfall(test=True)
        testvar.original_multiplier = Multiplier("1")
        big_detail = "This is a string"
        testvar._optimize_data_calculate_denominator(big_detail)

    # Test 6 - String instead of Multiplier for original_multiplier
    with pytest.raises(TypeError):
        testvar = BarWithWaterfall(test=True)
        testvar.original_multiplier = "This is a string"
        big_detail = 1
        testvar._optimize_data_calculate_denominator(big_detail) 
        
def test__optimize_data_adjust_decimals():
    # Test 1 - Good values, no decimal-influence
    testvar = BarWithWaterfall(test=True)
    testvar.force_zero_decimals = False
    testvar.force_max_one_decimals = False
    big_detail  = 12345678.921
    big_total   = 93485273.813
    denominator = 1000000
    testvar._optimize_data_adjust_decimals(big_detail, big_total, denominator)
    actual   = testvar.decimals_details
    expected = 1
    message  = "Test 1a - BarWithWaterfall._optimize_data_adjust_decimals returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message
    actual   = testvar.decimals_totals
    expected = 1
    message  = "Test 1b - BarWithWaterfall._optimize_data_adjust_decimals returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message

    # Test 2 - Good values, no decimal-influence
    testvar = BarWithWaterfall(test=True)
    testvar.force_zero_decimals = False
    testvar.force_max_one_decimals = False
    big_detail  = 12378.921
    big_total   = 193273.813
    denominator = 1000
    testvar._optimize_data_adjust_decimals(big_detail, big_total, denominator)
    actual   = testvar.decimals_details
    expected = 1
    message  = "Test 2a - BarWithWaterfall._optimize_data_adjust_decimals returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message
    actual   = testvar.decimals_totals
    expected = 0
    message  = "Test 2b - BarWithWaterfall._optimize_data_adjust_decimals returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message

    # Test 3 - Good values, no decimal-influence
    testvar = BarWithWaterfall(test=True)
    testvar.force_zero_decimals = False
    testvar.force_max_one_decimals = False
    big_detail  = 1234567.921
    big_total   = 9348523.813
    denominator = 1000000
    testvar._optimize_data_adjust_decimals(big_detail, big_total, denominator)
    actual   = testvar.decimals_details
    expected = 2
    message  = "Test 3a - BarWithWaterfall._optimize_data_adjust_decimals returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message
    actual   = testvar.decimals_totals
    expected = 2
    message  = "Test 3b - BarWithWaterfall._optimize_data_adjust_decimals returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message

    # Test 4 - Good values, no decimal-influence
    testvar = BarWithWaterfall(test=True)
    testvar.force_zero_decimals = False
    testvar.force_max_one_decimals = False
    big_detail  = 1238.921
    big_total   = 9933.813
    denominator = 1000
    testvar._optimize_data_adjust_decimals(big_detail, big_total, denominator)
    actual   = testvar.decimals_details
    expected = 2
    message  = "Test 4a - BarWithWaterfall._optimize_data_adjust_decimals returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message
    actual   = testvar.decimals_totals
    expected = 2
    message  = "Test 4b - BarWithWaterfall._optimize_data_adjust_decimals returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message

    # Test 5 - Good values, no decimal-influence
    testvar = BarWithWaterfall(test=True)
    testvar.force_zero_decimals = False
    testvar.force_max_one_decimals = False
    big_detail  = 123458.921
    big_total   = 9934563.813
    denominator = 1000
    testvar._optimize_data_adjust_decimals(big_detail, big_total, denominator)
    actual   = testvar.decimals_details
    expected = 0
    message  = "Test 5a - BarWithWaterfall._optimize_data_adjust_decimals returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message
    actual   = testvar.decimals_totals
    expected = 0
    message  = "Test 5b - BarWithWaterfall._optimize_data_adjust_decimals returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message

    # Test 6 - Good values, force_zero_decimals = True, force_max_one_decimals = False
    testvar = BarWithWaterfall(test=True)
    testvar.force_zero_decimals = True
    testvar.force_max_one_decimals = False
    big_detail  = 12345678.921
    big_total   = 93485273.813
    denominator = 1000000
    testvar._optimize_data_adjust_decimals(big_detail, big_total, denominator)
    actual   = testvar.decimals_details
    expected = 0
    message  = "Test 6a - BarWithWaterfall._optimize_data_adjust_decimals returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message
    actual   = testvar.decimals_totals
    expected = 0
    message  = "Test 6b - BarWithWaterfall._optimize_data_adjust_decimals returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message

    # Test 7 - Good values, force_zero_decimals = True, force_max_one_decimals = True
    testvar = BarWithWaterfall(test=True)
    testvar.force_zero_decimals = True
    testvar.force_max_one_decimals = True
    big_detail  = 1238.921
    big_total   = 9933.813
    denominator = 1000
    testvar._optimize_data_adjust_decimals(big_detail, big_total, denominator)
    actual   = testvar.decimals_details
    expected = 0
    message  = "Test 7a - BarWithWaterfall._optimize_data_adjust_decimals returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message
    actual   = testvar.decimals_totals
    expected = 0
    message  = "Test 7b - BarWithWaterfall._optimize_data_adjust_decimals returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message

    # Test 8 - Good values, force_zero_decimals = False, force_max_one_decimals = True
    testvar = BarWithWaterfall(test=True)
    testvar.force_zero_decimals = False
    testvar.force_max_one_decimals = True
    big_detail  = 1238.921
    big_total   = 9933.813
    denominator = 1000
    testvar._optimize_data_adjust_decimals(big_detail, big_total, denominator)
    actual   = testvar.decimals_details
    expected = 1
    message  = "Test 8a - BarWithWaterfall._optimize_data_adjust_decimals returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message
    actual   = testvar.decimals_totals
    expected = 1
    message  = "Test 8b - BarWithWaterfall._optimize_data_adjust_decimals returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message

    # Test 9 - Good values, force_zero_decimals = False, force_max_one_decimals = True
    testvar = BarWithWaterfall(test=True)
    testvar.force_zero_decimals = False
    testvar.force_max_one_decimals = True
    big_detail  = 12345678.921
    big_total   = 93485273.813
    denominator = 1000000
    testvar._optimize_data_adjust_decimals(big_detail, big_total, denominator)
    actual   = testvar.decimals_details
    expected = 1
    message  = "Test 9a - BarWithWaterfall._optimize_data_adjust_decimals returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message
    actual   = testvar.decimals_totals
    expected = 1
    message  = "Test 9b - BarWithWaterfall._optimize_data_adjust_decimals returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message

    # Test 10 - String instead of integer or float for big_detail
    with pytest.raises(TypeError):
        testvar = BarWithWaterfall(test=True)
        testvar.force_zero_decimals = False
        testvar.force_max_one_decimals = False
        big_detail  = "This is a string"
        big_total   = 1
        denominator = 1
        testvar._optimize_data_adjust_decimals(big_detail, big_total, denominator)

    # Test 11 - String instead of integer or float for big_total
    with pytest.raises(TypeError):
        testvar = BarWithWaterfall(test=True)
        testvar.force_zero_decimals = False
        testvar.force_max_one_decimals = False
        big_detail  = 1
        big_total   = "This is a string"
        denominator = 1
        testvar._optimize_data_adjust_decimals(big_detail, big_total, denominator)

    # Test 12 - String instead of integer or float for denominator
    with pytest.raises(TypeError):
        testvar = BarWithWaterfall(test=True)
        testvar.force_zero_decimals = False
        testvar.force_max_one_decimals = False
        big_detail  = 1
        big_total   = 1
        denominator = "This is a string"
        testvar._optimize_data_adjust_decimals(big_detail, big_total, denominator)

    # Test 13 - String instead of boolean for force_zero_decimals
    with pytest.raises(TypeBooleanError):
        testvar = BarWithWaterfall(test=True)
        testvar.force_zero_decimals = "This is a string"
        testvar.force_max_one_decimals = False
        big_detail  = 1
        big_total   = 1
        denominator = 1
        testvar._optimize_data_adjust_decimals(big_detail, big_total, denominator)

    # Test 14 - String instead of boolean for force_max_one_decimals
    with pytest.raises(TypeBooleanError):
        testvar = BarWithWaterfall(test=True)
        testvar.force_zero_decimals = False
        testvar.force_max_one_decimals = "This is a string"
        big_detail  = 1
        big_total   = 1
        denominator = 1
        testvar._optimize_data_adjust_decimals(big_detail, big_total, denominator)


def test__optimize_data_dataframe_details():
    # Test 1 - Good dataframe with all data_scenarios and a normal denominator
    dataset  = pd.DataFrame({'Year'       : ['2022', '2022', '2022', '2022', '2022'],
                             'PY'         : [39364.4, 39710.1, 40165.2, 38875.8, 38539.8],
                             'PL'         : [39846.8, 41769.6, 40615.4, 39770.7, 38879.1],
                             '_Category'  : ['Airbus', 'Boeing', 'OTHER', 'General Dynamics', 'Lockheed Martin'],
                             'AC'         : [40299.2, 39443.1, 41702.8, 40331.9, 41207.3],
                             'FC'         : [38389.8, 41972.8, 41420.2, 39889.2, 40879.4],
                             '_CBC_DELTA1': [  452.4, -2326.5,  1087.4,   561.2,  2328.2],     # FYI: Delta1 is AC-PL
                             '_CBC_DELTA2': [38842.2, 39646.3, 42507.6, 40450.4, 43207.6]})    # FYI: Delta2 is Delta1+FC
    testvar  = BarWithWaterfall(test=True)
    testvar.data_scenarios = ['PY', 'PL', 'FC', 'AC']
    testvar.multiplier_denominator = 1000
    expected =  {'Year'       : ['2022', '2022', '2022', '2022', '2022'],
                 'PY'         : [39.3644, 39.7101, 40.1652, 38.875800000000005, 38.5398],    # lots of decimals due to representation of values. less decimals gives errors
                 'PL'         : [39.8468, 41.7696, 40.6154, 39.7707, 38.8791],
                 '_Category'  : ['Airbus', 'Boeing', 'OTHER', 'General Dynamics', 'Lockheed Martin'],
                 'AC'         : [40.2992, 39.4431, 41.7028, 40.331900000000005, 41.207300000000004],
                 'FC'         : [38.3898, 41.9728, 41.420199999999994, 39.889199999999995, 40.879400000000004],
                 '_CBC_DELTA1': [0.45239999999999997, -2.3265, 1.0874000000000001, 0.5612, 2.3282],
                 '_CBC_DELTA2': [38.8422, 39.646300000000004, 42.5076, 40.4504, 43.2076]}
    actual   = testvar._optimize_data_dataframe_details(dataframe=dataset)
    actual   = actual.to_dict(orient='list')
    message  = "Test 1 - BarWithWaterfall._optimize_data_dataframe_details returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message

    # Test 2 - Good dataframe with not all data_scenarios and a less normal denominator
    dataset  = pd.DataFrame({'Year'       : ['2022', '2022', '2022', '2022', '2022'],
                             'PL'         : [39846.8, 41769.6, 40615.4, 39770.7, 38879.1],
                             '_Category'  : ['Airbus', 'Boeing', 'OTHER', 'General Dynamics', 'Lockheed Martin'],
                             'AC'         : [40299.2, 39443.1, 41702.8, 40331.9, 41207.3],
                             'FC'         : [38389.8, 41972.8, 41420.2, 39889.2, 40879.4],
                             '_CBC_DELTA1': [  452.4, -2326.5,  1087.4,   561.2,  2328.2],     # FYI: Delta1 is AC-PL
                             '_CBC_DELTA2': [38842.2, 39646.3, 42507.6, 40450.4, 43207.6]})    # FYI: Delta2 is Delta1+FC
    testvar  = BarWithWaterfall(test=True)
    testvar.data_scenarios = ['PL', 'FC', 'AC']
    testvar.multiplier_denominator = 300
    expected =  {'Year'       : ['2022', '2022', '2022', '2022', '2022'],
                 'PL'         : [132.82266666666666, 139.232, 135.38466666666667, 132.569, 129.597],
                 '_Category'  : ['Airbus', 'Boeing', 'OTHER', 'General Dynamics', 'Lockheed Martin'],
                 'AC'         : [134.33066666666664, 131.477, 139.00933333333333, 134.43966666666668, 137.3576666666667],
                 'FC'         : [127.96600000000001, 139.90933333333334, 138.06733333333332, 132.964, 136.26466666666667],
                 '_CBC_DELTA1': [1.508, -7.755, 3.624666666666667, 1.870666666666667, 7.760666666666666],
                 '_CBC_DELTA2': [129.474, 132.15433333333334, 141.692, 134.83466666666666, 144.02533333333332]}
    actual   = testvar._optimize_data_dataframe_details(dataframe=dataset)
    actual   = actual.to_dict(orient='list')
    message  = "Test 2 - BarWithWaterfall._optimize_data_dataframe_details returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message

    # Test 3 - Good dataframe with all data_scenarios and a less normal denominator
    dataset  = pd.DataFrame({'Year'       : ['2022', '2022', '2022', '2022', '2022'],
                             'PY'         : [39364.4, 39710.1, 40165.2, 38875.8, 38539.8],
                             'PL'         : [39846.8, 41769.6, 40615.4, 39770.7, 38879.1],
                             '_Category'  : ['Airbus', 'Boeing', 'OTHER', 'General Dynamics', 'Lockheed Martin'],
                             'AC'         : [40299.2, 39443.1, 41702.8, 40331.9, 41207.3],
                             'FC'         : [38389.8, 41972.8, 41420.2, 39889.2, 40879.4],
                             '_CBC_DELTA1': [  452.4, -2326.5,  1087.4,   561.2,  2328.2],     # FYI: Delta1 is AC-PL
                             '_CBC_DELTA2': [38842.2, 39646.3, 42507.6, 40450.4, 43207.6]})    # FYI: Delta2 is Delta1+FC
    testvar  = BarWithWaterfall(test=True)
    testvar.data_scenarios = ['PY', 'PL', 'FC', 'AC']
    testvar.multiplier_denominator = 250
    expected =  {'Year'       : ['2022', '2022', '2022', '2022', '2022'],
                 'PY'         : [157.4576, 158.8404, 160.6608, 155.50320000000002, 154.1592],
                 'PL'         : [159.3872, 167.0784, 162.4616, 159.0828, 155.5164],
                 '_Category'  : ['Airbus', 'Boeing', 'OTHER', 'General Dynamics', 'Lockheed Martin'],
                 'AC'         : [161.1968, 157.7724, 166.8112, 161.32760000000002, 164.82920000000001],
                 'FC'         : [153.5592, 167.8912, 165.68079999999998, 159.55679999999998, 163.51760000000002],
                 '_CBC_DELTA1': [1.8095999999999999, -9.306, 4.349600000000001, 2.2448, 9.3128],
                 '_CBC_DELTA2': [155.3688, 158.58520000000001, 170.0304, 161.8016, 172.8304]}
    actual   = testvar._optimize_data_dataframe_details(dataframe=dataset)
    actual   = actual.to_dict(orient='list')
    message  = "Test 3 - BarWithWaterfall._optimize_data_dataframe_details returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message

    # Test 4 - String instead of DataFrame
    with pytest.raises(TypeDataFrameError):
        dataset  = "This is a string"
        testvar  = BarWithWaterfall(test=True)
        testvar.data_scenarios = ['PY', 'PL', 'FC', 'AC']
        testvar.multiplier_denominator = 1000
        testvar._optimize_data_dataframe_details(dataframe=dataset)

    # Test 5 - String instead of list of data_scenarios
    with pytest.raises(TypeListError):
        dataset  = pd.DataFrame()
        testvar  = BarWithWaterfall(test=True)
        testvar.data_scenarios = "This is a string"
        testvar.multiplier_denominator = 1000
        testvar._optimize_data_dataframe_details(dataframe=dataset)

    # Test 6 - String instead of integer denominator
    with pytest.raises(TypeError):
        dataset  = pd.DataFrame()
        testvar  = BarWithWaterfall(test=True)
        testvar.data_scenarios = ['PY', 'PL', 'FC', 'AC']
        testvar.multiplier_denominator = "This is a string"
        testvar._optimize_data_dataframe_details(dataframe=dataset)


def test__optimize_data():
    # Just a test to see if all components still work. Those components are tested in their own test-functions.
    # Test 1 - Good dataframe with all data_scenarios and a normal denominator and 2 decimals
    dataset   = pd.DataFrame({'Year'       : ['2022', '2022', '2022', '2022', '2022'],
                              'PY'         : [39364.4, 39710.1, 40165.2, 38875.8, 38539.8],
                              'PL'         : [39846.8, 41769.6, 40615.4, 39770.7, 38879.1],
                              '_Category'  : ['Airbus', 'Boeing', 'OTHER', 'General Dynamics', 'Lockheed Martin'],
                              'AC'         : [40299.2, 39443.1, 41702.8, 40331.9, 41207.3],
                              'FC'         : [38389.8, 41972.8, 41420.2, 39889.2, 40879.4],
                              '_CBC_DELTA1': [  452.4, -2326.5,  1087.4,   561.2,  2328.2],     # FYI: Delta1 is AC-PL
                              '_CBC_DELTA2': [38842.2, 39646.3, 42507.6, 40450.4, 43207.6]})    # FYI: Delta2 is Delta1+FC
    testvar   = BarWithWaterfall(test=True)
    testvar.data_scenarios = ['PY', 'PL', 'FC', 'AC']
    testvar.data_total = {'PY':196655.3, 'PL':200881.6, 'AC':202984.3, 'FC':202551.4}
    testvar.original_multiplier = Multiplier("1")
    testvar.force_zero_decimals = False
    testvar.force_max_one_decimals = False
    testvar.scalingvalue = 38207.237138
    expected1 = {'Year': ['2022', '2022', '2022', '2022', '2022'],
                 'PY': [39.3644, 39.7101, 40.1652, 38.875800000000005, 38.5398],    # lots of decimals due to representation of values. less decimals gives errors
                 'PL': [39.8468, 41.7696, 40.6154, 39.7707, 38.8791],
                 '_Category': ['Airbus', 'Boeing', 'OTHER', 'General Dynamics', 'Lockheed Martin'],
                 'AC': [40.2992, 39.4431, 41.7028, 40.331900000000005, 41.207300000000004],
                 'FC': [38.3898, 41.9728, 41.420199999999994, 39.889199999999995, 40.879400000000004],
                 '_CBC_DELTA1': [0.45239999999999997, -2.3265, 1.0874000000000001, 0.5612, 2.3282],
                 '_CBC_DELTA2': [38.8422, 39.646300000000004, 42.5076, 40.4504, 43.2076]}
    expected2 = {'PY': 197, 'PL': 201, 'AC': 203, 'FC': 203}
    expected3 = 38
    actual1   = testvar._optimize_data(dataframe=dataset)
    actual1   = actual1.to_dict(orient='list')
    actual2   = testvar.data_total
    actual3   = testvar.scalingvalue
    message   = "Test 1a - BarWithWaterfall._optimize_data returned {0} instead of {1}".format(actual1, expected1)
    assert actual1 == pytest.approx(expected1), message
    message   = "Test 1b - BarWithWaterfall._optimize_data returned {0} instead of {1}".format(actual2, expected2)
    assert actual2 == pytest.approx(expected2), message
    message   = "Test 1c - BarWithWaterfall._optimize_data returned {0} instead of {1}".format(actual3, expected3)
    assert actual3 == pytest.approx(expected3), message


def test__add_yvalues_to_dataframe():
    # Test 1 - Good dataframe with all data_scenarios and category OTHER
    dataset  = pd.DataFrame({'Year'       : ['2022', '2022', '2022', '2022', '2022'],
                             'PY'         : [39364.4, 39710.1, 40165.2, 38875.8, 38539.8],
                             'PL'         : [39846.8, 41769.6, 40615.4, 39770.7, 38879.1],
                             '_Category'  : ['Airbus', 'Boeing', 'General Dynamics', 'Lockheed Martin', 'OTHER'],
                             'AC'         : [40299.2, 39443.1, 41702.8, 40331.9, 41207.3],
                             'FC'         : [38389.8, 41972.8, 41420.2, 39889.2, 40879.4],
                             '_CBC_DELTA1': [  452.4, -2326.5,  1087.4,   561.2,  2328.2],     # FYI: Delta1 is AC-PL
                             '_CBC_DELTA2': [38842.2, 39646.3, 42507.6, 40450.4, 43207.6]})    # FYI: Delta2 is Delta1+FC
    testvar  = BarWithWaterfall(test=True)
    testvar.barshift = 0.2
    testvar.barwidth = 0.5
    expected =  {'Year'       : ['2022', '2022', '2022', '2022', '2022'],
                 'PY'         : [39364.4, 39710.1, 40165.2, 38875.8, 38539.8],
                 'PL'         : [39846.8, 41769.6, 40615.4, 39770.7, 38879.1],
                 '_Category'  : ['Airbus', 'Boeing', 'General Dynamics', 'Lockheed Martin', 'OTHER'],
                 'AC'         : [40299.2, 39443.1, 41702.8, 40331.9, 41207.3],
                 'FC'         : [38389.8, 41972.8, 41420.2, 39889.2, 40879.4],
                 '_CBC_DELTA1': [452.4, -2326.5, 1087.4, 561.2, 2328.2],
                 '_CBC_DELTA2': [38842.2, 39646.3, 42507.6, 40450.4, 43207.6],
                 '_CBC_Y'     : [0, -1, -2, -3, -4.5],
                 '_CBC_Y1'    : [0.1, -0.9, -1.9, -2.9, -4.4],
                 '_CBC_Y2'    : [-0.1, -1.1, -2.1, -3.1, -4.6]}
    actual   = testvar._add_yvalues_to_dataframe(dataframe=dataset)
    actual   = actual.to_dict(orient='list')
    message  = "Test 1 - BarWithWaterfall._add_yvalues_to_dataframe returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message

    # Test 2 - Good dataframe with all data_scenarios without category OTHER
    dataset  = pd.DataFrame({'Year'       : ['2022', '2022', '2022', '2022', '2022'],
                             'PY'         : [39364.4, 39710.1, 40165.2, 38875.8, 38539.8],
                             'PL'         : [39846.8, 41769.6, 40615.4, 39770.7, 38879.1],
                             '_Category'  : ['Airbus', 'Boeing', 'General Dynamics', 'Lockheed Martin', 'Fokker'],
                             'AC'         : [40299.2, 39443.1, 41702.8, 40331.9, 41207.3],
                             'FC'         : [38389.8, 41972.8, 41420.2, 39889.2, 40879.4],
                             '_CBC_DELTA1': [  452.4, -2326.5,  1087.4,   561.2,  2328.2],     # FYI: Delta1 is AC-PL
                             '_CBC_DELTA2': [38842.2, 39646.3, 42507.6, 40450.4, 43207.6]})    # FYI: Delta2 is Delta1+FC
    testvar  = BarWithWaterfall(test=True)
    testvar.barshift = 0.2
    testvar.barwidth = 0.5
    expected =  {'Year'       : ['2022', '2022', '2022', '2022', '2022'],
                 'PY'         : [39364.4, 39710.1, 40165.2, 38875.8, 38539.8],
                 'PL'         : [39846.8, 41769.6, 40615.4, 39770.7, 38879.1],
                 '_Category'  : ['Airbus', 'Boeing', 'General Dynamics', 'Lockheed Martin', 'Fokker'],
                 'AC'         : [40299.2, 39443.1, 41702.8, 40331.9, 41207.3],
                 'FC'         : [38389.8, 41972.8, 41420.2, 39889.2, 40879.4],
                 '_CBC_DELTA1': [452.4, -2326.5, 1087.4, 561.2, 2328.2],
                 '_CBC_DELTA2': [38842.2, 39646.3, 42507.6, 40450.4, 43207.6],
                 '_CBC_Y'     : [0, -1, -2, -3, -4],
                 '_CBC_Y1'    : [0.1, -0.9, -1.9, -2.9, -3.9],
                 '_CBC_Y2'    : [-0.1, -1.1, -2.1, -3.1, -4.1]}
    actual   = testvar._add_yvalues_to_dataframe(dataframe=dataset)
    actual   = actual.to_dict(orient='list')
    message  = "Test 2 - BarWithWaterfall._add_yvalues_to_dataframe returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message

    # Test 3 - Good dataframe with all data_scenarios but category OTHER not on the last spot in the column
    with pytest.raises(ValueError):
        dataset  = pd.DataFrame({'Year'       : ['2022', '2022', '2022', '2022', '2022'],
                                 'PY'         : [39364.4, 39710.1, 40165.2, 38875.8, 38539.8],
                                 'PL'         : [39846.8, 41769.6, 40615.4, 39770.7, 38879.1],
                                 '_Category'  : ['Airbus', 'Boeing', 'OTHER', 'General Dynamics', 'Lockheed Martin'],
                                 'AC'         : [40299.2, 39443.1, 41702.8, 40331.9, 41207.3],
                                 'FC'         : [38389.8, 41972.8, 41420.2, 39889.2, 40879.4],
                                 '_CBC_DELTA1': [  452.4, -2326.5,  1087.4,   561.2,  2328.2],     # FYI: Delta1 is AC-PL
                                 '_CBC_DELTA2': [38842.2, 39646.3, 42507.6, 40450.4, 43207.6]})    # FYI: Delta2 is Delta1+FC
        testvar  = BarWithWaterfall(test=True)
        testvar.barshift = 0.2
        testvar.barwidth = 0.5
        testvar._add_yvalues_to_dataframe(dataframe=dataset)

    # Test 4 - String instead of DataFrame
    with pytest.raises(TypeDataFrameError):
        dataset  = "This is a string"
        testvar  = BarWithWaterfall(test=True)
        testvar.barshift = 0.2
        testvar.barwidth = 0.5
        testvar._add_yvalues_to_dataframe(dataframe=dataset)

    # Test 5 - String instead of integer or float
    with pytest.raises(TypeError):
        dataset  = pd.DataFrame()
        testvar  = BarWithWaterfall(test=True)
        testvar.barshift = "This is a string"
        testvar.barwidth = 0.5
        testvar._add_yvalues_to_dataframe(dataframe=dataset)

    # Test 6 - String instead of integer or float
    with pytest.raises(TypeError):
        dataset  = pd.DataFrame()
        testvar  = BarWithWaterfall(test=True)
        testvar.barshift = 0.2
        testvar.barwidth = "This is a string"
        testvar._add_yvalues_to_dataframe(dataframe=dataset)


def test__process_dataframe():
    # Just a test to see if all components still work. Those components are tested in their own test-functions.
    # Test 1 - Good dataframe with all data_scenarios
    dataset  = pd.DataFrame({'Year'       : ['2022', '2022', '2022', '2022', '2022'],
                             'PY'         : [39364.4, 39710.1, 40165.2, 38875.8, 38539.8],
                             'PL'         : [39846.8, 41769.6, 40615.4, 39770.7, 38879.1],
                             '_Category'  : ['Airbus', 'Boeing', 'OTHER', 'General Dynamics', 'Lockheed Martin'],
                             'AC'         : [40299.2, 39443.1, 41702.8, 40331.9, 41207.3],
                             'FC'         : [38389.8, 41972.8, 41420.2, 39889.2, 40879.4]})
    testvar  = BarWithWaterfall(test=True)
    testvar.base_scenarios = ['PL', 'PY']
    testvar.compare_scenarios = ['AC']
    testvar.remove_lines_with_zeros = False
    testvar.barwidth = 0.5
    testvar.data_scenarios = ['PY', 'PL', 'FC', 'AC']
    testvar.data_total = {'PY':196655.3, 'PL':200881.6, 'AC':202984.3, 'FC':202551.4}
    testvar.original_multiplier = Multiplier("1")
    testvar.force_zero_decimals = False
    testvar.force_max_one_decimals = False
    testvar.sort_dataframe = True
    testvar.scalingvalue = None
    expected = {'Year'         : ['2022', '2022', '2022', '2022', '2022'],
                'PY'           : [38.5398, 38.875800000000005, 39.3644, 39.7101, 40.1652],    # lots of decimals due to representation of values. less decimals gives errors
                'PL'           : [38.8791, 39.7707, 39.8468, 41.7696, 40.6154],
                '_Category'    : ['Lockheed Martin', 'General Dynamics', 'Airbus', 'Boeing', 'OTHER'],
                'AC'           : [41.207300000000004, 40.331900000000005, 40.2992, 39.4431, 41.7028],
                'FC'           : [40.879400000000004, 39.889199999999995, 38.3898, 41.9728, 41.420199999999994],
                '_CBC_TOPLAYER': ['AC', 'AC', 'AC', 'AC', 'AC'],
                '_CBC_DELTA1'  : [2.3282000000000043, 0.5612000000000044, 0.4523999999999942, -2.3265, 1.0874000000000015],
                '_CBC_DELTA2'  : [0.0, 0.0, 0.0, 0.0, 0.0],
                '_CBC_Y'       : [-0.0, -1.0, -2.0, -3.0, -4.5],
                '_CBC_Y1'      : [0.0625, -0.9375, -1.9375, -2.9375, -4.4375],
                '_CBC_Y2'      : [-0.0625, -1.0625, -2.0625, -3.0625, -4.5625]}
    actual   = testvar._process_dataframe(dataframe=dataset)
    actual   = actual.to_dict(orient='list')
    message  = "Test 1 - BarWithWaterfall._process_dataframe returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message


def test__check_and_process_data():
    # Test 1 - Good dataframe with all data_scenarios
    dataset  = pd.DataFrame({'Year'       : ['2022', '2022', '2022', '2022', '2022'],
                             'PY'         : [39364.4, 39710.1, 40165.2, 38875.8, 38539.8],
                             'PL'         : [39846.8, 41769.6, 40615.4, 39770.7, 38879.1],
                             '_Category'  : ['Airbus', 'Boeing', 'OTHER', 'General Dynamics', 'Lockheed Martin'],
                             'AC'         : [40299.2, 39443.1, 41702.8, 40331.9, 41207.3],
                             'FC'         : [38389.8, 41972.8, 41420.2, 39889.2, 40879.4]})
    testvar  = BarWithWaterfall(test=True)
    testvar.translate_headers=None
    testvar.category=None
    testvar.base_scenarios = ['PL', 'PY']
    testvar.compare_scenarios = ['AC']
    testvar.remove_lines_with_zeros = False
    testvar.barwidth = 0.5
    testvar.data_scenarios = ['PY', 'PL', 'FC', 'AC']
    testvar.data_total = {'PY':196655.3, 'PL':200881.6, 'AC':202984.3, 'FC':202551.4}
    testvar.original_multiplier = Multiplier("1")
    testvar.force_zero_decimals = False
    testvar.force_max_one_decimals = False
    testvar.sort_dataframe = True
    testvar.scalingvalue = None
    expected = {'Year'         : ['2022', '2022', '2022', '2022', '2022'],
                '_Category'    : ['Lockheed Martin', 'General Dynamics', 'Airbus', 'Boeing', 'OTHER'],
                'PY'           : [38.5398, 38.875800000000005, 39.3644, 39.7101, 40.1652],
                'PL'           : [38.8791, 39.7707, 39.8468, 41.7696, 40.6154],
                'AC'           : [41.207300000000004, 40.331900000000005, 40.2992, 39.4431, 41.7028],
                'FC'           : [40.879400000000004, 39.889199999999995, 38.3898, 41.9728, 41.420199999999994],
                '_CBC_TOPLAYER': ['AC', 'AC', 'AC', 'AC', 'AC'],
                '_CBC_DELTA1'  : [2.3282000000000043, 0.5612000000000044, 0.4523999999999942, -2.3265, 1.0874000000000015],
                '_CBC_DELTA2'  : [0.0, 0.0, 0.0, 0.0, 0.0],
                '_CBC_Y'       : [-0.0, -1.0, -2.0, -3.0, -4.5],
                '_CBC_Y1'      : [0.0625, -0.9375, -1.9375, -2.9375, -4.4375],
                '_CBC_Y2'      : [-0.0625, -1.0625, -2.0625, -3.0625, -4.5625]}
    testvar._check_and_process_data(data=dataset)
    actual   = testvar.data
    actual   = actual.to_dict(orient='list')
    message  = "Test 1 - BarWithWaterfall._check_and_process_data returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message

    # Test 2 - Dictionary
    dataset =  { 'HEADERS'      : ['PY','PL','AC','FC'],  # Special keyword 'HEADERS' to indicate the scenario of the value columns
                 'Spain'        : [ 30 , 33 , 53 ,  0 ],
                 'Greece'       : [ 38 , 33 , 39 ,  0 ],
                 'Sweden'       : [ 38 , 35 , 40 ,  0 ],
                 'Germany'      : [ 90 , 89 , 93 , 25 ],
                 'Russia'       : [ 60 , 56 , 60 ,  0 ],
                 'Italy'        : [ 15 , 12 , 14 ,  4 ],
                 'Great Britain': [ 15 , 13 , 15 ,  0 ],
                 'Slovenia'     : [  4 ,  5 ,  4 ,  0 ],
                 'Denmark'      : [ 29 , 35 , 33 , 10 ],
                 'Netherlands'  : [ 39 , 42 , 38 , 15 ],
                 'France'       : [ 60 , 77 , 63 ,  0 ],
                 'OTHER'        : [ 40 , 37 , 44 , 15 ]}  # Special keyword 'OTHERS' to indicate the row with the remaining values
    testvar  = BarWithWaterfall(test=True)
    testvar.translate_headers=None
    testvar.category=None
    testvar.base_scenarios = ['PL', 'PY']
    testvar.compare_scenarios = ['AC']
    testvar.remove_lines_with_zeros = False
    testvar.barwidth = 0.5
    testvar.data_scenarios = ['PY', 'PL', 'FC', 'AC']
    testvar.data_total = {'PY':196655.3, 'PL':200881.6, 'AC':202984.3, 'FC':202551.4}
    testvar.original_multiplier = Multiplier("1")
    testvar.force_zero_decimals = False
    testvar.force_max_one_decimals = False
    testvar.sort_dataframe = True
    testvar.scalingvalue = None
    expected = {'_Category': ['Spain', 'Greece', 'Sweden', 'Germany', 'Russia', 'Great Britain', 'Italy', 'Slovenia', 'Denmark', 'Netherlands', 'France', 'OTHER'],
                'PY': [30.0, 38.0, 38.0, 90.0, 60.0, 15.0, 15.0, 4.0, 29.0, 39.0, 60.0, 40.0],
                'PL': [33.0, 33.0, 35.0, 89.0, 56.0, 13.0, 12.0, 5.0, 35.0, 42.0, 77.0, 37.0],
                'AC': [53.0, 39.0, 40.0, 93.0, 60.0, 15.0, 14.0, 4.0, 33.0, 38.0, 63.0, 44.0],
                'FC': [0.0, 0.0, 0.0, 25.0, 0.0, 0.0, 4.0, 0.0, 10.0, 15.0, 0.0, 15.0],
                '_CBC_TOPLAYER': ['AC', 'AC', 'AC', 'AC', 'AC', 'AC', 'AC', 'AC', 'AC', 'AC', 'AC', 'AC'],
                '_CBC_DELTA1': [20.0, 6.0, 5.0, 4.0, 4.0, 2.0, 2.0, -1.0, -2.0, -4.0, -14.0, 7.0],
                '_CBC_DELTA2': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                '_CBC_Y': [0.0, -1.0, -2.0, -3.0, -4.0, -5.0, -6.0, -7.0, -8.0, -9.0, -10.0, -11.5],
                '_CBC_Y1': [0.0625, -0.9375, -1.9375, -2.9375, -3.9375, -4.9375, -5.9375, -6.9375, -7.9375, -8.9375, -9.9375, -11.4375],
                '_CBC_Y2': [-0.0625, -1.0625, -2.0625, -3.0625, -4.0625, -5.0625, -6.0625, -7.0625, -8.0625, -9.0625, -10.0625, -11.5625]}
    testvar._check_and_process_data(data=dataset)
    actual   = testvar.data
    actual   = actual.to_dict(orient='list')
    message  = "Test 2 - BarWithWaterfall._check_and_process_data returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message

    # Test 3 - String
    dataset =  """

HEADERS,PY,PL,AC,FC
Spain,30 , 33 , 53 ,  0 
Greece, 38 , 33 , 39 ,  0 
Sweden, 38 , 35 , 40 ,  0 
Germany, 90 , 89 , 93 , 25 


Russia, 60 , 56 , 60 ,  0 
Italy,15 , 12 , 14 ,  4 
Great Britain, 15 , 13 , 15 ,  0
Slovenia, 4 ,  5 ,  4 ,  0
Denmark, 29 , 35 , 33 , 10
Netherlands, 39 , 42 , 38 , 15
France, 60 , 77 , 63 ,  0
OTHER, 40 , 37 , 44 , 15 

    
"""
    testvar  = BarWithWaterfall(test=True)
    testvar.translate_headers=None
    testvar.category=None
    testvar.base_scenarios = ['PL', 'PY']
    testvar.compare_scenarios = ['AC']
    testvar.remove_lines_with_zeros = False
    testvar.barwidth = 0.5
    testvar.data_scenarios = ['PY', 'PL', 'FC', 'AC']
    testvar.data_total = {'PY':196655.3, 'PL':200881.6, 'AC':202984.3, 'FC':202551.4}
    testvar.original_multiplier = Multiplier("1")
    testvar.force_zero_decimals = False
    testvar.force_max_one_decimals = False
    testvar.sort_dataframe = True
    testvar.scalingvalue = None
    expected = {'_Category': ['Spain', 'Greece', 'Sweden', 'Germany', 'Russia', 'Great Britain', 'Italy', 'Slovenia', 'Denmark', 'Netherlands', 'France', 'OTHER'],
                'PY': [30.0, 38.0, 38.0, 90.0, 60.0, 15.0, 15.0, 4.0, 29.0, 39.0, 60.0, 40.0],
                'PL': [33.0, 33.0, 35.0, 89.0, 56.0, 13.0, 12.0, 5.0, 35.0, 42.0, 77.0, 37.0],
                'AC': [53.0, 39.0, 40.0, 93.0, 60.0, 15.0, 14.0, 4.0, 33.0, 38.0, 63.0, 44.0],
                'FC': [0.0, 0.0, 0.0, 25.0, 0.0, 0.0, 4.0, 0.0, 10.0, 15.0, 0.0, 15.0],
                '_CBC_TOPLAYER': ['AC', 'AC', 'AC', 'AC', 'AC', 'AC', 'AC', 'AC', 'AC', 'AC', 'AC', 'AC'],
                '_CBC_DELTA1': [20.0, 6.0, 5.0, 4.0, 4.0, 2.0, 2.0, -1.0, -2.0, -4.0, -14.0, 7.0],
                '_CBC_DELTA2': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                '_CBC_Y': [0.0, -1.0, -2.0, -3.0, -4.0, -5.0, -6.0, -7.0, -8.0, -9.0, -10.0, -11.5],
                '_CBC_Y1': [0.0625, -0.9375, -1.9375, -2.9375, -3.9375, -4.9375, -5.9375, -6.9375, -7.9375, -8.9375, -9.9375, -11.4375],
                '_CBC_Y2': [-0.0625, -1.0625, -2.0625, -3.0625, -4.0625, -5.0625, -6.0625, -7.0625, -8.0625, -9.0625, -10.0625, -11.5625]}
    testvar._check_and_process_data(data=dataset)
    actual   = testvar.data
    actual   = actual.to_dict(orient='list')
    message  = "Test 2 - BarWithWaterfall._check_and_process_data returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message


def test__convert_data_dictionary_to_pandas_dataframe():
    # Test 1 - Dictionary with 'HEADERS'
    dataset =  { 'HEADERS' : ['PY','PL','AC','FC'],  # Special keyword 'HEADERS' to indicate the scenario of the value columns
                 'Spain'   : [ 30 , 33 , 53 ,  0 ],
                 'Greece'  : [ 38 , 33 , 39 ,  0 ]}

    testvar  = BarWithWaterfall(test=True)
    expected = {'index': ['Spain', 'Greece'], 'PY': [30, 38], 'PL': [33, 33], 'AC': [53, 39], 'FC': [0, 0]}
    actual   = testvar._convert_data_dictionary_to_pandas_dataframe(data=dataset)
    actual   = actual.to_dict(orient='list')
    message  = "Test 1 - BarWithWaterfall._convert_data_dictionary_to_pandas_dataframe returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message

    # Test 2 - String instead of dictionary
    with pytest.raises(TypeDictionaryError):
        dataset  = "This is a string"
        testvar  = BarWithWaterfall(test=True)
        testvar._convert_data_dictionary_to_pandas_dataframe(data=dataset)

    # Test 3 - Dictionary without 'HEADERS'
    with pytest.raises(ValueError):
        dataset  = { 'Spain'   : [ 30 , 33 , 53 ,  0 ],
                     'Germany' : [ 90 , 89 , 93 , 25 ]}
        testvar2  = BarWithWaterfall(test=True)
        testvar2._convert_data_dictionary_to_pandas_dataframe(data=dataset)


def test__check_figsize():
    # Test 1 - figsize = None
    testvar  = BarWithWaterfall(test=True)
    testvar.figsize = None
    expected = 8
    actual   = testvar._check_figsize()
    message  = "Test 1 - BarWithWaterfall._check_figsize returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message

    # Test 2 - figsize = list with 2 values
    testvar  = BarWithWaterfall(test=True)
    testvar.figsize = [5,6]
    expected = (5,6)
    actual   = testvar._check_figsize()
    message  = "Test 2 - BarWithWaterfall._check_figsize returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message

    # Test 3 - figsize = tuple with 2 values
    testvar  = BarWithWaterfall(test=True)
    testvar.figsize = (9,7)
    expected = (9,7)
    actual   = testvar._check_figsize()
    message  = "Test 3 - BarWithWaterfall._check_figsize returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message

    # Test 4 - figsize = float
    testvar  = BarWithWaterfall(test=True)
    testvar.figsize = 11.3
    expected = 11.3
    actual   = testvar._check_figsize()
    message  = "Test 4 - BarWithWaterfall._check_figsize returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message

    # Test 5 - figsize = integer
    testvar  = BarWithWaterfall(test=True)
    testvar.figsize = 12
    expected = 12
    actual   = testvar._check_figsize()
    message  = "Test 5 - BarWithWaterfall._check_figsize returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message

    # Test 6 - String instead of list/tuple or integer/float
    with pytest.raises(TypeTupleError):
        testvar  = BarWithWaterfall(test=True)
        testvar.figsize = "This is a string"
        testvar._check_figsize()

    # Test 7 - Float value of 0
    with pytest.raises(ValueError):
        testvar  = BarWithWaterfall(test=True)
        testvar.figsize = 0.0
        testvar._check_figsize()

    # Test 8 - List with 3 values
    with pytest.raises(ValueError):
        testvar  = BarWithWaterfall(test=True)
        testvar.figsize = [1, 2, 3]
        testvar._check_figsize()

    # Test 9 - Tuple with 1 value
    with pytest.raises(ValueError):
        testvar  = BarWithWaterfall(test=True)
        testvar.figsize = tuple([1])
        testvar._check_figsize()

    # Test 10 - Tuple with 2 value, one value is < 0
    with pytest.raises(ValueError):
        testvar  = BarWithWaterfall(test=True)
        testvar.figsize = (10, -10)
        testvar._check_figsize()

    # Test 11 - Tuple with 2 value and fig has a value
    with pytest.raises(ValueError):
        testvar  = BarWithWaterfall(test=True)
        testvar.figsize = (11, 12)
        testvar.fig = "Just a value is enough"
        testvar._check_figsize()

    # Test 12 - Tuple with 2 value and ax has a value
    with pytest.raises(ValueError):
        testvar  = BarWithWaterfall(test=True)
        testvar.figsize = (11, 12)
        testvar.ax = "Just a value is enough"
        testvar._check_figsize()


def test__make_subplots():
    # Test 1 - Dataframe with 5 rows
    dataset  = pd.DataFrame({'Year'       : ['2022', '2022', '2022', '2022', '2022'],
                             'PY'         : [39364.4, 39710.1, 40165.2, 38875.8, 38539.8],
                             'PL'         : [39846.8, 41769.6, 40615.4, 39770.7, 38879.1],
                             '_Category'  : ['Airbus', 'Boeing', 'OTHER', 'General Dynamics', 'Lockheed Martin'],
                             'AC'         : [40299.2, 39443.1, 41702.8, 40331.9, 41207.3],
                             'FC'         : [38389.8, 41972.8, 41420.2, 39889.2, 40879.4]})
    testvar  = BarWithWaterfall(test=True)
    testvar.data = dataset
    testvar.figsize = None   # Not a given figure size (default value of this parameter)
    testvar.base_scenarios = ['PY', 'PL']  # Test with 2 base-scenarios
    testvar.title = None     # No title (default value of this parameter)
    testvar._make_subplots()
    expected = [8, 4.29]
    actual   = list(testvar.fig.get_size_inches())
    message  = "Test 1a - BarWithWaterfall._make_subplots returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message
    expected = 72
    actual   = testvar.fig.dpi
    message  = "Test 1b - BarWithWaterfall._make_subplots returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message

    # Test 2 - Dataframe with 3 rows
    dataset  = pd.DataFrame({'Year'       : ['2022', '2022', '2022'],
                             'PY'         : [39364.4, 39710.1, 40165.2],
                             'PL'         : [39846.8, 41769.6, 40615.4],
                             '_Category'  : ['Airbus', 'Boeing', 'OTHER'],
                             'AC'         : [40299.2, 39443.1, 41702.8],
                             'FC'         : [38389.8, 41972.8, 41420.2]})
    testvar  = BarWithWaterfall(test=True)
    testvar.data = dataset
    testvar.figsize = None   # Not a given figure size (default value of this parameter)
    testvar.base_scenarios = ['PY', 'PL']  # Test with 2 base-scenarios
    testvar.title = None     # No title (default value of this parameter)
    testvar._make_subplots()
    expected = [8, 3.53]
    actual   = list(testvar.fig.get_size_inches())
    message  = "Test 2a - BarWithWaterfall._make_subplots returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message
    expected = 72
    actual   = testvar.fig.dpi
    message  = "Test 2b - BarWithWaterfall._make_subplots returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message

    # Test 3 - String instead of dataframe
    with pytest.raises(TypeDataFrameError):
        testvar  = BarWithWaterfall(test=True)
        testvar.data = "This is a string"
        testvar.figsize = None   # Not a given figure size (default value of this parameter)
        testvar._make_subplots()


def test__check_base_scenario_totals():
    # Test 1 - Two base scenarios, PY < PL
    testvar  = BarWithWaterfall(test=True)
    testvar.all_scenarios = ['PY', 'PL', 'AC', 'FC']
    testvar.base_scenarios = ['PL', 'PY']
    testvar.data_total = {'PY': 220, 'PL': 250, 'AC': 235, 'FC': 30}
    testvar.barshift_value = 2.5
    expected1 = ['PY', 'PL']
    expected2 = 2.5
    expected3 = True
    expected4 = False
    actual1, actual2, actual3, actual4 = testvar._check_base_scenario_totals()
    message  = "Test 1a - BarWithWaterfall._check_base_scenario_totals() returned {0} instead of {1}".format(actual1, expected1)
    assert actual1 == pytest.approx(expected1), message
    message  = "Test 1b - BarWithWaterfall._check_base_scenario_totals() returned {0} instead of {1}".format(actual2, expected2)
    assert actual2 == pytest.approx(expected2), message
    message  = "Test 1c - BarWithWaterfall._check_base_scenario_totals() returned {0} instead of {1}".format(actual3, expected3)
    assert actual3 == pytest.approx(expected3), message
    message  = "Test 1d - BarWithWaterfall._check_base_scenario_totals() returned {0} instead of {1}".format(actual4, expected4)
    assert actual4 == pytest.approx(expected4), message

    # Test 2 - Two base scenarios, PY > PL*1.1
    testvar  = BarWithWaterfall(test=True)
    testvar.all_scenarios = ['PY', 'PL', 'AC', 'FC']
    testvar.base_scenarios = ['PL', 'PY']
    testvar.data_total = {'PY': 250, 'PL': 220, 'AC': 235, 'FC': 30}
    testvar.barshift_value = 3.5
    expected1 = ['PY', 'PL']
    expected2 = 3.5
    expected3 = False
    expected4 = True
    actual1, actual2, actual3, actual4 = testvar._check_base_scenario_totals()
    message  = "Test 2a - BarWithWaterfall._check_base_scenario_totals() returned {0} instead of {1}".format(actual1, expected1)
    assert actual1 == pytest.approx(expected1), message
    message  = "Test 2b - BarWithWaterfall._check_base_scenario_totals() returned {0} instead of {1}".format(actual2, expected2)
    assert actual2 == pytest.approx(expected2), message
    message  = "Test 2c - BarWithWaterfall._check_base_scenario_totals() returned {0} instead of {1}".format(actual3, expected3)
    assert actual3 == pytest.approx(expected3), message
    message  = "Test 2d - BarWithWaterfall._check_base_scenario_totals() returned {0} instead of {1}".format(actual4, expected4)
    assert actual4 == pytest.approx(expected4), message

    # Test 3 - Two base scenarios, PY > PL AND PY < PL*1.1
    testvar  = BarWithWaterfall(test=True)
    testvar.all_scenarios = ['PY', 'PL', 'AC', 'FC']
    testvar.base_scenarios = ['PL', 'PY']
    testvar.data_total = {'PY': 250, 'PL': 230, 'AC': 235, 'FC': 30}
    testvar.barshift_value = 0.235
    expected1 = ['PY', 'PL']
    expected2 = 0.235
    expected3 = True
    expected4 = True
    actual1, actual2, actual3, actual4 = testvar._check_base_scenario_totals()
    message  = "Test 3a - BarWithWaterfall._check_base_scenario_totals() returned {0} instead of {1}".format(actual1, expected1)
    assert actual1 == pytest.approx(expected1), message
    message  = "Test 3b - BarWithWaterfall._check_base_scenario_totals() returned {0} instead of {1}".format(actual2, expected2)
    assert actual2 == pytest.approx(expected2), message
    message  = "Test 3c - BarWithWaterfall._check_base_scenario_totals() returned {0} instead of {1}".format(actual3, expected3)
    assert actual3 == pytest.approx(expected3), message
    message  = "Test 3d - BarWithWaterfall._check_base_scenario_totals() returned {0} instead of {1}".format(actual4, expected4)
    assert actual4 == pytest.approx(expected4), message

    # Test 4 - One base scenarios
    testvar  = BarWithWaterfall(test=True)
    testvar.all_scenarios = ['PY', 'PL', 'AC', 'FC']
    testvar.base_scenarios = ['FC']
    testvar.data_total = {'PY': 220, 'PL': 250, 'AC': 235, 'FC': 30}
    testvar.barshift_value = 1.5
    expected1 = ['FC']
    expected2 = 0
    expected3 = False
    expected4 = True
    actual1, actual2, actual3, actual4 = testvar._check_base_scenario_totals()
    message  = "Test 4a - BarWithWaterfall._check_base_scenario_totals() returned {0} instead of {1}".format(actual1, expected1)
    assert actual1 == pytest.approx(expected1), message
    message  = "Test 4b - BarWithWaterfall._check_base_scenario_totals() returned {0} instead of {1}".format(actual2, expected2)
    assert actual2 == pytest.approx(expected2), message
    message  = "Test 4c - BarWithWaterfall._check_base_scenario_totals() returned {0} instead of {1}".format(actual3, expected3)
    assert actual3 == pytest.approx(expected3), message
    message  = "Test 4d - BarWithWaterfall._check_base_scenario_totals() returned {0} instead of {1}".format(actual4, expected4)
    assert actual4 == pytest.approx(expected4), message

    # Test 5 - String instead of list of all scenarios
    with pytest.raises(TypeListError):
        testvar = BarWithWaterfall(test=True)
        testvar.all_scenarios = "This is a string"
        testvar.base_scenarios = ['PL']
        testvar.data_total = {'PY': 220, 'PL': 250, 'AC': 235, 'FC': 30}
        testvar._check_base_scenario_totals()
 
    # Test 6 - String instead of list of base scenarios
    with pytest.raises(TypeListError):
        testvar = BarWithWaterfall(test=True)
        testvar.all_scenarios = ['PY', 'PL', 'AC', 'FC']
        testvar.base_scenarios = "This is a string"
        testvar.data_total = {'PY': 220, 'PL': 250, 'AC': 235, 'FC': 30}
        testvar._check_base_scenario_totals()

    # Test 7 - String instead of dictionary
    with pytest.raises(TypeDictionaryError):
        testvar = BarWithWaterfall(test=True)
        testvar.all_scenarios = ['PY', 'PL', 'AC', 'FC']
        testvar.base_scenarios = ['PY']
        testvar.data_total = "This is a string"
        testvar._check_base_scenario_totals()


def test__fill_ax_bar_label():
    # Test 1 - Dataframe with 4 rows, 2 decimals and no total indicator
    dataset  = pd.DataFrame({'Year'       : ['2021', '2021', '2021', '2021'],
                             '_Category'  : ['Car', 'Bike', 'Boat', 'Plane'],
                             'AC'         : [350.506, 275.497, 425, 335.987654]})
    testvar  = BarWithWaterfall(test=True)
    testvar.data = dataset   # data is necessary for the make_subplots
    testvar.figsize = None   # Not a given figure size (default value of this parameter)
    testvar.base_scenarios = ['PY', 'PL']  # Test with 2 base-scenarios
    testvar.title = None     # No title (default value of this parameter)
    testvar._make_subplots() # make_subplots is necessary to have an "ax"-object
    testvar.data_scenarios = ['AC']
    testvar.ax.barh(y=list(dataset['_Category']), width=list(dataset['AC']), left=0)
    testvar.data_text['AC'] = len(testvar.ax.containers)-1
    testvar.decimals_details = 2
    actual   = testvar._fill_ax_bar_label('AC')
    expected = ["350.51", "275.50", "425.00", "335.99"]
    for item, actual_item, expected_item in zip(["a", "b", "c", "d"], actual, expected):
        message  = "Test 1{0} - BarWithWaterfall._check_base_scenario_totals() returned {1} instead of {2}".format(item, actual_item._text, expected_item)
        assert actual_item._text == pytest.approx(expected_item), message

    # Test 2 - Dataframe with 4 rows, 1 decimal and total indicator
    dataset  = pd.DataFrame({'Year'       : ['2021', '2021', '2021', '2021'],
                             '_Category'  : ['Car', 'Bike', 'Boat', 'Plane'],
                             'AC'         : [350.506, 275.497, 425, 335.987654]})
    testvar  = BarWithWaterfall(test=True)
    testvar.data = dataset   # data is necessary for the make_subplots
    testvar.figsize = None   # Not a given figure size (default value of this parameter)
    testvar.base_scenarios = ['PY']  # Test with one base-scenario
    testvar.title = None     # No title (default value of this parameter)
    testvar._make_subplots() # make_subplots is necessary to have an "ax"-object
    testvar.data_scenarios = ['AC']
    testvar.ax.barh(y=list(dataset['_Category']), width=list(dataset['AC']), left=0)
    testvar.data_text['ACTOT'] = len(testvar.ax.containers)-1
    testvar.decimals_totals = 1
    actual   = testvar._fill_ax_bar_label('AC', total=True)
    expected = ["350.5", "275.5", "425.0", "336.0"]
    for item, actual_item, expected_item in zip(["a", "b", "c", "d"], actual, expected):
        message  = "Test 2{0} - BarWithWaterfall._check_base_scenario_totals() returned {1} instead of {2}".format(item, actual_item._text, expected_item)
        assert actual_item._text == pytest.approx(expected_item), message

    # Test 3 - None as Axes-object
    with pytest.raises(TypeAxesError):
        testvar = BarWithWaterfall(test=True)
        testvar.ax = None
        testvar.data_scenarios = ['AC']
        testvar._fill_ax_bar_label('AC', total=True)

    # Test 4 - Integer as scenario
    with pytest.raises(TypeStringError):
        testvar = BarWithWaterfall(test=True)
        testvar.data = pd.DataFrame()
        testvar.figsize = None   # Not a given figure size (default value of this parameter)
        testvar.base_scenarios = ['PY', 'PL']  # Test with 2 base-scenarios
        testvar.title = None     # No title (default value of this parameter)
        testvar._make_subplots() # make_subplots is necessary to have an "ax"-object
        testvar.data_scenarios = ['AC']
        testvar._fill_ax_bar_label(scenario=404, total=True)

    # Test 5 - String not in list
    with pytest.raises(ValueError):
        testvar = BarWithWaterfall(test=True)
        testvar.data = pd.DataFrame()
        testvar.figsize = None   # Not a given figure size (default value of this parameter)
        testvar.base_scenarios = ['PY']  # Test with 1 base-scenario
        testvar.title = None     # No title (default value of this parameter)
        testvar._make_subplots() # make_subplots is necessary to have an "ax"-object
        testvar.data_scenarios = ['AC']
        testvar._fill_ax_bar_label(scenario='PY', total=False)

    # Test 6 - Integer instead of boolean
    with pytest.raises(TypeBooleanError):
        testvar = BarWithWaterfall(test=True)
        testvar.data = pd.DataFrame()
        testvar.figsize = None   # Not a given figure size (default value of this parameter)
        testvar.base_scenarios = ['PY', 'PL']  # Test with 2 base-scenarios
        testvar.title = None     # No title (default value of this parameter)
        testvar._make_subplots() # make_subplots is necessary to have an "ax"-object
        testvar.data_scenarios = ['AC']
        testvar._fill_ax_bar_label(scenario='AC', total=404)


def test__prepare_delta_bar():
    # Test 1 - Complete dataframe with delta-columns
    dataset =  pd.DataFrame({'_Category'    : ['Spain', 'Greece', 'Sweden', 'Germany', 'Russia', 'Great Britain', 'Italy', 'Slovenia', 'Denmark', 'Netherlands', 'France', 'OTHER'],
                             'PY'           : [30, 38, 38, 90, 60, 15, 15, 4, 29, 39, 60, 40],
                             'PL'           : [33, 33, 35, 89, 56, 13, 12, 5, 35, 42, 77, 37],
                             'AC'           : [53, 39, 40, 93, 60, 15, 14, 4, 33, 38, 63, 44],
                             'FC'           : [0, 0, 0, 25, 0, 0, 4, 0, 10, 15, 0, 15],
                             '_CBC_TOPLAYER': ['AC', 'AC', 'AC', 'AC', 'AC', 'AC', 'AC', 'AC', 'AC', 'AC', 'AC', 'AC'],
                             '_CBC_DELTA1'  : [20, 6, 5, 4, 4, 2, 2, -1, -2, -4, -14, 7],
                             '_CBC_DELTA2'  : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             '_CBC_Y'       : [0.0, -1.0, -2.0, -3.0, -4.0, -5.0, -6.0, -7.0, -8.0, -9.0, -10.0, -11.5],
                             '_CBC_Y1'      : [0.08125, -0.91875, -1.91875, -2.91875, -3.91875, -4.91875, -5.91875, -6.91875, -7.91875, -8.91875, -9.91875, -11.41875],
                             '_CBC_Y2'      : [-0.08125, -1.08125, -2.08125, -3.08125, -4.08125, -5.08125, -6.08125, -7.08125, -8.08125, -9.08125, -10.08125, -11.58125]})
    testvar  = BarWithWaterfall(test=True)
    testvar.base_scenarios = ['PL', 'PY']
    testvar.dict_totals = {'PL':{'total':467}}
    expected = {'_Category'    : ['Spain', 'Greece', 'Sweden', 'Germany', 'Russia', 'Great Britain', 'Italy', 'Slovenia', 'Denmark', 'Netherlands', 'France', 'OTHER'],
                'PY'           : [30, 38, 38, 90, 60, 15, 15, 4, 29, 39, 60, 40],
                'PL'           : [33, 33, 35, 89, 56, 13, 12, 5, 35, 42, 77, 37],
                'AC'           : [53, 39, 40, 93, 60, 15, 14, 4, 33, 38, 63, 44],
                'FC'           : [0, 0, 0, 25, 0, 0, 4, 0, 10, 15, 0, 15],
                '_CBC_TOPLAYER': ['AC', 'AC', 'AC', 'AC', 'AC', 'AC', 'AC', 'AC', 'AC', 'AC', 'AC', 'AC'],
                '_CBC_DELTA1'  : [20, 6, 5, 4, 4, 2, 2, -1, -2, -4, -14, 7],
                '_CBC_DELTA2'  : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                '_CBC_Y'       : [0.0, -1.0, -2.0, -3.0, -4.0, -5.0, -6.0, -7.0, -8.0, -9.0, -10.0, -11.5],
                '_CBC_Y1'      : [0.08125, -0.91875, -1.91875, -2.91875, -3.91875, -4.91875, -5.91875, -6.91875, -7.91875, -8.91875, -9.91875, -11.41875],
                '_CBC_Y2'      : [-0.08125, -1.08125, -2.08125, -3.08125, -4.08125, -5.08125, -6.08125, -7.08125, -8.08125, -9.08125, -10.08125, -11.58125],
                '_CBC_BASE'    : [487.0, 493.0, 498.0, 502.0, 506.0, 508.0, 510.0, 509.0, 507.0, 503.0, 489.0, 496.0]}
    actual   = testvar._prepare_delta_bar(dataframe=dataset)
    actual   = actual.to_dict(orient='list')
    message  = "Test 1 - BarWithWaterfall._prepare_delta_bar returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message

    # Test 2 - String instead of DataFrame
    with pytest.raises(TypeDataFrameError):
        testvar = BarWithWaterfall(test=True)
        testvar.base_scenarios = ['PL', 'PY']
        testvar.dict_totals = {'PL':{'total':250}}
        testvar._prepare_delta_bar(dataframe='This is a string')

    # Test 3 - DataFrame with missing delta2
    with pytest.raises(ValueError):
        dataset =  pd.DataFrame({'_Category'    : ['Spain', 'Greece'],
                                 'PY'           : [30, 38],
                                 'PL'           : [33, 33],
                                 'AC'           : [53, 39],
                                 'FC'           : [0, 0],
                                 '_CBC_TOPLAYER': ['AC', 'AC'],
                                 '_CBC_DELTA1'  : [20, 6],
                                 '_CBC_Y'       : [0.0, -1.0],
                                 '_CBC_Y1'      : [0.08125, -0.91875],
                                 '_CBC_Y2'      : [-0.08125, -1.08125]})
        testvar = BarWithWaterfall(test=True)
        testvar.base_scenarios = ['PL', 'PY']
        testvar.dict_totals = {'PL':{'total':66}}
        testvar._prepare_delta_bar(dataframe=dataset)

    # Test 4 - String instead of list base scenario
    with pytest.raises(TypeListError):
        dataset = pd.DataFrame({'_CBC_DELTA1':[10, 15], '_CBC_DELTA2':[20,25]})
        testvar = BarWithWaterfall(test=True)
        testvar.base_scenarios = 'This is a string'
        testvar.dict_totals = {'PL':{'total':250}}
        testvar._prepare_delta_bar(dataframe=dataset)

    # Test 5 - List base scenario is empty
    with pytest.raises(ValueError):
        dataset = pd.DataFrame({'_CBC_DELTA1':[10, 15], '_CBC_DELTA2':[20,25]})
        testvar = BarWithWaterfall(test=True)
        testvar.base_scenarios = []
        testvar.dict_totals = {'PL':{'total':250}}
        testvar._prepare_delta_bar(dataframe=dataset)

    # Test 6 - String instead of dictionary
    with pytest.raises(TypeDictionaryError):
        dataset = pd.DataFrame({'_CBC_DELTA1':[10, 15], '_CBC_DELTA2':[20,25]})
        testvar = BarWithWaterfall(test=True)
        testvar.base_scenarios = ['PL', 'PY']
        testvar.dict_totals = 'This is a string'
        testvar._prepare_delta_bar(dataframe=dataset)

    # Test 7 - Dictionary missing values
    with pytest.raises(ValueError):
        dataset = pd.DataFrame({'_CBC_DELTA1':[10, 15], '_CBC_DELTA2':[20,25]})
        testvar = BarWithWaterfall(test=True)
        testvar.base_scenarios = ['PL', 'PY']
        testvar.dict_totals = {'AC':{'total':250}}
        testvar._prepare_delta_bar(dataframe=dataset)


def test__determine_y_ax_category_labels():
    # Test 1 - Dataframe with needed-columns and no replacement-text
    dataset =  pd.DataFrame({'_Category' : ['Spain', 'Greece', 'Sweden', 'Germany', 'Russia', 'Great Britain', 'Italy', 'Slovenia', 'Denmark', 'Netherlands', 'France', 'OTHER'],
                             '_CBC_Y2'   : [-0.08125, -1.08125, -2.08125, -3.08125, -4.08125, -5.08125, -6.08125, -7.08125, -8.08125, -9.08125, -10.08125, -11.58125]})
    testvar  = BarWithWaterfall(test=True)
    testvar.other_text = None
    expected1 = [-0.08125, -1.08125, -2.08125, -3.08125, -4.08125, -5.08125, -6.08125, -7.08125, -8.08125, -9.08125, -10.08125, -11.58125]
    expected2 = ['Spain', 'Greece', 'Sweden', 'Germany', 'Russia', 'Great Britain', 'Italy', 'Slovenia', 'Denmark', 'Netherlands', 'France', 'OTHER']
    actual1, actual2   = testvar._determine_y_ax_category_labels(dataframe=dataset)
    message  = "Test 1a - BarWithWaterfall._determine_y_ax_category_labels returned {0} instead of {1}".format(actual1, expected1)
    assert actual1 == pytest.approx(expected1), message
    message  = "Test 1b - BarWithWaterfall._determine_y_ax_category_labels returned {0} instead of {1}".format(actual2, expected2)
    assert actual2 == pytest.approx(expected2), message

    # Test 2 - Dataframe with needed-columns with replacement-text
    dataset =  pd.DataFrame({'_Category' : ['Spain', 'Greece', 'Sweden', 'Germany', 'Russia', 'Great Britain', 'Italy', 'Slovenia', 'Denmark', 'Netherlands', 'France', 'OTHER'],
                             '_CBC_Y2'   : [-0.08125, -1.08125, -2.08125, -3.08125, -4.08125, -5.08125, -6.08125, -7.08125, -8.08125, -9.08125, -10.08125, -11.58125]})
    testvar  = BarWithWaterfall(test=True)
    testvar.other_text = "Rest of Europe"
    expected1 = [-0.08125, -1.08125, -2.08125, -3.08125, -4.08125, -5.08125, -6.08125, -7.08125, -8.08125, -9.08125, -10.08125, -11.58125]
    expected2 = ['Spain', 'Greece', 'Sweden', 'Germany', 'Russia', 'Great Britain', 'Italy', 'Slovenia', 'Denmark', 'Netherlands', 'France', 'Rest of Europe']
    actual1, actual2   = testvar._determine_y_ax_category_labels(dataframe=dataset)
    message  = "Test 2a - BarWithWaterfall._determine_y_ax_category_labels returned {0} instead of {1}".format(actual1, expected1)
    assert actual1 == pytest.approx(expected1), message
    message  = "Test 2b - BarWithWaterfall._determine_y_ax_category_labels returned {0} instead of {1}".format(actual2, expected2)
    assert actual2 == pytest.approx(expected2), message

    # Test 3 - DataFrame with one column missing
    with pytest.raises(ValueError):
        dataset = pd.DataFrame({'_Category':['A', 'B'], '_CBC_Y1':[20, 25]})
        testvar = BarWithWaterfall(test=True)
        testvar.other_text = None
        testvar._determine_y_ax_category_labels(dataframe=dataset)

    # Test 4 - String instead of DataFrame
    with pytest.raises(TypeDataFrameError):
        dataset = 'This is a string'
        testvar = BarWithWaterfall(test=True)
        testvar.other_text = None
        testvar._determine_y_ax_category_labels(dataframe=dataset)

    # Test 5 - Other_text not of type string (but list in this case)
    with pytest.raises(TypeStringError):
        dataset = pd.DataFrame({'_Category':['A', 'B'], '_CBC_Y2':[20, 25]})
        testvar = BarWithWaterfall(test=True)
        testvar.other_text = [ 10.1 ]
        testvar._determine_y_ax_category_labels(dataframe=dataset)


def test__determine_y_ax_total_labels():
    # Test 1 - No replacement-text
    testvar  = BarWithWaterfall(test=True)
    testvar.total_text = None
    testvar.base_scenarios = ['PL', 'PY']
    testvar.compare_scenarios = ['AC']
    testvar.dict_totals = {'PY': {'yvalue': 2.125, 'total': 24.6}, 'PL': {'yvalue': 1.875, 'total': 27.3}, 'AC': {'yvalue': -15.58125, 'total': 26.0}}
    expected1 = [1.875, -15.58125]
    expected2 = ['Total', 'Total']
    expected3 = [2.125, 1.875, -15.58125]
    actual1, actual2, actual3   = testvar._determine_y_ax_total_labels()
    message  = "Test 1a - BarWithWaterfall._determine_y_ax_total_labels returned {0} instead of {1}".format(actual1, expected1)
    assert actual1 == pytest.approx(expected1), message
    message  = "Test 1b - BarWithWaterfall._determine_y_ax_total_labels returned {0} instead of {1}".format(actual2, expected2)
    assert actual2 == pytest.approx(expected2), message
    message  = "Test 1c - BarWithWaterfall._determine_y_ax_total_labels returned {0} instead of {1}".format(actual3, expected3)
    assert actual3 == pytest.approx(expected3), message

    # Test 2 - Replacement-text
    testvar  = BarWithWaterfall(test=True)
    testvar.total_text = "Europe"
    testvar.base_scenarios = ['PL', 'PY']
    testvar.compare_scenarios = ['AC']
    testvar.dict_totals = {'PY': {'yvalue': 2.125, 'total': 24.6}, 'PL': {'yvalue': 1.875, 'total': 27.3}, 'AC': {'yvalue': -15.58125, 'total': 26.0}}
    expected1 = [1.875, -15.58125]
    expected2 = ['Europe', 'Europe']
    expected3 = [2.125, 1.875, -15.58125]
    actual1, actual2, actual3   = testvar._determine_y_ax_total_labels()
    message  = "Test 2a - BarWithWaterfall._determine_y_ax_total_labels returned {0} instead of {1}".format(actual1, expected1)
    assert actual1 == pytest.approx(expected1), message
    message  = "Test 2b - BarWithWaterfall._determine_y_ax_total_labels returned {0} instead of {1}".format(actual2, expected2)
    assert actual2 == pytest.approx(expected2), message
    message  = "Test 2c - BarWithWaterfall._determine_y_ax_total_labels returned {0} instead of {1}".format(actual3, expected3)
    assert actual3 == pytest.approx(expected3), message

    # Test 3 - Base scenario is a string instead of list
    with pytest.raises(TypeListError):
        testvar = BarWithWaterfall(test=True)
        testvar.total_text = None
        testvar.base_scenarios = 'This is a string'
        testvar.compare_scenarios = ['AC']
        testvar.dict_totals = {'PY': {'yvalue': 2.125, 'total': 24.6}, 'PL': {'yvalue': 1.875, 'total': 27.3}, 'AC': {'yvalue': -15.58125, 'total': 26.0}}
        testvar._determine_y_ax_total_labels()

    # Test 4 - Compare scenario is a string instead of list
    with pytest.raises(TypeListError):
        testvar = BarWithWaterfall(test=True)
        testvar.total_text = None
        testvar.base_scenarios = ['PL', 'PY']
        testvar.compare_scenarios = 'This is a string'
        testvar.dict_totals = {'PY': {'yvalue': 2.125, 'total': 24.6}, 'PL': {'yvalue': 1.875, 'total': 27.3}, 'AC': {'yvalue': -15.58125, 'total': 26.0}}
        testvar._determine_y_ax_total_labels()

    # Test 5 - Dictionary of totals is a string instead of a dictionary
    with pytest.raises(TypeDictionaryError):
        testvar = BarWithWaterfall(test=True)
        testvar.total_text = None
        testvar.base_scenarios = ['PL', 'PY']
        testvar.compare_scenarios = ['AC']
        testvar.dict_totals = 'This is a string'
        testvar._determine_y_ax_total_labels()

    # Test 6 - Total text is a list instead of a string
    with pytest.raises(TypeStringError):
        testvar = BarWithWaterfall(test=True)
        testvar.total_text = ['This', 'is', 'a', 'list']
        testvar.base_scenarios = ['PL', 'PY']
        testvar.compare_scenarios = ['AC']
        testvar.dict_totals = {'PY': {'yvalue': 2.125, 'total': 24.6}, 'PL': {'yvalue': 1.875, 'total': 27.3}, 'AC': {'yvalue': -15.58125, 'total': 26.0}}
        testvar._determine_y_ax_total_labels()


def test_BarWithWaterfall_001():
    # Test barchart_001
    dataset =  { 'HEADERS'      : ['PY','PL','AC','FC'],  # Special keyword 'HEADERS' to indicate the scenario of the value columns
                 'Spain'        : [ 30 , 33 , 53 ,  0 ],
                 'Greece'       : [ 38 , 33 , 39 ,  0 ],
                 'Sweden'       : [ 38 , 35 , 40 ,  0 ],
                 'Germany'      : [ 90 , 89 , 93 , 25 ],
                 'Russia'       : [ 60 , 56 , 60 ,  0 ],
                 'Italy'        : [ 15 , 12 , 14 ,  0 ],
                 'Great Britain': [ 15 , 13 , 15 ,  4 ],
                 'Slovenia'     : [  4 ,  5 ,  4 ,  0 ],
                 'Denmark'      : [ 29 , 35 , 33 , 10 ],
                 'Netherlands'  : [ 39 , 42 , 38 , 15 ],
                 'France'       : [ 60 , 77 , 63 ,  0 ],
                 'OTHER'        : [ 40 , 37 , 44 , 15 ]}  # Special keyword 'OTHERS' to indicate the row with the remaining values
    title_dict = dict()
    title_dict['Reporting_unit']   = 'ACME inc.'          # Name of the company or the department
    title_dict['Business_measure'] = 'Net sales'          # Name of the business measure
    title_dict['Unit']             = 'mEUR'               # Unit: USD or EUR (monetary) or # (count)
    title_dict['Time']             = '2022'               # More specific information about the time selection
    buf = io.BytesIO()                                    # Declare a buffer to put the chart-output in
    testchart = BarWithWaterfall(data=dataset, title=title_dict, compare_scenarios='AC', 
                                 total_text="Europe", force_zero_decimals=True,
                                 filename=buf, other="Rest of Europe", do_not_show=True)
    buf.seek(0)
    sha256_hash = hashlib.sha256()                        # Initialize sha256
    for byte_block in iter(lambda: buf.read(4096),b""):
        sha256_hash.update(byte_block)
    actual=sha256_hash.hexdigest()
    buf.close()
    url = "https://raw.githubusercontent.com/MarcelW1323/clean_business_chart/main/test_charts/barchart_001.png"
    sha256_hash = hashlib.sha256()                        # Initialize sha256
    response = requests.get(url)
    sha256_hash.update(response.content)
    expected=sha256_hash.hexdigest()
    message  = "Test barchart_001.png - BarWithWaterfall returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

def test_BarWithWaterfall_002():
    # Test barchart_002
    dataset =  { 'HEADERS'      : ['PY','PL','AC','FC'],  # Special keyword 'HEADERS' to indicate the scenario of the value columns
                 'Spain'        : [ 30 , 33 , 53 ,  0 ],
                 'Greece'       : [ 38 , 33 , 39 ,  0 ],
                 'Sweden'       : [ 38 , 35 , 40 ,  0 ],
                 'Germany'      : [ 90 , 89 , 93 , 25 ],
                 'Russia'       : [ 60 , 56 , 60 ,  0 ],
                 'Italy'        : [ 15 , 12 , 14 ,  0 ],
                 'Great Britain': [ 15 , 13 , 15 ,  4 ],
                 'Slovenia'     : [  4 ,  5 ,  4 ,  0 ],
                 'Denmark'      : [ 29 , 35 , 33 , 10 ],
                 'Netherlands'  : [ 39 , 42 , 38 , 15 ],
                 'France'       : [ 60 , 77 , 63 ,  0 ],
                 'OTHER'        : [ 40 , 37 , 44 , 15 ]}  # Special keyword 'OTHERS' to indicate the row with the remaining values
    title_dict = dict()
    title_dict['Reporting_unit']   = 'ACME inc.'          # Name of the company or the department
    title_dict['Business_measure'] = 'Net sales'          # Name of the business measure
    title_dict['Unit']             = 'mEUR'               # Unit: USD or EUR (monetary) or # (count)
    title_dict['Time']             = '2022'               # More specific information about the time selection
    buf = io.BytesIO()                                    # Declare a buffer to put the chart-output in
    testchart = BarWithWaterfall(data=dataset, title=title_dict, base_scenarios=['PY', 'PL'], compare_scenarios='AC', 
                                 total_text="Europe", force_zero_decimals=True,
                                 filename=buf, other="Rest of Europe", do_not_show=True)
    buf.seek(0)
    sha256_hash = hashlib.sha256()                        # Initialize sha256
    for byte_block in iter(lambda: buf.read(4096),b""):
        sha256_hash.update(byte_block)
    actual=sha256_hash.hexdigest()
    buf.close()
    url = "https://raw.githubusercontent.com/MarcelW1323/clean_business_chart/main/test_charts/barchart_002.png"
    sha256_hash = hashlib.sha256()                        # Initialize sha256
    response = requests.get(url)
    sha256_hash.update(response.content)
    expected=sha256_hash.hexdigest()
    message  = "Test barchart_002.png - BarWithWaterfall returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message


def test__calculate_y_value_of_compare_total_bar():
    # Test 1 - Dataframe with fancy numbers for y-coordinate
    dataset =  pd.DataFrame({'_CBC_Y2'      : [-0.08125, 10, -7.08125, 5.29837]})
    testvar  = BarWithWaterfall(test=True)
    expected =  -8.58125
    actual   = testvar._calculate_y_value_of_compare_total_bar(dataframe=dataset)
    message  = "Test 1 - BarWithWaterfall._calculate_y_value_of_compare_total_bar returned {0} instead of {1}".format(actual, expected)
    assert actual == pytest.approx(expected), message

    # Test 2 - String instead of DataFrame
    with pytest.raises(TypeDataFrameError):
        testvar = BarWithWaterfall(test=True)
        testvar._calculate_y_value_of_compare_total_bar(dataframe='This is a string')
