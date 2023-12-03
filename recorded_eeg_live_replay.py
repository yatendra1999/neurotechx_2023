# Authors: Yatendra Singh, Ayush Sharma, Aatmjeet Singh
# Date: 2023-12-03

import time

from matplotlib import pyplot as plt

from mne_lsl.datasets import sample
from mne_lsl.lsl import local_clock
from mne_lsl.stream import StreamLSL as Stream
from mne_lsl.player import PlayerLSL as Player
import mne
import numpy as np
from plot import DynamicPlotter

import os

dump_path = os.path.join(os.getcwd(), "dumps/40hz_freq.edf" )
player = Player(dump_path)
player.start()
print(player.name)
stream = Stream(bufsize=5, name="NEUPHONY", stype="EEG")  # 5 seconds of buffer
stream = Stream(bufsize=5, name=player.name)  # 5 seconds of buffer
stream.connect(acquisition_delay=0.2)
print(stream.info)

## Here you can start replaying the recorded LSL Streams and process further