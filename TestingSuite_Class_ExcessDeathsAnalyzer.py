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
from PIL import Image
from unittest.mock import patch


#Test Data 1 contains two states' data for three weeks in March 2020
#Test Data 2 contains only one state's data for three weeks in March 2020
test_data1 = pd.read_csv('TestData1_Excess Deaths Cleaned.csv') 
test_data2 = test_data1[test_data1['State']=='Michigan']

#Convert 'Week Ending Date' series/column into datetime objects
test_todate = pd.to_datetime(test_data2['Week Ending Date'])
test_data2.loc[:,'Week Ending Date'] = test_todate

test_data2["Week Ending Date"]

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

    def test_is_timeSeries_plot_created(self):
        # Is timeSeries() method successfully creating the plot that is  
        # being produced. If not, something within the code failed for the plot 
        # to not be produced/called. ie: Did we plot something?
        
        Analyzer1 = eda.ExcessDeathsAnalyzer("Michigan", test_data1)
  
        # Sets up a mock test to see if a plot is retuned
        with patch('matplotlib.pyplot.show') as show_patch:
            Analyzer1.timeSeries()
            
            # Asserts that a plot is returned by plt.show() at the end of the
            # timeSeries method. If a plot is returned - test is ok. If a plot
            # is not returned - test fails
            assert show_patch.called 
    
    def test_is_timeSeries_plotting_right(self):
        #confirms that .timeSeries() method produces the correct plot
        #Note: checking for whether graphics look exactly like eachother can
        #by tricky and time consuming, especially as minor formatting tweaks are
        #are implemented.  Instead of automating the check, this test will show 
        #the tester what graphic is created for visual inspection. 
        #setup:
        analyzer1 = eda.ExcessDeathsAnalyzer('Michigan', test_data1)   
        analyzer1.timeSeries() 
        
        # Shows the sample chart for comparison purposes for the visual 
        # inspection accomplished below
        im = Image.open("testingSuite_timeSeries.png")
        im.show()
        
        #check (by asking tester to confirm the plot is correct)
        check = input("This is a visual test.\nDoes this look correct? [Y or N]: ")
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

class peakDateTestCase(unittest.TestCase): # inherit from unittest.TestCase
    # Unit testing peakDate() method in ExcessDeathsAnalyzers.py
    # Note: due to the way that this method is set-up, only one test for the
    #       method makes sense because the only return given by the method is
    #       the tested string output.
    
    def test_is_string_output_correct(self):
        # Is peakDate() method successfully calculating and storing the date 
        # that the peak excess deaths was reached within a given state and
        # returning the correct strings for this
        
        # Set-up: create object with state 'Michigan' and full data from 
        # imported CSV (above)
        analyzer1 = eda.ExcessDeathsAnalyzer("Michigan", test_data1)
        analyzer1.peakDate()
        
        # Assert that returned string will equal the given string
        # If equal, test passes. If not equal, test fails 
        self.assertEqual(analyzer1.peakDate(), 'The peak of Excess Deaths, all causes, for Michigan was on 2020-03-21. The peak of Excess Deaths, all causes except for COVID-19, for Michigan was on 2020-03-21')
        
class peakValueTestCase(unittest.TestCase): # inherit from unittest.TestCase
    # Unit testing peakValue() method in ExcessDeathsAnalyzers.py
    # Note: due to the way that this method is set-up, only one test for the
    #       method makes sense because the only return given by the method is
    #       the tested string output.
     
    def test_is_string_output_correct(self):
        # Is peakValue() method successfully calculating and storing the value 
        # that the peak excess deaths reached within a given state and
        # returning the correct strings for this
        
        # Set-up: create object with state 'Michigan' and full data from 
        # imported CSV (above)
        analyzer1 = eda.ExcessDeathsAnalyzer("Michigan", test_data1)
        analyzer1.peakValue()
        
        # Assert that returned string will equal the given string
        # If equal, test passes. If not equal, test fails 
        self.assertEqual(analyzer1.peakValue(), 'The peak of Excess Deaths, all causes, for Michigan was at 95 excess deathsThe peak of Excess Deaths, all causes except for COVID-19, for Michigan was at 74 excess deaths')
                
class compareToStateTestCase(unittest.TestCase): # inherit from unittest.TestCase
    # Unit testing compareToState() method in ExcessDeathsAnalyzers.py
    
    def test_is_compareToState_plot_created(self):
        # Is compareToState() method successfully creating the plot that is  
        # being produced. If not, something within the code failed for the plot 
        # to not be produced/called. ie: Did we plot something?
        
        Analyzer1 = eda.ExcessDeathsAnalyzer("Michigan", test_data1)
  
        # Sets up a mock test to see if a plot is retuned
        with patch('matplotlib.pyplot.show') as show_patch:
            Analyzer1.compareToState("Ohio")
            
            # Asserts that a plot is returned by plt.show() at the end of the
            # compareToState method. If a plot is returned - test is ok. If a 
            # plot is not returned - test fails
            assert show_patch.called 

    def test_is_compareToState_plotting_right(self):
        #confirms that compareToState() method produces the correct plot
        #Note: checking for whether graphics look exactly like eachother can
        #by tricky and time consuming, especially as minor formatting tweaks are
        #are implemented.  Instead of automating the check, this test will show 
        #the tester what graphic is created for visual inspection. 
        #setup:
        analyzer1 = eda.ExcessDeathsAnalyzer('Michigan', test_data1)   
        analyzer1.timeSeries() 
          
        # Shows the sample chart for comparison purposes for the visual 
        # inspection accomplished below
        im = Image.open("testingSuite_compareToState.png")
        im.show()
        
        #check (by asking tester to confirm the plot is correct)
        check = input("This is a visual test.\nDoes this plot look correct? [Y or N]: ")
        self.assertEqual(check, "Y")

if __name__ == '__main__':
    unittest.main()
