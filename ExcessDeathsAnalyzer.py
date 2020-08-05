# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 13:31:10 2020

@author: pcorb
"""

import pandas as pd
import numpy as np
from datetime import datetime as dt
from datetime import timedelta
import matplotlib.pyplot as plt


#%%
#Define ExcessDeathsAnalyzer class

class ExcessDeathsAnalyzer:
    
    def __init__(self, state, full_data):
        """
        This method is the constructor.  The object is initialized with the 
        state that the user chose to analyze and the dataset that contains 
        the excess death statistics per state and nationally.  The full dataset
        of all states is stored as "full_data." The constructor also creates 
        3 different subsets of the dataset:
            
            1. the subset of data for the state only, stored as "data"
            
            2. the subset of data for the state including the statistics 
            associated with deaths due to all causes, stored as "data_allCauses"
            
            3. the subset of data for the state including the statistics 
            associated with deaths due to all causes EXCEPT deaths caused
            by COVID-19, stored as "data_exceptCovid"
        
        """
        ## state chosen by the user to analyze
        self.state = state 

        self.state = state
        self.full_data = full_data
        
        #self.data is the full subset of data for the specified state
        self.data = self.full_data[self.full_data['State'] == self.state]               
        
        #convert date to a datetime
        week_todate = pd.to_datetime(self.data.loc[:,'Week Ending Date'].copy())
        self.data.loc[:, "Week Ending Date"] = week_todate
        
        #self.data_allCauses keeps only the rows for 'All causes'
        self.data_allCauses = self.data[self.data['Outcome'] == 'All causes']
        
        #self.data_exceptCovid keeps only the rows 
        #for 'All causes, excluding COVID-19'
        self.data_exceptCovid = self.data[self.data['Outcome'] == 'All causes,'\
                                          ' excluding COVID-19']

        
        
    def timeSeries(self, save = False, filename = None):
        """
        When the user runs this method, the user specifies whether they would
        like the output (the timeseries plot) to be saved in a file. If so, 
        they pass "save = True" and the name of the file. Otherwise, the plot
        is simply displayed in the console and not saved in a separate file.
        
        Run this method to build the time series plot of excess deaths
        for the state. The time series will show the range between
        the average estimate and the upper bound for excess deaths
        with and without COVID-19 included. The method will automatically
        display the plot before ending.

        """
        
        #### Isolate variables for plot ####
        ## x-axis of dates for all-causes
        all_x = self.data_allCauses['Week Ending Date']
        
        ## all-causes upper bound
        all_higher = self.data_allCauses['Excess Higher Estimate']
        
        ## all-causes lower bound
        all_lower = self.data_allCauses['Excess Lower Estimate']
        
        ## x-axis of dates for excess deaths not including COVID-19 deaths
        excCOVID_x = self.data_exceptCovid['Week Ending Date']
        
        ## deaths w/o COVID-19 upper bound
        excCOVID_higher = self.data_exceptCovid['Excess Higher Estimate']
        
        ## deaths w/o COVID-19 lower bound
        excCOVID_lower = self.data_exceptCovid['Excess Lower Estimate']
        
        
        #### Create plot ####
        ## plot upper bound, lower bound and interval for all-causes
        plt.plot(all_x, all_higher, color = 'navy', 
                 label = "Higher Estimate, All Causes")
        plt.plot(all_x, all_lower, color = 'blue',
                 label = "Lower Estimate, All Causes")
        plt.fill_between(all_x, all_lower, all_higher, color = 'lightskyblue')
        
        ## plot upper bound, lower bound and interval for deaths w/o COVID-19
        plt.plot(excCOVID_x, excCOVID_higher, color  = 'darkgreen', 
                 label = "Higher Estimate, Excluding COVID-19")
        plt.plot(excCOVID_x, excCOVID_lower, color = 'mediumseagreen', 
                 label = "Lower Estimate, Excluding COVID-19")
        plt.fill_between(excCOVID_x, excCOVID_lower, excCOVID_higher, 
                         color = 'lightgreen', alpha = 0.5)
        
        ## label legend and axes
        plt.legend(loc = 'upper left', fontsize = 8)
        plt.ylabel("Excess Deaths")
        plt.title("Excess Deaths with and without COVID-19- {}".format(self.state))
        
        ## save the plot in a file if the user chose to do so
        if save == True:
            plt.savefig(filename, bbox_inches = 'tight')
            
        ## display the plot    
        plt.show()   
        
        
    def peakDate(self):
        """
        Run this method to print out the date at which the state saw its
        peak of excess deaths. Peak date is displayed twice: once with and 
        once without COVID-19 deaths included.
        Method takes no arguments (it operates on the initialized attributes) 
        and returns nothing (it prints statements).
        
        """
        
        #### All causes of death, including COVID-19 ####
        ## find the maximum Excess Deaths - Higher Bound Estimate value
        ## for this state and store the corresponding Week Ending Date
        ## all causes included - COVID-19 and other causes of death
        max_date_all = self.data_allCauses.iloc[
            self.data_allCauses['Excess Higher Estimate'].argmax()]\
            ['Week Ending Date']
        
        max_date_all_print = max_date_all.date() ## printable version
        
     
        
        output_1 = ("The peak of Excess Deaths, all causes, for {} was "\
              "on {}. ".format(self.state, max_date_all_print))
        
            
        #### Without COVID-19 Deaths ####
        ## find the maximum Excess Deaths - Higher Bound Estimate value
        ## for this state and store the corresponding Week Ending Date
        ## no COVID-19 deaths included; only other causes of death    
        max_date_except_COVID = self.data_exceptCovid.iloc[
            self.data_exceptCovid['Excess Higher Estimate'].argmax()]['Week Ending Date']
        
        
        max_date_except_COVID_print = max_date_except_COVID.date() ## printable
        
            
        output_2 = ("The peak of Excess Deaths, all causes except for COVID-19"\
              ", for {} was on {}".format(self.state,
                                            max_date_except_COVID_print))
        print(output_1)
        print(output_2)
        return(output_1 + output_2)
        
    def peakValue(self):
        """
        Run this method to print out the state's peak of excess deaths. 
        Peak is displayed twice: once with and once without COVID-19 deaths 
        in the excess deaths count.
        Method takes no arguments (it operates on the initialized attributes) 
        and returns nothing (it prints statements).
        """
        
        #### All causes of death, including COVID-19 ####
        ## find the maximum Excess Deaths - Higher Bound Estimate value
        ## for this state and store that value (excess deaths w/ COVID-19)
        max_excess_all = self.data_allCauses.iloc[
            self.data_allCauses['Excess Higher Estimate'].argmax()]\
            ['Excess Higher Estimate']
    
        output_1 = ("The peak of Excess Deaths, all causes, for {} was"\
              " at {} excess deaths".format(self.state, int(max_excess_all)))
            
    
        #### Without COVID-19 Deaths ####
        ## find the maximum Excess Deaths - Higher Bound Estimate value
        ## for this state and store that value (excess deaths w/o COVID-19)
        max_excess_except_COVID = self.data_exceptCovid.iloc[
            self.data_exceptCovid['Excess Higher Estimate'].argmax()]\
            ['Excess Higher Estimate']
        
        output_2 = ("The peak of Excess Deaths, all causes except for COVID-19"\
              ", for {} was"\
              " at {} excess deaths".format(self.state, 
                                            int(max_excess_except_COVID)))
        
        print(output_1)
        print(output_2)
        return(output_1 + output_2)
            
    def compareToState(self, compare_state):
        """
        This method will take from the user as input a second state that 
        the defined object's state will be compared to. The method builds
        plots showing the higher estimate of excess deaths for both states
        as well as the difference between the two. These charts display
        excess deaths comparisons both with and without COVID-19 included 
        in the excess deaths count.
        """
        #### Dataset creation for plots ####
        ## create 2 variables for the states being compared
        state1 = self.state
        state2 = compare_state
        
        ## create 2 datasets with all the data from the 2 states being compared 
        data_1 = self.data
        data_2 = self.full_data[self.full_data['State'] == state2]
        week_todate = pd.to_datetime(data_2.loc[:,'Week Ending Date'].copy())
        data_2.loc[:, "Week Ending Date"] = week_todate
        
        ## x-axis of dates for time-series comparisions
        x = self.data['Week Ending Date'].unique() ## x-axis of dates
        
        ## create a subset of excess deaths due to all causes per state
        all_1 = self.data_allCauses['Excess Higher Estimate'].reset_index(drop = True)
        all_2 = data_2[data_2['Outcome'] == 'All causes']['Excess Higher Estimate'].reset_index(drop = True)
        
        ## create a subset of excess deaths w/o COVID-19 deaths per state
        nocovid_1 = self.data_exceptCovid['Excess Higher Estimate'].reset_index(drop = True)
        nocovid_2 = data_2[data_2['Outcome'] == 'All causes, excluding COVID-19']['Excess Higher Estimate'].reset_index(drop = True)
        
        ## create a dataset that represents the difference between the 2 states
        ## for both all-causes excess deaths and excess deaths excluding COVID
        difference_all = all_1 - all_2
        difference_nocovid = nocovid_1 - nocovid_2
        
        
        #### Create the plots ####
        ## create 4 plots to compare the 2 states
        fig, a = plt.subplots(2, 2, figsize = (20,10)) ## sized for easy view
        
        ## plot 1 - comparing excess deaths due to all causes
        a[0,0].plot(x, all_1, label = "Excess Deaths, All Causes- {}".format(state1))
        a[0,0].plot(x, all_2, label = "Excess Deaths, All Causes- {}".format(state2))
        a[0,0].legend(loc = "upper left", fontsize = 8)
        a[0,0].set_ylabel("Higher Estimate of Excess Deaths")
        a[0,0].set_title('Time Series of Excess Deaths, All Causes, Between {} and {}'.format(state1, state2))
        
        ## plot 2 - calculating and displaying the differences in excess deaths
        ## due to all causes over time between the 2 states
        a[0,1].plot(x, difference_all)
        a[0,1].set_ylabel("Estimate ({}) - Estimate ({})".format(state1, state2))
        a[0,1].set_title("Difference in Excess Deaths, All Causes, Between {} and {}".format(state1, state2))
        
        ## plot 3 - comparing excess deaths excluding COVID-19 deaths
        a[1,0].plot(x, nocovid_1, label = "Excess Deaths, All Causes Except COVID-19- {}".format(state1))
        a[1,0].plot(x, nocovid_2, label = "Excess Deaths, All Causes Except COVID-19- {}".format(state2))
        a[1,0].legend(loc = "upper left", fontsize = 8)
        a[1,0].set_ylabel("Higher Estimate of Excess Deaths")
        a[1,0].set_title('Time Series of Excess Deaths, All Causes except COVID-19, Between {} and {}'.format(state1, state2))
        
        ## plot 4 - calculating and displaying the differences in excess deaths
        ## excluding COVID-19 deaths over time between the 2 states
        a[1,1].plot(x, difference_nocovid)
        a[1,1].set_ylabel("Estimate ({}) - Estimate ({})".format(state1, state2))
        a[1,1].set_title("Difference in Excess Deaths, All Causes Except COVID-19, Between {} and {}".format(state1, state2))
        
        ## display all 4 plots
        plt.show()
        