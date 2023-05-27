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
    if isinteger(decimals):
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
        raise TypeError("list1 "+str(list1)+" is not a list, but it's type is: "+str(type(list1)))
    if not islist(list2):
        raise TypeError("list2 "+str(list2)+" is not a list, but it's type is: "+str(type(list2)))

    # The order of the list is important. So implementation not with intersection, but a list comprehension
    return [element for element in list1 if element in list2]


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


def dataframe_date_to_year_and_month(dataframe, date_field, year_field, month_field):
    """
    If the data is a pandas DataFrame, this function uses the column with the name 'Date' (if available) and extracts it to 'Year' and a 'Month'.
    If the 'Year' and 'Month' columns are already provided, they will be overwritten with the year and month out of the Date-column.
    No testing will be done if the year and month out of the date-column is the same as the provided year and month columns.

    Parameters
    ----------
    dataframe        : pandas DataFrame with a lot of columns. A column named 'Date' is not mandatory, but optional

    Returns
    -------
    export_dataframe : pandas DataFrame. If there was a column named 'Date', then there are now columns called 'Year' and 'Month' also with related values
    """
    # Check date_field, year_field and month_field parameter
    if not islist(date_field) or not islist(year_field) or not islist(month_field):
        raise TypeError("At least one of these is not a list: date_field:"+str(type(date_field))+", year_field:"+str(type(year_field))+ \
                        ", month_field:"+str(type(month_field)))

    # We want the header 'Date', but is not mandatory
    wanted_headers = date_field

    # Search for available headers
    available_headers = dataframe_search_for_headers(dataframe, search_for_headers=wanted_headers, error_not_found=False)

    # Copy the dataframe to the export-parameter
    export_dataframe = dataframe.copy()

    # Check for Date-headers
    if len(available_headers) > 0:
        # There is a date column in the pandas dataframe, but it can have a non-date format yet. Be sure to make it a dateformat first
        date_column = available_headers[0]
        export_dataframe[date_column] = pd.to_datetime(export_dataframe[date_column])
        # Now we have a real data-format in this column, now extract the year and the month
        export_dataframe[year_field[0]]  = export_dataframe[date_column].dt.year
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
    export_dataframe : pandas DataFrame sorted by available headers
    """
    # Search for available headers
    available_headers = dataframe_search_for_headers(dataframe, search_for_headers=wanted_headers, error_not_found=False)

    # Convert year to string.
    year = year_field[0]
    if year in available_headers:
        # Yes, year is available in the headers
        dataframe[year] = dataframe[year].apply(int).apply(str)

    # Convert month to string with length=2, filled with leading zeros if value < 10
    month = month_field[0]
    if month in available_headers:
        # Yes, month is available in the headers
        dataframe[month] = dataframe[month].apply(int).apply(str).str.zfill(2)

    # Sort dataframe by available headers
    export_dataframe = dataframe.sort_values(available_headers, ascending = [True] * len(available_headers)).copy()

    return export_dataframe