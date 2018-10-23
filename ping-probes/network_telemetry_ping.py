#!/usr/bin/env python3
"""
modular code to run ping probes in multithread and
send result via API to one or more InfluxDB instance
"""
import threading
import yaml
from credPass import credPass
from urllib3.exceptions import NewConnectionError
from urllib3.exceptions import MaxRetryError
from requests.exceptions import ConnectionError as ApiCallError
from influxdb import InfluxDBClient
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
    """ API call to InfluxDB """
    json_body = JsonBuilder(Ping(target).run_ping(), target, region).json_body()
    for client in db_list:
        try:
            connect = InfluxDBClient(
                host=client,
                port=8086,
                username=credPass().load(client, 'username'),
                password=credPass().load(client, 'password'),
                database='network_telemetry')
            connect.write_points(json_body)
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
        thread_ping()
