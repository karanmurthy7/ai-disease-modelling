'''Eradicate_Cold.py
Karan Murthy, CSE 415, Autumn 2017, University of Washington
UWNetID: karan7
Vaibhavi Rangarajan, CSE 415, Autumn 2017, University of Washington
UWNetID: vaibhavi
Instructor:  S. Tanimoto.
'''

# <METADATA>
QUIET_VERSION = "0.1"
PROBLEM_NAME = "Eradicate Cold"
PROBLEM_VERSION = "0.1"
PROBLEM_AUTHORS = ['K. Murthy', 'V. Rangarajan']
PROBLEM_CREATION_DATE = "28-OCT-2017"
PROBLEM_DESC = \
'''This formulation of the Eraticate_Cold uses generic
Python 3 constructs and has been tested with Python 3.6.
This is a model that aims to eradicate cold from the world.
'''
# </METADATA>

# <COMMON_CODE>

# This class PopulationState holds metrics such as  
# population count, count of sick people, count of healthy people,
# count of people born at the end of every week, and count of 
# people who die after every week.
class PopulationState:
    
    def __init__(self, population_count, sick_people_count, death_count, birth_count):
        self.population_count = population_count
        self.sick_people_count = sick_people_count
        self.death_count = death_count
        self.birth_count = birth_count
        self.healthy_people_count = population_count - sick_people_count
        
    def __hash__(self):
        return (self.__str__()).__hash__()
    
    def calc_percentage(num, total):
        return str((num / total) * 100)
    
    def __str__(self):
        # Produces a textual description of a state.
        text = "Population Count = " + str(self.population_count) + "\n"
        text += "Sick People Count / Percentage = " 
        + str(self.sick_people_count) + " / " 
        + calc_percentage(self.sick_people_count, self.population_count) + "%\n"
        text += "Healthy People Count / Percentage = " 
        + str(self.healthy_people_count) + " / " 
        + calc_percentage(self.healthy_people_count, self.population_count) + "%\n"
        return text    

# </COMMON_CODE>