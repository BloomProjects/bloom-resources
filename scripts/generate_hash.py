import os
import sys
import hashlib
from pathlib import Path

def main(path):
    file_paths = []
    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            file_paths.append(full_path)

    for file_path in file_paths:
        relative_path = Path(file_path).relative_to(path).as_posix()
        
        with open(file_path, "rb") as f:
            hash = hashlib.file_digest(f, "sha1").hexdigest()
            
        print(f"{relative_path} {hash}")

if __name__ == "__main__":
    path = sys.argv[1]
    main(path)
    