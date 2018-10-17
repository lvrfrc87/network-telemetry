#!/usr/bin/env python3
''' This code render a jinja2 template for Grafana dashboard provisioning.
    All variables are taken from YAML file. File is saved in the right dicrectory
    on docker container via pipeline '''

import os
import yaml
from jinja2 import Environment, FileSystemLoader

def dashboard():
    ''' grafan json file rendering from
    jinja2 template. Variables form yaml file '''
    jinja_env = Environment(loader=FileSystemLoader('.'))
    template = jinja_env.get_template('tcp-probes/var/dashboard_template.j2')
    for region in dic_targets.keys():
        directory = 'grafana/json/'
        file = os.path.join(directory + region.upper() + '_TCP' '.json')
        with open(file, 'w+') as dashboard_file:
            dashboard_file.write(template.render(yamlVar=dic_targets))
            dashboard_file.close()

if __name__ == '__main__':
    dic_targets = yaml.load(open('tcp-probes/var/targets.yaml', 'rb'))
    dashboard()
