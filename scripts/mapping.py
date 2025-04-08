import os
import re
import csv
from tqdm import tqdm

MAPPING_TYPE = "params" # fields, methods, params
MAPPING_NAME = "params.csv"

REGEX_FIND = ""

if MAPPING_TYPE == "params":
    REGEX_FIND = r"p_\d+_\d+_"
elif MAPPING_TYPE == "field":
    REGEX_FIND = r"field_\d+_\w+"
else:
    REGEX_FIND = r"func_\d+_\w+"

JAVA_FILES_FOLDER = ".."

def get_java_files():
    path_project = os.path.abspath(os.path.join(os.getcwd(), JAVA_FILES_FOLDER))
    return [os.path.join(dirpath, f) for dirpath, dirnames, files in os.walk(path_project) for f in files if f.endswith('.java')]

def get_mappings():
    with open(MAPPING_NAME, "r") as f:
        csv_reader = csv.reader(f, delimiter=',')
        return list(csv_reader)

files = get_java_files()
mappings = get_mappings()

mappings_kv = {}

for item in mappings:
    mappings_kv[item[0]] = item[1]

for file_path in tqdm(files):
    with open(file_path, "r") as f:
        file_text = f.read()

    found = re.findall(REGEX_FIND, file_text, re.MULTILINE)
    
    for item in found:
        if item not in mappings_kv:
            continue

        name = mappings_kv[item]

        file_text = file_text.replace(item, name)

    with open(file_path, "w") as f:
        f.write(file_text)
