# -*- coding: utf-8 -*-
"""
This testing suite will contain unit tests for each method defined in the
ExcessDeathsAnalyzer class. Each method tested will have its own test class.
    (1) __int__
    (2) timeSeries
    (3) peakDate
    (4) peakValues
    (5) compareToState
    
"""
#Import libraries and modules and test data

import unittest
import os
import pandas as pd
import ExcessDeathsAnalyzer as eda

#Test Data 1 contains two states' data for three weeks in March 2020
#Test Data 2 contains only one state's data for three weeks in March 2020
test_data1 = pd.read_csv('TestData1_Excess Deaths Cleaned.csv') 
test_data2 = test_data1[test_data1['State']=='Michigan']

#Convert 'Week Ending Date' series/column into datetime objects
pd.to_datetime(test_data2.loc[:,'Week Ending Date']) 


class ExcessDeathsAnalyzer_init_TestCase(unittest.TestCase):
    #Unit testing the creation of ExcessDeathsAnalyzer objects
    
    #the following methods all test whether objects' attirbutes are created 
    #correctly when passed all kwargs:
    def test_is_init_state_working_correctly(self):
        #Check that the state attribute was set correctly
        
        #setup
        #create object with state 'Michigan' and full data from 
        #imported CSV (above)
        analyzer1 = eda.ExcessDeathsAnalyzer('Michigan', test_data1) 
        
        #check
        self.assertEqual(analyzer1.state, 'Michigan')
     
    def test_is_init_full_data_working_correctly(self):
        #Check that the full data set attribute was set correctly
                
        #setup
        #create object with state 'Michigan' and full data from 
        #imported CSV (above)
        analyzer1 = eda.ExcessDeathsAnalyzer('Michigan', test_data1) 
        
        #check
        self.assertEqual(analyzer1.full_data.equals(test_data1), True)
     
    def test_is_init_data_working_correctly(self):    
        #Check that the state's data was obtained correctly from full data set
                
        #setup
        #create object with state 'Michigan' and full data from 
        #imported CSV (above)
        analyzer1 = eda.ExcessDeathsAnalyzer('Michigan', test_data1) 
        
        #check
        self.assertEqual(analyzer1.data.equals(test_data2), True)
        
    def test_is_init_data_converting_column_to_datetime(self): 
        #Check that type for "Week Ending Date" column was converted correctly
                
        #setup
        #create object with state 'Michigan' and full data from 
        #imported CSV (above)
        analyzer1 = eda.ExcessDeathsAnalyzer('Michigan', test_data1) 
        
        #check
        self.assertEqual(analyzer1.data['Week Ending Date'].dtype, test_data2['Week Ending Date'].dtype)
    
    def test_is_init_data_allCauses_correct(self):     
        #Check that data_allCauses attribute is correct
                
        #setup
        #create object with state 'Michigan' and full data from 
        #imported CSV (above)
        analyzer1 = eda.ExcessDeathsAnalyzer('Michigan', test_data1) 
        
        #check
        self.assertEqual(analyzer1.data_allCauses.equals(
            test_data2[ test_data2['Outcome'] == 'All causes']), True )
        
    def test_is_init_data_exceptCovid_correct(self):      
        #Check that data_exceptCovid attribute is correct
                
        #setup
        #create object with state 'Michigan' and full data from 
        #imported CSV (above)
        analyzer1 = eda.ExcessDeathsAnalyzer('Michigan', test_data1) 
        
        #check
        self.assertEqual(analyzer1.data_exceptCovid.equals(test_data2[
            test_data2['Outcome'] == 'All causes, excluding COVID-19']), True)

class ExcessDeathsAnalyzer_timeSeries_TestCase(unittest.TestCase):
    #Unit testing the creation of timeSeries plots from an ExcessDeathsAnalyzer
    #object
    

    def test_is_timeSeries_plotting_right(self):
        #confirms that .timeSeries() method produces the correct plot
        #Note: checking for whether graphics look exactly like eachother can
        #by tricky and time consuming, especially as minor formatting tweaks are
        #are implemented.  Instead of automating the check, this test will show 
        #the tester what graphic is created for visual inspection. 
        #setup:
        analyzer1 = eda.ExcessDeathsAnalyzer('Michigan', test_data1)   
        analyzer1.timeSeries() 
        
        #check (by asking tester to confirm the plot is correct)
        check = input("Does this look right? [Y or N]: ")
        self.assertEqual(check, "Y")
    
    def test_is_timeSeries_saving_right(self):
        #confirms that .timeSeries() method saves a file with the expected
        #name
        #setup:
        analyzer1 = eda.ExcessDeathsAnalyzer('Michigan', test_data1)   
        analyzer1.timeSeries(save = True, filename= 'Test_Plot')
        
        #check
        check = os.path.isfile('Test_Plot.png')
        self.assertTrue(check)
       
if __name__ == '__main__':
    unittest.main()        
        
        
        
        
        
        
        
        
        
        
        