import time
from clickhouse import ClickhouseService
from pylsl import StreamInlet, resolve_stream
from plot import DynamicPlotter
from utils.window import SensorWindows

"""Example program to show how to read a multi-channel time series from LSL."""

if __name__ == "__main__":

    print("looking for an EEG stream...")
    streams = resolve_stream('name', 'NEUPHONY')

    inlet = StreamInlet(streams[0])

    dynamic_plotter = DynamicPlotter()
    dynamic_plotter.show_plot()

    sensor_window = SensorWindows()

    while True:
        sample, timestamp = inlet.pull_sample()
        fft_values = sensor_window.sample_data(timestamp, sample)
        print(fft_values)
        # dynamic_plotter.update_plot(sample[4], sample[5], sample[7])
        # with ClickhouseService() as db:
        #     db.insert_values("dump", "lsl_dump", {
        #         "timestamp": time.time(),
        #         "values": sample
        #     })