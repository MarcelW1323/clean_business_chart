"""General functions."""

# Import modules
import matplotlib.pyplot as plt                   # for most graphics
from matplotlib.patches import ConnectionPatch    # for lines between subplots (used in the function "plot_line_accross_axes")
import pandas as pd                               # for easy pandas support
from clean_business_chart.exceptions import *     # for custom errors/exceptions


#####################    
# GENERAL FUNCTIONS #
#####################

def islist(inputvariable):
    """Returns whether the inputvariable is a list (True) or not (False)"""
    return isinstance(inputvariable, list)

def istuple(inputvariable):
    """Returns whether the inputvariable is a tuple (True) or not (False)"""
    return isinstance(inputvariable, tuple)

def isdictionary(inputvariable):
    """Returns whether the inputvariable is a dictionary (True) or not (False)"""
    return isinstance(inputvariable, dict)

def isinteger(inputvariable):
    """Returns whether the inputvariable is an integer (True) or not (False)"""
    return isinstance(inputvariable, int)

def isstring(inputvariable):
    """Returns whether the inputvariable is a string (True) or not (False)"""
    return isinstance(inputvariable, str)

def isfloat(inputvariable):
    """Returns whether the inputvariable is a float (True) or not (False)"""
    return isinstance(inputvariable, float)

def isnumber(inputvariable):
    """Returns whether the inputvariable is an integer or a float (True) or not (False)"""
    return isinstance(inputvariable, int) or isinstance(inputvariable, float)

def isboolean(inputvariable):
    """Returns whether the inputvariable is a boolean (True) or not (False)"""
    return isinstance(inputvariable, bool)

def isdataframe(inputvariable):
    """Returns whether the inputvariable is a pandas DataFrame (True) or not (False)"""
    return isinstance(inputvariable, pd.DataFrame)

def isaxes(inputvariable):
    """Returns whether the inputvariable is a matplotlib Axes (True) or not (False)"""
    return isinstance(inputvariable, plt.Axes)

def isfigure(inputvariable):
    """Returns whether the inputvariable is a matplotlib Figure (True) or not (False)"""
    return isinstance(inputvariable, plt.Figure)

def error_not_islist(inputvariable, name_inputvariable_in_text=None):
    """Returns a TypeError when the inputvariable is not a list"""
    if not islist(inputvariable):
        # inputvariable is not a list, construct message and generate a TypeError
        if name_inputvariable_in_text is not None:
            # Yes, extra information is given
            message = 'Variable "'+str(name_inputvariable_in_text)+'" is not of type list, but of type '+str(type(inputvariable))
        else:
            # No extra information is given, use this unified message
            message = 'Variable is not of type list, but of type '+str(type(inputvariable))
        raise TypeListError(message)
    # else:
        # inputvariable is a list, do return to caller
    return

def error_not_istuple(inputvariable, name_inputvariable_in_text=None):
    """Returns a TypeError when the inputvariable is not a tuple"""
    if not istuple(inputvariable):
        # inputvariable is not a tuple, construct message and generate a TypeError
        if name_inputvariable_in_text is not None:
            # Yes, extra information is given
            message = 'Variable "'+str(name_inputvariable_in_text)+'" is not of type tuple, but of type '+str(type(inputvariable))
        else:
            # No extra information is given, use this unified message
            message = 'Variable is not of type tuple, but of type '+str(type(inputvariable))
        raise TypeTupleError(message)
    # else:
        # inputvariable is a tuple, do return to caller
    return

def error_not_isdictionary(inputvariable, name_inputvariable_in_text=None):
    """Returns a TypeError when the inputvariable is not a dictionary"""
    if not isdictionary(inputvariable):
        # inputvariable is not a dictionary, construct message and generate a TypeError
        if name_inputvariable_in_text is not None:
            # Yes, extra information is given
            message = 'Variable "'+str(name_inputvariable_in_text)+'" is not of type dictionary, but of type '+str(type(inputvariable))
        else:
            # No extra information is given, use this unified message
            message = 'Variable is not of type dictionary, but of type '+str(type(inputvariable))
        raise TypeDictionaryError(message)
    # else:
        # inputvariable is a dictionary, do return to caller
    return

def error_not_isinteger(inputvariable, name_inputvariable_in_text=None):
    """Returns a TypeError when the inputvariable is not an integer"""
    if not isinteger(inputvariable):
        # inputvariable is not an integer, construct message and generate a TypeError
        if name_inputvariable_in_text is not None:
            # Yes, extra information is given
            message = 'Variable "'+str(name_inputvariable_in_text)+'" is not of type integer, but of type '+str(type(inputvariable))
        else:
            # No extra information is given, use this unified message
            message = 'Variable is not of type integer, but of type '+str(type(inputvariable))
        raise TypeIntegerError(message)
    # else:
        # inputvariable is an integer, do return to caller
    return

def error_not_isnumber(inputvariable, name_inputvariable_in_text=None):
    """Returns a TypeError when the inputvariable is not an integer and not a float"""
    if not isnumber(inputvariable):
        # inputvariable is not an integer and not a float, construct message and generate a TypeError
        if name_inputvariable_in_text is not None:
            # Yes, extra information is given
            message = 'Variable "'+str(name_inputvariable_in_text)+'" is not of type integer and not of type float, but of type '+str(type(inputvariable))
        else:
            # No extra information is given, use this unified message
            message = 'Variable is not of type integer and not of type float, but of type '+str(type(inputvariable))
        raise TypeNumberError(message)
    # else:
        # inputvariable is an integer or a float, do return to caller
    return

def error_not_isstring(inputvariable, name_inputvariable_in_text=None):
    """Returns a TypeError when the inputvariable is not a string"""
    if not isstring(inputvariable):
        # inputvariable is not a string, construct message and generate a TypeError
        if name_inputvariable_in_text is not None:
            # Yes, extra information is given
            message = 'Variable "'+str(name_inputvariable_in_text)+'" is not of type string, but of type '+str(type(inputvariable))
        else:
            # No extra information is given, use this unified message
            message = 'Variable is not of type string, but of type '+str(type(inputvariable))
        raise TypeStringError(message)
    # else:
        # inputvariable is a string, do return to caller
    return

def error_not_isboolean(inputvariable, name_inputvariable_in_text=None):
    """Returns a TypeError when the inputvariable is not a boolean"""
    if not isboolean(inputvariable):
        # inputvariable is not a boolean, construct message and generate a TypeError
        if name_inputvariable_in_text is not None:
            # Yes, extra information is given
            message = 'Variable "'+str(name_inputvariable_in_text)+'" is not of type boolean, but of type '+str(type(inputvariable))
        else:
            # No extra information is given, use this unified message
            message = 'Variable is not of type boolean, but of type '+str(type(inputvariable))
        raise TypeBooleanError(message)
    # else:
        # inputvariable is a boolean, do return to caller
    return

def error_not_isdataframe(inputvariable, name_inputvariable_in_text=None):
    """Returns a TypeError when the inputvariable is not a pandas DataFrame"""
    if not isdataframe(inputvariable):
        # inputvariable is not a pandas DataFrame, construct message and generate a TypeError
        if name_inputvariable_in_text is not None:
            # Yes, extra information is given
            message = 'Variable "'+str(name_inputvariable_in_text)+'" is not of type dataframe, but of type '+str(type(inputvariable))
        else:
            # No extra information is given, use this unified message
            message = 'Variable is not of type dataframe, but of type '+str(type(inputvariable))
        raise TypeDataFrameError(message)
    # else:
        # inputvariable is a pandas DataFrame, do return to caller
    return

def error_not_isaxes(inputvariable, name_inputvariable_in_text=None):
    """Returns a TypeError when the inputvariable is not a matplotlib Axes-object"""
    if not isaxes(inputvariable):
        # inputvariable is not a matplotlib Axes, construct message and generate a TypeError
        if name_inputvariable_in_text is not None:
            # Yes, extra information is given
            message = 'Variable "'+str(name_inputvariable_in_text)+'" is not of type Axes, but of type '+str(type(inputvariable))
        else:
            # No extra information is given, use this unified message
            message = 'Variable is not of type Axes, but of type '+str(type(inputvariable))
        raise TypeAxesError(message)
    # else:
        # inputvariable is a matplotlib Axes, do return to caller
    return

def error_not_isfigure(inputvariable, name_inputvariable_in_text=None):
    """Returns a TypeError when the inputvariable is not a matplotlib Figure-object"""
    if not isfigure(inputvariable):
        # inputvariable is not a matplotlib Figure, construct message and generate a TypeError
        if name_inputvariable_in_text is not None:
            # Yes, extra information is given
            message = 'Variable "'+str(name_inputvariable_in_text)+'" is not of type Figure, but of type '+str(type(inputvariable))
        else:
            # No extra information is given, use this unified message
            message = 'Variable is not of type Figure, but of type '+str(type(inputvariable))
        raise TypeFigureError(message)
    # else:
        # inputvariable is a matplotlib Figure, do return to caller
    return


def convert_to_native_python_type(value):
    """
    Converts a pandas/numpy integer or float variable to their native python type.

    Parameters
    ----------
    value : value to convert to a native python type.

    Returns
    -------
    export_value: a native python integer or float
    """
    # Check if the value is already a native integer or float
    if isinteger(value) or isfloat(value):
        export_value = value
        return export_value

    # Value is not a native python integer or float
    try:
        # We try to get the native format out of a pandas/numpy variable. The .item() is to get standard Python types back instead of numpy-types.
        export_value = value.item()
        if not isinteger(export_value) and not isfloat(export_value):
            # No, export_value is still not a native python integer or float
            raise ValueError("We like to go further with the except-clause")
        # else:
            # Yes, export_value is a native python integer or float

    except:
        # Check if it is a pandas/numpy variable
        if 'numpy' in str(type(value)):
            # Yes, it is a pandas/numpy variable
            if 'float' in str(type(value)):
                # The text 'float' is in the type information
                export_value = float(value)
            elif 'int' in str(type(value)):
                # The text 'int' is in the type information
                export_value = int(value)
        # else:
            # No, it is not a pandas/numpy variable

        # Check the type of export_value
        if not isinteger(export_value) and not isfloat(export_value):
            # No, export_value is still not a native python integer or float. We unconditionally convert it to a float.
            export_value = float(value)

    return export_value


def plot_line_accross_axes(fig, axbegin, xbegin, ybegin, axend, xend, yend, linecolor='black', arrowstyle='-', linewidth=1, endpoints=False, endpointcolor=None):
    """
    plot_line_accross_axes is needed when you want to draw a line over the borders of one subplot. Optionally the line has two endpoints to mark the beginning and end of the line

    Parameters
    ----------
    fig           : figure-object that contains all the axes
        
    axbegin       : ax-object where the line starts from
        
    xbegin        : x-coordinate of the point (xbegin, ybegin) where the line starts
        
    ybegin        : y-coordinate of the point (xbegin, ybegin) where the line starts
        
    axend         : ax-object where the line finishes
        
    xend          : x-coordinate of the point (xend, yend) where the line ends
        
    yend          : y-coordinate of the point (xend, yend) where the line ends
        
    linecolor     : color of the line
         (Default value = 'black')
    arrowstyle    : style of the arrow of the line
         (Default value = '-')
    linewidth     : width of the line
         (Default value = 1)
    endpoints     : toggle if you want to see endpoints (True) or no endpoints (False). An endpoint is a small filled outercircle in a given color (mostly white) with an even smaller filled innercircle in a given color (black)
         (Default value = False, no endpoints)
    endpointcolor : a tuple of list containing the color of the outercircle (at index 0) and the color of the innercircle (at index 1). The default value of None triggers a white outercircle and a black innercircle.
         (Default value = None)

    Returns
    -------
    None: This function has no real returnvalue. A line is added in the figure-object and optionally two endpoints are added on the end of this line on the related axes-object
    """
    
    # Make the line on the figure-object accross the axes
    line = ConnectionPatch(
            xyA = (xbegin, ybegin), coordsA = axbegin.transData,          # Starting point of the line
            xyB = (xend,   yend),   coordsB = axend.transData,            # Endpoint of the line
            arrowstyle=arrowstyle, linewidth=linewidth, color=linecolor)  # Basic line-properties
    fig.add_artist(line)                                                  # Line added to the figure-object
    
    # Check if enpoints are wanted
    if endpoints:
        # Yes, endpoints are wanted
        plot_endpoint(ax=axbegin, x=xbegin, y=ybegin, endpointcolor=endpointcolor, markersize_outercircle=7, markersize_innercircle=3)
        plot_endpoint(ax=axend,   x=xend,   y=yend,   endpointcolor=endpointcolor, markersize_outercircle=7, markersize_innercircle=3)
        

def plot_line_within_ax(ax, xbegin, ybegin, xend, yend, linecolor='black', arrowstyle='-', linewidth=1, endpoints=False, endpointcolor=None, zorder=None):
    """
    plot_line_within_axes is needed when you want to draw a line within the borders of one subplot. Optionally the line has two endpoints to mark the beginning and end of the line

    Parameters
    ----------
    ax            : ax-object where the line will be drawn
        
    xbegin        : x-coordinate of the point (xbegin, ybegin) where the line starts
        
    ybegin        : y-coordinate of the point (xbegin, ybegin) where the line starts
        
    xend          : x-coordinate of the point (xend, yend) where the line ends
        
    yend          : y-coordinate of the point (xend, yend) where the line ends
        
    linecolor     : color of the line
         (Default value = 'black')
    arrowstyle    : style of the arrow of the line
         (Default value = '-')
    linewidth     : width of the line
         (Default value = 1)
    endpoints     : toggle if you want to see endpoints (True) or no endpoints (False). An endpoint is a small filled outercircle in a given color (mostly white) with an even smaller filled innercircle in a given color (black)
         (Default value = False, no endpoints)
    endpointcolor : a tuple of list containing the color of the outercircle (at index 0) and the color of the innercircle (at index 1). The default value of None triggers a white outercircle and a black innercircle.
         (Default value = None)

    Returns
    -------
    None: This function has no real returnvalue. A line is added in the figure-object and optionally two endpoints are added on the end of this line on the related axes-object
    """
    if zorder is None:
        # No, don't use zorder. That is different from zorder=0
        ax.plot([xbegin, xend], [ybegin, yend], color=linecolor, linewidth=linewidth, solid_capstyle='butt')
        # Without solid_capstyle='butt' the lines increase in length because of increasing linewidth
    else:
        if isinteger(zorder) or isfloat(zorder):
            # Yes, use zorder
            ax.plot([xbegin, xend], [ybegin, yend], color=linecolor, linewidth=linewidth, solid_capstyle='butt', zorder=zorder)
            # Without solid_capstyle='butt' the lines increase in length because of increasing linewidth
        else:
            # Zorder is of wrong type
            raise TypeError("zorder can be integer or float. "+str(zorder)+" is now of type "+str(type(zorder))+".")
    
    # Check if enpoints are wanted
    if endpoints:
        # Yes, endpoints are wanted
        plot_endpoint(ax=ax, x=xbegin, y=ybegin, endpointcolor=endpointcolor, markersize_outercircle=7, markersize_innercircle=3)
        plot_endpoint(ax=ax, x=xend,   y=yend,   endpointcolor=endpointcolor, markersize_outercircle=7, markersize_innercircle=3)


def plot_endpoint(ax, x, y, endpointcolor=None, markersize_outercircle=7, markersize_innercircle=3):
    """
    plot_endpoint draws an outercircle at the specified coordinate. Then a smaller innercircle is drawn with a (preferably) contrast color

    Parameters
    ----------
    ax                     : ax-object where the endpoint will be drawn
        
    x                      : x-coordinate of the point (x, y)
        
    y                      : y-coordinate of the point (x, y)
        
    endpointcolor          : a tuple of list containing the color of the outercircle (at index 0) and the color of the innercircle (at index 1). The default value of None triggers a white outercircle and a black innercircle.
         (Default value = None)
    markersize_outercircle : width of the first circle. This first circle overwrites all objects in the neighbourhood of the point.
         (Default value = 7)
    markersize_innercircle : width of the second circle. The second circle overwrites the middle of the first circle.
         (Default value = 3)

    Returns
    -------
    None: This function has no real returnvalue. An endpoint is added on the axes-object
    """

    # First, check the endpointcolor
    if endpointcolor == None:
        # No colorinformation was passed for the endpoints
        endpointcolor = ('#FFFFFF', '#000000')                            # Color white for outercircle and black for innercircle
    elif type(endpointcolor) != type(tuple()) and type(endpointcolor) != type(list()):
        # endpointcolor is not a tuple and not a list
        raise ValueError("Expected value for endpointcolor would be a tuple or a list of two colors. The first color would be the outercircle-color and the second color would be the innercircle-color")
    elif len(endpointcolor) != 2:
        # enpointcolor does not contain two values. I do not check if these values are colors.
        raise ValueError("Expected value for endpointcolor would be a tuple or a list of two colors. The first color would be the outercircle-color and the second color would be the innercircle-color")

    # Second, check the markersize
    if markersize_outercircle <= markersize_innercircle:
        raise ValueError("markersize_outercircle needs to be greater than markersize_innercircle. For example: markersize_outercircle=7 and markersize_innercircle=3")

    # Third, add the outercircle around the endpoint
    ax.plot(x, y, color=endpointcolor[0], marker='o', markersize=markersize_outercircle)

    # Fourth, add smaller innercircle around the endpoint
    ax.plot(x, y, color=endpointcolor[1], marker='o', markersize=markersize_innercircle)

    
def prepare_title(title=None, multiplier=None):
    """
    Prepares a title
        
    Parameters
    ----------
    title : a dictionary with text values to construct a title. No part of the title is mandatory, except when 'Business_measure' is filled, the 'Unit' is expected to be filled too.
         (default value: None). No title will be constructed.
        
            more info:
                 title['Reporting_unit'] = 'Global Corporation'     # This is the name of the company or the project or business unit, added with a selection. For example 'ACME inc., Florida and California'
                 title['Business_measure'] = 'Net profit'           # This is the name of the metric. Can also be a ratio. For example: 'Net profit' or 'Cost per headcount'
                 title['Multiplier'] = 'm'                          # This is the multiplier used for the values in the dataset. Use 1 for one, k for 1000, m for 1000000 and b for 1000000000
                 title['Unit'] = 'CHF'                              # This is the name of the unit. For example: 'USD', 'EUR', '#', '%'.
                 title['Time'] = '2022: AC Jan..Aug, FC Sep..Dec'   # This is the description of the time, scenario's and variances. For example: '2022 AC, PL, FC, PL%'
    
    Returns
    -------
    title_text: the constructed title out of the dictionary or the value None if no title was given
    """
    # Check if there is a title
    if title == None:
        # No title
        return None

    # Prepair multiplier    
    if multiplier is None:
        multiplier_str = ''
    else:
        if multiplier == '1':
            multiplier_str = ''
        else:
            multiplier_str = multiplier

    # Construct the title
    # I use the math part to make a part of the title in bold, more specifically the 'Business_measure'
    title_text = ''
    for element in ('Reporting_unit', 'Business_measure', 'Unit', 'Time'):
        if element in title.keys():
            if element == 'Business_measure':
                if 'Unit' not in title.keys():
                    raise ValueError("Business_measure is filled, but Unit is empty. Please fill Unit also.")
                # In the math part below, spaces needs to be converted to backslash space, or the space won't be visible    
                title_text = title_text + r"$\bf{" + title[element].replace(' ', '\ ') + r"}$"
            elif element == 'Unit':
                title_text = title_text + ' in ' + multiplier_str + title[element] + '\n'
            else:
                title_text = title_text + title[element] + '\n'

    # Remove last 'new line' if available
    if title_text[-1:] == '\n':
        title_text = title_text[:-1]

    return title_text


def formatstring(decimals=None):
    """
    Give a string with the formatstring so values behave according to the formatstring.
    NOTE: Be aware that the displayed number will not be rounded, but just cut at the given position of decimals.

    Parameters
    ----------
    decimals : How many decimals do you need
         (default value: None). No decimals provided. This causes an error

    Returns
    -------
    string: this is a format-string
            %0i   : integer
            %0.1f : float with 1 decimal
            %0.2f : float with 2 decimals
            %0.3f : float with 3 decimals
    """
    if isinteger(decimals):
        # Integer-value provided
        if decimals >= 0 and decimals <= 3:
            return ["%0i", "%0.1f", "%0.2f", "%0.3f"][decimals]
    # All other values are not supported.
    raise ValueError("Decimals has value: "+str(decimals)+". Only values 0 to 3 are supported.")


def optimize_data(data=None, numerator=1, denominator=1, decimals=None):
    """
    Optimizes your data to multiply it with the numerator and divide it with the denominator.

    Parameters
    ----------
    data : Data to be optimized. Supports list, integer or float. 
           With integer or float, the optimization is done directly (value * numerator / denominator).
           With a list, each element will be handled with a recall to this function.
           With other data types, the value will be given back.
         (default value: None). This value will be given back.

    numerator   : The value to multiply with.
         (default value: 1).

    denominator : The value to devide with.
         (default value 1).

    decimals    : How many decimals needs to be supported?
         (default value None).

    Returns
    -------
    returnvalue: This can be an integer when the input is integer or float and decimals is equal to zero
                 This can be a float when the input is integer or float and decimals is not equeal to zero
                 This can be a list of processed values when the input is a list
                 This can be the input value of data, just given back to the caller
    """
    # Denominator may not be a zero, because of division by zero error
    if isinteger(denominator) or isfloat(denominator):
        # Denominator is an integer or a float
        if denominator == 0 or denominator == 0.0:
            raise ValueError("Denominator "+str(denominator)+" will cause a division-by-zero-error")
        # else there will be no division-by-zero-error, go further
    else:
        # Denominator is not an integer and not a float
        raise TypeError("Denominator "+str(denominator)+" is not of type integer or type float, but of type "+str(type(denominator)))

    # Numerator needs to be an integer or a float
    if not (isinteger(numerator) or isfloat(numerator)):
        # Numerator is not an integer and not a float
        raise TypeError("Numerator "+str(numerator)+" is not of type integer or type float")

    # Decimals needs to be an integer if not None
    if not decimals is None:
        error_not_isinteger(decimals, "decimals")
        # Decimals is now an integer

    # Process the data    
    if islist(data):
        # Data is a list
        returnvalue = data[:]
        for number, element in enumerate(returnvalue):
            returnvalue[number] = optimize_data(data=element, numerator=numerator, denominator=denominator, decimals=decimals)
    elif isinteger(data) or isfloat(data):
        # Data is a integer or data is a float
        if decimals is None:
            # No rounding
            returnvalue = data * numerator / denominator
        elif decimals == 0:
            # The function "round" returns a float and with 0 decimals, you like to have an integer
            returnvalue = int(round(data * numerator / denominator, decimals))
        else:
            # Decimals is an integer, but decimals <> 0, we can use the round-function
            returnvalue = round(data * numerator / denominator, decimals)        # Data is an integer or data is a float
    else:
        # Not a supported data type, just give the value back.
        returnvalue = data
    return returnvalue


def convert_number_to_string(data=None, decimals=None, delta_value=False):
    """
    The function convert_number_to_string converts a integer or float to a string or a list of items to a string.
    In case of a integer or a float, the number of decimals will be used for the output. If decimals is None, then a normal
    conversion to string will take place

    In case of delta_value=True then a positive sign will be placed before a positive value. Negative signs will be untouched for
    negative values.
    In case of delta_value=False, then positive integer and float values have no positive sign.
    That's why this function makes a string of a integer or float and adds a plus sign (+) to a positive value 
    (also adds a plus sign to a zero value).

    Parameters
    ----------
    data                  : An integer or float or list of integers and or floats. When of other type, the value will be 
                            converted to a string with no additional modification.
    decimals              : An integer indicating the number of decimals. Only values 0 - 3 are supported.
                            When decimals is None, no decimal reduction or extension will be done.
    delta_value           : A boolean to address the addition of a positive sign to positive integers, floats or 0-values.
                            True: A plus-sign will be added for positive values and 0-values.
                            False: No plus-sign will be added for positive values and 0-values.
                            Default value: False (No plus-sign)

    Returns
    -------
    returnvalue           : one single string or a list of strings
    """
    def _delta_treatment(string_value, value, delta_value):
        """
        The local function _delta_treatment adds a plus sign to a number-value in case of value >=0
        """
        error_not_isstring(string_value)
        error_not_isboolean(delta_value)
        if delta_value:
            # Yes, we need to add a plus sign in case of value >= 0
            if isinteger(value) or isfloat(value):
                # Yes, it is a number
                if value >= 0:
                    # Yes, it is positive or 0, add a plus sign
                    return '+' + string_value
                else:
                    # No, it is negative, return unmodified string_value
                    return string_value
            else:
                # No, it is not a number
                raise TypeNumberError("Value is not an integer or a float, but of type:"+str(type(value)))
        else:
            # No, we don't need to add a plus sign in case of value >=0, just return unmodified string_value
            return string_value

    def _check_decimals(string_value, decimals):
        """
        The local function _check_decimals checks and corrects the number of decimals
        """
        error_not_isstring(string_value)
        error_not_isinteger(decimals)
        if '.' in string_value:
            # Yes, there is a decimal point
            position = string_value.find('.')
            string_decimals = string_value[position+1:]+ '000'
            string_decimals = string_decimals[:decimals]
            return string_value[:position+1]+string_decimals
        else:
            # A decimal point is not available, add it and add the number of decimals
            return string_value + '.' + '0'*decimals
 
    # Check parameter decimals
    if not decimals is None:
        # Decimals has a value other than 0, only support for integer values 0 to 3
        error_not_isinteger(decimals, "decimals")
        # Decimals is an integer, check value
        if decimals < 0 or decimals > 3:
            # Decimals is out of supported range (0, 1, 2, 3 are supported)
            raise ValueError("Decimals is only supported for 0, 1, 2 or 3, but has value:"+str(decimals))
    # Decimals has now a valid value (None or 0, 1, 2 or 3)

    # Check parameter delta_value
    error_not_isboolean(delta_value, "delta_value")
    # Delta_value is a boolean

    # Supports int/float and lists of int/float
    if isinteger(data) or isfloat(data):
        # Data is of type integer or of type float
        if not decimals is None:
            # Decimals has a supported value of 0, 1, 2 or 3
            if decimals == 0:
                # Decimals=0. Round with 0 decimals gives a float with .0. You want an integer in this case!
                returnvalue = _delta_treatment(string_value=str(int(round(data, decimals))),
                                               value=data, delta_value=delta_value)
            else:
                # Decimals<>0.
                returnvalue = _check_decimals(string_value=_delta_treatment(string_value=str(round(data, decimals)),
                                                                            value=data, delta_value=delta_value),
                                              decimals=decimals)
        else:
            # Decimals is None
            returnvalue = data
    elif isstring(data):
        # Data is of type string. Return the same value
        returnvalue = data
    elif islist(data):
        # Data is of type list
        # Recursive so we check with the same code all elements of the list
        returnvalue = [convert_number_to_string(data=x, decimals=decimals, delta_value=delta_value) for x in data]
    else:
        # Data is not of type integer, not of type float, not of type string and not of type list
        returnvalue = str(data)

    return returnvalue


def string_to_value(value):
    """
    Tries to make integers or floats from a stringvalue. When provided with a list, the list will processed element-wise
    """
    if value is None:
        return value
    elif islist(value):
        for index, element in enumerate(value):
            value[index] = string_to_value(element)
        return value
    elif value == 'None':
        return None
    elif isinteger(value) or isfloat(value):
        return value
    elif isstring(value):
        if value.count(".") == 1:
            if value.lstrip('-').replace('.', '').isdigit():
                return float(value)
            else:
                # Not sure how to handle this, just return the value
                return value
        elif value.count(".") == 0:
            if value.lstrip('-').isdigit():
                return int(value)
            else:
                # Not sure how to handle this, just return the value
                return value
        else:
            # Not sure how to handle this, just return the value
            return value
    else:
        # Not sure how to handle it, just return the value
        return value


def filter_lists(list1=None, list2=None):
    """
    Filters list1 against list2 and returns only those elements who are in both lists, in the same order as list1
    If list1 or list2 (or both) are not a list a TypeError will occur.

    Parameters
    ----------
    list1          : the (mostly) smaller list
                     Default: None (no list will result in a TypeError)
    list2          : the (mostly) bigger list
                     Default: None (no list will result in a TypeError)

    Returns
    -------
    a list of elements who are in both lists in the same order as list1
    """
    if not islist(list1):
        raise TypeError("list1 "+str(list1)+" is not a list, but is of type: "+str(type(list1)))
    if not islist(list2):
        raise TypeError("list2 "+str(list2)+" is not a list, but is of type: "+str(type(list2)))

    # The order of the list is important. So implementation not with intersection, but a list comprehension
    return [element for element in list1 if element in list2]


def list1_is_subset_list2(list1=None, list2=None):
    """
    Checks the unique elements of list1 against the unique elements of list2. Gives true when all elements of list1 can be found in list2
    If list1 or list2 (or both) are not a list a TypeError will occur.

    Parameters
    ----------
    list1          : Can contain other elements
                     Default: None (no list will result in a TypeError)
    list2          : Contains the maximum of valid elements
                     Default: None (no list will result in a TypeError)

    Returns
    -------
    returnvalue    : True, all elements of list1 can be found in list2,
                     False, not all elements of list1 can be found in list2
    """
    # Check parameters
    error_not_islist(list1)
    error_not_islist(list2)

    # We use set operations to quickly find the other elements of list 1
    return set(list1).issubset(set(list2))


def convert_data_string_to_pandas_dataframe(data_string, separator=','):
    """
    If the data is like a string, this function sees it as a CSV-file pasted in a string and will make it a pandas DataFrame.

    Parameters
    ----------
    data_string      : data_string contains a string-like CSV-file.

    Returns
    -------
    export_dataframe : pandas DataFrame with stripped (remove leading and trailing spaces) object columns
    """
    # Check if data_string is a string
    if not isstring(data_string):
        # No, it is not a string
        raise TypeError(str(data_string)+" is not a string")

    # Data will be extracted from a list of lists (based on the first split '\n' (newline) and the second split with the separator), 
    # from line 1 (second line) and up
    # The column-names will be extracted from the line 0 (the first line)
    # Stripped lines with a lenght of 0 will be skipped. So empty lines will be skipped. 
    export_dataframe = pd.DataFrame(data=[x.strip().split(separator) for x in data_string.split('\n') if len(x.strip())>0][1:], 
                                    columns=[x.strip() for x in data_string.split('\n') if len(x.strip())>0][0].split(separator))

    # First strip the column names
    export_dataframe.columns = [x.strip() for x in export_dataframe.columns]

    # Select the columns with data type objects (because the stripping of spaces can only be done on objects, not lists or other types in the dataframe)
    dataframe_object = export_dataframe.select_dtypes(['object'])

    # Now strip these colums of the object types
    export_dataframe[dataframe_object.columns] = dataframe_object.apply(lambda x: x.str.strip())

    return export_dataframe


def convert_data_list_of_lists_to_pandas_dataframe(data_list):
    """
    Makes a pandas DataFrame out of a list of lists. The first list of the lists will be used as the header with the column names

    Parameters
    ----------
    data_list        : data_list contains a list of lists with the first list of the lists as the header with the column names.

    Returns
    -------
    export_dataframe : pandas DataFrame
    """
    # Check if the data is a list (or else we get a TypeError), because we need a list (containing more lists)
    if not islist(data_list):
        # No, it is not a list
        raise TypeError(str(data_list)+" is not a list.")
    else:
        # Yes, data_list is a list. Check if all elements are lists too
        for element in data_list:
            if not islist(element):
                # No, this element is not a list
                raise TypeError("Element "+str(element)+" is not a list")

    # First list-item (0) is the header with the column names. List-item 2 and up is the data.
    export_dataframe = pd.DataFrame(data_list[1:], columns=data_list[0])

    return export_dataframe


def convert_dataframe_scenario_columns_to_value(dataframe, scenariolist):
    """
    Convert columns in the dataframe in the scenariolist into integers or floats.

    Parameters
    ----------
    dataframe        : pandas DataFrame containing columns from scenariolist.
    scenariolist     : list of scenarios to convert from string to integer or float

    Returns
    -------
    export_dataframe : pandas DataFrame
    """
    # Check if the scenariolist is a list
    if not islist(scenariolist):
        # No, it is not a list
        raise TypeError(str(scenariolist)+" is not a list.")

    # Check dataframe
    error_not_isdataframe(dataframe, "dataframe")

    # Check scenariolist in DataFrame, error when not in DataFrame column-names
    dataframe_search_for_headers(dataframe, search_for_headers=scenariolist, error_not_found=True)

    export_dataframe = dataframe.copy()
    for scenario in scenariolist:
        valuelist = list(export_dataframe[scenario])
        newvaluelist = string_to_value(valuelist)
        export_dataframe[scenario] = newvaluelist

    return export_dataframe


def dataframe_translate_field_headers(dataframe, translate_headers=None):
    """
    If the variable translate_headers is filled with a dictionary, we can use it for translating the field headers.
    This function will do this translation to the columnheaders of the dataframe.

    Parameters
    ----------
    dataframe         : pandas DataFrame with 'old' field headers.

    translate_headers : dictionary of {'old-field-name':'new-field-name'} combinations
                        Default: None (no translation of fieldnames)

    Returns
    -------
    export_dataframe  : pandas DataFrame with translated field headers
    """
    # Check if the dataframe is a pandas DataFrame or not. Error when not a DataFrame.
    if not isdataframe(dataframe):
        raise TypeError(str(dataframe)+" is not a pandas DataFrame")

    # Prepare export_dataframe
    export_dataframe = dataframe.copy()

    # Is there a translation?
    if translate_headers is not None:
        # Yes, there is a translations
        if isdictionary(translate_headers):
            # Yes, and it of the type dictionary, now we can translate the field headers
            # Put the headers of the dataframe into 'columnlist'
            columnlist = list(export_dataframe.columns)
            for counter, fieldheader in enumerate(columnlist):
                if fieldheader in translate_headers:
                    # Yes, we have a match for translation
                    columnlist[counter] = translate_headers[fieldheader]
                # else
                    # No matching fieldheader, go further
            # Use the translated field headers for the dataframe
            export_dataframe.columns = columnlist
        else:
            raise TypeError('Parameter '+str(translate_headers)+' is not a dictionary!')
    # else
        # No translation available, go further

    return export_dataframe


def dataframe_search_for_headers(dataframe, search_for_headers, error_not_found=False):
    """
    If the data is a pandas DataFrame, this function will search for the headers and returns the found headers.
    If error_not_found=True, and the headers are not found, you'll get an error.
    
    Parameters
    ----------
    dataframe          : pandas DataFrame
    
    search_for_headers : a list with headers to search for in the DataFrame
    
    error_not_found    : if the search_for_headers are not completely found, True gives an error, False gives no error
                         Default: False (give no error)
    
    Returns
    -------
    available_headers  : The headers out of the list of search_for_headers who are found in the DataFrame
    """
    # Check if the dataframe is a pandas DataFrame or not. Error when not a DataFrame.
    if not isdataframe(dataframe):
        raise TypeError(str(dataframe)+" is not a pandas DataFrame.")

    # Check if search_for_headers is a list. Error when not a list
    if not islist(search_for_headers):
        raise TypeError(str(search_for_headers)+" is not a list")

    # Check if error_not_found is a boolean
    if not isboolean(error_not_found):
        raise TypeError(str(error_not_found)+" is not a boolean")

    # Determine which headers are available in the dataframe
    available_headers = filter_lists(list1=search_for_headers, list2=list(dataframe.columns))

    # Do we need to raise an error?
    if error_not_found:
        # Yes, we need to raise an error if both lists are not equal
        if available_headers != search_for_headers:
            raise ValueError("Expected columns in the DataFrame: "+str(search_for_headers)+". But found only these columns: "+str(available_headers))

    return available_headers


def dataframe_date_to_year_and_month(dataframe, date_field, year_field, month_field=None):
    """
    If the data is a pandas DataFrame, this function uses the column with the name 'Date' (if available) and extracts it to 'Year' and 'Month' (optional).
    If the 'Year' and 'Month' columns are already provided, they will be overwritten with the year and month out of the Date-column.
    No testing will be done if the year and month out of the date-column is the same as the provided year and month columns.

    Parameters
    ----------
    dataframe        : pandas DataFrame with a lot of columns. A column named 'Date' is not mandatory, but optional

    date_field       : list with one column name for the date field. ['Date'] would be a correct value

    year_field       : list with one column name for the year field. ['Year'] would be a correct value

    month_field      : list with one column name for the month field. ['Month'] would be a correct value
                       Default: None (No extraction to date column will be done)

    Returns
    -------
    export_dataframe : pandas DataFrame. If there was a column named 'Date', then there are now columns called 'Year' and 'Month' (optional)
                       also with related values
    """
    # Check date_field. It needs to be a list and it needs to have exactly one value.
    if not islist(date_field):
        raise TypeError("Date_field is not a list: "+str(type(date_field)))
    elif len(date_field) != 1:
        raise ValueError("Date_field needs to have exactly one value in the list: "+str(len(date_field)))

    # Check year_field. It needs to be a list and it needs to have exactly one value.
    if not islist(year_field):
        raise TypeError("Year_field is not a list: "+str(type(year_field)))
    elif len(year_field) != 1:
        raise ValueError("Year_field needs to have exactly one value in the list: "+str(len(year_field)))

    # Check month_field. It may be a list and when it is a list, it needs to have exactly one value.
    if month_field is not None and not islist(month_field):
        raise TypeError("Month_field is not None and month_field is not a list: "+str(type(month_field)))
    elif islist(month_field) and len(month_field) != 1:
        raise ValueError("If month_field is a list, it needs to have exactly one value: "+str(len(year_field)))

    # We want the header 'Date', but is not mandatory
    wanted_headers = date_field

    # Search for available headers
    available_headers = dataframe_search_for_headers(dataframe, search_for_headers=wanted_headers, error_not_found=False)

    # Copy the dataframe to the export-parameter
    export_dataframe = dataframe.copy()

    # Check for Date-headers
    if len(available_headers) > 0:
        # There is a date column in the pandas dataframe, but the values in this column can have a non-date format yet. Be sure to make it a dateformat first
        date_column = available_headers[0]
        export_dataframe[date_column] = pd.to_datetime(export_dataframe[date_column])
        # Now we have a real date-format in this column, now extract the year and the month
        export_dataframe[year_field[0]]  = export_dataframe[date_column].dt.year
        if islist(month_field):
            export_dataframe[month_field[0]] = export_dataframe[date_column].dt.month
    # else
        # We don't need to do something. It is not mandatory that there should be a date column.

    return export_dataframe


def dataframe_keep_only_relevant_columns(dataframe, wanted_headers):
    """
    If the data is a pandas DataFrame, this function will narrow this DataFrame down to the wanted columns. If not all wanted columns are available
    we will use only the available headers

    Parameters
    ----------
    dataframe        : pandas DataFrame with a lot of columns.
    wanted_headers   : list of wanted column names
    
    Returns
    -------
    export_dataframe : pandas DataFrame with at most the columns of the wanted headers
    """
    # Check for the list of wanted headers
    if not islist(wanted_headers):
        raise TypeError("Parameter 'wanted_headers' ("+str(wanted_headers)+") is of type "+str(type(wanted_headers)))

    # Search for available headers
    available_headers = dataframe_search_for_headers(dataframe, search_for_headers=wanted_headers, error_not_found=False)

    # We only need the data from these columns for the purpose of this chart
    export_dataframe = dataframe[available_headers].copy()
    
    return export_dataframe


def dataframe_convert_year_month_to_string(dataframe, wanted_headers, year_field, month_field):
    """
    If the data is a pandas DataFrame, this function will convert the year and month to string values (containing numbers) for convenient sorting.

    Precondition: The dataframe dataframe needs to be aggregated by the wanted_headers.

    Parameters
    ----------
    dataframe        : pandas DataFrame, aggregated by wanted headers.
    wanted_headers   : a list of column names
    year_field       : a list with one element representing the header for the year-column
    month_field      : a list with one element representing the header for the month-column

    Returns
    -------
    export_dataframe : pandas DataFrame sorted by available headers if year and/or month are in available headers
    """
    # Search for available headers
    available_headers = dataframe_search_for_headers(dataframe, search_for_headers=wanted_headers, error_not_found=False)

    # Initialise sort-variable: standard no-sorting
    sort_dataframe = False

    # Prepare the dataframe to be returned
    export_dataframe = dataframe.copy()

    # Convert year to string.
    year = year_field[0]
    if year in available_headers:
        # Yes, year is available in the headers, so we can sort on that
        export_dataframe[year] = export_dataframe[year].apply(int).apply(str)
        sort_dataframe = True

    # Convert month to string with length=2, filled with leading zeros if value < 10
    month = month_field[0]
    if month in available_headers:
        # Yes, month is available in the headers, so we can sort on that
        export_dataframe[month] = export_dataframe[month].apply(int).apply(str).str.zfill(2)
        sort_dataframe = True

    # Do we need to sort?
    if sort_dataframe:
       # Yes, sort dataframe by available headers
       export_dataframe = export_dataframe.sort_values(available_headers, ascending = [True] * len(available_headers)).copy()

    return export_dataframe


def get_default_scenarios(type_scenario=None, scenarios=None):
    """
    The function get_default_scenarios chooses the best possible scenarios given the type_scenario and available scenarios.

    Parameters
    ----------
    type_scenario    : Type of scenarios. Choose from 'base' or 'compare'.
                       Default: None
    scenarios        : List of scenarios to assign to the export_scenarios

    Returns
    -------
    export_scenarios : List of scenarios related to the type_scenario
    """
    # Check parameter type_scenario
    if type_scenario is None:
        return
    error_not_isstring(type_scenario)
    # Type_scenario is a string
    if not type_scenario == 'base' and not type_scenario == 'compare':
        raise ValueError('Parameter type_scenario needs to have value "base" or value "compare".')

    # Check parameter scenarios
    error_not_islist(scenarios)
    # scenarios is a list

    # Fill export variable
    export_scenarios = scenarios[:]

    if type_scenario == 'base':
        # Never 'AC' as a base scenario
        export_scenarios = [x for x in export_scenarios if x != 'AC']
        if len(export_scenarios) > 2:
            export_scenarios = export_scenarios[:2]
        export_scenarios.reverse()
    else:
        # Never 'PY' as a compare scenario
        export_scenarios = [x for x in export_scenarios if x != 'PY']
        if len(export_scenarios) > 1:
            #### THIS VERSION SUPPORTS ONLY ONE COMPARE SCENARIO
            export_scenarios.reverse()
            export_scenarios = export_scenarios[:1]
    return export_scenarios


def check_scenario_translation(standardscenarios, translation=None):
    """
    Incorporates the translation for the scenarios into the standard scenarios.

    For example:
    standardscenarios = {'PY':'PY', 'PL':'PL', 'AC':'AC', 'FC':'FC'}  # As standard scenarios are PY, PL, AC, FC
    translation       = {'PY':'PP', 'ZZ':'AA'}
    results into      : {'PY':'PP', 'PL':'PL', 'AC':'AC', 'FC':'FC'}  # PP will be adopted as outputtranslation for PY. but AA will not be adopted as ZZ is not a standard scenario

    Parameters
    ----------
    standardscenarios : Dictionary with standard scenarios as keys and their standard translation as value
    translation       : Dictionary with standard scenarios as keys (will have a valid translation) or other keys and translation as values
                        Default: None (No translation needed)
    Returns
    -------
    export_dictionary : Dictionary with standard scenarios as keys and their translation as value
    """
    # Standardscenarios needs to be a dictionary
    error_not_isdictionary(standardscenarios, "standardscenarios")
    # Standardscenarios is now a dictionary

    # Prepare exportvariable
    export_dictionary = standardscenarios

    #Check if a translation is given
    if translation is None:
        # No translation given
        return export_dictionary

    # Translation is given. This needs to be a dictionary
    error_not_isdictionary(translation, "translation")
    # Translation is now a dictionary

    export_dictionary = {key: translation.get(key, standardscenarios[key]) for key in standardscenarios}

    return export_dictionary