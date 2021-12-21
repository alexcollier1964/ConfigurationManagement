#!/usr/bin/env python3

# Build config files based on a JSON input file

import json
from jinja2 import Template, Environment, FileSystemLoader

conffn = "conf.json"
conftype = "vhost"
tplfile = conftype + ".jinja"

# File handling for the template file
file_loader = FileSystemLoader('.')
env = Environment(loader=file_loader)
template = env.get_template(tplfile)

# Load the JSON file
with open(conffn) as json_fh:
    # Create the JSON object and decode the loaded file
    data = json.load(json_fh)
    # Loop over customer and apps and emit a config file for each pairing
    for cust, custdata in data["config"].items():
        for apptag, appdata in data["config"][cust].items():
            custapp = cust + '-' + apptag
            conffile = custapp + "-" + conftype + ".conf"
            # Assemble the values to be passed to the templater
            templatevalues = {
                'custapp'  : custapp,
                'cust'     : cust,
                'apptag'   : apptag,
                'upstream' : appdata['upstream'],
                'external' : appdata['external']
            }
            # Render the template into the confout variable and write it out to the config file
            confout = template.render(templatevalues=templatevalues)
            with open(conffile, 'w') as conf_fh:
                print(confout, file=conf_fh)