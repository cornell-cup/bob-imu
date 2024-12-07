import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import csv
import time
import pandas as pd

#load CSV file:

# Replace 'your_file.csv' with the path to your file
df = pd.read_csv('unfi_data.csv')

# View the first few rows (optional)
print(df.head())

# Example: Assuming the CSV has columns 'Time' and 'Value'
plt.figure(figsize=(10, 5))

# Plot each series
plt.plot(df['Time_stamp'], df['accel_roll'], label='Accel Roll')
plt.plot(df['Time_stamp'], df['gyro_roll'], label='Gyro Roll')
plt.plot(df['Time_stamp'], df['com_angle'], label='Com Angle')

# Add labels and title
plt.title('Time-Series Plot')
plt.xlabel('Time')
plt.ylabel('Value')
plt.legend()

# Show the plot
plt.grid(True)
plt.savefig('example_graph.png')
plt.show()