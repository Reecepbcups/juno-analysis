'''
Makes commands since python has GIL bleh
'''

import os
from dotenv import load_dotenv
load_dotenv()

lowest_height = int(os.getenv("LOWEST_BLOCK_HEIGHT"))
end_height = int(os.getenv("END_BLOCK_HEIGHT"))
spread = int(os.getenv("HEIGHT_DATA_GROUPINGS", 500))

# loop between start and end height and make the commands
output = []
for height in range(end_height, lowest_height-1, -spread):
    # print(f"python3 main.py {height} {spread}")    
    # output.append(f"python3 main.py {height} {spread} &")
    # if height - spread < end_height:
    #     spread = height - end_height

    if height - spread < lowest_height:
        spread = height - lowest_height

    if spread == 0:
        continue

    output.append(f"python3 main.py {height} {spread} &") # kill python3 to stop since httpx & background

# save output to txt file in this dir
with open("commands.sh", "w") as f:
    f.write("\n".join(output))

print("\n\nNow Run `sh commands.sh` (This will take a while)")