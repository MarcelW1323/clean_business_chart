"""test General functions"""

from clean_business_chart.general_functions import *
import pytest


#####################    
# GENERAL FUNCTIONS #
#####################

def test_islist():
    # Test with a list
    expected = True
    actual   = islist(['list'])
    assert actual == expected, "islist(['list']) gives back "+str(actual)+" instead of "+str(exptected)
    # Test with a string
    expected = False
    actual   = islist('not a list')
    assert actual == expected, "islist('not a list') gives back "+str(actual)+" instead of "+str(exptected)


def test_isdictionary():
    # Test with a dictionary
    expected = True
    actual   = isdictionary({'dictionary':'yes'})
    assert actual == expected, "isdictionary({'dictionary':'yes'}) gives back "+str(actual)+" instead of "+str(exptected)
    # Test with a string
    expected = False
    actual   = isdictionary('not a dictionary')
    assert actual == expected, "isdictionary('not a dictionary') gives back "+str(actual)+" instead of "+str(exptected)


def test_plot_line_accross_axes():
    # The function plot_line_accross_axes() draws a line in a figure object.
    #### At the moment I have no idea how to test this function
    assert 1 == 1

def test_plot_line_within_ax():
    # The function plot_line_within_ax() draws a line in a figure object.
    #### At the moment I have no idea how to test this function
    assert 1 == 1


def test_plot_endpoint():
    # Only testing the parameters, not the functionality of the function
    with pytest.raises(ValueError):
        plot_endpoint(ax=1, x=2, y=3, endpointcolor=dict())
    with pytest.raises(ValueError):
        plot_endpoint(ax=1, x=2, y=3, endpointcolor=[1,2,3])
    with pytest.raises(ValueError):
        plot_endpoint(ax=1, x=2, y=3, endpointcolor=[1,2], markersize_outercircle=5, markersize_innercircle=7)


#### Need to add more test-functions for automatic testing
