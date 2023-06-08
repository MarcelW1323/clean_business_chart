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