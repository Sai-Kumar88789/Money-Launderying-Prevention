from typing import List
import pandas as pd
import os
import json
import csv
import yaml
import ast
from dotenv import load_dotenv
from scipy.stats import ks_2samp
from aml.utils.main_utils import read_yaml_file
from aml.constant import training_pipeline
from aml.exception import AMLException
import sys

# load_dotenv()
# data = training_pipeline.SCHEMA_FILE_PATH
# print(data)
# def read_yaml_file(file_path: str) -> dict:
#     try:
#         with open(file_path, "rb") as yaml_file:
#             return yaml.safe_load(yaml_file)
#     except Exception as e:
#         raise AMLException(e, sys) from e
# print(read_yaml_file(data))
# # def write_schema_file(file_path_source,file_path_destination):
#     data = pd.read_csv(file_path_source)
#     column_types = data.dtypes.tolist()
#     change_type = [str(i).replace('float64','float').replace('int64','int').replace('object','text') for i in column_types ]
#     columns_with_datatype = []
#     for idx,col in enumerate(data.columns):
#         di ={}
#         di[col] = change_type[idx]
#         columns_with_datatype.append(di)
#     content_dict = {}
#     numerical_columns = []
#     content_dict["columns"] = columns_with_datatype
#     for d in columns_with_datatype:
#         for key,val in d.items():
#             if val=='int' or val =="float":
#                 numerical_columns.append(key)
#     content_dict['numerical_columns']= numerical_columns

#     with open(file_path_destination, 'w') as file:
#         yaml.dump(content_dict, file)

        
class TargetValueMapping:
    def __init__(self):
        self.mapping = {'2.0': 0, '1.0': 1}

    def to_dict(self):
        return self.mapping

    def reverse_mapping(self):
        return {value : key for key, value in self.mapping.items()}

# Create an instance of the TargetValueMapping class
mapping = TargetValueMapping()

# Call the to_dict() method to get the mapping dictionary
mapping_dict = mapping.to_dict()

# Call the reverse_mapping() method to get the reversed dictionary
reversed_dict = mapping.reverse_mapping()

# Print both dictionaries
print(mapping_dict)
# print(reversed_dict)



