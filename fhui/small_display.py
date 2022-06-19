from fhui.message_update import MessageUpdate
from enum import IntEnum

from dataclasses import dataclass
from typing import List

class SmallDisplayTarget(IntEnum):
    STRIP_1 = 0x00
    STRIP_2 = 0x01
    STRIP_3 = 0x02
    STRIP_4 = 0x03
    STRIP_5 = 0x04
    STRIP_6 = 0x05
    STRIP_7 = 0x06
    STRIP_8 = 0x07
    SELECT_ASSIGN = 0x08

# class SmallDisplay:
#     cell : List[int]

#     class Target(IntEnum):
#         STRIP_1 = 0x00
#         STRIP_2 = 0x01
#         STRIP_3 = 0x02
#         STRIP_4 = 0x03
#         STRIP_5 = 0x04
#         STRIP_6 = 0x05
#         STRIP_7 = 0x06
#         STRIP_8 = 0x07
#         SELECT_ASSIGN = 0x08

#     @dataclass
#     class Update(MessageUpdate):
#         chardata: List[int]
#         target: 'SmallDisplayTarget'

#         @classmethod
#         def from_midi(cls, data) -> List['Update']:
#             address = SmallDisplay.Target(data[0])
#             if address is None:
#                 raise Exception("Unrecognized small character display ID")

#             retval = cls(target=address, chardata=data[1:5])

#             return [retval]


