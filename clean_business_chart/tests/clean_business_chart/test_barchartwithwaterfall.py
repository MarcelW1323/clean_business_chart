"""test BarWithWaterfall-module"""

from clean_business_chart.barchartwithwaterfall import *
import pandas as pd
from pandas import Timestamp  # Needed in test__dataframe_date_to_year_and_month()
import pytest


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
    with pytest.raises(TypeError):
        scenarios              = None
        default_scenariolist   = 15
        technical_scenariolist = ['PY', 'PL', 'AC', 'FC']
        testvar = BarWithWaterfall(test=True)
        testvar._simple_first_check_scenario_parameters_one_variable(scenarios=scenarios, default_scenariolist=default_scenariolist, 
                                                                     technical_scenariolist=technical_scenariolist)

    # Test 5 - technical_scenariolist is string (not a list)
    with pytest.raises(TypeError):
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
    with pytest.raises(TypeError):
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
    with pytest.raises(TypeError):
        testvar = BarWithWaterfall(test=True)
        testvar.data_scenarios = ['PY', 'PL', 'AC', 'FC']
        testvar._fill_data_total(dataframe="This is a string")  # Default parameter decimals is None and that is supported

    # Test 6 - parameter decimals is a string and not an integer
    with pytest.raises(TypeError):
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
    with pytest.raises(TypeError):
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
    expected = {'_Category': ['Airbus', 'Airbus', 'Boeing', 'Boeing'], 'Year': ['2021', '2022', '2021', '2022'], 
                'PY': [72.0, 38.0, 38.2, 39.0], 'PL': [74.0, 39.0, 38.98899, 40.0], 'AC': [74, 36, 33, 37], 'FC': [73, 40, 38, 39]}
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
    with pytest.raises(TypeError):
        testvar  = BarWithWaterfall(test=True)
        testvar._dataframe_aggregate(dataframe="This is a string", wanted_headers=['list-item 1', 'list-item 2'])

    # Test 4 - parameter wanted_headers is a string and not a list
    with pytest.raises(TypeError):
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
    testvar  = BarWithWaterfall(test=True)
    testvar.data_total = {'AC':1357.2468, 'PL':862.64, 'PY':8723.85, 'FC':103020.76932}
    expected = {'AC': 48.85, 'PL': 31.05, 'PY': 313.97, 'FC': 3707.69}
    testvar._optimize_data_total(numerator=14, denominator=389, decimals=2)
    actual   = testvar.data_total
    message  = "Test 1 - BarWithWaterfall._optimize_data_total returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 2 - good dictionary and good parameters (with normal, valid values and one decimals)
    testvar  = BarWithWaterfall(test=True)
    testvar.data_total = {'AC':1357.2468, 'PL':862.64, 'PY':8723.85, 'FC':103020.76932}
    expected = {'AC': 1.4, 'PL': 0.9, 'PY': 8.7, 'FC': 103.0}
    testvar._optimize_data_total(numerator=1, denominator=1000, decimals=1)
    actual   = testvar.data_total
    message  = "Test 2 - BarWithWaterfall._optimize_data_total returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 3 - good dictionary and good parameters (with unusual, valid values and no decimals)
    testvar  = BarWithWaterfall(test=True)
    testvar.data_total = {'AC':1357.2468, 'PL':862.64, 'PY':8723.85, 'FC':103020.76932}
    expected = {'AC': 68, 'PL': 43, 'PY': 436, 'FC': 5151}
    testvar._optimize_data_total(numerator=50, denominator=1000, decimals=0)
    actual   = testvar.data_total
    message  = "Test 3 - BarWithWaterfall._optimize_data_total returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 4 - Numerator is not an integer
    with pytest.raises(TypeError):
        testvar  = BarWithWaterfall(test=True)
        testvar.data_total = {'AC':1357.2468, 'PL':862.64, 'PY':8723.85, 'FC':103020.76932}
        testvar._optimize_data_total(numerator="This is a string", denominator=1, decimals=0)

    # Test 5 - Denominator is not an integer
    with pytest.raises(TypeError):
        testvar  = BarWithWaterfall(test=True)
        testvar.data_total = {'AC':1357.2468, 'PL':862.64, 'PY':8723.85, 'FC':103020.76932}
        testvar._optimize_data_total(numerator=1, denominator="This is a string", decimals=0)

    # Test 6 - Decimals is not an integer
    with pytest.raises(TypeError):
        testvar  = BarWithWaterfall(test=True)
        testvar.data_total = {'AC':1357.2468, 'PL':862.64, 'PY':8723.85, 'FC':103020.76932}
        testvar._optimize_data_total(numerator=1, denominator=1, decimals="This is a string")

    # Test 7 - Data_total is not a dictionary
    with pytest.raises(TypeError):
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
    with pytest.raises(TypeError):
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
    with pytest.raises(TypeError):
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
    with pytest.raises(TypeError):
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
    with pytest.raises(TypeError):
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
    with pytest.raises(TypeError):
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

    # Test 3 - String instead of dataframe
    with pytest.raises(TypeError):
        testvar = BarWithWaterfall(test=True)
        testvar._sort_dataframe_with_other_last(dataframe='This is a string')

    # Test 4 - Dataframe is missing the category-of-interest column
    with pytest.raises(ValueError):
        testvar = BarWithWaterfall(test=True)
        dataset = pd.DataFrame({'Year'       : ['2022', '2022', '2022', '2022', '2022'],
                                'PY'         : [32.7, 38.2, 40.0, 38.0, 35.0],
                                'PL'         : [33.0, 38.9, 41.0, 40.3, 36.0],
                                'AC'         : [32.25, 38.0, 33.6, 39.0, 36.6],
                                'FC'         : [38.65, 32.0, 41.0, 37.1, 35.1],
                                '_CBC_DELTA1': [-0.75, -0.9, -7.4, -1.3, 0.6],
                                '_CBC_DELTA2': [37.9, 31.1, 33.6, 35.8, 35.7]})
        testvar._sort_dataframe_with_other_last(dataframe=dataset)

    # Test 5 - Dataframe is missing the delta1 column
    with pytest.raises(ValueError):
        testvar = BarWithWaterfall(test=True)
        dataset = pd.DataFrame({'Year'       : ['2022', '2022', '2022', '2022', '2022'],
                                'PY'         : [32.7, 38.2, 40.0, 38.0, 35.0],
                                'PL'         : [33.0, 38.9, 41.0, 40.3, 36.0],
                                '_Category'  : ['Airbus', 'OTHER', 'Boeing', 'General Dynamics', 'Lockheed Martin'],
                                'AC'         : [32.25, 38.0, 33.6, 39.0, 36.6],
                                'FC'         : [38.65, 32.0, 41.0, 37.1, 35.1],
                                '_CBC_DELTA2': [37.9, 31.1, 33.6, 35.8, 35.7]})
        testvar._sort_dataframe_with_other_last(dataframe=dataset)

    # Test 6 - Dataframe is missing the delta2 column
    with pytest.raises(ValueError):
        testvar = BarWithWaterfall(test=True)
        dataset = pd.DataFrame({'Year'       : ['2022', '2022', '2022', '2022', '2022'],
                                'PY'         : [32.7, 38.2, 40.0, 38.0, 35.0],
                                'PL'         : [33.0, 38.9, 41.0, 40.3, 36.0],
                                '_Category'  : ['Airbus', 'OTHER', 'Boeing', 'General Dynamics', 'Lockheed Martin'],
                                'AC'         : [32.25, 38.0, 33.6, 39.0, 36.6],
                                'FC'         : [38.65, 32.0, 41.0, 37.1, 35.1],
                                '_CBC_DELTA1': [-0.75, -0.9, -7.4, -1.3, 0.6]})
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
    with pytest.raises(TypeError):
        testvar = BarWithWaterfall(test=True)
        testvar.remove_lines_with_zeros = True
        testvar.data_scenarios = ['PY', 'PL', 'FC', 'AC']
        testvar._drop_zero_lines(dataframe='This is a string')

    # Test 4 - String instead of boolean for remove_lines_with_zeros
    with pytest.raises(TypeError):
        testvar = BarWithWaterfall(test=True)
        testvar.remove_lines_with_zeros = "This is a string"
        testvar.data_scenarios = ['PY', 'PL', 'FC', 'AC']
        dataset = pd.DataFrame()
        testvar._drop_zero_lines(dataframe=dataset)

    # Test 5 - String instead of list for data_scenarios
    with pytest.raises(TypeError):
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