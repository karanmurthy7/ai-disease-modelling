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

import math
# <COMMON_CODE>
# The probability of a person getting sick is 50% on an average.
BASE_RISK_FACTOR = 0.5

# EFFECT_WASHING_HANDS means that washing hands can reduce the probability of 
# a person getting sick by 10%.
EFFECT_WASHING_HANDS = 0.1

# EFFECT_SLEEPING_WELL means that sleeping well can reduce the probability of 
# a person getting sick by 5%.
EFFECT_SLEEPING_WELL = 0.05

RECOVERY_THRESHOLD = 0.80
YEARLY_POPULATION_GROWTH_RATE = 0.012
NUMBER_OF_YEARS = 10
POPULATION_GROWTH_RATE = math.exp(YEARLY_POPULATION_GROWTH_RATE * NUMBER_OF_YEARS)
MORTALITY_RATE = 0.0095
class Person:
    
    def __init__(self, sickness_status):
        self.sickness_status = sickness_status


# This class PopulationState holds metrics such as  
# population count, count of sick people, count of healthy people,
# count of people born at the end of every week, and count of 
# people who die after every week.
class PopulationState:
    
    def __init__(self, population_count, sick_people_count):
        self.population_count = population_count
        self.sick_people_count = sick_people_count
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
    
    def copy(self):
        # Used to construct deep copies
        new_state = PopulationState(self.population_count, 
                                    self.sick_people_count)
        return new_state
    
    # habits is essentially a tuple containing variables (1,-1)
    # to indicate whether a person washes hands and sleeps well.
    # For instance, 1 = Washes Hands, -1 = Does not wash hands
    def move(self, habits):
        '''This computes a new state resulting from a legal move.'''
        wash_hands = habits[0]
        sleep_well = habits[1]
        risk_factor = BASE_RISK_FACTOR + EFFECT_WASHING_HANDS * wash_hands 
        + EFFECT_SLEEPING_WELL * sleep_well
        sick_people_count = 0
        healthy_people_count = 0
        diagnosed_people_count = 0
        
        for i in range(0, len(self.people_list)):
            if self.people_list[i].sickness_status:
                print('Person is sick')
                sick_people_count += 1
            else:
                print('Person is healthy')
                sick_interactions = random.randint(1, 10)
                recovery_probability = 1 - risk_factor ** sick_interactions
                if sickness_probability > RECOVERY_THRESHOLD:
                    healthy_people_count += 1
                else:
                    diagnosed_people_count += 1
                
        # Code that assumes that half of the sick people
        # recover at the end of every week.
        recovered_people_count = math.floor(sick_people_count/2)
        sick_people_count -= recovered_people_count
        healthy_people_count += recovered_people_count
        population_count = healthy_people_count + sick_people_count
        population_count -= math.floor(population_count * MORTALITY_RATE)
        new_state = self.copy()
        new_state.sick_people_count = sick_people_count
        new_state.population_count = math.floor(population_count * POPULATION_GROWTH_RATE)
        return new_state     

# </COMMON_CODE>
