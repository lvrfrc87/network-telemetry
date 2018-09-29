#!/usr/bin/env python3
import os, re, datetime, time, threading
from influxdb import InfluxDBClient
from credPass import credPass

def facebook():
    while True:
        ping = os.popen("ping -c 1 facebook.com")
        rtt = rttTime.search(ping.read())
        if rtt:
            value = float(rtt.group(2))
        else:
            value = float(0.000)
        jsonBody = [
         {
             "measurement": "ping_rtt",
             "tags": {
                 "target": "facebook.com",
             },
             "time": str(datetime.datetime.today()),
             "fields": {
                 "value": value
             }
         }
        ]
        client.write_points(jsonBody)
        time.sleep(3)

def google():
    while True:
        ping = os.popen("ping -c 1 google.com")
        rtt = rttTime.search(ping.read())
        if rtt:
            value = float(rtt.group(2))
        else:
            value = float(0.000)
        jsonBody = [
         {
             "measurement": "ping_rtt",
             "tags": {
                 "target": "google.com",
             },
             "time": str(datetime.datetime.today()),
             "fields": {
                 "value": value
             }
         }
        ]
        client.write_points(jsonBody)
        time.sleep(3)

if __name__ == '__main__':
    rttTime = re.compile(r'(time=)(\d+\.\d+)')
    influx = credPass()
    client = InfluxDBClient(host='db', port=8086, username=influx.load('influxdb','username'), password=influx.load('influxdb','password'), database='network_telemetry')
    fbDef = threading.Thread(name='facebook', target=facebook)
    glDef = threading.Thread(name='google', target=google)
    fbDef.start()
    glDef.start()
