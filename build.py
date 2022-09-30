# Copyright (c) 2022 Chuang Caleb
# http://github.com/chuangcaleb
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import sys
import os
from typing import Dict
import yaml

config_path = "config.yaml"


def strip_ext(s):
    """ Strip file extension from file name string """
    return ".".join(s.split(".")[:-1])


def load_config(config: Dict, field: str):

    if field not in config:
        sys.exit(
            f'\033[91mERROR: The "{field}" field was not defined in {config_path}\033[0m')

    value = config[field]

    if not value:
        sys.exit(
            f'\033[91mERROR: The "{field}" field is empty\033[0m')

    return value


# -------------------------------- Load config ------------------------------ #


with open(config_path, 'r') as f:

    config = yaml.safe_load(f)

    structure_list = load_config(config, "structure")
    sections_dir = load_config(config, "sections_dir")
    output_path = load_config(config, "output_path")

# --------------------------- Read the sections dir ------------------------- #

fountain_files = {}

for root, dirs, files in os.walk(sections_dir):

    # rel_dir = os.path.relpath(root, sections_dir)

    for file in files:
        fountain_files.update({
            strip_ext(file): os.path.join(root, file)
        })
        # fountain_filenames.append(strip_ext(file))
        # fountain_filepaths.append(os.path.join(root, file))
        # (strip_ext(file), os.path.join(rel_dir, file)))

# ------------------------------- Load sections ------------------------------ #

sections = []
for section in structure_list:

    if section[0] == "#":
        sections.append(f"\n{section}\n")
        continue

    # If section exists
    if section in fountain_files:

        # Append section to sections
        with open(fountain_files[section], 'r') as f:
            content = f.read()
            stripped_content = content.strip()
            sections.append(stripped_content)

    else:
        sys.exit(
            f'\033[91mERROR: "{section}.fountain" was not found in subdirectories of "{sections_dir}"\033[0m')

# ------------------------------- Write to out ------------------------------- #

main_doc = "\n\n".join(sections)

with open(output_path, 'w') as f:
    f.write(main_doc)
    print(
        f"\033[92mSuccessfully combined {len(fountain_files)} Fountain file(s) to {output_path}\033[0m\n")
