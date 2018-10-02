FROM python:3.7.0-alpine3.8
RUN apk update && apk add nmap-nping
RUN pip3 install influxdb && pip3 install credPass && pip3 install pyyaml
COPY ./network-telemetry-tcp.py /var/
COPY ./.credentials.json /root/
COPY ./targets.yaml /var/
CMD python3 /var/network-telemetry-tcp.py
