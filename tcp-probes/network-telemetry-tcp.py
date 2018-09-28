#!/usr/bin/env python3
import os, re, datetime, time, threading
from influxdb import InfluxDBClient
from credPass import credPass

def facebook():
    while True:
        nping = os.popen('nping --tcp -c 1 --dest-port 443 facebook.com')
        npingRead = nping.read()
        for i in npingRead.splitlines():
            if 'SENT' in i:
                rttTime = reTime.search(i)
                value = float(rttTime.group())
                if value:
                    pass
                else:
                    value = float(0.000)
                jsonBodyRtt = [
                 {
                     "measurement": "rtt_tcp_sent",
                     "tags": {
                         "target": "facebook.com",
                     },
                     "time": str(datetime.datetime.today()),
                     "fields": {
                         "value": value
                     }
                 }
                ]
                client.write_points(jsonBodyRtt)
            elif 'RCVD' in i:
                rttTime = reTime.search(i)
                value = float(rttTime.group())
                if value:
                    pass
                else:
                    value = float(0.000)
                jsonBodyRtt = [
                 {
                     "measurement": "rtt_tcp_rcvd",
                     "tags": {
                         "target": "facebook.com",
                     },
                     "time": str(datetime.datetime.today()),
                     "fields": {
                         "value": value
                     }
                 }
                ]
                client.write_points(jsonBodyRtt)
        time.sleep(2)

def google():
    while True:
        nping = os.popen('nping --tcp -c 1 --dest-port 443 google.com')
        npingRead = nping.read()
        for i in npingRead.splitlines():
            if 'SENT' in i:
                rttTime = reTime.search(i)
                value = float(rttTime.group())
                if value:
                    pass
                else:
                    value = float(0.000)
                jsonBodyRtt = [
                 {
                     "measurement": "rtt_tcp_sent",
                     "tags": {
                         "target": "google.com",
                     },
                     "time": str(datetime.datetime.today()),
                     "fields": {
                         "value": value
                     }
                 }
                ]
                client.write_points(jsonBodyRtt)
            elif 'RCVD' in i:
                rttTime = reTime.search(i)
                value = float(rttTime.group())
                if value:
                    pass
                else:
                    value = float(0.000)
                jsonBodyRtt = [
                 {
                     "measurement": "rtt_tcp_rcvd",
                     "tags": {
                         "target": "google.com",
                     },
                     "time": str(datetime.datetime.today()),
                     "fields": {
                         "value": value
                     }
                 }
                ]
                client.write_points(jsonBodyRtt)
        time.sleep(2)

if __name__ == '__main__':
    reTime = re.compile(r'(\d+\.\d+)')
    influx = credPass()
    client = InfluxDBClient(host='db', port=8086, username=influx.load('influxdb','username'), password=influx.load('influxdb','password'), database='network_telemetry')
    fbDef = threading.Thread(name='facebook', target=facebook)
    glDef = threading.Thread(name='google', target=google)
    fbDef.start()
    glDef.start()
