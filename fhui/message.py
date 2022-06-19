from typing import List
from dataclasses import dataclass
from fhui.small_display import SmallDisplayTarget
from fhui.vpot import VPotIdent, VPotRingAspect 

SYSEX_HEADER = [ 0x00, 0x00, 0x66, 0x05, 0x00 ] 

@dataclass
class Message:
    pass


class Ping(Message):
    pass


class PingReply(Message):
    pass


@dataclass
class SmallDisplayUpdate(Message):
    ident : SmallDisplayTarget
    data : List[int]


@dataclass
class LargeDisplayUpdate(Message):
    zone: int
    data: List[int]


@dataclass
class TimecodeDisplayUpdate(Message):
    data: List[int]


@dataclass 
class VUMeterUpdate(Message):
    channel: int
    side: int
    value: int


@dataclass
class VPotDisplayUpdate(Message):
    ident: VPotIdent
    aspect: VPotRingAspect 
    

@dataclass
class PortUpdate(Message):
    port: int
    state: bool


@dataclass
class ZoneSelectUpdate(Message):
    zone: int


@dataclass
class FaderPositionUpdate(Message):
    hi_byte: bool
    value: int


def sysex2message(data : List[int]) -> List[Message]:
    retval = list()
    if data[0] == 0x10 and len(data) == 6:
        retval.append(SmallDisplayUpdate(
            ident=SmallDisplayTarget(data[1]),
            data=data[2:6]))
    elif data[0] == 0x12 and len(data) in [12, 23, 34, 45]:
        for i in range(1,len(data),11):
            retval.append(LargeDisplayUpdate(
                zone=data[i],
                data=data[i+1:i+11]
                ))
    elif data[0] == 0x11 and 1 <= len(data) <= 8:
            retval.append(TimecodeDisplayUpdate(data=data[1:]))

    return retval


def midi2messages(midi) -> List[Message]:
    """
    Accept one midi message of the form (status, byte, byte...)
    """
    status, data = midi[0], midi[1:]
        
    if status == 0x90 and data[0:] == [0x00, 0x00]:
        return [Ping()]

    elif status == 0x90 and data[0:] == [0x00, 0x7f]:
        return [PingReply()]

    elif status == 0xf0 and data[0:5] == SYSEX_HEADER and data[-1] == 0xf7:
        return sysex2message( data[ 5 : len(data) - 1 ] )

    elif status == 0xa0 and data[0] & 0xF0 == 0x00 and len(data) == 2:
        return [VUMeterUpdate(
                channel=data[1] & 0x0F,
                side=(data[2] & 0xF0) >> 8,
                value=(data[2] & 0x0F)
                )]

    elif status == 0xb0 and data[0] & 0xF0 == 0x10 and len(data) == 2:
        return [VPotDisplayUpdate(
            ident=VPotIdent(data[1] &0x0F),
            aspect=VPotRingAspect(data[2]))]

    elif status == 0xb0:
        retval = list()
        
        for i in range(0, len(data), 2):
            if data[i] == 0x0c:
                retval.append(ZoneSelectUpdate(zone=data[i+1]))

            elif data[i] == 0x2c:
                state = (data[i+1] & 0xF0) == 0x40
                retval.append(PortUpdate(port=data[i+1] & 0x0F), state=state)

            elif data[i] & 0xF0 == 0x00 and ( 0 <= data[i] & 0x0F <= 7):
                retval.append(FaderPositionUpdate(hi_byte=True, value=data[i]))
            
            elif data[i] & 0xF0 == 0x20 and (0 <= data[i] & 0x0F <= 7):
                retval.append(FaderPositionUpdate(hi_byte=False, value=data[i]))

        return retval

    else:
        return list()


def message2midi(message: Message) -> List[int]:
    # to be implemented
    pass
