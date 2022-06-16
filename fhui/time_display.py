from enum import IntFlag
from typing import List
from dataclasses import dataclass
from fhui.messages import MessageUpdate

@dataclass
class TimeDisplay:
    digits : List[int] = list()
    decimal : List[bool] = list()
    
    class Update(MessageUpdate):
        digits: List[int]
        decimals: List[bool]

        @classmethod
        def from_midi(cls, data) -> List[Update]:
            retval = cls()
            for i in data:
                retval.digits.append(i & 0x0f)
                retval.decimals.append(i & 0x10 == 0x10)

            return [retval]


    @classmethod
    def decode_digit(cls, val: int) -> str:
        retval = ("%X" % (val))[0:1] 
        return retval

    def __init__(self):
        self.digits = [0x0] * 8
        self.decimal = [False] * 8

    def update(self, update: Update):
        pass
