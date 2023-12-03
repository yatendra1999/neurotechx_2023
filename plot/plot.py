# Authors: Yatendra Singh, Ayush Sharma, Aatmjeet Singh
# Date: 2023-12-03

import matplotlib.pyplot as plt
import numpy as np

class DynamicPlotter:

    def __init__(self) -> None:
        """
        The function initializes a plot with specified parameters for displaying sensor data over time.
        """
        plt.ion()
        x_len = 200         # Number of points to display
        y_range = [-0.000000, 0.001]  # Range of possible Y values to display

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
        """
        The function `show_plot` plots three lines on a graph using matplotlib and displays the graph.
        """
        self.o1_line, = self.ax.plot(self.xs, self.ys_o1, label='O1 Sensor')
        self.o2_line, = self.ax.plot(self.xs, self.ys_o2, label='O2 Sensor')
        self.pz_line, = self.ax.plot(self.xs, self.ys_pz, label='PZ Sensor')
        self.ax.legend()
        # draw and show it
        self.fig.canvas.draw()
        plt.show(block=False)

    def update_plot(self, data_values_o1, data_values_o2, data_values_pz, x_labels: list | None = None, reset: bool = False) -> None:
        """
        The `update_plot` function updates the data and x-axis labels of a plot, and redraws the plot with
        the updated data.
        
        :param data_values_o1: The parameter `data_values_o1` represents the data values for the first line
        in the plot. It can be a list or numpy array containing the y-values for the first line
        :param data_values_o2: data_values_o2 is a list of data values for the second line in the plot
        :param data_values_pz: `data_values_pz` is a list of data values for the "pz" line in the plot
        :param x_labels: The `x_labels` parameter is a list of labels for the x-axis of the plot. It is used
        to update the x-axis data. If `x_labels` is not provided (i.e., it is set to `None`), the x-axis
        data is generated as a list of integers
        :type x_labels: list | None
        :param reset: The `reset` parameter is a boolean flag that determines whether to reset the plot data
        or append new data to the existing plot data. If `reset` is set to `True`, the plot data (`ys_o1`,
        `ys_o2`, `ys_pz`) will be replaced with the, defaults to False
        :type reset: bool (optional)
        """
        
        if reset and all([isinstance(x, np.ndarray) for x in [data_values_o1, data_values_o2, data_values_pz]]):
            self.ys_o1 = data_values_o1
            self.ys_o2 = data_values_o2
            self.ys_pz = data_values_pz
        else:
            # Append new data to the ys lists
            self.ys_o1.append(data_values_o1)
            self.ys_o2.append(data_values_o2)
            self.ys_pz.append(data_values_pz)

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
    
    def plot_fft(self, events, stream_info):
        """
        The function `plot_fft` computes and plots the Fast Fourier Transform (FFT) for each channel of EEG
        data.
        
        :param events: The `events` parameter is a list containing the data for each channel. Each element
        in the list represents the data for a specific channel. In the code snippet you provided,
        `events[0]` represents the data for channel "O1", `events[1]` represents the data for
        :param stream_info: The `stream_info` parameter is a dictionary that contains information about the
        streaming data. It typically includes the sampling frequency (`sfreq`) which represents the number
        of samples per second
        """
        # Set epoch duration to 1 second
        # epoch_duration = 1.0

        channels = ["O1", "O2", "Pz"]

        # Sampling frequency and frequency bins for FFT
        sfreq = stream_info['sfreq']
        freqs = np.fft.rfftfreq(1, 1 / sfreq)


        # Compute and plot FFT for each channel
        o1_data = events[0]
        o2_data = events[1]
        pz_data = events[2]
        self.update_plot(np.abs(np.fft.rfft(o1_data)), np.abs(np.fft.rfft(o2_data)), np.abs(np.fft.rfft(pz_data)), freqs, True)