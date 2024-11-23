#!/usr/bin/env python
# coding: utf-8

# In[17]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta

# Read the counting.csv file
data = pd.read_csv('Data/counting.csv')
data['Time'] = pd.to_datetime(data['Time'])

# Create a new DataFrame with 2 minutes and 30 seconds added to the timestamp
new_times = data['Time'] + timedelta(minutes=2, seconds=30)
new_data = pd.DataFrame({'Time': new_times, 'Counts': np.nan})

# Combine the original and new DataFrames
combined_data = pd.concat([data, new_data]).sort_values(by='Time').reset_index(drop=True)

# Use interpolation to estimate the counts for new timestamps and round them to integers
combined_data['Counts'] = combined_data['Counts'].interpolate().round()

# Filter out the specific timestamp 2022-09-03 00:02:30
filtered_data = combined_data[combined_data['Time'] != '2022-09-03 00:02:30']

# Save the filtered DataFrame to a new CSV file in the Results folder
filtered_data.to_csv('Results/results_T1.csv', index=False)

# Plot the counts and save it as a png file in the Results folder
plt.plot(filtered_data['Time'], filtered_data['Counts'], marker='o')
plt.xlabel('Time')
plt.ylabel('Counts')
plt.title('Counts vs Time')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('Results/result_plot_T1.png')
plt.show()


# In[ ]:




