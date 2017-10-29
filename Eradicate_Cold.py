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
import random
# <COMMON_CODE>
# The probability of a person getting sick is % on an average.
BASE_RISK_FACTOR = 0.5

# EFFECT_WASHING_HANDS means that washing hands can reduce the probability of 
# a person getting sick by 10%.
EFFECT_WASHING_HANDS = 0.1

# EFFECT_SLEEPING_WELL means that sleeping well can reduce the probability of 
# a person getting sick by 5%.
EFFECT_SLEEPING_WELL = 0.05

#
RECOVERY_THRESHOLD = 0.80

#
YEARLY_POPULATION_GROWTH_RATE = 0.012
NUMBER_OF_YEARS = 10
POPULATION_GROWTH_RATE = math.floor(math.exp(YEARLY_POPULATION_GROWTH_RATE * NUMBER_OF_YEARS))
#
MORTALITY_RATE = 0.0095

class Person:
    def __init__(self, is_sick):
        self.is_sick = is_sick

# This class PopulationState holds metrics such as  
# population count, count of sick people, count of healthy people,
# count of people born at the end of every week, and count of 
# people who die after every week.
class PopulationState:
    
    def __init__(self, population_count, sick_people_count):
        self.population_count = population_count
        self.sick_people_count = sick_people_count
        self.healthy_people_count = population_count - sick_people_count
        self.people_list = self.build_people_list()

    def build_people_list(self):
        people_list = []
        for i in range(0, self.sick_people_count):
            people_list.append(Person(True))

        for i in range(0, self.healthy_people_count):
            people_list.append(Person(False))

        return people_list

    def adjust_population(self, sick_count, healthy_count):
        # Re-initializing sick people count to get the updated count
        # of sick and healthy people

        self.population_count = sick_count + healthy_count
        self.sick_people_count = sick_count
        self.healthy_people_count = healthy_count
        self.people_list = self.build_people_list()

    def __hash__(self):
        return (self.__str__()).__hash__()
    
    def calc_percentage(self, num, total):
        return (num / total) * 100

    def get_sick_percent(self):
        return self.calc_percentage(self.sick_people_count, self.population_count)

    def get_healthy_percent(self):
        return self.calc_percentage(self.healthy_people_count, self.population_count)

    def __str__(self):
        # Produces a textual description of a state.

        text = "Population Count = " + str(self.population_count)

        text += "\nSick People Count / Percentage = " +\
                str(self.sick_people_count) + " / " +\
                str(self.calc_percentage(self.sick_people_count, self.population_count))

        text += "\nHealthy People Count / Percentage = " +\
                str(self.healthy_people_count) + " / " +\
                str(self.calc_percentage(self.healthy_people_count, self.population_count))
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

        new_state = self.copy()
        #Assume that these habits are prevalent across the whole world
        wash_hands = habits[0]
        sleep_well = habits[1]

        #Common Risk Factor based on global habits
        risk_factor = BASE_RISK_FACTOR + (EFFECT_WASHING_HANDS * wash_hands) \
                      + (EFFECT_SLEEPING_WELL * sleep_well)


        #PART 0: Keep track of sick and healthy count before any process
        new_sick_count = new_state.sick_people_count
        new_healthy_count = new_state.healthy_people_count


        #PART 1 : Some sick people recover
        # Code that assumes that half of the sick people
        # recover at the end of every week. This is randomized
        # to ensure that a particular pattern is not followed everytime.
        recovered_count = math.ceil(new_state.sick_people_count/2)

        #Update sick and healthy counts due to Recovery
        new_sick_count -= recovered_count
        new_healthy_count +=recovered_count

        #PART 2 : Some healthy people get infected
        infected_count = 0
        for i in range(0, new_state.healthy_people_count):
                #Assume People have 21 interactions a week, with standard deviation 6
                num_interactions = math.floor(random.gauss(21,6))
                sick_percent = new_state.get_sick_percent()
                sick_interactions = math.floor(num_interactions*sick_percent)

                recovery_probability = 1 - risk_factor ** sick_interactions
                if recovery_probability < RECOVERY_THRESHOLD:
                    # Classify the person as sick if his/her
                    # recovery probability is less than the threshold.
                    infected_count+=1

        #Update sick and healthy counts due to Infection
        new_sick_count += infected_count
        new_healthy_count -= recovered_count


        #PART 3 : Some people die (Healthy or sick, doesn't matter)
        death_count = math.ceil(new_state.population_count * MORTALITY_RATE) #CEIL instead of Floor, so that minimum 1 person dies
        who_dies = set()
        sick_died =0
        healthy_died =0
        while(len(who_dies) < death_count):
            index = random.randint(0, new_state.population_count-1)   # if no -1, index out of bounds
            if who_dies.__contains__(index) ==False:
                if new_state.people_list[index] ==True:
                    sick_died+=1
                else: healthy_died +=1
                who_dies.add(index)

        # Update sick and healthy counts due to Death
        new_sick_count -= sick_died
        new_healthy_count -= healthy_died


        #PART 4 : Some healthy people are born
        birth_count = math.ceil(new_state.population_count * YEARLY_POPULATION_GROWTH_RATE)

        # Update healthy counts due to Birth
        new_healthy_count += birth_count


        # PART 5 : Reset New State's Healthy count, Sick count, population, and people list based on recovery, infection, birth and death
        new_state.adjust_population(new_sick_count, new_healthy_count)

        return new_state

    def delete_list_elements(self, index_list):
        index_list = set(index_list)
        result = [value for index, value in enumerate(self.people_list) if index not in index_list]
        return result



def goal_test(s):
    '''If More than 99% of the population is affected'''
    sick_percent = s.calc_percentage(s.sick_people_count,s.population_count)
    if float(sick_percent) > 99 or float(sick_percent) < 1:
        return True
    else:
        return False


def goal_message(s):
    return "The World Has Changed Forever!"

class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)


# </COMMON_CODE>


# <COMMON_DATA>
# </COMMON_DATA>

# <INITIAL_STATE>
DEFAULT_POPULATION = 3
DEFAULT_SICK_COUNT = 1
CREATE_INITIAL_STATE = lambda : PopulationState(DEFAULT_POPULATION, DEFAULT_SICK_COUNT)
# </INITIAL_STATE>

# <OPERATORS>
HABITS = [(1,1), (1,-1), (-1,1), (-1,-1)]
OPERATORS = [Operator("WASH HANDS? " + str(wash) + " \nSLEEP WELL?" + str(sleep),
                      lambda s: s.can_move(),
                      lambda s, h = (wash, sleep): s.move(h))
             for (wash, sleep) in HABITS]
# </OPERATORS>

# <GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
# </GOAL_TEST>

# <GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
# </GOAL_MESSAGE_FUNCTION>