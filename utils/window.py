# Authors: Yatendra Singh, Ayush Sharma, Aatmjeet Singh
# Date: 2023-12-03

import copy

# The Window class allows for sampling values within a specified time window and returns the previous
# samples if the window time has elapsed.
class Window:
    window_time = 1000 # milliseconds
    last_sample_time = None
    samples = []

    def __init__(self, window_time = 1000) -> None:
        self.window_time = window_time
   
    def sample(self, timestamp, value) -> None:
        """
        The `sample` function takes a timestamp and a value as input, and returns a copy of the samples if
        the time difference between the last sample and the current sample is greater than or equal to the
        window time, otherwise it adds the current sample to the list of samples.
        
        :param timestamp: The timestamp parameter represents the time at which the sample is taken. It is a
        numerical value that indicates the time in some unit (e.g., seconds, milliseconds)
        :param value: The "value" parameter represents the value of the sample that you want to add to the
        samples list
        :return: either a deep copy of the samples list or None.
        """
        # print(self.last_sample_time, timestamp)
        if self.last_sample_time != None:
            if self.last_sample_time + self.window_time/1000 <= timestamp:
                samples_copy = copy.deepcopy(self.samples)
                self.samples = [value]
                self.last_sample_time = timestamp
                return samples_copy
        else:
            self.last_sample_time = timestamp
        self.samples.append(value)
        return None

# The `SensorWindows` class represents a sensor with three window objects (`o1_window`, `o2_window`,
# `pz_window`) that can sample data at a given timestamp.
class SensorWindows():

    o1_window = Window()
    o2_window = Window()
    pz_window = Window()
    fft_values = []
    
    def __init__(self) -> list[list]:
        pass

    def sample_data(self, timestamp, values) -> None:
        """
        The function `sample_data` takes a timestamp and a list of values, extracts specific values from
        the list, and returns the results of calling the `sample` method on three different window objects
        with the timestamp and extracted values as arguments.
        
        :param timestamp: The timestamp parameter is the time at which the data is being sampled. It is
        typically a numerical value representing the time in seconds or milliseconds
        :param values: The `values` parameter is a list of values. In this code snippet, it is assumed that
        `values` has at least 8 elements. The values at index 4, 5, and 7 are assigned to `o1_value`,
        `o2_value`, and `pz_value
        :return: a list containing the results of three method calls:
        `self.o1_window.sample(timestamp,o1_value)`, `self.o2_window.sample(timestamp,o2_value)`, and
        `self.pz_window.sample(timestamp,pz_value)`.
        """
        o1_value = values[4]
        o2_value = values[5]
        pz_value = values[7]
        return [ self.o1_window.sample(timestamp,o1_value), self.o2_window.sample(timestamp,o2_value), self.pz_window.sample(timestamp,pz_value)]
        