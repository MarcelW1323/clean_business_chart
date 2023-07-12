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
