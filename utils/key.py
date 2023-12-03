# Authors: Yatendra Singh, Ayush Sharma, Aatmjeet Singh
# Date: 2023-12-03

import keyboard
import time

values = ["a", "s", "d", "f"]

class KeyboardHanlder:
    start_time = None
    # a = True

    def __init__(self) -> None:
        self.start_time = time
        keyboard.on_press(self.handle_callback)

    def handle_callback(self, event):
        print(event.__dict__)

KeyboardHanlder()

while True:
    pass