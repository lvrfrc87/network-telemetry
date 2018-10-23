FROM python:3.7.0-alpine3.8
RUN apk --no-cache add nmap-nping=7.70-r1
RUN pip3 install influxdb==5.2.0 && pip3 install credPass==1.1 && pip3 install pyyaml==4.2b4
RUN mkdir /var/classes
COPY ./network_telemetry_tcp.py /var/
COPY ./classes /var/classes
COPY ./.credentials.json /root/
COPY ./var/targets.yaml /var/
CMD ["/usr/local/bin/python3", "/var/network_telemetry_tcp.py"]
