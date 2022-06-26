from typing import List


class MainDisplay:
    def __init__(self):
        self._buffer = " " * 80
    
    @property
    def line1(self):
        return ("%40s" % self._buffer[0:40])

    @property
    def line2(self):
        return ("%40s" % self._buffer[40:80])

    def update(self, zone: int, data: str):
        start = zone * 10
        for i in range(10):
            self._buffer[i + start] = data[i]

    def display_string(self):
        return self.line1 + "\n" + self.line2
