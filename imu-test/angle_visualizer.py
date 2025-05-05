import numpy as np
import timedate as dt
import matplotlib.pyplot as plt
import angle_test

# Data for the graph
x = time
y1 = accel_roll
y2 = gyro_roll
y3 = kalman_roll

# Create the plot
plt.plot(x, y1, label='gyro_roll')
plt.plot(x, y2, label='accel_roll')
plt.plot(x, y3, label='complementary_roll')

# Add labels and a legend
plt.title('Example Graph')
plt.xlabel('time')
plt.ylabel('angle')
plt.legend()

plt.savefig('example_graph.png')

if __name__ == "__main__":
    main()