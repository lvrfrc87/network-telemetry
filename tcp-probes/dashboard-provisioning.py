#!/usr/bin/env python3
import os, yaml
from jinja2 import Environment, FileSystemLoader

def dashboard():
    ENV = Environment(loader=FileSystemLoader('.'))
    template = ENV.get_template('tcp-probes/var/dashboard_template.j2')
    for region in dicTargets.keys():
        directory = 'grafana/json/'
        file = os.path.join(directory + region.upper() + '_TCP''.json')
        with open(file, 'w+') as dashboardFile:
            dashboardFile.write(template.render(yamlVar=dicTargets))
            dashboardFile.close()

if __name__ == '__main__':
    dicTargets = yaml.load(open('tcp-probes/var/targets.yaml', 'rb'))
    dashboard()
