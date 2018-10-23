#!/usr/bin/env python3
"""
Values extracted in float datat type are:
1 - RTT packet sent
2 - RTT packet received
3 - Max RTT
4 - Min RTT
5 - Avg RTT
6 - Number packets sent
7 - Number packets recevied
8 - Number packets lost
9 - Percentage packet lost
10 - Execution time
"""
import re

class Parser():
    """__init__ and run_ping methods"""
    def __init__(self, splitted_values):
        self.splitted_values = splitted_values
        self.regex = re.compile(r'\d+\.\d+')

    def sent(self):
        """0.0057"""
        sent_rtt = float(self.regex.search(self.splitted_values[11]).group())
        return sent_rtt

    def received(self):
        """0.2066"""
        if 'RCVD' in self.splitted_values[22]:
            rcvd_rtt = float(self.regex.search(self.splitted_values[23]).group())
        else:
            rcvd_rtt = float(0)
        return rcvd_rtt

    def max_rtt(self):
        """200.910"""
        if 'RCVD' in self.splitted_values[22]:
            max_rtt = float(self.regex.search(self.splitted_values[38]).group())
        else:
            max_rtt = float(0)
        return max_rtt

    def min_rtt(self):
        """200.910"""
        if 'RCVD' in self.splitted_values[22]:
            min_rtt = float(self.regex.search(self.splitted_values[42]).group())
        else:
            min_rtt = float(0)
        return min_rtt

    def avg_rtt(self):
        """200.910"""
        if 'RCVD' in self.splitted_values[22]:
            avg_rtt = float(self.regex.search(self.splitted_values[46]).group())
        else:
            avg_rtt = float(0)
        return avg

    def sent_pckt(self):
        """1"""
        sent_p = float(self.splitted_values[50])
        return sent_p

    def rcvd_pckt(self):
        """1"""
        rcvd_p = float(self.splitted_values[54])
        return rcvd_p

    def lost_pckt(self):
        """0"""
        lost_pk = float(self.splitted_values[58])
        return lost_pk

    def lost_prc(self):
        """0.00"""
        lost_pr = float(self.regex.search(self.splitted_values[59]).group())
        return lost_pr

    def exec_time(self):
        """1.16"""
        exec_t = float(self.regex.search(self.splitted_values[67]).group())
        return exec_t
