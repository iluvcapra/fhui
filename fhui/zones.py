from enum import IntEnum, unique

@unique
class Zone(IntEnum):

    # 0xF0 for zone, 0x0f for port
    STRIP_1_FADER   = 0x0000
    STRIP_1_SELECT  = 0x0001
    STRIP_1_MUTE    = 0x0000
    STRIP_1_SOLO    = 0x0003
    STRIP_1_AUTO    = 0x0004
    STRIP_1_VSEL    = 0x0005
    STRIP_1_INS     = 0x0006
    STRIP_1_REC     = 0x0007

    STRIP_2_FADER   = 0x0100
    STRIP_2_SELECT  = 0x0101
    STRIP_2_MUTE    = 0x0100
    STRIP_2_SOLO    = 0x0103
    STRIP_2_AUTO    = 0x0104
    STRIP_2_VSEL    = 0x0105
    STRIP_2_INS     = 0x0106
    STRIP_2_REC     = 0x0107

    STRIP_3_FADER   = 0x0200
    STRIP_3_SELECT  = 0x0201
    STRIP_3_MUTE    = 0x0200
    STRIP_3_SOLO    = 0x0203
    STRIP_3_AUTO    = 0x0204
    STRIP_3_VSEL    = 0x0205
    STRIP_3_INS     = 0x0206
    STRIP_3_REC     = 0x0207

    STRIP_4_FADER   = 0x0300
    STRIP_4_SELECT  = 0x0301
    STRIP_4_MUTE    = 0x0300
    STRIP_4_SOLO    = 0x0303
    STRIP_4_AUTO    = 0x0304
    STRIP_4_VSEL    = 0x0305
    STRIP_4_INS     = 0x0306
    STRIP_4_REC     = 0x0307

    STRIP_5_FADER   = 0x0400
    STRIP_5_SELECT  = 0x0401
    STRIP_5_MUTE    = 0x0400
    STRIP_5_SOLO    = 0x0403
    STRIP_5_AUTO    = 0x0404
    STRIP_5_VSEL    = 0x0405
    STRIP_5_INS     = 0x0406
    STRIP_5_REC     = 0x0407

    STRIP_6_FADER   = 0x0500
    STRIP_6_SELECT  = 0x0501
    STRIP_6_MUTE    = 0x0500
    STRIP_6_SOLO    = 0x0503
    STRIP_6_AUTO    = 0x0504
    STRIP_6_VSEL    = 0x0505
    STRIP_6_INS     = 0x0506
    STRIP_6_REC     = 0x0507

    STRIP_7_FADER   = 0x0600
    STRIP_7_SELECT  = 0x0601
    STRIP_7_MUTE    = 0x0600
    STRIP_7_SOLO    = 0x0603
    STRIP_7_AUTO    = 0x0604
    STRIP_7_VSEL    = 0x0605
    STRIP_7_INS     = 0x0606
    STRIP_7_REC     = 0x0607

    STRIP_8_FADER   = 0x0700
    STRIP_8_SELECT  = 0x0701
    STRIP_8_MUTE    = 0x0700
    STRIP_8_SOLO    = 0x0703
    STRIP_8_AUTO    = 0x0704
    STRIP_8_VSEL    = 0x0705
    STRIP_8_INS     = 0x0706
    STRIP_8_REC     = 0x0707
    
    #keyboard shortcuts
    CTRL_CLTCH      = 0x0800
    SHIFT_ADD       = 0x0801
    EDITMODE        = 0x0802
    UNDO            = 0x0803
    ALT_FILE        = 0x0804
    OPTION_ALL      = 0x0805
    EDITTOOL        = 0x0806
    SAVE            = 0x0807
    
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

    MON_INPUT_3     = 0x1100
    MON_INPUT_2     = 0x1101
    MON_INPUT_1     = 0x1102
    MON_MUTE        = 0x1103
    MON_DISCRETE    = 0x1104




