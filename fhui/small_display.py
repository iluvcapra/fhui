from fhui.messages import MessageUpdate
from enum import IntEnum

class SmallDisplay:
    cell : List[int]

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

    @dataclass
    class Update(MessageUpdate):
        chardata: List[int]
        target: 'SmallDisplayTarget'

        @classmethod
        def from_midi(cls, data) -> List['Update']:
            address = SmallDisplayTarget(data[0])
            if address is None:
                raise Exception("Unrecognized small character display ID")

            retval = cls(chardata=data[1:4])
            # if data[5] is not 0xf7:
            #     raise Exception("Malformed Sysex message")

            return [retval]


