#!/usr/bin/env python3
"""
### REPLY ###
Starting Nping 0.7.70 ( https://nmap.org/nping ) at 2018-10-23 09:52 UTC
SENT (0.0057s) TCP 172.17.0.6:1410 > 216.58.208.142:443 S ...
RCVD (0.2066s) TCP 216.58.208.142:443 > 172.17.0.6:1410 SA ...

Max rtt: 200.910ms | Min rtt: 200.910ms | Avg rtt: 200.910ms
Raw packets sent: 1 (40B) | Rcvd: 1 (44B) | Lost: 0 (0.00%)
Nping done: 1 IP address pinged in 1.01 seconds

### NO REPLY ###
Starting Nping 0.7.70 ( https://nmap.org/nping ) at 2018-10-23 14:20 BST
SENT (0.1588s) TCP 172.31.8.96:38901 > 157.240.22.35:5555 S ...

Max rtt: N/A | Min rtt: N/A | Avg rtt: N/A
Raw packets sent: 1 (40B) | Rcvd: 0 (0B) | Lost: 1 (100.00%)
Nping done: 1 IP address pinged in 1.16 seconds
"""
import os

class Tcp():
    """__init__ and run_tcp methods"""
    def __init__(self, port, target):
        self.port = port
        self.target = target

    def run_tcp(self):
        """run tcp probe"""
        tcp_cmd = os.popen('sudo nping --tcp -c 1 --dest-port {} {}'.format(self.port, self.target))
        splitted_values = tcp_cmd.read().split()
        return splitted_values
