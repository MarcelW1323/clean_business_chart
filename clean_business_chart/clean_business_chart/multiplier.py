"""Multiplier-module"""

from clean_business_chart.general_functions    import isinteger, isfloat

class Multiplier:
    """
    The class Multiplier helps you manage a multiplier in validating the multiplier, let you get the corresponding value and gives you the string to show. 
    And this class multiplier has a capability to optimize it, based on the value passed in.
    
    A multiplier is a character with which you can identify by which value the original value needs to multiply to interpret the correct value.
    
    Examples in understanding what a multiplier is:
    125 kEUR : The 'k' in 'kEUR' is the multiplier and tells you that the value 125 needs to be multiplied with 1000 to know its complete value. In this case 125000.
    285 mEUR : The 'm' in 'mEUR' is the multiplier and tells you that the value 285 needs to be multiplied with 1000000 to know its complete value. In this case 285000000.
    432 EUR  : Here you don't see a multiplier visually, because the value 432 stays the same. The implicit multiplier is '1'. One times 432 is 432 in this case.
    
    Examples:
    ---------
    variable = Multiplier('k')
    This stores the multiplier 'k' within the instance of the class Multiplier in the variable.
    
    Now you can do the following:
    new_variable = variable.get_multiplier()
    This gets you the value 'k' back.
    
    new_variable = variable.get_multiplier_index()
    This gets you the value 1 (because the index of 'k' in a zero-based list of ('1', 'k', 'm', 'b') is spot 2 and that's index one). Note: This is a numeric value and not the string '1', which is an other multiplier.
    
    new_variable = variable.get_multiplier_value()
    This gets you the value 1000 because multiplier 'k' means 'thousand'.
    
    new_variable = variable.get_multiplier_string()
    This gets you the value 'k' which you can combine with a unit, for example 'EUR' so that it will be 'kEUR'.
    The difference between get_multiplier and get_multiplier_string is for the multiplier '1', which gives '1' in get_multiplier but gives an empty string '' in get_multiplier_string.
    
    new_variable = variable.optimize(768995)
    This gives you a denominator back of 1000. It works as follows:
    We start with the multiplier 'k' (see the first example above). So 768995 means 768995k. The optimizer tries to divide this value (768995) by thousand and checks if there are still values left of one and greater.
    Well this works. 768995 divided by 1000 is 768.995 and the integer part of this value is one or greater (in this case 768). But by dividing by 1000, it increases the multiplier from 'k' (1000) to 'm' 1000000.
    Next it tries to divide 768.995 by 1000. Well you can do that (768.995 / 1000 equals 0.768995), but the integer part of this value (0) is not one or greater. So the optimization ends here.
    You get a denominator of 1000 and the multiplier stored in this instance of the class is now 'm'.
    This denominator is very important. All the values you have which were related to the multiplier 'k' needs to be divided by this denominator, so their value corresponds with the new multiplier 'm'.
    """
    def __init__(self, multiplier=None):
        self._multipliers = ('1', 'k', 'm', 'b')                  # Characters: 1 (one, 10^0), k (kilo, 10^3), m (million, 10^6), b (billion, 10^9)
        self._multiplier_values = (1, 1000, 1000000, 1000000000)  # Values    : 1 (one, 10^0), k (kilo, 10^3), m (million, 10^6), b (billion, 10^9)
        self._multiplier_strings = ('', 'k', 'm', 'b')            # Text      : '' , 'k' (kilo, 10^3), 'm' (million, 10^6), 'b' (billion, 10^9)
        self.set_multiplier(multiplier)                           # set parameter multiplier to self.multiplier if valid
        
    def check_valid_multiplier(self, multiplier=None):    
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
        True: Multiplier is one of the supported values (1, k, m, b)
        """
        value_to_check = multiplier
        if value_to_check is None:
            value_to_check = self.multiplier

        if value_to_check not in self._multipliers:
            raise ValueError("Multiplier "+str(value_to_check)+" not supported. Multiplier not in list of valid multipliers: "+str(self._multipliers))
        else:
            return True   # Just to return a value. Return without a value would also work. Now you can use it in an if-statement.


    def set_multiplier(self, multiplier=None):
        """
        Set the multipliers into a class internal variable of this instance so it will be stored for future retrievements, only if it is given as a parameter and that the multiplier is valid.
        
        Parameters
        ----------
        multiplier : a string with one of the following values (1 character): '1', 'k', 'm', 'b'
             (default value: None). No multiplier available
        """
        if multiplier is not None:
            if self.check_valid_multiplier(multiplier):
                self.multiplier = multiplier


    def get_multiplier(self):
        """
        Returns the current multiplier for this instance of the class.
        
        Returns
        ----------
        multiplier : a string with one of the following values (1 character): '1', 'k', 'm', 'b'
        """
        return self.multiplier

 
    def get_multiplier_index(self, multiplier=None):
        """
        Returns the index of the parameter multiplier or when called without parameter the index of the current multiplier for this instance of the class.

        Parameters
        ----------
        multiplier : a string with one of the following values (1 character): '1', 'k', 'm', 'b'
             (default value: None). No multiplier available
             
        Returns
        ----------
        index of multiplier : number (0 to 3 inclusive) from the sequence of valid multipliers ('1', 'k', 'm', 'b')
        """
        if multiplier is not None:
            # Parameter filled
            if self.check_valid_multiplier(multiplier):
                # Parameter filled and valid, use parameter multiplier
                return self._multipliers.index(multiplier)
        else:
            # Parameter not filled, use stored multiplier
            return self._multipliers.index(self.multiplier)


    def get_multiplier_value(self, multiplier=None):
        """
        Returns the value of the parameter multiplier or when called without parameter the value of the current multiplier for this instance of the class.

        Parameters
        ----------
        multiplier : a string with one of the following values (1 character): '1', 'k', 'm', 'b'
             (default value: None). No multiplier available
             
        Returns
        ----------
        value of multiplier : number (1, 1000, 1000000, 1000000000) respectively from the sequence of valid multipliers ('1', 'k', 'm', 'b')
        """
        if multiplier is not None:
            # Parameter filled
            if self.check_valid_multiplier(multiplier):
                # Parameter filled and valid, use parameter multiplier
                return self._multiplier_values[self._multipliers.index(multiplier)]
        else:
            # Parameter not filled, use stored multiplier
            return self._multiplier_values[self._multipliers.index(self.multiplier)]


    def get_multiplier_string(self, multiplier=None):
        """
        Returns the string (0 or one character) of the parameter multiplier or when called without parameter the string (0 or one character) of the current multiplier for this instance of the class.

        Parameters
        ----------
        multiplier : a string with one of the following values (1 character): '1', 'k', 'm', 'b'
             (default value: None). No multiplier available
             
        Returns
        ----------
        value of multiplier : number (1, 1000, 1000000, 1000000000) respectively from the sequence of valid multipliers ('1', 'k', 'm', 'b')
        """
        if multiplier is not None:
            # Parameter filled
            if self.check_valid_multiplier(multiplier):
                # Parameter filled and valid, use parameter multiplier
                return self._multiplier_strings[self._multipliers.index(multiplier)]
        else:
            # Parameter not filled, use stored multiplier
            return self._multiplier_strings[self._multipliers.index(self.multiplier)]


    def optimize(self, value):
        """
        Optimizes the multiplier by trying to divide the value by 1000 over and over again als long as the result will be one or greater and as long as there are still multipliers left in the sequence ('1', 'k', 'm', 'b').
        The new optimized multiplier will be stored as multiplier in this instance of the class.

        Parameters
        ----------
        value : a numeric value (integer or float) which will be the optimized.
             
        Returns
        ----------
        denominator : a factor by which all related values needs to be divided by. The denominator can be 1 (no further optimization possible), 1000, 1000000 or 1000000000.
        """
        # Check for integer or float
        if not isinteger(value) and not isfloat(value):
            raise TypeError('Parameter value "'+str(value)+'" is not an integer or a float, but of type '+str(type(value)))

        # Prepare optimization
        multiplier_index = self.get_multiplier_index()
        copy_value = value
        denominator = 1

        # Keep on going to the next multiplier as long as the value with the next multiplier will be one or greater and as long as there are multipliers left
        while ((copy_value // 1000 ) >= 1) and (multiplier_index < len(self._multipliers)-1):
            multiplier_index += 1
            copy_value  /= 1000
            denominator *= 1000
        
        # Set the new multiplier
        self.set_multiplier(self._multipliers[multiplier_index])
        return denominator