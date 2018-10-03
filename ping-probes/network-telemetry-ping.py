#!/usr/bin/env python3
import os, re, datetime, time, threading, yaml
from influxdb import InfluxDBClient
from credPass import credPass

def threadPing():
    pingThreads = []
    for region,list in dicTargets.items():
        for target in list:
            threadTargets = threading.Thread(target=ping, args=(region,target))
            threadTargets.start()
            pingThreads.append(threadTargets)

def ping(region,target):
    influx = credPass()
    client = InfluxDBClient(host='db', port=8086, username=influx.load('influxdb','username'), password=influx.load('influxdb','password'), database='network_telemetry')
    rttTime = re.compile(r'(time=)(\d+\.\d+)')
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
             "region": region
         },
         "time": str(datetime.datetime.today()),
         "fields": {
             "value": value
         }
     }
    ]
    client.write_points(jsonBody)

if __name__ == '__main__':
    dicTargets = yaml.load(open('var/targets.yaml', 'rb'))
    while True:
        threadPing()
        time.sleep(3)
