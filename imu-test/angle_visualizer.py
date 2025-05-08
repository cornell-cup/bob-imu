import numpy as np
import time
from icm20948 import ICM20948
import math
import matplotlib.pyplot as plt

import angle_test
import angle_test_Rhea as kft
DT = 0.01
ALPHA = 0.9
imu = ICM20948()

start_time = time.time()

def main():
    curr_angle = 0
    kf = kft.kalman_filter()
    time_log = []
    accel_roll_log = []
    gyro_roll_log = []
    comp_roll_log = []
    kalman_roll_log = []

    start_time = time.time()

    try:
        
        while time.time() - start_time < 10: # Run for 10 seconds  
            loop_start = time.time()

            accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z = imu.read_accelerometer_gyro_data()
            # Complementary filter
            accel_roll, gyro_roll, curr_angle = angle_test.calculate_angle_comp(accel_x, accel_y, accel_z,gyro_x, gyro_y, gyro_z,curr_angle)
            
            # Kalman filter
            z = kft.sensor_reading(accel_x, accel_y, accel_z, gyro_x, gyro_y, curr_angle)

            # Predict and update steps for Kalman Filter
            kf.predict()
            kf.update(z)

            # Extract filtered pitch and roll
            # filtered_pitch = kft.kf.x[0][0]
            filtered_roll = kf.x[2][0]

            # Log data
            time_log.append(time.time() - start_time)
            accel_roll_log.append(accel_roll)
            gyro_roll_log.append(gyro_roll)
            comp_roll_log.append(curr_angle)
            kalman_roll_log.append(filtered_roll)

            # Delay
            end = time.clock_gettime(0)
            interval = time.time()-loop_start
            if (DT-interval)>0:
                time.sleep(DT-interval)  # Small delay for IMU reading and motor adjustment
    
    except KeyboardInterrupt: 
        print("Stopping...")

    # Data for the graph
    x = time_log
    r1 = accel_roll_log
    r2 = gyro_roll_log
    r3 = comp_roll_log
    r4 = kalman_roll_log
    # p1 = accel_pitch
    # p2 = gyro_pitch
    # p3 = comp_pitch
    # p4 = kalman_pitch

    # Create the plot
    plt.plot(x, r1, label='gyro_roll')
    plt.plot(x, r2, label='accel_roll')
    plt.plot(x, r3, label='complementary_roll')
    plt.plot(x, r4, label='kalman_roll')

    # Add labels and a legend
    plt.title('Roll Angle Over Time')
    plt.xlabel('time (s)')
    plt.ylabel('angle (degrees)')
    plt.legend()
    plt.savefig('roll_angle_plot.png')

if __name__ == "__main__":
    main()