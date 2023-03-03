"""test DeltaChart-module"""

from clean_business_chart.deltachart import *
import pytest
        
def test_check_valid_multiplier():  
    dataset = {'PY': [14, 16, 14, 17, 19, 17, 19, 22, 16, 17, 16, 22], 
               'PL': [11, 10, 10, 10, 10, 10, 15, 14, 15, 15, 15, 19],
               'AC': [15, 13, 16,  7,  5,  6, 17, 11],
               'FC': [ 0,  0,  0,  0,  0,  0,  0,  0, 26, 22, 13, 29]} 
    actual = DeltaChart()               
    actual.calculate(data=dataset, base_scenario='PL', compare_scenario_list=['AC', 'FC'])
    expected_delta_scenario_list = ['AC', 'AC', 'AC', 'AC', 'AC', 'AC', 'AC', 'AC', 'FC', 'FC', 'FC', 'FC']
    expected_delta_value_list    = [4, 3, 6, -3, -5, -4, 2, -3, 11, 7, -2, 10]
    assert actual.delta_scenario_list == expected_delta_scenario_list
    assert actual.delta_value_list    == expected_delta_value_list
    