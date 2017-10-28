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
class Person:
    
    def __init__(self, sickness_status):
        self.sickness_status = sickness_status


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
        self.people_list = []
        for i in range(0, sick_people_count):
            self.people_list.append(Person(True))
            
        for i in range(0, self.healthy_people_count):
            self.people_list.append(Person(False))
            
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
    
    def __eq__(self, state2):
        if (self.population_count == state2.population_count and 
        self.sick_people_count == state2.sick_people_count and
        self.death_count == state2.death_count and
        self.birth_count == state2.birth_count and
        self.healthy_people_count == state2.healthy_people_count):
            return True
        
        return False
    
    def can_move(self):
        '''This tests whether the move is legal.
            A move is legal as long as the count of healthy
            people is greater than 0.
        '''
        if self.healthy_people_count > 0:
            return True
        return False

    # habits is essentially a tuple containing boolean 
    # variables to indicate whether a person washes hands and
    # sleeps well.
    def move(self, habits):
        '''This computes a new state resulting from a legal move.'''
        wash_hands = habits[0]
        sleep_well = habits[1]
        for person in self.people_list:
            if person.sickness_status:
                print('Person is sick')
            else:
                print('Person is healthy')
        return new_state     

# </COMMON_CODE>