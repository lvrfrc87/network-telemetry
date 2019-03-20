#!/usr/bin/env python3
''' Code for tcp probe. The command is executed every
    3 seconds and the RTT is extraxcted via regex.
    The value is stored in one or more InfluxDb instance'''

import time
import threading
import yaml
from urllib3.exceptions import NewConnectionError
from urllib3.exceptions import MaxRetryError
from requests.exceptions import ConnectionError as ApiCallError
from credPass import credPass
from influxdb import InfluxDBClient
from classes.tcp_alpine import Tcp
from classes.influx_body import JsonBuilder

def thread_tcp():
    ''' multithreading tcp probes '''
    tcp_threads = []
    for region, values in dic_targets.items():
        for target, port in values.items():
            thread_targets = threading.Thread(target=influxdb_call, args=(target, port, region))
            thread_targets.start()
            tcp_threads.append(thread_targets)

def influxdb_call(target, region):
    """ DB json body build """
    json_body = JsonBuilder(Tcp(port, target).run_tcp(), target, region).json_body()
    thread_influx(json_body)

def thread_influx(json_body):
    """ threading for db call"""
    db_threads = []
    for db_client in db_list:
        db_targets = threading.Thread(target=influx_write, args=(json_body, db_client))
        db_targets.start()
        db_threads.append(db_targets)

def influxdb_call(target, port, region):
    """ write to db"""
        try:
            connect = InfluxDBClient(
                host=client,
                port=8086,
                username=credPass().load(client, 'username'),
                password=credPass().load(client, 'password'),
                database='network_telemetry')
            for json in json_body:
                connect.write_points(json)
        except (NewConnectionError, MaxRetryError, ApiCallError) as error:
            print(error)

if __name__ == '__main__':
    dic_targets = yaml.load(open('/var/targets.yaml', 'rb'))
    # Add DB hostname/IP to db_list in case you want send result to more than one DB.
    # Remember to update .credential.json with DBs login.
    db_list = [
        'db'
        ]
    while True:
        thread_tcp()
        time.sleep(3)
