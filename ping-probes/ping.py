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
7 - Delta between Min and Max response time
"""
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
7 - Delta between Min and Max response time
"""
import os
import datetime
import re

class Ping():
    """__init__ and run_ping methods"""
    def __init__(self, target, region):
        self.target = target
        self.region = region

    def run_ping(self):
        """ run ping command and extract values"""
        # -w for timeout in Alpine
        ping_cmd = os.popen("ping -c 1 -w 1 {}".format(self.target))
        regex = re.compile(r'\d+\.?\d?')
        output = ping_cmd.read()
        values = output.split()
        if 'time=' in output:
            json_body = [
                {
                    "measurement": "ping_rtt",
                    "tags": {
                        "host": self.target,
                        "region": self.region},
                    "time": str(datetime.datetime.today()),
                    "fields": {
                        "transmitted": float(values[19]),
                        "received": float(values[22]),
                        "loss": float(regex.search(values[25]).group()),
                        "min": float(values[31].split("/")[0]),
                        "avg": float(values[31].split("/")[1]),
                        # "stddev": float(values[31].split("/")[3]),
                        # stddev not supported in Alpine
                        "max": float(values[31].split("/")[2])}
                }
            ]
        else:
            json_body = [
                {
                    "measurement": "ping_rtt",
                    "tags": {
                        "host": self.target,
                        "region": self.region},
                    "time": str(datetime.datetime.today()),
                    "fields": {
                        "transmitted": float(1),
                        "received": float(0),
                        "loss": float(100.0),
                        "min": float(0),
                        "avg": float(0),
                        # "stddev": float(values[31].split("/")[3]),
                        # stddev not supported in Alpine
                        "max": float(0)}
                }
            ]
        return json_body
