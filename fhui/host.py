from fhui.zones import ZonePort
from fhui.vpot import VPotIdent, VPotRingAspect
from fhui.small_display import SmallDisplayTarget

class Host:
    def __init__(self):
        pass

    def clear_main_display(self):
        pass

    def clear_small_display(self, target: SmallDisplayTarget):
        pass

    def set_led_state(self, port: ZonePort, state: bool):
        pass

    def write_main_display(self, line: int, text: str):
        pass

    def write_small_display(self, display: SmallDisplayTarget, text: str):
        pass

    def set_fader_position(self, fader: int, position: int):
        pass

    def set_vpot_aspect(self, vpot: VPotIdent, aspect: VPotAspect):
        pass
