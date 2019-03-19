#!/usr/bin/env python3
"""
[{
    'measurement': 'ping_rtt',
    'tags': {
        'host': 'www.youtube.com',
        'region': 'aws-london'},
        'time': '2018-10-23 09:46:11.500537',
        'fields': {
        'transmitted': 1.0,
        'received': 1.0,
        'loss': 0.0,
        'min': 136.231,
        'avg': 136.231,
        'max': 136.231}
        }]
"""
import datetime
from classes.ping_alpine_parser import Parser

class JsonBuilder():
    "self variable extracted from ping_alpine_parser"
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
        "build json body for API call"
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
