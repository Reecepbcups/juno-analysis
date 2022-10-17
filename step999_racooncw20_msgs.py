CW20_ADDR = "juno1r4pzw8f9z0sypct5l9j906d47z998ulwvhvqe5xdwgy8wf84583sxwh0pa" # mintscan

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

    if contract != CW20_ADDR:
        continue

    # input(msg)
    # { 'msg': {'send': {'contract': 'juno1wgkhhyf5zg2pxfxfzmq7rtx7jx5r294m2kudq3vqktfua5jay6xs04375w', 'amount': '939141', 'msg': 'eyJyb2xsX3JhYyI6eyJhZGRyZXNzIjoianVubzE2NjN5aHcwcnJlNzBlZ2R3ZXozc3cyZTBlcnk5NHZnbm41ZWx6YSIsIm5iX29mX3JvbGxzIjozLCJtdWx0aXBsaWVyIjoyLCJuYl9vZl9lbXBvd2VyZWRfcm9sbHMiOjB9fQ=='}}, 'funds': [], 'height': '4899076'}    

    try:
        msg_data = dict(msg['msg'])        
        if 'send' not in msg_data: 
            continue

        if 'msg' in msg_data:
            msg_data = msg_data['msg']     

        # input(msg_data)   

        base64_msg = msg_data['send']['msg']        
        decoded_msg = base64.b64decode(base64_msg).decode('utf-8')

        if "buy_empowered_rolls" not in decoded_msg: continue

        if 'msg' in decoded_msg:
            decoded_msg = base64.b64decode(dict(base64_msg)['msg']).decode('utf-8')

        data = json.loads(decoded_msg)

        multiplier = int(data['buy_empowered_rolls']['multiplier'])
        nb_of_rolls = int(data['buy_empowered_rolls']['nb_of_rolls'])
        total_cw20_rolls = nb_of_rolls * multiplier        

        if sender not in most_frequent_senders:
            most_frequent_senders[sender] = 0
        most_frequent_senders[sender] += 1


        if sender not in all:
            all[sender] = 0
        all[sender] += total_cw20_rolls

             
    except Exception as e:
        print(e)
        # print(msg)
    
    

# from pprint import pprint
# pprint(all)

print(f"Sum of all items: {sum(all.values())}")

# save to file
with open(f"{extra_data}/rac_empowered_data.json", "w") as f:
    # sort all by the value
    all = {k: v for k, v in sorted(all.items(), key=lambda item: item[1], reverse=True)}
    json.dump(all, f, indent=4)

# save most_frequent_senders to file sorted
with open(f"{extra_data}/rac_empowered_data_most_frequent_senders.json", "w") as f:
    # sort all by the value
    most_frequent_senders = {k: v for k, v in sorted(most_frequent_senders.items(), key=lambda item: item[1], reverse=True)}
    json.dump(most_frequent_senders, f, indent=4)