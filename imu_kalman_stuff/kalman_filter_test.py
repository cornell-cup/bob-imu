import numpy as np
from kalman_filter import kf

# Simulated IMU data for pitch and roll
test_data = np.array([
    [0, 0.0, 0.0],
    [0.01, 0.0, 0.0],
    [0.02, 0.0, 0.0],
    [0.03, 0.1, 0.1],
    [0.04, 0.2, 0.2],
    [0.05, 0.3, 0.3],
    [0.06, 0.5, 0.5],
    [0.07, 0.5, 0.7],
    [0.08, 0.5, 1.0],
    [0.09, 0.6, 0.9],
    [0.10, 0.5, 1.1],
    [0.11, 0.4, 1.0],
])

def run_test(test_data):
    for i in range(len(test_data)):
        time, pitch, roll = test_data[i]
        z = np.array([pitch, roll])
        kf.predict()
        kf.update(z)

        filtered_pitch = kf.x[0][0]
        filtered_roll = kf.x[2][0]

        print(
            f"Test {i+1}: Time: {time:.2f}s, Measured: Pitch={pitch:.2f}, Roll={roll:.2f} "
    
        )

        print(f"Test {i+1}: Time={time:.2f}s, Measurement={z}")
    
        kf.predict()
        print(f"Predicted State: {kf.x.T}")
    
        kf.update(z)
        print(f"Updated State: {kf.x.T}")

run_test(test_data)
