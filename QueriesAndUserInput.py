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
#Read in cleaned data
excess_deaths_final = pd.read_csv('Excess Deaths Cleaned.csv')


#%%
#Read in ExcessDeathsAnalyzer class from ExcessDeathsAnalyzer.py
from ExcessDeathsAnalyzer import *


#%%Run our queries

#Query 1: National Time Series 
National = ExcessDeathsAnalyzer("United States")
National.timeSeries()

#%%
#Query 2: Peak date of excess deaths for national
National.peakDate()

#%%
#Query 3: Virginia time series
Virginia = ExcessDeathsAnalyzer("Virginia")
Virginia.timeSeries()


#%%
#Query 4: Compare Virginia to New York
Virginia.compare_to_state("New York Total")
#TODO: add an if statement in the class so if user enters "New York" 
#instead of "New York Total" it still works


#%%
#User input section

#Ask user what state they are from
user_state = input("What state are you from (enter the full name)?: ")
user_info = ExcessDeathsAnalyzer(user_state)

user_action = input("What would you like to see for {}? Enter 1 for time series, 2 for peak date, or 3 for both: ".format(user_state))

if int(user_action) == 1:
    print(user_info.timeSeries())
elif int(user_action) == 2:
    user_info.peakDate()
elif int(user_action) == 3:
    user_info.timeSeries()
    user_info.peakDate()
    
compare_y_n = input("Would you like to compare {} to another state? Enter Y (yes) or N (no): ".format(user_state))

if compare_y_n == "Y":
    second_state = input("Okay. which State (enter the full name)? : ")
    user_info.compare_to_state(second_state)
elif compare_y_n == "N":
    print("Okay.")


#After they look at their state, give the user the chance to keep looking at other states
break_indicator = 0

while break_indicator != -1:
    check_another_state = input("Would you like to see another state? Enter Y (yes) or N (no): ")
    if check_another_state == "N":
        print("Okay, thanks for checking out our analysis!")
        break_indicator = -1
    elif check_another_state == "Y":
        user_state = input("Sounds good! Which state would you like to see (enter the full name): ")
        user_info = ExcessDeathsAnalyzer(user_state)

        user_action = input("What would you like to see for {}? Enter 1 for time series, 2 for peak date, or 3 for both: ".format(user_state))
        
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
            user_info.compare_to_state(second_state)
        elif compare_y_n == "N":
            print("Okay.")