
import pygame.midi

import sys
sys.path.insert(0, '.')

from optparse import OptionParser, OptionGroup
import sys
import re

from time import sleep

from threading import Thread

from fhui.surface import Surface, SurfaceDelegate
from fhui.zones import ZonePort
from fhui.small_display import SmallDisplayTarget

import codecs

DEFAULT_MIDI_IN_RX=r'^.*HUI In$'
DEFAULT_MIDI_OUT_RX=r'^.*HUI Out$'


if not pygame.midi.get_init():
    pygame.midi.init()


def print_endpoint(index: int):
    f, n, xi, xo, op = pygame.midi.get_device_info(index)
    dirn = None
    if xi > 0:
        dirn = "IN"
    else:
        dirn = "OUT"

    log_out("[INFO] %i - %s : %s (%s)" % (index, codecs.decode(f, 'utf8'), codecs.decode(n, 'utf8'), dirn))


def iterate_endpoints():
    for i in range(pygame.midi.get_count()):
        f, n, xi, xo, op = pygame.midi.get_device_info(i)
        yield (i, codecs.decode(f, 'utf8'), codecs.decode(n, 'utf8'), xi, xo, op)


def list_endpoints():
    log_out("Inputs:")
    for index, interface, name, is_input, is_output, is_open in iterate_endpoints():
        if is_input == 1:
            print("%i - %s : %s" % (index, interface, name))

    log_out("")
    log_out("Outputs:")
    for index, interface, name, is_input, is_output, is_open in iterate_endpoints():
        if is_output == 1:
            log_out("%i - %s : %s" % (index, interface, name))


def get_default_input():
    port = None
    for i, _, name, xi, _, _ in iterate_endpoints():
        if xi == 1 and re.fullmatch(DEFAULT_MIDI_IN_RX, name) is not None:
            port = i
            break
    return port


def get_default_output():
    port = None
    for i, _, name, _, xo, _ in iterate_endpoints():
        if xo == 1 and re.match(DEFAULT_MIDI_OUT_RX, name) is not None:
            port = i
            break
    return port

class MonitorSurfaceDelegate(SurfaceDelegate):
    def __init__(self):
        self.time_display_str = "OFF-LINE"
        self.online = True
        self.main_display = ""
        self.small_displays = [""] * 9

    def go_online(self, surface):
        self.online = True

    def go_offline(self, surface):
        self.online = False

    def small_display_changed(self, surface, ident, text):
        self.small_displays[ident] = text

    def time_display_changed(self, surface, new_value):
        self.time_display_str = new_value.display_string()

    def main_display_changed(self, surface, _zone, _value):
        self.main_display = surface.main_display.display_string()

    
argv_parser = OptionParser()

group = OptionGroup(argv_parser, "MIDI Input-Output Selection", 
        "Select MIDI Input and Output ports for the virtual surface. "
        "By default the ports are scanned by name and ports with names "
        "matching %s and %s are selected. Use the -l option to list ports "
        "by their IDs if you need to override this." 
        % (DEFAULT_MIDI_IN_RX, DEFAULT_MIDI_OUT_RX))

group.add_option("-l", "--list", dest="list_endpoints", action="store_true", 
        help="List MIDI endpoints")

group.add_option("-i", "--input-id", dest="input_id",
        default=get_default_input(),
        help="Select input by PyGame MIDI ID (Default=%default)")
group.add_option("-o", "--output-id", dest="output_id",
        default=get_default_output(),
        help="Select output by PyGame MIDI ID (Default=%default)")

argv_parser.add_option_group(group)

if __name__ == '__main__':

    (options, args) = argv_parser.parse_args()
    
    if options.list_endpoints:
        list_endpoints()
        exit(0)

    if options.input_id is None:
        print("[FATAL] MIDI Input port not selected", file=sys.stderr)
        exit(-1)

    if options.output_id is None:
        print("[FATAL] MIDI Output port not selected", file=sys.stderr)
        exit(-1)
    
    
    delegate = MonitorSurfaceDelegate()
 
    run_in_bg = True
    
    midi_in = pygame.midi.Input(options.input_id)
    midi_out = pygame.midi.Output(options.output_id)
        
    surface = Surface(midi_input=midi_in, midi_output=midi_out, 
            delegate=delegate)
        
    def background_run():
        surface.send_reset()

        while run_in_bg:
            surface.run()

        midi_in.close()
        midi_out.close()


    def key_down_up(zoneport: ZonePort, delay=0.05):
        surface.key_down(zoneport, True)
        sleep(delay)
        surface.key_up(zoneport, False)


    bg_thread = Thread(target= background_run)
    bg_thread.start()

    while True:
        prompt = "Online> "
        if not delegate.online:
            prompt = "Offline> "

        command = input(prompt)

        words = command.split(" ")
        if words[0] in ['quit', 'q']:
            run_in_bg = False

            break
        elif words[0] in ['time', 't']:
            print(delegate.time_display_str)
        
        elif words[0] in ['main', 'm']:
            print(delegate.main_display)

        elif words[0] in ['disp', 'd']:
            for x in range(9):
                if 0 <= x <= 7:
                    print("Strip %i: %s" % (x, delegate.small_displays[x]))
                else:
                    print("Sel-Asgn: %s" % delegate.small_displays[8] )

        elif words[0] in ['key', 'k']:
            zone = int(words[1], base=16)
            port = int(words[2], base=16)
            zoneport = ZonePort.from_zone_port(zone, port)
            key_down_up(zoneport)
        elif words[0] in ['p', 'play']:
            key_down_up(ZonePort.PLAY)
        elif words[0] in ['s', 'stop']:
            key_down_up(ZonePort.STOP)
        elif words[0] in ['auto_fader']:
            print("Auto fader")
            key_down_up(ZonePort.AUTO_PLUGIN)
        elif words[0] == 'select':
            for w in words[1:]:
                key_down_up(ZonePort.from_zone_port(int(w), 1))
        elif words[0] == 'mute':
            for w in words[1:]:
                key_down_up(ZonePort.from_zone_port(int(w), 2))
        elif words[0] in ['help', 'h', "?"]:
            print("q: quit")
            print("h: help")
            print("t: time")
            print('d: small display')
            print('m: main display')
            print('p: play')
            print('s: stop')
            print('select CHAN... : select channel(s)')
            print('mute CHAN... : mute channel(s)')
            print("key ZONE PORT: press and release a key")

    
