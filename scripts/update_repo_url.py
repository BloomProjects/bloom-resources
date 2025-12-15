import json
import requests
import hashlib

REPO_SOURCES = [
    "https://repo1.maven.org/maven2/",
    "https://libraries.minecraft.net/",
    "https://repo.bloomprojects.lol/snapshots/"
]

session = requests.Session()

with open("java17/manifest/version/1.8.9.json", "r") as file:
    data = json.load(file)
    
for library in data["libraries"]:
    lib_name = library["name"]
    artifact_obj = library["downloads"]["artifact"]
    lib_name_split = lib_name.split(":")
    
    if len(lib_name_split) > 3:
        group, artifact, version, classifier = lib_name_split
        lib_path = f"{group.replace('.', '/')}/{artifact}/{version}/{artifact}-{version}-{classifier}.jar"
    else:
        group, artifact, version = lib_name_split
        lib_path = f"{group.replace('.', '/')}/{artifact}/{version}/{artifact}-{version}.jar"
    
    for repo in REPO_SOURCES:
        full_url = repo + lib_path

        response = session.get(full_url)
        if response.status_code == 200:
            print(f"Found {lib_name} at {full_url}")
            artifact_obj["url"] = full_url
            artifact_obj["size"] = len(response.content)
            artifact_obj["path"] = lib_path
            
            m = hashlib.sha1()
            m.update(response.content)
            artifact_obj["sha1"] = m.hexdigest()
            break
        
with open("java17/manifest/version/1.8.9.json", "w") as file:
    json.dump(data, file, indent=4)
    
# copy libraries to client/BloomClient.json
with open("java17/client/BloomClient.json", "r") as file:
    client_data = json.load(file)
    
client_data["libraries"] = data["libraries"]

with open("java17/client/BloomClient.json", "w") as file:
    json.dump(client_data, file, indent=4)
    
session.close()

