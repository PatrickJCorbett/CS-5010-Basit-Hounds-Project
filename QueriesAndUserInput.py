# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 13:37:19 2020

@author: pcorb
"""

#set up environment and packages
import pandas as pd
import numpy as np
from datetime import datetime as dt
from datetime import timedelta
import matplotlib.pyplot as plt


#%%

#Read in data from url and perform data cleaning
from ReadIn_EDA_Clean_Export import *

## clean dataset
input_data = excess_deaths_final


#%%
input_data = pd.read_csv('Excess Deaths Cleaned.csv')
#%%
#Read in ExcessDeathsAnalyzer class from ExcessDeathsAnalyzer.py
from ExcessDeathsAnalyzer import *


#%%Run our queries

#Query 1: National Time Series 
National = ExcessDeathsAnalyzer("United States", input_data)
National.timeSeries(save = True, filename = "testplot.png")


#%%

#Query 2: Peak date of excess deaths for national
National.peakDate()

#%%

#Query 3: Peak number of excess deaths for national
National.peakValue()

#%%

#Query 4: Virginia time series
Virginia = ExcessDeathsAnalyzer("Virginia", input_data)
Virginia.timeSeries()
Virginia.peakDate()
Virginia.peakValue()


#%%

#Query 5: Compare Virginia to New York
Virginia.compareToState("New York")


#%%
#User input section

"""
The following section defines several functions that will ask the user
for specific inputs and query our data accordingly, using the 
ExcessDeathsAnalyzer class methods.

We first define several individual functions to get specific pieces
of inputs and perform resulting queries. 

Then we define a function called user_input_activity which essentially
acts as a wrapper for the other functions we have defined. This 
function additionally utilizes a while loop that lets the user look at 
different states for as long as they want before ending the activity.
"""


    

#%%
def get_user_state():
    """
    This function will prompt the user to enter the state they are from
    which will be the first state the user gets the chance to analyze.
    The output, user_state, is used by the remaining functions.

    """
    
    #prompt the user to enter a state using the full name of the state
    user_state = input("What state are you from (enter the full name)?: ")
    #Fix the formatting so that the user doesn't get an error if they
    #forget to capitalize properly. The string.title() method takes a string
    #and puts the first letter of each word in uppercase, and the remaining
    #letters in lowercase. This way, we also account for missed capitalization
    #for states with two word names, such as New York.
    user_state = user_state.title()
    
    
    #This while loop will catch when the user enters a state value
    #that is not one of the states in the data. This prevents the activity
    #from crashing if the user makes a typo.
    while user_state not in input_data.State.unique():
        #Tell the user their entry is not a state, prompt them again,
        #and format the same way using string.title()
        user_state = input(
            "{} is not a state, please try again: ".format(user_state))
        user_state = user_state.title()
    
    #the state defined by the user is an input for other functions, so return.
    return user_state


def create_user_object(state):
    """
    This function takes a state as input and creates a
    ExcessDeathsAnalyzer object for that class.
    
    In the wrapper function, this function will be fed the output
    from get_user_state().
    
    We deliberately do not allow the user to change the input data here,
    as we leave the determination of the input data set up to the developer.
    
    """
    
    #Initialize the class object based on the state input
    user_object = ExcessDeathsAnalyzer(state, input_data)
    
    #Return this class object for querying in later functions
    return user_object

def get_user_query_choice(state):
    """
    This function will ask the user to state which query they 
    wish to perform for the state they have selected.
    We give a finite number of choices that correspond to some of the 
    methods of the ExcessDeathsAnalyzer class.
    
    """
    
    #Ask the user to specify which query they want to perform.
    user_action = input("What would you like to see for {}?"\
                        " Enter 1 for time series, 2 for peak date, 3 for"\
                        " peak value, or 4 for all three: ".format(state))
    
    #If the user enters a value outside of the choices, this while loop
    #will catch it and ask the user to correct their input, so that
    #the activity does not end in an error.
    while int(user_action) not in [1, 2, 3, 4]:
        user_action = input("Sorry, that choice is not one of the options."\
                            " Enter 1 for time series, 2 for peak date, "\
                            "3 for peak value, or 4 for all three: ")
    
    #Return the user's choice for use in querying
    return int(user_action)

def perform_user_query(user_object, query_choice):
    """
    This function actually performs the query that the user has 
    selected. 
    """
    #If user selected 1, execute the ExcessDeathsAnalyzer.timeSeries() method.
    if query_choice == 1:
        save_y_n = input("Would you like to save the output? "\
                         "Enter Y (yes) or N (no): ").upper()
        while save_y_n not in ['Y','N']:
            save_y_n = input("Invalid value. Enter Y (yes) or N (no):").upper()
        
        if save_y_n == "Y":
            user_file = input("Provide File Name For Output: ")
            user_object.timeSeries(save = True, filename = user_file)
        elif save_y_n == "N":
            user_object.timeSeries()
    #If user selected 2, execute the ExcessDeathsAnalyzer.peakDate() method
    elif query_choice == 2:
        user_object.peakDate()
    #if user selected 3, execute the ExcessDeathsAnalyzer.peakValue() method
    elif query_choice == 3:
        user_object.peakValue()
    #If user selected 4, execute all three of the above methods.
    elif query_choice == 4:
        save_y_n = input("Would you like to save the output? "\
                         "Enter Y (yes) or N (no): ").upper()
        while save_y_n not in ['Y','N']:
            save_y_n = input("Invalid value. Enter Y (yes) or N (no):").upper()
        
        if save_y_n == "Y":
            user_file = input("Provide File Name For Output: ")
            user_object.timeSeries(save = True, filename = user_file)
        elif save_y_n == "N":
            user_object.timeSeries()
        user_object.peakDate()
        user_object.peakValue()
    #The get_user_query_choice function should not allow a user to end up
    #with an invalid value. Just in case, we will raise an informative
    #error message if an invalid query option is given.
    else:
        raise ValueError("Invalid value given for query_choice. Value "\
                         "must be 1, 2, 3, or 4")


def ask_user_whether_to_compare(state):
    """
    This function asks the user whether they wish to compare 
    the state they chose to another state. This will be used
    to determine whether to perform additional querying.
    """
    
    #Ask the user to provide a response of Y or N.
    compare_y_n = input("Would you like to compare {} to another state? "\
                        "Enter Y (yes) or N (no): ".format(state)).upper()
    
    
    #If they have provided something else, prompt them to repeat until valid.
    while compare_y_n not in ['Y','N']:
        compare_y_n = input("Sorry, invalid response. Enter Y (yes)"\
                            " or N (no): ").upper()

    #Return the user's selection for further querying
    return compare_y_n

def ask_user_which_state_to_compare_to():
    """
    If the user elects to compare to another state, this function
    will ask them to specify which state
    """
    
    #Prompt the user for their comparison state, and format similar
    #to the first state
    second_state = input("Okay, which state (enter the full name)? : ")
    second_state = second_state.title()
    
    #Similar to the first state, prompt them again if entry is not a state.
    while second_state not in input_data.State.unique():
        second_state = input(
            "{} is not a state, please try again: ".format(second_state))
        second_state = second_state.title()
    
    #return the chosen state for comparison
    return second_state

def perform_user_comparison(user_object, compare_state):
    """
    This function performs the comparison between states
    that the user has specified, using the 
    ExcessDeathsAnalyzer.compareToState() method
    """
    user_object.compareToState(compare_state)
    

def ask_user_whether_to_do_another_state():
    """
    After completing the activity for the first state, this function
    will allow the user to say whether they would like to see another
    state.
    """
    check_another_state = input("Would you like to see another state? "\
                                "Enter Y (yes) or N (no): ").upper()
    
    while check_another_state not in ['Y','N']:
        check_another_state = input("Sorry, invalid response. Enter Y (yes)"\
                            " or N (no): ").upper()
    
    return check_another_state

def get_next_user_state():
    """
    This function is functionally identical to get_user_state, except
    that the prompt is no longer asking the user which state they are from,
    but rather which state they want to look at for the next round.
    """
    user_state = input("Sounds good! Which state (enter the full name)?: ")
    user_state = user_state.title()
    
    while user_state not in input_data.State.unique():
        user_state = input(
            "{} is not a state, please try again: ".format(user_state))
        user_state = user_state.title()
        
    return user_state

def user_input_activity():
    """
    This function is a wrapper for all the above functions, and comprises
    the actual user activity.
    """
    
    #A while loop is used to allow the user to keep doing the activity
    #as long as they want. We initialize a break indicator for the loop here.
    break_indicator = 0
    
    #The first time through, the user will be asked what state they are from.
    loop_ind = 1
    #We set -1 as the cardinal value for the while loop.
    while break_indicator != -1:
        if loop_ind == 1:
            user_state = get_user_state()
        else:
            user_state = get_next_user_state()
        #Initialize an ExcessDeathsAnalyzer object for the user_state
        user_info = create_user_object(user_state)
        
        #Ask the user which query they would like to perform
        user_query = get_user_query_choice(user_state)
        
        #Perform the user's selected query on the initialized class object
        perform_user_query(user_info, user_query)
        
        #Ask the user whether they wish to compare to another state.
        compare_ind = ask_user_whether_to_compare(user_state)
        
        #If the user chose to compare to another state, ask them which state,
        #then perform the compareToState query. 
        if compare_ind == "Y": 
            comparison_state = ask_user_which_state_to_compare_to()
            perform_user_comparison(user_info, comparison_state)
        
        #If the user chost not to compare to another state, move on to the 
        #next input request
        elif compare_ind == "N":
            print("Ok")
        
        #Ask the user whether they want to see another state
        another_state_ind = ask_user_whether_to_do_another_state()  
        
        #If the user does want to see another state, ask them
        #which one. In this case, the break_indicator remains equal to 0,
        #and so the while loop will begin again.
        if another_state_ind == "Y":
            loop_ind += 1
            
       
        #If fthe user does not want to see another state, thank them
        #for participating and set the break_indicator to the cardinal value,
        #ending the while loop and therefore the activity.
        elif another_state_ind == "N":
            print("Ok, thanks for checking out our analysis!")
            break_indicator = -1
            
#%%

#Execute the user activity
user_input_activity()




            
            
            
            
            
            