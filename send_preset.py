#!/usr/bin/env python

import argparse
import sys
import time

from rtmidi.midiutil import open_midioutput


def main(args=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--port", help="MIDI output port")
    ap.add_argument("-m", "--memory", help="The memory number")
    ap.add_argument("-f", "--file", help="The file to send")
    args = ap.parse_args()

    midiout, name = open_midioutput(args.port)
    print("Opened port '%s'." % name)

    f = open(args.file, "r")
    lines = f.readlines()

    for line in lines:
        line = line.replace("\n", "")
        if line == "{" or line == "" or line == "}" or line == "	\"device\": \"MiniLab mkII\",":
            continue
        print(line)
        tmp, value = line.replace('"','').replace(',','').replace(':','').split()
        control, param = tmp.split('_');
        strToSend = "F0 00 20 6B 7F 42 02 00 {:02X} {:02X} {:02X} F7".format(int(param), int(control), int(value))
        print("Sending %s" % strToSend)
        midiout.send_message(bytearray.fromhex(strToSend))

    data = bytearray.fromhex("F0 00 20 6B 7F 42 06 {:02X} F7".format(int(args.memory)))
    midiout.send_message(data)

    time.sleep(0.5)
    midiout.close_port()
    del midiout


if __name__ == "__main__":
    sys.exit(main() or 0)
