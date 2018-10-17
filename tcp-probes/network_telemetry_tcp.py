#!/usr/bin/env python3
''' Code for tcp probe. The command is executed every
    5 seconds and the RTT is extraxcted via regex.
    The value is stored in one or more InfluxDb instance'''
import os
import re
import datetime
import time
import threading
import yaml
from credPass import credPass
from urllib3.exceptions import NewConnectionError
from urllib3.exceptions import MaxRetryError
from requests.exceptions import ConnectionError as ApiCallError
from influxdb import InfluxDBClient

def thread_tcp():
    ''' multithreading tcp probes '''
    tcp_threads = []
    for region, values in dic_targets.items():
        for target, port in values.items():
            thread_targets = threading.Thread(target=tcp, args=(target, port, region))
            thread_targets.start()
            tcp_threads.append(thread_targets)

def tcp(target, port, region):
    ''' tcp probe execution and regex rtt '''
    nping = os.popen('nping --tcp -c 1 --dest-port {} {}'.format(port, target))
    nping_read = nping.read()
    json_body = []
    for i in nping_read.splitlines():
        if 'sent' in i:
            rtt_time = re_time.search(i)
            value_sent = float(rtt_time.group())
            if value_sent:
                pass
            else:
                value_sent = float(0.000)
            json_body_rtt_sent = [
                {
                    "measurement": "rtt_tcp_sent",
                    "tags": {
                        "target": target,
                        "region": region},
                    "time": str(datetime.datetime.today()),
                    "fields": {
                        "value": value_sent}
                }
            ]
            json_body.append(json_body_rtt_sent)
        elif 'rcvd' in i:
            rtt_time = re_time.search(i)
            value_rcvd = float(rtt_time.group())
            if value_rcvd:
                pass
            else:
                value_rcvd = float(0.000)
            json_body_rtt_rcvd = [
                {
                    "measurement": "rtt_tcp_rcvd",
                    "tags": {
                        "target": target,
                        "region": region},
                    "time": str(datetime.datetime.today()),
                    "fields": {
                        "value": value_rcvd}
                }
            ]
            json_body.append(json_body_rtt_rcvd)
        for client in db_list:
            try:
                connect = InfluxDBClient(
                    host=client,
                    port=8086,
                    username=influx.load(client, 'username'),
                    password=influx.load(client, 'password'),
                    database='network_telemetry')
                for json in json_body:
                    connect.write_points(json)
            except (NewConnectionError, MaxRetryError, ApiCallError) as error:
                print(error)

if __name__ == '__main__':
    dic_targets = yaml.load(open('var/targets.yaml', 'rb'))
    re_time = re.compile(r'(\d+\.\d+)')
    influx = credPass()
    # Add DB hostname/IP to db_list in case you want send result to more than one DB.
    # Remember to update .credential.json with DBs login.
    db_list = ['influxdb']
    while True:
        thread_tcp()
        time.sleep(5)
