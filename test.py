import time
from clickhouse import ClickhouseService
from pylsl import StreamInlet, resolve_stream
from plot import DynamicPlotter
from utils.window import SensorWindows
from utils.process import fft_from_numpy
import numpy as np
from kafka import KafkaService

"""Example program to show how to read a multi-channel time series from LSL."""

if __name__ == "__rain__":

    print("looking for an EEG stream...")
    streams = resolve_stream('name', 'NEUPHONY')

    inlet = StreamInlet(streams[0])

    dynamic_plotter = DynamicPlotter()
    
    dynamic_plotter.show_plot()

    sensor_window = SensorWindows()

    while True:
        sample, timestamp = inlet.pull_sample()
        sampled_values = sensor_window.sample_data(timestamp, sample)
        if any([x is not None for x in sampled_values]):
<<<<<<< Updated upstream
            fft_values = fft_from_numpy(sampled_values)
            freqs = np.fft.rfftfreq(len(fft_values[0]), 1 / 256)
            dynamic_plotter.update_plot(fft_values[0], fft_values[1], fft_values[2], freqs, True)

if __name__ == "__main__":
    with KafkaService() as kafka:
        kafka.send_message_to_topic("actions", {"direction": "UP"})
=======
            freqs = np.fft.rfftfreq(len(sampled_values[0]), 1 / 250)
            fft_values = np.abs(fft_from_numpy(sampled_values))
            dynamic_plotter.update_plot(fft_values[0], fft_values[1], fft_values[2], freqs, True)
>>>>>>> Stashed changes
