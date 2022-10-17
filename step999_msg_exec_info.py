'''
Gets info about what messages are mainly in the MsgExec and calculates them
'''

import base64
import json
import os
import requests

import matplotlib.pyplot as plt
from prettytable import PrettyTable


REST_URL = os.getenv('REST_URL', 'https://api.juno.chaintools.tech')

current_dir = os.path.dirname(os.path.realpath(__file__))
FILE = f"{current_dir}/msgs/cosmos.authz.v1beta1.MsgExec.json"
extra_data = f"{current_dir}/extra_data"
os.makedirs(extra_data, exist_ok=True)

print("Loading in all authz.v1beta1.MsgExec msgs...")
with open(FILE, "r") as f:
    msgexec = json.load(f)
print("Loaded, time to sort...")
print(f"\nTotal Number of authz.v1beta1.MsgExec's: #{len(msgexec):,}")


all = {

}

# TODO: save heights here as well for graphing! from step4_RacComparedToJuno
for msg in msgexec: # dict_keys(['@type', 'sender', 'contract', 'msg', 'funds', 'height'])
    for submsg in msg['msgs']: # since these are MsgExec, they have submsgs
        msg_type = submsg['@type']
            
        if msg_type not in all:
            all[msg_type] = { "total": 0 }

        # increase total
        # all[c_addr]["total"] = all[c_addr].get("total", 0) + 1
        all[msg_type]["total"] += 1

from pprint import pprint
pprint(all)