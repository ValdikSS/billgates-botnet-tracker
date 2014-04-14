#!/usr/bin/env python2
'''
This tool is intended to monitor BillGates botnet control commands.

This module can communicate with "Melinda" servers (DDoS module).
"Melinda" module is usually called atddd, ksapdd, kysapdd, sksapdd,
skysapdd, ferwfrre, gfhddsfew, gfhjrtfyhuf, rewgtf3er4t or sdmfdsfhjfe.
'''
from __future__ import print_function
import socket
import time
import re
import struct
import sys

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

def decode_command(data):
    global server
    command = data[0]
    if command == "\x01":
        # DDoS!
        ddos_type = data[25]
        if ddos_type == "\x80":
            ddos_type = "TCP"
        elif ddos_type == "\x81":
            ddos_type = "UDP"
        elif ddos_type == "\x82":
            ddos_type = "ICMP"
        elif ddos_type == "\x83":
            ddos_type = "DNS method 1"
        elif ddos_type == "\x84":
            ddos_type = "DNS method 2"

        ip = str(ord(data[26])) + '.' + str(ord(data[27])) + '.' + str(ord(data[28])) +\
            '.' + str(ord(data[29]))
        port = struct.unpack('H', data[30:32])[0]
        myprint("Got DDoS command! Type:", ddos_type, "IP:", str(ip + ':' + str(port)))

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

def melinda():
    global server
    servers = (('202.103.178.76', 10991), ('121.12.110.96', 10991), ('112.90.252.76', 10991), \
        ('112.90.22.197', 10991), ('112.90.252.79', 10991))

    server = servers[0]

    if len(sys.argv) >= 2 and int(sys.argv[1]) < len(servers):
        server = servers[int(sys.argv[1])]
        
    s = socket.create_connection(server)
    myprint("Connected to server", server)
    s.sendall(hello)
    myprint("Sent hello")

    while True:
        data = s.recv(4096)
        s.sendall(ping)
        time.sleep(0.1)
        decode_command(data)

if __name__ == "__main__":
    while True:
        try:
            melinda()
        except socket.error:
            myprint("Connection lost. Reconnecting...")
            time.sleep(5)