#!/usr/bin/env python3
"""
Values extracted in float datat type are:
1 - Packet transmitted
2 - Packet received
3 - Packet loss
4 - Min response time
5 - Average response time
6 - Max response time
"""
import datetime
from classes.ping_alpine_parser import Parser

class JsonBuilder():
    def __init__(self, splitted_values, target, region):
        self.target = target
        self.region = region
        self.transmitted = Parser(splitted_values).transmitted()
        self.received = Parser(splitted_values).received()
        self.loss = Parser(splitted_values).loss()
        self.min = Parser(splitted_values).min()
        self.avg = Parser(splitted_values).avg()
        self.max = Parser(splitted_values).max()

    def json_body(self):
        json_body = [
            {
                "measurement": "ping_rtt",
                "tags": {
                    "host": self.target,
                    "region": self.region},
                "time": str(datetime.datetime.today()),
                "fields": {
                    "transmitted": self.transmitted,
                    "received": self.received,
                    "loss": self.loss,
                    "min": self.min,
                    "avg": self.avg,
                    "max": self.max}
            }
        ]
        return json_body
