import numpy as np
import matplotlib.pyplot as plt

def fft_from_numpy(lists, sampling_freq=250):
    freqs = np.fft.rfftfreq(len(lists[0]), 1 / sampling_freq)

    # Plot setup
    plt.figure(figsize=(10, 6))

    # Compute and plot FFT for each channel in list1
    for i, channel_data in enumerate(lists):
        fft_data = np.fft.rfft(channel_data)
        plt.plot(freqs, np.abs(fft_data), label=f'List1 Channel {i+1}')

    # Finalizing the plot
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.show()
