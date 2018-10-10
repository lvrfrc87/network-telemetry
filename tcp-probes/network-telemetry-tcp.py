#!/usr/bin/env python3
import os, re, datetime, time, threading, yaml
from influxdb import InfluxDBClient
from credPass import credPass

def threadTcp():
    tcpThreads = []
    for region,dict in dicTargets.items():
        for target,port in dict.items():
            threadTargets = threading.Thread(target=tcp, args=(target,port,region))
            threadTargets.start()
            tcpThreads.append(threadTargets)

def tcp(target,port,region):
    nping = os.popen('nping --tcp -c 1 --dest-port {} {}'.format(port,target))
    npingRead = nping.read()
    jsonBody = []
    for i in npingRead.splitlines():
        if 'SENT' in i:
            rttTime = reTime.search(i)
            valueSENT = float(rttTime.group())
            if valueSENT:
                pass
            else:
                valueSENT = float(0.000)
            jsonBodyRttSENT = [
             {
                 "measurement": "rtt_tcp_sent",
                 "tags": {
                     "target": target,
                     "region": region
                 },
                 "time": str(datetime.datetime.today()),
                 "fields": {
                     "value": valueSENT
                 }
             }
            ]
            jsonBody.append(jsonBodyRttSENT)
        elif 'RCVD' in i:
            rttTime = reTime.search(i)
            valueRCVD = float(rttTime.group())
            if valueRCVD:
                pass
            else:
                valueRCVD = float(0.000)
            jsonBodyRttRCVD = [
             {
                 "measurement": "rtt_tcp_rcvd",
                 "tags": {
                     "target": target,
                     "region": region
                 },
                 "time": str(datetime.datetime.today()),
                 "fields": {
                     "value": valueRCVD
                 }
             }
            ]
            jsonBody.append(jsonBodyRttRCVD)
        for client in dbList:
            try:
                connect = InfluxDBClient(host=client, port=8086, username=influx.load(client,'username'), password=influx.load(client,'password'), database='network_telemetry')
                for json in jsonBody:
                    connect.write_points(json)
            except:
                pass

if __name__ == '__main__':
    dicTargets = yaml.load(open('var/targets.yaml', 'rb'))
    reTime = re.compile(r'(\d+\.\d+)')
    influx = credPass()
    # Add DB hostname/IP to dbList in case you want send result to more than one DB.
    # Remember to update .credential.json with DBs login.
    dbList = ['db']
    while True:
        threadTcp()
        time.sleep(5)
