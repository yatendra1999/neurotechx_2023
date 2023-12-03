# Authors: Yatendra Singh, Ayush Sharma, Aatmjeet Singh
# Date: 2023-12-03

import mne
import numpy as np


def create_edf(list, sampling_freq=250):
    """
    The function `create_edf` creates an EDF file from a list of data, with an optional sampling
    frequency parameter.
    
    :param list: The `list` parameter is a list of EEG data. Each element in the list represents the EEG
    data for a single channel at a specific time point. The shape of the `list` should be `(n_channels,
    n_samples)`, where `n_channels` is the number of EEG channels and
    :param sampling_freq: The sampling_freq parameter is the sampling frequency of the data, which
    represents the number of samples per second. It is typically measured in Hertz (Hz), defaults to 250
    (optional)
    :return: a RawArray object, which is created using the input list of data and the specified sampling
    frequency.
    """

    data = np.array(list)

    # Create an Info object
    # Replace 'EEG' with 'MEG', 'ECG', etc., as appropriate
    channel_types = 'eeg'
    channel_names = [f'EEG{i}' for i in range(1, data.shape[0] + 1)]
    info = mne.create_info(ch_names=channel_names, sfreq=sampling_freq, ch_types=channel_types)

    # Create a RawArray
    raw = mne.io.RawArray(data, info)
    return raw