# This is a class to make a virtual GPIO, an instance of this class serves as the reset pin of the
# Virtual_Roc object.

from typing import Callable


class VirtualGPIOPin:
    def __init__(self, reset_callback: Callable, mode: str):
        self.mode = mode
        if mode == "active_low":
            self.value = 1
        elif mode == "active_high":
            self.value = 0
        else:
            raise ValueError("mode must be 'active_low' or 'active_high'")
        self.reset_callback = reset_callback

    def write(self, value):
        """

        :param value:
        :return:
        """

        self.value = value
        if self.mode == "active_low" and self.value == 0:
            self.reset_callback()
        if self.mode == "active_high" and self.value == 1:
            self.reset_callback()
