from enum import IntFlag
from typing import List
from dataclasses import dataclass


@dataclass
class TimeDisplay:
    digits : List[int]
    decimal : List[bool] 

    @classmethod
    def decode_digit(cls, val: int) -> str:
        retval = ("%X" % (val))[0:1] 
        return retval

    def display_string(self):
        rep = ""
        for i in range(8):
            rep += TimeDisplay.decode_digit(self.digits[i])
            if self.decimal[i]:
                rep += "."

        return rep

    def update(self, raw_data: List[int]):
        for i in range(len(raw_data)):
            reg_addr = len(self.digits) - (i+1)
            this_digit = raw_data[i] & 0x0f
            self.digits[reg_addr] = this_digit
            self.decimal[reg_addr] = raw_data[i] & 0xf0 == 0x10


    def __init__(self):
        self.digits = [0x0] * 8
        self.decimal = [False] * 8

