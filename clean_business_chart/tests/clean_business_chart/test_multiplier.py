"""test Multiplier-module"""

from clean_business_chart.multiplier import *
import pytest
        
def test_check_valid_multiplier():    
    test = Multiplier('1')
    assert test.check_valid_multiplier('1') == True
    assert test.check_valid_multiplier('k') == True
    assert test.check_valid_multiplier('m') == True
    assert test.check_valid_multiplier('b') == True
    with pytest.raises(ValueError):
        test.check_valid_multiplier('2')

def test_set_multiplier():
    test = Multiplier('b')
    test.set_multiplier('1')
    assert test.multiplier == '1'
    test.set_multiplier('k')
    assert test.multiplier == 'k'
    test.set_multiplier('m')
    assert test.multiplier == 'm'
    test.set_multiplier('b')
    assert test.multiplier == 'b'
    with pytest.raises(ValueError):
        test.set_multiplier('2')

def test_get_multiplier():
    test = Multiplier('b')
    test.set_multiplier('1')
    assert test.get_multiplier() == '1'
    test.set_multiplier('k')
    assert test.get_multiplier() == 'k'
    test.set_multiplier('m')
    assert test.get_multiplier() == 'm'
    test.set_multiplier('b')
    assert test.get_multiplier() == 'b'

def test_get_multiplier_index():
    test = Multiplier('b')
    test.set_multiplier('1')
    assert test.get_multiplier_index() == 0
    test.set_multiplier('k')
    assert test.get_multiplier_index() == 1
    test.set_multiplier('m')
    assert test.get_multiplier_index() == 2
    test.set_multiplier('b')
    assert test.get_multiplier_index() == 3
    assert test.get_multiplier_index('1') == 0
    assert test.get_multiplier_index('k') == 1
    assert test.get_multiplier_index('m') == 2
    assert test.get_multiplier_index('b') == 3
    with pytest.raises(ValueError):
        test.get_multiplier_index('5')

def test_get_multiplier_value():
    test = Multiplier('b')
    test.set_multiplier('1')
    assert test.get_multiplier_value() == 1
    test.set_multiplier('k')
    assert test.get_multiplier_value() == 1000
    test.set_multiplier('m')
    assert test.get_multiplier_value() == 1000000
    test.set_multiplier('b')
    assert test.get_multiplier_value() == 1000000000
    assert test.get_multiplier_value('1') == 1
    assert test.get_multiplier_value('k') == 1000
    assert test.get_multiplier_value('m') == 1000000
    assert test.get_multiplier_value('b') == 1000000000
    with pytest.raises(ValueError):
        test.get_multiplier_value('5')

def test_get_multiplier_string():
    test = Multiplier('b')
    test.set_multiplier('1')
    assert test.get_multiplier_string() == ''
    test.set_multiplier('k')
    assert test.get_multiplier_string() == 'k'
    test.set_multiplier('m')
    assert test.get_multiplier_string() == 'm'
    test.set_multiplier('b')
    assert test.get_multiplier_string() == 'b'
    assert test.get_multiplier_string('1') == ''
    assert test.get_multiplier_string('k') == 'k'
    assert test.get_multiplier_string('m') == 'm'
    assert test.get_multiplier_string('b') == 'b'
    with pytest.raises(ValueError):
        test.get_multiplier_string('5')

def test_optimize():
    test = Multiplier('1')
    test.set_multiplier('1')
    assert test.optimize(5836415089) == 1000000000
    test.set_multiplier('k')
    assert test.optimize(5836415089) == 1000000
    test.set_multiplier('m')
    assert test.optimize(5836415089) == 1000
    test.set_multiplier('b')
    assert test.optimize(5836415089) == 1
    test.set_multiplier('k')
    assert test.optimize(58364.15089) == 1000
    with pytest.raises(TypeError):
        test.optimize('no integer or float')