# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 13:29:30 2020

@author: pcorb
"""

import pandas as pd
import numpy as np
from datetime import datetime as dt
from datetime import timedelta
import matplotlib.pyplot as plt
#%%

#Read in Excess Deaths dataset
excess_deaths = pd.read_csv('Excess_Deaths_Associated_with_COVID-19.csv')

#%%
#Perform some initial eda of the dataset

#see the columns we are working with
print(excess_deaths.columns)
"""
Index(['Week Ending Date', 'State', 'Observed Number', 'Upper Bound Threshold',
       'Exceeds Threshold', 'Average Expected Count', 'Excess Lower Estimate',
       'Excess Higher Estimate', 'Year', 'Total Excess Lower Estimate in 2020',
       'Total Excess Higher Estimate in 2020', 'Percent Excess Lower Estimate',
       'Percent Excess Higher Estimate', 'Type', 'Outcome', 'Suppress',
       'Note'],
      dtype='object')
"""

#see what type each column was read in as
print(excess_deaths.dtypes)
"""
Week Ending Date                         object
State                                    object
Observed Number                         float64
Upper Bound Threshold                   float64
Exceeds Threshold                          bool
Average Expected Count                  float64
Excess Lower Estimate                   float64
Excess Higher Estimate                  float64
Year                                      int64
Total Excess Lower Estimate in 2020       int64
Total Excess Higher Estimate in 2020      int64
Percent Excess Lower Estimate           float64
Percent Excess Higher Estimate          float64
Type                                     object
Outcome                                  object
Suppress                                 object
Note                                     object
dtype: object
"""

#Make sure we have all 50 states plus DC, as well as national level
len(excess_deaths.State.unique())
excess_deaths.State.value_counts()
#There are 54 unique values. This is because, in addition to the 50 states,
#DC, and National, we also have Puerto Rico, and New York City is recorded
#separately from New York State.


#See if we have any missing data for the fields 'Week Ending Date', 'State',
#'Observed Number', 'Upper Bound Threshold', ' Average Expected Count, 
#'Excess Lower Estimate', 'Excess Higher Estimate', or 'Outcome'. These
#are the fields we will be using to perform our queries.
check_vars = ['Week Ending Date', 'State','Observed Number',
              'Upper Bound Threshold', 'Average Expected Count',
              'Excess Lower Estimate','Excess Higher Estimate',
              'Outcome']

for i in check_vars:
    missing = excess_deaths[[i]].isnull().sum().iloc[0]
    print("Var {} has {} missing values".format(i, missing))

"""
Var Week Ending Date has 0 missing values
Var State has 0 missing values
Var Observed Number has 41 missing values
Var Upper Bound Threshold has 9 missing values
Var Average Expected Count has 9 missing values
Var Excess Lower Estimate has 16 missing values
Var Excess Higher Estimate has 16 missing values
Var Outcome has 0 missing values
"""

#We do have some missing values for "Observed Number", "Upper Bound Threshold"
#"Average Expected Count", "Excess Lower Estimate", and 
#"Excess Higher Estimate". Take a look at these observations to see if 
#they will be an issue

data_selected_fields = excess_deaths[check_vars]
obs_with_missing_data = data_selected_fields[
    data_selected_fields.isnull().any(axis = 1)]

obs_with_missing_data['Week Ending Date'].value_counts()

#For the most part, it turns out the missing values are from within the past
#3 weeks. This is probably not surprising, as the CDC notes that data
#collection from some states takes longer than others. The exception is 
#for North Carolina and West Virginia, where the missing values extend back
#to June.

#Ultimately we will probably need to drop the rows that have missing values.


#See if there are any duplicates by State, Date, and Outcome
check_dups = excess_deaths[['State','Week Ending Date','Outcome']]
duplicates = check_dups[check_dups.duplicated()].sort_values(by = 
                                                             ['State',
                                                              'Week Ending Date'])

#There are duplicates for each state, and this is because there are 
#entries for each state where obsesrved counts are weighted to account
#for incompletness of recent data. For our purposes, we will limit
#our data to only the dates where data is likely to be complete, so we 
#will not need to use both of these. Counts are presented for "All causes"
#and "All causes, excluding COVID-19" for the Predicted type, but only for
#"All causes" for the Unweighted type. Due to this, we will drop rows
#that have the value "Unweighted" for Type. This is done further down
#in the data cleaning section

#%%Clean the data

#The CDC notes that provisional counts used to measure COVID-19 deaths
#tend to lag reported numbers by an average of 1-2 weeks. To be conservative,
#we will drop the last two weeks from the data to reduce the risk of 
#using incomplete data

#first convert 'Week Ending Date' to a datetime
excess_deaths['Week Ending Date'] = pd.to_datetime(
    excess_deaths['Week Ending Date'])

latest_date = np.max(excess_deaths['Week Ending Date'])
#The latest date in the data is 2020-07-18
latest_minus_14 = latest_date - timedelta(days = 14)
excess_deaths_complete = excess_deaths[excess_deaths['Week Ending Date']
                                       < latest_minus_14]

#check that the filter worked correctly
print(np.max(excess_deaths_complete['Week Ending Date']))
#Latest value is now June 27th

#As mentioned in the previous section, we will drop rows that have the 
#value "Unweighted" for the Type column, since we have dropped dates that
#have incomplete data.
excess_deaths_predicted = excess_deaths_complete[
    excess_deaths_complete['Type'] == "Predicted (weighted)"]

#Next, we will limit our dataset to only the previously listed fields
#that will be used for our queries.
excess_deaths_selected = excess_deaths_predicted[check_vars]

#Additionally, for our analysis we wish to focus on 2020 data, so we 
#will limit to only values from 2020

excess_deaths_2020 = excess_deaths_selected[
    excess_deaths_selected['Week Ending Date'] >= '2020-01-01']


#This data tracks New York City and New York State separately. For our 
#purposes, we would like to combine these to get an overall view of 
#New York State including New York City

#First, filter to only the NY data
NY_data = excess_deaths_2020[excess_deaths_complete['State'].isin(
    ['New York','New York City'])]

#Next, sum the selected fields for each Week and Outcome
NY_data_aggregate = NY_data.groupby(['Week Ending Date','Outcome']).sum()
#Define the State value here as 'New York Total'
NY_data_aggregate['State'] = 'New York Total'

#Because we used the groupby function, Week Ending Date and Outcome
#are now part of the index. To combine this data back, need to reset index.
NY_data_aggregate = NY_data_aggregate.reset_index()

#Drop the unaggregated NY observations from the data
NY_rows = excess_deaths_2020[excess_deaths_complete['State'].isin(
    ['New York','New York City'])].index
excess_deaths_no_ny = excess_deaths_2020.drop(NY_rows)

#Concatenate this dataset with the aggregated NY data
excess_deaths_final = pd.concat([excess_deaths_no_ny, NY_data_aggregate])

#double check the state values of the final dataset
print(excess_deaths_final['State'].value_counts())
#We now have New York Total, and no longer have New York or New York City

excess_deaths_final.to_csv('Excess Deaths Cleaned.csv')