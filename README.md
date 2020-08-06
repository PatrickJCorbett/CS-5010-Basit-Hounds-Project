# CS-5010-Basit-Hounds-Project

CS 5010 Semester Project - COVID-19 Excess Deaths
Group: Basit Hounds
Members: Will Blickle, Patrick Corbett, Krissy North, Rowan Rice


Background:

As COVID-19 continues to infect and kill people, some members of the 
public have expressed concern that official counts of deaths due to the 
disease are exaggerated.  Other people believe that death counts are 
undercounting deaths due to COVID-19.  Still others believe that not only 
is there an extreme uptick in deaths due to COVID-19, but also there are 
increased deaths from other causes (such as strokes and heart attacks) 
due to the fact that people are delaying routine or urgent medical care 
because of an increased fear of contracting COVID-19 at healthcare
facilities.   

One way to evaluate these theories is to examine “excess deaths,” 
which is “typically defined as the difference between the observed numbers of 
deaths in specific time periods and expected numbers of deaths in the same 
time periods."  The "expected numbers" of deaths for a given time period is 
calculated by averaging the number of deaths in the same time period in 
previous years.  Currently the CDC is collecting death statistics from each
state (plus Washington DC and Puerto Rico) and is comparing the reported number 
of deaths in a given week to an average of deaths in the same weeks in 2017, 
2018 and 2019 to calculate a total excess death count.  The CDC specifies the 
number of deaths reported due to COVID-19 and the number of deaths reported 
due to other causes (such as strokes, heart attacks, cancer, natural causes, 
etc.) by week and by state.  

We've designed a program to help users visualize the CDC's data about excess 
deaths, both including and excluding COVID-19 deaths, to see the difference 
in the numbers in 2020 compared to the average over the last three years.  
Users of the program can view the numbers on the national level or drill down 
to a specific state (including DC and Puerto Rico) to see how the excess death
count has changed over time on a week-by-week basis.  Users can access the 
week that a state had its peak excess deaths and see what the number was.
Users can also choose to compare two states.

The program is comprised of the following files:
--ExcessDeathsAnalyzer.py
--QueriesAndUserInput.py
--ReadIn_EDA_Clean_Export.py
--TestingSuite_Class_ExcessDeathsAnalyzer.py
 
 
 
ReadIn_EDA_Clean_Export.py

Background on CDC excess deaths data: 

The CDC publishes numbers of excess deaths for the United States on a weekly 
basis on their website via csv files.  According to the CDC, "death counts 
were derived from the National Vital Statistics System database that provides 
the timeliest access to the vital statistics mortality data" and then are 
compiled as weekly counts by the CDC.  The CDC then compares weekly counts of 
deaths "with historical trends to determine whether the number of deaths is 
significantly higher than expected."  The resulting csv file that the CDC
publishes includes excess death counts for every state in the United States
by week starting in 2017 through the most recent week (at time of writing
it was updated last on July 29, 2020).

Description of the data cleaning process:

This file (ReadIn_EDA_Clean_Export) reads in the data from a csv via a url 
that is updated weekly by the CDC.  By reading in the csv file from the url, 
this ensures that the program can be run not just today but in the future with 
up-to-date data as the CDC updates their data.

The file then performs the following steps to clean the data for analysis:

1. Isolates data in the file that corresponds to excess deaths during 2020 only
(the CDC data file in full contains data from 2017 - present).
2. Removes the previous two weeks of data from the day of running the program 
due to the fact that excess death reports are not necessarily confirmed deaths
at the time of reporting to the CDC. At two weeks out, excess deaths estimates
are more reliable.
3. Combines New York City data and New York State data into one group called 
New York, then reviews the states that are included in the dataset: 53 items = 
all 50 states plus Washington DC, Puerto Rico, and United States (which 
represents the US as a whole).
4. Isolates the four summary statistics needed for each state for each week:
    1. Excess deaths all-causes, upper bound estimate
    2. Excess deaths all-causes, lower bound estimate
    3. Excess deaths excluding COVID-19, upper bound estimate
    4. Excess deaths excluding COVID-19, lower bound estimate

The output from this file (the final cleaned dataset used for analysis) is 
exported to a csv file called 'Excess Deaths Cleaned.csv' 



ExcessDeathsAnalyzer.py

Description:

This file contains an object called ExcessDeathsAnalyzer. The object has two 
main attributes: a state name and the excess death dataset that contains 
excess death information for all 50 states plus Puerto Rico, Washington DC and 
the United States as a whole.  For each state for each week in 2020, there is a 
count of the excess deaths due to all causes of death and a count of the 
excess deaths not including COVID-19 deaths.  The methods included in the class
query the dataset and produce visualizations for the user based on the user's
selected state. 

The methods in the class include:
--init
--timeSeries
--peakDate
--peakValue
--compareToState


Method name: __init__
Arguments: self, state (str), full_data (dataset)
Returns: nothing

This method is the constructor.  The object is initialized with the 
state that the user chooses to analyze and the dataset that contains 
the excess death statistics per state.  The full dataset
of all states is stored as "full_data." The constructor also creates 
3 different subsets of the full dataset:

    1. the subset of data for the state only, stored as "data"

    2. the subset of data for the state only including the statistics 
    associated with deaths due to all causes, stored as "data_allCauses"

    3. the subset of data for the state including the statistics 
    associated with deaths due to all causes EXCEPT deaths caused
    by COVID-19, stored as "data_exceptCovid"
  
  
Method name: timeSeries
Arguments: self, save (boolean), filename (string)
Returns: nothing

When the user runs this method, the user specifies whether they would
like the output (the timeseries plot) to be saved in a file. If so, 
they pass "save = True" and the name of the file. Otherwise, the plot
is simply displayed in the console and not saved in a separate file.

Run this method to build the time series plot of excess deaths
for the state. The time series will show the lower bound estimate and the 
upper bound estimate for excess deaths for all causes in blue, and the lower
bound and upper bound estimate for excess deaths excluding COVID-19 deaths 
in green. The method will automatically display the plot in the console.

        
Method name: peakDate
Arguments: self
Returns: nothing
     
Run this method to print out the date of the week ending during which
the state had its peak of excess deaths during the timeframe included
in the dataset. Peak date is displayed twice: once with and 
once without COVID-19 deaths included. Method takes no arguments (it 
operates on the initialized attributes) and returns nothing 
(it prints statements to the console).
        
        
Method name: peakValue
Arguments: self
Returns: nothing

Run this method to print out the state's peak count of excess deaths
during the timeframe included in the dataset. Peak is displayed twice: 
once with and once without COVID-19 deaths in the excess deaths count.
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



QueriesAndUserInput.py

Description:

This file is the driver for the program.  It imports the data table from the
ReadIn_EDA_Clean_Export file and the ExcessDeathsAnalyzer class.  The file 
first demonstrates the functionality of the program with 5 queries:
1. Display the excess deaths for the United States as whole via
a week-by-week time series graph of excess deaths all-causes and excess deaths 
excluding deaths from COVID-19 (timeSeries)
2. Produce the date of the week during which the United States as a whole
had the most excess deaths all-causes thus far in 2020.  (peakDate)
3. Produce the number of excess deaths all-causes that was the maximum 
observed excess deaths in a single week thus far in 2020 for the United States 
as a whole. (peakValue)
4. Display the excess deaths for Virginia via a time series graph of excess 
deaths all-causes and excess deaths excluding deaths from COVID-19 (timeSeries)
5. Compare excess deaths all-causes and excess deaths excluding COVID-19 
on week-by-week basis between Virginia and New York.

Then the file requests user input by asking what state the user is from.  The
program does error checking to make sure the state is in the dataset.  The 
program then allows the user to decide what queries to run on their state:
1. Time series
2. Peak date
3. Peak value
4. All three queries
Once the user runs a query on their state, the user is asked whether they would
like to compare their state to another state.  If so, the program takes in 
a second state name from the user and produces the comparison plots between 
the two states. 
The user is given the choice to continue feeding the program new states for as 
long as the user is interested in looking at the analyses.  The user can exit
the analysis when the user no longer wants to choose a new state.

The user-input section of this file included a number of helper functions to 
run the loops that asks the user for inputs.



TestingSuite_Class_ExcessDeathsAnalyzer.py

Description:

We designed and implemented a testing suite containing one test class for each method that exists in the ExcessDeathsAnalyzer module. 

Each test class attempts to test all features of a particular method; for instance, the __init__ unit test contains six test methods, one for each attribute of the object being initialized. 

We created a smaller test data set to use for unit testing: we narrowed the CDC data to only two states (Michigan and Ohio) for the first three weeks in March 2020.  By using this predefined test data set, we ensure that any future changes to the source dataset do not create faults in our unit testing. 


