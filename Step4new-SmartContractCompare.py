'''
Gets information on MsgExecutes
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

print("Loading in all MsgExecuteContract msgs...")
with open(FILE, "r") as f:
    executes = json.load(f)
print("Loaded, time to sort...")
print(f"\nTotal Number of MsgExecuteContract's: #{len(executes):,}")

# unique contracts which we want to count
specific_contracts = {    
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
        all[c_addr] = { "total": 0, "heights": {}}

    # increase total
    # all[c_addr]["total"] = all[c_addr].get("total", 0) + 1
    all[c_addr]["total"] += 1

    # number of executes at this given height
    # all[c_addr]["heights"][height] = all[c_addr]["heights"].get(height, 0) + 1
    if height not in all[c_addr]["heights"]:
        all[c_addr]["heights"][height] = 0
    all[c_addr]["heights"][height] += 1


TOTAL_EXECUTES = len(executes)

TABLE_OUTPUTS = []
x = PrettyTable()

x.title = "MOST USED JUNO CONTRACTS"
x.field_names = ["Rank", "Contract", "Name", "# of Execs", "% of Juno Total"]
topX = sorted(all.items(), key=lambda x: x[1]["total"], reverse=True)[:20]
for idx, top_i in enumerate(topX):
    contract = top_i[0]
    their_executes = top_i[1]['total']  
    their_percent = (their_executes / TOTAL_EXECUTES) * 100

    # https://github.com/CosmWasm/wasmd/blob/main/x/wasm/client/rest/query.go
    # https://api.mintscan.io/v1/juno/wasm/contracts/juno15u3dt79t6sxxa3x3kpkhzsy56edaa5a66wvt3kxmukqjz2sx0hes5sn38g
    CONTRACT_INFO_API = f"{REST_URL}/wasm/contract/{contract}"        
    contract_details = requests.get(CONTRACT_INFO_API, headers={"Content-Type": "application/json",}).json()           
    label = contract_details['result']["label"] if 'result' in contract_details.keys() else "Unknown"

    # x.add_row([f"#{idx+1}", contract, their_executes, f"{their_percent:.2f}%"])
    x.add_row([f"#{idx+1}", f"{contract}", f"{label}", f"{their_executes:,}", f"{their_percent:.2f}%"])

TABLE_OUTPUTS.append(x.get_string())

# # save to file
# with open(f"{extra_data}/most_used_juno_contracts.txt", "w") as f:
#     f.write(x.get_string())

x.clear()
x.title = "SPECIFIC CONTRACTS INFO"
x.field_names = ["Contract", "Name", "# of Execs", "% of Juno Total"]
# [('juno18hsatg55uk7sf2hm0j36402aej729g395egq9rt5rjvz7gazdfcss9egmd', 'Racoon DiceV2'), ('juno1r4pzw8f9z0sypct5l9j906d47z998ulwvhvqe5xdwgy8wf84583sxwh0pa', 'Racoon Buy Ticket'), ('juno1an55u6dmsuw9etmyw3pccjn2qm4uddnyu4c6yusc8y5mdf77yjlq9p4k9y', 'Racoon DungeonV2'), ('juno1sr4d0lq5njnfs0l59u92cerhr24zkczysxft4rvaas6gw3zt9lhqju02x4', 'Racoon LottoV2')]
topSpecificSorted = sorted(specific_contracts.items(), key=lambda x: all[x[0]]["total"], reverse=True)
for contract, name in topSpecificSorted:
    if contract in all:
        # https://github.com/CosmWasm/wasmd/blob/main/x/wasm/client/rest/query.go
        # https://api.mintscan.io/v1/juno/wasm/contracts/juno15u3dt79t6sxxa3x3kpkhzsy56edaa5a66wvt3kxmukqjz2sx0hes5sn38g
        CONTRACT_INFO_API = f"{REST_URL}/wasm/contract/{contract}"        
        contract_details = requests.get(CONTRACT_INFO_API, headers={"Content-Type": "application/json",}).json()           
        label = contract_details['result']["label"] if 'result' in contract_details.keys() else "Unknown"
        their_percent_of_all = (all[contract]['total'] / TOTAL_EXECUTES) * 100                            
        x.add_row([contract, label, f"{all[contract]['total']:,}", f"{their_percent_of_all:.2f}%"])
        
TABLE_OUTPUTS.append(x.get_string())


# SAve to file in the extra_data folder extra_data
smartContractTxt = f"{extra_data}/SmartContractExecuteInfo.txt"
with open(smartContractTxt, "w") as f:
    f.write("\n\n\n".join(TABLE_OUTPUTS))
print(f"Done, saved to file {smartContractTxt}")

# GRAPH & SORT HERE
# 'sort racoon_txs and get the highest and lowest key values' section in step4*.py