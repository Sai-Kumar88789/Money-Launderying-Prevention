from aml.data_access.transaction_data import TransactionData
from aml.constant.database import EDGELIST_COLLECTION_NAME, FEATURE_COLLECTION_NAME, CLASSES_COLLECTION_NAME
from dotenv import load_dotenv
load_dotenv()
import os
if __name__=='__main__':
    features_file_path ="elliptic_bitcoin_dataset/elliptic_txs_features.csv"
    edgelist_file_path ="elliptic_bitcoin_dataset/elliptic_txs_edgelist.csv"
    classes_file_path  ="elliptic_bitcoin_dataset/elliptic_txs_classes.csv"
    print(os.environ['MONGODB_URL'])
    sd = TransactionData()
    if EDGELIST_COLLECTION_NAME in sd.mongo_client.database.list_collection_names():
        sd.mongo_client.database[EDGELIST_COLLECTION_NAME].drop()
    sd.save_csv_file(file_path=edgelist_file_path,collection_name=EDGELIST_COLLECTION_NAME)

    if CLASSES_COLLECTION_NAME in sd.mongo_client.database.list_collection_names():
        sd.mongo_client.database[CLASSES_COLLECTION_NAME].drop()
    sd.save_csv_file(file_path=classes_file_path,collection_name=CLASSES_COLLECTION_NAME)

    if FEATURE_COLLECTION_NAME in sd.mongo_client.database.list_collection_names():
        sd.mongo_client.database[FEATURE_COLLECTION_NAME].drop()
    sd.save_csv_file(file_path=features_file_path,collection_name=FEATURE_COLLECTION_NAME)

    print('Successfully imported!')


