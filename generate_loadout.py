#! /bin/env python

from functools import reduce
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import sys
import yaml

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

def verify_container_not_overflowing(container_name, config, weights, capacities):
    lowercase_container_name = container_name.lower()
    if ((lowercase_container_name in config) and ("name" in config[lowercase_container_name]) and ("contents" in config[lowercase_container_name])):
        container_class = config[lowercase_container_name]["name"]
        container_contents = config[lowercase_container_name]["contents"]
        if ((container_class in capacities) and all(map(lambda item: item in weights, container_contents.keys()))):
            total_weight = sum([(weights[item] * qty) for (item, qty) in container_contents.items()])
            capacity = capacities[container_class]
            if (total_weight > capacity):
                print(f"\x1b[1;31m{container_name} is overloaded! Weight of contents [{total_weight} lbs] exceeds capacity [{capacity} lbs]\x1b[0m")
            else:
                print(f"\x1b[32m{container_name} contents are within capacity: [{total_weight} of {capacity} lbs]\x1b[0m")
        else:
            if (container_class not in capacities):
                print(f"\x1b[1;33mNo capacity available for {lowercase_container_name} [{container_class}]; cannot validate that {lowercase_container_name} is not overloaded\x1b[0m")

            for item in container_contents.keys():
                if (item not in weights):
                    print(f"\x1b[1;33mNo weight information for item [{item}]; cannot validate that {lowercase_container_name} is not overloaded\x1b[0m")

def main(config_file_names, output_dir_name):
    configs = dict([config
                    for entry in config_file_names
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
        weights_info = yaml.safe_load(weights_file)
        weights = dict([(key, value["mass"] / 10) for key, value in weights_info.items()])
        capacities = dict([(key, value["capacity"] / 10) for key, value in weights_info.items() if ("capacity" in value)])
        magazines = [key for key, value in weights_info.items() if ("magazine" in value and value["magazine"] is True)]

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
                output_file.write(ace_template.render(config=config, magazines=magazines))

            file_name = Path(output_dir_name) / f"{config_name}.weights.yaml"
            with open(file_name, "w") as output_file:
                print(f"Writing loadout [{file_name}]")
                output_file.write(weight_template.render(config=config, weights=weights, capacities=capacities))

            verify_container_not_overflowing("Uniform", config, weights, capacities)
            verify_container_not_overflowing("Vest", config, weights, capacities)
            verify_container_not_overflowing("Backpack", config, weights, capacities)

if (__name__ == "__main__"):
    output_dir_name = sys.argv[1]
    config_file_names = sys.argv[2:]

    main(config_file_names, output_dir_name)
