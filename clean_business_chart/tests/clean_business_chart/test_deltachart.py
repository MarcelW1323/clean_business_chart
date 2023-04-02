"""test DeltaChart-module"""

from clean_business_chart.deltachart import *
import pytest
        
def test_calculate_h():
    # Test 1 - good delta calculation 
    dataset = {'PY': [14, 16, 14, 17, 19, 17, 19, 22, 16, 17, 16, 22], 
               'PL': [11, 10, 10, 10, 10, 10, 15, 14, 15, 15, 15, 19],
               'AC': [15, 13, 16,  7,  5,  6, 17, 11],
               'FC': [ 0,  0,  0,  0,  0,  0,  0,  0, 26, 22, 13, 29]} 
    deltachart = DeltaChart()               
    deltachart.calculate_h(data=dataset, base_scenario='PL', compare_scenario_list=['AC', 'FC'])
    expected = ['AC', 'AC', 'AC', 'AC', 'AC', 'AC', 'AC', 'AC', 'FC', 'FC', 'FC', 'FC']
    actual   = deltachart.delta_scenario_list
    message  = "Test 1a - delta_scenario_list: deltachart.calculate returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    expected = [4, 3, 6, -3, -5, -4, 2, -3, 11, 7, -2, 10]
    actual   = deltachart.delta_value_list
    message = "Test 1b - delta_value_list: deltachart.calculate returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 2 - delta calculation not supported yet
    with pytest.raises(ValueError):
        dataset = {'PY': [14, 16, 14, 17, 19, 17, 19, 22, 16, 17, 16, 22], 
                   'PL': [11, 10, 10, 10, 10, 10, 15, 14, 15, 15, 15, 19],
                   'AC': [15, 13, 16,  7,  5,  6, 17, 11],
                   'FC': [ 0,  0,  0,  0,  0,  0,  0, 15, 26, 22, 13, 29]}  # Number 15 added
        actual = DeltaChart()               
        actual.calculate_h(data=dataset, base_scenario='PL', compare_scenario_list=['AC', 'FC'])