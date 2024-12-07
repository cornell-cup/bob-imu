import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from math import atan2, sqrt, degrees
from icm20948 import ICM20948  # Importing the ICM20948 module
import sensor_reading  # Replace with your Kalman filter implementation

# Initialize ICM20948 sensor
imu = ICM20948()

# Update speed
sampling_rate = 562.5  # Hz
update_interval = 1 / sampling_rate  # seconds
duration = 10  # seconds of simulated data

# Initialize empty lists for live plotting
time_window = int(sampling_rate)  # 1 second window for display
time_live = []
pitch_live_raw = []
pitch_live_filtered = []
roll_live_raw = []
roll_live_filtered = []

# Set up the plot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6))

line_pitch_raw, = ax1.plot([], [], label="Unfiltered Pitch", alpha=0.7)
line_pitch_filtered, = ax1.plot([], [], label="Filtered Pitch (Kalman)", linewidth=2)
ax1.set_title("Pitch Comparison")
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Pitch")
ax1.legend()
ax1.grid()

line_roll_raw, = ax2.plot([], [], label="Unfiltered Roll", alpha=0.7)
line_roll_filtered, = ax2.plot([], [], label="Filtered Roll (Kalman)", linewidth=2)
ax2.set_title("Roll Comparison")
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Roll")
ax2.legend()
ax2.grid()

plt.tight_layout()

# Function to calculate pitch and roll from accelerometer data
def calculate_pitch_roll(accel_x, accel_y, accel_z):
    pitch = atan2(-accel_x, sqrt(accel_y ** 2 + accel_z ** 2))
    roll = atan2(accel_y, accel_z)
    return degrees(pitch), degrees(roll)

# Initialize current angles for Kalman filter
curr_angle = {"pitch": 0.0, "roll": 0.0}

# Update function for animation
def update(frame):
    global time_live, pitch_live_raw, pitch_live_filtered, roll_live_raw, roll_live_filtered, curr_angle

    # Read data from IMU
    accel_x, accel_y, accel_z = imu.read_accelerometer()
    gyro_x, gyro_y, gyro_z = imu.read_gyroscope()

    # Calculate raw pitch and roll
    pitch_raw, roll_raw = calculate_pitch_roll(accel_x, accel_y, accel_z)

    # Calculate Kalman-filtered pitch and roll
    kalman_pitch, kalman_roll = sensor_reading.calculate_data_kalman(
        accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, curr_angle
    )

    # Update current angle state for the Kalman filter
    curr_angle["pitch"] = kalman_pitch
    curr_angle["roll"] = kalman_roll

    # Append new data
    current_time = frame * update_interval
    time_live.append(current_time)
    pitch_live_raw.append(pitch_raw)
    roll_live_raw.append(roll_raw)
    pitch_live_filtered.append(kalman_pitch)
    roll_live_filtered.append(kalman_roll)

    # Trim to time window
    if len(time_live) > time_window:
        time_live = time_live[-time_window:]
        pitch_live_raw = pitch_live_raw[-time_window:]
        roll_live_raw = roll_live_raw[-time_window:]
        pitch_live_filtered = pitch_live_filtered[-time_window:]
        roll_live_filtered = roll_live_filtered[-time_window:]

    # Update plot data
    line_pitch_raw.set_data(time_live, pitch_live_raw)
    line_pitch_filtered.set_data(time_live, pitch_live_filtered)
    line_roll_raw.set_data(time_live, roll_live_raw)
    line_roll_filtered.set_data(time_live, roll_live_filtered)

    # Update plot limits
    ax1.set_xlim(max(0, time_live[0]), time_live[-1])
    ax1.set_ylim(min(pitch_live_raw) - 5, max(pitch_live_raw) + 5)
    ax2.set_xlim(max(0, time_live[0]), time_live[-1])
    ax2.set_ylim(min(roll_live_raw) - 5, max(roll_live_raw) + 5)

# Animate
ani = FuncAnimation(fig, update, frames=range(int(duration * sampling_rate)), interval=update_interval * 1000, blit=False)

plt.show()

