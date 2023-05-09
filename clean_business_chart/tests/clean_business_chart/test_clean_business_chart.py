"""test Clean_Business_Chart-module"""

from clean_business_chart.clean_business_chart import *
import pytest


def test__fill_default_barwidths():
    # Test 1 - normal
    testvar  = GeneralChart()
    expected = {'measure':0.65, 'ratio':0.35}
    actual   = testvar.barwidths
    message  = "Test 1 - GeneralChart._fill_default_barwidths returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message


def test_get_barwidth():
    # Test 1 - measure=True
    measure  = True
    testvar  = GeneralChart()
    testvar.get_barwidth(measure=measure)
    expected = 0.65
    actual   = testvar.barwidth
    message  = "Test 1 - GeneralChart.get_barwidth returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 2 - measure=False
    measure  = False
    testvar  = GeneralChart()
    testvar.get_barwidth(measure=measure)
    expected = 0.35
    actual   = testvar.barwidth
    message  = "Test 2 - GeneralChart.get_barwidth returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 2 - measure is not a boolean
    expected = 0.35
    actual   = testvar.barwidth
    message  = "Test 2 - GeneralChart.get_barwidth returned {0} instead of {1}".format(actual, expected)
    assert actual == expected, message

    # Test 3 - measure is not a boolean
    with pytest.raises(TypeError):
        measure  = 'I am a string'
        testvar  = GeneralChart()
        testvar.get_barwidth(measure=measure)