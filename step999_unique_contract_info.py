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

unique_interactions = {
    # "contract_addr": {"addr1": 1}
}

all = {
    # "contract_addr": {
    #     "unique_wallet_interactions": 0, # len(unique_interactions[contract].keys())
    #     "total_number_of_calls": 0,
    # }
}

REST_URL = os.getenv('REST_URL', 'https://api.juno.chaintools.tech')
for msg in msgexec: # dict_keys(['@type', 'sender', 'contract', 'msg', 'funds', 'height'])            
    contract = msg['contract']
    sender = msg['sender']
    funds = msg['funds']

    try:
        msg_data = dict(msg['msg'])

        # setup
        if contract not in all:
            # https://github.com/CosmWasm/wasmd/blob/main/x/wasm/client/rest/query.go
            # https://api.mintscan.io/v1/juno/wasm/contracts/juno15u3dt79t6sxxa3x3kpkhzsy56edaa5a66wvt3kxmukqjz2sx0hes5sn38g
            CONTRACT_INFO_API = f"{REST_URL}/wasm/contract/{contract}"        
            contract_details = requests.get(CONTRACT_INFO_API, headers={"Content-Type": "application/json",}).json()
            label = contract_details['result']["label"] if 'result' in contract_details.keys() else "Unknown" 

            all[contract] = {
                "label": label,
                "unique_wallet_interactions": 0,
                "total_number_of_calls": 0,                          
            }

        if contract not in unique_interactions:
            unique_interactions[contract] = {}

        # total number of calls
        all[contract]["total_number_of_calls"] += 1

        # times called
        if sender not in unique_interactions[contract]:
            unique_interactions[contract][sender] = 1
        else:
            unique_interactions[contract][sender] += 1   

    except Exception as e:
        print(e)

for contract in unique_interactions:
    all[contract]["unique_wallet_interactions"] = len(unique_interactions[contract].keys())
          
        
        # print(msg)
    
def pie_chart(sorted_all: dict, filename: str):
    pie_chart = {
        "labels": [],
        "sizes": [],        
        "explode": [],        
    }

    total_contracts = len(sorted_all.keys())
    print(f"{total_contracts=}")

    for idx, contract in enumerate(sorted_all):        
        # if Staking is in sorted_all[contract]["label"]
        if "airdrop" in sorted_all[contract]["label"].lower():
            continue
        elif "rewards" in sorted_all[contract]["label"].lower():
            continue
        elif idx > total_contracts * 0.05: # only top X% of contracts are saved
            break

        pie_chart["labels"].append(sorted_all[contract]["label"])
        pie_chart["sizes"].append(sorted_all[contract]["total_number_of_calls"])        
        pie_chart["explode"].append(0.1)

    fig, ax = plt.subplots()
    ax.pie(pie_chart["sizes"], explode=pie_chart["explode"], labels=pie_chart["labels"], autopct='%1.1f%%', shadow=True, startangle=90)
    ax.axis('equal')
    plt.savefig(f"{extra_data}/{filename}")    

def bar_chart(sorted_all: dict, filename: str):
    bar_chart = {
        "labels": [],
        "sizes": [],
        "colors": [],
    }
    for contract in sorted_all:
        bar_chart["labels"].append(sorted_all[contract]["label"])
        bar_chart["sizes"].append(sorted_all[contract]["total_number_of_calls"])
        bar_chart["colors"].append("red")

    fig, ax = plt.subplots()
    ax.bar(bar_chart["labels"], bar_chart["sizes"], color=bar_chart["colors"])
    plt.xticks(rotation=90)
    plt.savefig(f"{extra_data}/{filename}")
    


# save to file
# with open(f"{extra_data}/unique_contract_info.json", "w") as f:
#     # sort all as a dict by unique_wallet_interactions
#     sorted_all = {k: v for k, v in sorted(all.items(), key=lambda item: item[1]['unique_wallet_interactions'], reverse=True)}
#     json.dump(sorted_all, f, indent=4)


# with open(f"{extra_data}/unique_contract_info-sorted-by-total-calls.json", "w") as f:    
    # sort all as a dict by unique_wallet_interactions
    # sorted_all = {k: v for k, v in sorted(all.items(), key=lambda item: item[1]['total_number_of_calls'], reverse=True)}
    # # json.dump(sorted_all, f, indent=4)
    # pie_chart(sorted_all, "unique_contract_info-sorted-by-total-calls.png")
    # bar_chart(sorted_all, "unique_contract_info-sorted-by-total-calls-bar.png")

    # save sorted_all to a pie chart with matplotlib
    # https://matplotlib.org/stable/gallery/pie_and_polar_charts/pie_features.html

sorted_all = {k: v for k, v in sorted(all.items(), key=lambda item: item[1]['total_number_of_calls'], reverse=True)}
pie_chart(sorted_all, "unique_contract_info-sorted-by-total-calls-5%.png")

sorted_all = {k: v for k, v in sorted(all.items(), key=lambda item: item[1]['unique_wallet_interactions'], reverse=True)}
pie_chart(sorted_all, "unique_contract_info-sorted-by-total-calls-unique-wallets-5%.png")

