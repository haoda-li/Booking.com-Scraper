from ast import literal_eval
import json
from os import listdir
import pandas as pd

def save_raw_listing_info(folder_in, folder_out):
    files = listdir(folder_in)

    all_info = []
    for f in files:
        if "json" not in f or "info" not in f:
            continue
        with open(folder_in + f, "r") as f:
            all_info += json.load(f)
    with open(folder_out + "INFO.json", "w") as f:
        json.dump(all_info, f, indent=2)
    attributes = list(all_info[0].keys())
    attributes.remove("room_types")
    df_dict = {}
    for attr in attributes:
        df_dict[attr] = []
    for info in all_info:
        for attr in attributes:
            df_dict[attr].append(info[attr])
    pd.DataFrame(df_dict).to_csv(folder_out + "/INFO.csv", index=False)
    
def save_raw_avalibility(folder_in, folder_out, date_in, date_out):
    all_b = [folder_in + e for e in listdir(folder_in) if date_in in e]
    collect = []
    for file in all_b:
        f = open(file, "r")
        collect += json.load(f)
    with open(folder_out + "AVALIBILITY"+date_in.replace("-","")+"_"+date_out.replace("-","")+".json", "w") as f:
        json.dump(collect, f, indent=2)
