import copy
from .process import fft_transform


class Window:
    window_time = 1000 # milliseconds
    start_time = None
    last_sample_time = None
    samples = []

    def __init__(self, window_time = 1000) -> None:
        self.window_time = window_time
   
    def sample(self, timestamp, value) -> None:
        print(self.start_time, self.last_sample_time, timestamp)
        if self.start_time == None:
            self.start_time = timestamp
        if self.last_sample_time != None:
            if self.last_sample_time + self.window_time/1000 <= timestamp:
                samples_copy = copy.deepcopy(self.samples)
                self.samples = [value]
                return samples_copy
        else:
            self.last_sample_time = timestamp
        self.samples.append(value)
        return None

class SensorWindows():

    o1_window = Window()
    o2_window = Window()
    pz_window = Window()
    fft_values = []
    
    def __init__(self) -> None:
        pass

    def sample_data(self, timestamp, values) -> None:
        o1_value = values[4]
        o2_value = values[5]
        pz_value = values[7]
        new_window_values = [ self.o1_window.sample(timestamp,o1_value), self.o2_window.sample(timestamp,o2_value), self.pz_window.sample(timestamp,pz_value)]
        fft_values = [fft_transform(x) for x in new_window_values if x is not None]
        return fft_values