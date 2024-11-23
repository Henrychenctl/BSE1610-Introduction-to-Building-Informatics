#!/usr/bin/env python
# coding: utf-8

# In[38]:


#First Method

#Import the pandas library for data manipulation and analysis
import pandas as pd
import os

# Create necessary directories
if not os.path.exists('Data'):
    os.makedirs('Data')
if not os.path.exists('Results'):
    os.makedirs('Results')

# Step 1: Read in the data from both csv files.
data_A = pd.read_csv('Data/Entrance_A.csv', parse_dates=['Time'])
data_B = pd.read_csv('Data/Entrance_B.csv', parse_dates=['Time'])

#Concatenate the entrance data from both entrances into a single dataframe
combined_data = pd.concat([data_A, data_B], ignore_index=True)

#Convert the 'Time' column of the combined dataframe to a datetime object for time manipulation
combined_data['Time'] = pd.to_datetime(combined_data['Time'])

#Set the index of the combined dataframe to the 'Time' column for easy time-based data aggregation
combined_data = combined_data.set_index('Time')

#Aggregate the data for each 5-minute interval by calculating the difference between 'Person In' and 'Person Out'
interval_data = combined_data.resample('5T').sum()['Person In'] - combined_data.resample('5T').sum()['Person Out'] #Time interval is 5 min

#Create a new dataframe to store the aggregated interval data with columns for start time, end time, and count
interval_df = pd.DataFrame({'Counts': interval_data, 'Start Time': interval_data.index})

#Create a new column for end time by subtracting 5 minutes from the start time
interval_df['End Time'] = interval_df['Start Time'] + pd.Timedelta(minutes=5)

#Replace the NaN value in the first row with the earliest start time
interval_df['End Time'].fillna(interval_df['Start Time'].iloc[0].floor('5T'), inplace=True)

#Reorder the columns to have 'Start Time', 'End Time', and 'Count' in that order
interval_df = interval_df[['Start Time', 'End Time', 'Counts']]

#Export the interval data to a CSV file with the 'index' (row numbers) removed
interval_df.to_csv('Results/T1 first method counts.csv', index=False)


# In[39]:


#Second Method

import csv
import datetime
import os

# Create necessary directories
if not os.path.exists('Data'):
    os.makedirs('Data')
if not os.path.exists('Results'):
    os.makedirs('Results')

# Read data from the first file
with open('Data/Entrance_A.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)

    data1 = [[datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S'), 1 if row[1] == '1' else (-1 if row[2] == '1' else 0)] for row in csv_reader if row[0]]

# Read data from the second file
with open('Data/Entrance_B.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # skip the first row
    data2 = [[datetime.datetime.strptime(row[0], '%Y/%m/%d %H:%M:%S'), 1 if row[1] == '1' else (-1 if row[2] == '1' else 0)] for row in csv_reader if row[0]]

# Combine the data from both files
data = sorted(data1 + data2)

# Calculate the counts for each 5-minute interval
counts = []
current_time = data[0][0].replace(minute=(data[0][0].minute//5)*5, second=0)
current_count = data[0][1]
for i in range(1, len(data)):
    time_diff = (data[i][0] - current_time).total_seconds() / 60
    if time_diff >= 5:
        counts.append([current_time, data[i-1][0], current_count])
        current_time = data[i][0].replace(minute=(data[i][0].minute//5)*5, second=0)
        current_count = data[i][1]
    else:
        current_count += data[i][1]
counts.append([current_time, data[-1][0].replace(minute=(data[-1][0].minute//5)*5, second=0), current_count])
while current_time + datetime.timedelta(seconds=299) < data[-1][0]:
    current_time = current_time + datetime.timedelta(seconds=299)
    counts.append([current_time, current_time + datetime.timedelta(seconds=299), 0])

# Replace NaN with 0 in the first column
for i in range(len(counts)):
    counts[i][0] = counts[i][0] if counts[i][0] else 0

# Write the counts to a new CSV file in the Data folder
file_path = os.path.join('Results', 'T1 second method counts.csv')
with open(file_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Start Time', 'End Time (exclusive)', 'Counts'])
    for i, row in enumerate(counts):
        # Make sure the next start time is at least 1 second after the current end time
        if i > 0 and row[0] < counts[i-1][1] + datetime.timedelta(seconds=1):
            row[0] = counts[i-1][1] + datetime.timedelta(seconds=1)
            row[1] = row[0] + datetime.timedelta(seconds=299)#time interval is 299s / 4min59s
        else:
            row[1] = row[0] + datetime.timedelta(seconds=299)
        csv_writer.writerow([row[0], row[1], row[2] if row[2] is not None else 0])

# Write the counts to a new CSV file in the Data folder
file_path = os.path.join('Results', 'T1 second method counts.csv')
with open(file_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Start Time', 'End Time (exclusive)', 'Counts'])
    i = 0
    current_time = counts[i][0].replace(hour=5, minute=35, second=0, microsecond=0)
    while current_time < counts[-1][1]:
        if i < len(counts) and current_time >= counts[i][0] and current_time < counts[i][1]:
            row = counts[i]
            i += 1
        else:
            row = [current_time, current_time + datetime.timedelta(seconds=299), 0]
        csv_writer.writerow([row[0], row[1], row[2]])
        current_time = current_time + datetime.timedelta(seconds=300)


# In[ ]:




