from typing import List


class MainDisplay:
    def __init__(self):
        self._buffer = [" " * 10] * 8
    
    @property
    def line1(self):
        return "".join(self._buffer[0:4])

    @property
    def line2(self):
        return "".join(self._buffer[4:8])

    def update(self, zone: int, data: str):
        self._buffer[zone] = ("%10s" % data)[0:10]

    def display_string(self):
        return self.line1 + "\n" + self.line2
