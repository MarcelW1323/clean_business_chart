"""General functions."""

# Import modules
import matplotlib.pyplot as plt                   # for most graphics
from matplotlib.patches import ConnectionPatch    # for lines between subplots (used in the function "plot_line_accross_axes")
import pandas as pd                               # for easy pandas support


#####################    
# GENERAL FUNCTIONS #
#####################

def islist(inputvariable):
    """Returns whether the inputvariable is a list (True) or not (False)"""
    return isinstance(inputvariable, list)

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

def isboolean(inputvariable):
    """Returns whether the inputvariable is a boolean (True) or not (False)"""
    return isinstance(inputvariable, bool)

def isdataframe(inputvariable):
    """Returns whether the inputvariable is a pandas DataFrame (True) or not (False)"""
    return isinstance(inputvariable, pd.DataFrame)   

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
        

def plot_line_within_ax(ax, xbegin, ybegin, xend, yend, linecolor='black', arrowstyle='-', linewidth=1, endpoints=False, endpointcolor=None):
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
    ax.plot([xbegin, xend], [ybegin, yend], color=linecolor, linewidth=linewidth, solid_capstyle='butt')
    # Without solid_capstyle='butt' the lines increase in length because of increasing linewidth
    
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

def check_valid_multiplier(multiplier=None):
    """
    Checks whether the multiplier is a valid multiplier (1, k, m, b).
        
    Parameters
    ----------
    multiplier : a string with one of the following values (1 character)
         (default value: None). No multiplier available
         
         valid options:
             1 : (this is the character 'one'). The corresponding value is one times that value (= the same value).
             k : kilo. The corresponding value needs to be multiplied with 1000 (ten to the third power) to get the real value.
             m : million. The corresponding value needs to be multiplied with 1000000 (ten to the sixth power) to get the real value.
             b : billion. This is the "short scale" billion (https://en.wikipedia.org/wiki/Billion). The corresponding value needs to be multiplied with 1000000000 (ten to the ninth power) to get the real value.             
    
    Returns
    -------
    True: multiplier is one of the supported values (1, k, m, b)
    False: multiplier is not one of the supported values
    """
    if multiplier not in ('1', 'k', 'm', 'b'):
        raise ValueError("multiplier "+str(multiplier)+" not supported. Multiplier not in list of valid multipliers: ('1', 'k', 'm', 'b')")
    else:
        return True


def formatstring(decimals=None):
    """
    Give a string with the formatstring so values behave according to the formatstring
        
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
    if type(decimals) == type(1):
        # Integer-value provided
        if decimals >= 0 and decimals <= 3:
            return ["%0i", "%0.1f", "%0.2f", "%0.3f"][decimals]
    # All other values are not supported.
    raise ValueError("Decimals has value: "+str(decimals)+". Only values 0 to 3 are supported.")


def optimize_data(data=None, numerator=1, denominator=1, decimals=0):
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

    Returns
    -------
    returnvalue: This can be an integer when the input is integer or float and decimals is equal to zero
                 This can be a float when the input is integer or float and decimals is not equeal to zero
                 This can be a list of processed values when the input is a list
                 This can be the input value of data, just given back to the caller
    """
    # Denominator may not be a zero, because of division by zero error
    if isinteger(denominator) or isfloat(denominator):
        if denominator == 0 or denominator == 0.0:
            raise ValueError("Denominator "+str(denominator)+" will cause a division-by-zero-error")
        # else there will be no division-by-zero-error, go further
    else:
        raise ValueError("Denominator "+str(denominator)+" is not of type integer or type float")

    # Numerator needs to be an integer or a float
    if not (isinteger(numerator) or isfloat(numerator)):
        raise ValueError("Numerator "+str(numerator)+" is not of type integer or type float")

    # Decimals needs to be an integer
    if not isinteger(decimals):
        raise ValueError("Decimals "+str(numerator)+" is not of type integer")    

    # Process the data    
    if islist(data):
        # Data is a list
        returnvalue = data[:]
        for number, element in enumerate(returnvalue):
            returnvalue[number] = optimize_data(data=element, numerator=numerator, denominator=denominator, decimals=decimals)
    elif isinteger(data) or isfloat(data):
        # Data is a integer or data is a float
        if decimals == 0:
            # The function "round" returns a float and with 0 decimals, you like to have an integer
            returnvalue = int(round(data * numerator / denominator, decimals))
        else:
            # Decimals <> 0, we can use the round-function
            returnvalue = round(data * numerator / denominator, decimals)
    else:
        # Not a supported data type, just give the value back.
        returnvalue = data
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
        