import pytest

from fhui.vpot import VPot, VPotRingAspect, VPotDisplayUpdate


class TestVPotDisplay:
    pass
    # def test_display_update(self):
    #     display = VPot()
    #     update = VPotDisplayUpdate(encoder_led=False, ring_aspect=VPotRingAspect.) 
    #     display.update_raw(0x14)
    #     assert display.encoder_led == False
    #     assert display.ring_aspect == VPotRingAspect.REL_L2

    #     display.update_raw(0x25)
    #     assert display.encoder_led == False
    #     assert display.ring_aspect == VPotRingAspect.MAG_5

    # def test_encoder_led(self):
    #     aspect, led = VPotRingAspect.decode(0x41)
    #     assert aspect == VPotRingAspect.ABS_L5
    #     assert led is True
        
