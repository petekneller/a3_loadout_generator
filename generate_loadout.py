#! /bin/env python

# Requires the following python libs to be installed:
# - pyyaml
# - jinja2

import sys
import yaml
from jinja2 import Environment, FileSystemLoader

config_name = sys.argv[1];

try:
    with open("in/{}.yaml".format(config_name), "r") as config_file:
        config = yaml.safe_load(config_file)

        env = Environment(
            loader=FileSystemLoader("."),
            keep_trailing_newline=True,
            trim_blocks=True,
            lstrip_blocks=True
        )
        template = env.get_template("arsenal_import.sqf.tmpl")

        with open("out/{}.sqf".format(config_name), "w") as output_file:
            output_file.write(template.render(config=config))

except Exception as exc:
    print(f"Exception raised: {exc}")
