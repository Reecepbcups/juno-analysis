'''
Reece Williams | 2022-Sept-17
Iterates over JUNO's data in the all_data json file & gets information about transactions
'''

import pprint
import base64
import ijson # pip install ijson
import json
import os
import time

current_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(current_dir, "extra_data")
os.makedirs(data_dir, exist_ok=True)

ALL_MSGS = {}

min_height = -1
max_height = -1

def set_height(height):
    height = int(height)
    global min_height, max_height
    if min_height == -1:
        min_height = height
    if max_height == -1:
        max_height = height
    if height < min_height:
        min_height = height
    if height > max_height:
        max_height = height        

all_data = os.path.join(current_dir, 'all_data.json')
if not os.path.exists(all_data):
    print("all_data.json not found. Please run step2 first to combine all into 1 :)")
    exit(1)

with open(all_data, 'rb') as f:
    print('Parsing all_data.json...')
    parser = ijson.kvitems(f, "")

    start_time = time.time()
    for idx, (height, value) in enumerate(parser):
        if len(value['decoded_txs']) == 0: continue
        # 4570598 {
        # 'time': '2022-08-29T04:46:40.171071833Z', 
        # 'num_txs': 1, 
        # 'decoded_txs': [{msg_here}]
        for msg in value['decoded_txs']:            
            msg['height'] = height  
            set_height(height)     
            # decoded_tx = str(base64.b64decode(tx))
            # msg_type = msg["@type"]     
            # ALL_MSGS[msg_type] = ALL_MSGS.get(msg_type, []) + [msg] # This is way to slow
            if msg["@type"] in ALL_MSGS:
                ALL_MSGS[msg["@type"]].append(msg)
            else:
                ALL_MSGS[msg["@type"]] = [msg]
            
        if idx % 10_000 == 0:
            print(f'Parsed {idx} blocks so far. Time: {time.time() - start_time:.2f}s')


msgs_dir = "msgs"
if not os.path.exists(msgs_dir):
    os.makedirs(msgs_dir, exist_ok=True)

for msg_type in ALL_MSGS.keys():      
    loc = os.path.join(current_dir, msgs_dir, f"{msg_type[1:]}.json")
    with open(loc, 'w') as f:
        print(f'Dumping {msg_type} to {loc}...')
        # json.dump(ALL_MSGS[msg_type], f, indent=4)
        json.dump(ALL_MSGS[msg_type], f, default=str) # fixes Object of type Decimal is not JSON serializable. Could have a custom func serialize_decimal, check if of Decimal, then return str() if so.


# print(ALL_MSGS['/cosmwasm.wasm.v1.MsgExecuteContract'])

# for each ALL_MSGS key, sum all len of the values
# then sort by the sum of the values & print the % total
total = sum([len(v) for v in ALL_MSGS.values()])
output = [f'Total msgs: {total:,}', f'Lowest height: {min_height} & Highest height: {max_height}. Spread: {max_height-min_height}\n']

sorted = {k: len(v) for k, v in sorted(ALL_MSGS.items(), key=lambda item: len(item[1]), reverse=True)}
for msg_type, msgs in sorted.items():      
    output.append(f'{msg_type:<75} {msgs:<10} ({msgs/total*100:.2f}%)')

filename = 'tx_percent_summary.txt'
with open(os.path.join(data_dir, filename), 'w') as f:
    f.write('\n'.join(output))
    print(f'Wrote {filename}')