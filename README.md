## Juno Transaction Counter
(Since block)
Counting the number of Txs per block for the RAC community.

[Twitter Post](https://twitter.com/Reecepbcups_/status/1571109060963078145?s=20&t=5fPdMu3FWXoCg_qHOT3pEw)

Solution:
- Use RPC / REST to query every block.
- Saves every XXXXX blocks to a JSON file with the data we want, using height as the key.
- Set of contract addresses that are Rac based (from their games). If it is one, we count it.
- save each height to its own grouped JSON file.
- Combine all into all_data file and graph it

Todo:
- save all blocks & txs to files then combine to be nice to RPC endpoints (future)
- Keep a running record of all Txs via JSON (Full node essentially) with all base64 data saved from earliest block height I can get
Other:
- Fix httpx timeout errors (2,000 blocks affected)
- Ensure the last command can't return blocks < minimum height required (despite spread)


How To Run:
- `python3 make_commands.py` will generate commands.sh for you (Linux only)
- `sh commands.sh` to run the forked processes (This will take a big)
- `python3 get_all_data_info.py` merges all the data/ files into 1 massive file all_data.json
- `graph_data_blocks.py` graph all data into matplot lib, and save to file (relative path)