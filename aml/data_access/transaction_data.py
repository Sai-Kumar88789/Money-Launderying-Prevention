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
    def save_csv_file(self,file_path ,collection_name: str,database_name: Optional[str] = None):
        try:
            data_frame=pd.read_csv(file_path)
            data_frame.reset_index(drop=True, inplace=True)
            records = list(json.loads(data_frame.T.to_json()).values())
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection_name]
            collection.insert_many(records)
            return len(records)
        except Exception as e:
            raise AMLException(e, sys)

    def export_collection_as_dataframe(self,collection_name: str, database_name: Optional[str] = None) -> pd.DataFrame:
        try:

            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection_name]
            df = pd.DataFrame(list(collection.find()))

            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)

            # df.replace({"na": np.nan}, inplace=True)

            return df
        
        except Exception as e:
            raise AMLException(e, sys)