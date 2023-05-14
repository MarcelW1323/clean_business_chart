"""DeltaChart-module"""

from clean_business_chart.clean_business_chart import GeneralChart 

class DeltaChart(GeneralChart):
    """
    The class DeltaChart helps you calculate a delta chart and prepare the visualisation of a delta chart.
    
    Capability:
    Calculate
    Prepare
    Visualize

    Examples:
    ---------
    ... to be documented ...
    """
    def __init__(self):
        
        print("DeltaChart-init")
        
        # Class variables
        self.delta_value_list    = list()
        self.delta_percent_list  = list()
        self.delta_scenario_list = list()
        self.delta_base_scenario = None
        self.use_max_length      = None
        
        dataset = {'PY': [14, 16, 14, 17, 19, 17, 19, 22, 16, 17, 16, 22], 
                   'PL': [11, 10, 10, 10, 10, 10, 15, 14, 15, 15, 15, 19],
                   'AC': [15, 13, 16,  7,  5,  6, 17, 11],
                   'FC': [ 0,  0,  0,  0,  0,  0,  0,  0, 26, 22, 13, 29]}
                   
        # TECHNICAL DEBT: Needed for the self.filter_scenarios
        self.data_scenarios = list(dataset.keys())
        print("data_scenarios = ", self.data_scenarios)
                   
        testvar = self.calculate_h(data=dataset, base_scenario='PL', compare_scenario_list=['AC', 'FC'])
        print("Testvar\n",testvar)
              

    def calculate_h(self, data, base_scenario, compare_scenario_list, max_length=None, round_decimals_percentages=1):
        """
        Calculate the delta values for a horizontal delta chart
        """
        print("Calculate\ndata:", data, "\nbase_scenario:", base_scenario, "\ncompare_scenario_list:", compare_scenario_list)
        self.delta_base_scenario = base_scenario                       # Get the value of the base scenario and put it in a class variable
        self.use_max_length      = self._calculate_max_length(data=data, base_scenario=base_scenario, compare_scenario_list=compare_scenario_list, max_length=max_length)
        print("self.use_max_length", self.use_max_length)
        
        # Initialize work variables
        self.delta_value_list    = [0]  * self.use_max_length     # Make a list with only zeros to record the delta values
        self.delta_percent_list  = [0]  * self.use_max_length     # Make a list with only zeros to record the delta percentages
        self.delta_scenario_list = [''] * self.use_max_length     # Make a list with only empty scenarios to record the comparable scenario responsible for the delta 
        
        if base_scenario in data.keys():
            work_base_list = list(data[base_scenario])            # Make a copy of the data-list for the base scenario because the work_base_list will be modified
        else:
            raise ValueError("Base_scenario", base_scenario, "not in the keys of de dictionary of the data.")

        # A delta is the difference of the compare_scenario value and the base_scenario value. We need to record this difference and the scenario this difference belongs to.
        # If the scenario alters, we add this information to the month-name if the related parameter add_scenario_to_month is True
        # IBCS advices to display 'n.a.' (not available) if the relative variance can not be interpreted. This is often the case when you compare a positive value to a negative reference value (in the denominator)        
        for new_scenario in self.filter_scenarios(scenario_list=compare_scenario_list):
            for number, compare_element in enumerate(data[new_scenario]):
                print("PRE Number:",number, "Scenario:", new_scenario, "Compare_element:", compare_element, "work_base_list[number]:", work_base_list[number])
                work_base_list[number], self.delta_scenario_list[number], self.delta_value_list[number] = \
                    self._calculate_element(old_scenario            = self.delta_scenario_list[number],
                                            old_delta_value_element = self.delta_value_list[number],
                                            base_element            = work_base_list[number], 
                                            new_scenario            = new_scenario, 
                                            compare_element         = compare_element)
                print("POST Number:",number, "Scenario_list:", self.delta_scenario_list[number], "Value_list:", self.delta_value_list[number], "work_base_list[number]:", work_base_list[number])
            print("Mid\n",self.delta_scenario_list,"\n",self.delta_value_list)
        print("END\n",self.delta_scenario_list,"\n",self.delta_value_list)
        print("TODO: calculate relative values")

    def _calculate_element(self, old_scenario, old_delta_value_element, base_element, new_scenario, compare_element):
        
        
        if compare_element is not None and compare_element != 0:
            if len(old_scenario) != 0:
                raise ValueError("New scenario "+str(new_scenario)+" on top of old scenario "+old_scenario+" not supported yet.")
            else:
                delta_scenario_element = new_scenario
                delta_value_element    = old_delta_value_element + compare_element - base_element
                return_base_element    = 0
        else:
            delta_scenario_element = old_scenario
            delta_value_element    = old_delta_value_element
            return_base_element    = base_element

        return return_base_element, delta_scenario_element, delta_value_element
 
        
    def _calculate_max_length(self, data, base_scenario, compare_scenario_list, max_length=None):
        """
        Calculate the max length of the lists, unless when max_length is already provided then use that provided max_length
        """
        print("\n_Calculate_max_length\ndata:", data, "\nbase_scenario:", base_scenario, "\ncompare_scenario_list:", compare_scenario_list)
        if max_length is not None:
            # Max_length is of an other type than None
            if isinstance(max_length, int):
                # Max_length is of type integer
                if max_length > 0:
                    # Max_length has a value greater than zero
                    return max_length
                else:
                    # Max_length has a value of 0 or less
                    raise ValueError("Variable max_length has a value of 0 or lower:"+str(max_length))
            else:
                # Max_length is not of type integer
                raise TypeError("Variable max_length is not of type int, but has this value:"+str(max_length))
        else:
            # Max_length is of type None. We must calculate the max_length out of the data
            scenarios  = self._calculate_concat_scenario(base_scenario=base_scenario, compare_scenario_list=compare_scenario_list)
            print("Scenarios:", scenarios)
            max_length = self._calculate_max_length_dataset(data=data, scenarios=scenarios)
            print("max_length:", max_length)
            return max_length


    def _calculate_concat_scenario(self, base_scenario, compare_scenario_list):
        """
        Make a list of all scenario's of the parameters
        """
        scenarios = list()
        scenarios.append(base_scenario)           # Add one string value to the list
        scenarios.extend(compare_scenario_list)   # Add elements from a list to the list (and not add a list as one element to the list)
        return scenarios

    def _calculate_max_length_dataset(self, data, scenarios):
        """
        Determine the max length of the list of the scenarios
        """
        # Check type of parameters
        if not isinstance(data, dict):
            raise TypeError("Variable data is not of type dictionary, but of type:"+str(data))
        if not isinstance(scenarios, list):
            raise TypeError("Variable scenarios is not of type list, but of type:"+str(scenarios))
        
        max_length = None
        for scenario in scenarios:
            if scenario not in data.keys():
                raise ValueError("Scenario "+str(scenario)+" not in the keys of dictionary data:"+str(data.keys()))
            if max_length is None:
                max_length = len(data[scenario])
            else:
                max_length = max(max_length, len(data[scenario]))
        if max_length is None:
            raise ValueError("Could not find data to determine max_length:"+str(max_length))
        return max_length
