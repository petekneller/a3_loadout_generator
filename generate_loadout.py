#! /bin/env python

# Requires the following python libs to be installed:
# - pyyaml
# - jinja2

from functools import reduce
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import sys
import yaml

config_dir_name = sys.argv[1]
output_dir_name = sys.argv[2]

def read_file(dir_entry):
    print(f"Reading [{dir_entry}]")

    try:
        with open(dir_entry, "r") as config_file:
            configs = yaml.safe_load_all(config_file)
            return [(config['name'], config) for config in configs]

    except Exception as exc:
        print(f"Exception raised in [{dir_entry}]: {exc}")

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

def resolve_config(config_name, configs):
    config = configs[config_name]
    if "extends" in config:
        print(f"Config {config_name} extends [{config['extends']}]")
        inherited = [resolve_config(base_name, configs) for base_name in config["extends"]]
    else:
        inherited = []

    inherited.append(config)
    return reduce(merge_configs, inherited)

def main(config_dir_name, output_dir_name):
    configs = dict([config
                    for entry in Path(config_dir_name).iterdir()
                    for config in read_file(entry)])

    env = Environment(
        loader=FileSystemLoader("."),
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True
    )
    vanilla_template = env.get_template("arsenal_import.vanilla.tmpl")
    ace_template = env.get_template("arsenal_import.ace.tmpl")
    weight_template = env.get_template("weights.tmpl")

    with open("weights.yaml", "r") as weights_file:
        weights = yaml.safe_load(weights_file)
        weights = dict([(key, value / 10 / 2.205) for key, value in weights.items()])

        for config_name in iter(configs):
            print(f"Processing config [{config_name}]")
            config = resolve_config(config_name, configs)

            file_name = Path(output_dir_name) / f"{config_name}.vanilla.sqf"
            with open(file_name, "w") as output_file:
                print(f"Writing loadout [{file_name}]")
                output_file.write(vanilla_template.render(config=config))

            file_name = Path(output_dir_name) / f"{config_name}.ace.sqf"
            with open(file_name, "w") as output_file:
                print(f"Writing loadout [{file_name}]")
                output_file.write(ace_template.render(config=config))

            file_name = Path(output_dir_name) / f"{config_name}.weights.yaml"
            with open(file_name, "w") as output_file:
                print(f"Writing loadout [{file_name}]")
                output_file.write(weight_template.render(config=config, weights=weights))

main(config_dir_name, output_dir_name)
