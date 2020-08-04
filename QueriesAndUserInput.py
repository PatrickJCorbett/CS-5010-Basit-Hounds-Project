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


#%%

#Query 5: Compare Virginia to New York
Virginia.compareToState("New York")


#%%
#User input section

#Ask user what state they are from
user_state = input("What state are you from (enter the full name)?: ")

######### TODO: ERROR CHECKING FOR STATE NAME

user_info = ExcessDeathsAnalyzer(user_state, input_data)

user_action = input("What would you like to see for {}? Enter 1 for time series, 2 for peak date, or 3 for both: ".format(user_state))
while user_action not in['1','2','3']:
    user_action = input("Invalid value. Please give a value of 1 for time series, 2 for peak date, or 3 for both: ")

if int(user_action) == 1:
    (user_info.timeSeries())
elif int(user_action) == 2:
    user_info.peakDate()
elif int(user_action) == 3:
    user_info.timeSeries()
    user_info.peakDate()
    
compare_y_n = input("Would you like to compare {} to another state? Enter Y (yes) or N (no): ".format(user_state))

if compare_y_n == "Y":
    second_state = input("Okay. which State (enter the full name)? : ")
    user_info.compareToState(second_state)
elif compare_y_n == "N":
    print("Okay.")

##### TODO: PRINT ERROR MESSAGE IF SOMETHING OTHER THAN Y OR N IS ENTERED


#After they look at their state, give the user the chance to keep looking at other states
break_indicator = 0


while break_indicator != -1:
    check_another_state = input("Would you like to see another state? Enter Y (yes) or N (no): ")
    if check_another_state == "N":
        print("Okay, thanks for checking out our analysis!")
        break_indicator = -1
    elif check_another_state == "Y":
        user_state = input("Sounds good! Which state would you like to see (enter the full name): ")
        
        ###### TODO: CHECK IF STATE NOT IN DATASET
        
        user_info = ExcessDeathsAnalyzer(user_state, input_data)

        user_action = input("What would you like to see for {}? Enter 1 for time series, 2 for peak date, or 3 for both: ".format(user_state))
        while user_action not in['1','2','3']:
            user_action = input("Invalid value. Please give a value of 1 for time series, 2 for peak date, or 3 for both: ")
        
        if int(user_action) == 1:
            user_info.timeSeries()
        elif int(user_action) == 2:
            user_info.peakDate()
        elif int(user_action) == 3:
            user_info.timeSeries()
            user_info.peakDate()
            
        compare_y_n = input("Would you like to compare {} to another state? Enter Y (yes) or N (no): ".format(user_state))
        
        if compare_y_n == "Y":
            second_state = input("Okay. which State (enter the full name)? : ")
            user_info.compareToState(second_state)
        elif compare_y_n == "N":
            print("Okay.")
            
            
            
            
            
            
            
            
            