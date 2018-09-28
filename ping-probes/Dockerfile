FROM python:3.7.0-alpine3.8
RUN pip3 install influxdb && pip3 install credPass
COPY ./network-telemetry-ping.py /var/
COPY ./.credentials.json /root/
CMD python3 /var/network-telemetry-ping.py
