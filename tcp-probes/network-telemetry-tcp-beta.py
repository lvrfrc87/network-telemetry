#!/usr/bin/env python3
import os, re, datetime, time, threading, yaml
from influxdb import InfluxDBClient
from credPass import credPass

def threadPing():
    threadPing = []
    for target,port in dicTargets.items():
        threadTargets = threading.Thread(target=ping, args=(target,port))
        threadTargets.start()
        threadPing.append(threadTargets)

def ping(target, port):
    nping = os.popen('sudo nping --tcp -c 1 --dest-port {} {}'.format(port,target))
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
                     "target": target,
                 },
                 "time": str(datetime.datetime.today()),
                 "fields": {
                     "value": value
                 }
             }
            ]
            print(jsonBodyRtt)
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
                     "target": target,
                 },
                 "time": str(datetime.datetime.today()),
                 "fields": {
                     "value": value
                 }
             }
            ]
            print(jsonBodyRtt)

if __name__ == '__main__':
    dicTargets = yaml.load(open('targets.yaml', 'rb'))
    reTime = re.compile(r'(\d+\.\d+)')
    influx = credPass()
    client = InfluxDBClient(host='db', port=8086, username=influx.load('influxdb','username'), password=influx.load('influxdb','password'), database='network_telemetry')
    while True:
        threadPing()
        time.sleep(3)
