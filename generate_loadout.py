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
    print(f"Reading [{dir_entry}]")

    try:
        with open(dir_entry, "r") as config_file:
            config = yaml.safe_load(config_file)
            return (config['name'], config)

    except Exception as exc:
        print(f"Exception raised in [{dir_entry}]: {exc}")

configs = dict([read_config(entry) for entry in Path(config_dir_name).iterdir()])
env = Environment(
    loader=FileSystemLoader("."),
    keep_trailing_newline=True,
    trim_blocks=True,
    lstrip_blocks=True
)
template = env.get_template("arsenal_import.sqf.tmpl")

def merge_configs(parent, child):
    out = parent.copy()
    for key in iter(child):
        if key not in out:
            out[key] = child[key]
        elif isinstance(out[key], dict):
            out[key] = merge_configs(out[key], child[key])
        else:
            out[key] = child[key]

    return out

def fetch_config(config_name):
    config = configs[config_name]
    if "extends" in config:
        print(f"Config {config_name} extends [{config['extends']}]")
        base_config = fetch_config(config['extends'])
        print(f"Merging base config into [{config_name}]")
        return merge_configs(base_config, config)
    else:
        return config

for config_name in iter(configs):
    file_name = Path(output_dir_name) / f"{config_name}.sqf"
    with open(file_name, "w") as output_file:
        print(f"Processing config [{config_name}]")
        config = fetch_config(config_name)
        print(f"Writing loadout [{file_name}]")
        output_file.write(template.render(config=config))
