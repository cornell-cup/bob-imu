import numpy as np
import math
# import angle_test

def simulate_sensor_reading(pitch, roll ):
    """
    Simulates a sensor reading for pitch, roll, and angle.
    """
    return np.array([pitch, roll])

#GET SENSOR_READING FROM ANGLE_TEST

DT = 0.01

ALPHA = 0.9

def calculate_data_kalman(accel_x, accel_y, accel_z,gyro_x, gyro_y, gyro_z,angle):
  # Calculate the angle from the accelerometer
  accel_roll = math.atan2(accel_y, accel_z) * 180 / math.pi
  # Integrate the gyroscope data
  gyro_roll = angle + gyro_x * DT
  # Apply the complementary filter
  angle = ALPHA * gyro_roll + (1 - ALPHA) * accel_roll
  return accel_roll, gyro_roll, angle


def sensor_reading(): 
    """
    Returns measurement vector based off of calculations from function
    calculate_angle_comp().
    """
    pitch, roll, _ = calculate_data_kalman()
    if pitch is None:
        raise ValueError("Invalid sensor reading: Pitch is None")
    if roll is None: 
        raise ValueError("Invalid sensor reading: Roll is None")
    return np.array([pitch, roll]) 