from aml.data_access.transaction_data import TransactionData

from dotenv import load_dotenv
from aml.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from aml.logger import logging
load_dotenv()
import os
if __name__=='__main__':
    labled_data_file_path = "data/labled_data.csv"

    sd = TransactionData()
    if DATA_INGESTION_COLLECTION_NAME in sd.mongo_client.database.list_collection_names():
        sd.mongo_client.database[DATA_INGESTION_COLLECTION_NAME].drop()
    sd.save_csv_file(file_path=labled_data_file_path,collection_name=DATA_INGESTION_COLLECTION_NAME)


