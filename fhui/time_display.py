from enum import IntFlag
from typing import List
from dataclasses import dataclass


class TimeDisplayUpdate:
    digits: List[int]
    decimals: List[bool]

    @classmethod
    def encode(cls, update: 'TimeDisplayUpdate') -> List[int]:
        retval = list()
        for i in range(0, len(update.digits)):
            this_val = update.digits[i]
            if update.decimal[i]:
                this_val += 0x10
            retval.append(this_val)

        return retval
            

    @classmethod
    def decode(cls, data: List[int]) -> 'TimeDisplayUpdate':
        retval = TimeDisplayUpdate()

        for i in data:
            retval.digits.append(i & 0x0f)
            retval.decimals.append(i & 0x10 > 0)

        return retval

@dataclass
class TimeDisplay:
    digits : List[int]
    decimal : List[bool]
    
    @classmethod
    def decode_digit(cls, val: int) -> str:
        retval = ("%X" % (val))[0:1] 
        return retval

    def __init__(self):
        self.digits = [0x0] * 8
        self.decimal = [False] * 8

    def update(self, update: TimeDisplayUpdate):
        pass
