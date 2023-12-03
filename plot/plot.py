import matplotlib.pyplot as plt
from clickhouse import LoggingDecorators
import numpy as np

class DynamicPlotter:

    def __init__(self) -> None:
        plt.ion()
        x_len = 200         # Number of points to display
        y_range = [-0.000000, 250]  # Range of possible Y values to display

        # Create figure for plotting
        self.fig, self.ax = plt.subplots()
        self.xs = list(range(0, x_len))
        self.ys_o1 = [0] * x_len
        self.ys_o2 = [0] * x_len
        self.ys_pz = [0] * x_len
        self.ax.set_ylim(y_range)
        # Add labels
        plt.title('Sensor Data over Time')
        plt.xlabel('Samples')
        plt.ylabel('Values')

    def show_plot(self) -> None:
        self.o1_line, = self.ax.plot(self.xs, self.ys_o1, label='O1 Sensor')
        self.o2_line, = self.ax.plot(self.xs, self.ys_o2, label='O2 Sensor')
        self.pz_line, = self.ax.plot(self.xs, self.ys_pz, label='PZ Sensor')
        self.ax.legend()
        # draw and show it
        self.fig.canvas.draw()
        plt.show(block=False)

    # @LoggingDecorators.functional
    def update_plot(self, data_values_o1, data_values_o2, data_values_pz, x_labels: list | None = None, reset: bool = False) -> None:
        
        if reset and all([isinstance(x, np.ndarray) for x in [data_values_o1, data_values_o2, data_values_pz]]):
            self.ys_o1 = data_values_o1
            self.ys_o2 = data_values_o2
            self.ys_pz = data_values_pz
        else:
            # Append new data to the ys lists
            self.ys_o1.append(data_values_o1)
            self.ys_o2.append(data_values_o2)
            self.ys_pz.append(data_values_pz)

        # Keep only the last x_len data points
        # self.ys_o1 = self.ys_o1[-len(self.xs):]
        # self.ys_o2 = self.ys_o2[-len(self.xs):]
        # self.ys_pz = self.ys_pz[-len(self.xs):]

        # Update the x-axis data
        if x_labels is not None:
            self.xs = x_labels
        else:
            self.xs = list(range(len(self.ys_o1)))

        # Update the plot data for each line
        self.o1_line.set_ydata(self.ys_o1)
        self.o2_line.set_ydata(self.ys_o2)
        self.pz_line.set_ydata(self.ys_pz)
        self.o1_line.set_xdata(self.xs)
        self.o2_line.set_xdata(self.xs)
        self.pz_line.set_xdata(self.xs)

        # Adjust the x-axis limits for the moving window effect
        self.ax.set_xlim(min(self.xs), max(self.xs))

        # Redraw the plot
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()