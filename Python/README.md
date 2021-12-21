# Build config files based on a JSON input file
## Features

- Leverages the json and jinja2 Python modules
- Transforms a JSON-based definition into a set of configuration files

## Use Case

Creating and maintaining a set of configuration files for different organisational units, each with several applications.

## Included Files
- Sample JSON file for a couple of customers with two apps each
- Template file for Nginx virtual host server block

## TODO
- Other base application support e.g. Squid
- Support for monolithic config files e.g. HAProxy