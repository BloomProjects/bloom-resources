import glob
import os
import re
import csv

be_replaced_files = []
be_replaced_names = []

# MAPPING_TYPE = "func"
# MAPPING_FILE = "methods.csv"

# MAPPING_TYPE = "field"
# MAPPING_FILE = "fields.csv"

MAPPING_TYPE = "params"
MAPPING_FILE = "params.csv"

REGEX_MAPPING = fr"{MAPPING_TYPE}_\d+_[a-zA-Z]+"
REGEX_PARAMS = r"p_\w+_\w+_"

# Load mapping to write
with open(f"../mappings/extended/{MAPPING_FILE}", "r") as f:
    reader = csv.DictReader(f)
    mapping_lines = [row for row in reader]

for path_file in glob.glob("../src/main/**/*.java", recursive=True):
    with open(path_file, "r") as f:
        code = f.read()

    code_find = re.findall(REGEX_PARAMS, code, re.MULTILINE)

    if not code_find:
        continue

    if path_file not in be_replaced_files:
        be_replaced_files.append(path_file)

    for name in code_find:
        if name not in be_replaced_names:
            be_replaced_names.append(name)

print(len(be_replaced_names))

for obfed_name in be_replaced_names:
    name = input(f"Name of {obfed_name}: ")
    side = input(f"Side of {obfed_name}: ")

    data = {
        "param": obfed_name,
        "name": name,
        "side": side
    }

    mapping_lines.append(data)

    for path_file in be_replaced_files:
        with open(path_file, "r") as f:
            code = f.read()
        
        code = code.replace(obfed_name, name)

        with open(path_file, "w") as f:
            f.write(code)

    with open(f"../mappings/extended/{MAPPING_FILE}", "w", newline='') as f:
        fieldnames = ['param', 'name', 'side']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(mapping_lines) 
