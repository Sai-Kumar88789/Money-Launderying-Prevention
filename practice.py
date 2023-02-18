from typing import List
import pandas as pd
import os
import json
import csv
import yaml
import ast
from dotenv import load_dotenv
from aml.utils.main_utils import read_yaml_file
load_dotenv()
def get_requirements():
    file = open('requirements.txt','r')
    req_list:List[str] = file.readlines()
    for idx, lib  in enumerate(req_list):
        req_list[idx] = lib.replace('\n','')

    return req_list

def write_schema_file(file_path_source,file_path_destination):
    data = pd.read_csv(file_path_source)
    column_types = data.dtypes.tolist()
    change_type = [str(i).replace('float64','float').replace('int64','int').replace('object','text') for i in column_types ]
    columns_with_datatype = []
    for idx,col in enumerate(data.columns):
        di ={}
        di[col] = change_type[idx]
        columns_with_datatype.append(di)
    content_dict = {}
    numerical_columns = []
    content_dict["columns"] = columns_with_datatype
    for d in columns_with_datatype:
        for key,val in d.items():
            if val=='int' or val =="float":
                numerical_columns.append(key)
    content_dict['numerical_columns']= numerical_columns

    with open(file_path_destination, 'w') as file:
        yaml.dump(content_dict, file)

        

