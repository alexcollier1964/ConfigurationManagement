#!/usr/bin/env python3

# Build config files based on a JSON input file
# Alex Collier, Version 1, December 2021

import json
from jinja2 import Template, Environment, FileSystemLoader
import os

conffn = "conf.json" # JSON data file
conftype = "haproxy" # what sort of output to create. There must be a matching '.jinja' template file
tplfile = conftype + ".jinja"
templatevaluelist = [] # Array of template values for monolithic files. 
generatedby = os.path.basename(__file__) # basename $0
multifileset = {"vhost"} # Config types in this set are treated as multi-file items
if conftype in multifileset:
    multifile = True # If True, create a set of files using a template with simple values
else:
    multifile = False # If False, create one monolithic file using a template with looping over an array of values

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
            if multifile:
                confout = template.render(templatevalues=templatevalues, generatedby=generatedby)
                with open(conffile, 'w') as conf_fh:
                    print(confout, file=conf_fh)
            else:
                templatevaluelist.append(templatevalues)

if not multifile:
    confout = template.render(templatevalues=templatevaluelist, generatedby=generatedby)
    conffile = conftype + ".conf"
    with open(conffile, 'w') as conf_fh:
        print(confout, file=conf_fh)
