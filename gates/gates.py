#!/usr/bin/env python2
'''
This tool is intended to monitor BillGates botnet control commands.

This module can communicate with "Gates" servers.
"Gates" module is usually called cupsdd or sfewfesfs.
'''
from __future__ import print_function
import socket
import time
import re
import struct
from pprint import pprint

def myprint(*args, **kwargs):
    print(time.strftime("%c"), *args, **kwargs)

def hexdump(src, length=16):
    FILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or '.' for x in range(256)])
    lines = []
    for c in xrange(0, len(src), length):
        chars = src[c:c+length]
        hex = ' '.join(["%02x" % ord(x) for x in chars])
        printable = ''.join(["%s" % ((ord(x) <= 127 and FILTER[ord(x)]) or '.') for x in chars])
        lines.append("%04x  %-*s  %s\n" % (c, length*3, hex, printable))
    return ''.join(lines)

def get_ip_addresses(ipaddrs):
    ips = re.findall("(?:[0-9]{1,3}\.){3}[0-9]{1,3}\x00.." ,ipaddrs)
    ip_list = list()
    for ip in ips:
        addr = ip[:-3]
        port = struct.unpack('H', ip[-2:])[0]
        ip_list.append((addr, port))
    return ip_list

def decode_command(data):
    command = data[0]
    if command == "\x01":
        # DDoS!
        ip_address_count = struct.unpack("B", data[0x47])[0]
        ips = get_ip_addresses(data[0x4B:])
        myprint("Got DDoS command!", ip_address_count, "Hosts:")
        pprint(ips, indent=3)

    elif command == "\x02":
        # Stop DDoS
        myprint("STOP DDoS")

    elif command == "\x04":
        # PING
        pass

    else:
        myprint("UNKNOWN COMMAND!")
        print(hexdump(data))
        save.write(hexdump(data))

hello = open('hello.bin', 'rb').read()
ping = open('ping.bin', 'rb').read()
save = open('unknown-commands.bin', 'w+b')

s = socket.create_connection(('116.10.189.246', 36008))
myprint("Connected")
s.sendall(hello)
myprint("Sent hello")
data = s.recv(1024)
myprint("Received server hello")

while True:
    s.sendall(ping)
    data = s.recv(4096)
    time.sleep(0.1)
    decode_command(data)