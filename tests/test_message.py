from fhui.message import *

class TestMessageConverter:

    def test_ping(self):
        data = [0x90, 0x00, 0x00]
        m = midi2messages(data)
        assert m == [Ping()]

    def test_ping_response(self):
        data=[0x90, 0x00, 0x7f]
        m = midi2messages(data)
        assert m == [PingReply()]

    def test_small_display(self):
        data = [0xf0, 0x00, 0x00, 0x66, 0x05, 0x00, 0x10, 0x03, 
                0x54, 0x72, 0x6b, 0x31, 0xf7]

        m = midi2messages(data)

        assert len(m) == 1

        assert m[0] == SmallDisplayUpdate(
                    ident=SmallDisplayTarget.STRIP_4,
                    data=list(map(ord, "Trk1")))
        



