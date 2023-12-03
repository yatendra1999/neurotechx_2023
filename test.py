import time
from clickhouse import ClickhouseService
from pylsl import StreamInlet, resolve_stream
from plot import DynamicPlotter
from utils.window import SensorWindows
from utils.process import fft_from_numpy
import numpy as np
from kafka import KafkaService
import json

"""Example program to show how to read a multi-channel time series from LSL."""

if __name__ == "__main__":

    print("looking for an EEG stream...")
    streams = resolve_stream('name', 'NEUPHONY')

    inlet = StreamInlet(streams[0])

    # dynamic_plotter = DynamicPlotter()
    
    # dynamic_plotter.show_plot()

    sensor_window = SensorWindows()

    # freq_values = []
    start_time = time.time()

    while time.time() < start_time + 600:
        sample, timestamp = inlet.pull_sample()
        sampled_values = sensor_window.sample_data(timestamp, sample)
        print([len(i) for i in sampled_values if i is not None])
        if any([x is not None for x in sampled_values]):
            freqs = np.fft.rfftfreq(len(sampled_values[0]), 1 / 256)
            fft_values = fft_from_numpy(sampled_values)
            timestamp = time.time()
            with ClickhouseService() as db:
                for index, item in enumerate(freqs):
                    for target_freq in [7, 13, 26, 39]:
                        if abs(item - target_freq) < 1:
                            # freq_values.append([timestamp, item, fft_values[0][index], fft_values[1][index], fft_values[2][index]])
                            db.insert_values("dump", "lsl_dump", {
                                "timestamp": time.time(),
                                "freq": item,
                                "o1": fft_values[0][index],
                                "o2": fft_values[1][index],
                                "pz": fft_values[2][index]
                            })


if __name__ == "__rain__":
    with KafkaService() as kafka:
        kafka.send_message_to_topic("actions", {"direction": "UP"})