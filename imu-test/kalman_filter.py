import time
import math
from icm20948 import ICM20948
import numpy as np
from filterpy.kalman import KalmanFilter
from filterpy.common import Q_discrete_white_noise

# Sampling period
DT = 1/562.5


imu = ICM20948()

def calculate_data_r(accel_y, accel_z, gyro_x, angle):
    """
    Calculates roll based off of the data from the IMU, no filters applied yet.
    Used in function sensor_reading().
    """
    # Calculate the angle from the accelerometer
    accel_roll = math.atan2(accel_y, accel_z) * 180 / math.pi

    # Integrate the gyroscope data
    gyro_roll = angle + gyro_x * DT

    return accel_roll, gyro_roll


def calculate_data_p(accel_x, accel_y, accel_z, gyro_y, angle):
    """
    Calculates pitch based off of the data from the IMU, no filters applied yet.
    Used in function sensor_reading().
    """
    # Calculate the angle from the accelerometer
    accel_pitch = math.atan2(-accel_x, math.sqrt(accel_y**2 + accel_z**2)) * 180 / math.pi

    # Integrate the gyroscope data
    gyro_pitch = angle + gyro_y * DT

    return accel_pitch, gyro_pitch


def sensor_reading(accel_x, accel_y, accel_z, gyro_x, gyro_y, angle):
    """
    Implements a complimentary low-pass filter to combine the accelerometer and
    gyroscope values for pitch and roll. Returns total pitch and total roll values
    as an array.
    """
    ALPHA = 0.9  #Can be adjusted
    BETA = 0.9   #Can be adjusted

    accel_pitch, gyro_pitch = calculate_data_p(accel_x, accel_y, accel_z, gyro_y, angle)
    accel_roll, gyro_roll = calculate_data_r(accel_y, accel_z, gyro_x, angle)

    pitch = ALPHA * gyro_pitch + (1 - ALPHA) * accel_pitch
    roll = BETA * gyro_roll + (1 - BETA) * accel_roll
    
    if pitch is None:
        raise ValueError("Invalid sensor reading: Pitch is None")
    if roll is None:
        raise ValueError("Invalid sensor reading: Roll is None")
    

    return np.array([pitch, roll])



def kalman_filter():
    """
    Implements a Kalman Filter for the IMU 20948 to track the angles for pitch and roll.
    """
    # Kalman Filter Initialization
    kf = KalmanFilter(dim_x=4, dim_z=2)

    # Initial state vector: [pitch, pitch angular velocity, roll, roll angular velocity]
    kf.x = np.array([[0], [0], [0], [0]])

    # State Transition Matrix
    del_t = DT
    kf.F = np.array([
        [1, del_t, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, del_t],
        [0, 0, 0, 1]
    ])

    # Measurement Function
    kf.H = np.array([
        [1, 0, 0, 0],
        [0, 0, 1, 0]
    ])

    # Covariance Matrix
    kf.P = np.eye(4) * 1000

    # Measurement noise (based on IMU specifications)
    kf.R = np.array([
        [0.0000385641, 0],
        [0, 0.00286225]
    ])

    # Process noise
    process_variance = 0.5
    kf.Q = Q_discrete_white_noise(dim=2, dt=del_t, var=process_variance, block_size=2)

    """
    Note: Process_variance can be adjusted based on system dynamics.
    Increase it if the filter is too slow to adapt; decrease it if it's too noisy.
    """

    return kf

def main():
    try:
        # Initialize Kalman Filter
        kf = kalman_filter()
        curr_angle = 0

        while True:
            start = time.clock_gettime(time.CLOCK_REALTIME)
            
            # Read accelerometer and gyroscope data from IMU
            accel_x, accel_y, accel_z, gyro_x, gyro_y= imu.read_accelerometer_gyro_data()

            # Get measurement vector from sensor readings
            z = sensor_reading(accel_x, accel_y, accel_z, gyro_x, gyro_y, curr_angle)

            # Predict and update steps for Kalman Filter
            kf.predict()
            kf.update(z)

            # Extract filtered pitch and roll
            filtered_pitch = kf.x[0][0]
            filtered_roll = kf.x[2][0]

            print(f"Filtered Pitch: {filtered_pitch:.2f}, Filtered Roll: {filtered_roll:.2f}")

            # Timing and sleep
            end = time.clock_gettime(time.CLOCK_REALTIME)
            interval = end - start
            if (DT - interval) > 0:
                time.sleep(DT - interval)

    except KeyboardInterrupt:
        print("Stopping...")

if __name__ == "__main__":
    main()
