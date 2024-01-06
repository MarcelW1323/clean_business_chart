"""ColumnWithWaterfall-module"""

import matplotlib.pyplot as plt                   # for most graphics
from matplotlib import rcParams as mpl_rcp        # for font in _title
#from matplotlib import __version__ as mpl_version
import pandas as pd                               # for easy pandas support

from clean_business_chart.clean_business_chart import GeneralChart 
from clean_business_chart.general_functions    import plot_line_accross_axes, plot_line_within_ax, prepare_title, formatstring, optimize_data, \
                                                      islist, isdictionary, isinteger, isstring, isfloat, isboolean, isdataframe, string_to_value, \
                                                      convert_data_string_to_pandas_dataframe, convert_data_list_of_lists_to_pandas_dataframe, \
                                                      dataframe_translate_field_headers, dataframe_search_for_headers, \
                                                      dataframe_date_to_year_and_month, dataframe_keep_only_relevant_columns, \
                                                      dataframe_convert_year_month_to_string, convert_number_to_string
from clean_business_chart.multiplier           import Multiplier


class ColumnWithWaterfall(GeneralChart):
    """
    Produces a column chart with a waterfall delta chart based on data of one year divided in 12 months
    
    Minimal requirements to make the chart
    --------------------------------------
    import clean_business_chart as cbc
    dataset = {'PY': [14, 16, 14, 17, 19, 17, 19, 22, 16, 17, 16, 22],      # 12 months of Previous Year data (optional)
               'PL': [11, 10, 10, 10, 10, 10, 15, 14, 15, 15, 15, 19],      # 12 months of PLan data
               'AC': [15, 13, 16, 7, 5, 6, 17, 11],                         # up to 12 months of ACtual data
               'FC': [0, 0, 0, 0, 0, 0, 0, 0, 26, 22, 13, 29],              # up to 12 months of ForeCast data
               'Year': 2022}                                                # the year to be mentioned in the chart
    cbc.ColumnWithWaterfall(data=dataset)
    
    Parameters
    ----------
    data                    : A dictionary with minimal PL and AC or PY and AC detailinformation, a string with CSV-values,
                              a list of lists or a pandas DataFrame. Read the documentation.
    positive_is_good        : On a variance chart it decides whether a positive number makes a good color (True) or 
                              a bad color (False).
                              Default: True (good color)
    preferred_base_scenario : PL uses PLaninfo as the base scenario in the main chart. PY uses Previous Year 
                              as the base scenario in the main chart
                              Default: None ('PL' will be used if available or else 'PY' will be used if available)
    title                   : A dictionary with optional values to make a title inspired by IBCS
                              Default: None (no title)
    measure                 : True -> measure, False -> ratio
                              Default: True (measure)
    multiplier              : One character with the multiplier ('1', 'k', 'm', 'b')
                              Default: '1' (one)
    filename                : String with filename and path to export the chart to, including extention.
                              Only tested with a .png and a .jpg-extention
                              Default: None (no export of the chart to a file)
    force_pl_is_zero        : If PL are all zeros, can PL be ignored (False) or force that PL can be zero (True)
                              Default: False (PL can be ignored when all zeros)
    force_zero_decimals     : If True, we use integers for output. This gives a more clean chart, 
                              but can lack some detail in some cases
                              Default: False (don't force zero decimals)
    force_max_one_decimals  : If True, the maximum of decimals used is one. Know that force_zero_decimals 
                              has a higher priority than force_max_one_decimals.
                              Default: False (don't force max one decimals)
    translate_headers       : Dictionary where you can translate field headers, example 
                              {'Orderdate':'Date', 'Revenue':'AC'}
                              Default: None (no translation of headers will occur)
    test                    : If True, only variables from the parent class are defined, together with other 
                              self-variables. This makes this module testable in an automatic way
                              Default: False (this call it is not an automatic test)
    """

    def __init__(self, data=None, positive_is_good=True, preferred_base_scenario=None, title=None, measure=True, multiplier='1', filename=None, 
                 force_pl_is_zero=False, force_zero_decimals=False, force_max_one_decimals=False, translate_headers=None, test=False, do_not_show=False):
        """
        This is the first function that will be called automatically. Here you'll find all the possible parameters to customize your experience.
        """
        super().__init__()                            # Get the variables from the parent class
        self._other_columnwithwaterfall_variables()   # Get additional variables for this class
        
        # for use to test automatically
        if test: return None
        
        # Store variables
        self.original_data          = data
        self.original_multiplier    = Multiplier(multiplier)
        self.year                   = None
        self.positive_is_good       = positive_is_good
        self.base_scenario          = preferred_base_scenario
        self.hatch                  = self.hatch_pattern
        self.filename               = filename
        self.force_pl_is_zero       = force_pl_is_zero
        self.force_zero_decimals    = force_zero_decimals
        self.force_max_one_decimals = force_max_one_decimals
        self.translate_headers      = translate_headers
        
        # Make chart
        self.get_barwidth(measure)
        self._check_data(data)
        if self.year is None: raise ValueError("No 'Year' supplied in data.")
        self._make_subplots()
        self.calculate_delta(base_scenario=self.base_scenario, compare_scenario_list=['AC', 'FC'], delta_name='main')
        self._fill_leftside_ax()
        self._fill_side_axsum()
        self._fill_axcomments()
        self._fill_main_ax()
        self._show_delta()
        self._fill_delta_ax_text()

        # Add the title as the last element        
        self._title(title)
        
        # We are exporting the chart if the filename has a value
        if self.filename is not None:
            plt.savefig(self.filename, bbox_inches='tight', dpi=150)
        
        # For automatic testing of complete images of chart
        if not do_not_show:
            # No, no automatic testing of complete images of chart -> show the chart
            plt.show()
        

    def _other_columnwithwaterfall_variables(self):
        """
        A collection of variables for columnchartwithwaterfall
        """
        # Supported scenario's
        self.p_scenarios       = ['PY', 'PL']              # Previous Year, PLan
        self.p_scenarios_prio  = ['PL', 'PY']              # Priority for the p-scenarios: First PLan, then Previous Year
        self.c_scenarios       = ['AC', 'FC']              # ACtual, ForeCast
        self.c_scenarios_prio  = ['AC', 'FC']              # Priority for the c-scenarios: First AC, then FC
        self.all_scenarios     = ['PY', 'PL', 'AC', 'FC']  # Previous Year, PLan, ACtual, ForeCast (in order of time)
        
        # Decimals
        self.decimals_details  = 0
        self.decimals_totals   = 0
        
        # # Multipliers
        # self.multipliers            = ('1', 'k', 'm', 'b')            # Multiplier 1 (one, 10^0), k (kilo, 10^3), m (million, 10^6), b (billion, 10^9)
        # self.multipliers_value      = (1, 1000, 1000000, 1000000000)  # Values of the multipliers
        self.multiplier             = None                            # Initial value
        self.multiplier_denominator = 1                               # Denominator is the diviser
        
        # Other
        self.filename          = None       # When filename is None, no export
        

    def _optimize_multiplier(self):
        """
        Optimizes the multiplier.
        First we are going to find the biggest number of the details.
        Then we try to divide the biggest number by one or more multiplications of 1000. If you still have a number which is bigger than or equal to one then you can go on.
        
        Self variables
        --------------
        self.multiplier             : Multiplier which we will use during the output

        self.original_multiplier    : Original multiplier from the parameters of the calling of the class

        self.multiplier_denominator : The factor where each numeric value will be divided with
        
        self.decimals_details       : The number of decimals where the detail data will be rounded to
        
        self.decimals_totals        : The number of decimals where the total data will be rounded to
        
        self.data                   : Detail values for each scenario. Scenario is the key for the list of detail values
        
        self.data_total             : Total values for each scenario. Scenario is the key for the total value
 
        self.force_zero_decimals    : If True, we use integers for output. This gives a more clean chart, but can lack some detail in some cases

        self.force_max_one_decimals : If True, the maximum of decimals used is one. Know that force_zero_decimals has a higher priority than force_max_one_decimals
        """
        def _compare_values(old_value, new_value, type=None):
            """
            Helper function to determine wich is the biggest value.
            """
            returnvalue = None
            if type == 'max':
                if old_value == None:
                    returnvalue = new_value
                elif old_value < new_value:
                    returnvalue = new_value
                else:
                    returnvalue = old_value
            if type == 'min':
                if old_value == None:
                    returnvalue = new_value
                elif old_value > new_value:
                    returnvalue = new_value
                else:
                    returnvalue = old_value
            return returnvalue

        self.multiplier = Multiplier(self.original_multiplier.get_multiplier())
        
        # Find the min and the max of the details and of the totals
        max_detail = None
        min_detail = None
        max_total  = None
        min_total  = None
        for scenario in self.data.keys():
            if len(self.data[scenario]) == 0:
                continue
            max_temp = max([value for value in self.data[scenario] if value is not None])
            min_temp = min([value for value in self.data[scenario] if value is not None])
            max_detail = _compare_values(old_value=max_detail, new_value=max_temp                 , type='max')
            min_detail = _compare_values(old_value=min_detail, new_value=min_temp                 , type='min')
            max_total  = _compare_values(old_value=max_total , new_value=self.data_total[scenario], type='max')
            min_total  = _compare_values(old_value=min_total , new_value=self.data_total[scenario], type='min')
        
        big_detail = _compare_values(old_value=abs(min_detail) , new_value=abs(max_detail), type='max')
        big_total  = _compare_values(old_value=abs(min_total)  , new_value=abs(max_total) , type='max')
        
        self.multiplier_denominator = self.multiplier.optimize(big_detail)
        
        self.decimals_details  = max(0, 3 - len(str(int(round(big_detail / self.multiplier_denominator, 0)))))
        self.decimals_totals   = max(0, 3 - len(str(int(round(big_total / self.multiplier_denominator, 0)))))
        
        # Is the parameter force_zero_decimals set to True?
        if self.force_zero_decimals:
            # Yes, we are forcing zero decimals!
            self.decimals_details = 0
            self.decimals_totals = 0

        # Is the parameter force_max_one_decimals set to True?
        if self.force_max_one_decimals:
           # Yes, but force_zero_decimals has higher priority, so we take the minimum of the decimals currently and 1!
           self.decimals_details = min(self.decimals_details, 1)
           self.decimals_totals  = min(self.decimals_totals , 1)

        self._optimize_data()     # You need to do this step as the denominator and the changed multiplier needs to be in sync


    def _optimize_data(self):
        """
        Optimize the detail data and total data with the denominator and the number of decimals.

        Self variables
        --------------
        self.multiplier_denominator : The factor where each numeric value will be divided with
        
        self.decimals_details       : The number of decimals where the detail data will be rounded to
        
        self.decimals_totals        : The number of decimals where the total data will be rounded to
        
        self.data                   : Detail values for each scenario. Scenario is the key for the list of detail values
        
        self.data_total             : Total values for each scenario. Scenario is the key for the total value
        """
        for scenario in self.data.keys():
            self.data[scenario]       = optimize_data(data=self.data[scenario]      , numerator=1, denominator=self.multiplier_denominator, decimals=None)
            self.data_total[scenario] = optimize_data(data=self.data_total[scenario], numerator=1, denominator=self.multiplier_denominator, decimals=None)

 
    def _check_data(self, data=None):
        """Check if the keys of the dictionary are supported (PL, PY, AC, FC) and that the details are of the needed length.
           It also stores the datavalues in self.data, totalizes the data and store the totals in self.data_total, determines whether a grouped barchart is needed (self.barshift)

        Parameters
        ----------
        data : data contains a dictionary with the scenario's as a key and the detail values as a list, or a string-like CSV-file or a list of lists.
             (Default value = None)

        Self variables
        --------------
        self.barshift           : The barshift for the main part of the chart. This value will be overruled with barshift_value if there are other relevant scenario's available
        
        self.barshift_leftside  : The barshift for the left side part of the chart. This value will be overruled with barshift_value if there are relevant scenario's available
        
        self.barshift_value     : The portion a grouped bar chart will be out of the middle
        
        self.data               : Detail values for each scenario. Scenario is the key for the list of detail values
        
        self.data_total         : Total values for each scenario. Scenario is the key for the total value
        
        self.year               : Year of the data
        """
        # Do we need to convert the data to a dictionary? We support string (as CSV-file), list (of lists) and pandas DataFrame.
        if isstring(data):
            # data is in the form of a string. We need to convert it to a pandas DataFrame
            data = convert_data_string_to_pandas_dataframe(data)
            # data is now in the form of a pandas DataFrame
        if islist(data):
            # Data is in the form of a list (of lists). We need to convert it to a pandas DataFrame
            data = convert_data_list_of_lists_to_pandas_dataframe(data)
            # data is now in the form of a pandas DataFrame
        if isdataframe(data):
            # data is in the form of a pandas DataFrame
            data = self._prepare_dataframe(data)
            # data is now in the form of a dictionary
        
        # Check for existence of data
        if data is None:
            raise ValueError("No data available. Dictionary expected {'PY': [12x#], 'PL': [12x#], 'AC': [up to 12x#], 'FC': [up to 12x] }")
        
        # Was the parameter preferred_base_scenario given?
        if self.base_scenario is None:
            # No the parameter preferred_base_scenario was not given. We instead define this preference as most wanted 'PL' and less wanted 'PY'
            scenarios = [i for i in ['PL', 'PY'] if i in data.keys()]
            # See if there is a scenario to use as a base_scenario
            if len(scenarios) > 0:
                # Yes, we can use a base_scenario
                self.base_scenario = scenarios[0]
        
        # Check if the base_scenario is in the data
        if self.base_scenario not in data.keys():
            raise ValueError("Variable preferred_base_scenario "+str(self.base_scenario)+" is not available in provided data. Possible values are: "+str(list(data.keys())))

        # self.barshift is already initialized in the superclass     # barshift is used to group bars in Px vs xC comparison
        for scenario in data.keys():
            if scenario == 'PL' or scenario == 'PY':
                # Scenario is Plan or Previous Year, the length of values needs to be 12
                if len(data[scenario]) != 12: raise ValueError("For "+scenario+" expected list of 12 values")
                self.data[scenario]       = data[scenario]           # Make a copy of the values
                self.data_total[scenario] = sum(data[scenario])      # Sum the values as a total
                self.barshift             = self.barshift_value      # Yes, there is a PL or PY scenario, so the barshift value needs to be set <> 0
            elif scenario == 'AC':
                # Scenario is Actual, the length of the list of values needs to be somewhere between 1 and 12 (both inclusive)
                if len(data[scenario]) < 1 or len(data[scenario]) > 12: raise ValueError("For AC expected list minimal 1 up to 12 values, but not more")
                self.data[scenario]       = data[scenario]           # Make a copy of the values
                if sum(x is None for x in data[scenario]) > 0:
                    raise ValueError(str(data[scenario])+" contains one or more values of None. This is not supported for AC.")
                self.data_total[scenario] = sum(data[scenario])      # Sum the values as a total
            elif scenario == 'FC':
                # Scenario is Forecast, the length of the list of values needs to be somewhere between 1 and 12 (both inclusive)
                if len(data[scenario]) < 1 or len(data[scenario]) > 12: raise ValueError("For FC expected list minimal 1 up to 12 values, but not more")
                self.data[scenario]       = data[scenario]           # Make a copy of the values
                self.data_total[scenario] = sum([x for x in data[scenario] if type(x) != type(None)])            # Only sum the values as a total from real values (not the value None)
            elif scenario == 'Year':
                self.year = data['Year']
            else:
                # Not Plan, Not Previous Year, Not Actual, Not Forecast. Other scenario's are not supported
                raise ValueError("Unknown scenario. Known scenario's are PL, PY, AC, FC. Variable data contains: "+str(list(data.keys())))

        # Are there PL-values?
        if not self.force_pl_is_zero:
            # If pl is zero then this scenario can be deleted
            if 'PL' in self.data_total.keys():
                if self.data_total['PL'] == 0:
                    del self.data['PL']           # delete the dictionary-element with key PL from the data detailinformation
                    del self.data_total['PL']     # delete the dictionary-element with key PL from the data total-information

        # Centrally store the available scenarios (for filter_scenarios-function)
        self.data_scenarios = list(self.data_total.keys())

        # Determine barshift for leftside chart. self.barshift_leftside is already initialized in the superclass
        if len(self.filter_scenarios(["PY", "PL"])) == 2:
            # Both PY and PL are in the data set
            self.barshift_leftside = self.barshift_value

        # Is there forecast information which we can't use (because we have actual-information for all FC-columns) or do we have overlap in AC and FC information?
        if len(self.filter_scenarios(["AC", "FC"])) == 2:
            # Both AC and FC are in the data sets
            if len(self.data['AC']) >= len(self.data['FC']):
                # Actual is long enough to cover all columns. Can we delete FC so it don't disturbs outcomes?
                twin_value = 0
                ac_serie = 0
                fc_serie = 0
                for number, (ac, fc) in enumerate(zip(self.data['AC'],self.data['FC']), start=1):
                    if ac != 0 and ac_serie == number-1:
                        ac_serie = number
                        if fc is not None and fc != 0:
                            twin_value += 1  # Both ac and fc has a value
                    elif fc is not None and fc != 0:
                        if fc_serie == 0: fc_serie = number
                        if ac != 0: twin_value += 1

                temp_list = self.data["AC"][:]
                self.data["AC"] = temp_list[:ac_serie]
                if fc_serie == 0 or len(self.data["AC"]) == len(self.data["FC"]):
                    del self.data['FC']           # delete the dictionary-element with key FC from the data detailinformation
                    del self.data_total['FC']     # delete the dictionary-element with key FC from the data total-information
                    twin_value = 0
                if twin_value != 0:
                    raise ValueError("AC and FC overlapping not supported yet")
            
            if "FC" in self.data.keys():
                # Make sure that overlapping values are None, but only if the current FC-value is 0 or None
                temp_list = self.data['FC'][:]
                for index in range(len(self.data['AC'])):
                    if temp_list[index] == 0 or temp_list[index] == None:
                        temp_list[index] = None
                    else:
                        raise ValueError("Actuals overlap Forecast while Forecast has values: "+str(self.data['FC']))
                self.data['FC'] = temp_list[:]
        
        if self.base_scenario not in self.data_total.keys():
            temp_list = self.filter_scenarios(scenario_list=self.p_scenarios)
            if len(temp_list) == 0:
                raise ValueError("No PL or PY scenario available. Please use an other chart")
            else:
                self.base_scenario = temp_list[0]

        # Update centrally store the available scenarios (for filter_scenarios-function)
        self.data_scenarios = list(self.data_total.keys())

        # Optimize multiplier and data        
        self._optimize_multiplier()


    def _dataframe_aggregate(self, dataframe):
        """
        If the data is a pandas DataFrame, this function will aggregate this DataFrame by 'Year' and 'Month'.
        
        Precondition: The dataframe should only have the needed columns.

        Parameters
        ----------
        dataframe        : pandas DataFrame with hopefully a 'Year' and 'Month' column.
        
        Returns
        -------
        export_dataframe : aggregated pandas DataFrame, aggregated by 'Year' and 'Month'
        """
        # We need the 'Year' and 'Month' columns
        needed_headers = ['Year', 'Month']

        # Search for available headers
        available_headers = dataframe_search_for_headers(dataframe, search_for_headers=needed_headers, error_not_found=True)

        # Aggregate data
        export_dataframe = dataframe.groupby(available_headers).sum().reset_index()
        
        return export_dataframe


    def _dataframe_full_year(self, dataframe):
        """
        If the data is a pandas DataFrame, this function will make incomplete years complete by adding missing months.
        
        Precondition: The dataframe dataframe needs to be aggregated by Year and Month and only contains the data from one year.

        Parameters
        ----------
        dataframe        : pandas DataFrame with data from one year.
        
        Returns
        -------
        export_dataframe : empty pandas DataFrame or pandas DataFrame with 12 rows, one for each month
        """
        # We need the 'Year' and 'Month' columns
        needed_headers = ['Year', 'Month']

        # Search for available headers
        dataframe_search_for_headers(dataframe, search_for_headers=needed_headers, error_not_found=True)
        
        # Check for emptyness
        if dataframe.empty:
            # DataFrame is empty, return this empty dataframe
            export_dataframe = dataframe.copy()
            return export_dataframe

        min_year = dataframe['Year'].min()
        max_year = dataframe['Year'].max()
        if min_year != max_year:
            raise ValueError("More than one year in DataFrame. Min year:"+str(min_year)+". Max year:"+str(max_year))
        
        year = [str(min_year)] * 12  # min_year is equal to max_year. So max_year was also fine in this line of code
        month = [ ('00'+str(x))[-2:] for x in range(1,13)]  # Gives the numbers 1 to 12, both inclusive
        df = pd.DataFrame({'Year':year, 'Month':month})     # Makes a dataframe with 12 lines with Year and Month on each line

        # Fill full year
        export_dataframe = pd.merge(df, dataframe, how='left' ,on=['Year', 'Month']).copy()
        export_dataframe = export_dataframe.fillna(0)  # Fill the not-existing values with 0
        
        return export_dataframe
    

    def _dataframe_handle_previous_year(self, dataframe):
        """
        If the dataframe contains 2 years of actual information and also previous year information, then the actuals of previous year will be compared with
        the previous year information in the highest year. Error when not equal.
        If the dataframe contains 2 years of actual information and no previous year information, then the actuals of previous year will be
        the previous year information in the highest year.

        Parameters
        ----------
        dataframe         : pandas DataFrame with possibly more year information

        Returns
        -------
        export_dataframe  : pandas DataFrame with 'optimized' information of te highest year (possibly added with 'previous year' information)
        """
        # We need the 'Year' column
        needed_headers = ['Year']

        # Search for available headers
        dataframe_search_for_headers(dataframe, search_for_headers=needed_headers, error_not_found=True)

        # Determine the max-year and the year before the max-year. These will be the actual (AC) and previous year (PY)
        max_year        = dataframe['Year'].max()
        before_max_year = str(int(max_year)-1)

        # Split the dataframes in the actual and previous year
        df_ac = dataframe[dataframe['Year'] == max_year].copy()
        df_py = dataframe[dataframe['Year'] == before_max_year].copy()
        
        # Complete dataframe for missing month-values. Nothing worse than incomplete time-axis
        df_ac = self._dataframe_full_year(df_ac)
        df_py = self._dataframe_full_year(df_py)
        
        if 'PY' in df_ac.columns:
            if 'AC' in df_py.columns and not df_py.empty:
                # Dataframe with previous year information is not empty and has an actual column
                if not (df_ac['PY'] == df_py['AC']).all():
                    raise ValueError(str(max_year)+"-DataFrame previous year does not match "+str(before_max_year)+ "-Dataframe", str(df_ac), str(df_py))
                # else:
                #    Everything is fine, go further
            # else:
            #    No actual values in previous year dataframe or dataframe is empty
        else:
            # No previous year column in actual dataframe
            if 'AC' in df_py.columns and not df_py.empty:
                # We can use the actual values in te previous year dataframe as previous year values in the actual dataframe
                df_ac['PY'] = df_py['AC'].copy()
            # else:
            #   No actual values in previous year dataframe or dataframe is empty

        # Prepare export_dataframe
        export_dataframe = df_ac.copy()
        
        return export_dataframe


    def _dataframe_to_dictionary(self, dataframe):
        """
        Straight forward conversion of the column names into the keys and the values into a list of values.
        Only the year will be a single value.
        And make sure that next to the scenarios (PY, PL, AC and/or FC) there will only be the 'Year'. So delete 'Month' if available

        Parameters
        ----------
        dataframe         : pandas DataFrame with a 'Year' column and scenario (PY, PL, AC and/or FC) columns

        Returns
        -------
        export_dictionary : dictionary with scenarios (PY, PL, AC and/or FC) and a Year-value
        """
        # We need the 'Year' column
        needed_headers = ['Year']

        # Search for available headers
        dataframe_search_for_headers(dataframe, search_for_headers=needed_headers, error_not_found=True)

        # Convert to dictionary
        export_dictionary = dataframe.to_dict(orient='list')

        # Make a single year value
        export_dictionary['Year'] = dataframe['Year'].max()

        # Remove the 'Month'-entry, if available
        if 'Month' in export_dictionary:
            del export_dictionary['Month']

        # Convert the values (that can be of type string) from the scenarios in integer or float values
        for scenario in ['PY', 'PL', 'AC', 'FC']:
            if scenario in export_dictionary.keys():
                valuelist = export_dictionary[scenario]
                export_dictionary[scenario] = string_to_value(valuelist)

        return export_dictionary


    def _prepare_dataframe(self, dataframe):
        """
        This function orchestrates other functions to transform a pandas DataFrame into a dictionary of scenarios.

        Parameters
        ----------
        dataframe         : pandas DataFrame
        
        Returns
        -------
        export_dictionary : dictionary with for each available scenario a list of 12 values and one value for the Year
        """
        # If the dictionary self.translate_headers is filled with {'old-name':'new-name'} combinations, this will be translated in the upcoming function
        dataframe = dataframe_translate_field_headers(dataframe, translate_headers=self.translate_headers)

        # If the dataframe has a column named 'Date' then the date information in this column will be converted to the 'Year' and 'Month' columns.
        dataframe = dataframe_date_to_year_and_month(dataframe, date_field=self.date_column, year_field=self.year_column, month_field=self.month_column)

        # If the dataframe has more columns than relevant, only keep the relevant columns
        wanted_headers = self.year_column + self.month_column + self.all_scenarios
        dataframe = dataframe_keep_only_relevant_columns(dataframe, wanted_headers=wanted_headers)

        # It is possible that the dataframe has more detailed lines (especially when removing non-relevant columns). Aggregate them on Year/Month-level
        dataframe = self._dataframe_aggregate(dataframe)

        # Convert year and month to strings and sort the dataframe on year and month
        wanted_headers = self.year_column + self.month_column
        dataframe_search_for_headers(dataframe, search_for_headers=wanted_headers, error_not_found=True)   # Year and Month needs to be column headers
        dataframe = dataframe_convert_year_month_to_string(dataframe, wanted_headers=wanted_headers, year_field=self.year_column, month_field=self.month_column)

        # Handle previous year information
        dataframe = self._dataframe_handle_previous_year(dataframe)

        # Transform the DataFrame into a dictionary
        export_dictionary = self._dataframe_to_dictionary(dataframe)

        return export_dictionary
        

    def _make_subplots(self):
        """
        Creates the figure and subplots:
           subplot "left" for a total bar of the previous year and/or a total bar of the plan information
           subplot "main" for the detail bars and the delta graphics
           subplot "sum" for the total of actuals and forecast data
           subplot "comment" for extra lines and texts

        Self variables
        --------------
        self.fig      : Figure-object for the generated plot and subplots

        self.ax       : Dictionary of axesobjects for the generated subplots

        """
        self.ax = dict()
        
        scenarios = self.filter_scenarios(scenario_list=['PY', 'PL'])
        if len(scenarios) == 2:
            left_width = 1.8
        else:
            left_width = 1.4
        
        self.fig, (self.ax["left"], self.ax["main"], self.ax["sum"], self.ax["comment"]) = \
                   plt.subplots(nrows=1, ncols=4, sharey='row', figsize=(15,6),
                                gridspec_kw={'width_ratios': [left_width, 15, 1.4, 1.2]})
                                #width_ratios=[left_width, 15, 1.2, 1.2]) # From matplotlib-version 3.6.0 and above

        #plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.15, hspace=None)   # wspace is for the space between the subplots
        self.fig.set_facecolor('white')   # Make a white background so the export to a file will have a white background

    
    def _fill_main_ax(self):
        """
        Fill all the components of the main ax:
           plot bars for the comparison scenario, AC and/or FC
           put text on the bars
           put label for the months

        Self variables
        --------------
        self.base_scenario  : scenario to use for comparison bars, next to AC and/or FC
        """
        for scenario in self.filter_scenarios(scenario_list=[self.base_scenario, 'AC', 'FC']):
            self._fill_main_ax_bar(scenario=scenario)
        self._fill_main_ax_text()
        self._fill_main_ax_monthlabel()
        
        
    def _fill_main_ax_bar(self, scenario):
        """
        Plots the bars from the comparison scenario and the actual and the forecast scenario

        Parameters
        ----------
        scenario              : the scenario of which the bars will be plotted

        Self variables
        --------------
        self.data             : is a dictionary of the detaildata

        self.barshift         : the barshift for the main part of the chart.

        self.barwidth         : a float with the width of the bars for measure of ratio

        self.colors           : a dictionary of colors needed for the consistent look of the charts

        self.linewidth_bar    : the width of the lines from a bar

        self.hatch            : the pattern for hatched

        self.data_text        : a dictionary with the number of the matplotlib-ax-containers of the bar-data including the texts of the bars

        self.decimals_details : number of decimals for detailed information
        """
        scenario_data = optimize_data(data=self.data[scenario], numerator=1, denominator=1, decimals=self.decimals_details)
        ax = self.ax["main"]
        if scenario[0] == 'P':
            xvalue = [x - self.barshift * self.barwidth for x in range(len(scenario_data))]
            ax.bar(xvalue, scenario_data, color=self.colors[scenario][0], width=self.barwidth, linewidth=self.linewidth_bar, edgecolor=self.colors[scenario][1], label=scenario)
        if scenario == 'AC':
            xvalue = [x + self.barshift * self.barwidth for x in range(len(scenario_data))]
            ax.bar(xvalue, scenario_data, color=self.colors[scenario][0], width=self.barwidth, linewidth=self.linewidth_bar, edgecolor=self.colors[scenario][1], label=scenario)
        if scenario == 'FC':
            xvalue = [x + self.barshift * self.barwidth for x in range(len(scenario_data))]
            ax.bar(xvalue[scenario_data.count(None):len(scenario_data)], 
                       scenario_data[scenario_data.count(None):], color=self.colors[scenario][0], width=self.barwidth, linewidth=self.linewidth_bar, edgecolor=self.colors[scenario][1], 
                       label=scenario, hatch=self.hatch)
        self.data_text[scenario] = len(ax.containers)-1


    def _fill_main_ax_text(self):
        """
        Fills the valuelabels above the AC and FC scenario on the main ax
        
        Self variables
        --------------
        self.ax          : Dictionary of axesobjects for the generated subplots

        self.padding     : Padding between the bars and the text

        self.font        : All text in a chart has the same font
        
        self.fontsize    : All text in a chart has the same height
        
        self.data_text   : A dictionary with the number of the matplotlib-ax-containers of the bar-data including the texts of the bars
        """
        ax = self.ax["main"]
        format_string = formatstring(self.decimals_details)
        # Puts the values of actual and forecast above the bars in the 12 months bars.
        for scenario in self.filter_scenarios(scenario_list=['AC', 'FC']):
            # Only the available scenario's will be processed. With a full year of actuals, no forecast is left.
            ax.bar_label(ax.containers[self.data_text[scenario]], fmt=format_string, label_type='edge', padding=self.padding, font=self.font, fontsize=self.fontsize )


    def _fill_main_ax_monthlabel(self):
        """
        Fills the month information on the x-axis in the main-ax-area
        
        Self variables
        --------------
        self.ax             : Dictionary of axesobjects for the generated subplots

        self.colors         : A dictionary with all color information

        self.barwidth       : A float with the width of the bars for measure of ratio
        
        self.main_months    : Month-names with delta scenario information. Delta_name is the key for the list of month-names

        self.font           : All text in a chart has the same font
        
        self.fontsize       : All text in a chart has the same height
        
        self.linewidth_zero : Linewidth of the zeroline
        
        self.barshift       : Information about how much we need to shift the bar to fit right on top of the other charts
        """
        ax = self.ax["main"]
        ax.tick_params(top=False, bottom=False, left=False, right=False, labelleft=False, labelbottom=True)
        
        # Make a list of coordinates to shift the names of the months a bit to the right (if there is a comparison in the chart)
        xvalue = [x + self.barshift * self.barwidth for x in range(len(self.main_months["main"]))]
        ax.set_xticks(xvalue, self.main_months["main"], font=self.font, fontsize=self.fontsize)
        ax.spines[['top', 'left', 'right', 'bottom']].set_visible(False)
        
        # This is the "Zeroline"
        plot_line_within_ax(ax=ax, xbegin=0-0.5, ybegin=0, xend=11+0.5, yend=0, linecolor=self.colors['zeroline'], arrowstyle='-', linewidth=self.linewidth_zero, endpoints=False, endpointcolor=None)

    
    def _fill_leftside_ax(self): 
        """
        Fills the leftside ax (left of the main ax) with Previous Year and/or Plan information

        Self variables
        --------------
        self.ax            : Dictionary of axesobjects for the generated subplots

        self.font          : All text in a chart has the same font
        
        self.fontsize      : All text in a chart has the same height
        
        self.colors        : A dictionary with all color information

        self.barwidth      : A float with the width of the bars for measure of ratio
        
        self.linewidth_bar : The width of the lines from a bar

        self.data_total    : Total values for each scenario. Scenario is the key for the total value

        self.year          : Year of the data
        
        self.fig              : Figure-object for the generated plot and subplots

        self.delta_base_value : Base_values for the delta charts. Delta_name is the key for the value

        self.linewidth_line_n : The normal width of the lines
        
        self.barshift_leftside  : The barshift for the left side part of the chart. This value will be overruled with barshift_value if there are relevant scenario's available
        
        self.outside_factor   : Factor to use to keep lines as much as possible outside of the bars
        
        self.base_scenario  : scenario to use for comparison bars, next to AC and/or FC
        """
        ax = self.ax["left"]

        scenarios = self.filter_scenarios(scenario_list=['PY', 'PL'])

        for scenario in scenarios:
            PY_valuetext_special = False
            if len(scenarios) == 2:
                # Yes, there are 2 scenario's. We need to put the bar of PY on the left and PL on the right.
                textadjustment = 0.8
                if scenario == 'PY':
                    # Scenario is Previous Year
                    barsign    = -1     # Negative factor to place the PY-bar a bit to the left
                    if self.data_total['PY'] > self.data_total['PL']: linesign = -1
                    else: linesign = +1  
                    textsign   = -1
                    halignment = 'right'
                    xend       = 1    # We need a line to the end of the ax-comments if there are 2 scenario's for the PY-scenario
                    if self.data_total['PY'] < self.data_total['PL']*1.1: PY_valuetext_special = True  # PY-bar is not high enough to have it's value centered
                else:
                    # Scenario is PLan
                    barsign    = +1     # Positive factor to place the PL-bar a bit to the right
                    linesign   = +1
                    textsign   = +1
                    halignment = 'left'
                    xend       = 0    # The line needs to go to the beginning of the ax-comments if there are 2 scenario's for the PL-scenario
            else:
                # No, there is only 1 scenario. We put it in the middle
                textadjustment = 0.6
                barsign    = 0
                linesign   = 1
                textsign   = -1
                halignment = 'right'
                xend       = 0

            # Make the line accross the axes for the scenario
            base_value = self.data_total[scenario]
            xbegin = 0 + (linesign * self.barshift_leftside) + (self.barwidth/2 * self.outside_factor)  
            plot_line_accross_axes(fig=self.fig, axbegin=self.ax["left"],    xbegin=xbegin,  ybegin=base_value,
                                                 axend  =self.ax["comment"], xend  =xend,    yend  =base_value,
                                                 endpoints=False, linecolor=self.colors['line'], arrowstyle='-', linewidth=self.linewidth_line_n, endpointcolor=None)

            # Remember the base_value for the integrated waterfall delta chart
            if self.base_scenario == scenario:
                self.delta_base_value['main'] = base_value

            # Make the column for the scenario            
            ax.bar(0 + (barsign * self.barshift_leftside), self.data_total[scenario], color=self.colors[scenario][0], width=self.barwidth, linewidth=self.linewidth_bar, edgecolor=self.colors[scenario][1], label=scenario)

            # Put the value on the column for the scenario
            if PY_valuetext_special:
                # The PL-column with text is so high, that the valuetext of the PY-column needs to be more adjusted to the left.
                ax.text(0-self.barwidth/2.5, self.data_total[scenario]*(1+(self.padding/250)),
                        s=convert_number_to_string(data=self.data_total[scenario], decimals=self.decimals_totals, delta_value=False),
                        horizontalalignment='right', verticalalignment='bottom',
                        font=self.font, fontsize=self.fontsize, color=self.colors['text'])
            else:
                # The PL-column with text is small enough, that we can put the valuetext centered on top of the PY-column.
                string_list = [convert_number_to_string(data=self.data_total[scenario], decimals=self.decimals_totals, delta_value=False)]
                ax.bar_label(ax.containers[-1], labels=string_list, label_type='edge', padding=self.padding, font=self.font, fontsize=self.fontsize)

            #if len(self.filter_scenarios(['PY', 'PL'])) > 1:
                # Inline legend (barwidth * 0.8 to be close to the bar, but not adjacent)
            ax.text(0 + (textsign * self.barwidth * textadjustment), self.data_total[scenario]/2, scenario, horizontalalignment=halignment, font=self.font, 
                         fontsize=self.fontsize, color=self.colors['text'], verticalalignment='center')
               
                
        ax.tick_params(top=False, bottom=False, left=False, right=False, labelleft=False, labelbottom=True)
        # Puts the name of the year under the PL-bar
        ax.set_xticks([0+self.barshift_leftside], [str(self.year)], font=self.font, fontsize=self.fontsize)
        ax.spines[['top', 'left', 'right', 'bottom']].set_visible(False)
        
        # This is the "Zeroline"
        plot_line_within_ax(ax=ax, xbegin=0-self.barshift_leftside-0.37, ybegin=0, xend=0+self.barshift_leftside+0.37, yend=0, linecolor=self.colors['zeroline'], arrowstyle='-', linewidth=self.linewidth_zero, endpoints=False, endpointcolor=None)
    
    
    def _fill_side_axsum(self): 
        """
        Fills the subplot with the (stacked) bar on the right of the main ax.

        Self variables
        --------------
        self.ax              : Dictionary of axesobjects for the generated subplots

        self.padding         : Padding between the bars and the text

        self.font            : All text in a chart has the same font

        self.fontsize        : All text in a chart has the same height

        self.colors          : A dictionary with all color information

        self.barwidth        : A float with the width of the bars for measure of ratio

        self.decimals_totals : Number of decimals for total information

        self.linewidth_bar   : The width of the lines from a bar

        self.data_total      : Total values for each scenario. Scenario is the key for the total value

        self.year            : Year of the data
        """
        ax = self.ax["sum"]
        bottom = 0 

        scenarios = self.filter_scenarios(scenario_list=['AC', 'FC'])

        for scenario in scenarios:
            # Determine the hatch
            hatch = None
            if scenario == 'FC': 
                hatch = self.hatch

            # Plot the (part of the stacked) bar (due to parameter bottom)
            ax.bar(0, self.data_total[scenario], color=self.colors[scenario][0], width=self.barwidth, linewidth=self.linewidth_bar,
                   edgecolor=self.colors[scenario][1], bottom=bottom, label=scenario, hatch=hatch)

            # Inline legend (barwidth * 0.6 to be close to the bar, but not adjacent)
            ax.text(0+self.barwidth*0.6, bottom + self.data_total[scenario]/2, scenario, horizontalalignment='left', font=self.font, fontsize=self.fontsize, color=self.colors['text'], verticalalignment='center')

            # Only stacked bar values inside if more than 1 scenario
            if len(scenarios)>1:
                # Round the value with the desired number of decimals and make it a string
                value_string = convert_number_to_string(data=self.data_total[scenario], decimals=self.decimals_totals, delta_value=False)

                # Two different kinds of adding text in the bars
                if scenario == 'FC':
                    # use text function because the use of backgroundcolor
                    ax.text(0, bottom + self.data_total[scenario]/2, s=value_string, horizontalalignment='center',
                            verticalalignment='center', font=self.font, fontsize=self.fontsize, color=self.colors[scenario][2],
                            backgroundcolor=self.colors[scenario][3],
                            bbox=dict(facecolor=self.colors[scenario][3], edgecolor='none', pad=0.8, alpha=0.85))
                else:
                    # use standard label function
                    ax.bar_label(ax.containers[-1], labels=[value_string], label_type='center', font=self.font, fontsize=self.fontsize, color=self.colors[scenario][2])

            bottom = bottom + self.data_total[scenario]

        # add top label
        # Round the value with the desired number of decimals and make it a string
        value_string = convert_number_to_string(data=bottom, decimals=self.decimals_totals, delta_value=False)
        ax.bar_label(ax.containers[-1], labels=[value_string], label_type='edge', padding=self.padding, font=self.font, fontsize=self.fontsize, color=self.colors['text'])

        ax.tick_params(top=False, bottom=False, left=False, right=False, labelleft=False, labelbottom=True)
        ax.set_xticks([0], [str(self.year)], font=self.font, fontsize=self.fontsize)
        ax.spines[['top', 'left', 'right', 'bottom']].set_visible(False)   
        plot_line_within_ax(ax=ax, xbegin=0-0.37, ybegin=0, xend=0+0.37, yend=0, linecolor=self.colors['zeroline'], arrowstyle='-', linewidth=self.linewidth_zero, endpoints=False, endpointcolor=None)

    def _show_delta(self, delta_name='main', last_line=True):
        """
        Plots a delta bar on the main ax subplot of the chart

        Self variables
        --------------
        self.ax               : Dictionary of axesobjects for the generated subplots

        self.fig              : Figure-object for the generated plot and subplots

        self.data_text        : A dictionary with the number of the matplotlib-ax-containers of the bar-data including the texts of the bars

        self.delta_base_value : Base_values for the delta charts. Delta_name is the key for the value

        self.barshift         : Information about how much we need to shift the bar to fit right on top of the other charts

        self.colors           : A dictionary with all color information

        self.barwidth         : A float with the width of the bars for measure of ratio
        
        self.linewidth_line_n : The normal width of the lines
        
        self.linewidth_bar    : The width of the lines from a bar
        """
        # For the best visual, first plot the line, then plot the bars.
        # In that case, when you zoom in on the visual, the bars are neat and not slightly overwritten by the lines
        #### This is the theory, but when I look at the visuals, this is not always the case... Need to improve on this.
        
        ax = self.ax["main"]
        
        # Get the info of the delta bar
        delta_info = self.prepare_delta_bar(base_value=self.delta_base_value[delta_name],delta_name=delta_name, waterfall=True)

        if delta_info == dict():
            return

        # Make lines between the future bars so it looks like a waterfall
        for xvalue, yvalue in enumerate(delta_info['connect'][:-1]):
            point1 = ( (0 + xvalue + self.barshift * self.barwidth + (self.barwidth / 2)), yvalue)
            point2 = ( (1 + xvalue + self.barshift * self.barwidth - (self.barwidth / 2)), yvalue)
            plot_line_within_ax(ax=ax, xbegin=point1[0], ybegin=point1[1], xend=point2[0], yend=point2[1], linecolor=self.colors['line'], arrowstyle='-', linewidth=self.linewidth_line_n, endpoints=False, endpointcolor=None)

        if last_line == True:
            # Plot the last line accross axes so it ends in the sum axis
            plot_line_accross_axes(fig=self.fig, axbegin=ax, xbegin=len(delta_info['connect'])-1 + self.barshift * self.barwidth + (self.barwidth / 2),  ybegin=delta_info['connect'][-1],
                                   axend=self.ax["sum"],      xend=0-(self.barwidth/2), yend=delta_info['connect'][-1],
                                   endpoints=False, linecolor=self.colors['line'], arrowstyle='-', linewidth=self.linewidth_line_n, endpointcolor=None)
        
        # Plot the delta bar
        ax.bar(delta_info['xvalue'], delta_info['yvalue'], bottom=delta_info['bottom'], color=delta_info['color'], width=self.barwidth, linewidth=self.linewidth_bar, edgecolor=delta_info['edgecolor'], 
                       label=delta_info['scenario_label'], hatch=delta_info['hatch'], zorder=10)
        self.data_text['delta'] = len(ax.containers)-1

        
    def _fill_delta_ax_text(self, delta_name='main'):
        """
        Puts the text on the delta charts
        
        Self variables
        --------------
        self.ax          : Dictionary of axesobjects for the generated subplots

        self.delta_value : A dictionary with lists of delta values

        self.data_text   : A dictionary with the number of the matplotlib-ax-containers of the bar-data including the texts of the bars

        self.padding     : Padding between the bars and the text

        self.font        : All text in a chart has the same font
        
        self.fontsize    : All text in a chart has the same height
        """
        ax = self.ax["main"]
        label_value_list = convert_number_to_string(data=self.delta_value[delta_name], decimals=self.decimals_details, delta_value=True)
        
        if len(label_value_list) > 0:
            ax.bar_label(ax.containers[self.data_text['delta']], labels=label_value_list, label_type='edge', padding = self.padding, font=self.font, fontsize=self.fontsize, zorder=10)



    def _fill_axcomments(self):
        """
        Fills the last subplot with the lines, delta-lines and numbers of differences

        Self variables
        --------------
        self.ax               : Dictionary of axesobjects for the generated subplots
        
        self.fig              : Figure-object for the generated plot and subplots
        
        self.font             : All text in a chart has the same font
        
        self.fontsize         : All text in a chart has the same height
        
        self.colors           : Collection of colors. IBCS advices green for good variance, red for bad variance and blue for highlight. The rest is monochrome.
        
        self.barwidth         : A float with the width of the bars for measure of ratio
        
        self.linewidth_line_n : The normal width of the lines
        
        self.linewidth_delta  : The width of the delta-lines with the good or bad colors
        
        self.outside_factor   : Factor to use to keep lines as much as possible outside of the bars
        
        self.data_total       : Total values for each scenario. Scenario is the key for the total value
        """
        ax = self.ax["comment"]

        # Calculate the maximum value of the axsum-bars
        yvaluesum = 0
        for scenario in self.filter_scenarios(scenario_list=['AC', 'FC']):
            yvaluesum += self.data_total[scenario]
        
        # Determine the end-coordinate for the PY and PL scenario's
        scenarios = self.filter_scenarios(scenario_list=['PL', 'PY'])
        if len(scenarios) == 2:
            xend = 1                 # The end of a normal ax is 1, so we need to go to the last value for 2 scenario's
            textadjustment = 0.12    # While having 2 scenario's, the textadjustment to set the numbers is bigger than for 1 scenario. #### I'm searching for a better implementation of this
        else: 
            xend = 0                 # If you have 1 scenario, you can keep everything in the neighbourhood of 0
            textadjustment = 0.01    # If you have 1 scenario, the textadjustment-value makes a larger impact than with 2 scenario's above. #### I'm searching for a better implementation of this
        
        # Plot line from the top of the ax-sum-bar to the ax-comment
        plot_line_accross_axes(fig=self.fig, axbegin=self.ax["sum"], xbegin=0 + (self.barwidth/2)*(self.outside_factor), ybegin=yvaluesum, axend=self.ax["comment"], xend=xend, yend=yvaluesum, 
                          endpoints=False, linecolor=self.colors['line'], arrowstyle='-', linewidth=self.linewidth_line_n, endpointcolor=None)

        # For each scenario (PY and/or PL), plot the vertical deltabar in the right color and put the number next to that vertical bar
        for xbegin, scenario in enumerate(scenarios):
            yvalue_scenario = self.data_total[scenario]
            color = self.good_or_bad_color(differencevalue=yvaluesum-yvalue_scenario)

            # Plot vertical bar in a good or bad color
            plot_line_within_ax(ax=self.ax["comment"], xbegin=xbegin, ybegin=yvaluesum, xend=xbegin, yend=yvalue_scenario, endpoints=False, linecolor=color, arrowstyle='-', linewidth=self.linewidth_delta)
        
            # Set the value next to the vertical bar
            ####value = optimize_data(data=(yvaluesum-yvalue_scenario), numerator=1, denominator=1, decimals=self.decimals_totals)
            ax.text(xbegin + textadjustment, (yvaluesum+yvalue_scenario)/2,
                    s=convert_number_to_string(data=yvaluesum-yvalue_scenario, decimals=self.decimals_totals, delta_value=True),
                    horizontalalignment='left', verticalalignment='center',
                    font=self.font, fontsize=self.fontsize, color=self.colors['text'], zorder=10)

        ax.tick_params(top=False, bottom=False, left=False, right=False, labelleft=False, labelbottom=False)
        ax.spines[['top', 'left', 'right', 'bottom']].set_visible(False)


    def _title(self, title=None):
        """
        Puts a title in the upper left corner of the chart
        
        Parameters
        ----------
        title : a dictionary with text values to construct a title. No part of the title is mandatory, except when 'Business_measure' is filled, the 'Unit' is expected to be filled too.
             (default value: None). No title will be constructed with value None.
        
                more info:
                     title['Reporting_unit'] = 'Global Corporation'     # This is the name of the company or the project or business unit, added with a selection. For example 'ACME inc., Florida and California'
                     title['Business_measure'] = 'Net profit'           # This is the name of the metric. Can also be a ratio. For example: 'Net profit' or 'Cost per headcount'
                     title['Unit'] = 'mUSD'                             # This is the name of the unit. For example: 'USD', 'EUR', '#', '%'. Add k for 1000, m for 1000000 and b for 1000000000
                     title['Time'] = '2022: AC Jan..Aug, FC Sep..Dec'   # This is the description of the time, scenario's and variances. For example: '2022 AC, PL, FC, PL%'
        
        Self variables
        --------------
        self.ax       : dictionary of axesobjects for the generated subplots
        
        self.font     : all text in a chart has the same font
        
        self.fontsize : all text in a chart has the same height
        
        self.colors   : collection of colors. IBCS advices green for good variance, red for bad variance and blue for highlight. The rest is monochrome.
        
        self.barwidth : a float with the width of the bars for measure of ratio
        """
        
        title_text = prepare_title(title, multiplier=self.multiplier.get_multiplier_string())
        # Check if there is a title prepared
        if title_text == None:
            # No title
            return
        
        # Determine in which ax the title needs to start
        scenario = self.filter_scenarios(scenario_list=['PY', 'PL'])
        if len(scenario) == 0:
           # No Previous Year or Plan
           ax = self.ax["main"]
        else:
           # The left ax
           ax = self.ax["left"]
           
        #from matplotlib import rcParams as mpl_rcp  # This line is on top of this module, but only needed for this below.
        mpl_rcp['mathtext.rm'] = self.font           # import matplotlib as mpl : mpl.rcParams['mathtext.rm'] = self.font   ## This should do the same, but imports a whole matplotlib
        
        
        # Get the current limits of the axis
        limits = ax.axis()  # 4th value. Also possible with ax.get_ylim(), but then 2nd value
        
        # Plot the title
        #### Need to think of a good strategy to fit the title at best!
        ax.text(0 - self.barwidth*1.2, limits[3]*1.1, title_text, horizontalalignment='left', font=self.font, fontsize=self.fontsize, color=self.colors['text'], verticalalignment='bottom')