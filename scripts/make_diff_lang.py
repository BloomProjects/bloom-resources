import os

DEFAULT_LANG = "en_US"

def load_properties(filepath, sep='=', comment_char='#'):
    """
    Read the file passed as parameter as a properties file.
    """
    keys = []
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
        for line in lines:
            l = line.strip()
            if l and not l.startswith(comment_char):
                key_value = l.split(sep)
                key = key_value[0].strip()
                keys.append(str(key))
                
    return keys

f = []
for (dirpath, dirnames, filenames) in os.walk("java17/manifest/assets/minecraft/lang"):
    f.extend(filenames)
    break

for file_name in f:
    lang = file_name.split(".")[0]
    path = os.path.join("java17/manifest/assets/minecraft/lang", file_name)
    data = load_properties(path)
    
    print(data)