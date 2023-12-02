import mne
import numpy as np


def create_edf(list, sampling_freq=250):

    data = np.array(list)

    # Create an Info object
    # Replace 'EEG' with 'MEG', 'ECG', etc., as appropriate
    channel_types = 'eeg'
    channel_names = [f'EEG{i}' for i in range(1, data.shape[0] + 1)]
    info = mne.create_info(ch_names=channel_names, sfreq=sampling_freq, ch_types=channel_types)

    # Create a RawArray
    raw = mne.io.RawArray(data, info)