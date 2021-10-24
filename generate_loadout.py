#! /bin/env python

# Requires the following python libs to be installed:
# - pyyaml
# - jinja2

from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import sys
import yaml

config_dir_name = sys.argv[1]
output_dir_name = sys.argv[2]

def read_config(dir_entry):
    print(f"Reading: {dir_entry}")

    try:
        with open(dir_entry, "r") as config_file:
            return yaml.safe_load(config_file)

    except Exception as exc:
        print(f"Exception raised in {dir_entry}: {exc}")

configs = [read_config(entry) for entry in Path(config_dir_name).iterdir()]
env = Environment(
    loader=FileSystemLoader("."),
    keep_trailing_newline=True,
    trim_blocks=True,
    lstrip_blocks=True
)
template = env.get_template("arsenal_import.sqf.tmpl")

for config in configs:
    file_name = Path(output_dir_name) / config['name']
    with open(file_name, "w") as output_file:
        print(f"Writing loadout: {file_name}")
        output_file.write(template.render(config=config))
