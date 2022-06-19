from fhui.message import *
from fhui.vpot import VPotIdent

class TestMessageConverter:

    def test_ping(self):
        data = [0x90, 0x00, 0x00]
        m = midi2messages(data)
        assert m == [Ping()]

    def test_ping_response(self):
        data=[0x90, 0x00, 0x7f]
        m = midi2messages(data)
        assert m == [PingReply()]

    def test_small_display_update(self):
        data = [0xf0, 0x00, 0x00, 0x66, 0x05, 0x00, 0x10, 0x03, 
                0x54, 0x72, 0x6b, 0x31, 0xf7]

        m = midi2messages(data)

        assert len(m) == 1
        assert m[0] == SmallDisplayUpdate(
                    ident=SmallDisplayTarget.STRIP_4,
                    data=list(map(ord, "Trk1")))

    def test_large_display_update(self):
        
        msg1 = [0x48, 0x65, 0x6c, 0x6c, 0x6f, 0x2c, 0x20, 0x77, 0x6f, 0x72]
        msg2 = [0x6c, 0x64, 0x21, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20]

        data = [0xf0, 0x00, 0x00, 0x66, 0x05, 0x00, 0x12, 
                0x00] + msg1 + [0x01] + msg2 + [0xf7]

        m = midi2messages(data)

        assert len(m) == 2
        assert m[0] == LargeDisplayUpdate(zone=0, 
                data=list(map(ord, "Hello, wor")))

        assert m[1] == LargeDisplayUpdate(zone=1,
                data=list(map(ord, "ld!       ")))

    def test_vu_meters_update(self):
        data = [0xa0, 0x02, 0x0b]

        m = midi2messages(data)

        assert len(m) == 1
        assert m[0] == VUMeterUpdate(channel=2, 
                side=VUMeterSide.LEFT, 
                value=VUMeterValue.YELLOW_2)

    def test_timecode_display_update(self):
        data = [0xf0, 0x00, 0x00, 0x66, 0x05, 0x00, 0x11, 
                0x03, 0x02, 0x19, 0x05, 0xf7]

        m = midi2messages(data)

        assert len(m) == 1
        assert m[0] == TimecodeDisplayUpdate(
                data=[0x03,0x02,0x19,0x05])

    def test_vpot_ring_display_update(self):
        data = [0xb0, 0x1a, 0x27]

        m = midi2messages(data)

        assert len(m) == 1
        assert m[0] == VPotDisplayUpdate(
                ident=VPotIdent.PARAM_3, 
                aspect=VPotRingAspect.MAG_7)




