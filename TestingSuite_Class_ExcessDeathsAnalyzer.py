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
from ExcessDeathsAnalyzer import *

#Test Data 1 contains two states' data for three weeks in March 2020
#Test Data 2 contains only one state's data for three weeks in March 2020
test_data1 = pd.read_csv('TestData1_Excess Deaths Cleaned.csv') 

test_data2 = test_data1[test_data1['State']=='Michigan']
pd.to_datetime(test_data2.loc[:,'Week Ending Date']) 


#for_csv.to_csv('TestData2_Excess Deaths Cleaned.csv')
#test_data2 = pd.read_csv('TestData2_Excess Deaths Cleaned.csv') 

#real_data = pd.read_csv('Excess Deaths Cleaned.csv')

class ExcessDeathsAnalyzer_init_TestCase(unittest.TestCase):
    #Unit testing the creation of ExcessDeathsAnalyzer objects
    
    def test_is_init_working_correctly_with_kwargs(self):
        #test whether objects are created correctly when passed all kwargs
        
        #create object with state 'Michigan' and full data from 
        #imported CSV (above)
        analyzer1 = ExcessDeathsAnalyzer('Michigan', test_data1)
        
        #Check that the state attribute was set correctly
        self.assertEqual(analyzer1.state, 'Michigan')
        
        #Check that the full data set attribute was set correctly
        self.assertEqual(analyzer1.full_data.equals(test_data1), True)
        
        #Check that the state's data was obtained correctly from full data set
        self.assertEqual(analyzer1.data.equals(test_data2), True)
        
        #Check that type for "Week Ending Date" column was converted correctly
        self.assertEqual(analyzer1.data['Week Ending Date'].dtype, test_data2['Week Ending Date'].dtype)
        
        #Check that data_allCauses attribute is correct
        self.assertEqual(analyzer1.data_allCauses.equals(
            test_data2[ test_data2['Outcome'] == 'All causes']), True )
        
        #Check that data_exceptCovid attribute is correct
        self.assertEqual(analyzer1.data_exceptCovid.equals(test_data2[
            test_data2['Outcome'] == 'All causes, excluding COVID-19']), True)
          
       
if __name__ == '__main__':
    unittest.main()        
        
        
        
        
        
        
        
        
        
        
        