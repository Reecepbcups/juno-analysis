'''
Goal: Compare total network Txss for juno minus msgWithdrawDelegatorReward
'''

from cProfile import label
import os, json
import matplotlib.pyplot as plt

# Comment out lines you do not want to show / count
SHOW_SPECIFIC_MSGS = [
    # "cosmwasm.wasm.v1.MsgStoreCode",
    # "cosmos.staking.v1beta1.MsgEditValidator",
    # "cosmos.distribution.v1beta1.MsgWithdrawDelegatorReward",
    "cosmos.staking.v1beta1.MsgDelegate",
    "cosmos.authz.v1beta1.MsgGrant",
    "ibc.core.channel.v1.MsgAcknowledgement",
    "ibc.applications.transfer.v1.MsgTransfer",
    "cosmos.bank.v1beta1.MsgSend",
    "cosmos.authz.v1beta1.MsgExec",
    # "cosmos.distribution.v1beta1.MsgWithdrawValidatorCommission",
    "cosmos.staking.v1beta1.MsgUndelegate",
    "cosmos.authz.v1beta1.MsgRevoke",
    # "ibc.core.channel.v1.MsgRecvPacket",
    # "cosmwasm.wasm.v1.MsgInstantiateContract",
    "cosmos.staking.v1beta1.MsgBeginRedelegate",
    # "cosmwasm.wasm.v1.MsgExecuteContract"
]
# v = [v.replace(".json", "") for v in total_messages.keys()] # <- generate above with this
# input(json.dumps(v, indent=4))

# loop through all msgs folder
current_dir = os.path.dirname(os.path.realpath(__file__))
total_msgs_file = f"{current_dir}/json/total_messages.json"

# make any dirs in path if they don't exist
for file in [total_msgs_file]:
    os.makedirs(os.path.dirname(file), exist_ok=True)    
    open(file, "w").close() # clear file

total_messages = {}
lowest_height = -1
highest_height = -1

def set_height(height):
    global lowest_height, highest_height
    height = int(height)
    if lowest_height == -1:
        lowest_height = height
    if highest_height == -1:
        highest_height = height
    if height < lowest_height:
        lowest_height = height
    if height > highest_height:
        highest_height = height    

# saves msg amounts by height to file
for file in os.listdir(f"{current_dir}/msgs"):
    if not file.endswith(".json"):
        continue

    print(f"Processing {file}")
    with open(f"{current_dir}/msgs/{file}", "r") as f:
        msg_list = json.load(f)    

    values_at_heights = {}
    for msg in msg_list:        
        height = msg["height"]   
        set_height(height)

        if height not in values_at_heights:
            values_at_heights[height] = 0
        values_at_heights[height] += 1
        
    total_messages[file] = values_at_heights

with open(total_msgs_file, "w") as f:
    json.dump(total_messages, f)

# exit()

final_output = {}
range_jumps = 5_000
range_jumps = int((highest_height-lowest_height+1)*0.025) # maybe take a % of the highest height - lowest height

for msg_type, heights_data in total_messages.items():
    # heights_data => {'4801196': 1, '4801189': 1, '4800030': 1}
    name = msg_type.replace(".json", "")
    # sorted_heights = sorted(v.keys(), key=lambda x: x[0])
    # print(sorted_heights)
    if len(heights_data.keys()) == 0: continue
    if name not in SHOW_SPECIFIC_MSGS: continue

    all_txs = {k: 0 for k in range(lowest_height, highest_height, range_jumps)}

    for height, amt in heights_data.items():
        # find the closest key to k
        closest_height = min(all_txs, key=lambda x:abs(x-int(height)))
        # print(closest)
        # add the # of txs to the closest key
        # final_output[closest_height] = final_output.get(closest_height, 0) + amt

        # TODO: Ensure this works
        # all_txs[closest_height] = all_txs.get(closest_height, 0) + amt # this is way to slow
        if closest_height in all_txs:
            all_txs[closest_height] += amt
        else:
            all_txs[closest_height] = amt

    # print(final_output)
    # exit()
    
    plt.plot(all_txs.keys(), all_txs.values(), label=name)    
    plt.legend(loc='upper right')
    plt.title(f'Juno Txs By Type')
    plt.xlabel('Block height (* 1 million)')
    plt.ylabel('Txs Over Time')    
    
fig = plt.gcf()
fig.set_size_inches(18.5, 10.5)
fig.savefig('graphs/specific-juno_txs_over_time.png', dpi=100)