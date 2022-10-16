'''
Loop through all data files & save the data to one big dict file
(Was saved in chunks incase errors happened.)

We use this for step3 and step999 graphing data blocks
'''

import os
import json

current_dir = os.path.dirname(os.path.realpath(__file__))

data = {}

for file in os.listdir(os.path.join(current_dir, "data")):
    with open(os.path.join(current_dir, "data", file), "r") as f:
        data.update(json.load(f))

with open(os.path.join(current_dir, "all_data.json"), "w") as f:
    json.dump(data, f)