import os, re, csv

file_path = os.path.dirname(os.path.realpath(__file__))
javafiles = [os.path.join(root, name)
             for root, dirs, files in os.walk(file_path)
             for name in files
             if name.endswith((".java"))]
clean_func = [x 
              for x in [re.findall(r'\bp_\w+_\w+', open(i, "r").read()) for i in javafiles] 
              if x]

flattened = []
for item in clean_func:
    if isinstance(item, list): flattened.extend(item) 
    else: flattened.append(item)

obf_need = list(dict.fromkeys(list(set(flattened))))
    
# Read the methods file
with open(file_path + '\\49_params.csv', 'r', newline='') as file:
    reader = csv.DictReader(file)
    
    # Convert the reader object to a list of dictionaries
    methods = [row for row in reader]

list_methods = []
for i in obf_need:
    for m in methods:
        if m["param"] == i:
            list_methods.append(m)
            
# Create a new list to preserve order
ul = []
for item in list_methods:
    if item not in ul:
        ul.append(item)
  
with open(file_path + '\\params.csv', 'a', newline='') as file:
    fieldnames = ['param', 'name', 'side']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    
    writer.writeheader()
    writer.writerows(ul) 

o = 0
for i in ul:
    for f in javafiles:
        # Read the file
        with open(f, 'r') as file:
            content = file.read()
            
        if(i["param"] not in content): continue

        # Replace all occurrences of strings starting with old_prefix
        modified_content = content.replace(i["param"], i["name"])

        # Write the modified content back to the file
        with open(f, 'w') as file:
            file.write(modified_content)
    o+=1
    print(f"Replaced all occurrences starting with '{i['param']}' with '{i['name']}' with side {i['side']}. {o} / {len(ul)} Passed")
    