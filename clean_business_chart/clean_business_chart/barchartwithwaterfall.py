"""BarWithWaterfall-module"""

import matplotlib.pyplot as plt                   # for most graphics
from matplotlib import rcParams as mpl_rcp        # for font in _title
import pandas as pd                               # for easy pandas support

from clean_business_chart.clean_business_chart import GeneralChart 
from clean_business_chart.general_functions    import plot_line_accross_axes, plot_line_within_ax, prepare_title, formatstring, optimize_data, \
                                                      islist, isdictionary, isinteger, isstring, isfloat, isboolean, isdataframe, error_not_islist, \
                                                      error_not_isdictionary, error_not_isinteger, error_not_isstring, error_not_isboolean, \
                                                      error_not_isdataframe, error_not_isaxes, \
                                                      string_to_value, filter_lists, convert_data_string_to_pandas_dataframe, convert_data_list_of_lists_to_pandas_dataframe, \
                                                      dataframe_translate_field_headers, dataframe_search_for_headers, dataframe_keep_only_relevant_columns, \
                                                      dataframe_date_to_year_and_month, dataframe_convert_year_month_to_string, list1_is_subset_list2, \
                                                      convert_dataframe_scenario_columns_to_value
                                                      
from clean_business_chart.multiplier           import Multiplier
from clean_business_chart.exceptions           import *  # for custom errors/exceptions


class BarWithWaterfall(GeneralChart):
    """
    The class BarWithWaterfall produces a bar chart with a waterfall deltachart based on data of one category-column (the category-of-interest).
    
    Minimal requirements to make the chart
    --------------------------------------
    import clean_business_chart as cbc
    dataset =  { 'HEADERS'      : ['PY','PL','AC','FC'],     # Special keyword 'HEADERS' to indicate the scenario of the value columns
                 'Spain'        : [ 30 , 33 , 53 ,  0 ],
                 'Greece'       : [ 38 , 33 , 39 ,  0 ],
                 'Sweden'       : [ 38 , 35 , 40 ,  0 ],
                 'Germany'      : [ 90 , 89 , 93 ,  0 ],
                 'Russia'       : [ 60 , 56 , 60 ,  0 ],
                 'Italy'        : [ 15 , 12 , 14 ,  0 ],
                 'Great Britain': [ 15 , 13 , 15 ,  0 ],
                 'Slovenia'     : [  4 ,  5 ,  4 ,  0 ],
                 'Denmark'      : [ 29 , 35 , 33 ,  0 ],
                 'Netherlands'  : [ 39 , 42 , 38 ,  0 ],
                 'France'       : [ 60 , 77 , 63 ,  0 ],
                 'OTHER'        : [ 40 , 37 , 44 ,  0 ]}     # Special keyword 'OTHERS' to indicate the row with the remaining values
    cbc.BarWithWaterfall(data=dataset)
    
    Parameters
    ----------
    data                    : Preferably a pandas DataFrame, but Dictionary, CSV-like string or a list-of-lists can also be processed.
    positive_is_good        : On a variance chart it decides whether a positive number makes a good color (True) or a bad color (False).
                              Default: True (positive number gets a good color)
    base_scenarios          : Use a list of max two scenario's. The first scenario is the preferred base scenario and will be used in the 
                              detailed part of the chart.
                              The second scenario will only be used for the aggregated chart part in the beginning (upper bars).
                              PL, use PLaninfo as the base scenario in the chart. PY uses Previous Year als the base scenario in the chart,
                              FC, use Forecast as the base scenario in the chart.
                              Default: None (tries to use ['PL', 'PY'] if both are available or else try one of these)
    compare_scenarios       : Use a list of max two scenario's to compare with the preferred base scenario. For example if preferred base scenario
                              is PL, you can use ['AC', 'FC'] to compare the actuals with the forecast against the plan.
                              Possible lists to be used: ['AC'], ['AC', 'FC'], ['AC', 'PL'], ['AC', 'PY'], ['FC'] or ['PL'], but it depends on the
                              preferred base scenario if the combination can be used
                              NOTE: IN THIS VERSION THERE IS NO SUPPORT FOR TWO COMPARE SCENARIOS.
                              Default: None (tries to use ['AC', 'FC'] if both are available or else try one of these)
    title                   : A dictionary with optional values to make a title inspired by IBCS
                              Default: None (no title)
    measure                 : True -> measure, False -> ratio
                              Default: True (measure)
    multiplier              : One character with the multiplier ('1', 'k', 'm', 'b')
                              Default: '1' (one)
    filename                : String with filename and path to export the chart to, including extention. Only tested with a .png-extention
                              Default: None (no export of the chart to a file)
    force_pl_is_zero        : If PL are all zeros, can PL be ignored (False) or force that PL can be zero (True)
                              NOTE: THIS PARAMETER IS NOT SUPPORTED YET IN THIS VERSION
                              Default: False (PL can be ignored when all zeros)
    force_zero_decimals     : If True, we use integers for output. This gives a more clean chart, but can lack some detail in some cases
                              Default: False (don't force zero decimals)
    force_max_one_decimals  : If True, the maximum of decimals used is one. Know that force_zero_decimals has a higher priority than force_max_one_decimals.
                              Default: False (don't force max one decimals)
    translate_headers       : Dictionary where you can translate field headers, example {'Orderdate':'Date', 'Revenue':'AC'}
                              Default: None (no translation of headers will occur)
    category_of_interest    : Name of the category of interest (after 'translate_headers').
                              Default: None (the first column available except one of these column names 'Date', 'Year', 'Month', 'AC', 'FC', 'PY', 'PL'.
    previous_year           : Boolean if the previous year needs to be calculated out of the data
                              Default: False (there is no previous year to be calculated out of the data)
                              NOTE: THIS PARAMETER IS NOT SUPPORTED YET IN THIS VERSION
    total_text              : Text that will be added to the 'total'-bars instead of 'Total'
                              Default: None (text 'Total' will be added)
    total_line              : If True, a line just above the total bar will be displayed
                              Default: True (line will be displayed)
    remove_lines_with_zeros : If True, category-elements with zero in all scenarios will be removed. If False, nothing will be removed
                              Default: True (category-elements with zero in all scenarios will be removed)    
    other                   : Text that will be displayed instead of "OTHER"
                              Default: None ("OTHER" will be displayed)
    """

    def __init__(self, data=None, positive_is_good=True, base_scenarios=None, compare_scenarios=None, title=None, measure=True, multiplier='1', 
                 filename=None, force_pl_is_zero=False, force_zero_decimals=False, force_max_one_decimals=False, translate_headers=None, 
                 category_of_interest=None, previous_year=False, total_text=None, total_line=True, remove_lines_with_zeros=True, other=None, test=False,
                 do_not_show=False):
        """
        The function __init__ is the first function that will be called automatically. Here you'll find all the possible parameters to customize your experience.
        """
        super().__init__()                         # Get the variables from the parent class
        self._other_barwithwaterfall_variables()   # Get additional variables for this class

        # for use to test automatically
        if test: return None

        # Store variables
        self.original_data              = data
        self.original_multiplier        = Multiplier(multiplier)
        self.positive_is_good           = positive_is_good
        self.original_base_scenarios    = base_scenarios
        self.original_compare_scenarios = compare_scenarios
        self.hatch                      = self.hatch_pattern
        self.filename                   = filename
        self.force_pl_is_zero           = force_pl_is_zero
        self.force_zero_decimals        = force_zero_decimals
        self.force_max_one_decimals     = force_max_one_decimals
        self.translate_headers          = translate_headers
        self.category                   = category_of_interest
        self.previous_year              = previous_year
        self.total_text                 = total_text
        self.total_line                 = total_line
        self.remove_lines_with_zeros    = remove_lines_with_zeros
        self.other_text                 = other

        # Check scenarios
        self.simple_first_check_scenario_parameters()     
        
        # Calculate chart
        self.get_barwidth(measure)
        self._check_and_process_data(data)
        
        # Make chart and fill the chart
        self._make_subplots()
        self._fill_chart()

        # Add the title as the last element 
        self._title_figure(title)
        
        # Check if you need to display the total_line
        if self.total_line:
            self._plot_total_line()
        
        # We are exporting the chart if the filename has a value
        if self.filename is not None:
            plt.savefig(self.filename, bbox_inches='tight', dpi=150)
        
        # For automatic testing of complete images of chart
        if not do_not_show:
            # No, no automatic testing of complete images of chart -> show the chart
            plt.show()


    def _other_barwithwaterfall_variables(self):
        """
        A collection of variables for barchartwithwaterfall
        """
        # Data
        self.data              = None       # Data used for the barchart
        self.data_total        = dict()     # Totals of the data (all scenarios)
        self.dict_totals       = dict()     # Totals of the data (only one entry for the last total line underneath the detailed chart)
                                            # One entry each for the base scenarios, only one entry with the name of the first item of the compare scenarios
                                            # Combined with the Y-coordinate of the bar
        self.all_header_fields = self.all_date_columns + self.all_scenarios # All header fields needed to calculate the dataset
        
        # Scenarios
        self.base_scenarios    = None       # This variable will hold a list of max 2 base scenarios. Only the first is used in the detail chart
        self.compare_scenarios = None       # This variable will hold a list of max 2 scenarios that will be used in the comparison with the first base scenario.
        
        # Decimals
        self.decimals_details  = 0          # Number of decimals used in the numbers of the detail chart
        self.decimals_totals   = 0          # Number of decimals used in the numbers of the total chart
        
        # Multipliers
        self.multiplier             = None  # Initial value
        self.multiplier_denominator = 1     # Denominator is the diviser
        
        # Other
        self.year_column = ['Year']            # Year column, needed for calculating previous year information
        self.filename    = None                # When filename is None, no export
        self.barshift    = self.barshift_value # Value to use with partly overlapping bars
        
        # Chart
        self.fig         = None             # Figure variable for the chart. Initial value is None to easy check in automatic testing
        self.ax          = None             # Axis variable for the chart. Initial value is None to easy check in automatic testing
        
        return


    def _simple_first_check_scenario_parameters_one_variable(self, scenarios=None, default_scenariolist=None, technical_scenariolist=None):
        """
        In this function scenarios will be checked if they are None, a string or a list. 
        When None, then they will become equal to the default scenariolist.
        When string, they will be transformed into a list.
        At the end, the scenarios are in a list and then will be checked if they are valid scenarios out of a superlist (technical_scenariolist).
        And the last check is that the list will contain one or two scenarios.

        Parameters
        ----------
        scenarios              : None, a string or a list
        default_scenariolist   : List with default scenarios. Will be used when parameter scenarios is None.
        technical_scenariolist : List with all valid scenarios. Will be used to check the scenarios against.

        Returns
        -------
        return_scenarios       : List with valid scenarios
        """
        # Check if the default_scenariolist is a list
        error_not_islist(default_scenariolist, "default_scenariolist")

        # Check if the technical_scenariolist is a list
        error_not_islist(technical_scenariolist, "technical_scenariolist")

        # Make sure to convert everything to a list of scenarios
        if scenarios is None:
            return_scenarios    = default_scenariolist    # Later on will be checked if these scenarios are present
        elif isstring(scenarios):
            return_scenarios    = [x.strip() for x in scenarios.strip().split(sep=',')]
        elif islist(scenarios):
            return_scenarios    = scenarios
        else:
            raise TypeError(str(scenarios)+" not supported. Please use a list with max 2 scenarios (for example: "+str(default_scenariolist)+")")

        # Check for technical valid scenarios
        for element in return_scenarios:
            if element not in technical_scenariolist:
                raise ValueError(str(element)+" not supported. Please use one or two scenarios out of this list: "+str(technical_scenariolist))

        # Check for one or two elements
        if len(return_scenarios) < 1 or len(return_scenarios) > 2:
            raise ValueError(str(len(return_scenarios))+" scenarios ("+str(return_scenarios)+ \
                             ") not supported. Please use a list with max 2 scenarios (for example: "+str(default_scenariolist)+")")

        return return_scenarios


    def simple_first_check_scenario_parameters(self):
        """
        The function simple_first_check_scenario_parameters will check if the parameters given for the scenarios to this class are technically valid.

        Self variables
        --------------
        self.original_base_scenarios    : This variable holds the original parameter passed to this class
        self.base_scenarios             : This variable will hold a list of max 2 base scenarios after this first check. 
                                          Only the first value of the list is used in the detail chart
        self.original_compare_scenarios : This variable holds the original parameter passed to this class
        self.compare_scenarios          : This variable will hold a list of max 2 scenarios after this first check 
                                          that will be used in the comparison with the first base scenario.
        self.all_scenarios              : A list of all supported scenarios in the right time order
        """
        self.base_scenarios    = self._simple_first_check_scenario_parameters_one_variable(scenarios              = self.original_base_scenarios, 
                                                                                           default_scenariolist   = filter_lists(['PL', 'PY'], self.all_scenarios),
                                                                                           technical_scenariolist = self.all_scenarios)

        self.compare_scenarios = self._simple_first_check_scenario_parameters_one_variable(scenarios              = self.original_compare_scenarios, 
                                                                                           default_scenariolist   = filter_lists(['AC', 'FC'], self.all_scenarios),
                                                                                           technical_scenariolist = self.all_scenarios)

        return


    def _check_scenario_parameters(self):
        """
        The function simple_first_check_scenario_parameters will check if the parameters given for the scenarios to this class are technically valid.

        Self variables
        --------------
        self.data_scenarios             : List with scenarios found in the data
        self.base_scenarios             : List of max 2 scenarios of which the first is used for comparisation and is used in the detail chart. 
        self.compare_scenarios          : List of max 2 scenarios that will be used in the comparison with the first base scenario.
        """
        base = self.base_scenarios[0]
        compare = self.compare_scenarios

        #### FIRST VERSION SUPPORTS ONLY ONE COMPARE SCENARIO
        if len(compare) > 1:
            raise ValueError("More than one compare scenario is still not supported:"+str(compare))
        
        if base == 'PY':
            # The first bar is Previous Year
            if compare not in ( ['AC'], ['AC', 'FC'], ['AC', 'PL'], ['AC', 'PY'], ['FC'], ['PL'] ):
                raise ValueError('Scenario combinations '+str(base)+' and '+str(compare)+' are not supported')
                # PY and AC   : Compare the current actuals against the previous year.
                #               Gives answer to the question: How am I doing this time period compared to the same time period previous year.
                # PY and AC,FC: Compare the current actuals with forecast added against the previous year. Actual timeframe and forecast timeframe do not overlap.
                #               Gives answer to the question: How am I doing this time period with added forecast for the remaining period not present in actuals
                #               compared to the same time period previous year.
                # PY and AC,PL: Compare the current actuals with plan added against the previous year. Actual timeframe and plan timeframe do not overlap.
                #               Gives answer to the question: How am I doing this time period when the rest of the time period goes like plan
                #               compared to the same time period previous year.
                # PY and AC,PY: Compare the current actuals with previous year added against the previous year. Actual timeframe and PY timeframe do not overlap.
                #               Gives answer to the question: How am I doing this time period when the rest of the time period goes like previous year
                #               compared to the same time period previous year.
                # PY and FC   : Compare the forecast against the previous year.
                #               Gives answer to the question: How is my forecast this time period compared to the same time period previous year.
                # PY and PL   : Compare the plan against the previous year.
                #               Gives answer to the question: How is my plan this time period compared to the same time period previous year.
        if base == 'PL':
            # The first bar is PLan
            if compare not in ( ['AC'], ['AC', 'FC'], ['AC', 'PY'], ['AC', 'PL'], ['FC'] ):
                raise ValueError('Scenario combinations '+str(base)+' and '+str(compare)+' are not supported')
                # PL and AC   : Compare the current actuals against the plan.
                #               Gives answer to the question: How am I doing this time period compared to the plan of the same time period.
                # PL and AC,FC: Compare the current actuals with forecast added against the plan. Actual timeframe and forecast timeframe do not overlap.
                #               Gives answer to the question: How am I doing this time period with added forecast for the remaining period not present in actuals
                #               compared to the plan of the same time period.
                # PL and AC,PL: Compare the current actuals with plan added against the plan. Actual timeframe and plan timeframe do not overlap.
                #               Gives answer to the question: How am I doing this time period when the rest of the time period goes like plan
                #               compared to the plan of the same time period.
                # PL and AC,PY: Compare the current actuals with previous year added against the plan. Actual timeframe and previous year timeframe do not overlap.
                #               Gives answer to the question: How am I doing this time period when the rest of the time period goes like previous year
                #               compared to the plan of the same time period.
                # PL and FC   : Compare the forecast against the plan.
                #               Gives answer to the question: How is my forecast this time period compared to the plan of the same time period.
        if base == 'FC':
            # The first bar is Forecast
            if compare not in ( ['AC'], ['AC', 'FC'], ['AC', 'PY'], ['AC', 'PL'] ):
                raise ValueError('Scenario combinations '+str(base)+' and '+str(compare)+' are not supported')
                # FC and AC   : Compare the current actuals against the forecast.
                #               Gives answer to the question: How am I doing this time period compared to the forecast of the same time period.
                # FC and AC,FC: Compare the current actuals with forecast added against the forecast. Actual timeframe and forecast timeframe do not overlap.
                #               Gives answer to the question: How am I doing this time period with added forecast for the remaining period not present in actuals
                #               compared to the forecast of the same time period.
                # FC and AC,PY: Compare the current actuals with previous year added against the forecast. Actual timeframe and previous year timeframe do not overlap.
                #               Gives answer to the question: How am I doing this time period when the rest of the time period goes like previous year
                #               compared to the forecast of the same time period.
                # FC and AC,PL: Compare the current actuals with plan added against the forecast. Actual timeframe and plan timeframe do not overlap.
                #               Gives answer to the question: How am I doing this time period when the rest of the time period goes like plan
                #               compared to the forecast of the same time period.
        if base not in ['PY', 'PL', 'FC']:
            raise ValueError("Base scenario "+str(base)+" not supported.")

       # Check if the base-scenarios are in the data scenarios 
        if self.base_scenarios != filter_lists(list1=self.base_scenarios, list2=self.data_scenarios):
            raise ValueError("Base scenarios "+str(self.base_scenarios)+" not in the data scenarios "+str(self.data_scenarios)+" of the dataframe.")

        # Check if the compare-scenarios are in the data scenarios
        if self.compare_scenarios != filter_lists(list1=self.compare_scenarios, list2=self.data_scenarios):
            raise ValueError("Compare scenarios "+str(self.compare_scenarios)+" not in the data scenarios "+str(self.data_scenarios)+" of the dataframe.")

        return


    def _add_yvalues_to_dataframe(self, dataframe):
        """
        This function calculates based on the number of lines in the DataFrame the y-coordinate for the chart. A line with "OTHER" will be handled separately.
        Extra column _CBC_Y is the middle of the Y-coordinate
        Extra column _CBC_Y1 is for the upper bar (base)
        Extra column _CBC_Y2 is for the lower bar (compare)

        # Precondition: all delta-columns are made and dataframe is sorted in the right order for output to chart
        # Precondition: if 'OTHER' is available, it needs to be the last value in the column

        Parameters
        ----------
        dataframe              : pandas DataFrame

        Self variables
        --------------
        self.barshift          : value to use to shift one bar up and the other bar down with partly overlapping bars
        self.barwidth          : A float with the width of the bars for measure or ratio

        Returns
        -------
        export_dataframe       : pandas DataFrame with added y-coordinates
        """
        # Check dataframe
        error_not_isdataframe(dataframe, 'dataframe')

        # Check some self-variables
        if not isinteger(self.barshift) and not isfloat(self.barshift):
            raise TypeError('self.barshift "'+str(self.barshift)+'" is not a float or an integer, but of type '+str(type(self.barshift)))
        if not isinteger(self.barwidth) and not isfloat(self.barwidth):
            raise TypeError('self.barwidth "'+str(self.barwidth)+'" is not a float or an integer, but of type '+str(type(self.barwidth)))

        # Check if 'OTHER'-category-value
        if 'OTHER' in list(dataframe['_Category']):
            # Yes, OTHER is in the category-values. OTHER needs to be the last value in the column
            if list(dataframe['_Category'])[-1] != 'OTHER':
                # No, the last entry is not OTHER
                raise ValueError('OTHER is not the last value in the category-of-interest-column')
            # else:
                # Yes, the last entry is OTHERS
        # else:
            # No, no OTHER value in the category-values

        # Prepare the return value
        export_dataframe = dataframe.copy()

        # Make column with the Y-values for the categories.
        export_dataframe.insert(loc = len(export_dataframe.columns), column='_CBC_Y', value=range(0, len(export_dataframe)*-1, -1))
        export_dataframe.loc[export_dataframe['_Category']=='OTHER', ['_CBC_Y']] = export_dataframe[export_dataframe['_Category']=='OTHER']['_CBC_Y'] - 0.5

        # Make columns Y1 for the "upper" bar, Y2 for the bar located lower, but partly on top of the "upper" bar.
        export_dataframe.insert(loc = len(export_dataframe.columns), column='_CBC_Y1', value=export_dataframe['_CBC_Y'] + self.barshift * self.barwidth)
        export_dataframe.insert(loc = len(export_dataframe.columns), column='_CBC_Y2', value=export_dataframe['_CBC_Y'] - self.barshift * self.barwidth)

        return export_dataframe


    def _determine_bar_layers_in_dataframe(self, dataframe):
        """
        This function checks if there are two compare scenarios which of these two scenarios is on top.
        Main idea is that we search upfront for the top bars of each scenario.
        Then we can make the bars of these top bars separately from the other bars of the same scenario, so we can use the bar_label function for
        correct placement of the figures.
        The scenario of the top bar is recorded in the new column _CBC_TOPLAYER.
        
        Parameters
        ----------
        dataframe              : pandas DataFrame

        Self variables
        --------------
        self.compare_scenarios : List of max 2 scenarios that will be used in the comparison with the first base scenario.

        Returns
        -------
        export_dataframe       : pandas DataFrame with included top-layer-column
        """
        # How many layers are there (min 1, max 2). Check scenario
        scenario = self.compare_scenarios
        error_not_islist(scenario, "scenario")
        # Scenario is a list!
        if len(scenario) != 1 and len(scenario) != 2:
            # Less than 1 or more than 2 entries
            raise ValueError(str(scenario)+' needs to have 1 or 2 scenarios.')
        # else:
            # 1 or 2 entries is OK

        # Check dataframe
        error_not_isdataframe(dataframe, 'dataframe')

        # Make the export variables
        export_dataframe = dataframe.copy()

        # Make a new column at the end
        export_dataframe.insert(loc = len(export_dataframe.columns), column='_CBC_TOPLAYER', value='')

        # Fill the new column with the last scenario in the list if the column with that scenario has a value not equal to 0
        export_dataframe.loc[export_dataframe[scenario[-1]] != 0, ['_CBC_TOPLAYER']] = scenario[-1]
        # Fill the new column with the first scenario in the list if the column with the last scenario has a value equal to 0
        export_dataframe.loc[export_dataframe[scenario[-1]] == 0, ['_CBC_TOPLAYER']] = scenario[0]

        return export_dataframe


    def _check_base_scenario_totals(self):
        """
        This function calculates the totals of the base scenarios. This can be one scenario or two scenarios.
        Next it determines the barshift (<>0 with 2 scenarios)
        Also the position of the text-value of the first scenario is determined as special or not
        And also the start of the line of the first scenario is determined.

        Self variables
        --------------
        self.base_scenarios         : List of max 2 scenarios of which the first is used for comparisation and is used in the detail chart
        self.all_scenarios          : List of all supported scenarios in the right time order
        self.barshift_value         : The portion a grouped bar chart will be out of the middle
        self.data_total             : Dictionary with totals of the data (of available scenarios in the dataframe)

        Returns:
        --------
        scenarios                   : A list of the base scenarios in the order of the 'all_scenarios'
        barshift                    : The value to use for barshifting (only <>0 with two scenarios)
        first_scenario_special_text : Does the upper bar needs to have it's value-text placed on a special place?
                                      True  -> the text-value needs to be placed a bit higher because the top scenario 
                                               is not significantly longer than than the bottom scenario
                                      False -> the text-value can be placed in a normal position (just right of the top scenario bar)
        first_scenario_line_start   : Does the line from the first scenario start at this first scenario or not? When not, start from the 2nd scenario.
                                      True  -> the line can start at the top scenario
                                      False -> the line needs to start at the bottom scenario because the top scenario is equal or shorter
        """
        # Check scenario-lists
        error_not_islist(self.all_scenarios,  "self.all_scenarios")
        error_not_islist(self.base_scenarios, "self.base_scenarios")

        # Check dictionary
        error_not_isdictionary(self.data_total, "self.data_total")

        # Filter all supported scenarios against the base scenarios. With this, we get the order of the 'all_scenarios'.
        scenarios = filter_lists(list1=self.all_scenarios, list2=self.base_scenarios)

        first_scenario_special_text = False
        first_scenario_line_start = True

        if len(scenarios)==2:
            barshift = self.barshift_value
            first_scenario_special_text = (self.data_total[scenarios[0]] < self.data_total[scenarios[1]]*1.1)
            first_scenario_line_start   = (self.data_total[scenarios[0]] > self.data_total[scenarios[1]])
        else:
            barshift = 0

        return scenarios, barshift, first_scenario_special_text, first_scenario_line_start

 
    def _plot_base_scenario_totals(self):
        """
        This function plots the base_scenario total bars:
        Determine whether the line needs to start from the first scenario.
        Plot the base_scenario total bars with the scenario label half way and the value label on the right of the bars
        Save the y-coordinate and the value of the total scenario in a dictionary for later

        Self variables
        --------------
        self.ax               : Axesobject for the generated subplot
        self.font             : All text in a chart has the same font
        self.fontsize         : All text in a chart has the same height
        self.colors           : Dictionary with colors
        self.barwidth         : A float with the width of the bars for measure or ratio
        self.data_total       : Dictionary (key=scenario) with the total value
        self.dict_totals      : Totals of the data (only one entry for the last total line underneath the detailed chart)
                                One entry each for the base scenarios, only one entry with the name of the first item of the compare scenarios
                                Combined with the Y-coordinate of the bar
        """
        # Check axis-object
        error_not_isaxes(self.ax, "self.ax")
        ax = self.ax
        
        # Check the base scenario totals
        scenarios, barshift, first_scenario_special_text, first_scenario_line_start = self._check_base_scenario_totals()
        # scenarios                   : A list of the base scenarios in the order of the 'all_scenarios'
        # barshift                    : The value to use for barshifting (only <>0 with two scenarios)
        # first_scenario_special_text : Does the upper bar needs to have its value-text placed on a special place?
        # first_scenario_line_start   : Does the line from the first scenario start at this first scenario or not? When not, start from the 2nd scenario.

        # For each of the (max two) base scenarios        
        for x, scenario in enumerate(scenarios):
            tot_base = self.data_total[scenario]
            yvalue = 2 + (([1, -1][x]) * barshift)   # x can only have a value of 0 or 1, so it takes the first value (1) or the second value (-1) out of the list

            # Does the line from the first scenario need to start at this first scenario?
            if first_scenario_line_start:
                # Yes, the line starts at the first scenario
                yvalue_line = yvalue
            else:
                # No, the line starts from the second scenario
                yvalue_line = 2 + (-1 * barshift)

            # Are we running the first or the second scenario right now? x==0 -> first scenario, x==1 -> second scenario
            if x==0:
                # The first scenario is running now
                # Put the label of the scenario half way on top of the bar
                ax.text(tot_base / 2, yvalue + self.barwidth*0.8, scenario, horizontalalignment='center', font=self.font, 
                        fontsize=self.fontsize, color=self.colors['text'])
            else:
                # The second scenario is running now, we need to set the first_scenario-variables to False
                first_scenario_special_text = False
                first_scenario_line_start = False
                # Put the label of the scenario half way underneath of the bar
                ax.text(tot_base / 2, yvalue - self.barwidth*1.4, scenario, horizontalalignment='center', font=self.font, 
                        fontsize=self.fontsize, color=self.colors['text'])
           
            # Plot bar
            self._plot_barh(y=yvalue, width=tot_base, scenario=scenario, height=self.barwidth, left=0, total=True)
            # Add valuelabel of the bar
            if first_scenario_special_text:
                ax.text(tot_base * 1.01, yvalue, str(tot_base), horizontalalignment='left', verticalalignment='bottom', 
                        font=self.font, fontsize=self.fontsize, color=self.colors['text'], fontweight='bold')
            else:
                self._fill_ax_bar_label(scenario, total=True)
        
            #Save values for later
            total_dict = dict()
            total_dict['yvalue'] = yvalue
            total_dict['total']  = tot_base
            self.dict_totals[scenario] = total_dict
        
        return

  
    def _plot_total_line(self):
        """
        The function _plot_total_line plots a line just after the detail bars and just before the last total bar. This bar just makes the chart a bit more
        like a table, where you can find a line just before the totals.
        
        Thanks to user jared on stackoverflow.com (https://stackoverflow.com/users/12131013) for helping me out
        with the starting coordinate of the line: https://stackoverflow.com/questions/76502232

        Self variables
        --------------
        self.ax                : Axesobject for the generated subplot
        self.compare_scenarios : List of compare scenarios
        self.colors            : Dictionary with colors
        self.dict_totals       : Totals of the data (only one entry for the last total line underneath the detailed chart)
                                 One entry each for the base scenarios, only one entry with the name of the first item of the compare scenarios
                                 Combined with the Y-coordinate of the bar
        """
        # Check axis-object
        error_not_isaxes(self.ax, "self.ax")
        ax = self.ax

        # Check compare scenarios
        error_not_islist(self.compare_scenarios, "self.compare_scenarios")
        # Check if empty list or not
        if self.compare_scenarios:
            # List is not empty
            compare_scenario = self.compare_scenarios[0]
        else:
            # List is empty
            raise ValueError("self.compare_scenarios is empty")

        # The figure needs to be drawn before the coordinate can be determined
        self.fig.draw_without_rendering()
        self.fig.tight_layout()

        ytickboxes = [l.get_window_extent() for l in ax.get_yticklabels()]
        ytickboxesdatacoords = [l.transformed(ax.transAxes.inverted()) for l in ytickboxes]

        # Get the minimum x-coordinate
        start_position = min([l.x0 for l in ytickboxesdatacoords])

        # Fixed maximum x-coordinate  #### TECHNICAL DEBT, this needs to be improved!
        end_position = 1.035

        # Y-coordinate just above the last total bar underneath the detail bars
        y_coordinate_line = self.dict_totals[compare_scenario]['yvalue'] + 0.7

        trans = ax.get_yaxis_transform()

        # Plot line
        ax.plot([start_position, end_position], [y_coordinate_line, y_coordinate_line], color=self.colors['totalline'], transform=trans, clip_on=False)

        return


    def _plot_base_scenario_details(self, dataframe):
        """
        The function _plot_base_scenario_details plots only the bars of the first base scenario, no value labels

        Parameters
        ----------
        dataframe           : pandas DataFrame with y-coordinates for base-scenario

        Self variables
        --------------
        self.barwidth       : A float with the width of the bars for measure or ratio
        self.base_scenarios : List of base scenarios
        """
        # Check dataframe
        error_not_isdataframe(dataframe, "dataframe")

        # Check base scenarios
        error_not_islist(self.base_scenarios, "self.base_scenarios")
        # Check if empty list or not
        if self.base_scenarios:
            # List is not empty
            base_scenario = self.base_scenarios[0]
        else:
            # List is empty
            raise ValueError("self.base_scenarios is empty")
        
        # Base scenario details: a list of y-coordinates and related data-values
        yvalue_base = list(dataframe['_CBC_Y1'])
        data_base = list(dataframe[base_scenario])
        
        # Plot the bars
        self._plot_barh(y=yvalue_base, width=data_base, scenario=base_scenario, height=self.barwidth, left=0)
        
        return


    def _plot_compare_scenario_details(self, dataframe):
        """
        The function _plot_compare_scenario_details plots the bars of the compare scenarios and also value labels on the right of the bar

        Parameters
        ----------
        dataframe              : pandas DataFrame with y-coordinates for compare-scenario

        Self variables
        --------------
        self.barwidth          : A float with the width of the bars for measure or ratio
        self.compare_scenarios : List of compare scenarios
        """
        # Check dataframe
        error_not_isdataframe(dataframe, "dataframe")

        # Check compare scenarios
        error_not_islist(self.compare_scenarios, "self.compare_scenarios")
        # Check if empty list or not
        if self.compare_scenarios:
            # List is not empty
            compare_scenario = self.compare_scenarios[0]
        else:
            # List is empty
            raise ValueError("self.compare_scenarios is empty")

        # Assign first and last compare scenario from the list as scenario 1 and scenario 2
        compare_scenario1 = self.compare_scenarios[0]
        compare_scenario2 = self.compare_scenarios[-1]

        # Scenario 1 - with numbers. Make a list of y-coordinates and data-values for those who are the 'top'-scenario.
        yvalue_compare = list(dataframe[dataframe['_CBC_TOPLAYER']==compare_scenario1]['_CBC_Y2'])
        data_compare1 = list(dataframe[dataframe['_CBC_TOPLAYER']==compare_scenario1][compare_scenario1])

        # Plot the bars and put the value-labels on.
        self._plot_barh(y=yvalue_compare, width=data_compare1, scenario=compare_scenario1, height=self.barwidth, left=0)
        self._fill_ax_bar_label(compare_scenario1)

        # Scenario 1 - without numbers. Make a list of y-coordinates and data-values for those who are the 'bottom'-scenario.
        yvalue_compare = list(dataframe[dataframe['_CBC_TOPLAYER']!=compare_scenario1]['_CBC_Y2'])
        data_compare1 = list(dataframe[dataframe['_CBC_TOPLAYER']!=compare_scenario1][compare_scenario1])

        # Plot only the bar (no value-labels)
        self._plot_barh(y=yvalue_compare, width=data_compare1, scenario=compare_scenario1, height=self.barwidth, left=0)

        # Check if scenario1 is not equal to scenario2        
        if compare_scenario1 != compare_scenario2:
            # There are two scenarios. Make a list of y-coordinates and data-values
            yvalue_compare = list(dataframe[dataframe['_CBC_TOPLAYER']==compare_scenario2]['_CBC_Y2'])
            data_compare2 = list(dataframe[dataframe['_CBC_TOPLAYER']==compare_scenario2][compare_scenario2])

            # Plot the bars and put the value-labels on. The second scenario is always on top
            self._plot_barh(y=yvalue_compare, width=data_compare2, scenario=compare_scenario2, height=self.barwidth, left=data_compare1)
            self._fill_ax_bar_label(compare_scenario2)

        return


    def _plot_compare_scenario_totals(self, dataframe):
        """
        The function _plot_compare_scenario_totals plots the total bar of the compare scenarios

        Parameters
        ----------
        dataframe              : pandas DataFrame with y-coordinates for compare-scenario

        Self variables
        --------------
        self.ax                : Axesobject for the generated subplot
        self.barwidth          : A float with the width of the bars for measure or ratio
        self.colors            : Dictionary with colors
        self.compare_scenarios : List of compare scenarios
        self.data_total        : Dictionary (key=scenario) with the total value
        self.dict_totals       : Totals of the data (only one entry for the last total line underneath the detailed chart)
                                 One entry each for the base scenarios, only one entry with the name of the first item of the compare scenarios
                                 Combined with the Y-coordinate of the bar
        self.font              : All text in a chart has the same font
        self.fontsize          : All text in a chart has the same height
        """
        # Check axis-object
        error_not_isaxes(self.ax, "self.ax")
        ax = self.ax

        # Check dataframe
        error_not_isdataframe(dataframe, "dataframe")

        # Check compare scenarios
        error_not_islist(self.compare_scenarios, "self.compare_scenarios")
        # Check if empty list or not
        if self.compare_scenarios:
            # List is not empty
            compare_scenario = self.compare_scenarios[0]
        else:
            # List is empty
            raise ValueError("self.compare_scenarios is empty")
       
        # Assign first and last compare scenario from the list as scenario 1 and scenario 2
        compare_scenario1 = self.compare_scenarios[0]
        compare_scenario2 = self.compare_scenarios[-1]
        
        # Get the sum of both scenarios
        tot_comp1 = self.data_total[compare_scenario1]
        tot_comp2 = self.data_total[compare_scenario2]
        
        # The Y-coordinate is 1.5 below the lowest detail horizontal bar
        yvalue = dataframe['_CBC_Y2'].min() - 1.5 

        # Prepare storage of the Y-coordinate in a dictionary and the total (later on in this function)
        total_dict = dict()
        total_dict['yvalue'] = yvalue

        # Plot the horizontal bar for the first compare scenario
        self._plot_barh(y=yvalue, width=tot_comp1, scenario=compare_scenario1, height=self.barwidth, left=0, total=True, zorder=0)
        
        # Check if there are two separate compare scenarios or check that the first scenario is the same as the last scenario
        if compare_scenario1 != compare_scenario2:
            # Yes, there are two compare scenarios. In that case we set the scenario abbreviation underneath the bar near the center of the length of the bar
            ax.text(tot_comp1 / 2, yvalue - self.barwidth*1.2, compare_scenario1, horizontalalignment='center', font=self.font, fontsize=self.fontsize, color=self.colors['text']) #, verticalalignment='center')

            # Now plot the horizontal bar of the second compare scenario as a stacked bar on top of the first bar
            self._plot_barh(y=yvalue, width=tot_comp2, scenario=compare_scenario2, height=self.barwidth, left=tot_comp1, total=True, zorder=0)
            # Write the total sum of the lenght of both bars combines on the right of the second (stacked) bar
            self._fill_ax_bar_label(compare_scenario2, total=True)
            # Also here, set the scenario abbreviation of the second scenario underneath the second (stacked) bar near the center of this addition
            ax.text(tot_comp1 + (tot_comp2 / 2), yvalue - self.barwidth*1.2, compare_scenario2, horizontalalignment='center', font=self.font, fontsize=self.fontsize, color=self.colors['text']) #, verticalalignment='center')
            # Sum both totals and store it in the dictionary
            total_dict['total']  = tot_comp1 + tot_comp2
        else:
            # No, there is just one compare scenario. Write the length of this one horizontal bar on the right
            self._fill_ax_bar_label(compare_scenario1, total=True)
            # Store this total in the dictionary
            total_dict['total']  = tot_comp1
            # Put the scenario text underneath the bar near the center of the length of the bar
            ax.text(tot_comp1 / 2, yvalue - self.barwidth*1.4, compare_scenario1, horizontalalignment='center', font=self.font, fontsize=self.fontsize, color=self.colors['text']) #, verticalalignment='center')

        
        # As the total for the compare scenarios is just one horizontal bar (one horizontal stacked bar in case of two compare scenarios)
        self.dict_totals[compare_scenario1] = total_dict    # Always assign the information to the first compare scenario

        return

 
    def _plot_lines_with_total_delta(self, dataframe):
        """
        Function _plot_lines_with_total_delta plots the line(s) between the base total bar(s) and the compare total bar 
        and make the delta on total level visible

        Parameters
        ----------
        dataframe              : pandas DataFrame with y-coordinates for compare-scenario

        Self variables
        --------------
        self.ax                : Axesobject for the generated subplot
        self.barwidth          : A float with the width of the bars for measure or ratio
        self.base_scenarios    : List of base scenarios
        self.colors            : Dictionary with colors
        self.compare_scenarios : List of compare scenarios
        self.decimals_totals   : Number of decimals for total information
        self.dict_totals       : Totals of the data (only one entry for the last total line underneath the detailed chart)
                                 One entry each for the base scenarios, only one entry with the name of the first item of the compare scenarios
                                 Combined with the Y-coordinate of the bar
        self.font              : All text in a chart has the same font
        self.fontsize          : All text in a chart has the same height
        self.linewidth_delta   : The width of the delta-lines with the good or bad colors
        self.linewidth_line_n  : The normal width of the lines
        """
        # Check axis-object
        error_not_isaxes(self.ax, "self.ax")
        ax = self.ax

        # Check dataframe
        error_not_isdataframe(dataframe, "dataframe")

        # Check the base scenario totals
        scenarios, barshift, first_scenario_special_text, first_scenario_line_start = self._check_base_scenario_totals()
        # scenarios                   : A list of the base scenarios in the order of the 'all_scenarios'
        # barshift                    : The value to use for barshifting (only <>0 with two scenarios)
        # first_scenario_special_text : Does the upper bar needs to have its value-text placed on a special place?
        # first_scenario_line_start   : Does the line from the first scenario start at this first scenario or not? When not, start from the 2nd scenario.

        # Endpoint of the vertical line
        ymin_start = dataframe['_CBC_Y2'].min() - 3
        
        for y_extra, scenario in enumerate(self.base_scenarios):
            base_dict  = self.dict_totals[scenario]
            total_base = base_dict['total']
            if y_extra == 0 or first_scenario_line_start:
                y_base     = base_dict['yvalue']
              
            comp_dict  = self.dict_totals[self.compare_scenarios[0]]
            total_comp = comp_dict['total']
            y_comp     = comp_dict['yvalue']
            
            ymin = ymin_start - (y_extra * 1.4)
            
            # Plot a line at the total level from one of the base scenarios to under the compare scenario bar
            plot_line_within_ax(ax=ax, xbegin=total_base, ybegin=y_base-(self.barwidth/2), xend=total_base, yend=ymin, 
                                linecolor=self.colors['line'], arrowstyle='-', linewidth=self.linewidth_line_n, endpoints=False, endpointcolor=None, zorder=0)

            # Plot a line at the total level from the compare scenario to under the compare scenario bar
            plot_line_within_ax(ax=ax, xbegin=total_comp, ybegin=y_comp-(self.barwidth/2), xend=total_comp, yend=ymin, 
                                linecolor=self.colors['line'], arrowstyle='-', linewidth=self.linewidth_line_n, endpoints=False, endpointcolor=None, zorder=0)
        
            color = self.good_or_bad_color(differencevalue=total_comp-total_base)
        
            # Plot horizontal bar in a good or bad color
            plot_line_within_ax(ax=ax, xbegin=total_comp, ybegin=ymin, xend=total_base, yend=ymin, endpoints=False, linecolor=color, arrowstyle='-', linewidth=self.linewidth_delta)
        
            # Set the value next to the horizontal bar
            value = optimize_data(data=(total_comp-total_base), numerator=1, denominator=1, decimals=self.decimals_totals)
            # Dataframe-values are not the same as internal int or float. To avoid importing numpy for example a numpy.integer we do a string to non-string conversion
            value = string_to_value(str(value))
        
            ax.text(total_comp - (total_comp-total_base)/2, ymin-0.8, self.convert_to_delta_string(value), horizontalalignment='center', #verticalalignment='center', 
                    font=self.font, fontsize=self.fontsize, color=self.colors['text'],zorder=10)

        return


    def _add_deltavalues_to_dataframe(self, dataframe):
        """
        This function adds the deltacolumns to the dataframe and calculates the delta.
        
        Precondition: Everything needs to be aggregated at 'category of interest'-level.

        Parameters
        ----------
        dataframe              : pandas DataFrame for the column names
        
        Self variables
        --------------
        self.all_scenarios     :
        self.base_scenarios    : List of base scenarios
        self.compare_scenarios : List of compare scenarios
        self.barshift          : The value to use for the barshift. When no barshift neccessairy, then barshift is equal to zero
        self.barshift_value    : The value which can be used for the barshift. This value is centrally defined
        
        Returns
        -------
        export_dataframe       : pandas DataFrame with two additional columns '_CBC_DELTA1' and '_CBC_DELTA2'
        """
        # Check dataframe
        error_not_isdataframe(dataframe, 'dataframe')

        # Check pre-condition
        if not list1_is_subset_list2(list1=list(dataframe.columns), list2=['_Category', '_CBC_TOPLAYER']+self.year_column+self.all_scenarios):
            raise ValueError("Dataframe is not aggregated at 'category of interest'-level: "+str(list(dataframe.columns)))

        # Split the scenarios into easy to handle variables
        base_scenario     = self.base_scenarios[0]      # The first scenario is the scenario to use as the base scenario
        compare_scenario1 = self.compare_scenarios[0]   # The first scenario is the scenario to compare with against the base for the first compare-column
        compare_scenario2 = self.compare_scenarios[-1]  # The last scenario (out of max 2 scenarios) to compare with against the base for the second compare-column
                                                        #     It is possible that the last scenario is equal to the first scenario (in case of one entry in the list)

        # Prepare the export variable
        export_dataframe = dataframe.copy()

        # Initialize barshift when we compare the base scenario with the compare scenario
        if len(self.base_scenarios) != 0 and len(self.compare_scenarios) != 0:
            # Yes, there will be two bars to compare, initialize the barshift
            self.barshift = self.barshift_value

        # Make first column DELTA1 with the delta-values for the categories for the comparison with the first compare scenario
        export_dataframe.insert(loc = len(export_dataframe.columns), column='_CBC_DELTA1', value=0)              # Make column
        export_dataframe['_CBC_DELTA1'] = export_dataframe[compare_scenario1] - export_dataframe[base_scenario]  # Calculate delta

        # Make second column DELTA2 with the delta-values for the categories for the comparison with the second compare scenario
        export_dataframe.insert(loc = len(export_dataframe.columns), column='_CBC_DELTA2', value=0)              # Always make the column
        # Check if there is a 2nd compare scenario
        if compare_scenario1 != compare_scenario2:
            # Only fill column if there are two compare scenario's
            export_dataframe['_CBC_DELTA2'] = export_dataframe['_CBC_DELTA1'] + export_dataframe[compare_scenario2]
        # else:
            # No, there is no 2nd scenario, do nothing

        return export_dataframe


    def _prepare_delta_bar(self, dataframe):
        """
        The function _prepare_delta_bar adds the base-column to the dataframe and calculates the waterfall-leaving coordinate for the small lines.
        
        # Precondition: Columns for Delta1 and Delta2 needs to be available
        
        Parameters
        ----------
        dataframe           : pandas DataFrame with _CBC_DELTA1-column and _CBC_DELTA2-column

        Self variables
        --------------
        self.base_scenarios : List of base scenarios
        self.dict_totals    : Totals of the data (only one entry for the last total line underneath the detailed chart)
                              One entry each for the base scenarios, only one entry with the name of the first item of the compare scenarios
                              Combined with the Y-coordinate of the bar

        Returns
        -------
        export_dataframe    : pandas DataFrame with additional column '_CBC_BASE'
        """
        # Check dataframe
        error_not_isdataframe(dataframe, "dataframe")
        # Check precondition
        if not list1_is_subset_list2(list1=["_CBC_DELTA1", "_CBC_DELTA2"], list2=list(dataframe.columns)):
            raise ValueError("Dataframe doesn't contain both delta-columns '_CBC_DELTA1' and '_CBC_DELTA2': "+str(list(dataframe.columns)))

        # Check base scenarios
        error_not_islist(self.base_scenarios, "self.base_scenarios")

        # Check if empty list or not and get first base scenario
        if self.base_scenarios:
            # List is not empty
            base_scenario = self.base_scenarios[0]
        else:
            # List is empty
            raise ValueError("self.base_scenarios is empty")

        # Check dictionary with total-information
        error_not_isdictionary(self.dict_totals, "self.dict_totals")

        # Get delta_base_value
        if base_scenario in self.dict_totals.keys():
            base_dict = self.dict_totals[base_scenario]
            delta_base_value = base_dict['total']
        else:
            raise ValueError(str(base_scenario)+" not available in total-information "+str(self.dict_totals))

        # Make column with the base_values for each delta
        # Make a copy of the dataframe as the return value
        export_dataframe = dataframe.copy()

        # Add column "_CBC_BASE"
        export_dataframe.insert(loc = len(export_dataframe.columns), column='_CBC_BASE', value=0)

        # Make _CBC_BASE the sum of the two deltas
        export_dataframe['_CBC_BASE'] = export_dataframe['_CBC_DELTA1'] + export_dataframe['_CBC_DELTA2']

        # Make the sum of these deltas cumulative
        export_dataframe['_CBC_BASE'] = export_dataframe['_CBC_BASE'].expanding().sum()

        # Now add the base value to the cumulative deltas to make it a waterfall
        export_dataframe['_CBC_BASE'] = export_dataframe['_CBC_BASE'] + delta_base_value

        return export_dataframe


    def _plot_delta_bar(self, dataframe):
        """
        The function _plot_delta_bar plots the lines between the delta-bars first and then the delta-bars second.
        
        # Precondition: DataFrame needs to have the columns _CBC_BASE, _CBC_DELTA1 and _CBC_Y2

        Parameters
        ----------
        dataframe              : pandas DataFrame with the columns _CBC_BASE, _CBC_DELTA1 and _CBC_Y2

        Self variables
        --------------
        self.ax                : Axesobject for the generated subplot
        self.barwidth          : A float with the width of the bars for measure or ratio
        self.base_scenarios    : List of base scenarios
        self.colors            : Dictionary with colors
        self.compare_scenarios : List of compare scenarios
        self.data_text         : Dictionary with the number of the matplotllib-ax-containers of the bar-data including the texts of the bars
        self.data_total        : Dictionary (key=scenario) with the total value
        self.dict_totals       : Totals of the data (only one entry for the last total line underneath the detailed chart)
                                 One entry each for the base scenarios, only one entry with the name of the first item of the compare scenarios
                                 Combined with the Y-coordinate of the bar
        self.font              : All text in a chart has the same font
        self.fontsize          : All text in a chart has the same height
        self.linewidth_bar     : The width of the lines from a bar
        self.linewidth_line_n  : The normal width of the lines
        self.padding           : Padding between the bars and the text
        """
        # Check parameter
        error_not_isdataframe(dataframe, "dataframe")
        if not list1_is_subset_list2(list1=['_CBC_BASE', '_CBC_DELTA1', '_CBC_Y2'], list2=list(dataframe.columns)):
            raise ValueError("Dataframe doesn't contain these columns '_CBC_BASE', '_CBC_DELTA1' and '_CBC_Y2': "+str(list(dataframe.columns)))

        # Check ax
        error_not_isaxes(self.ax, "self.ax")
        
        # Check dictionary of totals
        error_not_isdictionary(self.dict_totals, "self.dict_totals")
        error_not_isdictionary(self.data_total, "self.data_total")
        
        # Check scenarios
        error_not_islist(self.base_scenarios, "self.base_scenarios")
        error_not_islist(self.compare_scenarios, "self.compare_scenarios")

        # Step 1: Make lines between the future bars so it looks like a waterfall
        ax = self.ax
        delta_lines = list(dataframe['_CBC_BASE'])
        yvalues     = list(dataframe['_CBC_Y2'])
        
        for yvalue_van, yvalue_tot, xvalue in zip(yvalues[:-1], yvalues[1:], delta_lines[:-1]):
            point1 = ( xvalue, (yvalue_van - (self.barwidth / 2)) )
            point2 = ( xvalue, (yvalue_tot + (self.barwidth / 2)) )
            plot_line_within_ax(ax=ax, xbegin=point1[0], ybegin=point1[1], xend=point2[0], yend=point2[1], linecolor=self.colors['line'], 
                                arrowstyle='-', linewidth=self.linewidth_line_n, endpoints=False, endpointcolor=None, zorder=0)

        # Prepare the last line from the delta to the total-bar
        comp_scenario = self.compare_scenarios[0]
        if comp_scenario in self.dict_totals.keys():
            comp_dict = self.dict_totals[comp_scenario]
            delta_comp_value = comp_dict['total']
            yvalue_tot = comp_dict['yvalue']
        else:
            raise ValueError(str(comp_scenario)+" not available in total-information "+str(self.dict_totals))
        
        # Plot the last line
        plot_line_within_ax(ax=ax, xbegin=delta_comp_value, ybegin=yvalues[-1] - (self.barwidth / 2), xend=delta_comp_value, 
                            yend=yvalue_tot + (self.barwidth / 2), linecolor=self.colors['line'], arrowstyle='-', 
                            linewidth=self.linewidth_line_n, endpoints=False, endpointcolor=None, zorder=0)

        # Step 2: Plot the delta-bars
        # Prepare the bars
        base_scenario = self.base_scenarios[0]
        base_value    = self.data_total[base_scenario]
        yvalues       = list(dataframe['_CBC_Y2'])
        delta_lines   = [base_value]+list(dataframe['_CBC_BASE'])[:-1]
        height        = list(dataframe['_CBC_DELTA1'])
        colors        = [self.good_or_bad_color(differencevalue=x) for x in height]
        
        # Plot the bars
        ax.barh(y=yvalues, width=height, color=colors, height=self.barwidth, left=delta_lines, linewidth=self.linewidth_bar, 
                        edgecolor=colors, label='AC', hatch=None)
        
        self.data_text['delta'] = len(ax.containers)-1
        
        label_value_list = self.convert_to_delta_string(height)
        
        if len(label_value_list) > 0:
            ax.bar_label(ax.containers[self.data_text['delta']], labels=label_value_list, fmt= '%0i', label_type='edge', padding = self.padding, 
                         font=self.font, fontsize=self.fontsize, zorder=10)

        # Plot the downarrow (\u2193). The up-arrow has code: \u2191. \u0394 is a delta-sign
        ax.text(base_value, yvalues[0]+0.75, "\u0394"+base_scenario+"(\u2193)", horizontalalignment='left', font=self.font, 
                             fontsize=self.fontsize, color=self.colors['text'])

        return


    def _plot_detail_delta(self, dataframe):
        """
        The function _plot_detail_delta prepares the delta-bar and finally plots them.
        
        # Precondition: all detail delta-info is available
        #               line from the base scenarios to the compare scenarios is already available       

        Parameters
        ----------
        dataframe : pandas DataFrame
        """
        # Check parameter
        error_not_isdataframe(dataframe, "dataframe")
        
        dataframe = self._prepare_delta_bar(dataframe)
        self._plot_delta_bar(dataframe)
        
        return


    def _determine_y_ax_category_labels(self, dataframe): 
        """
        The function _determine_y_ax_category_labels makes two lists: 
        one list of y-coordinates for the category labels. 
        one list for the names to use for the category labels.

        # Precondition: Columns for Y2 and category-of-interest needs to be available

        Parameters
        ----------
        dataframe       : pandas DataFrame with category-of-interest and Y2-column

        Self variables
        --------------
        self.other_text : Text that will be displayed instead of 'OTHER'

        Returns
        -------
        yvalue          : list of y-values where the categories need to be placed
        category_labels : list of names of the categories
        """
        # Check dataframe
        error_not_isdataframe(dataframe, "dataframe")
        # Check precondition
        if not list1_is_subset_list2(list1=["_CBC_Y2", "_Category"], list2=list(dataframe.columns)):
            # We miss the needed columns
            raise ValueError("Dataframe doesn't contain both delta-columns '_CBC_Y2' and '_Category': "+str(list(dataframe.columns)))

        # Make a list of y-coordinates for the category labels
        yvalue = list(dataframe["_CBC_Y2"])
        
        # Make a list of the names to use for the category labels
        category_labels = list(dataframe["_Category"])
        # Do we have a replacement-text for 'OTHER'?
        if self.other_text is not None:
            # Yes, we have a other_text, but is it of type string?
            error_not_isstring(self.other_text, 'self.other_text')
            # Is 'OTHER' available in the data?
            if "OTHER" in category_labels:
                # 'OTHER' is available in the data, we can replace the text
                category_labels[category_labels.index("OTHER")] = self.other_text

        return yvalue, category_labels


    def _determine_y_ax_total_labels(self): 
        """
        The function _determine_y_ax_total_labels makes 3 lists:
        one list of y-coordinates for total labels. 
        one list of names for the total bars
        one list of y-coordinates for the zeroline
        
        Self variables
        --------------
        self.base_scenarios    : List of base scenarios
        self.compare_scenarios : List of compare scenarios
        self.dict_totals       : Totals of the data (only one entry for the last total line underneath the detailed chart)
                                 One entry each for the base scenarios, only one entry with the name of the first item of the compare scenarios
                                 Combined with the Y-coordinate of the bar
        self.total_text        : Text that will be added to the 'total'-bars

        Returns
        -------
        yvalue           : list of y-values where the categories need to be placed
        category_labels  : list of names of the categories
        yvalue_zero      : list of coordinates for the zero-lines (can have more entries than 'yvalue'-list)
        """
        # Check self variables
        error_not_islist(self.base_scenarios, 'self.base_scenarios')
        error_not_islist(self.compare_scenarios, 'self.compare_scenarios')
        error_not_isdictionary(self.dict_totals, 'self.dict_totals')
        
        # Initialize variables
        yvalue      = list()   # y-coordinates for total labels
        total_names = list()   # names for total bar
        yvalue_zero = list()   # y-coordinates for zeroline of the total bars

        for scenario in self.dict_totals.keys():
            totals = self.dict_totals[scenario]
            # Check if scenario is a base scenario or a compare scenario
            if scenario in self.compare_scenarios:
                # Yes, scenario is a compare scenario, check if there is text for the total bars
                if self.total_text is not None:
                    # Yes, there is something for the total bars, but is it text?
                    error_not_isstring(self.total_text, 'self.total_text')
                    # Yes, it is text! Use this text.
                    total_names.append(self.total_text)
                else:
                    # No, there is no text for the total bars. Then take the default: 'Total'
                    total_names.append('Total')
                yvalue.append(totals['yvalue'])
            else:
                # No, scenario is a base scenario
                if scenario == self.base_scenarios[0]:
                    # Yes, it is the most important base scenario, check if there is text for the total bars
                    if self.total_text is not None:
                        # Yes, there is something for the total bars, but is it text?
                        error_not_isstring(self.total_text, 'self.total_text')
                        # Yes, it is text! Use this text.
                        total_names.append(self.total_text)
                    else:
                        # No, there is no text for the total bars. Then take the default: 'Total'
                        total_names.append('Total')
                    yvalue.append(totals['yvalue'])
            yvalue_zero.append(totals['yvalue'])

        return yvalue, total_names, yvalue_zero


    def _plot_y_axis_labels(self, dataframe):
        """
        The function _plot_y_axis_labels plots the labels of the detail bars, the labels of the total bars as well as the y-axisline (zeroline) of all bars.

        Parameters
        ----------
        dataframe           : pandas DataFrame

        Self variables
        --------------
        self.ax             : Axesobject for the generated subplot
        self.barwidth       : A float with the width of the bars for measure or ratio
        self.colors         : Dictionary with colors
        self.font           : All text in a chart has the same font
        self.fontsize       : All text in a chart has the same height
        self.linewidth_zero : The width of the zerolines
        """
        # Check parameter
        error_not_isdataframe(dataframe, "dataframe")

        # Check ax
        error_not_isaxes(self.ax, "self.ax")

        ax = self.ax
        
        # yvalue1 = y-coordinate of the details, bar_names1 = names of the detail bars
        yvalue1, bar_names1 = self._determine_y_ax_category_labels(dataframe=dataframe)
        
        # yvalue2 = y-coordinate of the total bars, bar_names2 = names of the total bars
        yvalue2, bar_names2, yvalue_zero = self._determine_y_ax_total_labels()

        # Merge together, so the 
        yvalue = list(yvalue1)
        yvalue.extend(yvalue2)
        bar_names = list(bar_names1)
        bar_names.extend(bar_names2)
        
        # This is the "Zeroline" (line on the y-axis) for the detail bars
        ymax = max(yvalue1) + 0.75
        ymin = min(yvalue1) - 0.6
        plot_line_within_ax(ax=ax, xbegin=0, ybegin=ymax, xend=0, yend=ymin, linecolor=self.colors['zeroline'], arrowstyle='-', linewidth=self.linewidth_zero, endpoints=False, endpointcolor=None)
        
        # These are the "Zerolines" (line on the y-axis) for the total bars
        for y in yvalue_zero:
            plot_line_within_ax(ax=ax, xbegin=0, ybegin=y+self.barwidth*0.8, xend=0, yend=y-self.barwidth*0.8, linecolor=self.colors['zeroline'], arrowstyle='-', linewidth=self.linewidth_zero, endpoints=False, endpointcolor=None)
        
        # Put the category-names on the chart
        ax.set_yticks(yvalue, bar_names, font=self.font, fontsize=self.fontsize)
        
        # As fontweight can not be used in ax.set_yticks, we need to solve it like this
        # Modify the y-axis-labels
        labels = ax.get_yticklabels()
        for label in labels:
            ycoordinate = label.get_position()[1]
            if ycoordinate in yvalue2:
                # It is a total bar
                label.set_weight('bold')

        return        


    def _fill_chart(self):
        """
        The function _fill_chart orchestrates other functions for plotting the total base scenario bars, the detail base scenario bars,
        the detail compare scenario bars, the total compare bars and the category-labeling and zerolines on the y-axis.

        Self variables
        --------------
        self.data : pandas DataFrame with detail values
        """
        # Check dataframe
        error_not_isdataframe(self.data, 'self.data')

        dataframe = self.data

        # Base scenarios
        # Plot the total base scenario bars with the value labels        
        self._plot_base_scenario_totals()

        # Plot the detail base scenario bars with the value labels
        self._plot_base_scenario_details(dataframe=dataframe)

        # Compare scenarios
        # Plot the total compare scenario bars with the value labels
        self._plot_compare_scenario_details(dataframe=dataframe)
        # Plot the detail compare scenario bars with the value labels
        self._plot_compare_scenario_totals(dataframe=dataframe)

        # Plot the lines between the total base bars and the total compare bar and make a delta on total level
        self._plot_lines_with_total_delta(dataframe=dataframe)

        # Plot the delta-bars as a waterfall
        self._plot_detail_delta(dataframe=dataframe)

        # Plot the category-names of the detail bars and the total bars and plot the y-axis (zeroline)
        self._plot_y_axis_labels(dataframe=dataframe)

        return 


    def _plot_barh(self, y, width, scenario, height, left=0, total=False, zorder=None):
        """
        The function _plot_barh plots horizontal bars. With scenario FC it makes new lists of coordinates and values where there is something to plot.

        Parameters
        ----------
        y                  : List of y-coordinates or Float of one y-coordinate
        width              : List of length of horizontal bars or Float of one length of a horizontal bar
        scenario           : String with scenario
        height             : Float of the width of the horizontal bars
        left               : List of x-coordinates or float of a x-coordinate where stacked horizontal bar(s) start
                             Default value: 0 (No stacking of bars)
        total              : Boolean if the bar is a total horizontal bar (True) or a detail horizontal bar (False)
                             Default value: False (Detail horizontal bar(s))
        zorder             : Float or Integer of the 'stacking value' of lines and objects. Higher zorder-values will be drawn later.
                             Default value: None (No zorder-value will be passed through the line or object/bar)

        Self variables
        --------------
        self.ax            : Axesobject for the generated subplot
        self.colors        : Dictionary with colors
        self.data_text     : Dictionary with the number of the matplotllib-ax-containers of the bar-data including the texts of the bars
        self.hatch         : String with pattern for hatched. More elements is more density
        self.linewidth_bar : The width of the lines from a bar
        """
        # Check parameter scenario
        error_not_isstring(scenario, "scenario")
        # Is it a valid scenario?
        if not scenario in self.data_scenarios:
            # Not an existing scenario
            raise ValueError('Scenario "'+str(scenario)+'" is not in the list of available scenarios: '+str(self.data_scenarios))

        # Check parameter total
        error_not_isboolean(total, "total")

        # Check axis-object
        error_not_isaxes(self.ax, "self.ax")
        ax = self.ax

        # PY, PL or AC
        if scenario in ['PY', 'PL', 'AC']:
             # Scenario is PY or PL or AC
             if zorder is None:
                 # Zorder has no defined value
                 ax.barh(y=y, width=width, color=self.colors[scenario][0], height=height, linewidth=self.linewidth_bar, 
                         edgecolor=self.colors[scenario][1], label=scenario)
             else:
                 # Zorder has a defined value
                 ax.barh(y=y, width=width, color=self.colors[scenario][0], height=height, linewidth=self.linewidth_bar, 
                         edgecolor=self.colors[scenario][1], label=scenario, zorder=zorder)

        # FC
        if scenario == 'FC':
            # Scenario is FC
            if islist(y):
                # Make new lists with only the FC-information. 0-values needs to be excluded, or else the horizontal bars will include 0-value bars
                y2 = [i for j,i in enumerate(y) if width[j] != 0]    # Y-coordinates for widths <> 0
                width2 = [i for i in width if i !=0]                 # Widths for widths <> 0
                if not islist(left):
                    # Left is a single value, expand it to a list of length or the y-coordinates
                    left2 = [left] * len(y2)                         # Left-values for widths <> 0
                else:
                    # Left is a list of values
                    left2 = [i for j,i in enumerate(left) if width[j] != 0]   # Left-values for widths <> 0
                # Plot the horizontal bar based on the new lists without widths==0
                ax.barh(y=y2, width=width2, color=self.colors['FC'][0], height=height, left=left2, linewidth=self.linewidth_bar, 
                        edgecolor=self.colors['FC'][1], label='FC', hatch=self.hatch)

            else:
                # Just plot a single horizontal bar
                ax.barh(y=y, width=width, color=self.colors['FC'][0], height=height, left=left, linewidth=self.linewidth_bar, 
                        edgecolor=self.colors['FC'][1], label='FC', hatch=self.hatch)

        # Will the label be of a total bar (True) or not (False)
        if not total:
            # Total is False. It is detail information. Add the data-labels in the dictionary of the scenario
            self.data_text[scenario] = len(ax.containers)-1
        else:
            # Total is True. It is total-bar information. Add the data-label(s) in the dictionary of the scenario+"TOT" (so they will not overwrite detailinfo)
            self.data_text[scenario+'TOT'] = len(ax.containers)-1

        return


    def _fill_ax_bar_label(self, scenario, total=False):
        """
        The function _fill_ax_bar_label fills the valuelabels for the horizontal bars.
        
        Parameters
        ----------
        scenario              : String with the scenario
        total                 : Boolean switch for indicating a total value of this scenario (True) or detail values of this scenario (False)
                                Default value: False (detail values)

        Self variables
        --------------
        self.ax               : Axesobject for the generated subplot
        self.colors           : Dictionary with colors
        self.data_scenarios   : List of available scenarios
        self.data_text        : A dictionary with the number of the matplotlib-ax-containers of the bar-data including the texts of the bars
        self.decimals_details : Number of decimals for detailed information
        self.decimals_totals  : Number of decimals for total information
        self.font             : All text in a chart has the same font
        self.fontsize         : All text in a chart has the same height
        self.padding          : Padding between the bars and the text

        Returns
        -------
        return_value          : Return_value only for automatic testing
        """
        # Check axis-object
        error_not_isaxes(self.ax, "self.ax")
        ax = self.ax

        # Check parameter scenario
        error_not_isstring(scenario, "scenario")
        # Is it a valid scenario?
        if not scenario in self.data_scenarios:
            # Not an existing scenario
            raise ValueError('Scenario "'+str(scenario)+'" is not in the list of available scenarios: '+str(self.data_scenarios))

        # Check parameter total
        error_not_isboolean(total, "total")

        # Will the label be of a total bar (True) or not (False)
        if total:
            # Yes, label will be of a total bar
            fontweight = 'bold'
            used_scenario = scenario+"TOT"
            format_string = formatstring(self.decimals_totals)
        else:
            # No, label will be of a normal bar
            fontweight = 'normal'
            used_scenario = scenario
            format_string = formatstring(self.decimals_details)
            
        # Puts the values after the horizontal bars.
        return_value = ax.bar_label(ax.containers[self.data_text[used_scenario]], fmt=format_string, label_type='edge', padding=self.padding, 
                                    font=self.font, fontsize=self.fontsize, fontweight=fontweight, color=self.colors['text'])

        return return_value  # Return_value only for automatic testing
    

    def _dataframe_keep_only_relevant_columns(self, dataframe, keep_date=False):
        """
        The function _dataframe_keep_only_relevant_columns narrows the DataFrame down to the needed columns.

        Parameters
        ----------
        dataframe        : pandas DataFrame with a lot of columns.
        keep_date        : Boolean switch for taking some date-related columns as relevant (True) together with the scenario columns or
                           only the scenario columns (False)
                           Default value: False (only scenario columns)

        Self variables
        --------------
        self.all_header_fields : List of all supported date columns and all supported scenarios
        self.all_scenarios     : List of Previous Year, PLan, ACtual, ForeCast [PY, PL, AC, FC] (in order of time)

        Returns
        -------
        export_dataframe       : pandas DataFrame with at least the columns '_Category' and all the supported scenarios
        """
        # Check parameters
        error_not_isdataframe(dataframe, "dataframe")
        error_not_isboolean(keep_date, "keep_date")

        # Check other important fields
        error_not_islist(self.all_header_fields, "self.all_header_fields")
        error_not_islist(self.all_scenarios, "self.all_scenarios")

        # We want the headers '_Category' and some header fields depending on 'keep_date'.
        if keep_date:
            wanted_headers = ['_Category'] + self.all_header_fields
        else:
            wanted_headers = ['_Category'] + self.all_scenarios

        # Search for available headers
        available_headers = dataframe_search_for_headers(dataframe, search_for_headers=wanted_headers, error_not_found=False)

        # We only need the data from these columns for the purpose of this chart
        export_dataframe = dataframe[available_headers].copy()

        return export_dataframe


    def _dataframe_aggregate(self, dataframe, wanted_headers):
        """
        The function _dataframe_aggregate aggregates (sums) the DataFrame by the wanted headers (which should include '_Category').

        Parameters
        ----------
        dataframe        : pandas DataFrame with at least a category of interest column.
        wanted_headers   : column headers that will be used (also with the category of interest columnname)
        
        Returns
        -------
        export_dataframe : aggregated pandas DataFrame
        """
        # Check parameters
        error_not_isdataframe(dataframe, "dataframe")
        error_not_islist(wanted_headers, "wanted_headers")

        # Search for available headers. Check for dataframe and wanted_headers-list is in the called function.
        available_headers = dataframe_search_for_headers(dataframe, search_for_headers=wanted_headers, error_not_found=False)

        if '_Category' not in available_headers:
            raise ValueError("Available headers does not contain the category of interest: "+str(available_headers))

        # Aggregate data
        export_dataframe = dataframe.groupby(available_headers).sum().reset_index().copy()

        return export_dataframe 


    def _dataframe_find_category_of_interest(self, dataframe):
        """
        The function _dataframe_find_category_of_interest will search for the first available category that is not known in the self.all_header_fields.
        This function will only do this if category-of-interest is not provided (self.category).

        Parameters
        ----------
        dataframe              : pandas DataFrame for the column names

        Self variables
        --------------
        self.all_header_fields : List of all supported date columns and all supported scenarios
        self.category          : Column-name of the category-of-interest (input as parameter of this class, output as checked column name)

        Returns
        -------
        export_category        : Category of interest
        """
        # Check dataframe
        error_not_isdataframe(dataframe, 'dataframe')

        # Declare export variable
        export_category = None

        # Check if the category of interest was provided
        if self.category is None:
            # Category of interest was not provided
            export_category = [x for x in dataframe.columns if x not in self.all_header_fields]

            # Check if there were column names found other than the supported date and scenario column names
            if len(export_category) == 0:
                # No, there were no column names found other than the supported date and scenario column names
                raise ValueError('No fields available for the category of interest in column headers: '+str(list(dataframe.columns)))
            # Keep first value as category of interest. Update export variable and the self-variable
            export_category = export_category[0]
            self.category = export_category
        else:
            # Category of interest was provided, copy it into the export variable
            export_category = self.category

            # Check if the category of interest is in the supported date columns or supported scenarios
            if export_category in self.all_header_fields:
                # Yes, the category is one of the supported date columns or supported scenarios
                raise ValueError('Field '+str(export_category)+' is available in supported date columns or supported scenarios '+str(self.all_header_fields))

            # Check if the category of interest is in the column names of the dataframe
            if export_category not in dataframe.columns:
                # No, the category is not one of the names of the columns
                raise ValueError('Field '+str(export_category)+' not available in column headers '+str(list(dataframe.columns)))

        return export_category


    def _dataframe_full_category(self, dataframe, category_of_interest_values):
        """
        The function _dataframe_full_category will make incomplete categories complete by adding missing values.
        
        Precondition: The dataframe dataframe needs to be aggregated by Year and category-of-interest and only contains the data from one year.

        Parameters
        ----------
        dataframe        : pandas DataFrame with data from one year.
        
        Self variables
        --------------
        self.year_column : List of only 'Year' as supported headercolumn
        
        Returns
        -------
        export_dataframe : empty pandas DataFrame or pandas DataFrame with extra category-of-interest-values
        """
        # Check dataframe
        error_not_isdataframe(dataframe, 'dataframe')

        # Check for emptyness
        if dataframe.empty:
            # DataFrame is empty, return this empty dataframe
            export_dataframe = dataframe.copy()
            return export_dataframe

        # We want the '_Category' and 'Year' columns
        wanted_headers = ['_Category'] + self.year_column

        # Search for available headers
        available_headers = dataframe_search_for_headers(dataframe, search_for_headers=wanted_headers, error_not_found=False)

        # Check for year
        year = self.year_column[0]
        if year in available_headers:
            # Yes, we have a year-column
            min_year = dataframe[year].min()
            max_year = dataframe[year].max()
            if min_year != max_year:
                raise ValueError("More than one year in DataFrame. Min year:"+str(min_year)+". Max year:"+str(max_year))

            # Check for category-of-interest
            if '_Category' in available_headers:
                # Yes, we have a category-of-interest-column
                
                # Check if the category of interest is usable: Is it a list, is it not empty and does it have equal or more entries than the related column in dataframe
                error_not_islist(category_of_interest_values, "category_of_interest_values")
                if len(category_of_interest_values) == 0:
                    raise ValueError("Category-of-interest is an empty list: "+str(category_of_interest_values))
                if len(list(set(dataframe['_Category'].unique()) - set(category_of_interest_values))) > 0:
                    raise ValueError("Category-of-interest "+str(category_of_interest_values)+" has less values than the column _Category in the dataframe: "+\
                                     str(list(dataframe['_Category'].unique())))
                
                yearlist = [str(min_year)] * len(category_of_interest_values)  # min_year is equal to max_year. So max_year was also fine in this line of code
                df = pd.DataFrame({year:yearlist, "_Category":category_of_interest_values})  # Makes a dataframe with lines with Year and category on each line

                # Fill full category
                export_dataframe = pd.merge(df, dataframe, how='left' ,on=[year, "_Category"]).copy()
                for column in export_dataframe.columns:
                    # Get dtype of the column
                    dtype_of_column = export_dataframe[column].dtype 
                    # Is it a integer or a float
                    if dtype_of_column == int or dtype_of_column == float:
                        export_dataframe[column].fillna(0, inplace=True)
                    else:
                        export_dataframe[column].fillna("", inplace=True)
                
            else:
                # No, we don't have a category-of-interest-column
                raise ValueError('No category-of-interest-column in available headers: '+str(available_headers))
        else:
            # No, we don't have a year-column
            raise ValueError('No year is not supported yet')   #### Technical debt for adding support

        return export_dataframe


    def _dataframe_handle_previous_year(self, dataframe):
        """
        The function _dataframe_handle_previous_year checks and/or adds previous year information based on actual information of earlier years.
        If the dataframe contains 2 years of actual information and also previous year information, then the actuals of previous year will be compared with
        the previous year information in the highest year. Error when not equal.
        If the dataframe contains 2 years of actual information and no previous year information, then the actuals of previous year will be
        the previous year information in the highest year.

        Precondition: The dataframe only has the category of interest as the categorical variables besides the scenarios and optionally the year-column.
                      If no year is provided, the dataframe will be returned without modifications.

        Parameters
        ----------
        dataframe          : pandas DataFrame with possibly more year information

        Self variables
        --------------
        self.all_scenarios : List of Previous Year, PLan, ACtual, ForeCast [PY, PL, AC, FC] (in order of time)
        self.year_column   : List of only 'Year' as supported headercolumn

        Returns
        -------
        export_dataframe   : pandas DataFrame with 'optimized' information of the highest year (possibly added with 'previous year' information)
        """
        # We want the 'Year' column
        wanted_headers = self.year_column

        # Search for available headers
        available_headers = dataframe_search_for_headers(dataframe, search_for_headers=wanted_headers, error_not_found=False)

        # Check for too many columns
        if not list1_is_subset_list2(list1=list(dataframe.columns), list2=self.year_column+['_Category']+self.all_scenarios):
            # Too many columns
            raise ValueError("Too many columns in dataframe: "+str(list(dataframe.columns)))

        # Check if _Category is in the available headers
        if not '_Category' in dataframe.columns:
            raise ValueError('_Category is not available in column headers of dataframe: '+str(list(dataframe.columns)))

        # Check if year is in the available headers
        year = self.year_column[0]
        if year in available_headers:
            # Yes, there is a year available

            # Determine the max-year and the year before the max-year. These will be the actual (AC) and previous year (PY)
            max_year        = dataframe[year].max()
            before_max_year = str(int(max_year)-1)

            # Split the dataframes in the actual and previous year
            df_ac = dataframe[dataframe[year] == max_year].copy()
            df_py = dataframe[dataframe[year] == before_max_year].copy()

            # Complete dataframe for missing category-of-interest-values. Nothing worse than incomplete categories
            category_of_interest_values = list(dataframe['_Category'].unique())
            df_ac = self._dataframe_full_category(df_ac, category_of_interest_values)
            df_py = self._dataframe_full_category(df_py, category_of_interest_values)

            # Check for previous year column in actual dataframe
            if 'PY' in df_ac.columns:
                # Yes, previous year column in actual dataframe
                # Check if there is an actual column in the previous year dataframe and check if the previous year dataframe is not empty
                if 'AC' in df_py.columns and not df_py.empty:
                    # Dataframe with previous year information is not empty and has an actual column
                    # Check if the values for previous year in the actual dataframe are the same as the actual values in the previous year dataframe
                    #if not (df_ac[['PY']] == df_py[['AC']]).all():    #### Technical debt: How to check if dataframe-columns are the same?
                    if not (list(df_ac['PY']) == list(df_py['AC'])):
                        # Not all values are the same
                        raise ValueError(str(max_year)+"-DataFrame previous year does not match "+str(before_max_year)+ "-Dataframe", str(df_ac), str(df_py))
                    # else:
                    #    All values are the same, go further
                # else:
                #    No actual values in previous year dataframe or dataframe is empty, go further
            else:
                # No previous year column in actual dataframe
                if 'AC' in df_py.columns and not df_py.empty:
                    # We can use the actual values in the previous year dataframe as previous year values in the actual dataframe
                    df_ac['PY'] = df_py['AC'].copy()
                # else:
                #   No actual values in previous year dataframe or dataframe is empty, go further

            # Prepare export_dataframe
            export_dataframe = df_ac.copy()

        else:
            # No, there is no year-column available, just return the unmodified dataframe
            export_dataframe = dataframe.copy()

        return export_dataframe


    def _prepare_dataframe(self, dataframe):
        """
        The function _prepare_dataframe orchestrates other functions for better column names, determine category_of_interest, keep relevant columns and remove not needed,
        convert date to year and optional month, aggregation, handling previous year, check scenario parameters and calculate totals.

        Parameters
        ----------
        dataframe              : pandas DataFrame

        Self variables
        --------------
        self.all_date_columns  : List of date, year and month as supported headercolumns
        self.all_scenarios     : List of Previous Year, PLan, ACtual, ForeCast [PY, PL, AC, FC] (in order of time)
        self.date_column       : List of only 'Date' as supported headercolumn
        self.month_column      : List of only 'Month' as supported headercolumn
        self.translate_headers : Dictionary where you can translate fieldheaders
        self.year_column       : List of only 'Year' as supported headercolumn

        Returns
        -------
        dataframe              : pandas DataFrame
        """
        # If the dictionary self.translate_headers is filled with {'old-name':'new-name'} combinations, this will be translated in the upcoming function
        dataframe = dataframe_translate_field_headers(dataframe, translate_headers=self.translate_headers)

        # Determine the category of interest (if not given)
        category_of_interest = self._dataframe_find_category_of_interest(dataframe)

        # Rename the category of interest
        dataframe = dataframe_translate_field_headers(dataframe, translate_headers={category_of_interest:'_Category'})

        # If the dataframe has more columns than relevant, only keep the relevant columns
        wanted_headers = ['_Category'] + self.all_date_columns + self.all_scenarios
        dataframe = dataframe_keep_only_relevant_columns(dataframe, wanted_headers=wanted_headers)

        # If the dataframe has a 'Date'-column, convert it to 'Year' and (optional) 'Month' (Year and Month gets overwritten if exist)
        dataframe = dataframe_date_to_year_and_month(dataframe, date_field=self.date_column, year_field=self.year_column)

        # Now make the relevant columns even smaller by not include the date column (info is already converted to year and month)
        wanted_headers = ['_Category'] + self.year_column + self.all_scenarios
        dataframe = dataframe_keep_only_relevant_columns(dataframe, wanted_headers=wanted_headers)

        # It is possible that the dataframe has more detailed lines (especially when removing non-relevant columns).
        wanted_headers = ['_Category'] + self.year_column
        dataframe = self._dataframe_aggregate(dataframe, wanted_headers=wanted_headers)

        # Convert year and month to strings and sort the dataframe on year
        wanted_headers = ['_Category'] + self.year_column
        dataframe = dataframe_convert_year_month_to_string(dataframe, wanted_headers, year_field=self.year_column, month_field=self.month_column)

        # Handle previous year information
        dataframe = self._dataframe_handle_previous_year(dataframe)

        # Now we know if PY is part of the scenarios, so we can fill the data scenarios
        self._fill_data_scenarios(dataframe=dataframe)

        # If we know all the data scenarios, we can check the base and compare scenarios against them
        self._check_scenario_parameters()

        # The dataframe has its final figures, we can calculate the totals
        self._fill_data_total(dataframe=dataframe)

        return dataframe


    def _fill_data_scenarios(self, dataframe):
        """
        The function _fill_data_scenarios extracts the scenarios out of the columnheaders of the pandas DataFrame.
        It is checked against all supported scenarios and stored in the list self.data_scenarios.

        Parameters:
        -----------
        dataframe           : dataframe of the data with the scenarios in the column headers

        Self variables
        --------------
        self.all_scenarios  : List of all supported scenarios: Previous Year, PLan, ACtual, ForeCast [PY, PL, AC, FC] (in order of time)
        self.data_scenarios : List of scenarios available in the column headers of the dataframe out of the list of all supported scenarios
        """
        # Check dataframe
        error_not_isdataframe(dataframe, 'dataframe')
        
        # Extract the data scenarios
        self.data_scenarios = filter_lists(list1=self.all_scenarios, list2=list(dataframe.columns))

        return


    def _optimize_data_total(self, numerator=1, denominator=1, decimals=0):
        """
        The function _optimize_data_total makes each element up to the desired number of significant figures and store these in the dictionary self.data_total.
        Every value will be multiplied with the numerator, divided with the denominator and then round to the desired number of decimals.
        In formula: ROUND( value * numerator / denominator, number of decimals)

        Parameters:
        -----------
        numerator       : numerator is the number to multiply with.
                          Default: 1 (multiply with 1, which is the same as keeping the value)
        denominator     : denominator is the number to divide by.
                          Default: 1 (dividy by 1, which is the same as keeping the value)
        decimals        : number of decimals with which the totals are rounded and stored.
                          Default: 0 (zero decimals)

        Self variables
        --------------
        self.data_total : dictionary (key=scenario) with the adjusted total value
        """
        # Check if the parameters are integers
        error_not_isinteger(numerator, "numerator")
        error_not_isinteger(denominator, "denominator")
        error_not_isinteger(decimals, "decimals")
     
        # Check if data_total is a dictionary
        error_not_isdictionary(self.data_total, "self.data_total")
     
        # Process for each value in the dictionary
        for element in self.data_total.keys():
            value = self.data_total[element]
            self.data_total[element] = optimize_data(data=value, numerator=numerator, denominator=denominator, decimals=decimals)
 
        return


    def _fill_data_total(self, dataframe, decimals=None):
        """
        The function _fill_data_total sums up the values per scenario and stores these in the dictionary self.data_total.

        Parameters:
        -----------
        dataframe           : dataframe of the data with the scenarios in the column headers
        decimals            : number of decimals with which the totals are rounded and stored. When None then no rounding will be done.
                              Default: None (no rounding)

        Self variables
        --------------
        self.data_scenarios : List of scenarios available in the column headers of the dataframe out of the list of all supported scenarios
        self.data_total     : Dictionary (key=scenario) with the total value        
        """
        # Check dataframe
        error_not_isdataframe(dataframe, 'dataframe')

        # Empty the data_total
        self.data_total = dict()

        for element in self.data_scenarios:
            if decimals is None:
                # No rounding, just sum it up and store. The .item() is to get standard Python types back instead of numpy-types.
                self.data_total[element] = dataframe[element].sum().item()
            else:
                # Rounding is activated, but we can only round on an integer number of decimals
                error_not_isinteger(decimals, "decimals")
                # Parameter decimals is an integer, do the rounding calculation and store it to the scenario of data_total.
                # The .item() is to get standard Python types back instead of numpy-types.
                self.data_total[element] = optimize_data(data=dataframe[element].sum().item(), numerator=1, denominator=1, decimals=decimals)

        return


    def _optimize_data_get_big_detail(self, dataframe):
        """
        This function searches for the largest absolute values in the detail information.

        # Precondition: self.data_scenarios contains the scenarios of the dataframe

        Parameters:
        -----------
        dataframe           : pandas DataFrame with the detail information

        Self variables
        --------------
        self.data_scenarios : List of scenarios available in the column headers of the dataframe out of the list of all supported scenarios

        Returns
        -------
        big_detail          : the biggest absolute value in the dataframe
        """
        # Check dataframe
        error_not_isdataframe(dataframe, 'dataframe')

        # Check precondition
        error_not_islist(self.data_scenarios, 'self.data_scenarios')
        # Self.data_scenarios is a list, check if there is content
        if not self.data_scenarios:
            # List is empty
            raise ValueError("self.data_scenarios is an empty dictionary.")

        # Start with an empty list
        big_details = list()

        # For each scenario-column append the absolute value of the min-value and the max-value of the column to the big_details-list.
        for element in filter_lists(self.data_scenarios + ['_CBC_DELTA1', '_CBC_DELTA2'], list(dataframe.columns)):
            big_details.append(abs(dataframe[element].min()))
            big_details.append(abs(dataframe[element].max()))

        # Now take the maximum of the list. Due to absolute values a lower minus value can be the max value now!
        big_detail = max(big_details)

        return big_detail


    def _optimize_data_get_big_total(self):
        """
        The function _optimize_data_get_big_total searches for the largest absolute values in the dictionary of total values.

        # Precondition: self.data_total is a dictionary and has total values

        Self variables
        --------------
        self.data_total     : Dictionary (key=scenario) with the total value of each scenario

        Returns
        -------
        big_total           : the biggest absolute value in the self.data_total dictionary
        """
        # Check precondition
        error_not_isdictionary(self.data_total, 'self.data_total')
        # Self.data_total is a dictionary, check if there is content
        if not self.data_total:
            # Dictionary is empty
            raise ValueError("self.data_total is an empty dictionary.")
        # else:
            # Yes, there is content (dictionary is not empty)

        # Put the values of the self.data_total-dictionary into the list big_totals
        big_totals = list(self.data_total.values())

        # Make big_totals values absolute
        big_totals = [abs(x) for x in big_totals]

        # Now take the maximum of the list. Due to absolute values a lower minus value can be the max value now!
        big_total  = max(big_totals)

        return big_total


    def _optimize_data_calculate_denominator(self, big_detail):
        """
        The function _optimize_data_calculate_denominator calculates the denominator to optimize the maximum value of the detail information 
        to a maximum of 3 significant digits.

        Parameters
        ----------
        big_detail               : Float with the absolute maximum value of the pandas DataFrame

        Self variables
        --------------
        self.multiplier          : Multiplier-type with the actual multiplier
        self.original_multiplier : Original multiplier when called this class, converted to a multiplier-type

        Returns
        -------
        export_denominator       : Dividervalue for all DataFrame-values and total-values
        """
        # Check parameters
        if not isinteger(big_detail) and not isfloat(big_detail):
            raise TypeError('Parameter big_detail "'+str(big_detail)+'" is not an integer or a float, but of type '+str(type(big_detail)))
 
        # Check self-variables
        if not isinstance(self.original_multiplier, Multiplier):
            raise TypeError('self.original_multiplier "'+str(self.original_multiplier)+'" is not a Multiplier, but of type '+str(type(self.original_multiplier)))

        # Get the value of the parameter multiplier
        self.multiplier = Multiplier(self.original_multiplier.get_multiplier())

        # Optimize the maximum of the detail values and get the denominator back to adjust all values with. The multiplier-type is also adjusted internally.
        export_denominator = self.multiplier.optimize(big_detail)

        return export_denominator


    def _optimize_data_adjust_decimals(self, big_detail, big_total, denominator):
        """
        The function _optimize_data_adjust_decimals calculates the number of decimals to have at most 3 significant figures in detail.
        Parameters force_zero_decimals and force_max_one_decimals are also taken in consideration.

        Parameters:
        -----------
        big_detail                  : Float with the absolute maximum value of the pandas DataFrame
        big_total                   : Float with the absolute maximum value of the dictionary of totals
        denominator                 : Dividervalue for all DataFrame-values and total-values

        Self variables
        --------------
        self.decimals_details       : Number of decimals for detailed information
        self.decimals_totals        : Number of decimals for total information
        self.force_max_one_decimals : Boolean when True, the maximum of decimals used is one. Know that force_zero_decimals has a higher priority than force_max_one_decimals
        self.force_zero_decimals    : Boolean when True, integers are used for output
        """
        # Check parameters
        if not isinteger(big_detail) and not isfloat(big_detail):
            raise TypeError('Parameter big_detail "'+str(big_detail)+'" is not an integer or a float, but of type '+str(type(big_detail)))
        if not isinteger(big_total) and not isfloat(big_total):
            raise TypeError('Parameter big_total "'+str(big_total)+'" is not an integer or a float, but of type '+str(type(big_total)))
        if not isinteger(denominator) and not isfloat(denominator):
            raise TypeError('Parameter denominator "'+str(denominator)+'" is not an integer or a float, but of type '+str(type(denominator)))

        # Check some self-variables
        error_not_isboolean(self.force_zero_decimals, 'self.force_zero_decimals')
        error_not_isboolean(self.force_max_one_decimals, 'self.force_max_one_decimals')

        # Calculate the number of decimals by making an integer of the optimized value of the maximums and see how many decimals are needed for 3 significant figures
        self.decimals_details  = max(0, 3 - len(str(int(big_detail / denominator))))
        self.decimals_totals   = max(0, 3 - len(str(int(big_total / denominator))))

        # Is the parameter force_zero_decimals set to True?
        if self.force_zero_decimals:
            # Yes, we are forcing zero decimals!
            self.decimals_details = 0
            self.decimals_totals = 0
        # else:
            # No, we are not forcing zero decimals!

        # Is the parameter force_max_one_decimals set to True?
        if self.force_max_one_decimals:
           # Yes, but force_zero_decimals has higher priority, so we take the minimum of the decimals currently and 1!
           self.decimals_details = min(self.decimals_details, 1)
           self.decimals_totals  = min(self.decimals_totals , 1)
        # else:
            # No, we are not forcing max one decimals!

        return 


    def _optimize_data_dataframe_details(self, dataframe):
        """
        The function _optimize_data_dataframe_details optimizes the detail information in the dataframe so that it will have a maximum of 3 significant digits.

        Parameters:
        -----------
        dataframe                   : pandas DataFrame with the detail information

        Self variables
        --------------
        self.data_scenarios         : List of scenarios available in the column headers of the dataframe out of the list of all supported scenarios
        self.decimals_details       : Number of decimals for detailed information
        self.multiplier_denominator : Diviser as a result of optimizing the multiplier

        Returns
        -------
        export_dataframe            : pandas DataFrame with optimized detail information
        """
        # Check dataframe
        error_not_isdataframe(dataframe, 'dataframe')

        # Check some self-variables
        error_not_islist(self.data_scenarios, 'self.data_scenarios')
        if not isinteger(self.multiplier_denominator) and not isfloat(self.multiplier_denominator):
            raise TypeError('self.multiplier_denominator "'+str(self.multiplier_denominator)+'" is not a float or an integer, but of type '+str(type(self.multiplier_denominator)))
        if not isinteger(self.decimals_details) and not isfloat(self.decimals_details):
            raise TypeError('self.decimals_details "'+str(self.decimals_details)+'" is not a float or an integer, but of type '+str(type(self.decimals_details)))

        # Prepare the return value
        export_dataframe = dataframe.copy()

        # Adjust each column with scenarios and delta values so that they are optimized
        for element in filter_lists(self.data_scenarios + ['_CBC_DELTA1', '_CBC_DELTA2'], list(dataframe.columns)):
            export_dataframe[element] = optimize_data(data=list(export_dataframe[element]), numerator=1, denominator=self.multiplier_denominator,
                                                      decimals=self.decimals_details)

        return export_dataframe


    def _optimize_data(self, dataframe):
        """
        The function _optimize_data orchestrates other functions which will search for the largest absolute values in the detail information
        and in the total values. Then the maximum value of the detail information will be optimized so that it will have a maximum of 3 significant digits.

        Next the number of decimals will be calculated to have at most 3 significant figures in detail.
        Parameters force_zero_decimals and force_max_one_decimals are also taken in consideration.

        Finally the detail data and total data will be optimized.

        # Precondition: self.data_total has total values and self.data_scenarios contains the scenarios of the dataframe

        Parameters:
        -----------
        dataframe                   : pandas DataFrame with the detail information

        Self variables
        --------------
        self.data_scenarios         : List of scenarios available in the column headers of the dataframe out of the list of all supported scenarios
        self.data_total             : Dictionary (key=scenario) with the total value of each scenario
        self.decimals_totals        : Number of decimals for total information
        self.multiplier_denominator : Diviser as a result of optimizing the multiplier

        Returns
        -------
        export_dataframe            : pandas DataFrame with optimized detail information
        """
        # Check parameter
        error_not_isdataframe(dataframe, 'dataframe')

        # Check precondition
        error_not_isdictionary(self.data_total, 'self.data_total')
        # Self.data_total is a dictionary, check if there is content
        if not self.data_total:
            # Dictionary is empty
            raise ValueError("self.data_total is an empty dictionary.")
        # else:
            # Yes, there is content (dictionary is not empty)

        # Check precondition
        error_not_islist(self.data_scenarios, 'self.data_scenarios')
        # Self.data_scenarios is a list, check if there is content
        if not self.data_scenarios:
            # List is empty
            raise ValueError("self.data_scenarios is an empty list.")
        # else:
            # Yes, there is content (list is not empty)

        # Get the big_detail (biggest absolute value of the dataframe) and the big_total (biggest absolute value of the data_total list)
        big_detail = self._optimize_data_get_big_detail(dataframe)
        big_total  = self._optimize_data_get_big_total()

        # Calculate the dominator
        self.multiplier_denominator = self._optimize_data_calculate_denominator(big_detail)

        # Adjust decimals based on the effect of the dominator on the big_detail and big_total
        self._optimize_data_adjust_decimals(big_detail, big_total, self.multiplier_denominator)

        # Update details in dataframe based on denominator and decimals
        export_dataframe = self._optimize_data_dataframe_details(dataframe)

        # Update totals based on denominator and decimals.
        # Note: We also adjust the totals from within this function because it should be an "atomic" transaction together with the details
        self._optimize_data_total(numerator=1, denominator=self.multiplier_denominator, decimals=self.decimals_totals)

        return export_dataframe


    def _drop_zero_lines(self, dataframe):
        """
        The function _drop_zero_lines removes lines of data where all figures are zero if and only if the parameter self.remove_lines_with_zeros is True.
        
        Parameters
        ----------
        dataframe                    : pandas DataFrame

        Self variables
        --------------
        self.data_scenarios          : List of scenarios available in the column headers of the dataframe out of the list of all supported scenarios
        self.remove_lines_with_zeros : Boolean, when True determines that we want to drop lines with zeros

        Returns
        -------
        export_dataframe             : pandas DataFrame with or without zero lines
        """
        # Check dataframe
        error_not_isdataframe(dataframe, 'dataframe')

        # Check data_scenarios
        error_not_islist(self.data_scenarios, 'self.data_scenarios')
        # Yes, data_scenarios is a list! Check if the list has entries
        if not self.data_scenarios:
            # The list has no entries. This could result in an empty dataframe at the end
            raise ValueError("Data_scenarios '"+str(self.data_scenarios)+"' has no entries.")

        # Check if remove_lines_with_zeros is a True/False variable
        error_not_isboolean(self.remove_lines_with_zeros)
        # Yes, it is a True/False variable. Check if we want to remove lines with zeros
        if self.remove_lines_with_zeros:
            # Yes, we want to drop the lines with all zeros
            export_dataframe = dataframe.loc[~(dataframe[self.data_scenarios] == 0).all(axis=1)].copy()
        else:
            # No, we don't want to drop lines
            export_dataframe = dataframe.copy()

        return export_dataframe


    def _sort_dataframe_with_other_last(self, dataframe):
        """
        The function _sort_dataframe_with_other_last sorts the dataframe by the delta-value, but exclude rows with OTHER value from sorting
        and put them at the bottom
        
        # pre-condition: Columns category-of-interest, delta1 and delta2 needs to be available
        
        NOTE: Only the first delta-column is supported for sorting!

        Parameters
        ----------
        dataframe : pandas DataFrame with all values
        
        Returns
        -------
        export_dataframe: pandas DataFrame sorted by delta-values where OTHER value is handled separate
        """
        # Check dataframe
        error_not_isdataframe(dataframe, 'dataframe')

        # Check pre-condition
        if not list1_is_subset_list2(list1=['_Category', '_CBC_DELTA1', '_CBC_DELTA2'], list2=list(dataframe.columns)):
            raise ValueError("Dataframe doesn't contain these columns '_Category', '_CBC_DELTA1' and '_CBC_DELTA2': "+str(list(dataframe.columns)))

        # Separate the OTHER value
        df_other         = dataframe[dataframe['_Category'] == "OTHER"].copy()

        # Use all values except the OTHER value and then sort the dataframe
        df_all_but_other = dataframe[dataframe['_Category'] != "OTHER"].copy()
        df_all_but_other = df_all_but_other.sort_values(by=['_CBC_DELTA1'], ascending=False).copy()

        # Add the OTHER values back to the dataframe
        export_dataframe = pd.concat([df_all_but_other, df_other], ignore_index=True).copy()

        return export_dataframe


    def _process_dataframe(self, dataframe):
        """
        The function _process_dataframe calculates the deltavalues, sort the dataframe by the delta-values, removes zerolines by request,
        optimizes the data for viewing and adds the y-values for making the chart

        Parameters
        ----------
        dataframe : pandas DataFrame 
        
        Returns
        -------
        dataframe : pandas DataFrame with delta-values, sorted, optimized for viewing and added with y-values for charting
        """
        # Check for each bar which scenario needs to be on top of the compare_scenarios
        dataframe = self._determine_bar_layers_in_dataframe(dataframe=dataframe)

        # Add columns for delta-values and compute these delta-values
        dataframe = self._add_deltavalues_to_dataframe(dataframe=dataframe)
        
        # Sort the delta-values by handling the "OTHER"-value separate
        dataframe = self._sort_dataframe_with_other_last(dataframe=dataframe)

        # Remove lines out of the dataframe (on request) if all data-values in that line are zeros
        dataframe = self._drop_zero_lines(dataframe=dataframe)
        
        # Optimize the data for viewing by making the values about 3 figures long (total values about 4 figures long)
        dataframe = self._optimize_data(dataframe=dataframe)

        # Calculate the y-coordinates for the chart
        dataframe = self._add_yvalues_to_dataframe(dataframe=dataframe)
        
        return dataframe


    def _convert_data_dictionary_to_pandas_dataframe(self, data):
        """
        The function _convert_data_dictionary_to_pandas_dataframe converts a dictionary to a pandas DataFrame.

        # precondition: The dictionary needs to have a key-entry with the value 'HEADERS'

        Parameters
        ----------
        data             : data contains a dictionary

        Returns
        -------
        export_dataframe : pandas DataFrame with column names
        """
        # Check parameter is dictionary
        error_not_isdictionary(data, 'data')

        # Check if the value 'HEADERS' is in the dictionary-keys
        if not 'HEADERS' in data:
            # 'HEADERS' is not in the dictionary-keys
            raise ValueError("No 'HEADERS' found in dictionary "+str(list(data.keys())))

        # Conversion to dataframe    
        export_dataframe = pd.DataFrame.from_dict({k: v for k, v in data.items() if k != 'HEADERS'}, orient='index', columns=data['HEADERS']).reset_index()

        return export_dataframe
    

    def _check_and_process_data(self, data=None):
        """
        The function _check_and_process_data tries to convert the data, if it is not a pandas DataFrame yet, to a pandas DataFrame-format.
        At the end, it calls the function to process this dataframe.
        Finally it stores the DataFrame in self.data.

        Parameters
        ----------
        data : Data contains a dictionary, a string-like CSV-file, a list of lists or a pandas DataFrame.
               (Default value = None)

        Self variables
        --------------
        self.data           : pandas DataFrame with detail values
        self.data_scenarios : List of scenarios available in the column headers of the dataframe out of the list of all supported scenarios
        """
        # If it is a string, convert it to a dataframe
        if isstring(data):
            # Data is in the form of a string. We need to convert it to a pandas DataFrame
            data = convert_data_string_to_pandas_dataframe(data)
            self._fill_data_scenarios(data)     # fills self.data_scenarios with all scenarios available in the dataframe
            data = convert_dataframe_scenario_columns_to_value(data, self.data_scenarios)   # Converts string values to integer or floats of the scenarios
            # Data is now in the form of a pandas DataFrame

        if isdictionary(data):
            # Data is in the form of a dictionary. We need to convert it to a pandas DataFrame
            data = self._convert_data_dictionary_to_pandas_dataframe(data)
            # Data is now in the form of a pandas DataFrame

        # If it is a list of list, convert it to a dataframe
        if islist(data):
            # Data is in the form of a list (of lists). We need to convert it to a pandas DataFrame
            data = convert_data_list_of_lists_to_pandas_dataframe(data)
            # Data is now in the form of a pandas DataFrame

        # The only support from here on is a dataframe
        if isdataframe(data):
            # Data is in the form of a pandas DataFrame
            data = self._prepare_dataframe(data)
            # Data is still in the form of a pandas DataFrame and a possibly availability of Previous Year is integrated
        else:
            # Data is not in the form of a dataframe or there is no data
            raise TypeDataFrameError("No data available or not in the correct form. Please read:\n"+str(BarWithWaterfall.__doc__))

        # Process the dataframe
        data = self._process_dataframe(data)

        # Put the dataframe in self.data so other parts of the program can use it.
        self.data = data.copy()
 
        return


    def _make_subplots(self):
        """
        The function _make_subplots creates the figure and subplot for the chart. The figure size in heigt depends on the number of dataframe-rows. 
        Next it cleans up the chart-borders and ticks.

        Self variables
        --------------
        self.data     : Dataframe with detail data, needed here to get the number of dataframe-rows
        self.fig      : Figure-object for the generated plot and subplots
        self.ax       : axisobject
        """
        # Check dataframe
        error_not_isdataframe(self.data, "self.data")
        
        # Get the number of dataframe-rows out of the shape of the dataframe
        dataframe_rows = self.data.shape[0]
        
        # Create the figure-object and the axis-object
        self.fig, self.ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 2 + dataframe_rows*0.5), dpi=72) # dpi=72 solves some strange linewidth issues.
        
        # Clean up the ticks and make the left-side available for the labels
        self.ax.tick_params(top=False, bottom=False, left=False, right=False, labelleft=True, labelbottom=False)
        
        # Remove the lines around the chart
        self.ax.spines[['top', 'left', 'right', 'bottom']].set_visible(False)
        
        return


    def _title_figure(self, title=None):
        """
        The function _title_figure puts a title in the upper left corner of the chart.
        
        Parameters
        ----------
        title : Dictionary with text values to construct a title. 
                No part of the title is mandatory, except when 'Business_measure' is filled, the 'Unit' is expected to be filled too.
             (default value: None). No title will be constructed with value None.
        
                more info:
                     title['Reporting_unit'] = 'Global Corporation'     # This is the name of the company or the project or business unit, added with a selection. For example 'ACME inc., Florida and California'
                     title['Business_measure'] = 'Net profit'           # This is the name of the metric. Can also be a ratio. For example: 'Net profit' or 'Cost per headcount'
                     title['Unit'] = 'mUSD'                             # This is the name of the unit. For example: 'USD', 'EUR', '#', '%'. Add k for 1000, m for 1000000 and b for 1000000000
                     title['Time'] = '2022: AC Jan..Aug, FC Sep..Dec'   # This is the description of the time, scenario's and variances. For example: '2022 AC, PL, FC, PL%'

        Self variables
        --------------
        self.barwidth : A float with the width of the bars for measure or ratio
        self.colors   : Dictionary with colors
        self.fig      : Figure-object for the generated plot and subplots
        self.font     : All text in a chart has the same font
        self.fontsize : All text in a chart has the same height
        """
        title_text = prepare_title(title, multiplier=self.multiplier.get_multiplier_string())
        # Check if there is a title prepared
        if title_text is None:
            # No title
            return
        
        fig = self.fig
        
        #### TECHNICAL DEBT: How to determine the right x and y values?
        fig.suptitle(t=title_text, font=self.font, fontsize=self.fontsize, color=self.colors['text'], ha='left', va='top',x=0,y=0.95)  #### x=-0.01??
