# CS-5010-Basit-Hounds-Project

ExcessDeathsAnalyzer
QueriesAndUserInput
ReadIn_EDA_Clean_Export


ExcessDeathsAnalyzer.py

Method name: __init__
Arguments: self, state (str), full_data (dataset)
Returns: nothing

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
  
  
Method name: timeSeries
Arguments: self
Returns: nothing

When the user runs this method, the user specifies whether they would
like the output (the timeseries plot) to be saved in a file. If so, 
they pass "save = True" and the name of the file. Otherwise, the plot
is simply displayed in the console and not saved in a separate file.

Run this method to build the time series plot of excess deaths
for the state. The time series will show the range between
the average estimate and the upper bound for excess deaths
with and without COVID-19 included. The method will automatically
display the plot before ending.


        
Method name: peakDate
Arguments: self
Returns: nothing
     
Run this method to print out the date at which the state saw its
peak of excess deaths. Peak date is displayed twice: once with and 
once without COVID-19 deaths included.
Method takes no arguments (it operates on the initialized attributes) 
and returns nothing (it prints statements).
        

        
Method name: peakValue
Arguments: self
Returns: nothing

Run this method to print out the state's peak of excess deaths. 
Peak is displayed twice: once with and once without COVID-19 deaths 
in the excess deaths count.
Method takes no arguments (it operates on the initialized attributes) 
and returns nothing (it prints statements).

        
Method name: compareToState
Arguments: self, compare_state (string)
Returns: nothing

This method will take from the user as input a second state that 
the defined object's state will be compared to. The method builds
plots showing the higher estimate of excess deaths for both states
as well as the difference between the two. These charts display
excess deaths comparisons both with and without COVID-19 included 
in the excess deaths count.
