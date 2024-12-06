import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time

# Set up the figure and axis
fig, ax = plt.subplots()
x_data, y_data = [], []
line, = ax.plot([], [], 'b-', label="Sine Wave")
ax.set_xlim(0, 10)
ax.set_ylim(-1.5, 1.5)
ax.set_title("Real-Time Animation with Matplotlib")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Amplitude")
ax.legend()

# Initialize the data source
start_time = time.time()

# Call this function periodically
def animate(i, xs, ys):
    current_time = time.time() - start_time
    new_x = current_time
    new_y = np.sin(2 * np.pi * current_time)
    
    # Append new data
    x_data.append(new_x)
    y_data.append(new_y)
    
    # Limit the amount of data shown
    if len(x_data) > 100:
        x_data.pop(0)
        y_data.pop(0)
    
    # Update the line plot
    line.set_data(x_data, y_data)
    ax.set_xlim(max(0, new_x - 10), new_x)  # Keep the x-axis scrolling dynamically

# Create the animation
ani = animation.FuncAnimation(fig, animate, fargs=(x_data, y_data), interval=100, save_count=100)  # Update every 100 ms
plt.show()
