import time
import math
from icm20948 import ICM20948

# Code borrowed from ankle_sync_v2.py

DT = 0.01

imu = ICM20948()

ALPHA = 0.9

# Complementary Filter
# Calculate angle based on imu accelerometer and gyroscope data
def calculate_angle_comp(accel_x, accel_y, accel_z,gyro_x, gyro_y, gyro_z,angle):
  # Calculate the angle from the accelerometer
  accel_roll = math.atan2(accel_y, accel_z) * 180 / math.pi
  # Integrate the gyroscope data
  gyro_roll = angle + gyro_x * DT
  # Apply the complementary filter
  angle = ALPHA * gyro_roll + (1 - ALPHA) * accel_roll
  return accel_roll, gyro_roll, angle

# Kalman Filter angle calculation
def calculate_angle_kalman():
  return 0

def main():
    try:
        curr_angle = 0
        while True:
          start=time.clock_gettime(0)
          accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z = imu.read_accelerometer_gyro_data()
          accel_roll, gyro_roll, curr_angle = calculate_angle_comp(accel_x, accel_y, accel_z,gyro_x, gyro_y, gyro_z,curr_angle)

          abs_g = math.sqrt(accel_x*accel_x+accel_y*accel_y+accel_z*accel_z)
          
          # Reset Logic
          # if accel_z>0.995 and accel_z<1.005 and abs_g>0.95 and abs_g<1.05:
          #     curr_angle = 0

          # Print current angle
          print(curr_angle)

          end = time.clock_gettime(0)
          interval = end-start
          if (DT-interval)>0:
            time.sleep(DT-interval)  # Small delay for IMU reading and motor adjustment"""
    
    except KeyboardInterrupt: 
        print("Stopping...")

if __name__ == "__main__":
    main()
