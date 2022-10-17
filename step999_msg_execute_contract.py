'''
Gets info about what kinds of messages are used for Execute Msg on Juno
'''

import base64
import json
import os
import requests

import matplotlib.pyplot as plt
from prettytable import PrettyTable


REST_URL = os.getenv('REST_URL', 'https://api.juno.chaintools.tech')

current_dir = os.path.dirname(os.path.realpath(__file__))
FILE = f"{current_dir}/msgs/cosmwasm.wasm.v1.MsgExecuteContract.json"
extra_data = f"{current_dir}/extra_data"
os.makedirs(extra_data, exist_ok=True)

print("Loading in all cosmwasm.wasm.v1.MsgExecuteContract.json msgs...")
with open(FILE, "r") as f:
    msgexec = json.load(f)
print("Loaded, time to sort...")
print(f"\nTotal Number of cosmwasm.wasm.v1.MsgExecuteContract.json: #{len(msgexec):,}")


all = {}

most_frequent_senders = {}

for msg in msgexec: # dict_keys(['@type', 'sender', 'contract', 'msg', 'funds', 'height'])            
    contract = msg['contract']
    sender = msg['sender']

    try:
        msg_data = dict(msg['msg'])
        action = "{}"
        if len(msg_data.keys()) > 0:
            action = list(msg_data.keys())[0]

        if sender not in most_frequent_senders:
            most_frequent_senders[sender] = 0
        most_frequent_senders[sender] += 1


        if contract not in all:
            all[contract] = {}

        if action not in all[contract]:
            all[contract][action] = 0

        all[contract][action] += 1
    except Exception as e:
        print(e)
        print(msg)
    
    

# from pprint import pprint
# pprint(all)

# save to file
with open(f"{extra_data}/contract_execute_data.json", "w") as f:
    # sort all based off of the largest item() in .item()
    all = {k: v for k, v in sorted(all.items(), key=lambda item: max(item[1].items(), key=lambda x: x[1])[1], reverse=True)}
    json.dump(all, f, indent=4)

    # save most_frequent_senders
with open(f"{extra_data}/most_frequent_senders.json", "w") as f:
    # sort most_frequent_senders by the value & remove any which are less than 10
    most_frequent_senders = {k: v for k, v in sorted(most_frequent_senders.items(), key=lambda item: item[1], reverse=True) if v > 10}
    json.dump(most_frequent_senders, f, indent=4)