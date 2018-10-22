import yaml
import time
import threading
from classes.ping_alpine import Ping
from classes.influx_body import JsonBuilder
from influxdb import InfluxDBClient
from credPass import credPass
from urllib3.exceptions import NewConnectionError
from urllib3.exceptions import MaxRetryError
from requests.exceptions import ConnectionError as ApiCallError

def thread_ping():
    """ threading for ping probes """
    ping_threads = []
    for region, target_list in dic_targets.items():
        for target in target_list:
            thread_targets = threading.Thread(target=influxdb_call, args=(target, region))
            thread_targets.start()
            ping_threads.append(thread_targets)

def influxdb_call(target, region):
    splitted_values = Ping(target).run_ping()
    json_body = JsonBuilder(splitted_values, target, region).json_body()
    for client in db_list:
        try:
            connect  = InfluxDBClient(
                host=client,
                port=8086,
                username=credPass().load(client, 'username'),
                password=credPass().load(client, 'password'),
                database='network_telemetry')
            connect.write_points(json_body)
        except (NewConnectionError, MaxRetryError, ApiCallError) as error:
            print(error)

if __name__ == '__main__':
    dic_targets = yaml.load(open('var/targets.yaml', 'rb'))
    db_list = ['db']
    while True:
        thread_ping()
