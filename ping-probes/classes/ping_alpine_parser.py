#!/usr/bin/env python3
"""python class to extract ping values from ping UNIX command
and returned in json format ready to be written on InfluxDVself.
Below an utput example:

PING www.google.com (216.58.216.4): 56 data bytes
64 bytes from 216.58.216.4: icmp_seq=0 ttl=42 time=130.795 ms

--- www.google.com ping statistics ---
1 packets transmitted, 1 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 130.795/130.795/130.795/0.000 ms

Values extracted in float datat type are:
1 - Packet transmitted
2 - Packet received
3 - Packet loss
4 - Min response time
5 - Average response time
6 - Max response time
"""
import re

class Parser():
    """__init__ and run_ping methods"""
    def __init__(self, splitted_values):
        self.splitted_values = splitted_values
        self.regex = re.compile(r'\d+\.?\d?')

    def transmitted(self):
        """1"""
        if 'time=' in self.splitted_values[12]:
            transmitted = float(self.splitted_values[19])
        else:
            transmitted = float(0)
        return transmitted

    def received(self):
        """1"""
        if 'time=' in self.splitted_values[12]:
            received = float(self.splitted_values[22])
        else:
            received = float(0)
        return received

    def loss(self):
        """0.0"""
        if 'time=' in self.splitted_values[12]:
            loss = float(self.regex.search(self.splitted_values[25]).group())
        else:
            loss = float(0)
        return loss

    def min(self):
        """130.795"""
        if 'time=' in self.splitted_values[12]:
            min_rtt = float(self.splitted_values[31].split("/")[0])
        else:
            min_rtt = float(0)
        return min_rtt

    def avg(self):
        """130.795"""
        if 'time=' in self.splitted_values[12]:
            avg_rtt = float(self.splitted_values[31].split("/")[1])
        else:
            avg_rtt = float(0)
        return avg_rtt

    def max(self):
        """130.795"""
        if 'time=' in self.splitted_values[12]:
            max_rtt = float(self.splitted_values[31].split("/")[2])
        else:
            max_rtt = float(0)
        return max_rtt
