import numpy as np
import timedate as dt
import matplotlib.pyplot as plt
import angle_test

# Data for the graph
x = time
r1 = accel_roll
r2 = gyro_roll
r3 = comp_roll
r4 = kalman_roll
p1 = accel_pitch
p2 = gyro_pitch
p3 = comp_pitch
p4 = kalman_pitch

# Create the plot
plt.plot(x, r1, label='gyro_roll')
plt.plot(x, r2, label='accel_roll')
plt.plot(x, r3, label='complementary_roll')
plt.plot(x, r3, label='kalman_roll')

# Add labels and a legend
plt.title('Example Graph')
plt.xlabel('time')
plt.ylabel('angle')
plt.legend()

plt.savefig('example_graph.png')

if __name__ == "__main__":
    main()