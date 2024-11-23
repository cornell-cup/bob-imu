import numpy as np
import matplotlib.pyplot as plt

# Data for the graph
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create the plot
plt.plot(x, y, label='sin(x)')

# Add labels and a legend
plt.title('Example Graph')
plt.xlabel('x-axis')
plt.ylabel('y-axis')
plt.legend()

# Show the plot
plt.show()

plt.savefig('example_graph.png')