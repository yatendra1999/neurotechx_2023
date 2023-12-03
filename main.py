# Authors: Yatendra Singh, Ayush Sharma, Aatmjeet Singh
# Date: 2023-12-03

import time
from pylsl import StreamInlet, resolve_stream
from plot import DynamicPlotter
from utils.window import SensorWindows
from utils.artifact_analysis import fft_from_numpy
import numpy as np
import keyboard
import os
from peak_detection import Peak

"""Main program to run the  multi-channel time series from LSL."""

if __name__ == "__main__":

    print(os.environ)

    print("looking for an EEG stream...")
    streams = resolve_stream('name', 'NEUPHONY')

    inlet = StreamInlet(streams[0])
    sensor_window = SensorWindows()

    start_time = time.time()

    key_data = {
        "left": False, "right": False, "down": False, "up": False
    }
    freq_action_map = {
        7: "left",
        13: "right",
        26: "up",
        39: "down"
    }

    peak_managers = {
        7: Peak(),
        13: Peak(),
        26: Peak(),
        39: Peak()
    }

    while time.time() < start_time + 900:
        sample, timestamp = inlet.pull_sample()
        sampled_values = sensor_window.sample_data(timestamp, sample)
        if any([x is not None for x in sampled_values]):
            key_data = {
                "left": False,
                "right": False,
                "down": False,
                "up": False
            }
            freqs = np.fft.rfftfreq(len(sampled_values[0]), 1 / 256)
            fft_values = fft_from_numpy(sampled_values)
            timestamp = time.time()
            for index, item in enumerate(freqs):
                for target_freq in [7, 13, 26, 39]:
                    if abs(item - target_freq) < 1:
                        key_value = peak_managers[target_freq].sample(fft_values[0][index], fft_values[1][index], fft_values[2][index])
                        key_data[freq_action_map[target_freq]] = key_value
            print(key_data)
