#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os

# Create necessary directories
if not os.path.exists('Data'):
    os.makedirs('Data')
if not os.path.exists('Results'):
    os.makedirs('Results')

# Read in the data from both csv files.
data_A = pd.read_csv('Data/Entrance_A.csv', parse_dates=['Time'])
data_B = pd.read_csv('Data/Entrance_B.csv', parse_dates=['Time'])

# Merge the two datasets into a single dataframe.
combined_data = pd.concat([data_A, data_B])

# Sort the data by time.
combined_data = combined_data.sort_values('Time')

# Calculate the cumulative number of people in the space at each 5-minute interval.
interval_data = (combined_data.set_index('Time')
                 .resample('5T', closed='right')
                 .agg({'Person In': 'sum', 'Person Out': 'sum'})
                 .fillna(0)
                 .cumsum())

# Shift the data forward by 5 minutes.
interval_data = interval_data.shift(1, freq='5T', fill_value=0) #Time gap is 5 min

# Calculate the number of people in the space at each 5-minute interval.
interval_data['Counts'] = interval_data['Person In'] - interval_data['Person Out']

# Insert the first row with a timestamp of 2022-09-02 05:35:00 and a count of 0.
interval_data.loc[pd.Timestamp('2022-09-02 05:35:00')] = [0, 0, 0]

# Sort the data by time again.
interval_data = interval_data.sort_index()

# Write the counts to a new csv file.
interval_df = pd.DataFrame({'Counting Timestamp': interval_data.index, 'Counts': interval_data['Counts']})

#Export the interval data to a CSV file with the 'index' (row numbers) removed
interval_df.to_csv('Results/T2 interval_counts.csv', index=False)

