#!/usr/bin/env python3
import os, re, datetime, time, threading, yaml
from influxdb import InfluxDBClient
from credPass import credPass

def threadPing():
    pingThreads = []
    for i in dicTargets['targets']:
        threadTargets = threading.Thread(target=ping, args=(i,))
        threadTargets.start()
        pingThreads.append(threadTargets)

def ping(target):
    ping = os.popen("ping -c 1 {}".format(target))
    rtt = rttTime.search(ping.read())
    if rtt:
        value = float(rtt.group(2))
    else:
        value = float(0.000)
    jsonBody = [
     {
         "measurement": "ping_rtt",
         "tags": {
             "target": target,
         },
         "time": str(datetime.datetime.today()),
         "fields": {
             "value": value
         }
     }
    ]
    client.write_points(jsonBody)

if __name__ == '__main__':
    dicTargets = yaml.load(open('/var/targets.yaml', 'rb'))
    rttTime = re.compile(r'(time=)(\d+\.\d+)')
    influx = credPass()
    client = InfluxDBClient(host='db', port=8086, username=influx.load('influxdb','username'), password=influx.load('influxdb','password'), database='network_telemetry')
    while True:
        threadPing()
        time.sleep(3)
