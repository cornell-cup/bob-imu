import time
import math
import csv
from icm20948 import ICM20948
# import sensor_reading
# from kalman_filter import kf
# Initialize the sensor
DT = 0.01
imu = ICM20948()
ALPHA = 0.9
output_file = "unfi_data.csv"
headers = ["Time_stamp", "accel_roll", "gyro_roll", "com_angle", "kal_angle"]
def calculate_roll_comp(accel_x, accel_y, accel_z,gyro_x, gyro_y, gyro_z,angle):
  # Calculate the angle from the accelerometer
  accel_roll = math.atan2(accel_y, accel_z) * 180 / math.pi
  # Integrate the gyroscope data
  gyro_roll = angle + gyro_x * DT
  # Apply the complementary filter
  angle = ALPHA * gyro_roll + (1 - ALPHA) * accel_roll
  return accel_roll, gyro_roll, angle
# def calculate_pitch_comp(accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, angle):
#     # Calculate the pitch angle from the accelerometer
#     accel_pitch = math.atan2(-accel_x, math.sqrt(accel_y**2 + accel_z**2)) * 180 / math.pi
#     # Integrate the gyroscope data for pitch
#     gyro_pitch = angle + gyro_y * DT
#     # Apply the complementary filter
#     angle = ALPHA * gyro_pitch + (1 - ALPHA) * accel_pitch
#     return accel_pitch, gyro_pitch, angle
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    try:
        curr_angle = 0
        while True:
            start=time.clock_gettime(0)
            accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z = imu.read_accelerometer_gyro_data()
            #  kal_accel_roll, kal_gyro_roll, kal_angle = sensor_reading.calculate_data_kalman(accel_x, accel_y, accel_z,gyro_x, gyro_y, gyro_z,curr_angle)
            accel_roll, gyro_roll, com_angle = calculate_roll_comp(accel_x, accel_y, accel_z,gyro_x, gyro_y, gyro_z,curr_angle)
            timestamp = time.time()
            # Prepare row data
            row = [timestamp, accel_roll, gyro_roll, com_angle]
            # Write to CSV
            writer.writerow(row)
            end = time.clock_gettime(0)
            interval = end-start
            if (DT-interval)>0:
                time.sleep(DT-interval)  # Small delay for IMU reading and motor adjustment"""
    except KeyboardInterrupt:
        print("Stopping...")

