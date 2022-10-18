'''
Goal: Get all addresses which are related to junoswap & print out as a list. 
- Reason: So we can ignore these in the data & see unique dAPPs to the juno network.
'''
from requests import get

asset_list = "https://raw.githubusercontent.com/CosmosContracts/junoswap-asset-list/main/pools_list.json"
# rewards_list = "https://raw.githubusercontent.com/CosmosContracts/junoswap-asset-list/main/rewards_list.json"

IGNORE_CW20_Token       = True # "Gov Token"
IGNORE_Rewards          = True
IGNORE_Staking          = True
IGNORE_PoolSwapAddress  = True # swap_address

def asset_list_contracts() -> list[str]:
    addresses = {}

    data = get(asset_list).json()
    if 'pools' not in data.keys():
        print("Error: pools not in data.keys()")
        return addresses
    
    for pool in data['pools']:        
        staking_address = pool['staking_address']
        if IGNORE_CW20_Token == True and staking_address != "":
            addresses[staking_address] = None

        swap_address = pool['swap_address']
        if IGNORE_PoolSwapAddress == True and swap_address != "":
            addresses[swap_address] = None

        for reward in pool['rewards_tokens']:
            rewards_address = reward['rewards_address']
            if IGNORE_Rewards == True and rewards_address != "":
                addresses[rewards_address] = None

            token_address = reward['token_address'] # CW20 / gov token
            if IGNORE_CW20_Token == True and token_address != "":
                addresses[token_address] = None

            # Do I need to do this double?
            swap_address = reward['swap_address'] # JUNO/RAW Pool
            if IGNORE_PoolSwapAddress == True and swap_address != "":
                addresses[swap_address] = None
        
    return list(addresses.keys())


l = asset_list_contracts()
print(l)