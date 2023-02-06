from typing import List
import pandas as pd
import os
import json
import csv
from dotenv import load_dotenv
load_dotenv()
def get_requirements():
    file = open('requirements.txt','r')
    req_list:List[str] = file.readlines()
    for idx, lib  in enumerate(req_list):
        req_list[idx] = lib.replace('\n','')

    return req_list
# csvFile = open(os.getenv("EXPORT_EDGELIST_PATH"), 'r')
# header = csvFile.readlines()[0].split(',')
# header[-1]= header[-1].replace('\n','')
# reader = csv.DictReader(csvFile)

data = pd.read_csv("elliptic_bitcoin_dataset/elliptic_txs_classes.csv")
print(data.head())


