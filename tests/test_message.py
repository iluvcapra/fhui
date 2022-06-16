from fhui.messages import MessageConverter
from fhui.main_display import MainDisplay

class TestMessageConverter:
    
    def setup(self):
        self.converter = MessageConverter()
    
    def teardown(self):
        self.converter = None

    def test_main_display_message(self):

        m = self.converter.midi2update([0xf0, 0x00, 0x00, 0x66, 0x05, 0x00,
            0x12, 0x03, 
            ord("H"), ord("e"), ord("l"), ord("l"), ord("o"),
            ord(","), ord(" "), ord("W"), ord("o"), ord("r"),
            0xf7])

        assert type(m) == list 
        assert len(m) == 1
        assert type(m[0]) == MainDisplay.Update

        assert m[0].zone == 3
        assert m[0].chardata == list(map(ord, "Hello, Wor"))

    def test_main_display_multi_message(self):
        
        zone1 = list(map(ord, "Hello, wor"))
        zone2 = list(map(ord, "ld!       "))

        m = self.converter.midi2update([0xf0, 0x00, 0x00, 0x66, 0x05, 0x00,
            0x12, 0x00] + zone1 +
            [0x01] + zone2 + [0xf7])

        assert len(m) == 2
        assert type(m[0]) == MainDisplay.Update
        assert type(m[1]) == MainDisplay.Update

    def test_small_display_message(self):
        pass
        
