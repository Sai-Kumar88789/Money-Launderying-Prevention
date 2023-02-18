from aml.constant.database import DATABASE_NAME
from typing import Optional
import sys,json,os,csv
import pandas as pd
import ast
import numpy as np
from aml.exception import AMLException
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from dotenv import load_dotenv
load_dotenv()

class TransactionData:
    """
    This class help to export entire mongo db record as pandas dataframe
    """
    def __init__(self):
        """
        Connecting to Cassandra database
        """
        try:
            cloud_config= {
            'secure_connect_bundle': os.getenv("SECURE_CONNECT_FILE")
            }
            auth_provider = PlainTextAuthProvider(os.getenv('CLIENT_ID'), os.getenv('CLIENT_SECRET'))
            self.cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
            self.session = self.cluster.connect()

        except Exception as e:
            raise AMLException(e, sys)
    def save_csv_file(self,file_path ,keyspace_name: str, collection_name: str):
        try:
            data_frame=pd.read_csv(file_path)
            # data_frame.reset_index(drop=True, inplace=True)
            # records = list(json.loads(data_frame.T.to_json()).values())
            # if database_name is None:
            #     collection = self.mongo_client.database[collection_name]
            # else:
            #     collection = self.mongo_client[database_name][collection_name]
            # collection.insert_many(records)
            # return len(records)
            if keyspace_name is None:
                self.session.execute("""
                        CREATE KEYSPACE IF NOT EXISTS test_keyspace
                        WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': 1 }
                         """)
            # create a dynamic sql query for creation and insertion
            column_types = data_frame.dtypes.tolist()
            change_type = [str(i).replace('float64','float').replace('int64','int').replace('object','text') for i in column_types ]
            di = {}
            for idx,col in enumerate(data_frame.columns):
                di[col] = change_type[idx]
            s1 = ""
            s2 = ""
            n = len(di)
            c= 0
            for col,dtyp in di.items():
                if c == 0:
                    s1 += col + " " + dtyp 
                    s2 += col
                elif c==n-1:
                    s1 += ", " + col + " " + dtyp
                    s2 += ", " + col
                else:
                    s1 += ", " + col + " " + dtyp
                    s2 += ", " + col
                c+=1
            s1 = s1 +", PRIMARY KEY ((timestamp) , txid)"
            self.session.execute(f"CREATE TABLE IF NOT EXISTS {keyspace_name}.{collection_name}({s1})")
            # Read data from the CSV file and insert it into the table
            count = 0
            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    count +=1
                    values = tuple([row[col] if type(row[col])==data_frame[col].dtype  or data_frame[col].dtype == 'object' else ast.literal_eval(row[col]) for col in data_frame.columns ])
                    self.session.execute(f"INSERT INTO {keyspace_name}.{collection_name}({s2}) VALUES{values}".format(*values))
                    if count == 5:
                        break
            # Close the connection to the Cassandra cluster
            self.cluster.shutdown()
        except Exception as e:
            raise AMLException(e, sys)

    def export_collection_as_dataframe(
        self, save_file_path:str,keyspace_name: str, collection_name: str,) -> pd.DataFrame:
        try:

            column_names_query = f"SELECT column_name FROM system_schema.columns WHERE keyspace_name = '{keyspace_name}' AND table_name = '{collection_name}'"

            # Execute the query to retrieve the column names
            column_names = [row[0] for row in self.session.execute(column_names_query)]

            # Select data from the table and write it to the CSV file
            rows = self.session.execute(f"SELECT * FROM {keyspace_name}.{collection_name}")
            with open(save_file_path, 'w') as file:
                writer = csv.writer(file)
                writer.writerow(column_names) # Write the header
                for row in rows:
                    writer.writerow(row)

            # Close the connection to the Cassandra cluster
            self.cluster.shutdown()

            data_frame = pd.read_csv(save_file_path)
            return data_frame
        
        except Exception as e:
            raise AMLException(e, sys)