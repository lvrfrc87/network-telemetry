#!/usr/bin/env python3
"""
/ # ping -c 1 -w 1 10.78.65.1
PING 10.78.65.1 (10.78.65.1): 56 data bytes
64 bytes from 10.78.65.1: seq=0 ttl=254 time=1.176 ms

--- 10.78.65.1 ping statistics ---
1 packets transmitted, 1 packets received, 0% packet loss
round-trip min/avg/max = 1.176/1.176/1.176 ms
/ #
/ #
/ # ping -c 1 -w 1 8.8.8.8
PING 8.8.8.8 (8.8.8.8): 56 data bytes

--- 8.8.8.8 ping statistics ---
1 packets transmitted, 0 packets received, 100% packet loss
"""
import os

class Ping():
    """__init__ and run_ping methods"""
    def __init__(self, target):
        self.target = target

    def run_ping(self):
        ping_cmd = os.popen("ping -c 1 -t 1 {}".format(self.target))
        splitted_values = ping_cmd.read().split()
        return splitted_values
