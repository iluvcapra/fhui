import pygame.midi

import sys
sys.path.insert(0, '.')

from enum import Enum

from fhui.zones import ZonePort
from fhui.vpot import VPotRingAspect, VPotIdent
from fhui.main_display import MainDisplay
from fhui.small_display import SmallDisplayTarget
from fhui.time_display import TimeDisplay
from fhui.charsets import SmallDisplayCharSet, LargeDisplayCharSet
from fhui.surface import SurfaceDelegate, Surface

import mido

from optparse import OptionParser, OptionGroup
import sys
import re
from time import sleep, monotonic as now, strftime
import codecs

import fileinput


DEFAULT_MIDI_IN_RX=r'^.*HUI In$'
DEFAULT_MIDI_OUT_RX=r'^.*HUI Out$'


if not pygame.midi.get_init():
    pygame.midi.init()

script_start = now()


def log_out(m):
    print("%s (%f): %s" % (strftime("%H:%M:%S"), now() - script_start, m))


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


class LogLevels(Enum):
    DEBUG = 5
    NORMAL = 3
    ERRORS = 1


parser = OptionParser()


group = OptionGroup(parser, "MIDI Input-Output Selection", 
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

parser.add_option_group(group)

parser.add_option("-p", dest="print_pings", action='store_true', 
        help="Report ping responses", 
        default=False)


class Logger(SurfaceDelegate):

    def go_offline(self, surface):
        log_out("[STATUS] Surface OFF-LINE.")

    def go_online(self, surface):
        log_out("[STATUS] Surface ON-LINE.")

    def ping_received(self, surface):
        log_out("[PING] Received ping from host.")

    def fader_moved(self, surface, fader_id: int, new_value: int):
        log_out("[FADER] Fader %x moved to position %x." % (fader_id, new_value))

    def led_changed(self, surface, led: ZonePort, new_state: bool):
        log_out("[LED] %s %s." % (led, "ON" if new_state else "OFF"))
    
    def vpot_changed(self, surface, ident: VPotIdent, new_state: VPotRingAspect):
        log_out("[VPOT] %s changed to %s." % (ident, new_state.led_string()))

    def time_display_changed(self, surface, new_value: TimeDisplay):
        log_out("[TIME] %s" % (surface.time_display.display_string()))

    def small_display_changed(self, surface, ident: SmallDisplayTarget, text: str):
        log_out("[DISP] Small display %s \"%s\"" % (ident, text))

    def main_display_changed(self, surface, zone: int, text: str):
        log_out("[MAIN] 1: \"%s\"" % surface.main_display.line1)
        log_out("[MAIN] 2: \"%s\"" % surface.main_display.line2)

    def unrecognized_message(self, surface, message: mido.Message):
        log_out("[WARN] Unrecognized message: %s" % message)
        

if __name__ == '__main__':

    (options, args) = parser.parse_args()
    
    if options.list_endpoints:
        list_endpoints()
        exit(0)

    if options.input_id is None:
        log_out("[FATAL] MIDI Input port not selected")
        exit(-1)

    if options.output_id is None:
        log_out("[FATAL] MIDI Output port not selected")
        exit(-1)

    log_out("[INFO] Beginning run %s" % strftime("%a, %d %b %Y %H:%M:%S"))

    log_out("[INFO] Creating MIDI connections...")
    log_out("[INFO] MIDI input:")
    print_endpoint(options.input_id)

    log_out("[INFO] MIDI Out:")
    print_endpoint(options.output_id)
    
    midi_in = pygame.midi.Input(options.input_id)
    midi_out = pygame.midi.Output(options.output_id)
    
    logger = Logger()
    surface = Surface(midi_input=midi_in, midi_output=midi_out, delegate=logger)
    
    log_out("[INFO] Sending MIDI system reset...")
    surface.send_reset()
    
    sleep_factor = 0.05

    log_out("[INFO] Establishing run loop. Sleep factor %f." % (sleep_factor))

    while True:
        surface.run()
        sleep(sleep_factor)

    log_out("[INFO] Exiting...")
    midi_in.close()
    midi_out.close()
    
    del midi_in
    del midi_out



