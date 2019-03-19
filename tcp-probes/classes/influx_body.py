#!/usr/bin/env python3
"""
[{
    'measurement': 'ping_rtt',
    'tags': {
        'host': 'google.com',
        'region': 'eu-east-1a'},
    'time': '2018-10-23 15:09:42.156060',
    'fields': {
        'transmitted': 0.0092,
        'received': 0.1502,
        'max_rtt': 141.019,
        'min_rtt': 141.019,
        'avg_rtt': 141.019,
        'packet_sent': 1.0,
        'packet_received': 1.0,
        'packet_lost': 0.0,
        'packet_lost_percent': 0.0,
        'execution_tim': 1.01}
}]
"""
import datetime
from classes.tcp_alpine_parser import Parser

class JsonBuilder():
    "self variable extracted from ping_alpine_parser"
    def __init__(self, splitted_values, target, region):
        self.target = target
        self.region = region
        self.transmitted = Parser(splitted_values).sent()
        self.received = Parser(splitted_values).received()
        self.max_rtt = Parser(splitted_values).max_rtt()
        self.min_rtt = Parser(splitted_values).min_rtt()
        self.avg_rtt = Parser(splitted_values).avg_rtt()
        self.sent_pckt = Parser(splitted_values).sent_pckt()
        self.rcvd_pckt = Parser(splitted_values).rcvd_pckt()
        self.lost_pckt = Parser(splitted_values).lost_pckt()
        self.lost_prc = Parser(splitted_values).lost_prc()
        self.exec_time = Parser(splitted_values).exec_time()

    def json_body(self):
        "build json body for API call"
        json_body = [
            {
                "measurement": "tcp_rtt",
                "tags": {
                    "host": self.target,
                    "region": self.region},
                "time": str(datetime.datetime.today()),
                "fields": {
                    "transmitted": self.transmitted,
                    "received": self.received,
                    "max_rtt": self.max_rtt,
                    "min_rtt": self.min_rtt,
                    "avg_rtt": self.avg_rtt,
                    "packet_sent": self.sent_pckt,
                    "packet_received": self.rcvd_pckt,
                    "packet_lost": self.lost_pckt,
                    "packet_lost_percent": self.lost_prc,
                    "execution_tim": self.exec_time}
            }
        ]
        return json_body
