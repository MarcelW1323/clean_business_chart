"""Main module."""

# Import modules
import matplotlib.pyplot as plt                   # for most graphics
from matplotlib.patches import ConnectionPatch    # for lines between subplots (used in the function "plot_line_accross_axes")
from clean_business_chart.general_functions    import islist, isdictionary, isinteger, isstring, isfloat, isboolean, isdataframe, filter_lists


class GeneralChart:
    """
    The class GeneralChart is for general variables and general functions related to these variables. This provides unity.
    
    Don't call this class from outside the module.
    """
    
    # Variables filled in dedicated functions, public variables for all instances
    colors            = dict()   # Collection of colors. IBCS advices green for good variance, red for bad variance and blue for highlight. The rest is monochrome.
    month             = dict()   # Collection of monthsnames or abbreviations
    barwidths         = dict()   # Collection of default barwidths to use in charts
    
    # Variables with direct value assignment, public variables for all instances
    fontsize          = 12       # All text in a chart has the same height
    fontsize_small    = 10       # Small fontsize for footnotes
    footnote_fontsize = {'small': fontsize_small, 'normal':fontsize}  # Normal is default
    font              = 'Arial'  # All text in a chart has the same font. Default font of matplotlib is 'DejaVu Sans'.
    padding           = 3        # Padding between the bars and the text
    
    delta_sign        = 'Δ'      # Delta sign to use for titles of deltacharts
    not_available     = 'n.a.'   # Not available
    barshift_value    = 0.125    # The portion a grouped bar chart will be out of the middle
    barshift          = 0        # The barshift for the main part of the chart. This value will be overruled with barshift_value if there are other relevant scenario's available
    barshift_leftside = 0        # The barshift for the left side part of the chart. This value will be overruled with barshift_value if there are relevant scenario's available
    hatch_pattern     = '//////' # The pattern for hatched   #### I am searching to make the individual hatchlines a bit thicker
    linewidth_zero    = 2        # The width of the zerolines
    linewidth_bar     = 2        # The width of the lines from a bar
    linewidth_line_n  = 2        # The normal width of the lines
    linewidth_line_s  = 1        # The small width of the lines
    linewidth_delta   = 10       # The width of the delta-lines with the good or bad colors
    outside_factor    = 1 + (4*linewidth_bar/100)   # Factor to use to keep lines as much as possible outside of the bars

    # Changing font back to default font.
    font              = 'DejaVu Sans'  # All text in a chart has the same font. Default font of matplotlib is 'DejaVu Sans'.
    # Trying to make the mathematical font the same as the normal font. Both attempts below doesn't work according my tests.
    # from matplotlib import rc
    # rc('font', family=font)
    # or
    # from matplotlib import rcParams
    # rcParams['mathtext.rm'] = font


    def __init__(self):
        """
        __init__ initializes this class automatically then called. For inherited classes, add super().__init__() in the initialization of that class 
        """
        self._fill_default_colors()
        self._fill_month()
        self._fill_default_barwidths()
        self._other_variables()
    
    def _other_variables(self):
        """
        Declaration of variables who are private for each instance. This don't need to be centralized, but I think this makes it a valuable summary
        """
        # Scenarios
        self.all_scenarios    = ['PY', 'PL', 'AC', 'FC']  # Previous Year, PLan, ACtual, ForeCast (in order of time)
        self.all_scenarios_translate = {'PY':'PY', 'PL':'PL', 'AC':'AC', 'FC':'FC'}  # Translate standard scenarios
        self.data_scenarios   = list()      # Every class needs to fill this variable to indicate which scenarios are in the data

        # Date columns
        self.date_column      = ['Date']    # Date only as supported headercolumn
        self.year_column      = ['Year']    # Year only as supported headercolumn
        self.month_column     = ['Month']   # Month only as supported headercolumn
        self.all_date_columns = ['Date', 'Year', 'Month'] # Date, year and month are supported headercolumns

        # Data storage of input variables and totalisation
        self.data             = dict()      # Detail values for each scenario. Scenario is the key for the list of detail values
        self.data_total       = dict()      # Total values for each scenario. Scenario is the key for the total value
        self.use_PL_as_FC     = True        # Default value for a parameter which causes the use of Plan-information when no Forecast information is available (PL-FC=0 for these cases while calculating the delta PL-FC)

        # Storage of delta information
        self.delta_value      = dict()      # Delta values. Delta_name is the key for the list of delta values
        self.delta_percent    = dict()      # Delta relative values. Delta_name is the key for the list of delta relative values
        self.delta_scenario   = dict()      # Delta scenarios. Delta_name is the key for the list of delta scenario
        self.main_months      = dict()      # Month-names with delta scenario information. Delta_name is the key for the list of month-names
        self.delta_base_value = dict()      # Base_values for the delta charts. Delta_name is the key for the value
        self.delta_digits     = 1           # Defaultvalue for number of digits when rounding delta values

        # Storage of figure, axes and order of axes
        self.figure           = None        # Figure-object, needed for cross subplot lines
        self.ax               = dict()      # Dictionary of matplotlib-subplot-axes
                                            # self.ax["left"] contains axes-object for Previous Year and/or Planned information subplot
                                            #### self.ax["PY"]   contains axes-object for Previous Year subplot
                                            #### self.ax["PL"]   contains axes-object for Planned information subplot
                                            # self.ax["main"] contains axes-object for main subplot for actual, forecast and deltacharts
                                            # self.ax["sum"]  contains axes-object for sum subplot for actual-sum, forecast-sum and more
                                            # self.ax["average"] contains axes-object for average subplot
                                            # self.ax["comment"] contains axes-object for comment subplot
        self.ax_order         = ["left", "PY", "PL", "main", "sum", "average", "comment"]  #### Order of the subplots. Not all subplots are in every chart available
        
        self.data_text        = dict()      # A dictionary with the number of the matplotllib-ax-containers of the bar-data including the texts of the bars
        self.barwidth         = 0           # A float with the width of the bars for measure or ratio
        

    def _fill_default_colors(self):
        """
        Assigns the default IBCS-inspired values into the dictionary variable colors.
        If there is some need to use other colors, it can be implemented in a central way.
        
        Self variables
        --------------
        self.colors : a dictionary of colors needed for the consistent look of the charts
        """
        self.colors['text']           = '#000000'   # Text is in black (exception: scalingband -> highlight)
        self.colors['textbackground'] = '#FFFFFF'   # Background of text is in white
        self.colors['AC']             = ('#404040', '#404040', '#FFFFFF') #index 0= color, 1= bordercolor, 2=textcolor stacked bar
        self.colors['PY']             = ('#B0B0B0', '#B0B0B0')
        self.colors['PL']             = ('#FFFFFF', '#404040')
        self.colors['FC']             = ('#FFFFFF', '#404040', '#000000', '#FFFFFF') #index 0= color, 1= bordercolor, 2=textcolor stacked bar, 3=background color text stacked bar
        self.colors['line']           = '#C0C0C0'
        self.colors['barborder']      = self.colors['AC']
        self.colors['good']           = 'lightgreen'
        self.colors['bad']            = 'red'
        self.colors['highlight']      = '#0064FF'
        self.colors['endpoint']       = ('#FFFFFF', '#000000')  # index 0= outercircle color, 1= innercirclecolor
        self.colors['zeroline']       = '#000000'
        self.colors['totalline']      = '#000000'

        
    def _fill_month(self, language="EN"):
        """
        _fill_month is designed to add multilingual support for description of months in 1 or 3 character space.
        Months are filled with 1 character (self.month['1']) or with 3 characters (self.month['3']).
    
        Parameters
        ----------
        language : Language of the month descriptions you like to have. If the language isn't supported by now, you'll receive English descriptions
             (Default value = 'EN')

        Self variables
        --------------
        self.month : a dictionary of monthnames or abbreviations
        """
        # Default language is English, in short "EN". Just as used by wikipedia (en.wikipedia.org)
        self.month["1"] = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]
        self.month["3"] = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        # The NL-language means "Dutch". Abbreviation just as used by wikipedia (nl.wikipedia.org)
        if language=="NL":
            self.month["1"] = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]
            self.month["3"] = ["Jan", "Feb", "Maa", "Apr", "Mei", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dec"]

        
    def _fill_default_barwidths(self):
        """
        Assigns the default barwidth of charts into the dictionary variable barwidths 

        Self variables
        --------------
        self.barwidths : a dictionary of barwidths for measure and ratio
        """
        # Commented out because of the linewidth, see implementation below.
        self.barwidths["measure"] = 0.65      # IBCS advices the width of 2/3 of a bar for measures
        self.barwidths["ratio"]   = 0.35      # IBCS advices the width of 1/3 of a bar for ratios
        
        #### IMPROVEMENT: I like to make the linewidth inside of the bars, but now the linewidth is outside of the bars
        # So the bars need to be smaller to have the complete width about 2/3 for measures and 1/3 for ratios
        # The values below are approx-values that look OK, but are not tested in every environment.
        # It would be nice if this could be improved, where the linewidth would be part of the formula.
        #self.barwidths["measure"] = 0.60      # IBCS advices the width of 2/3 of a bar for measures, now there is room for the linewidth
        #self.barwidths["ratio"]   = 0.30      # IBCS advices the width of 1/3 of a bar for ratios, now there is room for the linewidth

        return


    def get_barwidth(self, measure):
        """
        Chooses the right barwidth based whether it is a measure (about 2/3 in width) or not a measure (about 1/3 in width)

        Parameters
        ----------
        measure : Indication whether the data is a measure (True) or not (False)
                  True:  Data is a measure
                  False: Data is not a measure
            
        Self variables
        --------------
        self.barwidths : a dictionary of barwidths for measure and ratio

        self.barwidth  : a float with the width of the bars for measure of ratio

        Returns
        -------
        self.barwidth contains a float with the width of the bars
        """
        # Check for type of parameter measure
        if not isboolean(measure):
            raise TypeError("Wrong value for boolean 'measure':"+str(measure)+". Please provide True or False.")
        
        # Assign value to self.barwidth
        value = ["ratio", "measure"][measure]     # When False, value will be 'ratio'. When True, value will be 'measure'
        self.barwidth = self.barwidths[value]
        
        return

 
    def filter_scenarios(self, scenario_list):
        """
        Filters the scenario_list against a complete list of avaliable scenarios and returns only those scenario who are in both lists, 
        in the same order as the scenario list.

        Parameters
        ----------
        scenario_list          : list of scenarios you like to validate against the complete scenario list
        
        Self variables
        --------------
        self.data_scenarios    : list of all scenarios who are available

        Returns
        -------
        a list of scenario's who are in both lists in the same order as the scenario list
        """
        # The order of the list is important. So implementation not with intersection, but a list comprehension, implemented in function filter_lists
        return filter_lists(list1=scenario_list, list2=self.data_scenarios)


    def calculate_delta(self, base_scenario, compare_scenario_list, delta_name, month_list=None, add_scenario_to_month=False, round_decimals_percentages=1):
        """
        Calculates the delta between the base_scenario and the compare_scenario_list.
        It is possible to calculate the delta between a planned scenario and the actual and forecast scenario's, but also between a previous year and the actual and forecast scenario's

        Parameters
        ----------
        base_scenario              : one scenario, mostly "PL" or "PY"
        
        compare_scenario_list      : a list of one or two scenario's (mostly 'AC' and/or 'FC')
        
        delta_name                 : identifier to recognize the calculated delta's
                
        month_list                 : a list of descriptions of the months
             (Default value = None)
        add_scenario_to_month      : would you like to add the scenario under the name of the month if the scenario changes. False: do not add scenario to month name. True: yes, add scenario to month name
             (Default value = False)
        round_decimals_percentages : number of decimals you want to show in the delta percentage values


        Self variables
        --------------
        self.data                  : a dictionary containing all available scenario's with their detail list
        
        self.delta_scenario        : a dictionary with lists of scenario's of the delta values so we can made the translation to the visualisation
        
        self.delta_value           : a dictionary with lists of delta values
        
        self.delta_percent         : a dictionary with lists of delta percentages
        
        self.not_available         : a variable with a string value for 'not available'

        self.month                 : a dictionary containing lists with month names/abbreviations

        self.main_months           : a list of months with scenario-change-information  
        """
        
        # Initialize work variables
        delta_value_list    = [0] * len(self.data[base_scenario])      # Make a list with only zeros with the size of base_set
        delta_percent_list  = delta_value_list[:]                      # Make a copy of the same list with only zeros
        delta_scenario_list = [''] * len(self.data[base_scenario])     # Make a list with only empty scenarios
        scenario_text = None
        
        work_base  = self.data[base_scenario][:]                       # Make an independant copy because values can be modified
        
        # Get the default month_list if not given by parameter
        if month_list is None:
            work_month = self.month['1'][:]                            # Make an independant copy because values can be modified
        else: 
            work_month = month_list[:]                                 # Make an independant copy because values can be modified
        

        # A delta is the difference of the compare_scenario value and the base_scenario value. We need to record this difference and the scenario this difference belongs to.
        # If the scenario alters, we add this information to the month-name if the related parameter add_scenario_to_month is True
        # IBCS advices to display 'n.a.' (not available) if the relative variance can not be interpreted. This is often the case when you compare a positive value to a negative reference value (in the denominator)        
        for scenario in self.filter_scenarios(scenario_list=compare_scenario_list):
            for number, compare_element in enumerate(self.data[scenario]):
                if compare_element is not None:
                    # Yes, there is an element to compare with                    
                    if add_scenario_to_month:
                        # Yes, add the scenario to month
                        if scenario_text is None:
                            work_month[number] += '\n'+scenario
                            scenario_text       = scenario
                        elif scenario_text != scenario:
                            work_month[number] += '\n'+scenario
                            scenario_text       = scenario
                    
                    # Calculate the absolute delta value and add this to the list
                    delta_value_list[number]    = compare_element - work_base[number]                                              # Absolute value
                    
                    # Calculate relative value, while take care of division by zero and not-available relative values
                    if work_base[number] != 0:
                        delta_percent_list[number]  = round((delta_value_list[number] / work_base[number]) * 100, round_decimals_percentages)  # Relative value
                        if work_base[number] < 0 and delta_value_list[number] > 0:  # This combination can not be interpreted (often)
                            delta_percent_list[number] = self.not_available
                    else:   # No division by zero!
                        delta_percent_list[number] = self.not_available

                    # Mark that the work_base-value has been used and note the used scenario
                    work_base[number]           = 0
                    delta_scenario_list[number] = scenario

        # Make the delta calculation available
        self.delta_scenario[delta_name] = [x for x in delta_scenario_list if x != '']                  # Shorten the list to leave only those scenario values who got an assignment
        self.delta_value[delta_name]    = delta_value_list[0:len(self.delta_scenario[delta_name])]     # Shorten the list of delta values to the same length as the list of scenario's above
        self.delta_percent[delta_name]  = delta_percent_list[0:len(self.delta_scenario[delta_name])]   # Shorten the list of delta values to the same length as the list of scenario's above
        self.main_months[delta_name]    = work_month[:]                                                # Keep the list of modified month descriptions


    def good_or_bad_color(self, differencevalue):
        """Helperfunction to determine which color you need to display.

        Parameters
        ----------
        differencevalue       : the difference or variance between two values. It can contain a positive number, zero or a negative number.

        Self variables
        --------------
        self.colors           : a dictionary of colors including the colors for good and bad in the view of the business.

        self.positive_is_good : When true, positive differencevalues get a goodcolor and negative differencevalues get a badcolor. When false this is vice-versa.

        Returns
        -------
        color : the color needed to use. This can be a goodcolor or a badcolor depending on the differencevalue and whether positive is good or not.
        """
        # True has a value of 1, False has a value of 0. We use this value to index the list of the two colors.
        if differencevalue >= 0:
            # if positive_is_good is true, color will get the goodcolor and when false, color will get the badcolor
            color = [self.colors['bad'], self.colors['good']][self.positive_is_good]
        else:  # if differencevalue < 0:
            # if positive_is_good is true, color will get the badcolor and when false, color will get the goodcolor
            color = [self.colors['good'], self.colors['bad']][self.positive_is_good]
        return color


    def prepare_delta_bar(self, base_value, delta_name, waterfall=True):
        """
        Prepares a delta_bar, based on a calculated delta

        Parameters
        ----------
        base_value : the starting height of the delta bar

        delta_name : the name of the delta to address all related information

        waterfall : do we need to prepare a delta bar for a waterfall or just a simple delta bar

        Self variables
        --------------
        self.barshift       : information about how much we need to shift the bar to fit right on top of the other charts

        self.barwidth       : the width each bar element should be

        self.colors         : a dictionary with all color information

        self.delta_value    : a dictionary with one or more lists with delta values

        self.delta_scenario : a dictionary with one or more lists with scenario values

        self.hatch          : in case of forecast information, what would the hatch value be



        Returns
        -------
        delta_info: a dictionary of lists with all the information you need to plot a delta bar or an empty dictionary when there is no data
        """
        bottom = base_value                       # make a copy of base_value to bottom, because the value of bottom can be changed
        delta_info = dict()                       # dictionary for the complete delta bar preparation

        delta_info['xvalue']         = list()     # list of x-coordinates of the delta bars                 # noqa: E221
        delta_info['yvalue']         = list()     # list of y-coordinates of the height of the delta bars   # noqa: E221
        delta_info['bottom']         = list()     # list of y-coordinates of the bottom ot the delta bars   # noqa: E221
        delta_info['color']          = list()     # list of colors of the delta bars                        # noqa: E221
        delta_info['hatch']          = list()     # list of hatch-values (for forecast) or None (for actual) for the delta bars      # noqa: E221
        delta_info['edgecolor']      = list()     # list of edgecolors of the delta bars                    # noqa: E221
        delta_info['scenario_label'] = list()     # list of scenario labels AC or FC                        # noqa: E221
        delta_info['connect']        = list()     # list of y-coordinates of connection lines between the bars to make a waterfall   # noqa: E221

        for xvalue, (delta_element, scenario_element) in \
            enumerate(zip(self.delta_value[delta_name], 
                          self.delta_scenario[delta_name])):
            color_to_use = \
                self.good_or_bad_color(differencevalue=delta_element)

            delta_info['xvalue'] += [xvalue + self.barshift * self.barwidth]
            delta_info['yvalue'] += [delta_element]
            delta_info['bottom'] += [bottom]
            if scenario_element == 'FC':
                delta_info['color'] += [self.colors["FC"][0]]
                delta_info['hatch'] += [self.hatch]
            else:
                delta_info['color'] += [color_to_use]
                delta_info['hatch'] += [None]
            delta_info['edgecolor'] += [color_to_use]
            delta_info['scenario_label'] += [scenario_element]
            if waterfall:
                bottom += delta_element
            delta_info['connect'] += [bottom]
            
        # Check content of delta_info
        count_length_of_lists = 0
        for key in delta_info.keys():
            count_length_of_lists += len(delta_info[key])
        # Count_length_of_lists ==0 -> there is no info. delta_info will contain an empty dictionary.
        if count_length_of_lists == 0:
            delta_info = dict()

        return delta_info