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
#read in data
excess_deaths_final = pd.read_csv('Excess Deaths Cleaned.csv')

#%%
#Define ExcessDeathsAnalyzer class

class ExcessDeathsAnalyzer:
    
    def __init__(self, state, full_data):
        """
        

        Parameters
        ----------
        state : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        Object of this class is initialized with two arguments, the state and
        the dataset to be used.
        
        (The dataset can be generated using the ReadIn_EDA_Clean_Export module)
        
        The initializer defines the state attribute and the data subsets
        for the state.
        
        """
        self.state = state
        self.full_data = full_data
        
        #self.data is the full subset of data for the specified state
        self.data = self.full_data[self.full_data['State'] == self.state]               
        
        #convert date to a datetime
        pd.to_datetime(self.data.loc[:,'Week Ending Date']) 
        
        #self.data_allCauses keeps only the rows for 'All causes'
        self.data_allCauses = self.data[self.data['Outcome'] == 'All causes']
        
        #self.data_exceptCovid keeps only the rows 
        #for 'All causes, excluding COVID-19'
        self.data_exceptCovid = self.data[self.data['Outcome'] == 'All causes,'\
                                          ' excluding COVID-19']
        
        
        
        
        
    def timeSeries(self, save = False, filename = None):
        """
        Run this method to return the time series of excess deaths
        for the state. The time series will show the range between
        the average estimate and the upper bound, for excess deaths
        with and without COVID-19 included.

        """
        all_x = self.data_allCauses['Week Ending Date']
        all_higher = self.data_allCauses['Excess Higher Estimate']
        all_lower = self.data_allCauses['Excess Lower Estimate']
        
        excCOVID_x = self.data_exceptCovid['Week Ending Date']
        excCOVID_higher = self.data_exceptCovid['Excess Higher Estimate']
        excCOVID_lower = self.data_exceptCovid['Excess Lower Estimate']
        
        plt.plot(all_x, all_higher, color = 'navy', 
                 label = "Higher Estimate, All Causes")
        plt.plot(all_x, all_lower, color = 'blue',
                 label = "Lower Estimate, All Causes")
        plt.fill_between(all_x, all_lower, all_higher, color = 'lightskyblue')
        
        plt.plot(excCOVID_x, excCOVID_higher, color  = 'darkgreen', 
                 label = "Higher Estimate, Excluding COVID-19")
        plt.plot(excCOVID_x, excCOVID_lower, color = 'mediumseagreen', 
                 label = "Lower Estimate, Excluding COVID-19")
        plt.fill_between(excCOVID_x, excCOVID_lower, excCOVID_higher, 
                         color = 'lightgreen', alpha = 0.5)
        plt.legend(loc = 'upper left', fontsize = 8)
        plt.ylabel("Excess Deaths")
        plt.title("Excess Deaths with and without COVID-19- {}".format(self.state))
        
        if save == True:
            plt.savefig(filename, bbox_inches = 'tight')
            
        plt.show()
        
        
        
    def peakDate(self):
        """
        Run this method to print out the date at which the state saw its
        peak of excess deaths. Peak date is returned both with and without
        COVID-19 included
        
        """
        

        max_date_all = self.data_allCauses.iloc[
            self.data_allCauses['Excess Higher Estimate'].argmax()]\
            ['Week Ending Date']
        
        max_date_all_print = max_date_all.date()
        
        max_excess_all = self.data_allCauses.iloc[
            self.data_allCauses['Excess Higher Estimate'].argmax()]\
            ['Excess Higher Estimate']
        
        print("National peak of Excess Deaths, all causes, for {} was on {}"\
              " at {} excess deaths".format(self.state, max_date_all_print, 
                                            int(max_excess_all)))
        
        max_date_except_COVID = self.data_exceptCovid.iloc[
            self.data_exceptCovid['Excess Higher Estimate'].argmax()]['Week Ending Date']
        
        
        max_date_except_COVID_print = max_date_except_COVID.date()
        
        max_excess_except_COVID = self.data_exceptCovid.iloc[
            self.data_exceptCovid['Excess Higher Estimate'].argmax()]\
            ['Excess Higher Estimate']
            
        print("National peak of Excess Deaths, all causes except for COVID-19"\
              ", for {} was on {}"\
              " at {} excess deaths".format(self.state,
                                            max_date_except_COVID_print,
                                            int(max_excess_except_COVID)))
      
        # def peakValue(self):
        #    """
        #    Run this method to print out the date at which the state saw its
        #    peak of excess deaths. Peak date is returned both with and without
        #    COVID-19 included
        
        #    """
            
        
        #    max_excess_all = self.data_allCauses.iloc[
        #        self.data_allCauses['Excess Higher Estimate'].argmax()]\
        #        ['Excess Higher Estimate']
        
        #    print("National peak of Excess Deaths, all causes, for {} was"\
        #          " at {} excess deaths".format(self.state, max_date_all_print, 
        #                                        int(max_excess_all)))
        
        
        
        #    max_excess_except_COVID = self.data_exceptCovid.iloc[
        #        self.data_exceptCovid['Excess Higher Estimate'].argmax()]\
        #        ['Excess Higher Estimate']
            
        #    print("National peak of Excess Deaths, all causes except for COVID-19"\
        #          ", for {} was"\
        #          " at {} excess deaths".format(self.state, 
        #                                        int(max_excess_except_COVID)))
            
    def compareToState(self, compare_state):
        """
        

        Parameters
        ----------
        compare_state : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        This method will take from the user as input a second state that 
        the defined object's state will be compared to. This will return
        plots showing the higher estimate of excess deaths for both states
        as well as the difference between the two. These charts are returned
        for excess deaths both with and without COVID-19
        """
        state1 = self.state
        state2 = compare_state
        
        data_1 = self.data
        data_2 = self.full_data[self.full_data['State'] == state2]
        data_2['Week Ending Date'] = pd.to_datetime(data_2['Week Ending Date'])
        
        x = self.data['Week Ending Date'].unique()
        all_1 = self.data_allCauses['Excess Higher Estimate'].reset_index(drop = True)
        all_2 = data_2[data_2['Outcome'] == 'All causes']['Excess Higher Estimate'].reset_index(drop = True)
        
        nocovid_1 = self.data_exceptCovid['Excess Higher Estimate'].reset_index(drop = True)
        nocovid_2 = data_2[data_2['Outcome'] == 'All causes, excluding COVID-19']['Excess Higher Estimate'].reset_index(drop = True)
        
        
        difference_all = all_1 - all_2
        difference_nocovid = nocovid_1 - nocovid_2
        
        
        fig, a = plt.subplots(2, 2, figsize = (20,10))
        
        a[0,0].plot(x, all_1, label = "Excess Deaths, All Causes- {}".format(state1))
        a[0,0].plot(x, all_2, label = "Excess Deaths, All Causes- {}".format(state2))
        a[0,0].legend(loc = "upper left", fontsize = 8)
        a[0,0].set_ylabel("Higher Estimate of Excess Deaths")
        a[0,0].set_title('Time Series of Excess Deaths, All Causes, Between {} and {}'.format(state1, state2))
        
        a[0,1].plot(x, difference_all)
        a[0,1].set_ylabel("Estimate ({}) - Estimate ({})".format(state1, state2))
        a[0,1].set_title("Difference in Excess Deaths, All Causes, Between {} and {}".format(state1, state2))
        
        a[1,0].plot(x, nocovid_1, label = "Excess Deaths, All Causes Except COVID-19- {}".format(state1))
        a[1,0].plot(x, nocovid_2, label = "Excess Deaths, All Causes Except COVID-19- {}".format(state2))
        a[1,0].legend(loc = "upper left", fontsize = 8)
        a[1,0].set_ylabel("Higher Estimate of Excess Deaths")
        a[1,0].set_title('Time Series of Excess Deaths, All Causes except COVID-19, Between {} and {}'.format(state1, state2))
        
        a[1,1].plot(x, difference_nocovid)
        a[1,1].set_ylabel("Estimate ({}) - Estimate ({})".format(state1, state2))
        a[1,1].set_title("Difference in Excess Deaths, All Causes Except COVID-19, Between {} and {}".format(state1, state2))
        plt.show()
        