import numpy as np
from filterpy.kalman import KalmanFilter
from filterpy.common import Q_discrete_white_noise
# import angle_test
import sensor_reading


"""
Implements  Kalman Filter for the IMU 20948 that tracks the angle 
of the IMU for pitch and roll

Pitch is represented in the first two columns of each matrix, 
Roll is represented in the last two columns of each matrix

State vector: x(t) = [theta(t), omega(t)]. 
theta(t) is the pitch or roll angle at time t
w(t) is the angular velocity of the pitch or roll angle at time t

Install filterpy before running this script: pip install filterpy

Specs for the IMU were taken from this datasheet (below):
https://invensense.tdk.com/wp-content/uploads/2016/06/DS-000189-ICM-20948-v1.3.pdf

Process for Kalman Filter modelled of following documentation: 
https://filterpy.readthedocs.io/en/latest/kalman/KalmanFilter.html

"""

#Kalman Filter Initialization:

kf = KalmanFilter(dim_x = 4, dim_z = 2) 

#Initial value for pitch
#Matrix format: [pitch, angular velocity, roll, angular velocity]
kf.x = np.array([[0],[0],[0],[0]]) 
pitch = kf.x[0][0]
roll = kf.x[2][0]


# DEFINE ATTRIBUTES

#State Transition Matrix:
#theta changes by del_t*theta, omega stays constant

del_t = 1/562.5 #step in time: 1/sampling rate from IMU 20948 specifications
kf.F = np.array([[1,del_t,0,0], [0,1,0,0], [0,0,1,del_t],[0,0,0,1]])

#Measurement Function: 
kf.H = np.array([[1,0,0,0],[0,0,1,0]]) #Measurement only depends on theta

#Covariance Matrix: 
#Set the uncertainty to a high number (1000) so it relies more on the incoming values
#Covariances (non-diagonal numbers in the matrix) are 0 because 
#(continued) these two variables are independent

kf.P = np.eye(4)*1000

#Measurement noise (uncertainty in sensor measurements): 
#Diagonal values calculated from specifications from IMU 20948 Specification Sheet

"""
Specifications from IMU 20948 Datasheet: 

Variances calculated as follows: 
Standard deviation = Noise density * (sqrt(Sampling Rate) 
Variance = (standard deviation) ^2:

Covariances (non-diagonal numbers in the matrix) are 0 because 
these two variables are independent


Gyroscope: 
    Noise Spectral Density: 0.014 dps/sqrt(Hz) for gyroscope at full scale +/- 250 dps)
    Sampling Rate: 562.5 Hz (Low-Noise mode)
    Calculated Standard Deviation: 0.00621 rad/s
    Calculated Variance: 0.0000385641

Accelerometer:
    Noise Density: 0.230 mg/sqrt(Hz)
    Sampling Rate: 562.5 Hz
    Calculated Standard Deviation: 0.0535 m/s^2
    Calculated variance: 0.00286225

"""

kf.R = np.array([[0.0000385641, 0], [0, 0.00286225]])

#Process noise: (Uses Q_discrete_white_noise)
process_variance = 0.5 #I made this large to account for a more dynamic system
kf.Q = Q_discrete_white_noise(dim=2, dt=del_t, var=process_variance, block_size=2)

"""
Note on process_variance variable: Can be adjusted based on system's dynamics
If filter is too slow to adapt, increase value, if filter is too noisy, 
decrease value.
"""


# PREDICT-UPDATE LOOP 
if __name__ == "__main__":
    try: 
        while True: 
            z = sensor_reading.simulate_sensor_reading(pitch, roll)
            kf.predict()
            kf.update(z)
            print(f"Filtered Pitch: {kf.x[0][0]:.2f}, Filtered Roll: {kf.x[2][0]:.2f}")
    except KeyboardInterrupt: 
        print("Terminating Kalman filter.")

