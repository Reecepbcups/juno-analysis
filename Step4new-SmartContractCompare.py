'''
Gets information on MsgExecutes
'''

import base64
import json
import os

import matplotlib.pyplot as plt

current_dir = os.path.dirname(os.path.realpath(__file__))
FILE = f"{current_dir}/msgs/cosmwasm.wasm.v1.MsgExecuteContract.json"

with open(FILE, "r") as f:
    executes = json.load(f)

# len of data
print(f"\nTotal Number of MsgExecuteContract's: #{len(executes):,}")
# unique contracts which we want to count
list_of_contracts = {    
    # Racoon
    # Pulled from racoon.bet RPC queries via inspect element & thanks to Racoon Admins
    # "juno1ft5nuq4ck8ucwaunv0l064e22gw4lndexswqu5772mslgvf43ymqsgxznw": "Racoon DungeonV1",
    "juno1an55u6dmsuw9etmyw3pccjn2qm4uddnyu4c6yusc8y5mdf77yjlq9p4k9y": "Racoon DungeonV2",      
    # "juno1mpufvc3j6v2zc2959lf838lnfv80c3hscgpfzqzkezyeceth9z6s37yeck": "Racoon LottoV1",
    "juno1sr4d0lq5njnfs0l59u92cerhr24zkczysxft4rvaas6gw3zt9lhqju02x4": "Racoon LottoV2", 
    "juno1r4pzw8f9z0sypct5l9j906d47z998ulwvhvqe5xdwgy8wf84583sxwh0pa": "Racoon Buy Ticket",    
    # "juno1xkvhguzrectvswn6f20t4gggs8wl70sj2rd5rt3trl73fjn8666qer96u0": "Racoon DiceV1",
    "juno18hsatg55uk7sf2hm0j36402aej729g395egq9rt5rjvz7gazdfcss9egmd": "Racoon DiceV2",    
    # "juno1wgkhhyf5zg2pxfxfzmq7rtx7jx5r294m2kudq3vqktfua5jay6xs04375w": "Racoon Slots Empowered Spins",
}

# any other contract that gets executes we put here
all = {
    # "contract_addr": {
    #     "total": 0,
    #     "heights": {
    #         "1": 0,
    #         "2": 10,
    #     }
    # }
}

# TODO: save heights here as well for graphing! from step4_RacComparedToJuno
for msg in executes: # dict_keys(['@type', 'sender', 'contract', 'msg', 'funds', 'height'])
    c_addr = msg["contract"]
    height = str(msg["height"])
    # if c_addr in list_of_contracts: # do we even need this? lets just do in all
    #     list_of_contracts[c_addr]['count'] += 1
        
    if c_addr not in all:
        all[c_addr] = {
            "total": 0,
            "heights": {}
        }

    # increase total
    all[c_addr]["total"] = all[c_addr].get("total", 0) + 1
    # number of executes at this given height
    all[c_addr]["heights"][height] = all[c_addr]["heights"].get(height, 0) + 1




print("\nMOST USED CONTRACTS")
topX = sorted(all.items(), key=lambda x: x[1]["total"], reverse=True)[:5]
TOTAL_EXECUTES = len(executes)
for top_i in topX:
    contract = top_i[0]
    their_executes = top_i[1]['total']  
    their_percent = (their_executes / TOTAL_EXECUTES) * 100
    print(f"{contract}: {their_executes}\t({their_percent:.2f}%)")


print("\nSPECIAL CONTRACTS")
for contract, name in list_of_contracts.items():
    if contract in all:
        their_percent_of_all = (all[contract]['total'] / TOTAL_EXECUTES) * 100        
        print(f"{contract}: {all[contract]['total']}\t({their_percent_of_all:.2f}%) ({name})")
        # print(f"Executes as a % of Juno: {round(total_rac_executes / total_juno_executes * 100, 2)}%")


# GRAPH & SORT HERE
# 'sort racoon_txs and get the highest and lowest key values' section in step4*.py