'''
Loops through the MsgTransfer IBC message and makes a dict of the accounts which have sent out the most
Then print those out
'''

import os, json

current_dir = os.path.dirname(os.path.realpath(__file__))
extra_data = os.path.join(current_dir, 'extra_data')
ibc_msgs = json.load(open(os.path.join(current_dir, 'msgs', 'ibc.applications.transfer.v1.MsgTransfer.json')))

# [{"@type": "/ibc.applications.transfer.v1.MsgTransfer", "source_port": "transfer", "source_channel": "channel-58", "token": {"denom": "ibc/495D80DBC0BAB80BE1DD17D5A9B970C7403E4AFC5A87E68189B58160965D1701", "amount": "1"}, "sender": "juno1ukzhpadacxf54p345f6dwzrk9wju7guyfvwpxm", "receiver": "ki1ukzhpadacxf54p345f6dwzrk9wju7guywnu49n", "timeout_height": {"revision_number": "2", "revision_height": "12234449"}, "timeout_timestamp": "0", "height": "5506998"}, 

# ibc messages is an array of dicts

biggest_senders = {}
for idx, msg in enumerate(ibc_msgs):
    # print(msg)

    source_port = msg['source_port'] # transfer
    source_channel = msg['source_channel'] # channel-0
    token = msg['token']['denom'] # {'denom': 'ujuno', 'amount': '621683173'}
    amount = msg['token']['amount'] # {'denom': 'ujuno', 'amount': '621683173'}
    sender = msg['sender'] # juno1...
    receiver = msg['receiver'] # osmo1...
    height = msg['height'] # '5506927'

    # if idx >= 10: exit()

    if source_port != 'transfer':
        continue

    if not receiver.startswith('osmo1'): # sending to osmosis
        continue

    if not token == 'ujuno':
        continue # only show juno

    if sender not in biggest_senders:
        biggest_senders[sender] = 0

    biggest_senders[sender] += int(amount)/1_000_000 # normal juno
    
    # if idx >= 10: break

# print(biggest_senders)
# save to ext

# sort biggest_senders based off its values
sorted_biggest_senders = {k: v for k, v in sorted(biggest_senders.items(), key=lambda item: item[1], reverse=True)}

save_path = os.path.join(extra_data, 'ibc_sells.json')
save_path_csv = os.path.join(extra_data, 'ibc_sells.csv')

with open(save_path, 'w') as f:
    json.dump(sorted_biggest_senders, f, indent=4)

with open(save_path_csv, 'w') as f:    
    for k, v in sorted_biggest_senders.items():
        f.write(f'{k},{v},{f"https://www.mintscan.io/juno/account/{k}"}\n')