"""ColumnWithWaterfall-module"""

import matplotlib.pyplot as plt                   # for most graphics
from matplotlib import rcParams as mpl_rcp        # for font in _title
#from matplotlib import __version__ as mpl_version
import pandas as pd                               # for easy pandas support

from clean_business_chart.clean_business_chart import GeneralChart 
from clean_business_chart.general_functions    import plot_line_accross_axes, plot_line_within_ax, prepare_title, formatstring, optimize_data, \
                                                      islist, isdictionary, isinteger, isstring, isfloat, isboolean, isdataframe, string_to_value
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
    data                    : A dictionary with minimal PL and AC or PY and AC detailinformation, a string with CSV-values or a list of lists is also supported. Read the documentation.
    positive_is_good        : On a variance chart it decides whether a positive number makes a good color (True) or a bad number (False).
                              Default: True (good color)
    preferred_base_scenario : PL, use PLaninfo as the base scenario in the main chart. PY uses Previous Year als the base scenario in the main chart
    title                   : A dictionary with optional values to make a title inspired by IBCS
                              Default: None (no title)
    measure                 : True -> measure, False -> ratio
                              Default: True (measure)
    multiplier              : One character with the multiplier ('1', 'k', 'm', 'b')
                              Default: '1' (one)
    filename                : String with filename and path to export the chart to, including extention. Only tested with a .png-extention
                              Default: None (no export of the chart to a file)
    force_pl_is_zero        : If PL are all zeros, can PL be ignored (False) or force that PL can be zero (True)
                              Default: False (PL can be ignored when all zeros)
    force_zero_decimals     : If True, we use integers for output. This gives a more clean chart, but can lack some detail in some cases
                              Default: False (don't force zero decimals)
    force_max_one_decimals  : If True, the maximum of decimals used is one. Know that force_zero_decimals has a higher priority than force_max_one_decimals.
                              Default: False (don't force max one decimals)
    test                    : If True, only variables from the parent class are defined, together with other self-variables.
                              This makes this module testable in an automatic way
                              Default: False (this call it is not an automatic test)
    """

    def __init__(self, data=None, positive_is_good=True, preferred_base_scenario='PL', title=None, measure=True, multiplier='1', filename=None, 
                 force_pl_is_zero=False, force_zero_decimals=False, force_max_one_decimals=False, test=False):
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
            self.data[scenario]       = optimize_data(data=self.data[scenario]      , numerator=1, denominator=self.multiplier_denominator, decimals=self.decimals_details)
            self.data_total[scenario] = optimize_data(data=self.data_total[scenario], numerator=1, denominator=self.multiplier_denominator, decimals=self.decimals_totals)

 
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
        # Do we need to convert the data to a dictionary? We support string and list.
        if isstring(data):
            # data is in the form of a string. We need to convert it to a list of lists (easier step) to prepare the conversion to a dictionary
            data = self._convert_data_string_to_list_of_lists(data)
            # data is now in the form of a list of lists
        if isdataframe(data):
            # data is in the form of a pandas DataFrame
            data = self._prepare_data_frame(data)
            # data is now in the form of a dictionary
        if islist(data):
            # Data is in the form of a list (of lists). We need to convert it to a dictionary
            data = self._convert_data_list_of_lists_to_dict(data)
        
        # Check for existence of data
        if data is None:
            raise ValueError("No data available. Dictionary expected {'PY': [12x#], 'PL': [12x#], 'AC': [up to 12x#], 'FC': [up to 12x] }")
        
        # Check for the existence of the base_scenario
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
                    elif ac != 0:
                        raise ValueError("Actual values of 0 are not supported yet")
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
        
        
        # Optimize multiplier and data        
        self._optimize_multiplier()


    def _convert_data_string_to_list_of_lists(self, data_string):
        """
        If the data is like a string, this function sees it as a CSV-file pasted in a string and will make it first to a list of lists.

        Parameters
        ----------
        data_string : data_string contains a string-like CSV-file.
        
        Returns
        -------
        data_list   : data_list contains a list of lists
        """
        # Check if the data_string is not a string
        if not isstring(data_string):
            raise ValueError(str(data_string)+" is not a string")
        
        # Split the string into lines, based on the 'new line'-character
        lines = data_string.splitlines()
        
        # Create an empty list to receive each line (as a list). So we end with the variable data_list as a list of lists.
        data_list = list()
        for line in lines:
            if len(line.strip()) == 0:
                # skip the empty line
                continue
            splitted_line = line.strip().split(',')
            data_list.append(splitted_line)
        
        return data_list

    def _convert_dataframe_to_list_of_lists_old_(self, dataframe):
        """
        If the data is a pandas DataFrame, this function will make it to a list of lists.

        Parameters
        ----------
        dataframe : pandas DataFrame containing the columns Year and Month mandatory and the columns PY, PL, AC and/or FC.
        
        Returns
        -------
        data_list   : data_list contains a list of lists
        """
        # Check if the dataframe is not a pandas DataFrame
        if not isdataframe(dataframe):
            raise ValueError(str(dataframe)+" is not a pandas DataFrame")

        dataframe = self._data_frame_keep_only_relevant_columns(dataframe)
        dataframe = self._data_frame_aggregate(dataframe)

        data_list = [dataframe.columns.tolist()] + dataframe.values.tolist()

        return data_list

    def _data_frame_keep_only_relevant_columns(self, dataframe):
        """
        If the data is a pandas DataFrame, this function will narrow this DataFrame down to the needed columns.

        Parameters
        ----------
        dataframe        : pandas DataFrame with a lot of columns.
        
        Returns
        -------
        export_dataframe : pandas DataFrame with at most the columns 'Year', 'Month', 'PY', 'PL', 'AC' and 'FC'
        """
        # Check if the dataframe is not a pandas DataFrame
        if not isdataframe(dataframe):
            raise ValueError(str(dataframe)+" is not a pandas DataFrame")

        wanted_headers = ['Year', 'Month', 'PY', 'PL', 'AC', 'FC']

        # Determine which wanted headers are available in the dataframe
        available_headers = [x for x in wanted_headers if x in dataframe.columns]

        # We only need the data from the columns for the purpose of this chart
        export_dataframe = dataframe[available_headers].copy()
        
        return export_dataframe

    def _data_frame_aggregate(self, dataframe):
        """
        If the data is a pandas DataFrame, this function will aggregate this DataFrame by 'Year' and 'Month'.
        
        Precondition: The dataframe should only have te needed columns.

        Parameters
        ----------
        dataframe        : pandas DataFrame with hopefully a 'Year' and 'Month' column.
        
        Returns
        -------
        export_dataframe : aggregated pandas DataFrame, aggregated by 'Year' and 'Month'
        """
        # Check if the dataframe is not a pandas DataFrame
        if not isdataframe(dataframe):
            raise ValueError(str(dataframe)+" is not a pandas DataFrame")

        # We need the Year and Month columns
        needed_headers = ['Year', 'Month']

        # Determine which needed headers are available in the dataframe
        available_headers = [x for x in needed_headers if x in dataframe.columns]

        if available_headers != needed_headers:
            raise ValueError("Expected columns in the DataFrame: "+str(needed_headers)+". But found only these columns: "+str(available_headers))

        # Aggregate data
        export_dataframe = dataframe.groupby(available_headers).sum().reset_index()
        
        return export_dataframe

    def _data_frame_full_year(self, dataframe):
        """
        If the data is a pandas DataFrame, this function will make incomplete years complete by adding missing months.
        
        Precondition: The dataframe dataframe needs to be aggregated by Year and Month and only contains the data from one year.

        Parameters
        ----------
        dataframe        : pandas DataFrame with data from one year.
        
        Returns
        -------
        export_dataframe : pandas DataFrame with 12 rows, one for each month
        """
        # Check if the dataframe is not a pandas DataFrame
        if not isdataframe(dataframe):
            raise ValueError(str(dataframe)+" is not a pandas DataFrame")

        # We need the Year and Month columns
        needed_headers = ['Year', 'Month']

        # Determine which needed headers are available in the dataframe
        available_headers = [x for x in needed_headers if x in dataframe.columns]
        
        if available_headers != needed_headers:
            raise ValueError("Expected columns in the DataFrame: "+str(needed_headers)+". But found only these columns: "+str(available_headers))

        min_year = dataframe['Year'].min()
        max_year = dataframe['Year'].max()
        if min_year != max_year:
            raise ValueError("More than one year in DataFrame. Min year:"+str(min_year)+". Max year:"+str(max_year))
        
        year = [str(min_year)] * 12
        month = [ ('00'+str(x))[-2:] for x in range(1,13)]  # Gives the numbers 1 to 12, both inclusive
        df = pd.DataFrame({'Year':year, 'Month':month})

        # Fill full year
        export_dataframe = pd.merge(df, dataframe, how='left' ,on=['Year', 'Month'])
        export_dataframe = export_dataframe.fillna(0)
        
        return export_dataframe
    
    def _convert_year_month_to_string_dataframe(self, dataframe):
        """
        If the data is a pandas DataFrame, this function will convert the year and month to string values (containing numbers) for convenient sorting.
        
        Precondition: The dataframe dataframe needs to be aggregated by Year and Month.

        Parameters
        ----------
        dataframe        : pandas DataFrame, aggregated by Year and Month.
        
        Returns
        -------
        export_dataframe : pandas DataFrame sorted by Year and Month
        """
        # Check if the dataframe is not a pandas DataFrame
        if not isdataframe(dataframe):
            raise ValueError(str(dataframe)+" is not a pandas DataFrame")

        # We need the Year and Month columns
        needed_headers = ['Year', 'Month']

        # Determine which needed headers are available in the dataframe
        available_headers = [x for x in needed_headers if x in dataframe.columns]

        if available_headers != needed_headers:
            raise ValueError("Expected columns in the DataFrame: "+str(needed_headers)+". But found only these columns: "+str(available_headers))

        # Convert year to string. Convert month to string with length=2, filled with leading zeros if value < 10
        dataframe['Year'] = dataframe['Year'].apply(int).apply(str)
        dataframe['Month'] = dataframe['Month'].apply(int).apply(str).str.zfill(2)
        
        # Sort dataframe by Year and Month
        export_dataframe = dataframe.sort_values(['Year', 'Month'], ascending = [True, True]).copy()
        
        return export_dataframe

    def _prepare_data_frame(self, dataframe):
        """
        This function orchestrates other functions to transform a pandas DataFrame into a dictionary of scenarios.

        Parameters
        ----------
        dataframe         : pandas DataFrame
        
        Returns
        -------
        export_dictionary : dictionary with for each available scenario a list of 12 values and one value for the Year
        """
        # If the dataframe has more columns than relevant, only keep the relevant columns
        dataframe = self._data_frame_keep_only_relevant_columns(dataframe)
        
        # It is possible that the dataframe has more detailed lines (especially when removing non-relevant columns). Aggregate them on Year/Month-level
        dataframe = self._data_frame_aggregate(dataframe)
        
        # Convert year and month to strings and sort the dataframe on year and month
        dataframe = self._convert_year_month_to_string_dataframe(dataframe)
        
        # Determine the max-year and the year before the max-year. These will be the actual (AC) and previous year (PY)
        max_year        = dataframe['Year'].max()
        before_max_year = str(int(max_year)-1)

        # Split the dataframes in the actual and previous year
        df_ac = dataframe[dataframe['Year'] == max_year].copy()
        df_py = dataframe[dataframe['Year'] == before_max_year].copy()
        
        # Complete dataframe for missing month-values. Nothing worse than incomplete time-axis
        df_ac = self._data_frame_full_year(df_ac)
        df_py = self._data_frame_full_year(df_py)
        
        if 'PY' in df_ac.columns:
            if 'AC' in df_py.columns:
                if not (df_ac['PY'] == df_py['AC']).all():
                    raise ValueError(str(max_year)+"-DataFrame previous year does not match "+str(before_max_year)+ "-Dataframe", df_ac, df_py)
                # else:
                #    Everything is fine, go further
            # else:
            #    No actual values in previous year dataframe
        else:
            # No previous year values in actual dataframe
            if 'AC' in df_py.columns:
                # We can use the actual values in te previous year dataframe as previous year values in the actual dataframe
                df_ac['PY'] = df_py['AC'].copy()
        
        # Transform the DataFrame into a dictionary
        export_dictionary = df_ac.to_dict(orient='list')
        export_dictionary['Year'] = max_year
        if 'Month' in export_dictionary:
            del export_dictionary['Month']
        # Convert the values (that can be of type string) from the scenarios in integer or float values
        for scenario in ['PY', 'PL', 'AC', 'FC']:
            if scenario in export_dictionary.keys():
                valuelist = export_dictionary[scenario]
                export_dictionary[scenario] = string_to_value(valuelist)

        return export_dictionary
        

    def _convert_data_list_of_lists_to_dict(self, data_list):
        """
        Makes a dictionary out of a list of lists.
 
        Parameters
        ----------
        data_list          : data_list contains a list of lists.
        
        self variables
        --------------
        self.all_scenarios : all possible supported scenario's
        
        Returns
        -------
        checked_data_dict  : checked_data_dict contains a dictionary with the scenario's as a key and the detail values as a list
       """
        # Check if the data is not a list (ValueError), because we need a list (containing more lists)
        if not islist(data_list):
            raise ValueError(str(data_list)+" is not a list")
        
        # Headers will ultimately contain the needed headers of the 'CSV'-list-structure
        headers = None
        headerlength = 0
        
        # Data_dict will contain the dictionary of lists to return from this function
        data_dict  = dict()
        
        # We keep track of the year_month-combinations for completeness (all 12 month from a year) and for uniqueness (each combination occurs one times)
        year_month = list()
        
        # Process each element of the list (which should be a list by themself)
        for element_list in data_list:
            # Is the element_list containing data?
            if len(element_list) == 0:
                # skip the empty line
                continue
            
            # Check again if the element_list is not a list (ValueError), because we need a list at this level
            if not islist(element_list):
                raise ValueError("The element "+str(element_list)+" is not a list")
        
            if headers is None:
                # Headers has no headervalues right now, use this first line as headers
                # The element_list usable as header must contain Year and Month information or else we can not prepare the data for the charts later
                if "Year" not in element_list or "Month" not in element_list:
                    raise ValueError("Year and Month needs to be in the first line of the dataset"+str(element_list))
                headerline = [i for i in ["Year", "Month"]+self.all_scenarios if i in element_list]
                headers = list()
                for headerelement in headerline:
                    headers.append([headerelement, element_list.index(headerelement)])
                    data_dict[headerelement] = list()
                headerline   = element_list  # keep the original headerline for explanation of lines with other lenghts
                headerlength = len(headerline)
            else:
                # Headers has headervalues
                
                # For a correct dataset the element_list needs to contain exactly the same amount of elements than the headerline
                if len(element_list) != headerlength:
                    raise ValueError("Headerline "+str(headerline)+" is of length "+str(headerlength)+" and that's different in length than this line "+ \
                                     str(element_list)+" with a length of "+str(len(element_list)))
                                     
                year  = None
                month = None
                for headerelement, index in headers:
                    worklist = data_dict[headerelement]
                    element = element_list[index]
                    # If the element is still a string, we need to convert it to an integer of a float
                    if type(element) == type(''):
                        # element is still of type string
                        if '.' in element:
                            # Yes, a dot, so we convert to float
                            element=float(element)
                        else:
                            # No dot, so we convert to integer
                            element=int(element)
                    if headerelement in ('Year', 'Month'):
                        element = int(element)
                    worklist.append(element)
                    data_dict[headerelement] = worklist
                    if headerelement == "Year" : year = element
                    if headerelement == "Month": month = element
                year_month.append(str(year)+'.'+("0"+str(month))[-2:])

        # The list year_month needs to be of the same lenght than the set of this list to ensure all unique values
        if len(year_month) != len(set(year_month)):
            raise ValueError("Same year/month occurs more than once somewhere in this list:\n"+str(sorted(year_month)))

        checked_data_dict = self._check_data_dict(data_dict, year_month, headers)

        return checked_data_dict


    def _check_data_dict(self, data_dict, year_month, headers):
        """
        Checks the dictionary. Find out the most recent year (that will be the actual year).
        Also filters out the previous year and the actual year (if more data is provided).
        Sorts the values within the year from the first month to the last month.
        Check if the actual of the previous year is the same als the previous-year-column in the actual year (if both provided).
        If no previous year info provided in the actual year, but actual info provided in the previous year, it makes that the previous-year-data of the actual year.
        Finally make it the dictionary-form to use with the visual.
 
        parameters
        ----------
        data_dict          : a dictionary of lists of the needed elements

        year_month         : a list of year-month combinations

        headers            : a list of lists where you can find the header-elements and their position
        
        self variables
        --------------
        self.all_scenarios : all possible supported scenario's
        
        returns
        -------
        dataset            : a dictionary containing the dataset in the preferred format

        """
        # AC, PY and make headers simple
        actual_year    = max(data_dict["Year"])
        previous_year  = actual_year - 1
        headers_simple = list(list(zip(*headers))[0])  # Use of double list because the first element [0] of the inner list is a tuple!
        
        # Fill the combined list and remind where the year is in this combined list
        combinedlist = list()
        combinedlist.append(year_month)    # This is the first field. We use it for sorting later on 
        yearlistnumber = None
        for counter, element in enumerate(headers_simple):
            combinedlist.append(data_dict[element])
            if element == "Year": yearlistnumber=counter+1
        
        # Filter the lists based on year
        transposelist     = list(zip(*combinedlist))   # We need to transpose the list, so we can filter on a value in the inner list
        actualyear_list   = [x for x in transposelist if x[yearlistnumber]==actual_year]
        previousyear_list = [x for x in transposelist if x[yearlistnumber]==previous_year]
        
        # Sort the lists by the first field in the sublist (year_month)
        actualyear_list   = sorted(actualyear_list  , key = lambda x: x[0])
        previousyear_list = sorted(previousyear_list, key = lambda x: x[0])
        
        # Transpose back to combinedlists, one for actual year and one for previous year
        actualyear_list = list(zip(*actualyear_list))
        previousyear_list = list(zip(*previousyear_list))
        
        if 'PY' in headers_simple and 'AC' in headers_simple:
            # PY is provided, but PY is also the AC of the previous year. Check for consistency!!
            PY_index = headers_simple.index('PY') + 1   # Because year_month is at 0!!
            AC_index = headers_simple.index('AC') + 1   # Because year_month is at 0!!
            if len(previousyear_list) > 0:
                # Yes, there is information of previous year, now we need to check if the values are the same
                if actualyear_list[PY_index] != previousyear_list[AC_index]:
                    raise ValueError("PY in the actual year\n"+str(actualyear_list[PY_index])+" is not equal to the AC in the previous year\n"+str(previousyear_list[AC_index]))
        
        if 'PY' not in headers_simple and 'AC' in headers_simple:
            AC_index = headers_simple.index('AC') + 1   # Because year_month is at 0!!
            # PY is not provided, we can use the AC of the previous year
            if len(previousyear_list) > 0:
                # There is previous-year-data!
                if len(previousyear_list[AC_index]) == 12:
                    headers_simple.append('PY')
                    actualyear_list.append(previousyear_list[AC_index])

        # Make a dataset to use for the visuals        
        dataset = dict()
        for element, element_list in zip(headers_simple, actualyear_list[1:]):   # We start from the 2nd element in actualyear_list, because the first element is the combined year_month list.
            if element == 'Year':
                dataset[element] = max(element_list)   # min or average should also work, or even the first index [0]
            elif element in self.all_scenarios:
                dataset[element] = list(element_list)  # the element_list is technically a tuple and is now converted to a list
            # else, do nothing. If the element doesn't match Year or a scenario, ignore the data
        
        return dataset


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
        self._fill_main_ax_label()
        
        
    def _fill_main_ax_bar(self, scenario):
        """
        Plots the bars from the comparison scenario and the actual and the forecast scenario

        Parameters
        ----------
        scenario : the scenario of which the bars will be plotted

        Self variables
        --------------
        self.data          : is a dictionary of the detaildata

        self.barshift      : the barshift for the main part of the chart.

        self.barwidth      : a float with the width of the bars for measure of ratio

        self.colors        : a dictionary of colors needed for the consistent look of the charts

        self.linewidth_bar : the width of the lines from a bar

        self.hatch         : the pattern for hatched

        self.data_text     : a dictionary with the number of the matplotlib-ax-containers of the bar-data including the texts of the bars

        """
        # print(scenario+":", self.data[scenario])
        scenario_data = self.data[scenario]
        ax = self.ax["main"]
        if scenario[0] == 'P':
            #xvalue_temp     = [x for x in range(len(scenario_data)]
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


    def _fill_main_ax_label(self): 
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
                    barsign    = -1
                    if self.data_total['PY'] > self.data_total['PL']: linesign = -1
                    else: linesign = +1  
                    textsign   = -1
                    halignment = 'right'
                    xend       = 1    # We need a line to the end of the ax-comments if there are 2 scenario's for the PY-scenario
                    if self.data_total['PY'] < self.data_total['PL']: PY_valuetext_special = True
                else:
                    barsign    = +1
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
                ax.text(0-self.barwidth/2.5, self.data_total[scenario]*(1+(self.padding/250)), str(self.data_total[scenario]), horizontalalignment='right', verticalalignment='bottom', 
                            font=self.font, fontsize=self.fontsize, color=self.colors['text'])
            else:
                # The PL-column with text is small enough, that we can put the valuetext centered on top of the PY-column.
                format_string = formatstring(decimals=self.decimals_totals)
                ax.bar_label(ax.containers[-1], fmt=format_string, label_type='edge', padding=self.padding, font=self.font, fontsize=self.fontsize)
        
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
        self.ax            : Dictionary of axesobjects for the generated subplots

        self.padding       : Padding between the bars and the text

        self.font          : All text in a chart has the same font
        
        self.fontsize      : All text in a chart has the same height
        
        self.colors        : A dictionary with all color information

        self.barwidth      : A float with the width of the bars for measure of ratio
        
        self.linewidth_bar : The width of the lines from a bar

        self.data_total    : Total values for each scenario. Scenario is the key for the total value

        self.year          : Year of the data
        """
        
        ax = self.ax["sum"]
        bottom = 0 
        
        scenarios = self.filter_scenarios(scenario_list=['AC', 'FC'])
        format_string = formatstring(decimals=self.decimals_totals)

        for scenario in scenarios:
            # Determine the hatch
            hatch = None
            if scenario == 'FC': 
                hatch = self.hatch
            
            # Plot the (part of the stacked) bar (due to parameter bottom)
            ax.bar(0, self.data_total[scenario], color=self.colors[scenario][0], width=self.barwidth, linewidth=self.linewidth_bar, edgecolor=self.colors[scenario][1], bottom=bottom, label=scenario, hatch=hatch)

            # Inline legend (barwidth * 0.6 to be close to the bar, but not adjacent)
            ax.text(0+self.barwidth*0.6, bottom + self.data_total[scenario]/2, scenario, horizontalalignment='left', font=self.font, fontsize=self.fontsize, color=self.colors['text'], verticalalignment='center')
               
            # Only stacked bar values inside if more than 1 scenario
            if len(scenarios)>1:
               
                # Two different kinds of adding text in the bars
                if scenario == 'FC':
                    # Round the value with the desired number of decimals. With numerator=1 and denominator=1 you get the same value.
                    value = optimize_data(data=self.data_total[scenario], numerator=1, denominator=1, decimals=self.decimals_totals)
                    
                    # use text function because the use of backgroundcolor
                    #### I am searching to make the backgroundcolor of white a bit transparant, so we can see the hatching through it.
                    ax.text(0, bottom + self.data_total[scenario]/2, str(value), horizontalalignment='center', verticalalignment='center', 
                            font=self.font, fontsize=self.fontsize, color=self.colors[scenario][2], backgroundcolor=self.colors[scenario][3])
                else:
                    # use standard label function
                    ax.bar_label(ax.containers[-1], fmt=format_string, label_type='center', font=self.font, fontsize=self.fontsize, color=self.colors[scenario][2])    

            bottom = bottom + self.data_total[scenario]
        # add top label
        ax.bar_label(ax.containers[-1], fmt=format_string, label_type='edge', padding=self.padding, font=self.font, fontsize=self.fontsize, color=self.colors['text']) 
        
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
        label_value_list = self.convert_to_delta_string(self.delta_value[delta_name])
        
        if len(label_value_list) > 0:
            ax.bar_label(ax.containers[self.data_text['delta']], labels=label_value_list, fmt= '%0i', label_type='edge', padding = self.padding, font=self.font, fontsize=self.fontsize, zorder=10)


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
            value = optimize_data(data=(yvaluesum-yvalue_scenario), numerator=1, denominator=1, decimals=self.decimals_totals)
            ax.text(xbegin + textadjustment, (yvaluesum+yvalue_scenario)/2, self.convert_to_delta_string(value), horizontalalignment='left', verticalalignment='center', 
                                 font=self.font, fontsize=self.fontsize, color=self.colors['text'],zorder=10)

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