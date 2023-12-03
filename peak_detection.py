# Authors: Yatendra Singh, Ayush Sharma(), Aatmjeet Singh, Krish Verma
# Date: 2023-12-03

from scipy.signal import find_peaks
import time

# The `Peak` class tracks the history of three values (`o1_value`, `o2_value`, `pz_value`) and checks
# if there are any peaks in the last 10 seconds of data.

class Peak:
    o1_history = []
    o2_history = []
    pz_history = []

    def __init__(self):
        """
        The above function initializes the start time of an object.
        """
        self.start_time = time.time()

    def sample(self, o1_value, o2_value, pz_value):
        """
        The `sample` function appends values to three different lists and checks if the last element of each
        list is greater than or equal to the length of the list minus 5.
        
        :param o1_value: The `o1_value` parameter represents the value of the first variable `o1` at a given
        time
        :param o2_value: The `o2_value` parameter represents the value of the variable `o2` at a specific
        time
        :param pz_value: The `pz_value` parameter represents the value of the variable `pz` at a specific
        time
        :return: a boolean value.
        """
        self.o1_history.append(o1_value)
        self.o2_history.append(o2_value)
        self.pz_history.append(pz_value)
        if self.start_time + 10 > time.time():
            return False
        else:
            o1_peaks, _ = find_peaks(self.o1_history)
            o2_peaks, _ = find_peaks(self.o2_history)
            pz_peaks, _ = find_peaks(self.pz_history)
            print(o1_peaks, o2_peaks, pz_peaks)
            print(len(o1_peaks))
            print([x[-1] >= len(o1_peaks) - 5 for x in [o1_peaks, o2_peaks, pz_peaks]])
            return any([x[-1] >= len(o1_peaks) - 5 for x in [o1_peaks, o2_peaks, pz_peaks]])
