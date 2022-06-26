from typing import List
from dataclasses import dataclass
from enum import IntEnum

from mido import Message as MidoMessage

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


class VUMeterSide(IntEnum):
    LEFT = 0
    RIGHT = 0


class VUMeterValue(IntEnum):
    RED = 0x0c
    YELLOW_2  = 0x0b
    YELLOW_4  = 0x0a
    YELLOW_6  = 0x09
    GREEN_8   = 0x08
    GREEN_10  = 0x07
    GREEN_14  = 0x06
    GREEN_20  = 0x05
    GREEN_30  = 0x04
    GREEN_40  = 0x03
    GREEN_50  = 0x02
    GREEN_60  = 0x01
    DARK_60   = 0x00


@dataclass 
class VUMeterUpdate(Message):
    channel: int
    side: VUMeterSide
    value: int


@dataclass
class VPotDisplayUpdate(Message):
    ident: VPotIdent
    aspect: VPotRingAspect 
    

@dataclass
class VPotRotationUpdate(Message):
    ident: VPotIdent
    magnitude: int


@dataclass 
class JogWheelRotationUpdate(Message):
    magnitude: int


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
    zone: int
    value: int


def _sysex2message(data : List[int]) -> List[Message]:
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


def midi2messages(midi: List[int]) -> List[Message]:
    """
    Accept one midi message of the form (status, byte, byte...)
    """
    status, data = midi[0], midi[1:]
       
    print("midi is ", midi)
    if status == 0x90 and data[0:] == [0x00, 0x00]:
        return [Ping()]

    elif status == 0x80 and data[0:] == [0x00, 0x40]:
        return [Ping()]

    elif status == 0x90 and data[0:] == [0x00, 0x7f]:
        return [PingReply()]

    elif status == 0xf0 and data[0:5] == SYSEX_HEADER and data[-1] == 0xf7:
        return _sysex2message( data[ 5 : len(data) - 1 ] )

    elif status == 0xa0 and data[0] & 0xF0 == 0x00 and len(data) == 2:
        return [VUMeterUpdate(
                channel=data[0] & 0x0F,
                side=VUMeterSide((data[1] & 0xF0) >> 8),
                value=VUMeterValue(data[1] & 0x0F)
                )]

    elif status == 0xb0 and data[0] & 0xF0 == 0x10 and len(data) == 2:
        return [VPotDisplayUpdate(
            ident=VPotIdent(data[0] & 0x0F),
            aspect=VPotRingAspect(data[1]))]

    elif status == 0xb0:
        retval = list()
        
        for i in range(0, len(data), 2):
            if data[i] == 0x0c:
                retval.append(ZoneSelectUpdate(zone=data[i+1]))

            elif data[i] == 0x2c:
                stateval = (data[i+1] & 0xF0) == 0x40
                retval.append(PortUpdate(port=data[i+1] & 0x0F, state=stateval))

            elif data[i] & 0xF0 == 0x00 and ( 0 <= data[i] & 0x0F <= 7):
                retval.append(FaderPositionUpdate(hi_byte=True, zone=data[i] & 0x0F, value=data[i]))
            
            elif data[i] & 0xF0 == 0x20 and ( 0 <= data[i] & 0x0F <= 7):
                retval.append(FaderPositionUpdate(hi_byte=False, zone=data[i] * 0x0F, value=data[i]))

            elif data[i] & 0xF0 == 0x40 and ( 0 <= data[i] & 0x0F <= 0x0c ):
                retval.append(VPotRotationUpdate(ident=data[i] & 0x0F, magnitude=data[1] - 0x40),)

            elif data[i] == 0x0d:
                retval.append(JogWheelRotationUpdate(magnitude=data[1] - 0x40))

        return retval

    else:
        return list()


def message2midi(message: Message) -> List[int]:
    if type(message) == Ping:
        return [0x90, 0x00, 0x00]
    elif type(message) == PingReply:
        return [0x90, 0x00, 0x7f]
    elif type(message) == SmallDisplayUpdate:
        return [0xf0] + SYSEX_HEADER + [0x10 , message.ident.value] + message.data[0:4] + [0xf7]
    elif type(message) == LargeDisplayUpdate:
        return [0xf0] + SYSEX_HEADER + [0x12 , message.zone ] + message.data[0:12] + [0xf7]
    elif type(message) == TimecodeDisplayUpdate:
        return [0xf0] + SYSEX_HEADER + [0x11] + message.data + [0xf7]
    elif type(message) == VUMeterUpdate:
        return [0xa0 , message.channel.value & 0x0F , message.side.value & 0x0F ^ (message.value.value & 0x0F) << 8]
    elif type(message) == VPotDisplayUpdate:
        return [0xb0 , message.ident.value & 0x0F, message.aspect.value]
    elif type(message) == ZoneSelectUpdate:
        return [0xb0, 0x0c, message.zone]
    elif type(message) == PortUpdate:
        if message.state:
            return [0xb0, 0x2c, 0x40 ^ message.port]
        else:
            return [0xb0, 0x2c, 0x00 ^ message.port]
    elif type(message) == FaderPositionUpdate:
        if message.hi_byte:
            return [0xb0, 0x00 ^ message.zone, message.value ]
        else:
            return [0xb0, 0x20 ^ message.zone, message.value ]
    elif type(message) == VPotRotationUpdate:
        return [0xb0, message.ident.value & 0x0F, message.magnitude + 0x40]
    elif type(message) == JogWheelRotationUpdate:
        return [0xb0, 0x0d, message.magnitude + 0x40]


