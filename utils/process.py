import numpy as np
from clickhouse.decorator import LoggingDecorators

@LoggingDecorators.functional
def fft_transform(values: list[float]):
    return np.fft.fft(values)

scipy.signal.welch
