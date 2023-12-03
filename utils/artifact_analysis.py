# Authors: Yatendra Singh, Ayush Sharma, Aatmjeet Singh
# Date: 2023-12-03

import numpy as np
from scipy import signal
import mne


# @LoggingDecorators.functional
def fft_from_numpy(window_samples):

    # # Plot setup
    # plt.figure(figsize=(10, 6))

    # Compute and plot FFT for each channel in list1
    return [ np.abs(np.fft.rfft(channel_data)) for channel_data in window_samples]
    
        # plt.plot(freqs, np.abs(fft_data), label=f'List1 Channel {i+1}')

    # Finalizing the plot

def bandpass_filter(inp_signal, low_cutoff, high_cutoff, order=4):
    """
    The `bandpass_filter` function applies a Butterworth bandpass filter to an input signal using the
    specified low and high cutoff frequencies.
    
    :param inp_signal: The input signal that you want to apply the bandpass filter to. This should be a
    1-dimensional array-like object, such as a list or a numpy array, containing the time-domain samples
    of the signal
    :param low_cutoff: The low_cutoff parameter is the lower frequency limit of the bandpass filter. It
    specifies the frequency below which the signal will be attenuated
    :param high_cutoff: The high_cutoff parameter in the bandpass_filter function is the upper frequency
    limit for the bandpass filter. It specifies the highest frequency that should be allowed to pass
    through the filter
    :param order: The order parameter determines the order of the filter. A higher order value will
    result in a steeper roll-off and a narrower bandwidth. The default value is 4, but you can adjust it
    based on your specific requirements, defaults to 4 (optional)
    :return: the filtered signal after applying the bandpass filter.
    """
    # Convert cutoff frequencies to normalized frequencies
    nyquist_freq = 0.5 * 125  # Assuming signal is sampled at Nyquist rate
    low_norm = low_cutoff / nyquist_freq
    high_norm = high_cutoff / nyquist_freq

    # Calculate filter coefficients
    b, a = np.array(signal.butter(order, [low_norm, high_norm], btype='bandpass'))

    # Apply filter to signal
    filtered_signal = signal.filtfilt(b, a, inp_signal)

    return filtered_signal

def smoothing_filter(values):
    """
    The function `smoothing_filter` applies a Savitzky-Golay filter to a given set of values to smooth
    out noise.
    
    :param values: The input values that you want to apply the smoothing filter to. These values can be
    a 1-dimensional array or a list of numbers
    :return: the smoothed values using the Savitzky-Golay filter.
    """
    return signal.savgol_filter(values, window_length=11, polyorder=3, mode="nearest")

def clean_bad_sengments(values):
    """
    The function `clean_bad_segments` applies notch filtering and bandpass filtering to a set of values,
    and then identifies and removes bad segments based on amplitude and gradient limits.
    
    :param values: The `values` parameter is a numpy array containing the raw data values
    :return: the cleaned values after removing the bad segments.
    """
    raw_values = raw_values.notch_filter(freqs = 50, notch_widths = 3)
    raw_values = raw_values.filter(l_freq=1, h_freq=45)

    gradient = np.diff(values, n=1, axis=-1,append=0)/0.004
    gradient_limit=4500
    amplitude_limit=200
    bad_indices = []
    for index in range(len(values[:])):
        #bad amplitude
        if abs(values[index])>amplitude_limit or abs(gradient[index])>gradient_limit:
            bad_indices.append(index)
    print(len(bad_indices), len(values))
    for i in bad_indices:
        values[i] = 0
    return values