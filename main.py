import os
import sys
import json
import httpx
import base64
import subprocess

from dotenv import load_dotenv
load_dotenv()

# RPC = 
RPC = os.getenv("JUNO_RPC", "https://rpc.juno.strange.love")
LOWEST_HEIGHT = int(os.getenv("LOWEST_BLOCK_HEIGHT")) # https://rpc.juno.strange.love/block?height=2000000
HEIGHT_DATA_GROUPINGS = int(os.getenv("HEIGHT_DATA_GROUPINGS", 500))
# print(RPC); print(LOWEST_HEIGHT)

client = httpx.Client()
current_dir = os.path.dirname(os.path.realpath(__file__))


# TOTAL_RAC_TXS = 0
TOTAL_JUNO_TXS = 0
data = {} # int(height) = {other_data_here}


def run_cmd(cmd) -> str:
    # return subprocess.Popen(cmd, shell=True, text=False, stdout=subprocess.PIPE).stdout.read()
    # return subprocess.run(cmd, shell=True, text=True, capture_output=True).stdout
    return os.popen(cmd).read()    


# ensure junod is installed
version = run_cmd("junod version")
if len(version) == 0:
    print("Junod not installed. Please install junod and try again.")
    exit(1)

def main():
    global data, HEIGHT_DATA_GROUPINGS

    # latest = int(get_latest_height())
    # print("Latest" + str(latest))

    start = int(sys.argv[1]) # starting height
    # end = int(sys.argv[2]) # start - spread
    spread = int(sys.argv[2]) #10k

    os.makedirs(os.path.join(current_dir, "data"), exist_ok=True)
    
    if spread < HEIGHT_DATA_GROUPINGS:
        HEIGHT_DATA_GROUPINGS = spread
    
    # loop through blocks backwards from latest to LOWEST_HEIGHT
    # for idx, block_h in enumerate(range(latest, LOWEST_HEIGHT, -1)):    
    for idx, block_h in enumerate(range(start, start-HEIGHT_DATA_GROUPINGS-1, -1)):        
        if idx % (HEIGHT_DATA_GROUPINGS) == 0:            
            if len(data) == 0:
                # print(f"{block_h} was empty")
                pass
            else:
                with open(os.path.join(current_dir, "data", f"blocks_{block_h}.json"), "w") as f:
                    json.dump(data, f)
                    data = {}
                    print(f"Saved {block_h}")
        get_block_data(block_h)        

import multiprocessing as mp
p = mp.Pool(mp.cpu_count())

IGNORED_MESSAGES = {    
    "ibc.core.channel.v1.MsgChannelOpenAck": None,
    "ibc.core.channel.v1.MsgChannelOpenInit": None,
    "ibc.core.client.v1.MsgCreateClient": None,
    "cosmos.slashing.v1beta1.MsgUnjail": None,
    "cosmos.staking.v1beta1.MsgEditValidator": None,
    "cosmos.staking.v1beta1.MsgCreateValidator": None,
    "cosmwasm.wasm.v1.MsgStoreCode": None, # already ignored right?
    "ibc.core.client.v1.MsgUpdateClient": None,
    "cosmos.gov.v1beta1.MsgSubmitProposal": None,
    "cosmos.gov.v1beta1.MsgDeposit": None,
}

def get_block_data(height):
    global TOTAL_JUNO_TXS, data    
    block = get_block(height)    

    if block == -2: # height too low
        return
    if block == -1: # error getting block
        return

    get_time = block["header"]["time"]
    txs = block["data"]["txs"]
    num_txs = len(txs)
    # print(f"Block {height} has {num_txs} transactions. Time: {get_time}")

    # loop through txs, and decode base64
    TOTAL_JUNO_TXS += num_txs

    human_txs = []    
    for tx in txs:        
        try:
            tx_json = json.loads(run_cmd(f"junod tx decode {tx} --output json"))            
            messages = tx_json['body']["messages"]            
            for msg in messages:                                 
                if msg["@type"][1:] in IGNORED_MESSAGES.keys(): # skip these
                    continue
                human_txs.append(msg)          
        except:
            # argument list too long = store code
            # input(f"Error decoding tx {tx}. {e}")            
            pass   
    
    data[height] = {
        "time": get_time,
        "num_txs": num_txs,        
        "decoded_txs": human_txs, # does this work?
    }

    if height % HEIGHT_DATA_GROUPINGS == 0:
        print(f"[{height}] Total Juno: {TOTAL_JUNO_TXS}")


# == RPC Logic ==
def get_latest_height():    
    resp = client.get(f"{RPC}/abci_info")    
    height = int(resp.json()["result"]["response"]["last_block_height"])
    # round height down to nearest 100 for sake of file formatting
    height = height - (height % 100)
    return height

def get_block(height) -> int:
    if height < LOWEST_HEIGHT:
        # print("Height too low")
        return -2

    try:
        resp = client.get(f"{RPC}/block?height={height}")        
        return resp.json()["result"]["block"]
    except Exception as e:
        # print(f"Error getting block {height}")
        # print(f"Error getting block {height}. {e}")
        return -1


if __name__ == "__main__":
    main()
