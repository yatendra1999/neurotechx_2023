import numpy as np
from scipy import signal
import mne

def fft_transform(values: list[float]):
    return np.fft.fft(values)

# @LoggingDecorators.functional
def fft_from_numpy(window_samples):

    # # Plot setup
    # plt.figure(figsize=(10, 6))

    # Compute and plot FFT for each channel in list1
    return [np.fft.rfft(clean_bad_sengments(channel_data)) for channel_data in window_samples]
    
        # plt.plot(freqs, np.abs(fft_data), label=f'List1 Channel {i+1}')

    # Finalizing the plot
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.show()

def bandpass_filter(inp_signal, low_cutoff, high_cutoff, order=4):
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
    return signal.savgol_filter(values, window_length=11, polyorder=3, mode="nearest")

def clean_bad_sengments(values):
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