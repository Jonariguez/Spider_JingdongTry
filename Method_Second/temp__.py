
import json
with open("1.json",'w') as f:
    json.dump({1:2,2:3},f)

with open("1.json",'r') as f:
    a = json.load(f)
    print(a)

import os
os.path.exists("cookies.json")