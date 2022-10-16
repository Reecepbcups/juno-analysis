'''
Goal of this file is to compare Rac Execute messages compared to others
'''

import base64
import json
import os

import matplotlib.pyplot as plt

# current_dir = os.path.dirname(os.path.realpath(__file__))
# with open(f"{current_dir}/msgs/cosmwasm.wasm.v1.MsgExecuteContract.json", "r") as f:
#     data = json.load(f)


# # Pulled from racoon.bet RPC queries via inspect element
# list_of_racoon_contracts = {
#     # Dungeon
#     "juno1ft5nuq4ck8ucwaunv0l064e22gw4lndexswqu5772mslgvf43ymqsgxznw": "DungeonV1",  
#     "juno1an55u6dmsuw9etmyw3pccjn2qm4uddnyu4c6yusc8y5mdf77yjlq9p4k9y": "Dungeon V2",  
#     # Lotto  
#     "juno1mpufvc3j6v2zc2959lf838lnfv80c3hscgpfzqzkezyeceth9z6s37yeck": "LottoV1",
#     "juno1sr4d0lq5njnfs0l59u92cerhr24zkczysxft4rvaas6gw3zt9lhqju02x4": "LottoV2",  
#     "juno1r4pzw8f9z0sypct5l9j906d47z998ulwvhvqe5xdwgy8wf84583sxwh0pa": "Lottery Buy Ticket Rac",
#     # dice
#     "juno1xkvhguzrectvswn6f20t4gggs8wl70sj2rd5rt3trl73fjn8666qer96u0": "DiceV1",
#     "juno18hsatg55uk7sf2hm0j36402aej729g395egq9rt5rjvz7gazdfcss9egmd": "Dice V2",
#     # slots (excludes empowered spin Txs)
#     "juno1wgkhhyf5zg2pxfxfzmq7rtx7jx5r294m2kudq3vqktfua5jay6xs04375w": "Slots",
# }


# # len of data
# print(f"Length of data: {len(data)}")

racoon_txs = {}
juno_txs = {} # height, amt

for height, tx_list in data.items():
    # input(f"{height}, {tx_list}")

    juno_txs[height] = juno_txs.get(height, 0) + len(tx_list)

    for tx in tx_list:
        # base64 decode it
        decoded = str(base64.b64decode(tx))
        # check if any racoon.keys() are in decoded
        for key in list_of_racoon_contracts:
            if key in decoded:
                racoon_txs[height] = racoon_txs.get(height, 0) + 1
                break

total_rac_executes = sum(racoon_txs.values())
total_juno_executes = sum(juno_txs.values())

# 11.24% of all Juno executes are Racoon executes
print(f"Total Racoon Executes: {total_rac_executes}")
print(f"Total Juno Executes: {total_juno_executes}")
print(f"Racoon Executes % of Juno: {round(total_rac_executes / total_juno_executes * 100, 2)}%")


# sort racoon_txs and get the highest and lowest key values
sorted_racoon_txs = sorted(racoon_txs.items(), key=lambda x: x[0])
lowest = int(sorted_racoon_txs[0][0])
highest = int(sorted_racoon_txs[-1][0])

print(f"Lowest: {lowest}, Highest: {highest}")


all_transactions = {k: 0 for k in range(lowest, highest+1, 5_000)}
rac_values = {k: 0 for k in range(lowest, highest+1, 5_000)} # sets the X axis values
for height, amt in racoon_txs.items():
    # find the closest key to k
    closest = min(rac_values, key=lambda x:abs(x-int(height)))
    # print(closest)

    # add the value to the closest key
    rac_values[closest] = rac_values.get(closest, 0) + amt

# juno total
for height, amt in juno_txs.items():
    closest = min(all_transactions, key=lambda x:abs(x-int(height)))
    # add the value to the closest key
    all_transactions[closest] = all_transactions.get(closest, 0) + amt


# Executes over time
plt.plot(rac_values.keys(), rac_values.values())
plt.title('Racoon Txs Over Time')
plt.xlabel('Block height')
plt.ylabel('Txs Over Time')
# plt.show()
# plt.savefig('rac_txs_over_time.png')
plt.plot(all_transactions.keys(), all_transactions.values())
plt.title('Juno Execute Messages compared to Racoon Games')
plt.xlabel('Block height')
plt.ylabel('Executes Over Time')
# plt.show()
plt.savefig('rac_juno_msgExecute.png')


