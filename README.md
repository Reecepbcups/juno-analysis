# DEPRECATED
My indexer now handles this MUCH better <https://github.com/Reecepbcups/cosmos-indexer>

---

## Juno Tx Analysis
Saves every Tx as JSON for future processing of the data by height, and message data.

[Example Post](https://twitter.com/Reecepbcups_/status/1571109060963078145?s=20&t=5fPdMu3FWXoCg_qHOT3pEw)

In the future, you can cross-compare data between different networks.

### Solution:
- Use RPC / REST to query every block.
- Saves every XXXX blocks to a JSON file with the data we want, using height as the key. Forked processes for speed
- Combine all into all_data file and graph it / sort
- Loop through given data sets with what ever logic we want :)


### How To Run:
```bash
cp .env.example .env # then edit

pip install -r requirements/requirements.txt

# STEP 1
# This is a temp link, I need to buy a dedi machine for long term
wget http://95.217.113.126/juno_data_backup.zip -O juno_data_backup.zip
unzip juno_data_backup.zip # This will create a data/ folder for heights

# OR if the above link doesn't work, do the next 2 commands and/or contact Reece#3370
python3 step1_make_commands.py # generates commands to run forked main's for (batching Height groups)
sh commands.sh # to run the forked processes (With junod tx decode, this takes ~4 hours for 500k blocks on a Ryzen 5 3600 Hetzner)

# After you have a data/ folder, you can process the heights -> sorted files with 2 and 3
python3 step2.py # combines all the data/ into 1 large file
python3 step3.py # combines all the data.json -> sorted sub files, name = file type

# steps 4+ are logic using the data and comparing.
```


### Future todo
- Bring proto decoding into here, sys calls too expensive. Forking is just fine
- Easy backup all msgs -> nginx server for others to easily download compressed version of already decoded msg JSON
- More Networks
- Make more OOP based for commonly used functions, like loading all the msgs into 1 dict
