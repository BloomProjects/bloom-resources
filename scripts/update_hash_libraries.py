import json
import requests
import hashlib

with open("java17/manifest/version/1.8.9.json", "r") as f:
    data = json.load(f)
    
for library in data["libraries"]:
    url = library["downloads"]["artifact"]["url"]
    
    resp = requests.get(url)
    m = hashlib.sha1()
    m.update(resp.content)
    
    library["downloads"]["artifact"]["sha1"] = m.hexdigest()
    library["downloads"]["artifact"]["size"] = len(resp.content)
    
with open("java17/manifest/version/1.8.9.json", "w") as f:
    json.dump(data, f, indent=2)
    
