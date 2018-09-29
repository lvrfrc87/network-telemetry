#!/usr/bin/env bash

# INFLUXDB
docker run --name db -d \
      -e INFLUXDB_DB=network_telemetry \
      -e INFLUXDB_ADMIN_USER=root -e INFLUXDB_ADMIN_PASSWORD=supersecretpassword \
      -v $PWD/influxdb/config/influxdb.conf:/etc/influxdb/influxdb.conf:ro \
      -v $PWD/influxdb:/var/lib/influxdb \
      influxdb

# RUN GRAFANA AND LINK TO DB
docker run -d --name=grafana --link db -p 3000:3000 -v $PWD/grafana:/var/lib/grafana grafana

# BUILD PING PROBE CONTAINER AND LINK TO DB
docker build ping-probes/ -t network-telemetry-ping:latest
docker run -d --name=ping --link db --restart=always network-telemetry-ping

# BUILD PING PROBE CONTAINER AND LINK TO DB
docker build tcp-probes/ -t network-telemetry-tcp:latest
docker run -d --name=tcp --link db --restart=always network-telemetry-tcp
