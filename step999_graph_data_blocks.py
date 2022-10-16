# WIP

import os
import json

import matplotlib.pyplot as plt

current_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(current_dir, "all_data.json"), 'r') as f:
    all_data = dict(json.load(f))


heights = []
num_txs = []

# for k, v in all_data.items():
#     heights.append(k)
#     num_txs.append(v['num_txs'])

lowest = 4444500 # lowest block we could get
highest = 4845000 # latest height from commands.sh

# find the difference
# diff = highest - lowest


rac_values = {k: 0 for k in range(lowest, highest+1, 5_000)}
juno_values = {k: 0 for k in range(lowest, highest+1, 5_000)}

for k, v in all_data.items():
    # find the closest key to k
    closest = min(rac_values, key=lambda x:abs(x-int(k)))
    # print(closest)

    # add the value to the closest key
    rac_values[closest] = rac_values.get(closest, 0) + v['rac_txs']
    juno_values[closest] = juno_values.get(closest, 0) + v['num_txs']


# print(len(rac_values))

# plt.plot(heights, num_txs)
plt.plot(rac_values.keys(), rac_values.values())
plt.title('Racoon Txs Over Time')
plt.xlabel('Block height')
plt.ylabel('Txs Over Time')
# plt.show()
plt.savefig('rac_txs_over_time.png')

plt.plot(juno_values.keys(), juno_values.values())
plt.title('Juno Txs Over Time w/ Rac Overlay')
plt.xlabel('Block height')
plt.ylabel('Txs Over Time')
# plt.show()
plt.savefig('juno_txs_over_time_with_overlay.png')

# clear plot
plt.clf()


# plot just juno
plt.plot(juno_values.keys(), juno_values.values())
plt.title('Juno Standalone Txs over time')
plt.xlabel('Block height')
plt.ylabel('Txs Over Time')
# plt.show()
plt.savefig('juno_txs_standalone.png')