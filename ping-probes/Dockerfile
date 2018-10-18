FROM python:3.7.0-alpine3.8
RUN pip3 install influxdb==5.2.0 && pip3 install credPass==1.1 && pip3 install pyyaml==4.2b4
COPY ./network_telemetry_ping.py /var/
COPY ./ping.py /var/
COPY ./.credentials.json /root/
COPY ./var/targets.yaml /var/
CMD ["/usr/local/bin/python3", "/var/network_telemetry_ping.py"]
