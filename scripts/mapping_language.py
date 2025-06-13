import os
import json

ASSETS_FOLDER = "C:\\Users\\Admin\\.gradle\\bloom\\assets"
OBJECTS_FOLDER  = f"{ASSETS_FOLDER}\\objects"
INDEX_FILE_PATH = f"{ASSETS_FOLDER}\\indexes\\1.8.json"

def getLanguageFiles():
    with open(INDEX_FILE_PATH, "r") as f:
        data = json.load(f)
        
    objects = data["objects"]
    
    for path, attr in objects.items():
        if ".lang" not in path:
            continue
        
        hash = attr["hash"]
        id_hash = hash[0:2]
        with open(f"{OBJECTS_FOLDER}\\{id_hash}\\{hash}", "rb") as f:
            with open(path, "wb") as fw:
                fw.write(f.read())
    
getLanguageFiles()