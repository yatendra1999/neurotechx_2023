import numpy as np
from clickhouse.decorator import LoggingDecorators


def fft_transform(values: list[float]):
    return np.fft.fft(values)

@LoggingDecorators.functional
def fft_from_numpy(window_samples):

    # # Plot setup
    # plt.figure(figsize=(10, 6))

    # Compute and plot FFT for each channel in list1
    return [np.fft.rfft(channel_data) for channel_data in window_samples]
    
        # plt.plot(freqs, np.abs(fft_data), label=f'List1 Channel {i+1}')

    # Finalizing the plot
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.show()
