'''
Gets info about what kinds of messages are used for Execute Msg on Juno
'''

import base64
import json
import os
import requests

import matplotlib.pyplot as plt
from prettytable import PrettyTable

IGNORE_JUNOSWAP = True
IGNORE_AIRDROP = True # if airdrop in label, ignore
IGNORE_LP_TOKEN = True # WasmSwap -> lp_token ex: juno1s4rn507yhlqw8p7haqpmd3uuvttehact7acsgd9s94pvnkw78t4smkuacv
IGNORE_GOV_TOKENS = True # if the token has "gov" in it
# JunoSwap addresses to ignore (CW20, pool swap, rewards). From `scripts/get_junoswap_addrs.py`
JUNOSWAP_ADDRS = ['juno1jk7kz2xd880ew9gel2xjh6ucpterflg6jkjymd2636kc9fnqku6qf3ajq0', 'juno124d0zymrkdxv72ccyuqrquur8dkesmxmx2unfn7dej95yqx5yn8s70x3yj', 'juno1clh29453aa9tndsjty7ejvc8m838nh3dn2t34k6wkl5pjnh5lxsqvs5qr5', 'juno125rv72jrlxr5qslt8n6vrefm4es4kq0vmm4ffnvc8rvf46tp0j7qw7thfl', 'juno15u3dt79t6sxxa3x3kpkhzsy56edaa5a66wvt3kxmukqjz2sx0hes5sn38g', 'juno1ehnmjq4232yxh7t2xfkjfqkeddsflcc4z5xd2f7lfcms904szf4skk7pju', 'juno1ddulcgq7hjwal3jjx9n33x9rr0xf5j0p3je0j4kytt4uyrnk0uhq0ehcyh', 'juno1sg6chmktuhyj4lsrxrrdflem7gsnk4ejv6zkcc4d3vcqulzp55wsf4l4gl', 'juno10h94gypnj05uwvskmpq9dqan5asu07p5g424hr0jgu0m4m9j06ks6wqzhn', 'juno1r48lst84vsh8jyshqmva58znvyr59w2aejht3gkuy4ex3yd9hlzsmwp349', 'juno1cuu9qxjqukh9drptk2y50r5tvepes7cy55hffh7quvvawk95lxlq6rzzj0', 'juno1ctsmp54v79x7ea970zejlyws50cj9pkrmw49x46085fn80znjmpqz2n642', 'juno13nqp4zaryv0psnjlzdmwah4nl8fdwy9qev34kv42yp7pu4457cwquu0w6t', 'juno15sfz9cz97uj38uc9nhuchjwcj638xkt4y5k909tq8ag5dkt8ys5qh0sjwj', 'juno1hue3dnrtgf9ly2frnnvf8z5u7e224ctc4hk7wks2xumeu3arj6rs9vgzec', 'juno1j7pdtemw0qvl6rmnl0sf324409gz2p4sdt6rv659482x9rqqz6mqd653dg', 'juno10mrlcttkwt99wxnqfyk6327lq3ac9yhfle2fd0c5s4rp8dzqy9ps3sjzyf', 'juno1yqum3uy7jx60qarnputjzn6fewmlwc8flvzs6q0raw7ec6l4p00qwytzcs', 'juno1el6rfmz6h9pwpdlf6k2qf4dwt3y5wqd7k3xpyvytklsnkt9uv2aqe8aq4v', 'juno1zggudwdt32t6qva3a3jqg47nlz69n39ru5u7vsmvq4kyj2nr50nsv67thv', 'juno1z5vukf037r6acgln3n37tr8a5rv7wafqzhcq29ddn9etwwtfrytsn6xvux', 'juno1730cx75d8uevqvrkcwxpy9trhqqfksu5u9xwqss0qe4tn7x0tt3shakhk8', 'juno1tmxx3rdnnrcckkh7pjde924lftjs724rzd44sqte5xh8xax0yf2sc7v7dk', 'juno1yaff0t6tfheqcdep24euu7w0xhnhs2yjwwv7r2c280vlns8trghq5d72pd', 'juno152lfpmadpxh2xha5wmlh2np5rj8fuy06sk72j55v686wd4q4c9jsvwj0gm', 'juno1gpa5ardzal22el6czj4j0d2pwy0m9qj06lr20t2l8fca3gkws63qfnx8eq', 'juno1hkz5dhn59w6l29k8w8ceuramqx2f35qpen7xtlx6ezketwh8ndxq8rwq2a', 'juno12sulrvp220gpsp8jsr7dpk9sdydhe8plasltftc6fnxl7yukh24qjvqcu9', 'juno1e8n6ch7msks487ecznyeagmzd5ml2pq9tgedqt2u63vra0q0r9mqrjy6ys', 'juno1s43j4ct4tp3s5ywk0j4flr6e5ev74ce2lnuv8xwtzx2yfr6kmwaqmxfkdt', 'juno1acs6q36t6qje5k82h5g74plr258y2q90cjf9z4wnktt7caln0mhsx8mt7z', 'juno133xa84qnue3uy0mj9emvauddxzw554rfl9rr6eadhfau50ws7gvs4ynm79', 'juno16zn96yf3vnxengke3vcf6mg9x7qyppgsdh3dnnmvdd8hvtpw58wsrjuu56', 'juno1gv2gswtan8wsk54h663waefffywnuc9wcxr7xl5pnnxvjaqunpgs20t39g', 'juno1653nhx2330rnhmzk2qe9w74kwwa3jtxe4lrfs5cfq8szfms8pqzsra5fvq', 'juno1z698dxy9gj4fnrs76xwmtqwh84lamav9xl0w35pd35vnfx7987nqudxyge', 'juno18nflutunkth2smnh257sxtxn9p5tq6632kqgsw6h0c02wzpnq9rq927heu', 'juno1asuge3uue74s0rzjvrptgeq2jn5kgv098lh33a8k2nwchct2uk6szn5a9u', 'juno1m08vn7klzxh9tmqwajuux202xms2qz3uckle7zvtturcq7vk2yaqpcwxlz', 'juno19t4w2zwaxf2wxwcp4hphwdvjmwun369h5ffw9gsvn9wllzct9j5qwescus', 'juno1r4pzw8f9z0sypct5l9j906d47z998ulwvhvqe5xdwgy8wf84583sxwh0pa', 'juno1uhu0nuyz6wqx0h5564nx05fsgfh8jdh5qy3gj4nask3n9ehxn5cs2d9rsy', 'juno1cvjuc66rdg34guugmxpz6w59rw6ghrun5m33z3hpvx6q60f40knqglhzzx', 'juno14nak8v6xeawstrq7r7qmpa67qqfc9xzzymfdfpnp0luycv8knyuq5a6w2m', 'juno1enl842z00cklnathpv8f3t3w2u70dkrq22crz3gxg38we7xjfq5s8lktmg', 'juno14p3wvpeezqueenfu9jy29s96xuk0hp38k5d5k4ysyzk789v032sqp8uvh3', 'juno1fzl79pekf8wtd0y37q92dmz5h9dxtfpl97w3kguyc59m7ufnlzvsf46vf8', 'juno19859m5x8kgepwafc3h0n36kz545ngc2vlqnqxx7gx3t2kguv6fws93cu25', 'juno1xkm8tmm7jlqdh8kua9y7wst8fwcxpdnk6gglndfckj6rsjg4xc5q8aaawn', 'juno1fpphzkkq5uyezm7amk6sslyz8r94wl658zg2ku47v8mtslueyx5q29rkzq', 'juno1w7l7hetsm4x6hxa55dsjwszqh9elzwqrd6cud2qkqhafrd6u9vrqc2zh48', 'juno15y0xjc6f25f3whu92d2zppl5fws994r9xhs555sxzn7x43rq8vwqhcsxs5', 'juno1jz50fj5zkcv3h6hmcfr3nr6eer7rj5pmsry5qj5jc8rfvpeavyzsgknm83', 'juno17maxguaz574lxzkggfqwwsxrl335f4rzp6t3lpajxmzxl68urz6qek2zda', 'juno14lycavan8gvpjn97aapzvwmsj8kyrvf644p05r0hu79namyj3ens87650k', 'juno1rft4xp5e6ffta5a8aqwtu4kgdfjqw4jhnleu8agmmedzrxsat7pqxfgfrs', 'juno1sfs7tqehejtz3u65h4cwdkel3qp369thdfu39qhgk4g7nnz7g4esnvaeen', 'juno17h4sgpaksygdnswpx74szv98hggddc08ny4zv5ca63jv53qptxrshacvku', 'juno1gt0w9yyxasc6acje7q4rnwvpwpdmk4sg65mfm2cusmtkwv4mwjas47nk4p', 'juno1qsmywlded2sdggud5wft44gq2u6c3epl3qhzr4qv7psj536t8yhsfvrcf6', 'juno1fneqh5xvv6az0e7mxad78wqtsnzs4hlyuqapkn30sff6plgrnausa0un2v', 'juno150vj5jusg4g8n82q40nd9cmq3unc255u3hf5qh6pud4dexkgyp0ss7yvwq', 'juno15vu0n3rvpzdprzerqualvdag6xw6c2rj2dmjpvheykzmx7jja82qzyl7cc', 'juno13926947pmrjly5p9hf5juey65c6rget0gqrnx3us3r6pvnpf4hwqm8mchy', 'juno14xzzfld96htg7f4rwezlak7tcrhu6838q2l2tspefnfts99wukrqs9e6lc', 'juno1cugrrrryrpl383kfca0w5swywffa08zwqshrsfre82059vxjlx6syhf73y', 'juno1wrczl2fmpd2cgdnqrd8xlytadqmfsy8x750rdked2r236sg29jus5x74zq', 'juno1j0a9ymgngasfn3l5me8qpd53l5zlm9wurfdk7r65s5mg6tkxal3qpgf5se', 'juno1x9hta758ddr6swfcl7rangnmsjpn5ewuqj3kxfamfm6v4yv948pque0dv3', 'juno1gz8cf86zr4vw9cjcyyv432vgdaecvr9n254d3uwwkx9rermekddsxzageh', 'juno1wstya996rl4fpgdmekj42t0xd0lj8k4rwlzt5lapa6cdu9daz2fqphua88', 'juno15exy530csjch68unw3zdncgyyymwnufx6mmfu9sjzcfsafa9utsqhf94y4', 'juno1fha0ux5k6xxzzknhwk0j2rtwxtczlp8kzk6w9g383lzjhu337k9swvjdlv', 'juno1jsykneh8hhdxztz5vxmnvgs9yl4qhrfua9huw9w0xfcsw9ma2m8sxr8xmq', 'juno19rqljkh95gh40s7qdx40ksx3zq5tm4qsmsrdz9smw668x9zdr3lqtg33mf', 'juno174el7090aahaug8lgd9w52x6kedv3jsna2rtzxnrwylf2aua4yqssfwmxy', 'juno1ahm693l08esz4a99jz4nvkpsa2w6l3um55znumjvuclksfsdeyhsa7ra2w', 'juno1gxvcltkl0tf20rpsn2wf9q6ex0vr5xk6j3tzezuv6yyjez97w5vqmxk0cv', 'juno1pdd5dz2p36t05rgc67j25fnm0yfg4jhhl3sh4zfykcdrs0jthprssy90ve', 'juno1h824nt965e5psjjlk5pg3nmsxj5g3k4flgdgw75x3u5mlr84ef6sf2nfms', 'juno1maj5xlggctfwm6ct6x2e3456zxm8chadq9prqxl9kjxzzs9edalsk5wzwh', 'juno13jaullyjmhpg0zm86s50hfjjys3275rmcm52h3euxcdd8deqdnyqj30sc4', 'juno17v2d2993me50e6dgzx50ckuuah0vmfyanl0segxsdcg3s4qzqersyrvu8n', 'juno19dn05lxpuhqg0zl28yalvsu5f9vun0xwuf2vfh8pupdkuerhn90syzyfzy', 'juno15gezc5ra6uwxkygfa672cqe3vf4u3pd5wgdc64tsaf9660wtl5ssp3cp2x', 'juno1d04vn4t3cw494md0xleyqk6hxt8ctn5gmr353h06uvnudlvk5chq93vmjq', 'juno1jcjh9yu9275ltp52r5nv5uze2347mq9fy48d87fn9a079xel56cqt96upl', 'juno1vujvwn7m9ekdshg678k2arg0s7a32z4wgppj39965gervwrzmeuqpejyw0', 'juno14hrt7htv42234xwpsxmxaxu7wywak7zflpk9jf5nze3w6e93czdsfwe0ly', 'juno1ruaj63w8jlgunjdr9tvc7d2rehnkxknerf33f536nhtl0222nj4swfwvdk', 'juno1qt7uzjg9su3mk78jpt695rmxce4sa7evz7wa0edexjrsxghy35hsgje5l9', 'juno19qswdr73m7u5l6vmxyr86emlfugpd0jlmpsu7n9zexkt5x80g2vq4gx0e8', 'juno107l74mj5q7d6zdzqzwpmdkk76628az2p9z08z9cj5pa7s5fpucws96f57e', 'juno1zkf802n7j2npye49napwpzrdt2n5yx7e9n04q8fh3tudgx98tf5q9h9n43', 'juno1p8x807f6h222ur0vssqy3qk6mcpa40gw2pchquz5atl935t7kvyq894ne3', 'juno19yv0nw00fzs30p0hhgm967fwy5e9ntzxspct4mjw7v7czg8pum9sp0hpz7', 'juno1fjmrqc5tjj2t5mfwkk5utwz2t0gcpkfajjefllrfahuqanctn9ys968emr', 'juno1724y4ur5xarup9mcm9lw3jzyec0ujhrhlet62a54sw0hjmhq5y4sr3zrft', 'juno147t4fd3tny6hws6rha9xs5gah9qa6g7hrjv9tuvv6ce6m25sy39sq6yv52', 'juno1na8zlnp3pqsjfzllcncq2ahsxg9zkdkqrz3sl4ae5lergh2wrjes7jl9gr', 'juno1pxn38k3kz9k8cjlrghdwzmkxz67l343k5xuxn744wa56vfddrepsx72j5x']
JUNOSWAP_ADDRS = set(JUNOSWAP_ADDRS)

# BLOCK spammer (124k msgs)
IGNORE_USER_ADDRESSES = set(['juno14wh3tl6ygjrydwd5j5mjtmqsttqz46s83hh5xq'])

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
label_cache = {}
cache_contracts_file = f"{extra_data}/cache_contrac_labels.json"
for msg in msgexec: # dict_keys(['@type', 'sender', 'contract', 'msg', 'funds', 'height'])            
    contract = msg['contract']
    sender = msg['sender']
    funds = msg['funds']

    try:
        msg_data = dict(msg['msg'])

        if IGNORE_JUNOSWAP == True and contract in JUNOSWAP_ADDRS: continue

        # setup
        if contract not in all:
            # save contract_details to a extra_data/contract_label.json file                                                
            if len(label_cache.keys()) == 0 and os.path.exists(cache_contracts_file):
                with open(cache_contracts_file, "r") as f:
                    label_cache = json.load(f)

            if contract in label_cache:                
                contract_details = label_cache[contract]
            else:
                # https://github.com/CosmWasm/wasmd/blob/main/x/wasm/client/rest/query.go
                # https://api.mintscan.io/v1/juno/wasm/contracts/juno15u3dt79t6sxxa3x3kpkhzsy56edaa5a66wvt3kxmukqjz2sx0hes5sn38g
                CONTRACT_INFO_API = f"{REST_URL}/wasm/contract/{contract}"        
                contract_details = requests.get(CONTRACT_INFO_API, headers={"Content-Type": "application/json",}).json()                
                label_cache[contract] = contract_details['result']["label"] if 'result' in contract_details.keys() else "Unknown"
                # print(f"{contract=}, {label_cache[contract]=}")
                # label_cache[contract] = "testingreece"
                                 

            label = str(label_cache[contract])

            if IGNORE_AIRDROP == True and "airdrop" in label.lower():
                # print(f"Skipping airdrop contract: {contract}")
                continue

            if IGNORE_LP_TOKEN == True and "lp_token" in label.lower():
                # print(f"Skipping lp_token contract: {contract}")
                continue

            if IGNORE_GOV_TOKENS == True and "gov" in label.lower():
                # print(f"Skipping gov contract: {contract}")
                continue

            # print(contract, label)

            all[contract] = {
                "label": label,
                "unique_wallet_interactions": 0,
                "total_number_of_calls": 0,                          
            }

        if contract not in unique_interactions:
            unique_interactions[contract] = {}

        if sender in IGNORE_USER_ADDRESSES: continue

        # total number of calls
        all[contract]["total_number_of_calls"] += 1

        # times called
        if sender not in unique_interactions[contract]:
            unique_interactions[contract][sender] = 1
        else:
            unique_interactions[contract][sender] += 1   

    except Exception as e:
        print(e)

# dump cache_contracts_file
with open(cache_contracts_file, "w") as f:
    json.dump(label_cache, f)

print("Unique wallet saving :D")
for contract in unique_interactions:
    all[contract]["unique_wallet_interactions"] = len(unique_interactions[contract].keys())
    # print(msg)
    
def pie_chart(sorted_all: dict, filename: str, title = "my title"):
    PERCENT = 0.02 # top X% of contracts only shown
    pie_chart = {
        "labels": [],
        "sizes": [],        
        "explode": [],        
    }

    total_contracts = len(sorted_all.keys())
    print(f"{total_contracts=}")

    for idx, contract in enumerate(sorted_all):                
        if idx > total_contracts * PERCENT: # only top X% of contracts are saved
            break

        pie_chart["labels"].append(sorted_all[contract]["label"])
        pie_chart["sizes"].append(sorted_all[contract]["total_number_of_calls"])        
        pie_chart["explode"].append(0.1)

    fig, ax = plt.subplots()
    plt.rcParams.update({'font.size': 12})
    ax.pie(pie_chart["sizes"], explode=pie_chart["explode"], labels=pie_chart["labels"], autopct='%1.1f%%', shadow=True, startangle=90)
    ax.axis('auto')
    # add padding to width
    fig.set_size_inches(15, 10)    
    
    plt.title(title, fontsize=20, fontweight='bold')

    # shift graph to the left to make room for legend
    # plt.subplots_adjust(left=0.0, bottom=0.1, right=0.9)

    # make the actual plot smaller
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])


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
#  unique_interactions
# with open(f"{extra_data}/unique_interactions-executes.json", "w") as f:
#     json.dump(unique_interactions, f, indent=4)

with open(f"{extra_data}/unique_contract_info-no_jswap.json", "w") as f:
    # sort all as a dict by unique_wallet_interactions
    sorted_all = {k: v for k, v in sorted(all.items(), key=lambda item: item[1]['unique_wallet_interactions'], reverse=True)}
    json.dump(sorted_all, f, indent=4)
    pie_chart(sorted_all, "unique_contract_info-noswap-uniquewallets.png", "No JSwap, Unique Wallets per dAPP")
    # bar_chart(sorted_all, "unique_contract_info-noswap-uniquewallets-bar.png")


with open(f"{extra_data}/unique_contract_info-sorted-by-total-calls-ignore_jswap.json", "w") as f:    
    # sort all as a dict by unique_wallet_interactions
    sorted_all = {k: v for k, v in sorted(all.items(), key=lambda item: item[1]['total_number_of_calls'], reverse=True)}
    json.dump(sorted_all, f, indent=4)
    pie_chart(sorted_all, "unique_contract_info-noswap-totalcalls.png", "No JSwap, Total Calls per dAPP")
    # bar_chart(sorted_all, "unique_contract_info-noswap-totalcalls-bar.png")

    # save sorted_all to a pie chart with matplotlib
    # https://matplotlib.org/stable/gallery/pie_and_polar_charts/pie_features.html

# sorted_all = {k: v for k, v in sorted(all.items(), key=lambda item: item[1]['total_number_of_calls'], reverse=True)}
# pie_chart(sorted_all, "unique_contract_info-sorted-by-total-calls-5%.png")

# sorted_all = {k: v for k, v in sorted(all.items(), key=lambda item: item[1]['unique_wallet_interactions'], reverse=True)}
# pie_chart(sorted_all, "unique_contract_info-sorted-by-total-calls-unique-wallets-5%.png")

