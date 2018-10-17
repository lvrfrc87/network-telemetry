#!/usr/bin/env python3
''' Code for ping probe. The command is executed every
    3 seconds and the RTT is extraxcted via regex.
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

def thread_ping():
    ''' multithreading ping probes '''
    ping_threads = []
    for region, target_list in dic_targets.items():
        for target in target_list:
            thread_targets = threading.Thread(target=ping_probe, args=(region, target))
            thread_targets.start()
            ping_threads.append(thread_targets)

def ping_probe(region, target):
    ''' ping probe execution and regex rtt '''
    ping = os.popen("ping -c 1 {}".format(target))
    rtt = rtt_time.search(ping.read())
    if rtt:
        value = float(rtt.group(2))
    else:
        value = float(0.000)
    json_body_ping = [
        {
            "measurement": "ping_rtt",
            "tags": {
                "target": target,
                "region": region},
            "time": str(datetime.datetime.today()),
            "fields": {
                "value": value}
        }
    ]
    for client in db_list:
        try:
            connect = InfluxDBClient(
                host=client,
                port=8086,
                username=influx.load(client, 'username'),
                password=influx.load(client, 'password'),
                database='network_telemetry')
            connect.write_points(json_body_ping)
        except (NewConnectionError, MaxRetryError, ApiCallError) as error:
            print(error)
if __name__ == '__main__':
    dic_targets = yaml.load(open('var/targets.yaml', 'rb'))
    rtt_time = re.compile(r'(time=)(\d+\.\d+)')
    influx = credPass()
    # Add DB hostname/IP to db_list in case you want send result to more than one DB.
    # Remember to update .credential.json with DBs login.
    db_list = [
        'db'
        ]
    while True:
        thread_ping()
        time.sleep(3)
