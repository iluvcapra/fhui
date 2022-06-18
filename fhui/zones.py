from enum import IntEnum, unique
from fhui.message_update import MessageUpdate
from dataclasses import dataclass
from typing import List, Optional


@unique
class ZonePort(IntEnum):

    # 0xF0 for zone, 0x0F for port
    STRIP_1_FADER   = 0x0000
    STRIP_1_SELECT  = 0x0001
    STRIP_1_MUTE    = 0x0002
    STRIP_1_SOLO    = 0x0003
    STRIP_1_AUTO    = 0x0004
    STRIP_1_VSEL    = 0x0005
    STRIP_1_INS     = 0x0006
    STRIP_1_REC     = 0x0007

    STRIP_2_FADER   = 0x0100
    STRIP_2_SELECT  = 0x0101
    STRIP_2_MUTE    = 0x0102
    STRIP_2_SOLO    = 0x0103
    STRIP_2_AUTO    = 0x0104
    STRIP_2_VSEL    = 0x0105
    STRIP_2_INS     = 0x0106
    STRIP_2_REC     = 0x0107

    STRIP_3_FADER   = 0x0200
    STRIP_3_SELECT  = 0x0201
    STRIP_3_MUTE    = 0x0202
    STRIP_3_SOLO    = 0x0203
    STRIP_3_AUTO    = 0x0204
    STRIP_3_VSEL    = 0x0205
    STRIP_3_INS     = 0x0206
    STRIP_3_REC     = 0x0207

    STRIP_4_FADER   = 0x0300
    STRIP_4_SELECT  = 0x0301
    STRIP_4_MUTE    = 0x0302
    STRIP_4_SOLO    = 0x0303
    STRIP_4_AUTO    = 0x0304
    STRIP_4_VSEL    = 0x0305
    STRIP_4_INS     = 0x0306
    STRIP_4_REC     = 0x0307

    STRIP_5_FADER   = 0x0400
    STRIP_5_SELECT  = 0x0401
    STRIP_5_MUTE    = 0x0402
    STRIP_5_SOLO    = 0x0403
    STRIP_5_AUTO    = 0x0404
    STRIP_5_VSEL    = 0x0405
    STRIP_5_INS     = 0x0406
    STRIP_5_REC     = 0x0407

    STRIP_6_FADER   = 0x0500
    STRIP_6_SELECT  = 0x0501
    STRIP_6_MUTE    = 0x0502
    STRIP_6_SOLO    = 0x0503
    STRIP_6_AUTO    = 0x0504
    STRIP_6_VSEL    = 0x0505
    STRIP_6_INS     = 0x0506
    STRIP_6_REC     = 0x0507

    STRIP_7_FADER   = 0x0600
    STRIP_7_SELECT  = 0x0601
    STRIP_7_MUTE    = 0x0602
    STRIP_7_SOLO    = 0x0603
    STRIP_7_AUTO    = 0x0604
    STRIP_7_VSEL    = 0x0605
    STRIP_7_INS     = 0x0606
    STRIP_7_REC     = 0x0607

    STRIP_8_FADER   = 0x0700
    STRIP_8_SELECT  = 0x0701
    STRIP_8_MUTE    = 0x0702
    STRIP_8_SOLO    = 0x0703
    STRIP_8_AUTO    = 0x0704
    STRIP_8_VSEL    = 0x0705
    STRIP_8_INS     = 0x0706
    STRIP_8_REC     = 0x0707
    
    #keyboard shortcuts
    KBD_CTRL_CLTCH  = 0x0800
    KBD_SHIFT_ADD   = 0x0801
    KBD_EDITMODE    = 0x0802
    KBD_UNDO        = 0x0803
    KBD_ALT_FINE    = 0x0804
    KBD_OPTION_ALL  = 0x0805
    KBD_EDITTOOL    = 0x0806
    KBD_SAVE        = 0x0807
    
    # windows
    MIX             = 0x0900
    EDIT            = 0x0901
    TRANSPORT       = 0x0902
    MEM_LOC         = 0x0903
    STATUS          = 0x0904
    ALT             = 0x0905
    
    #strip banking
    CHAN_LEFT       = 0x0a00
    BANK_LEFT       = 0x0a01
    CHAN_RIGHT      = 0x0a02
    BANK_RIGHT      = 0x0a03
    
    #assignment 1
    ASSIGN_OUTPUT   = 0x0b00
    ASSIGN_INPUT    = 0x0b01
    ASSIGN_PAN      = 0x0b02
    ASSIGN_SEND_E   = 0x0b03
    ASSIGN_SEND_D   = 0x0b04
    ASSIGN_SEND_C   = 0x0b05 
    ASSIGN_SEND_B   = 0x0b06
    ASSIGN_SEND_A   = 0x0b07
    
    #assignment 2
    ASSIGN_ASSIGN   = 0x0c00
    ASSIGN_DEFAULT  = 0x0c01
    ASSIGN_SUSPEND  = 0x0c02
    ASSIGN_SHIFT    = 0x0c03
    ASSIGN_MUTE     = 0x0c04
    ASSIGN_BYPASS   = 0x0c05
    ASSIGN_RECRDY   = 0x0c06

    CURSOR_DOWN     = 0x0d00
    CURSOR_LEFT     = 0x0d01
    CURSOR_MODE     = 0x0d02
    CURSOR_RIGHT    = 0x0d03
    CURSOR_UP       = 0x0d04
    SCRUB           = 0x0d05
    SHUTTLE         = 0x0d06

    TALKBACK        = 0x0e00
    REWIND          = 0x0e01
    FFWD            = 0x0e02
    STOP            = 0x0e03
    PLAY            = 0x0e04
    RECORD          = 0x0e05

    LOCATE_RTZ      = 0x0f00
    LOCATE_END      = 0x0f01
    ONLINE          = 0x0f02
    LOOP            = 0x0f03
    QUICKPUNCH      = 0x0f04

    AUDITION        = 0x1000
    PRE             = 0x1001
    IN              = 0x1002
    OUT             = 0x1003
    POST            = 0x1004
    
    # control room section
    MON_INPUT_3     = 0x1100
    MON_INPUT_2     = 0x1101
    MON_INPUT_1     = 0x1102
    MON_MUTE        = 0x1103
    MON_DISCRETE    = 0x1104

    MON_OUTPUT_3    = 0x1200
    MON_OUTPUT_2    = 0x1201
    MON_OUTPUT_1    = 0x1202
    MON_DIM         = 0x1203
    MON_MONO        = 0x1204
    
    # numeric entry keypad
    KEYPAD_0        = 0x1300
    KEYPAD_1        = 0x1301
    KEYPAD_4        = 0x1302
    KEYPAD_2        = 0x1303
    KEYPAD_5        = 0x1304
    KEYPAD_DECIMAL  = 0x1305
    KEYPAD_3        = 0x1306
    KEYPAD_6        = 0x1307

    KEYPAD_ENTER    = 0x1400
    KEYPAD_PLUS     = 0x1401

    KEYPAD_7        = 0x1500
    KEYPAD_8        = 0x1501
    KEYPAD_9        = 0x1502
    KEYPAD_MINUS    = 0x1503
    KEYPAD_CLEAR    = 0x1504
    KEYPAD_EQUALS   = 0x1505
    KEYPAD_SOLIDUS  = 0x1506
    KEYPAD_ASTERISK = 0x1507
    
    #time display indicators
    ANN_TIMECODE    = 0x1600
    ANN_FEET        = 0x1601
    ANN_BEAT        = 0x1602
    ANN_RUDE_SOLO   = 0x1603

    #automation enables
    AUTO_PLUGIN     = 0x1700
    AUTO_PAN        = 0x1701
    AUTO_FADER      = 0x1702
    AUTO_SENDMUTE   = 0x1703
    AUTO_SEND       = 0x1704
    AUTO_MUTE       = 0x1705

    #automation mode
    MODE_TRIM       = 0x1800
    MODE_LATCH      = 0x1801
    MODE_READ       = 0x1802
    MODE_OFF        = 0x1803
    MODE_WRITE      = 0x1804
    MODE_TOUCH      = 0x1805

    #status/group
    STATUS_PHASE    = 0x1900
    STATUS_MONITOR  = 0x1901
    STATUS_AUTO     = 0x1902
    GROUP_SUSPEND   = 0x1903
    GROUP_CREATE    = 0x1904
    GROUP_GROUP     = 0x1905

    #clip/region tools
    EDIT_PASTE      = 0x1a00
    EDIT_CUT        = 0x1a01
    EDIT_CAPTURE    = 0x1a02
    EDIT_DELETE     = 0x1a03
    EDIT_COPY       = 0x1a04
    EDIT_SEPARATE   = 0x1a05

    #function keys
    FUNC_F1         = 0x1b00
    FUNC_F2         = 0x1b01
    FUNC_F3         = 0x1b02
    FUNC_F4         = 0x1b03
    FUNC_F5         = 0x1b04
    FUNC_F6         = 0x1b05
    FUNC_F7         = 0x1b06
    FUNC_F8_ESC     = 0x1b07

    #dsp/parameter edit
    DSP_INS_PARAM   = 0x1c00
    DSP_ASSIGN      = 0x1c01
    DSP_SELECT1     = 0x1c02
    DSP_SELECT2     = 0x1c03
    DSP_SELECT3     = 0x1c04
    DSP_SELECT4     = 0x1c05
    DSP_BYPASS      = 0x1c06
    DSP_COMPARE     = 0x1c07

    #utility
    UTIL_RELAY1     = 0x1d00
    UTIL_RELAY2     = 0x1d01
    UTIL_CLICKER    = 0x1d02
    UTIL_BEEPER     = 0x1d03

    @classmethod
    def from_zone_port(cls, zone: int, port: int) -> 'ZonePort':
        return cls( (zone & 0xF0 << 8) ^ ( port & 0x0F ))

    @property
    def zone(self):
        return (self.value >> 8) & 0x0F

    @property
    def port(self):
        return (self.value & 0x0F)


class ZonePort:

    @dataclass
    class Update(MessageUpdate):
        port: ZonePort
        led_state: bool
