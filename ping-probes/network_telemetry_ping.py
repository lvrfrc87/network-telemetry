#!/usr/bin/env python3
"""EU-WEST-1C - app1.net.awsieprod2.linsys.tmcs"""

import threading
import time
import yaml
from influxdb import InfluxDBClient
from credPass import credPass
from urllib3.exceptions import NewConnectionError
from urllib3.exceptions import MaxRetryError
from requests.exceptions import ConnectionError as ApiCallError
from classes.ping_alpine import Ping
from classes.influx_body import JsonBuilder

def thread_ping():
    """ threading for ping probes """
    ping_threads = []
    for region, target_list in dic_targets.items():
        for target in target_list:
            thread_targets = threading.Thread(target=influxdb_call, args=(target, region))
            thread_targets.start()
            ping_threads.append(thread_targets)

def influxdb_call(target, region):
    """ DB json body build """
    json_body = JsonBuilder(Ping(target).run_ping(), target, region).json_body()
    thread_influx(json_body)

def thread_influx(json_body):
    """ threading for db call"""
    db_threads = []
    for db_client in db_list:
        db_targets = threading.Thread(target=influx_write, args=(json_body, db_client))
        db_targets.start()
        db_threads.append(db_targets)

def influx_write(json_body, db_client):
    """write to db"""
    try:
        connect = InfluxDBClient(
            host=db_client,
            port=8086,
            username=credPass().load(db_client, 'username'),
            password=credPass().load(db_client, 'password'),
            database='network_telemetry')
        connect.write_points(json_body)
    except (NewConnectionError, MaxRetryError, ApiCallError) as error:
        print(error)

if __name__ == '__main__':
    dic_targets = yaml.load(open('/var/targets.yaml', 'rb'))
    db_list = [
        'app1.net.awsieprod2.linsys.tmcs',
        'db1.telemetry.netams1.netsys.tmcs'
        ]
    while True:
        thread_ping()
        time.sleep(1)
