import time

from matplotlib import pyplot as plt

from mne_lsl.datasets import sample
from mne_lsl.lsl import local_clock
from mne_lsl.stream import StreamLSL as Stream
import mne
import numpy as np
from plot import DynamicPlotter

# fname = sample.data_path() / "sample-ant-raw.fif"
# player = Player(fname)
# player.start()
stream = Stream(bufsize=5, name="NEUPHONY", stype="EEG")  # 5 seconds of buffer
stream.connect(acquisition_delay=0.2)
print(stream.info)

stream.pick(["Pz", "O1", "O2"])
print(stream.info)

def process_data(data):
    print(type(data))
    notch_filtered_raw = mne.filter.notch_filter(data.astype(np.float64), stream.info['sfreq'], freqs = 50, notch_widths = 2)
    bp_filtered_raw =  mne.filter.filter_data(notch_filtered_raw, stream.info['sfreq'],l_freq=1, h_freq=45)
    gradient_slice_array = np.diff(bp_filtered_raw, n=1, axis=-1,append=0)/0.004 #-1 axis is row
    bad_indices = []
    print(len(bad_indices), len(bp_filtered_raw))
    for index in range(len(bp_filtered_raw[0,:])):
        if max(abs(bp_filtered_raw[:,index]))>200e-6 or max(abs(gradient_slice_array[:,index]))>4500e-6:
            bad_indices.append(index)
    bp_filtered_raw = np.delete(bp_filtered_raw, bad_indices, axis=1)

    return bp_filtered_raw

dynamic_plotter = DynamicPlotter()

dynamic_plotter.show_plot()

while True:
    winsize = stream.n_new_samples / stream.info["sfreq"]
    data, ts = stream.get_data(winsize)
    processed_data = process_data(data)
    dynamic_plotter.update_plot(processed_data[0, :], processed_data[0, :], processed_data[0, :], None, True)
    time.sleep(1)
    print(f"Number of new samples: {processed_data}")
